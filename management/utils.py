"""
Management utilities for database, system monitoring, and file operations
"""

import contextlib
import os
import re
import subprocess
import time
from datetime import datetime

import psutil
import tablib
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.db import connection, transaction
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
    def _strip_sql_strings(sql):
        """Remove quoted string/identifier literals, SQL comments, and
        dollar-quoted literals so the guard cannot be fooled by keywords or
        semicolons hiding inside them (e.g. `SELECT 1 -- update statistics`
        or `SELECT $$DELETE; DROP$$`)."""
        result = []
        i = 0
        n = len(sql)
        while i < n:
            ch = sql[i]
            # Line comment: -- ... up to end of line
            if ch == "-" and i + 1 < n and sql[i + 1] == "-":
                i += 2
                while i < n and sql[i] != "\n":
                    i += 1
                continue
            # Block comment: /* ... */ (PostgreSQL allows nesting)
            if ch == "/" and i + 1 < n and sql[i + 1] == "*":
                depth = 1
                i += 2
                while i < n and depth:
                    if sql[i] == "/" and i + 1 < n and sql[i + 1] == "*":
                        depth += 1
                        i += 2
                    elif sql[i] == "*" and i + 1 < n and sql[i + 1] == "/":
                        depth -= 1
                        i += 2
                    else:
                        i += 1
                continue
            # Dollar-quoted literal: $$...$$ or $tag$...$tag$
            if ch == "$":
                tag_end = None
                if i + 1 < n and sql[i + 1] == "$":
                    tag_end = i + 1
                elif i + 1 < n and (sql[i + 1].isalpha() or sql[i + 1] == "_"):
                    j = i + 2
                    while j < n and (sql[j].isalnum() or sql[j] == "_"):
                        j += 1
                    if j < n and sql[j] == "$":
                        tag_end = j
                if tag_end is not None:
                    tag = sql[i : tag_end + 1]
                    end = sql.find(tag, tag_end + 1)
                    i = n if end == -1 else end + len(tag)
                    continue
            # Single-quoted string / double-quoted identifier
            if ch in ("'", '"'):
                quote = ch
                i += 1
                while i < n:
                    if sql[i] == quote:
                        # A doubled quote is an escaped quote, not a terminator.
                        if i + 1 < n and sql[i + 1] == quote:
                            i += 2
                            continue
                        i += 1
                        break
                    i += 1
                continue
            result.append(ch)
            i += 1
        return "".join(result)

    @staticmethod
    def execute_query(query, fetch_results=True, read_only=False):
        """Execute a SQL query safely"""
        if read_only:
            stripped = re.sub(
                r"^(/\*.*?\*/|--[^\n]*\n|\s)+", "", query.strip(), flags=re.DOTALL
            ).upper()
            if not stripped.startswith(("SELECT", "EXPLAIN", "SHOW", "WITH")):
                return {
                    "success": False,
                    "error": "Only SELECT, EXPLAIN, SHOW, and WITH queries are allowed.",
                    "execution_time": 0,
                }
            # The prefix check alone is not enough: a stacked statement
            # (`SELECT 1; DROP TABLE users`) starts with an allowed keyword yet
            # still mutates the database. Reject stacked statements outright,
            # inspecting the query with string/identifier literals removed so a
            # semicolon hiding inside a literal cannot fool the split.
            unquoted = DatabaseManager._strip_sql_strings(stripped)
            if len([s for s in unquoted.split(";") if s.strip()]) > 1:
                return {
                    "success": False,
                    "error": "Multiple SQL statements are not allowed in read-only mode.",
                    "execution_time": 0,
                }
        start_time = time.time()
        try:
            # Authoritative enforcement: run inside a PostgreSQL READ ONLY
            # transaction so the database itself rejects every data-modifying
            # statement — including ones a text scan cannot detect, such as
            # `SELECT nextval('seq')`, `SELECT ... INTO new_table`, or a
            # side-effecting function call. The block is always rolled back,
            # which costs nothing (read-only) and undoes the SET LOCAL should
            # this run nested inside a surrounding request transaction.
            read_only_tx = transaction.atomic() if read_only else contextlib.nullcontext()
            with read_only_tx:
                with connection.cursor() as cursor:
                    if read_only:
                        cursor.execute("SET LOCAL transaction_read_only = on")
                    cursor.execute(query)
                    execution_time = time.time() - start_time

                    if fetch_results and cursor.description:
                        columns = [desc[0] for desc in cursor.description]
                        rows = cursor.fetchall()
                        result = {
                            "success": True,
                            "columns": columns,
                            "rows": rows,
                            "execution_time": execution_time,
                            "row_count": len(rows),
                        }
                    else:
                        result = {
                            "success": True,
                            "execution_time": execution_time,
                            "rows_affected": cursor.rowcount,
                        }
                if read_only:
                    transaction.set_rollback(True)
                return result
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

            # The backup name becomes a filesystem path component, so restrict it
            # to a safe character set. This rejects path separators, `..`, and
            # absolute paths, preventing the backup from escaping the backups dir.
            if not re.fullmatch(r"[A-Za-z0-9._-]+", backup_name or ""):
                return {
                    "success": False,
                    "error": "Invalid backup name. Use only letters, numbers, "
                    "dots, hyphens, and underscores.",
                }

            filename = f"{backup_name}_{timestamp}.sql"

            if compression == "gzip":
                filename += ".gz"

            backups_dir = os.path.join(settings.MEDIA_ROOT, "backups")
            os.makedirs(backups_dir, exist_ok=True)

            # Defence in depth: confirm the resolved destination stays inside the
            # backups directory even after symlink resolution.
            backup_path = FileManager.safe_path(backups_dir, filename)
            if backup_path is None:
                return {
                    "success": False,
                    "error": "Invalid backup name.",
                }

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
                    # pg_dump can succeed while gzip fails (e.g. disk full),
                    # leaving a truncated .gz. Treat a nonzero gzip exit as
                    # failure and discard the partial output.
                    if p2.returncode != 0:
                        if os.path.exists(backup_path):
                            os.remove(backup_path)
                        return {
                            "success": False,
                            "error": "gzip compression failed while writing the backup.",
                        }
            else:
                # Stream pg_dump straight to disk instead of buffering the whole
                # dump in memory, which can exhaust worker memory on large DBs.
                with open(backup_path, "w") as f:
                    result = subprocess.run(
                        cmd, stdout=f, stderr=subprocess.PIPE, text=True, env=cmd_env
                    )
                if result.returncode != 0:
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                    return {
                        "success": False,
                        "error": f"pg_dump failed: {result.stderr.strip() or 'unknown error'}",
                    }

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
        # Resolve symlinks (not just `..` components) so a symlink under the
        # base pointing outside it cannot slip a path past the containment check.
        base = os.path.realpath(base_path)
        requested = os.path.realpath(os.path.join(base, requested_path))
        try:
            if os.path.commonpath([base, requested]) == base:
                return requested
        except ValueError:
            # Different drives / mixed path kinds — treat as outside base.
            pass
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
