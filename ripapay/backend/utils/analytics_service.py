from typing import Dict, List, Any
import logging
import csv
import json
from io import StringIO
from datetime import datetime, timedelta
from qubipy.rpc.rpc_client import QubiPy_RPC
from collections import defaultdict

logger = logging.getLogger(__name__)

class AnalyticsService:
	def __init__(self, qubic_client: QubiPy_RPC):
		self.qubic_client = qubic_client

	async def get_transaction_analytics(self, business_uuid: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
		try:
			transactions = await self.qubic_client.get_business_transactions(
				business_uuid=business_uuid,
				start_time=start_date.isoformat(),
				end_time=end_date.isoformat()
			)
			
			# Enhanced analytics
			analytics = {
				"summary": {
					"total_volume": sum(float(tx.get('amount', 0)) for tx in transactions),
					"transaction_count": len(transactions),
					"average_transaction": sum(float(tx.get('amount', 0)) for tx in transactions) / len(transactions) if transactions else 0,
					"unique_customers": len(set(tx.get('from_address') for tx in transactions)),
					"success_rate": len([tx for tx in transactions if tx.get('status') == 'success']) / len(transactions) if transactions else 0
				},
				"time_series": self._generate_time_series(transactions, start_date, end_date),
				"distribution": self._analyze_transaction_distribution(transactions),
				"customer_insights": self._analyze_customer_behavior(transactions),
				"hourly_patterns": self._analyze_hourly_patterns(transactions),
				"growth_metrics": self._calculate_growth_metrics(transactions, start_date, end_date)
			}
			
			return analytics
		except Exception as e:
			logger.error(f"Failed to get transaction analytics: {str(e)}")
			raise

	async def export_data(self, business_uuid: str, format: str = "csv") -> bytes:
		try:
			data = await self.qubic_client.get_business_transactions(business_uuid=business_uuid)
			if format == "csv":
				return self._export_to_csv(data)
			elif format == "json":
				return self._export_to_json(data)
			else:
				raise ValueError(f"Unsupported export format: {format}")
		except Exception as e:
			logger.error(f"Failed to export data: {str(e)}")
			raise

	def _generate_time_series(self, transactions: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict]:
		# Generate time series data for visualization
		time_series = []
		current_date = start_date
		while current_date <= end_date:
			daily_transactions = [tx for tx in transactions if tx.get('timestamp', '').startswith(current_date.date().isoformat())]
			time_series.append({
				"date": current_date.date().isoformat(),
				"volume": sum(float(tx.get('amount', 0)) for tx in daily_transactions),
				"count": len(daily_transactions)
			})
			current_date += timedelta(days=1)
		return time_series

	def _analyze_transaction_distribution(self, transactions: List[Dict]) -> Dict[str, Any]:
		# Analyze transaction size distribution
		if not transactions:
			return {"small": 0, "medium": 0, "large": 0}

		amounts = [float(tx.get('amount', 0)) for tx in transactions]
		max_amount = max(amounts)
		
		return {
			"small": len([a for a in amounts if a <= max_amount * 0.33]),
			"medium": len([a for a in amounts if max_amount * 0.33 < a <= max_amount * 0.66]),
			"large": len([a for a in amounts if a > max_amount * 0.66])
		}

	def _analyze_customer_behavior(self, transactions: List[Dict]) -> Dict[str, Any]:
		customer_data = defaultdict(list)
		for tx in transactions:
			customer_data[tx.get('from_address', '')].append(float(tx.get('amount', 0)))
		
		return {
			"repeat_customers": len([c for c in customer_data.values() if len(c) > 1]),
			"customer_segments": {
				"high_value": len([c for c in customer_data.values() if sum(c) > 1000]),
				"medium_value": len([c for c in customer_data.values() if 100 <= sum(c) <= 1000]),
				"low_value": len([c for c in customer_data.values() if sum(c) < 100])
			},
			"average_customer_value": sum(sum(amounts) for amounts in customer_data.values()) / len(customer_data) if customer_data else 0
		}

	def _analyze_hourly_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
		hourly_data = defaultdict(int)
		for tx in transactions:
			hour = datetime.fromisoformat(tx.get('timestamp', '')).hour
			hourly_data[hour] += 1
		
		return {
			"peak_hours": sorted(hourly_data.items(), key=lambda x: x[1], reverse=True)[:3],
			"quiet_hours": sorted(hourly_data.items(), key=lambda x: x[1])[:3],
			"hourly_distribution": dict(sorted(hourly_data.items()))
		}

	def _calculate_growth_metrics(self, transactions: List[Dict], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
		if not transactions:
			return {"growth_rate": 0, "projected_growth": 0}
		
		# Sort transactions by date
		sorted_txs = sorted(transactions, key=lambda x: x.get('timestamp', ''))
		days_span = (end_date - start_date).days or 1
		
		# Calculate daily averages
		daily_volumes = defaultdict(float)
		for tx in transactions:
			date = datetime.fromisoformat(tx.get('timestamp', '')).date()
			daily_volumes[date] += float(tx.get('amount', 0))
		
		if len(daily_volumes) > 1:
			growth_rate = (list(daily_volumes.values())[-1] - list(daily_volumes.values())[0]) / list(daily_volumes.values())[0]
		else:
			growth_rate = 0
		
		return {
			"growth_rate": growth_rate,
			"daily_average_volume": sum(daily_volumes.values()) / len(daily_volumes) if daily_volumes else 0,
			"projected_monthly_volume": (sum(daily_volumes.values()) / days_span) * 30
		}

	def _export_to_csv(self, data: List[Dict]) -> bytes:
		output = StringIO()
		if not data:
			return b""
		
		fieldnames = ['timestamp', 'amount', 'from_address', 'to_address', 'status', 'transaction_id']
		writer = csv.DictWriter(output, fieldnames=fieldnames)
		writer.writeheader()
		
		for transaction in data:
			row = {
				'timestamp': transaction.get('timestamp', ''),
				'amount': transaction.get('amount', '0'),
				'from_address': transaction.get('from_address', ''),
				'to_address': transaction.get('to_address', ''),
				'status': transaction.get('status', ''),
				'transaction_id': transaction.get('transaction_id', '')
			}
			writer.writerow(row)
		
		return output.getvalue().encode('utf-8')

	def _export_to_json(self, data: List[Dict]) -> bytes:
		formatted_data = {
			'transactions': data,
			'metadata': {
				'count': len(data),
				'total_volume': sum(float(tx.get('amount', 0)) for tx in data),
				'export_timestamp': datetime.utcnow().isoformat()
			}
		}
		return json.dumps(formatted_data, indent=2).encode('utf-8')