from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qubipy.rpc.rpc_client import QubiPy_RPC
from utils.transaction_builder import TransactionBuilder
from utils.qr_payment import QRPaymentGenerator
import os
from dotenv import load_dotenv
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from utils.dashboard_metrics import DashboardMetricsService
from utils.transaction_tracker import TransactionTracker
from utils.account_manager import (
	AccountManager,
	AccountCreationRequest,
	AccountDetailsRequest,
	AccountBackupRequest,
	AccountRestoreRequest,
	CloudIntegrationRequest
)
from utils.b2b_payment import B2BPaymentService
from utils.uuid_generator import UUIDGenerator
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.debug(f"QUBIC_RPC_URL: {os.getenv('QUBIC_RPC_URL')}")
logger.debug(f"QUBIC_NETWORK: {os.getenv('QUBIC_NETWORK')}")

app = FastAPI(title="RipaPay Backend", description="Qubic Blockchain Integration for RipaPay")

# Configure CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],  # React dev server
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Initialize services
try:
	qubic_client = QubiPy_RPC(
		rpc_url=os.getenv("QUBIC_RPC_URL", "https://api.qubic.li/v1/")
	)
	transaction_builder = TransactionBuilder()
	qr_generator = QRPaymentGenerator()
	dashboard_metrics = DashboardMetricsService(qubic_client)
	transaction_tracker = TransactionTracker(qubic_client)
	account_manager = AccountManager(qubic_client)
	b2b_service = B2BPaymentService(qubic_client)
	uuid_generator = UUIDGenerator()
	logger.debug("Successfully initialized services")
except Exception as e:
	logger.error(f"Failed to initialize: {str(e)}")
	raise

class TransactionRequest(BaseModel):
	from_address: str
	to_address: str
	amount: float
	business_uuid: str

class QRPaymentRequest(BaseModel):
	business_uuid: str
	amount: float
	merchant_name: Optional[str] = None
	reference: Optional[str] = None

class B2BTransferRequest(BaseModel):
	from_business_id: str
	to_business_id: str
	amount: float
	currency: str = "QUBIC"
	memo: Optional[str] = None

class ChainRegistrationRequest(BaseModel):
	chain_name: str
	chain_config: Dict[str, Any]

class BusinessRegistrationRequest(BaseModel):
	business_name: str
	country: str
	legal_entity_type: str
	registration_number: str
	industry_type: str

@app.get("/")
async def root():
	return {"message": "RipaPay API is running"}

@app.get("/health")
async def health_check():
	try:
		loop = asyncio.get_event_loop()
		status = await loop.run_in_executor(None, qubic_client.get_status)
		logger.debug(f"Health check status: {status}")
		return {"status": "healthy", "qubic_status": status}
	except Exception as e:
		logger.error(f"Health check failed: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions")
async def create_transaction(transaction: TransactionRequest):
	try:
		logger.debug(f"Creating transaction: {transaction}")
		result = await transaction_builder.create_payment_transaction(
			from_address=transaction.from_address,
			to_address=transaction.to_address,
			amount=transaction.amount,
			business_uuid=transaction.business_uuid
		)
		logger.debug(f"Transaction result: {result}")
		return result
	except Exception as e:
		logger.error(f"Transaction failed: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/qr/generate")
async def generate_qr_payment(payment: QRPaymentRequest):
	try:
		logger.debug(f"Generating QR code for payment: {payment}")
		payment_data = {
			"business_uuid": payment.business_uuid,
			"amount": payment.amount,
			"merchant_name": payment.merchant_name,
			"reference": payment.reference,
			"timestamp": datetime.utcnow().isoformat()
		}
		qr_result = qr_generator.generate_payment_qr(payment_data)
		logger.debug("QR code generated successfully")
		return qr_result
	except Exception as e:
		logger.error(f"QR code generation failed: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/qr/verify")
async def verify_qr_payment(qr_data: dict, payment_data: dict):
	try:
		logger.debug(f"Verifying QR payment: {qr_data} against {payment_data}")
		is_valid = qr_generator.verify_qr_payment(qr_data, payment_data)
		return {"valid": is_valid}
	except Exception as e:
		logger.error(f"QR payment verification failed: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/wallet/connect")
