from qubipy.rpc.rpc_client import QubiPy_RPC
from typing import Dict, List, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TransactionTracker:
	def __init__(self, qubic_client: QubiPy_RPC):
		self.qubic_client = qubic_client

	async def get_inbound_transactions(self, address: str, limit: int = 10) -> List[Dict]:
		"""Get incoming transactions for an address"""
		try:
			transactions = await self.qubic_client.get_transactions(
				destination=address,
				limit=limit
			)
			return self._format_transactions(transactions, "inbound")
		except Exception as e:
			logger.error(f"Failed to get inbound transactions: {str(e)}")
			raise

	async def get_outbound_transactions(self, address: str, limit: int = 10) -> List[Dict]:
		"""Get outgoing transactions from an address"""
		try:
			transactions = await self.qubic_client.get_transactions(
				source=address,
				limit=limit
			)
			return self._format_transactions(transactions, "outbound")
		except Exception as e:
			logger.error(f"Failed to get outbound transactions: {str(e)}")
			raise

	async def get_transaction_details(self, tx_id: str) -> Dict:
		"""Get detailed information about a specific transaction"""
		try:
			tx_details = await self.qubic_client.get_transaction(tx_id)
			return {
				"id": tx_details.get("id"),
				"timestamp": tx_details.get("timestamp"),
				"source": tx_details.get("source"),
				"destination": tx_details.get("destination"),
				"amount": tx_details.get("amount"),
				"fee": tx_details.get("fee"),
				"status": tx_details.get("status"),
				"block_height": tx_details.get("block_height"),
				"confirmations": tx_details.get("confirmations")
			}
		except Exception as e:
			logger.error(f"Failed to get transaction details: {str(e)}")
			raise

	def _format_transactions(self, transactions: List[Dict], tx_type: str) -> List[Dict]:
		"""Format transaction data for frontend display"""
		formatted = []
		for tx in transactions:
			formatted.append({
				"id": tx.get("id"),
				"timestamp": tx.get("timestamp"),
				"amount": tx.get("amount"),
				"fee": tx.get("fee"),
				"status": tx.get("status"),
				"type": tx_type,
				"counterparty": tx.get("destination" if tx_type == "outbound" else "source")
			})
		return formatted