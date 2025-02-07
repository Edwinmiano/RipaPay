from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import io
import json
from typing import Optional, List, Dict

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveStorage:
	def __init__(self):
		self.creds = None
		self.service = None
		self.token_path = 'token.json'
		self.credentials_path = 'credentials.json'
		
	def authenticate(self) -> bool:
		if os.path.exists(self.token_path):
			self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
		
		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
				self.creds = flow.run_local_server(port=0)
			
			with open(self.token_path, 'w') as token:
				token.write(self.creds.to_json())
		
		self.service = build('drive', 'v3', credentials=self.creds)
		return True

	def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> Dict:
		try:
			file_metadata = {'name': os.path.basename(file_path)}
			if folder_id:
				file_metadata['parents'] = [folder_id]
			
			media = MediaFileUpload(file_path, resumable=True)
			file = self.service.files().create(
				body=file_metadata,
				media_body=media,
				fields='id, name, webViewLink'
			).execute()
			
			return {
				'id': file.get('id'),
				'name': file.get('name'),
				'link': file.get('webViewLink')
			}
		except Exception as e:
			raise Exception(f"Failed to upload file: {str(e)}")

	def download_file(self, file_id: str, destination_path: str) -> bool:
		try:
			request = self.service.files().get_media(fileId=file_id)
			fh = io.BytesIO()
			downloader = MediaIoBaseDownload(fh, request)
			
			done = False
			while not done:
				status, done = downloader.next_chunk()
			
			fh.seek(0)
			with open(destination_path, 'wb') as f:
				f.write(fh.read())
				f.flush()
			
			return True
		except Exception as e:
			raise Exception(f"Failed to download file: {str(e)}")

	def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
		try:
			file_metadata = {
				'name': folder_name,
				'mimeType': 'application/vnd.google-apps.folder'
			}
			if parent_id:
				file_metadata['parents'] = [parent_id]
			
			file = self.service.files().create(
				body=file_metadata,
				fields='id'
			).execute()
			
			return file.get('id')
		except Exception as e:
			raise Exception(f"Failed to create folder: {str(e)}")

	def list_files(self, folder_id: Optional[str] = None) -> List[Dict]:
		try:
			query = f"'{folder_id}' in parents" if folder_id else None
			results = self.service.files().list(
				q=query,
				pageSize=100,
				fields="files(id, name, mimeType, webViewLink)"
			).execute()
			
			return results.get('files', [])
		except Exception as e:
			raise Exception(f"Failed to list files: {str(e)}")