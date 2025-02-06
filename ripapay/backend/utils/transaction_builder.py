from qubipy.rpc.rpc_client import QubiPy_RPC
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class TransactionBuilder:
	def __init__(self):
		self.rpc_client = QubiPy_RPC(
			rpc_url=os.getenv("QUBIC_RPC_URL", "https://api.qubic.li/v1/")
		)


	async def create_payment_transaction(
		self,
		from_address: str,
		to_address: str,
		amount: float,
		business_uuid: str
	) -> Dict[str, Any]:
		"""
		Create a payment transaction with fee calculation
		"""
		try:
			# Calculate fee (1.25%)
			fee = amount * 0.0125
			net_amount = amount - fee

			# Build transaction using RPC client
			tx_data = {
				"source": from_address,
				"destination": to_address,
				"amount": int(net_amount),  # Convert to smallest unit
				"fee": int(fee),  # Convert to smallest unit
				"reference": business_uuid
			}

			# Broadcast transaction
			result = self.rpc_client.create_transaction(tx_data)
			
			return {
				"status": "success",
				"transaction_id": result.get("id"),
				"amount": amount,
				"fee": fee,
				"net_amount": net_amount
			}
		except Exception as e:
			raise Exception(f"Failed to create transaction: {str(e)}")
