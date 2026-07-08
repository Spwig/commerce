"""
Docker container management utilities for the translation service
"""
import subprocess
import json
import logging
from typing import Dict, Optional, List, Tuple

from django.conf import settings

logger = logging.getLogger(__name__)


class DockerManager:
    """Manages Docker containers for the translation service"""

    CONTAINER_NAME = "shop-translator-1"  # Default docker-compose naming (with hyphens)
    SERVICE_NAME = "translator"
    COMPOSE_FILE = "docker-compose.yml"

    @classmethod
    def check_docker_installed(cls) -> bool:
        """Check if Docker is installed and accessible"""
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @classmethod
    def check_docker_compose_installed(cls) -> bool:
        """Check if Docker Compose is installed"""
        try:
            # Try docker-compose command
            result = subprocess.run(
                ['docker-compose', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True

            # Try docker compose command (newer version)
            result = subprocess.run(
                ['docker', 'compose', 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @classmethod
    def get_container_status(cls) -> Dict[str, any]:
        """Get the status of the translator container"""
        try:
            # Try to find container by name or service
            result = subprocess.run(
                ['docker', 'ps', '-a', '--filter', f'name={cls.CONTAINER_NAME}', '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                return {
                    'exists': False,
                    'running': False,
                    'error': result.stderr
                }

            if not result.stdout.strip():
                # Try alternative name pattern
                result = subprocess.run(
                    ['docker', 'ps', '-a', '--filter', f'name={cls.SERVICE_NAME}', '--format', 'json'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

            if result.stdout.strip():
                # Parse the JSON output (one container per line)
                container_info = json.loads(result.stdout.strip().split('\n')[0])

                return {
                    'exists': True,
                    'running': 'Up' in container_info.get('Status', ''),
                    'container_id': container_info.get('ID', ''),
                    'name': container_info.get('Names', ''),
                    'status': container_info.get('Status', ''),
                    'state': container_info.get('State', ''),
                    'ports': container_info.get('Ports', ''),
                    'created': container_info.get('CreatedAt', ''),
                }

            return {
                'exists': False,
                'running': False,
                'message': 'Container not found'
            }

        except subprocess.TimeoutExpired:
            return {
                'exists': False,
                'running': False,
                'error': 'Docker command timed out'
            }
        except Exception as e:
            logger.error(f"Error checking container status: {e}")
            return {
                'exists': False,
                'running': False,
                'error': str(e)
            }

    @classmethod
    def start_container(cls) -> Tuple[bool, str]:
        """Start the translator Docker container"""
        try:
            status = cls.get_container_status()

            if status.get('running'):
                return True, "Container is already running"

            if status.get('exists'):
                # Container exists but stopped, start it
                result = subprocess.run(
                    ['docker', 'start', status.get('container_id', cls.CONTAINER_NAME)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    return True, "Container started successfully"
                else:
                    return False, f"Failed to start container: {result.stderr}"
            else:
                # Container doesn't exist, try docker-compose
                return cls.start_with_compose()

        except subprocess.TimeoutExpired:
            return False, "Starting container timed out"
        except Exception as e:
            logger.error(f"Error starting container: {e}")
            return False, str(e)

    @classmethod
    def start_with_compose(cls) -> Tuple[bool, str]:
        """Start the translator service using docker-compose"""
        try:
            # Try docker-compose command
            result = subprocess.run(
                ['docker-compose', '-f', cls.COMPOSE_FILE, 'up', '-d', cls.SERVICE_NAME],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(settings.BASE_DIR)  # Run compose from the Django project root
            )

            if result.returncode != 0:
                # Try docker compose (newer syntax)
                result = subprocess.run(
                    ['docker', 'compose', '-f', cls.COMPOSE_FILE, 'up', '-d', cls.SERVICE_NAME],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(settings.BASE_DIR)
                )

            if result.returncode == 0:
                return True, "Translator service started with docker-compose"
            else:
                return False, f"Failed to start with docker-compose: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Docker-compose command timed out"
        except Exception as e:
            logger.error(f"Error starting with docker-compose: {e}")
            return False, str(e)

    @classmethod
    def stop_container(cls) -> Tuple[bool, str]:
        """Stop the translator Docker container"""
        try:
            status = cls.get_container_status()

            if not status.get('running'):
                return True, "Container is not running"

            container_id = status.get('container_id', cls.CONTAINER_NAME)

            result = subprocess.run(
                ['docker', 'stop', container_id],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return True, "Container stopped successfully"
            else:
                return False, f"Failed to stop container: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Stopping container timed out"
        except Exception as e:
            logger.error(f"Error stopping container: {e}")
            return False, str(e)

    @classmethod
    def restart_container(cls) -> Tuple[bool, str]:
        """Restart the translator Docker container"""
        try:
            # First stop
            stop_success, stop_msg = cls.stop_container()
            if not stop_success and "not running" not in stop_msg.lower():
                return False, f"Failed to stop: {stop_msg}"

            # Then start
            start_success, start_msg = cls.start_container()
            if start_success:
                return True, "Container restarted successfully"
            else:
                return False, f"Failed to start: {start_msg}"

        except Exception as e:
            logger.error(f"Error restarting container: {e}")
            return False, str(e)

    @classmethod
    def get_container_logs(cls, lines: int = 50) -> str:
        """Get recent logs from the translator container"""
        try:
            status = cls.get_container_status()

            if not status.get('exists'):
                return "Container does not exist"

            container_id = status.get('container_id', cls.CONTAINER_NAME)

            result = subprocess.run(
                ['docker', 'logs', '--tail', str(lines), container_id],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return result.stdout or "No logs available"
            else:
                return f"Failed to get logs: {result.stderr}"

        except subprocess.TimeoutExpired:
            return "Getting logs timed out"
        except Exception as e:
            logger.error(f"Error getting container logs: {e}")
            return str(e)

    @classmethod
    def pull_image(cls) -> Tuple[bool, str]:
        """Pull the latest translator Docker image"""
        try:
            # Check docker-compose.yml for image name
            result = subprocess.run(
                ['docker-compose', '-f', cls.COMPOSE_FILE, 'pull', cls.SERVICE_NAME],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout for pulling
                cwd=str(settings.BASE_DIR)
            )

            if result.returncode != 0:
                # Try docker compose (newer syntax)
                result = subprocess.run(
                    ['docker', 'compose', '-f', cls.COMPOSE_FILE, 'pull', cls.SERVICE_NAME],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=str(settings.BASE_DIR)
                )

            if result.returncode == 0:
                return True, "Image pulled successfully"
            else:
                return False, f"Failed to pull image: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Pulling image timed out (may still be downloading)"
        except Exception as e:
            logger.error(f"Error pulling image: {e}")
            return False, str(e)