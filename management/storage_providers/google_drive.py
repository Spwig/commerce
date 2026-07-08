"""
Google Drive storage provider.

Uses Google Drive API v3 for backup file storage.
OAuth 2.0 authorization code flow via google-auth-oauthlib.
"""
import io
import logging
import os
from typing import Any, Callable, Dict, List, Optional

from .base import (
    BaseStorageProvider,
    ConnectionTestResult,
    RemoteFile,
    UploadResult,
)

logger = logging.getLogger(__name__)

GOOGLE_TOKEN_URI = 'https://oauth2.googleapis.com/token'
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveOAuthHandler:
    """OAuth 2.0 handler for Google Drive authorization code flow."""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        if not client_id or not client_secret or not redirect_uri:
            raise ValueError('client_id, client_secret and redirect_uri are required')

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client_config = {
            'web': {
                'client_id': client_id,
                'client_secret': client_secret,
                'auth_uri': 'https://accounts.google.com/o/oauth2/v2/auth',
                'token_uri': GOOGLE_TOKEN_URI,
                'redirect_uris': [redirect_uri],
            }
        }

    def get_authorization_url(self, state: Optional[str] = None) -> Dict[str, str]:
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_config(
            self.client_config,
            scopes=DRIVE_SCOPES,
            redirect_uri=self.redirect_uri,
        )
        authorization_url, state_value = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent',
        )
        return {'authorization_url': authorization_url, 'state': state_value}

    def exchange_code_for_tokens(self, authorization_code: str) -> Dict[str, Any]:
        from google_auth_oauthlib.flow import Flow

        if not authorization_code:
            raise ValueError('authorization_code is required')

        flow = Flow.from_client_config(
            self.client_config,
            scopes=DRIVE_SCOPES,
            redirect_uri=self.redirect_uri,
        )
        flow.fetch_token(code=authorization_code)
        creds = flow.credentials

        result = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': list(creds.scopes) if creds.scopes else DRIVE_SCOPES,
        }
        if creds.expiry:
            result['expiry'] = creds.expiry.isoformat()
        return result


