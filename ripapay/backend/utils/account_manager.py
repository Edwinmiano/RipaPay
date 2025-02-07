from qubipy.rpc.rpc_client import QubiPy_RPC
from typing import Dict, List, Any, Optional
import logging
from pydantic import BaseModel, Field
import json
import os
from datetime import datetime
from .cloud_storage import GoogleDriveStorage

logger = logging.getLogger(__name__)

class AccountManager:
	def __init__(self, qubic_client: QubiPy_RPC):
		self.qubic_client = qubic_client
		self.cloud_storage = None

	async def create_account(self, mnemonic: str) -> Dict[str, Any]:
		try:
			account = await self.qubic_client.create_account(mnemonic)
			return account
		except Exception as e:
			logger.error(f"Failed to create account: {str(e)}")
			raise

	async def get_account_details(self, address: str) -> Dict[str, Any]:
		try:
			details = await self.qubic_client.get_account_details(address)
			return details
		except Exception as e:
			logger.error(f"Failed to get account details: {str(e)}")
			raise

	async def backup_account(self, address: str, backup_path: str) -> Dict[str, Any]:
		try:
			# Get account details for backup
			account_details = await self.get_account_details(address)
			
			# Create backup file locally
			backup_data = {
				"address": address,
				"account_details": account_details,
				"timestamp": str(datetime.now())
			}
			
			with open(backup_path, 'w') as f:
				json.dump(backup_data, f, indent=4)
			
			# If cloud storage is configured, upload to cloud
			if self.cloud_storage:
				upload_result = self.cloud_storage.upload_file(backup_path)
				return {
					"local_backup": backup_path,
					"cloud_backup": upload_result
				}
			
			return {"local_backup": backup_path}
			
		except Exception as e:
			logger.error(f"Failed to backup account: {str(e)}")
			raise

	async def restore_account(self, backup_path: str) -> Dict[str, Any]:
		try:
			if self.cloud_storage and not os.path.exists(backup_path):
				# Try to download from cloud if file doesn't exist locally
				file_id = backup_path  # Assuming backup_path is the file_id for cloud storage
				local_path = f"temp_restore_{file_id}.json"
				self.cloud_storage.download_file(file_id, local_path)
				backup_path = local_path

			with open(backup_path, 'r') as f:
				backup_data = json.load(f)
			
			return backup_data
			
		except Exception as e:
			logger.error(f"Failed to restore account: {str(e)}")
			raise

	async def cloud_integration(self, address: str, cloud_provider: str, credentials: Dict[str, Any]) -> bool:
		try:
			if cloud_provider.lower() == "google_drive":
				self.cloud_storage = GoogleDriveStorage()
				# Initialize and authenticate Google Drive
				if self.cloud_storage.authenticate():
					# Create a folder for the account
					folder_name = f"ripapay_backup_{address[:8]}"
					folder_id = self.cloud_storage.create_folder(folder_name)
					
					# Store folder ID for future use
					self._store_cloud_config(address, {
						"provider": cloud_provider,
						"folder_id": folder_id
					})
					
					return True
			return False
			
		except Exception as e:
			logger.error(f"Failed to integrate with cloud provider: {str(e)}")
			raise

	def _store_cloud_config(self, address: str, config: Dict[str, Any]) -> None:
		try:
			config_path = f"cloud_config_{address}.json"
			with open(config_path, 'w') as f:
				json.dump(config, f)
		except Exception as e:
			logger.error(f"Failed to store cloud configuration: {str(e)}")
			raise

class AccountCreationRequest(BaseModel):
	mnemonic: str = Field(..., description="Mnemonic phrase for account creation")

class AccountDetailsRequest(BaseModel):
	address: str = Field(..., description="Qubic address to retrieve details for")

class AccountBackupRequest(BaseModel):
	address: str = Field(..., description="Qubic address to backup")
	backup_path: str = Field(..., description="Path to save the backup file")

class AccountRestoreRequest(BaseModel):
	backup_path: str = Field(..., description="Path to the backup file")

class CloudIntegrationRequest(BaseModel):
	address: str = Field(..., description="Qubic address to integrate")
	cloud_provider: str = Field(..., description="Cloud provider name (e.g., Google Drive)")
	credentials: Dict[str, Any] = Field(..., description="Cloud provider credentials")