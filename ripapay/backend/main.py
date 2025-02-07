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
from typing import Optional
from utils.dashboard_metrics import DashboardMetricsService
from utils.transaction_tracker import TransactionTracker

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