class GoogleDriveStorageProvider(BaseStorageProvider):
    provider_type = 'google_drive'
    provider_name = 'Google Drive'
    requires_oauth = True
    oauth_scopes = DRIVE_SCOPES

    credential_fields = [
        {
            'key': 'client_id',
            'label': 'Client ID',
            'secret': False,
            'required': True,
            'type': 'text',
            'help_text': 'From Google Cloud Console \u2192 APIs & Services \u2192 Credentials.',
        },
        {
            'key': 'client_secret',
            'label': 'Client Secret',
            'secret': True,
            'required': True,
            'type': 'password',
        },
    ]

    settings_fields = [
        {
            'key': 'folder_name',
            'label': 'Backup Folder',
            'type': 'text',
            'required': False,
            'default': 'Spwig Backups',
            'help_text': 'Folder name in Google Drive (created automatically).',
        },
    ]

    @classmethod
    def create_oauth_handler(cls, client_id, client_secret, redirect_uri):
        return GoogleDriveOAuthHandler(client_id, client_secret, redirect_uri)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_credentials(self):
        """Build google.oauth2.credentials.Credentials from stored dict."""
        from google.oauth2.credentials import Credentials

        return Credentials(
            token=self.credentials.get('token'),
            refresh_token=self.credentials.get('refresh_token'),
            token_uri=self.credentials.get('token_uri', GOOGLE_TOKEN_URI),
            client_id=self.credentials.get('client_id'),
            client_secret=self.credentials.get('client_secret'),
            scopes=self.credentials.get('scopes', DRIVE_SCOPES),
        )

    def _get_service(self):
        """Build an authorized Drive API v3 service client."""
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = self._build_credentials()
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Persist refreshed token back to self.credentials
            self.credentials['token'] = creds.token
            if creds.expiry:
                self.credentials['expiry'] = creds.expiry.isoformat()

        return build('drive', 'v3', credentials=creds, cache_discovery=False)

    def _get_or_create_folder(self, service) -> str:
        """Find or create the backup folder. Returns folder ID."""
        folder_name = self.settings.get('folder_name', 'Spwig Backups')

        # Search for existing folder (escape quotes for Drive API query syntax)
        safe_name = folder_name.replace("\\", "\\\\").replace("'", "\\'")
        query = (
            f"name='{safe_name}' and mimeType='application/vnd.google-apps.folder' "
            f"and trashed=false"
        )
        results = service.files().list(
            q=query, fields='files(id, name)', pageSize=1
        ).execute()
        files = results.get('files', [])

        if files:
            return files[0]['id']

        # Create folder
        metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        folder = service.files().create(
            body=metadata, fields='id'
        ).execute()
        return folder['id']

    def refresh_credentials_if_needed(self) -> Dict[str, Any]:
        """Refresh OAuth token if expired."""
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

        creds = self._build_credentials()
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            self.credentials['token'] = creds.token
            if creds.expiry:
                self.credentials['expiry'] = creds.expiry.isoformat()
        return self.credentials

    # ------------------------------------------------------------------
    # ABC implementation
    # ------------------------------------------------------------------

    def test_connection(self) -> ConnectionTestResult:
        try:
            service = self._get_service()

            # Get user info and storage quota
            about = service.about().get(
                fields='user,storageQuota'
            ).execute()

            user = about.get('user', {})
            quota = about.get('storageQuota', {})

            email = user.get('emailAddress', 'Unknown')
            storage_limit = int(quota.get('limit', 0))
            storage_usage = int(quota.get('usage', 0))

            # Verify we can find/create the backup folder
            folder_id = self._get_or_create_folder(service)

            details = {
                'email': email,
                'folder_id': folder_id,
                'folder_name': self.settings.get('folder_name', 'Spwig Backups'),
            }

            return ConnectionTestResult(
                success=True,
                message=f'Connected to Google Drive as {email}.',
                details=details,
                storage_used=storage_usage if storage_limit else None,
                storage_available=(storage_limit - storage_usage) if storage_limit else None,
            )

        except Exception as e:
            error_msg = str(e)
            if 'invalid_grant' in error_msg.lower():
                msg = 'Authorization expired or revoked. Please re-authorize.'
            elif 'access_denied' in error_msg.lower() or '403' in error_msg:
                msg = 'Access denied. Check that the Google Drive API is enabled in your Cloud Console.'
            elif 'invalid_client' in error_msg.lower():
                msg = 'Invalid Client ID or Client Secret.'
            else:
                msg = f'Connection failed: {error_msg}'
            return ConnectionTestResult(success=False, message=msg)

    def upload_file(
        self,
        local_path: str,
        remote_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> UploadResult:
        try:
            from googleapiclient.http import MediaFileUpload

            service = self._get_service()
            folder_id = self._get_or_create_folder(service)
            file_size = os.path.getsize(local_path)
            filename = os.path.basename(remote_path)

            metadata = {
                'name': filename,
                'parents': [folder_id],
            }

            media = MediaFileUpload(
                local_path,
                resumable=True,
                chunksize=5 * 1024 * 1024,  # 5 MB chunks
            )

            request = service.files().create(
                body=metadata,
                media_body=media,
                fields='id,name,size',
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status and progress_callback:
                    progress_callback(
                        int(status.resumable_progress), file_size
                    )

            if progress_callback:
                progress_callback(file_size, file_size)

            file_id = response.get('id', '')

            return UploadResult(
                success=True,
                remote_path=file_id,
                file_size=file_size,
                message='Upload completed.',
            )

        except Exception as e:
            logger.error('Google Drive upload failed: %s', e)
            return UploadResult(success=False, message=str(e))

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> bool:
        try:
            from googleapiclient.http import MediaIoBaseDownload

            service = self._get_service()

            # remote_path is the file ID for Google Drive
            file_id = remote_path

            # Get file size for progress
            file_meta = service.files().get(
                fileId=file_id, fields='size'
            ).execute()
            total_size = int(file_meta.get('size', 0))

            request = service.files().get_media(fileId=file_id)

            with open(local_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status and progress_callback and total_size:
                        progress_callback(
                            int(status.resumable_progress), total_size
                        )

            if progress_callback and total_size:
                progress_callback(total_size, total_size)

            return True

        except Exception as e:
            logger.error('Google Drive download failed: %s', e)
            return False

    def list_files(self, prefix: str = '') -> List[RemoteFile]:
        try:
            service = self._get_service()
            folder_id = prefix or self._get_or_create_folder(service)

            query = f"'{folder_id}' in parents and trashed=false"
            files: List[RemoteFile] = []

            page_token = None
            while True:
                results = service.files().list(
                    q=query,
                    fields='nextPageToken, files(id, name, size, modifiedTime)',
                    pageSize=100,
                    pageToken=page_token,
                ).execute()

                for item in results.get('files', []):
                    files.append(
                        RemoteFile(
                            path=item['id'],
                            size=int(item.get('size', 0)),
                            last_modified=item.get('modifiedTime'),
                            metadata={'name': item.get('name', '')},
                        )
                    )

                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            return files

        except Exception as e:
            logger.error('Google Drive list_files failed: %s', e)
            return []

    def delete_file(self, remote_path: str) -> bool:
        try:
            service = self._get_service()
            service.files().delete(fileId=remote_path).execute()
            return True
        except Exception as e:
            logger.error('Google Drive delete failed: %s', e)
            return False
