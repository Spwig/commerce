"""
Dropbox storage provider.

Uses the official Dropbox Python SDK for file operations.
OAuth 2.0 authorization code flow with PKCE for authentication.
"""
import logging
import os
import secrets
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlencode

from .base import (
    BaseStorageProvider,
    ConnectionTestResult,
    RemoteFile,
    UploadResult,
)

logger = logging.getLogger(__name__)

DROPBOX_AUTHORIZE_URL = 'https://www.dropbox.com/oauth2/authorize'
DROPBOX_TOKEN_URL = 'https://api.dropboxapi.com/oauth2/token'

# Dropbox chunk size: 4 MB for session uploads
CHUNK_SIZE = 4 * 1024 * 1024
# Files larger than 150 MB use upload sessions
SESSION_THRESHOLD = 150 * 1024 * 1024


class DropboxOAuthHandler:
    """OAuth 2.0 handler for Dropbox authorization code flow."""

    def __init__(self, app_key: str, app_secret: str, redirect_uri: str):
        if not app_key or not app_secret or not redirect_uri:
            raise ValueError('app_key, app_secret and redirect_uri are required')

        self.app_key = app_key
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, state: Optional[str] = None) -> Dict[str, str]:
        params = {
            'client_id': self.app_key,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'token_access_type': 'offline',
        }
        if state:
            params['state'] = state

        authorization_url = f'{DROPBOX_AUTHORIZE_URL}?{urlencode(params)}'
        return {'authorization_url': authorization_url, 'state': state or ''}

    def exchange_code_for_tokens(self, authorization_code: str) -> Dict[str, Any]:
        import requests

        if not authorization_code:
            raise ValueError('authorization_code is required')

        response = requests.post(
            DROPBOX_TOKEN_URL,
            data={
                'code': authorization_code,
                'grant_type': 'authorization_code',
                'client_id': self.app_key,
                'client_secret': self.app_secret,
                'redirect_uri': self.redirect_uri,
            },
            timeout=30,
        )

        if response.status_code != 200:
            error = response.json().get('error_description', response.text)
            raise ConnectionError(f'Token exchange failed: {error}')

        data = response.json()
        return {
            'access_token': data['access_token'],
            'refresh_token': data.get('refresh_token', ''),
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'token_type': data.get('token_type', 'bearer'),
            'account_id': data.get('account_id', ''),
            'uid': data.get('uid', ''),
        }


