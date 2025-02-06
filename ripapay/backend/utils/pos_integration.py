from typing import Dict, Any
from datetime import datetime
from .qr_payment import QRPaymentGenerator
from .transaction_builder import TransactionBuilder

class POSIntegration:
	def __init__(self, transaction_builder: TransactionBuilder, qr_generator: QRPaymentGenerator):
		self.transaction_builder = transaction_builder
		self.qr_generator = qr_generator
		
	async def create_pos_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Create a POS payment with QR code and transaction details
		"""
		try:
			# Generate payment QR code
			qr_data = {
				"business_uuid": payment_data["business_uuid"],
				"amount": payment_data["amount"],
				"merchant_name": payment_data.get("merchant_name", ""),
				"reference": payment_data.get("reference", ""),
				"timestamp": datetime.utcnow().isoformat(),
				"pos_id": payment_data.get("pos_id", ""),
				"terminal_id": payment_data.get("terminal_id", "")
			}
			
			qr_result = self.qr_generator.generate_payment_qr(qr_data)
			
			return {
				"qr_data": qr_result,
				"payment_info": {
					"amount": payment_data["amount"],
					"merchant": payment_data.get("merchant_name", ""),
					"terminal": payment_data.get("terminal_id", ""),
					"timestamp": qr_data["timestamp"]
				}
			}
		except Exception as e:
			raise Exception(f"Failed to create POS payment: {str(e)}")
			
	async def process_pos_payment(self, payment_data: Dict[str, Any], transaction_data: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Process a POS payment after QR code scan
		"""
		try:
			# Verify QR payment data
			is_valid = self.qr_generator.verify_qr_payment(payment_data, transaction_data)
			if not is_valid:
				raise Exception("Invalid payment data")
				
			# Process transaction
			result = await self.transaction_builder.create_payment_transaction(
				from_address=transaction_data["from_address"],
				to_address=transaction_data["to_address"],
				amount=transaction_data["amount"],
				business_uuid=transaction_data["business_uuid"]
			)
			
			return {
				"status": "success",
				"transaction": result,
				"pos_info": {
					"terminal_id": payment_data.get("terminal_id", ""),
					"pos_id": payment_data.get("pos_id", ""),
					"timestamp": datetime.utcnow().isoformat()
				}
			}
		except Exception as e:
			raise Exception(f"Failed to process POS payment: {str(e)}")