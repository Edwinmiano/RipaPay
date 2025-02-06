import qrcode
import json
from typing import Dict, Any
from base64 import b64encode
from io import BytesIO

class QRPaymentGenerator:
	def __init__(self):
		self.qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4,
		)

	def generate_payment_qr(self, payment_data: Dict[str, Any]) -> str:
		"""
		Generate QR code for payment data
		Returns base64 encoded QR code image
		"""
		try:
			# Format payment data
			qr_data = {
				"business_uuid": payment_data["business_uuid"],
				"amount": payment_data["amount"],
				"reference": payment_data.get("reference", ""),
				"merchant_name": payment_data.get("merchant_name", ""),
				"timestamp": payment_data.get("timestamp", "")
			}

			# Create QR code
			self.qr.clear()
			self.qr.add_data(json.dumps(qr_data))
			self.qr.make(fit=True)

			# Create image
			img = self.qr.make_image(fill_color="black", back_color="white")
			
			# Convert to base64
			buffered = BytesIO()
			img.save(buffered, format="PNG")
			qr_base64 = b64encode(buffered.getvalue()).decode()
			
			return {
				"qr_code": qr_base64,
				"payment_data": qr_data
			}
		except Exception as e:
			raise Exception(f"Failed to generate QR code: {str(e)}")

	def verify_qr_payment(self, qr_data: Dict[str, Any], payment_data: Dict[str, Any]) -> bool:
		"""
		Verify if QR payment data matches transaction data
		"""
		try:
			return (
				qr_data["business_uuid"] == payment_data["business_uuid"] and
				qr_data["amount"] == payment_data["amount"]
			)
		except Exception as e:
			raise Exception(f"Failed to verify QR payment: {str(e)}")