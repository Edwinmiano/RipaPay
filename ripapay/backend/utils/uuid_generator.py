import uuid
import re
from typing import Optional, Dict
import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class UUIDGenerator:
	def __init__(self):
		self._used_uuids = set()
		
	def generate_business_uuid(self, business_name: str) -> str:
		"""Generate a unique 8-digit business identifier"""
		try:
			# Create a base number from timestamp (last 6 digits)
			timestamp = int(datetime.now().timestamp())
			base_number = str(timestamp)[-6:]
			
			# Add 2 random digits for uniqueness
			random_suffix = str(random.randint(10, 99))
			
			# Combine to create an 8-digit number
			business_uuid = f"{base_number}{random_suffix}"
			
			# Ensure uniqueness
			while business_uuid in self._used_uuids:
				timestamp = int(datetime.now().timestamp())
				base_number = str(timestamp)[-6:]
				random_suffix = str(random.randint(10, 99))
				business_uuid = f"{base_number}{random_suffix}"
			
			self._used_uuids.add(business_uuid)
			return business_uuid
			
		except Exception as e:
			logger.error(f"Failed to generate business UUID: {str(e)}")
			raise

	def validate_business_uuid(self, business_uuid: str) -> bool:
		"""Validate the format of a business UUID"""
		try:
			pattern = r"^\d{8}$"  # Exactly 8 digits
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