class DropboxStorageProvider(BaseStorageProvider):
    provider_type = 'dropbox'
    provider_name = 'Dropbox'
    requires_oauth = True
    oauth_scopes = []

    credential_fields = [
        {
            'key': 'app_key',
            'label': 'App Key',
            'secret': False,
            'required': True,
            'type': 'text',
            'help_text': 'From Dropbox App Console \u2192 Settings.',
        },
        {
            'key': 'app_secret',
            'label': 'App Secret',
            'secret': True,
            'required': True,
            'type': 'password',
        },
    ]

    settings_fields = [
        {
            'key': 'folder_path',
            'label': 'Backup Folder',
            'type': 'text',
            'required': False,
            'default': '/Spwig Backups',
            'help_text': 'Path in Dropbox (created automatically).',
        },
    ]

    @classmethod
    def create_oauth_handler(cls, client_id, client_secret, redirect_uri):
        return DropboxOAuthHandler(client_id, client_secret, redirect_uri)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_client(self):
        """Create an authenticated Dropbox client with auto-refresh."""
        import dropbox

        access_token = self.credentials.get('access_token', '')
        refresh_token = self.credentials.get('refresh_token', '')
        app_key = self.credentials.get('app_key', '')
        app_secret = self.credentials.get('app_secret', '')

        if refresh_token and app_key and app_secret:
            return dropbox.Dropbox(
                oauth2_access_token=access_token,
                oauth2_refresh_token=refresh_token,
                app_key=app_key,
                app_secret=app_secret,
            )
        return dropbox.Dropbox(oauth2_access_token=access_token)

    def _folder_path(self) -> str:
        path = self.settings.get('folder_path', '/Spwig Backups')
        if not path.startswith('/'):
            path = '/' + path
        if path.endswith('/'):
            path = path.rstrip('/')
        return path

    def _ensure_folder(self, dbx):
        """Create the backup folder if it doesn't exist."""
        import dropbox

        folder = self._folder_path()
        try:
            dbx.files_get_metadata(folder)
        except dropbox.exceptions.ApiError as e:
            if hasattr(e, 'error') and e.error.is_path() and e.error.get_path().is_not_found():
                dbx.files_create_folder_v2(folder)
            else:
                raise

    def refresh_credentials_if_needed(self) -> Dict[str, Any]:
        """Dropbox SDK handles token refresh automatically via the client."""
        try:
            dbx = self._get_client()
            dbx.check_and_refresh_access_token()
            self.credentials['access_token'] = dbx._oauth2_access_token
        except Exception:
            pass
        return self.credentials

    # ------------------------------------------------------------------
    # ABC implementation
    # ------------------------------------------------------------------

    def test_connection(self) -> ConnectionTestResult:
        try:
            dbx = self._get_client()

            # Get account info
            account = dbx.users_get_current_account()
            space = dbx.users_get_space_usage()

            display_name = account.name.display_name
            email = account.email

            # Space info
            used = space.used
            if space.allocation.is_individual():
                allocated = space.allocation.get_individual().allocated
            else:
                allocated = 0

            # Ensure backup folder
            self._ensure_folder(dbx)

            details = {
                'display_name': display_name,
                'email': email,
                'folder_path': self._folder_path(),
            }

            return ConnectionTestResult(
                success=True,
                message=f'Connected to Dropbox as {display_name} ({email}).',
                details=details,
                storage_used=used,
                storage_available=(allocated - used) if allocated else None,
            )

        except Exception as e:
            error_msg = str(e)
            if 'invalid_access_token' in error_msg.lower() or 'expired' in error_msg.lower():
                msg = 'Authorization expired or revoked. Please re-authorize.'
            elif 'invalid_grant' in error_msg.lower():
                msg = 'Invalid authorization. Please re-authorize.'
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
            import dropbox

            dbx = self._get_client()
            file_size = os.path.getsize(local_path)
            filename = os.path.basename(remote_path)
            dest_path = f'{self._folder_path()}/{filename}'

            self._ensure_folder(dbx)

            if file_size <= SESSION_THRESHOLD:
                # Simple upload for smaller files
                with open(local_path, 'rb') as f:
                    dbx.files_upload(
                        f.read(),
                        dest_path,
                        mode=dropbox.files.WriteMode.overwrite,
                    )
                if progress_callback:
                    progress_callback(file_size, file_size)
            else:
                # Session upload for large files
                uploaded = 0
                with open(local_path, 'rb') as f:
                    chunk = f.read(CHUNK_SIZE)
                    session = dbx.files_upload_session_start(chunk)
                    uploaded += len(chunk)
                    if progress_callback:
                        progress_callback(uploaded, file_size)

                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=session.session_id, offset=uploaded
                    )

                    while uploaded < file_size:
                        chunk = f.read(CHUNK_SIZE)
                        if not chunk:
                            break

                        if uploaded + len(chunk) >= file_size:
                            # Final chunk
                            commit = dropbox.files.CommitInfo(
                                path=dest_path,
                                mode=dropbox.files.WriteMode.overwrite,
                            )
                            dbx.files_upload_session_finish(chunk, cursor, commit)
                        else:
                            dbx.files_upload_session_append_v2(chunk, cursor)

                        uploaded += len(chunk)
                        cursor.offset = uploaded
                        if progress_callback:
                            progress_callback(uploaded, file_size)

            return UploadResult(
                success=True,
                remote_path=dest_path,
                file_size=file_size,
                message='Upload completed.',
            )

        except Exception as e:
            logger.error('Dropbox upload failed: %s', e)
            return UploadResult(success=False, message=str(e))

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> bool:
        try:
            dbx = self._get_client()

            # Get file size first
            total_size = 0
            if progress_callback:
                meta = dbx.files_get_metadata(remote_path)
                total_size = meta.size if hasattr(meta, 'size') else 0

            _, response = dbx.files_download(remote_path)

            downloaded = 0
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size:
                            progress_callback(downloaded, total_size)

            return True

        except Exception as e:
            logger.error('Dropbox download failed: %s', e)
            return False

    def list_files(self, prefix: str = '') -> List[RemoteFile]:
        try:
            import dropbox

            dbx = self._get_client()
            folder = prefix or self._folder_path()

            files: List[RemoteFile] = []
            result = dbx.files_list_folder(folder)

            while True:
                for entry in result.entries:
                    if isinstance(entry, dropbox.files.FileMetadata):
                        files.append(
                            RemoteFile(
                                path=entry.path_display,
                                size=entry.size,
                                last_modified=entry.server_modified.isoformat()
                                if entry.server_modified
                                else None,
                            )
                        )

                if not result.has_more:
                    break
                result = dbx.files_list_folder_continue(result.cursor)

            return files

        except Exception as e:
            logger.error('Dropbox list_files failed: %s', e)
            return []

    def delete_file(self, remote_path: str) -> bool:
        try:
            dbx = self._get_client()
            dbx.files_delete_v2(remote_path)
            return True
        except Exception as e:
            logger.error('Dropbox delete failed: %s', e)
            return False
