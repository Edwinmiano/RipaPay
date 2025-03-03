from datetime import datetime, timedelta
from typing import Dict, List, Optional
from qubipy.rpc.rpc_client import QubiPy_RPC
import logging

logger = logging.getLogger(__name__)

class DashboardMetricsService:
	def __init__(self, qubic_client: QubiPy_RPC):
		self.qubic_client = qubic_client

	async def get_key_metrics(self, business_uuid: str) -> Dict:
		try:
			# Get metrics for the last 24 hours
			end_time = datetime.utcnow()
			start_time = end_time - timedelta(hours=24)

			# TODO: Implement actual metrics calculation using QubiPy
			metrics = {
				"total_transactions": await self._get_transaction_count(business_uuid, start_time, end_time),
				"total_volume": await self._get_transaction_volume(business_uuid, start_time, end_time),
				"average_transaction_size": await self._get_average_transaction(business_uuid, start_time, end_time),
				"active_wallets": await self._get_active_wallets_count(business_uuid, start_time, end_time)
			}
			return metrics
		except Exception as e:
			logger.error(f"Failed to get key metrics: {str(e)}")
			raise

	async def get_transaction_monitoring(self, business_uuid: str, limit: int = 10) -> List[Dict]:
		try:
			# TODO: Implement actual transaction monitoring using QubiPy
			transactions = await self.qubic_client.get_business_transactions(
				business_uuid=business_uuid,
				limit=limit
			)
			return self._format_transactions(transactions)
		except Exception as e:
			logger.error(f"Failed to get transaction monitoring: {str(e)}")
			raise

	async def _get_transaction_count(self, business_uuid: str, start_time: datetime, end_time: datetime) -> int:
		try:
			transactions = await self.qubic_client.get_business_transactions(
				business_uuid=business_uuid,
				start_time=start_time.isoformat(),
				end_time=end_time.isoformat()
			)
			return len(transactions)
		except Exception as e:
			logger.error(f"Failed to get transaction count: {str(e)}")
			return 0

	async def _get_transaction_volume(self, business_uuid: str, start_time: datetime, end_time: datetime) -> float:
		try:
			transactions = await self.qubic_client.get_business_transactions(
				business_uuid=business_uuid,
				start_time=start_time.isoformat(),
				end_time=end_time.isoformat()
			)
			return sum(float(tx.get('amount', 0)) for tx in transactions)
		except Exception as e:
			logger.error(f"Failed to get transaction volume: {str(e)}")
			return 0.0

	async def _get_average_transaction(self, business_uuid: str, start_time: datetime, end_time: datetime) -> float:
		try:
			count = await self._get_transaction_count(business_uuid, start_time, end_time)
			if count == 0:
				return 0.0
			volume = await self._get_transaction_volume(business_uuid, start_time, end_time)
			return volume / count
		except Exception as e:
			logger.error(f"Failed to get average transaction: {str(e)}")
			return 0.0

	async def _get_active_wallets_count(self, business_uuid: str, start_time: datetime, end_time: datetime) -> int:
		try:
			transactions = await self.qubic_client.get_business_transactions(
				business_uuid=business_uuid,
				start_time=start_time.isoformat(),
				end_time=end_time.isoformat()
			)
			unique_wallets = set()
			for tx in transactions:
				unique_wallets.add(tx.get('from_address'))
				unique_wallets.add(tx.get('to_address'))
			return len(unique_wallets)
		except Exception as e:
			logger.error(f"Failed to get active wallets count: {str(e)}")
			return 0

	def _format_transactions(self, transactions: List[Dict]) -> List[Dict]:
		# Format transactions for frontend display
		formatted = []
		for tx in transactions:
			formatted.append({
				"id": tx.get("id"),
				"timestamp": tx.get("timestamp"),
				"amount": tx.get("amount"),
				"status": tx.get("status"),
				"from_address": tx.get("from_address"),
				"to_address": tx.get("to_address")
			})
		return formatted