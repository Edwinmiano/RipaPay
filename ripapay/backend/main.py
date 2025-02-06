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

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=55003)
