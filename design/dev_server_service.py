"""
Theme SDK Development Server Service.

Handles business logic for theme development including:
- Session management
- File synchronization
- CSS compilation
- Hot reload notifications
- Theme validation
"""

import os
import json
import hashlib
import shutil
import logging
import queue
import threading
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate

from .models import DevSession
from .theme_service import ThemeService

logger = logging.getLogger(__name__)


class DevServerService:
    """Service for managing theme development sessions and file sync."""

    # Queue for SSE hot reload notifications
    _reload_queues: Dict[str, queue.Queue] = {}
    _queue_lock = threading.Lock()

    def __init__(self):
        self.theme_service = ThemeService()
        self.dev_themes_dir = self._get_dev_themes_dir()

    def _get_dev_themes_dir(self) -> Path:
        """Get the directory for development themes."""
        dev_dir = getattr(
            settings,
            'THEME_DEV_DIR',
            settings.BASE_DIR / 'theme_dev'
        )
        Path(dev_dir).mkdir(parents=True, exist_ok=True)
        return Path(dev_dir)

    # ========== Session Management ==========

    def create_session(
        self,
        user,
        theme_name: str,
        theme_path: str = '',
        client_info: dict = None
    ) -> DevSession:
        """
        Create a new development session.

        Args:
            user: Authenticated staff user
            theme_name: Name of theme being developed
            theme_path: Local path on developer's machine
            client_info: CLI version, OS info, etc.

        Returns:
            DevSession instance with generated token
        """
        # Deactivate any existing sessions for this user/theme
        DevSession.objects.filter(
            user=user,
            theme_name=theme_name,
            is_active=True
        ).update(is_active=False)

        # Create new session
        session = DevSession.objects.create(
            user=user,
            theme_name=theme_name,
            theme_path=theme_path,
            client_info=client_info or {}
        )

        # Create dev theme directory
        theme_dev_path = self.dev_themes_dir / session.token
        theme_dev_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Created dev session for {theme_name} by {user.username}")
        return session

    def validate_token(self, token: str) -> Optional[DevSession]:
        """
        Validate a session token and return the session if valid.

        Args:
            token: Session authentication token

        Returns:
            DevSession if valid, None otherwise
        """
        try:
            session = DevSession.objects.get(token=token)
            if session.is_valid():
                # Refresh expiry on each valid access
                session.refresh_expiry()
                return session
            return None
        except DevSession.DoesNotExist:
            return None

    def end_session(self, session: DevSession) -> bool:
        """
        End a development session and cleanup.

        Args:
            session: DevSession to end

        Returns:
            True if successful
        """
        # Cleanup dev theme directory
        theme_dev_path = self.dev_themes_dir / session.token
        if theme_dev_path.exists():
            shutil.rmtree(theme_dev_path)

        # Remove SSE queue
        self._remove_reload_queue(session.token)

        # Deactivate session
        session.deactivate()

        logger.info(f"Ended dev session for {session.theme_name}")
        return True

    def get_session_status(self, session: DevSession) -> dict:
        """Get current session status."""
        return {
            'token': session.token,
            'theme_name': session.theme_name,
            'is_active': session.is_active,
            'is_expired': session.is_expired(),
            'last_sync': session.last_sync.isoformat() if session.last_sync else None,
            'synced_files_count': len(session.synced_files),
            'created_at': session.created_at.isoformat(),
            'expires_at': session.expires_at.isoformat(),
        }

    # ========== File Synchronization ==========

    def sync_files(
        self,
        session: DevSession,
        files: List[Dict[str, Any]]
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Sync files from SDK to dev server.

        Args:
            session: Active dev session
            files: List of file dicts with 'path', 'content', 'checksum'

        Returns:
            Tuple of (success, result_dict)
        """
        theme_dev_path = self.dev_themes_dir / session.token
        synced = {}
        errors = []
        css_changed = False
        template_changed = False

        for file_data in files:
            file_path = file_data.get('path', '')
            content = file_data.get('content', '')
            checksum = file_data.get('checksum', '')

            # Validate file path (prevent directory traversal)
            if '..' in file_path or file_path.startswith('/'):
                errors.append(f"Invalid file path: {file_path}")
                continue

            # Determine file type for reload strategy
            if file_path.endswith('.css'):
                css_changed = True
            elif file_path.endswith(('.html', '.json')):
                template_changed = True

            # Write file
            full_path = theme_dev_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                # Handle binary vs text content
                if isinstance(content, bytes):
                    full_path.write_bytes(content)
                else:
                    full_path.write_text(content, encoding='utf-8')

                synced[file_path] = checksum
                logger.debug(f"Synced file: {file_path}")

            except Exception as e:
                errors.append(f"Failed to write {file_path}: {str(e)}")
                logger.error(f"Failed to sync file {file_path}: {e}")

        # Update session
        session.update_sync(synced)

        # Trigger appropriate reload
        if css_changed:
            self._notify_reload(session.token, 'css')
        elif template_changed:
            self._notify_reload(session.token, 'full')

        result = {
            'synced': list(synced.keys()),
            'errors': errors,
            'reload_type': 'css' if css_changed else ('full' if template_changed else 'none')
        }

        return len(errors) == 0, result

    def sync_full_theme(
        self,
        session: DevSession,
        theme_archive: bytes
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Sync complete theme archive (ZIP).

        Args:
            session: Active dev session
            theme_archive: ZIP file bytes

        Returns:
            Tuple of (success, result_dict)
        """
        import zipfile
        import io

        theme_dev_path = self.dev_themes_dir / session.token

        # Clear existing files
        if theme_dev_path.exists():
            shutil.rmtree(theme_dev_path)
        theme_dev_path.mkdir(parents=True)

        try:
            # Extract archive
            with zipfile.ZipFile(io.BytesIO(theme_archive)) as zf:
                zf.extractall(theme_dev_path)

            # Build file list with checksums
            synced = {}
            for file_path in theme_dev_path.rglob('*'):
                if file_path.is_file():
                    rel_path = str(file_path.relative_to(theme_dev_path))
                    checksum = hashlib.sha256(file_path.read_bytes()).hexdigest()
                    synced[rel_path] = checksum

            session.update_sync(synced)

            # Trigger full reload
            self._notify_reload(session.token, 'full')

            return True, {
                'synced': list(synced.keys()),
                'file_count': len(synced)
            }

        except Exception as e:
            logger.error(f"Failed to sync full theme: {e}")
            return False, {'error': str(e)}

    def get_dev_theme_path(self, session: DevSession) -> Path:
        """Get the path to a session's dev theme directory."""
        return self.dev_themes_dir / session.token

    # ========== Hot Reload (SSE) ==========

    def _get_reload_queue(self, token: str) -> queue.Queue:
        """Get or create SSE queue for a session."""
        with self._queue_lock:
            if token not in self._reload_queues:
                self._reload_queues[token] = queue.Queue()
            return self._reload_queues[token]

    def _remove_reload_queue(self, token: str):
        """Remove SSE queue for a session."""
        with self._queue_lock:
            self._reload_queues.pop(token, None)

    def _notify_reload(self, token: str, reload_type: str):
        """
        Send reload notification to connected browsers.

        Args:
            token: Session token
            reload_type: 'css' for CSS-only, 'full' for full page reload
        """
        q = self._get_reload_queue(token)
        event = {
            'type': reload_type,
            'timestamp': timezone.now().isoformat()
        }
        q.put(event)
        logger.debug(f"Queued {reload_type} reload for session {token[:8]}...")

    def get_reload_events(self, token: str, timeout: float = 30.0):
        """
        Generator for SSE reload events.

        Args:
            token: Session token
            timeout: Seconds to wait for events

        Yields:
            Event dicts as they arrive
        """
        q = self._get_reload_queue(token)

        while True:
            try:
                event = q.get(timeout=timeout)
                yield event
            except queue.Empty:
                # Send keepalive
                yield {'type': 'keepalive'}

    # ========== CSS Compilation ==========

    def compile_css(self, session: DevSession) -> Tuple[bool, str]:
        """
        Compile CSS for the dev theme.

        Args:
            session: Active dev session

        Returns:
            Tuple of (success, css_url or error_message)
        """
        theme_dev_path = self.dev_themes_dir / session.token

        try:
            # Read design tokens from dev theme
            tokens_path = theme_dev_path / 'design_tokens.json'
            if not tokens_path.exists():
                return False, "design_tokens.json not found"

            tokens = json.loads(tokens_path.read_text())

            # Generate CSS from tokens
            css = self._generate_css_from_tokens(tokens)

            # Write to static-servable location
            css_output_path = theme_dev_path / 'compiled' / 'theme.css'
            css_output_path.parent.mkdir(parents=True, exist_ok=True)
            css_output_path.write_text(css)

            # Return URL
            css_url = f"/api/theme-dev/static/{session.token}/compiled/theme.css"
            return True, css_url

        except Exception as e:
            logger.error(f"CSS compilation failed: {e}")
            return False, str(e)

    def _generate_css_from_tokens(self, tokens: dict) -> str:
        """Generate CSS custom properties from design tokens."""
        css_lines = [':root {']

        # Colors
        colors = tokens.get('colors', {})
        for name, value in colors.items():
            css_lines.append(f'  --color-{name}: {value};')

        # Typography
        typography = tokens.get('typography', {})
        for name, value in typography.items():
            css_lines.append(f'  --font-{name}: {value};')

        # Spacing
        spacing = tokens.get('spacing', {})
        if isinstance(spacing.get('scale'), list):
            for i, value in enumerate(spacing['scale']):
                css_lines.append(f'  --spacing-{i}: {value};')

        css_lines.append('}')
        return '\n'.join(css_lines)

    # ========== Validation ==========

    def validate_theme(self, session: DevSession) -> Dict[str, Any]:
        """
        Validate the dev theme structure and files.

        Args:
            session: Active dev session

        Returns:
            Validation result dict with errors and warnings
        """
        theme_dev_path = self.dev_themes_dir / session.token
        errors = []
        warnings = []

        # Check required files
        required_files = ['manifest.json', 'design_tokens.json']
        for filename in required_files:
            if not (theme_dev_path / filename).exists():
                errors.append(f"Missing required file: {filename}")

        # Validate manifest
        manifest_path = theme_dev_path / 'manifest.json'
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())

                # Check required fields
                required_fields = ['name', 'version', 'spwig_version']
                for field in required_fields:
                    if field not in manifest:
                        errors.append(f"Manifest missing required field: {field}")

                # Check bundled components
                for component in manifest.get('bundled_components', []):
                    component_path = theme_dev_path / component.get('path', '')
                    if not component_path.exists():
                        errors.append(f"Bundled component not found: {component.get('name')}")

            except json.JSONDecodeError as e:
                errors.append(f"Invalid manifest.json: {e}")

        # Validate design tokens
        tokens_path = theme_dev_path / 'design_tokens.json'
        if tokens_path.exists():
            try:
                tokens = json.loads(tokens_path.read_text())

                if 'colors' not in tokens:
                    warnings.append("design_tokens.json missing 'colors' section")
                if 'typography' not in tokens:
                    warnings.append("design_tokens.json missing 'typography' section")

            except json.JSONDecodeError as e:
                errors.append(f"Invalid design_tokens.json: {e}")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'error_count': len(errors),
            'warning_count': len(warnings)
        }

    # ========== Component Operations ==========

    def list_components(self, session: DevSession) -> List[Dict[str, Any]]:
        """List components in the dev theme."""
        theme_dev_path = self.dev_themes_dir / session.token
        components = []

        # Read manifest for bundled components
        manifest_path = theme_dev_path / 'manifest.json'
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())

                for component in manifest.get('bundled_components', []):
                    component_path = theme_dev_path / component.get('path', '')
                    component_manifest_path = component_path / 'manifest.json'

                    comp_info = {
                        'name': component.get('name'),
                        'type': component.get('type'),
                        'path': component.get('path'),
                        'exists': component_path.exists()
                    }

                    # Read component manifest if exists
                    if component_manifest_path.exists():
                        comp_manifest = json.loads(component_manifest_path.read_text())
                        comp_info['version'] = comp_manifest.get('version')
                        comp_info['display_name'] = comp_manifest.get('display_name')

                    components.append(comp_info)

            except json.JSONDecodeError:
                pass

        return components

    def get_component(self, session: DevSession, component_name: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific component."""
        components = self.list_components(session)
        for comp in components:
            if comp.get('name') == component_name:
                # Add full component data
                theme_dev_path = self.dev_themes_dir / session.token
                component_path = theme_dev_path / comp.get('path', '')

                if component_path.exists():
                    comp['files'] = [
                        str(f.relative_to(component_path))
                        for f in component_path.rglob('*')
                        if f.is_file()
                    ]

                return comp
        return None


# Singleton instance
_dev_server_service = None


def get_dev_server_service() -> DevServerService:
    """Get the singleton DevServerService instance."""
    global _dev_server_service
    if _dev_server_service is None:
        _dev_server_service = DevServerService()
    return _dev_server_service