async def connect_wallet():
	# TODO: Implement Qubic wallet connection logic here
	return {"status": "success", "message": "Wallet connected (placeholder)"}

class WalletBalanceRequest(BaseModel):
	address: str

class WalletTransactionRequest(BaseModel):
	address: str
	limit: Optional[int] = 10
	offset: Optional[int] = 0

class TransactionListRequest(BaseModel):
	address: str
	limit: Optional[int] = 10

class TransactionDetailRequest(BaseModel):
	transaction_id: str

@app.post("/wallet/balance")
async def get_wallet_balance(request: WalletBalanceRequest):
	try:
		logger.debug(f"Getting balance for address: {request.address}")
		# TODO: Implement actual balance fetching using QubiPy
		balance = await qubic_client.get_balance(request.address)
		return {"address": request.address, "balance": balance}
	except Exception as e:
		logger.error(f"Failed to get wallet balance: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/wallet/transactions")
async def get_wallet_transactions(request: WalletTransactionRequest):
	try:
		logger.debug(f"Getting transactions for address: {request.address}")
		# TODO: Implement actual transaction history fetching using QubiPy
		transactions = await qubic_client.get_transactions(
			address=request.address,
			limit=request.limit,
			offset=request.offset
		)
		return {
			"address": request.address,
			"transactions": transactions,
			"total": len(transactions)
		}
	except Exception as e:
		logger.error(f"Failed to get wallet transactions: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/dashboard/metrics/{business_uuid}")
async def get_dashboard_metrics(business_uuid: str):
	try:
		logger.debug(f"Getting dashboard metrics for business: {business_uuid}")
		metrics = await dashboard_metrics.get_key_metrics(business_uuid)
		return metrics
	except Exception as e:
		logger.error(f"Failed to get dashboard metrics: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/dashboard/transactions/{business_uuid}")
async def get_dashboard_transactions(business_uuid: str, limit: int = 10):
	try:
		logger.debug(f"Getting transaction monitoring for business: {business_uuid}")
		transactions = await dashboard_metrics.get_transaction_monitoring(business_uuid, limit)
		return transactions
	except Exception as e:
		logger.error(f"Failed to get transaction monitoring: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/inbound")
async def get_inbound_transactions(request: TransactionListRequest):
	try:
		logger.debug(f"Getting inbound transactions for: {request.address}")
		transactions = await transaction_tracker.get_inbound_transactions(
			request.address,
			request.limit
		)
		return transactions
	except Exception as e:
		logger.error(f"Failed to get inbound transactions: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/outbound")
async def get_outbound_transactions(request: TransactionListRequest):
	try:
		logger.debug(f"Getting outbound transactions for: {request.address}")
		transactions = await transaction_tracker.get_outbound_transactions(
			request.address,
			request.limit
		)
		return transactions
	except Exception as e:
		logger.error(f"Failed to get outbound transactions: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/{transaction_id}")
async def get_transaction_details(transaction_id: str):
	try:
		logger.debug(f"Getting transaction details for: {transaction_id}")
		details = await transaction_tracker.get_transaction_details(transaction_id)
		return details
	except Exception as e:
		logger.error(f"Failed to get transaction details: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/create")
async def create_account(request: AccountCreationRequest):
	try:
		logger.debug("Creating new account")
		account = await account_manager.create_account(request.mnemonic)
		return account
	except Exception as e:
		logger.error(f"Failed to create account: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts/{address}")
async def get_account_details(address: str):
	try:
		logger.debug(f"Getting account details for: {address}")
		details = await account_manager.get_account_details(address)
		return details
	except Exception as e:
		logger.error(f"Failed to get account details: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/backup")
async def backup_account(request: AccountBackupRequest):
	try:
		logger.debug(f"Backing up account: {request.address}")
		backup_result = await account_manager.backup_account(
			request.address,
			request.backup_path
		)
		
		return {
			"status": "success",
			"message": "Account backup completed",
			"backup_details": backup_result,
			"timestamp": datetime.utcnow().isoformat()
		}
	except Exception as e:
		logger.error(f"Failed to backup account: {str(e)}")
		raise HTTPException(
			status_code=500,
			detail=f"Backup failed: {str(e)}"
		)

