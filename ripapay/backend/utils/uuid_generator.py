import uuid
import re
from typing import Optional, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UUIDGenerator:
	def __init__(self):
		self._used_uuids = set()
		self._business_prefix = "RPY"  # RipaPay prefix
		
	def generate_business_uuid(self, business_name: str) -> str:
		"""Generate a unique business identifier similar to M-Pesa's Pay Bill"""
		try:
			# Create a base number from timestamp
			timestamp = int(datetime.now().timestamp())
			# Take last 6 digits
			base_number = str(timestamp)[-6:]
			
			# Create a business-specific suffix (2 chars)
			business_suffix = ''.join(c for c in business_name.upper()[:2] if c.isalnum())
			
			# Combine to create a PayBill-like number
			business_uuid = f"{self._business_prefix}{base_number}{business_suffix}"
			
			# Ensure uniqueness
			while business_uuid in self._used_uuids:
				timestamp = int(datetime.now().timestamp())
				base_number = str(timestamp)[-6:]
				business_uuid = f"{self._business_prefix}{base_number}{business_suffix}"
			
			self._used_uuids.add(business_uuid)
			return business_uuid
			
		except Exception as e:
			logger.error(f"Failed to generate business UUID: {str(e)}")
			raise

	def validate_business_uuid(self, business_uuid: str) -> bool:
		"""Validate the format of a business UUID"""
		try:
			pattern = f"^{self._business_prefix}\\d{{6}}[A-Z0-9]{{2}}$"
			return bool(re.match(pattern, business_uuid))
		except Exception as e:
			logger.error(f"Failed to validate business UUID: {str(e)}")
			return False

	def generate_transaction_uuid(self) -> str:
		"""Generate a unique transaction identifier"""
		return str(uuid.uuid4())

	def validate_transaction_uuid(self, transaction_uuid: str) -> bool:
		"""Validate a transaction UUID"""
		try:
			uuid.UUID(transaction_uuid)
			return True
		except ValueError:
			return False