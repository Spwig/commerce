"""
SFTP storage provider using paramiko.
"""
import io
import logging
import os
import stat
from typing import Any, Callable, Dict, List, Optional

from .base import (
    BaseStorageProvider,
    ConnectionTestResult,
    RemoteFile,
    UploadResult,
)

logger = logging.getLogger(__name__)


class SFTPStorageProvider(BaseStorageProvider):
    provider_type = 'sftp'
    provider_name = 'SFTP'

    credential_fields = [
        {
            'key': 'hostname',
            'label': 'Hostname',
            'secret': False,
            'required': True,
            'type': 'text',
            'help_text': 'Server hostname or IP address.',
        },
        {
            'key': 'port',
            'label': 'Port',
            'secret': False,
            'required': True,
            'type': 'number',
            'default': '22',
        },
        {
            'key': 'username',
            'label': 'Username',
            'secret': False,
            'required': True,
            'type': 'text',
        },
        {
            'key': 'password',
            'label': 'Password',
            'secret': True,
            'required': False,
            'type': 'password',
            'help_text': 'Either password or SSH private key is required.',
        },
        {
            'key': 'private_key',
            'label': 'SSH Private Key',
            'secret': True,
            'required': False,
            'type': 'textarea',
            'help_text': 'Paste PEM-formatted private key. Leave blank to use password.',
        },
    ]

    settings_fields = [
        {
            'key': 'remote_directory',
            'label': 'Remote Directory',
            'type': 'text',
            'required': True,
            'default': '/backups/spwig/',
            'help_text': 'Absolute path on the remote server.',
        },
    ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self):
        """Return (SSHClient, SFTPClient) tuple. Caller must close."""
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        hostname = self.credentials.get('hostname', '')
        port = int(self.credentials.get('port', 22))
        username = self.credentials.get('username', '')
        password = self.credentials.get('password')
        private_key_str = self.credentials.get('private_key')

        connect_kwargs = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'timeout': 30,
        }

        if private_key_str:
            key_file = io.StringIO(private_key_str)
            try:
                pkey = paramiko.RSAKey.from_private_key(key_file)
            except paramiko.SSHException:
                key_file.seek(0)
                try:
                    pkey = paramiko.Ed25519Key.from_private_key(key_file)
                except paramiko.SSHException:
                    key_file.seek(0)
                    pkey = paramiko.ECDSAKey.from_private_key(key_file)
            connect_kwargs['pkey'] = pkey
        elif password:
            connect_kwargs['password'] = password
        else:
            raise ValueError('Either password or SSH private key is required.')

        ssh.connect(**connect_kwargs)
        sftp = ssh.open_sftp()
        return ssh, sftp

    def _ensure_remote_dir(self, sftp, path: str):
        """Recursively create remote directories if they don't exist."""
        dirs_to_create = []
        current = path
        while current and current != '/':
            try:
                sftp.stat(current)
                break
            except FileNotFoundError:
                dirs_to_create.append(current)
                current = os.path.dirname(current)

        for d in reversed(dirs_to_create):
            sftp.mkdir(d)

    def _remote_dir(self) -> str:
        d = self.settings.get('remote_directory', '/backups/spwig/')
        if d and not d.endswith('/'):
            d += '/'
        return d

    # ------------------------------------------------------------------
    # ABC implementation
    # ------------------------------------------------------------------

    def test_connection(self) -> ConnectionTestResult:
        ssh = sftp = None
        try:
            ssh, sftp = self._connect()
            remote_dir = self._remote_dir()

            # Ensure remote directory exists
            self._ensure_remote_dir(sftp, remote_dir.rstrip('/'))

            # Write + read + delete test file
            test_path = remote_dir + '.spwig_connection_test'
            with sftp.open(test_path, 'w') as f:
                f.write('spwig-connection-test')

            sftp.stat(test_path)
            sftp.remove(test_path)

            # Get disk info via SSH if available
            details = {
                'hostname': self.credentials.get('hostname'),
                'remote_directory': remote_dir,
            }
            try:
                _, stdout, _ = ssh.exec_command(f'df -B1 {remote_dir}')
                output = stdout.read().decode().strip().split('\n')
                if len(output) >= 2:
                    parts = output[1].split()
                    if len(parts) >= 4:
                        details['disk_total'] = int(parts[1])
                        details['disk_available'] = int(parts[3])
            except Exception:
                pass

            return ConnectionTestResult(
                success=True,
                message=f'Successfully connected to {self.credentials.get("hostname")}.',
                details=details,
                storage_used=details.get('disk_total', 0) - details.get('disk_available', 0)
                if 'disk_total' in details
                else None,
                storage_available=details.get('disk_available'),
            )

        except Exception as e:
            error_msg = str(e)
            if 'Authentication failed' in error_msg:
                msg = 'Authentication failed. Check username, password, or SSH key.'
            elif 'No existing session' in error_msg or 'Error reading SSH' in error_msg:
                msg = 'Could not connect to the server. Check hostname and port.'
            elif 'timed out' in error_msg.lower():
                msg = 'Connection timed out. Check hostname, port, and firewall rules.'
            else:
                msg = f'Connection failed: {error_msg}'
            return ConnectionTestResult(success=False, message=msg)

        finally:
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()

    def upload_file(
        self,
        local_path: str,
        remote_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> UploadResult:
        ssh = sftp = None
        try:
            ssh, sftp = self._connect()
            file_size = os.path.getsize(local_path)

            # Ensure target directory exists
            remote_dir = os.path.dirname(remote_path)
            if remote_dir:
                self._ensure_remote_dir(sftp, remote_dir)

            callback = None
            if progress_callback:
                def callback(bytes_transferred, total_bytes):
                    progress_callback(bytes_transferred, total_bytes)

            sftp.put(local_path, remote_path, callback=callback)

            return UploadResult(
                success=True,
                remote_path=remote_path,
                file_size=file_size,
                message='Upload completed.',
            )

        except Exception as e:
            logger.error('SFTP upload failed: %s', e)
            return UploadResult(success=False, message=str(e))

        finally:
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> bool:
        ssh = sftp = None
        try:
            ssh, sftp = self._connect()

            total_size = 0
            if progress_callback:
                file_stat = sftp.stat(remote_path)
                total_size = file_stat.st_size or 0

            callback = None
            if progress_callback and total_size:
                def callback(bytes_transferred, total_bytes):
                    progress_callback(bytes_transferred, total_bytes)

            sftp.get(remote_path, local_path, callback=callback)
            return True

        except Exception as e:
            logger.error('SFTP download failed: %s', e)
            return False

        finally:
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()

    def list_files(self, prefix: str = '') -> List[RemoteFile]:
        ssh = sftp = None
        try:
            ssh, sftp = self._connect()
            remote_dir = prefix or self._remote_dir().rstrip('/')

            files: List[RemoteFile] = []
            for entry in sftp.listdir_attr(remote_dir):
                if stat.S_ISREG(entry.st_mode or 0):
                    from datetime import datetime, timezone

                    mtime = None
                    if entry.st_mtime:
                        mtime = datetime.fromtimestamp(
                            entry.st_mtime, tz=timezone.utc
                        ).isoformat()

                    files.append(
                        RemoteFile(
                            path=f'{remote_dir}/{entry.filename}',
                            size=entry.st_size or 0,
                            last_modified=mtime,
                        )
                    )
            return files

        except Exception as e:
            logger.error('SFTP list_files failed: %s', e)
            return []

        finally:
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()

    def delete_file(self, remote_path: str) -> bool:
        ssh = sftp = None
        try:
            ssh, sftp = self._connect()
            sftp.remove(remote_path)
            return True

        except Exception as e:
            logger.error('SFTP delete failed: %s', e)
            return False

        finally:
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()
