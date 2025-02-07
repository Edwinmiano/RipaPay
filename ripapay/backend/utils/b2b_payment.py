from typing import Dict, Any, Optional
import logging
from qubipy.rpc.rpc_client import QubiPy_RPC
from datetime import datetime
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class B2BPaymentService:
	def __init__(self, qubic_client: QubiPy_RPC):
		self.qubic_client = qubic_client
		self.supported_chains = {
			"qubic": {
				"name": "Qubic",
				"enabled": True,
				"client": qubic_client
			}
		}

	async def business_transfer(
		self,
		from_business_id: str,
		to_business_id: str,
		amount: float,
		currency: str = "QUBIC",
		memo: Optional[str] = None
	) -> Dict[str, Any]:
		try:
			# Get business wallet addresses
			from_address = await self._get_business_wallet(from_business_id)
			to_address = await self._get_business_wallet(to_business_id)

			# Create transfer with business context
			transfer_data = {
				"source": from_address,
				"destination": to_address,
				"amount": int(amount),
				"currency": currency,
				"memo": memo or f"B2B Transfer - {datetime.utcnow().isoformat()}",
				"transfer_type": "b2b",
				"business_context": {
					"from_business": from_business_id,
					"to_business": to_business_id,
					"timestamp": datetime.utcnow().isoformat()
				}
			}

			# Execute transfer on appropriate chain
			if currency == "QUBIC":
				result = await self._execute_qubic_transfer(transfer_data)
			else:
				raise ValueError(f"Unsupported currency: {currency}")

			return {
				"status": "success",
				"transfer_id": result.get("id"),
				"from_business": from_business_id,
				"to_business": to_business_id,
				"amount": amount,
				"currency": currency,
				"timestamp": datetime.utcnow().isoformat()
			}

		except Exception as e:
			logger.error(f"B2B transfer failed: {str(e)}")
			raise

	async def _execute_qubic_transfer(self, transfer_data: Dict[str, Any]) -> Dict[str, Any]:
		try:
			# Calculate B2B fee (0.75% - reduced rate for B2B)
			amount = transfer_data["amount"]
			fee = amount * 0.0075
			net_amount = amount - fee

			tx_data = {
				"source": transfer_data["source"],
				"destination": transfer_data["destination"],
				"amount": int(net_amount),
				"fee": int(fee),
				"memo": transfer_data["memo"]
			}

			result = await self.qubic_client.create_transaction(tx_data)
			return result

		except Exception as e:
			logger.error(f"Qubic transfer failed: {str(e)}")
			raise

	async def _get_business_wallet(self, business_id: str) -> str:
		# TODO: Implement business wallet lookup
		# This should fetch the primary wallet address for the business
		# For now, return a placeholder
		return f"placeholder_address_{business_id}"

	def get_supported_chains(self) -> Dict[str, Dict[str, Any]]:
		return self.supported_chains

	async def register_chain(self, chain_name: str, chain_config: Dict[str, Any]) -> bool:
		try:
			if chain_name in self.supported_chains:
				raise ValueError(f"Chain {chain_name} already registered")

			# Validate chain configuration
			required_fields = ["name", "client_config", "enabled"]
			for field in required_fields:
				if field not in chain_config:
					raise ValueError(f"Missing required field: {field}")

			# Store chain configuration
			self.supported_chains[chain_name] = {
				"name": chain_config["name"],
				"enabled": chain_config["enabled"],
				"client": None  # Initialize client based on config when needed
			}

			return True

		except Exception as e:
			logger.error(f"Failed to register chain {chain_name}: {str(e)}")
			return False