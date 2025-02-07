from qubipy.rpc.rpc_client import QubiPy_RPC
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class WalletService:
	def __init__(self, qubic_client: QubiPy_RPC):
		self.qubic_client = qubic_client

	async def connect_wallet(self, address: str) -> Dict:
		try:
			# Verify the address format and existence
			is_valid = await self.qubic_client.validate_address(address)
			if not is_valid:
				raise ValueError("Invalid Qubic address")
			
			return {
				"status": "connected",
				"address": address
			}
		except Exception as e:
			logger.error(f"Wallet connection failed: {str(e)}")
			raise

	async def get_balance(self, address: str) -> float:
		try:
			balance = await self.qubic_client.get_balance(address)
			return float(balance)
		except Exception as e:
			logger.error(f"Failed to get balance: {str(e)}")
			raise

	async def get_transactions(self, address: str, limit: int = 10, offset: int = 0) -> List[Dict]:
		try:
			transactions = await self.qubic_client.get_transactions(
				address=address,
				limit=limit,
				offset=offset
			)
			return transactions
		except Exception as e:
			logger.error(f"Failed to get transactions: {str(e)}")
			raise