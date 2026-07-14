"""
Management utilities for database, system monitoring, and file operations
"""

import os
import subprocess
import time
from datetime import datetime

import psutil
import tablib
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.db import connection
from django.utils import timezone


class DatabaseManager:
    """Database management utilities"""

    @staticmethod
    def get_database_info():
        """Get database connection info and statistics"""
        with connection.cursor() as cursor:
            # Get database size
            cursor.execute("""
                SELECT pg_size_pretty(pg_database_size(current_database())) as size,
                       current_database() as name
            """)
            db_info = cursor.fetchone()

            # Get table statistics
            cursor.execute("""
                SELECT
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    null_frac
                FROM pg_stats
                WHERE schemaname = 'public'
                ORDER BY tablename, attname;
            """)
            table_stats = cursor.fetchall()

            # Get active connections
            cursor.execute("""
                SELECT count(*) FROM pg_stat_activity
                WHERE state = 'active'
            """)
            active_connections = cursor.fetchone()[0]

            return {
                "database_name": db_info[1],
                "database_size": db_info[0],
                "active_connections": active_connections,
                "table_stats": table_stats,
            }

    @staticmethod
    def get_table_list():
        """Get list of all tables with row counts"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    table_name,
                    (xpath('/row/c/text()',
                        query_to_xml('SELECT count(*) AS c FROM ' || quote_ident(table_name),
                        false, true, '')))[1]::text::int AS row_count
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            return cursor.fetchall()

    @staticmethod
    def execute_query(query, fetch_results=True, read_only=False):
        """Execute a SQL query safely"""
        if read_only:
            import re

            stripped = re.sub(
                r"^(/\*.*?\*/|--[^\n]*\n|\s)+", "", query.strip(), flags=re.DOTALL
            ).upper()
            if not stripped.startswith(("SELECT", "EXPLAIN", "SHOW", "WITH")):
                return {
                    "success": False,
                    "error": "Only SELECT, EXPLAIN, SHOW, and WITH queries are allowed.",
                    "execution_time": 0,
                }
        start_time = time.time()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                execution_time = time.time() - start_time

                if fetch_results and cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return {
                        "success": True,
                        "columns": columns,
                        "rows": rows,
                        "execution_time": execution_time,
                        "row_count": len(rows),
                    }
                else:
                    return {
                        "success": True,
                        "execution_time": execution_time,
                        "rows_affected": cursor.rowcount,
                    }
        except Exception as e:
            return {"success": False, "error": str(e), "execution_time": time.time() - start_time}

    @staticmethod
    def _find_db_container():
        """Find the database Docker container name for docker exec fallback.

        Uses the CONTAINER_PREFIX env var convention (matching DockerLogService):
        container name = {CONTAINER_PREFIX}_db (e.g., spwig_db, spwig_my-store_db).
        Falls back to scanning running containers if the convention doesn't match.
        """
        import shutil

        if not shutil.which("docker"):
            return None

        def _has_pg_dump(container_name):
            """Check if pg_dump exists in the given container."""
            try:
                check = subprocess.run(
                    ["docker", "exec", container_name, "which", "pg_dump"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                return check.returncode == 0
            except Exception:
                return False

        # Strategy 1: Use CONTAINER_PREFIX convention (e.g., spwig_db)
        prefix = os.environ.get("CONTAINER_PREFIX", "spwig")
        expected_name = f"{prefix}_db"
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name=^/{expected_name}$", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.stdout.strip() and _has_pg_dump(expected_name):
                return expected_name
        except Exception:
            pass

        # Strategy 2: Fallback — scan running containers for any with 'db' and pg_dump
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            for name in result.stdout.strip().split("\n"):
                if name and "db" in name.lower() and "redis" not in name.lower():
                    if _has_pg_dump(name):
                        return name
        except Exception:
            pass

        return None

    @staticmethod
    def create_backup(backup_name, backup_type="full", compression="gzip"):
        """Create database backup using pg_dump"""
        import shutil

        try:
            db_settings = settings.DATABASES["default"]
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{backup_name}_{timestamp}.sql"

            if compression == "gzip":
                filename += ".gz"

            backup_path = os.path.join(settings.MEDIA_ROOT, "backups", filename)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

            # Determine how to run pg_dump
            use_docker = False
            docker_container = None

            if not shutil.which("pg_dump"):
                # pg_dump not available locally, try docker exec into db container
                docker_container = DatabaseManager._find_db_container()
                if not docker_container:
                    return {
                        "success": False,
                        "error": "pg_dump is not installed and no database container found. "
                        "Install postgresql-client or ensure the database container is running.",
                    }
                use_docker = True

            # Build pg_dump arguments
            pg_dump_args = []
            if use_docker:
                # When running inside the db container, connect locally
                pg_dump_args = ["-U", db_settings["USER"], "-d", db_settings["NAME"]]
            else:
                pg_dump_args = [
                    "-h",
                    db_settings["HOST"],
                    "-p",
                    str(db_settings["PORT"]),
                    "-U",
                    db_settings["USER"],
                    "-d",
                    db_settings["NAME"],
                ]

            if backup_type == "schema":
                pg_dump_args.append("--schema-only")
            elif backup_type == "data":
                pg_dump_args.append("--data-only")

            # Build the full command
            if use_docker:
                cmd = [
                    "docker",
                    "exec",
                    "-e",
                    f"PGPASSWORD={db_settings['PASSWORD']}",
                    docker_container,
                    "pg_dump",
                ] + pg_dump_args
                cmd_env = os.environ.copy()
            else:
                cmd = ["pg_dump"] + pg_dump_args
                cmd_env = os.environ.copy()
                cmd_env["PGPASSWORD"] = db_settings["PASSWORD"]

            # Execute backup
            if compression == "gzip":
                with open(backup_path, "wb") as f:
                    p1 = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=cmd_env
                    )
                    p2 = subprocess.Popen(["gzip"], stdin=p1.stdout, stdout=f)
                    p1.stdout.close()
                    p2.communicate()
                    p1.wait()
                    if p1.returncode != 0:
                        stderr = p1.stderr.read().decode() if p1.stderr else ""
                        # Clean up empty/partial file
                        if os.path.exists(backup_path):
                            os.remove(backup_path)
                        return {
                            "success": False,
                            "error": f"pg_dump failed: {stderr.strip() or 'unknown error'}",
                        }
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, env=cmd_env)
                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"pg_dump failed: {result.stderr.strip() or 'unknown error'}",
                    }
                with open(backup_path, "w") as f:
                    f.write(result.stdout)

            file_size = os.path.getsize(backup_path)

            return {
                "success": True,
                "file_path": backup_path,
                "file_size": file_size,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


class SystemMonitor:
    """System monitoring utilities"""

    @staticmethod
    def get_system_metrics():
        """Get current system metrics"""
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        load_avg = os.getloadavg() if hasattr(os, "getloadavg") else [0, 0, 0]

        # Memory metrics
        memory = psutil.virtual_memory()

        # Disk metrics
        disk = psutil.disk_usage("/")

        # Network metrics
        network = psutil.net_io_counters()

        # Django-specific metrics
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now()).count()

        # Cache metrics (if using Redis)
        cache_stats = {"hits": 0, "misses": 0}
        try:
            cache_stats = cache.get_stats() or cache_stats
        except Exception:
            pass

        return {
            "timestamp": timezone.now(),
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "load_average": list(load_avg),
            "memory_total": memory.total,
            "memory_available": memory.available,
            "memory_percent": memory.percent,
            "memory_used": memory.used,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_free": disk.free,
            "disk_percent": (disk.used / disk.total) * 100,
            "network_bytes_sent": network.bytes_sent,
            "network_bytes_recv": network.bytes_recv,
            "network_packets_sent": network.packets_sent,
            "network_packets_recv": network.packets_recv,
            "active_sessions": active_sessions,
            "cache_hits": cache_stats.get("hits", 0),
            "cache_misses": cache_stats.get("misses", 0),
        }

    @staticmethod
    def get_process_info():
        """Get Django process information"""
        current_process = psutil.Process()
        return {
            "pid": current_process.pid,
            "cpu_percent": current_process.cpu_percent(),
            "memory_info": current_process.memory_info()._asdict(),
            "create_time": timezone.make_aware(
                datetime.fromtimestamp(current_process.create_time())
            ),
            "num_threads": current_process.num_threads(),
            "connections": len(current_process.connections()),
        }


class FileManager:
    """File management utilities"""

    @staticmethod
    def get_directory_listing(path, show_hidden=False):
        """Get directory listing with file details"""
        try:
            items = []
            for item in os.listdir(path):
                if not show_hidden and item.startswith("."):
                    continue

                item_path = os.path.join(path, item)
                stat = os.stat(item_path)

                # Format file size for display
                size_display = ""
                if not os.path.isdir(item_path):
                    size = stat.st_size
                    if size < 1024:
                        size_display = f"{size} B"
                    elif size < 1048576:
                        size_display = f"{size / 1024:.1f} KB"
                    elif size < 1073741824:
                        size_display = f"{size / 1048576:.1f} MB"
                    else:
                        size_display = f"{size / 1073741824:.1f} GB"

                items.append(
                    {
                        "name": item,
                        "path": item_path,
                        "is_dir": os.path.isdir(item_path),
                        "size": stat.st_size,
                        "size_display": size_display,
                        "modified": timezone.make_aware(datetime.fromtimestamp(stat.st_mtime)),
                        "permissions": oct(stat.st_mode)[-3:],
                    }
                )

            return sorted(items, key=lambda x: (not x["is_dir"], x["name"].lower()))
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_file_info(file_path):
        """Get detailed file information"""
        try:
            stat = os.stat(file_path)
            return {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": stat.st_size,
                "modified": timezone.make_aware(datetime.fromtimestamp(stat.st_mtime)),
                "created": timezone.make_aware(datetime.fromtimestamp(stat.st_ctime)),
                "permissions": oct(stat.st_mode)[-3:],
                "is_readable": os.access(file_path, os.R_OK),
                "is_writable": os.access(file_path, os.W_OK),
                "is_executable": os.access(file_path, os.X_OK),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def safe_path(base_path, requested_path):
        """Ensure requested path is within base path (security)"""
        base = os.path.abspath(base_path)
        requested = os.path.abspath(os.path.join(base, requested_path))
        if requested == base or requested.startswith(base + os.sep):
            return requested
        return None


class DataExporter:
    """Data export utilities"""

    @staticmethod
    def export_table_data(table_name, format="csv"):
        """Export table data in various formats"""
        try:
            # Validate table exists in public schema (prevent SQL injection)
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM information_schema.tables "
                    "WHERE table_schema = 'public' AND table_name = %s",
                    [table_name],
                )
                if not cursor.fetchone():
                    return "Error: Invalid table name"

            safe_name = connection.ops.quote_name(table_name)
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {safe_name} LIMIT 1000")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

            # Create tablib dataset
            data = tablib.Dataset()
            data.headers = columns
            for row in rows:
                data.append(row)

            # Export in requested format
            format_attr_map = {
                "csv": "csv",
                "json": "json",
                "xlsx": "xlsx",
                "yaml": "yaml",
            }
            return getattr(data, format_attr_map.get(format, "csv"))

        except Exception as e:
            return f"Error: {str(e)}"
