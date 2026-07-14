"""
Docker Log Service

Service for streaming and parsing Docker container logs.
Connects to Docker socket, streams logs from containers,
parses log lines, and stores in Redis for real-time access.
"""

import json
import logging
import os
import re
from datetime import datetime

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class DockerLogService:
    """
    Service for streaming and parsing Docker container logs.

    Connects to Docker socket, streams logs from containers,
    parses log lines, and stores in Redis.
    """

    # Container prefix - read from environment (set by docker-compose from .env)
    # Default 'spwig' matches production deployment
    CONTAINER_PREFIX = os.environ.get("CONTAINER_PREFIX", "spwig")

    # Service names and display labels - match docker-compose service names
    # Container naming pattern: {CONTAINER_PREFIX}_{service} (e.g., spwig_db)
    CONTAINER_SERVICES = {
        "db": "PostgreSQL",
        "redis": "Redis",
        "minio": "MinIO",
        "shop": "Spwig Web",
        "celery": "Celery Worker",
        "celery_beat": "Celery Beat",
        "translator": "Translator",
        "nginx": "Nginx",
        "upgrader": "Upgrader",
    }

    # Service name aliases for cross-environment compatibility
    # Dev docker-compose uses different service names than production
    SERVICE_ALIASES = {
        "shop": ["web"],
        "celery": ["celery_worker"],
    }

    # Log level patterns for different container types
    LOG_PATTERNS = {
        "default": re.compile(
            r"(?P<timestamp>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.,]?\d*Z?)\s*"
            r"(?:-\s*)?(?P<level>INFO|WARNING|ERROR|CRITICAL|DEBUG|WARN)\s*"
            r"(?:-\s*)?(?P<message>.*)",
            re.IGNORECASE,
        ),
        "nginx": re.compile(
            r"(?P<ip>\d+\.\d+\.\d+\.\d+)\s*-\s*-\s*"
            r"\[(?P<timestamp>[^\]]+)\]\s*"
            r'"(?P<method>\w+)\s+(?P<path>[^\s]+)[^"]*"\s*'
            r"(?P<status>\d+)\s*(?P<size>\d+)",
        ),
        "postgres": re.compile(
            r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+\s+\w+)\s*"
            r"\[(?P<pid>\d+)\]\s*(?P<level>\w+):\s*(?P<message>.*)",
        ),
        "django": re.compile(
            r"(?P<level>INFO|WARNING|ERROR|CRITICAL|DEBUG)\s+"
            r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+)\s+"
            r"(?P<module>\S+)\s+"
            r"(?P<message>.*)",
            re.IGNORECASE,
        ),
        "celery": re.compile(
            r"\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+):\s*"
            r"(?P<level>\w+)/[\w-]+\]\s*(?P<message>.*)",
        ),
    }

    # Pre-compiled sanitization patterns for sensitive data redaction
    SANITIZE_PATTERNS = [
        (re.compile(r"password[=:]\s*[^\s,;]+", re.IGNORECASE), "password=***REDACTED***"),
        (re.compile(r"token[=:]\s*[^\s,;]+", re.IGNORECASE), "token=***REDACTED***"),
        (re.compile(r"secret[=:]\s*[^\s,;]+", re.IGNORECASE), "secret=***REDACTED***"),
        (re.compile(r"api[_-]?key[=:]\s*[^\s,;]+", re.IGNORECASE), "api_key=***REDACTED***"),
        (
            re.compile(r"authorization:\s*bearer\s+[^\s,;]+", re.IGNORECASE),
            "Authorization: Bearer ***REDACTED***",
        ),
        (
            re.compile(r"access[_-]?token[=:]\s*[^\s,;]+", re.IGNORECASE),
            "access_token=***REDACTED***",
        ),
        (
            re.compile(r"refresh[_-]?token[=:]\s*[^\s,;]+", re.IGNORECASE),
            "refresh_token=***REDACTED***",
        ),
        (
            re.compile(r"client[_-]?secret[=:]\s*[^\s,;]+", re.IGNORECASE),
            "client_secret=***REDACTED***",
        ),
        (
            re.compile(r"private[_-]?key[=:]\s*[^\s,;]+", re.IGNORECASE),
            "private_key=***REDACTED***",
        ),
    ]

    # Redis key patterns
    REDIS_LOG_KEY = "logs:{container}"  # List of log entries
    REDIS_STATS_KEY = "log_stats:{container}"  # Hash of level counts
    REDIS_GLOBAL_STATS_KEY = "log_stats:global"  # Global counts
    REDIS_POSITION_KEY = "log_stream:position:{container}"  # Last read position

    def __init__(self):
        self._docker_client = None
        self._redis_client = None
        self._settings = None

    @property
    def log_settings(self):
        """Get log viewer settings (cached)"""
        if self._settings is None:
            from management.models import LogViewerSettings

            self._settings = LogViewerSettings.get_instance()
        return self._settings

    def get_docker_client(self):
        """Get Docker client, connecting to socket"""
        if self._docker_client is None:
            try:
                import docker

                # Connect via Unix socket (mounted in docker-compose)
                self._docker_client = docker.from_env()
            except ImportError:
                logger.error("Docker SDK not installed. Install with: pip install docker")
                raise
            except Exception as e:
                logger.error(f"Failed to connect to Docker: {e}")
                raise
        return self._docker_client

    def get_redis_client(self):
        """Get Redis client for log storage"""
        if self._redis_client is None:
            import redis as redis_lib

            # Parse Redis URL from Django cache settings
            redis_location = settings.CACHES.get("default", {}).get(
                "LOCATION", "redis://redis:6379/1"
            )
            if "://" in redis_location:
                self._redis_client = redis_lib.from_url(redis_location, decode_responses=True)
            else:
                # Fallback for simple host:port format
                host = getattr(settings, "REDIS_HOST", "redis")
                port = getattr(settings, "REDIS_PORT", 6379)
                self._redis_client = redis_lib.Redis(
                    host=host, port=port, db=1, decode_responses=True
                )
        return self._redis_client

    def get_container(self, service_name: str):
        """Get container by service name using multiple discovery strategies.

        Tries in order:
        1. Explicit name: {CONTAINER_PREFIX}_{service} (production naming)
        2. Service name directly (legacy fallback)
        3. Docker Compose service label (works with auto-generated names)
        4. Service aliases (handles dev/prod name differences)
        """
        try:
            client = self.get_docker_client()
        except Exception as e:
            logger.warning(f"Docker client not available: {e}")
            return None

        # Strategy 1: Container name = {prefix}_{service} (e.g., spwig_db)
        container_name = f"{self.CONTAINER_PREFIX}_{service_name}"
        try:
            return client.containers.get(container_name)
        except Exception:
            pass

        # Strategy 2: try service name directly
        try:
            return client.containers.get(service_name)
        except Exception:
            pass

        # Strategy 3: Filter by Docker Compose service label
        # Docker Compose V2 adds com.docker.compose.service labels
        names_to_try = [service_name] + self.SERVICE_ALIASES.get(service_name, [])
        for name in names_to_try:
            try:
                containers = client.containers.list(
                    all=True, filters={"label": f"com.docker.compose.service={name}"}
                )
                if containers:
                    return containers[0]
            except Exception:
                pass

        logger.debug(f"Container not found: {service_name}")
        return None

    def parse_log_line(self, line: str, container_type: str) -> dict | None:
        """Parse a log line and extract level, timestamp, message"""
        line = line.strip()
        if not line:
            return None

        # Remove Docker timestamp prefix if present (format: 2024-01-15T10:30:00.123456789Z)
        docker_ts_match = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z?)\s+(.*)$", line)
        if docker_ts_match:
            timestamp_str = docker_ts_match.group(1)
            line = docker_ts_match.group(2)
        else:
            timestamp_str = timezone.now().isoformat()

        # Default values
        level = "INFO"
        message = line

        # Determine which pattern to use based on service name
        if container_type in ["nginx"]:
            pattern_name = "nginx"
        elif container_type in ["db"]:
            pattern_name = "postgres"
        elif container_type in ["celery", "celery_beat"]:
            pattern_name = "celery"
        elif container_type in ["shop"]:
            pattern_name = "django"
        else:
            pattern_name = "default"

        pattern = self.LOG_PATTERNS.get(pattern_name, self.LOG_PATTERNS["default"])
        match = pattern.match(line)

        if match:
            groups = match.groupdict()
            if "timestamp" in groups:
                timestamp_str = groups["timestamp"]
            if "level" in groups:
                level = groups["level"].upper()
            if "message" in groups:
                message = groups["message"]

            # Handle nginx access logs - determine level from status code
            if pattern_name == "nginx" and "status" in groups:
                status = int(groups.get("status", 200))
                if status >= 500:
                    level = "ERROR"
                elif status >= 400:
                    level = "WARNING"
                else:
                    level = "INFO"
                message = f"{groups.get('method', 'GET')} {groups.get('path', '/')} {status}"

            # Normalize level names
            if level == "WARN":
                level = "WARNING"
            if level in ("DEBUG", "TRACE", "VERBOSE"):
                return None  # Skip DEBUG level logs
            if level == "FATAL":
                level = "CRITICAL"
        else:
            # Heuristic level detection for unstructured logs
            line_upper = line.upper()
            if any(x in line_upper for x in ["ERROR", "EXCEPTION", "TRACEBACK", "FAILED"]):
                level = "ERROR"
            elif any(x in line_upper for x in ["WARNING", "WARN", "DEPRECATED"]):
                level = "WARNING"
            elif any(x in line_upper for x in ["CRITICAL", "FATAL", "PANIC"]):
                level = "CRITICAL"

        # Ensure level is valid
        if level not in ("INFO", "WARNING", "ERROR", "CRITICAL"):
            level = "INFO"

        return {
            "level": level,
            "timestamp": timestamp_str,
            "message": self.sanitize_message(message),
            "raw_line": line[:2000],  # Truncate very long lines
        }

    def sanitize_message(self, message: str) -> str:
        """Remove sensitive information from log messages"""
        if not message:
            return message

        for compiled_pattern, replacement in self.SANITIZE_PATTERNS:
            message = compiled_pattern.sub(replacement, message)

        # Apply custom patterns from settings
        for pattern in self.log_settings.sensitive_patterns or []:
            try:
                message = re.sub(pattern, "***REDACTED***", message, flags=re.IGNORECASE)
            except re.error:
                logger.warning(f"Invalid regex pattern in settings: {pattern}")

        return message

    def collect_container_logs(self, container_name: str, tail: int = 20) -> int:
        """
        Collect recent logs from a container and store in Redis.
        Uses a Redis pipeline to batch all operations for efficiency.
        Returns the number of logs collected.
        """
        container = self.get_container(container_name)
        if not container:
            return 0

        container_type = container_name.split("_")[0]  # e.g., 'celery' from 'celery_worker'

        # Phase 1: Parse all log lines (no Redis calls)
        parsed_entries = []
        try:
            logs = container.logs(tail=tail, timestamps=True)
            if isinstance(logs, bytes):
                logs = logs.decode("utf-8", errors="replace")

            for line in logs.split("\n"):
                if not line.strip():
                    continue
                parsed = self.parse_log_line(line, container_type)
                if parsed:
                    parsed["container"] = container_name
                    parsed_entries.append(parsed)
        except Exception as e:
            logger.warning(f"Failed to collect logs from {container_name}: {e}")
            return 0

        if not parsed_entries:
            return 0

        # Phase 2: Batch all Redis operations in a single pipeline
        try:
            redis = self.get_redis_client()
            settings_obj = self.log_settings
            key = self.REDIS_LOG_KEY.format(container=container_name)
            stats_key = self.REDIS_STATS_KEY.format(container=container_name)
            ttl = settings_obj.redis_retention_minutes * 60

            pipe = redis.pipeline()
            for entry in parsed_entries:
                pipe.lpush(key, json.dumps(entry))
                pipe.hincrby(stats_key, entry["level"], 1)
                pipe.hincrby(self.REDIS_GLOBAL_STATS_KEY, entry["level"], 1)
                pipe.hincrby(self.REDIS_GLOBAL_STATS_KEY, "total", 1)
            pipe.ltrim(key, 0, settings_obj.max_logs_per_container - 1)
            pipe.expire(key, ttl)
            pipe.expire(stats_key, ttl)
            pipe.expire(self.REDIS_GLOBAL_STATS_KEY, ttl)
            pipe.execute()
        except Exception as e:
            logger.warning(f"Redis pipeline failed for {container_name}: {e}")
            return 0

        return len(parsed_entries)

    def get_recent_logs(
        self,
        container: str | None = None,
        level: str | None = None,
        limit: int = 50,
        offset: int = 0,
        search: str | None = None,
    ) -> list[dict]:
        """Get recent logs from Redis with optional filtering"""
        try:
            redis = self.get_redis_client()
        except Exception as e:
            logger.warning(f"Redis not available: {e}")
            return []

        results = []
        containers = [container] if container else list(self.CONTAINER_SERVICES.keys())

        for c in containers:
            key = self.REDIS_LOG_KEY.format(container=c)
            logs = redis.lrange(key, 0, -1)  # Get all for filtering

            for log_json in logs:
                try:
                    entry = json.loads(log_json)
                    if "container" not in entry:
                        entry["container"] = c

                    # Apply filters
                    if level and entry.get("level") != level:
                        continue
                    if search and search.lower() not in entry.get("message", "").lower():
                        continue

                    results.append(entry)
                except json.JSONDecodeError:
                    continue

        # Sort by timestamp descending
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # Apply pagination
        return results[offset : offset + limit]

    def get_log_stats(self) -> dict:
        """Get log statistics from Redis"""
        try:
            redis = self.get_redis_client()
        except Exception as e:
            logger.warning(f"Redis not available: {e}")
            return {"global": {}, "by_container": {}}

        stats = {
            "global": redis.hgetall(self.REDIS_GLOBAL_STATS_KEY) or {},
            "by_container": {},
        }

        for container in self.CONTAINER_SERVICES:
            key = self.REDIS_STATS_KEY.format(container=container)
            container_stats = redis.hgetall(key)
            if container_stats:
                stats["by_container"][container] = container_stats

        return stats

    def get_container_status(self) -> list[dict]:
        """Get status of all monitored containers as list for template iteration"""
        results = []

        try:
            self.get_docker_client()
        except Exception:
            # Return all containers as unknown if Docker is not available
            for service_name, display_name in self.CONTAINER_SERVICES.items():
                results.append(
                    {
                        "name": service_name,
                        "display_name": display_name,
                        "running": False,
                        "status": "unknown",
                        "started_at": None,
                    }
                )
            return results

        for service_name, display_name in self.CONTAINER_SERVICES.items():
            container = self.get_container(service_name)
            if container:
                try:
                    results.append(
                        {
                            "name": service_name,
                            "display_name": display_name,
                            "running": container.status == "running",
                            "status": container.status,
                            "started_at": container.attrs.get("State", {}).get("StartedAt"),
                        }
                    )
                except Exception:
                    results.append(
                        {
                            "name": service_name,
                            "display_name": display_name,
                            "running": False,
                            "status": "error",
                            "started_at": None,
                        }
                    )
            else:
                results.append(
                    {
                        "name": service_name,
                        "display_name": display_name,
                        "running": False,
                        "status": "not_found",
                        "started_at": None,
                    }
                )

        return results

    def clear_stats(self):
        """Clear all log statistics from Redis"""
        try:
            redis = self.get_redis_client()
        except Exception:
            return

        # Clear global stats
        redis.delete(self.REDIS_GLOBAL_STATS_KEY)

        # Clear per-container stats
        for container in self.CONTAINER_SERVICES:
            redis.delete(self.REDIS_STATS_KEY.format(container=container))

    def archive_logs_to_db(self, batch_size: int = 100) -> int:
        """
        Archive logs from Redis to PostgreSQL using bulk_create.
        Returns the number of logs archived.
        """
        from management.models import LogEntry

        try:
            redis = self.get_redis_client()
        except Exception as e:
            logger.warning(f"Redis not available for archiving: {e}")
            return 0

        entries_to_create = []

        for container in self.CONTAINER_SERVICES:
            key = self.REDIS_LOG_KEY.format(container=container)

            while len(entries_to_create) < batch_size:
                log_json = redis.rpop(key)
                if not log_json:
                    break

                try:
                    entry = json.loads(log_json)

                    timestamp_str = entry.get("timestamp", "")
                    try:
                        if "T" in timestamp_str:
                            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        else:
                            timestamp = timezone.now()
                    except Exception:
                        timestamp = timezone.now()

                    if timezone.is_naive(timestamp):
                        timestamp = timezone.make_aware(timestamp)

                    entries_to_create.append(
                        LogEntry(
                            container_name=container,
                            level=entry.get("level", "INFO"),
                            message=entry.get("message", ""),
                            timestamp=timestamp,
                            raw_line=entry.get("raw_line", ""),
                            source=entry.get("source", "stdout"),
                        )
                    )
                except (json.JSONDecodeError, Exception) as e:
                    logger.warning(f"Failed to parse log entry for archive: {e}")

        if entries_to_create:
            LogEntry.objects.bulk_create(entries_to_create)

        return len(entries_to_create)