@app.post("/accounts/restore")
async def restore_account(request: AccountRestoreRequest):
	try:
		logger.debug("Restoring account from backup")
		account = await account_manager.restore_account(request.backup_path)
		
		return {
			"status": "success",
			"message": "Account restored successfully",
			"account_data": account,
			"timestamp": datetime.utcnow().isoformat()
		}
	except Exception as e:
		logger.error(f"Failed to restore account: {str(e)}")
		raise HTTPException(
			status_code=500,
			detail=f"Restore failed: {str(e)}"
		)

@app.post("/accounts/cloud-integration")
async def integrate_with_cloud(request: CloudIntegrationRequest):
	try:
		logger.debug(f"Integrating account with cloud provider: {request.cloud_provider}")
		if request.cloud_provider.lower() != "google_drive":
			raise HTTPException(
				status_code=400,
				detail="Currently only Google Drive is supported as a cloud provider"
			)
		
		success = await account_manager.cloud_integration(
			request.address,
			request.cloud_provider,
			request.credentials
		)
		
		if success:
			return {
				"status": "success",
				"message": "Successfully integrated with Google Drive",
				"provider": request.cloud_provider,
				"address": request.address,
				"timestamp": datetime.utcnow().isoformat()
			}
		else:
			raise HTTPException(
				status_code=400,
				detail="Failed to integrate with Google Drive"
			)
	except Exception as e:
		logger.error(f"Failed to integrate with cloud provider: {str(e)}")
		raise HTTPException(
			status_code=500,
			detail=f"Cloud integration failed: {str(e)}"
		)

@app.post("/b2b/transfer")
async def business_transfer(request: B2BTransferRequest):
	try:
		logger.debug(f"Processing B2B transfer: {request}")
		result = await b2b_service.business_transfer(
			from_business_id=request.from_business_id,
			to_business_id=request.to_business_id,
			amount=request.amount,
			currency=request.currency,
			memo=request.memo
		)
		return result
	except Exception as e:
		logger.error(f"B2B transfer failed: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.get("/b2b/supported-chains")
async def get_supported_chains():
	try:
		chains = b2b_service.get_supported_chains()
		return {"chains": chains}
	except Exception as e:
		logger.error(f"Failed to get supported chains: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/b2b/register-chain")
async def register_chain(request: ChainRegistrationRequest):
	try:
		success = await b2b_service.register_chain(
			request.chain_name,
			request.chain_config
		)
		if success:
			return {
				"status": "success",
				"message": f"Chain {request.chain_name} registered successfully"
			}
		raise HTTPException(
			status_code=400,
			detail=f"Failed to register chain {request.chain_name}"
		)
	except Exception as e:
		logger.error(f"Chain registration failed: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

@app.post("/business/register")
async def register_business(request: BusinessRegistrationRequest):
	try:
		logger.debug(f"Registering business: {request.business_name}")
		
		# Generate business UUID
		business_uuid = uuid_generator.generate_business_uuid(request.business_name)
		
		# Store business details (you'll need to implement proper storage)
		business_data = {
			"uuid": business_uuid,
			"name": request.business_name,
			"country": request.country,
			"legal_entity_type": request.legal_entity_type,
			"registration_number": request.registration_number,
			"industry_type": request.industry_type,
			"registration_date": datetime.utcnow().isoformat()
		}
		
		return {
			"status": "success",
			"message": "Business registered successfully",
			"business_uuid": business_uuid,
			"data": business_data
		}
	except Exception as e:
		logger.error(f"Failed to register business: {str(e)}")
		raise HTTPException(
			status_code=500,
			detail=f"Business registration failed: {str(e)}"
		)

@app.post("/payment/link")
async def generate_payment_link(payment: QRPaymentRequest):
	try:
		logger.debug(f"Generating payment link for: {payment}")
		payment_data = {
			"business_uuid": payment.business_uuid,
			"amount": payment.amount,
			"merchant_name": payment.merchant_name,
			"reference": payment.reference,
			"timestamp": datetime.utcnow().isoformat()
		}
		payment_link = qr_generator.generate_payment_link(payment_data)
		logger.debug("Payment link generated successfully")
		return {"payment_link": payment_link, "payment_data": payment_data}
	except Exception as e:
		logger.error(f"Payment link generation failed: {str(e)}")
		raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=55003)
