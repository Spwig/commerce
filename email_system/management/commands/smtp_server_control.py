"""
Management command to control the SMTP server via supervisor.

This command provides a simple interface for starting/stopping/restarting
the SMTP server when running in Docker with supervisor.

Usage:
    ./manage.py smtp_server_control start
    ./manage.py smtp_server_control stop
    ./manage.py smtp_server_control restart
    ./manage.py smtp_server_control status
"""

import subprocess

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Control the SMTP server (start, stop, restart, status)"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            type=str,
            choices=["start", "stop", "restart", "status"],
            help="Action to perform: start, stop, restart, or status",
        )

    def handle(self, *args, **options):
        action = options["action"]

        try:
            # Check if supervisorctl is available
            result = subprocess.run(["which", "supervisorctl"], capture_output=True, text=True)

            if result.returncode != 0:
                self.stdout.write(
                    self.style.WARNING(
                        "Supervisor not detected. This command only works in Docker.\n"
                        "To run SMTP server manually, use: ./manage.py start_smtp_server"
                    )
                )
                return

            # Execute supervisor command
            cmd = ["supervisorctl", action, "smtp-server"]

            self.stdout.write(f"Executing: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True)

            # Display output
            if result.stdout:
                self.stdout.write(result.stdout)

            if result.stderr:
                self.stdout.write(self.style.ERROR(result.stderr))

            # Status-specific output
            if action == "start":
                if result.returncode == 0:
                    self.stdout.write(self.style.SUCCESS("\n✓ SMTP server started successfully"))
                    self.stdout.write("  - Listening on: 127.0.0.1:2525")
                    self.stdout.write("  - Relaying to: Postfix (127.0.0.1:25)")
                    self.stdout.write("  - DKIM signing: Enabled")
                    self.stdout.write(
                        "\nView logs: docker exec <container> tail -f /app/logs/smtp-server-stdout.log"
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"\n✗ Failed to start SMTP server (exit code: {result.returncode})"
                        )
                    )

            elif action == "stop":
                if result.returncode == 0:
                    self.stdout.write(self.style.SUCCESS("\n✓ SMTP server stopped"))
                else:
                    self.stdout.write(
                        self.style.WARNING("\n⚠ SMTP server may not have been running")
                    )

            elif action == "restart":
                if result.returncode == 0:
                    self.stdout.write(self.style.SUCCESS("\n✓ SMTP server restarted"))

            elif action == "status":
                # Parse status output
                if "RUNNING" in result.stdout:
                    self.stdout.write(self.style.SUCCESS("\n✓ SMTP server is RUNNING"))
                elif "STOPPED" in result.stdout:
                    self.stdout.write(self.style.WARNING("\n⚠ SMTP server is STOPPED"))
                elif "FATAL" in result.stdout or "BACKOFF" in result.stdout:
                    self.stdout.write(self.style.ERROR("\n✗ SMTP server has ERRORS"))
                    self.stdout.write(
                        "\nCheck logs: docker exec <container> tail -n 50 /app/logs/smtp-server-stderr.log"
                    )
                else:
                    self.stdout.write(self.style.WARNING(f"\n? Status: {result.stdout.strip()}"))

        except FileNotFoundError:
            raise CommandError(
                "supervisorctl command not found. "
                "This command only works when running in Docker with supervisor."
            )

        except Exception as e:
            raise CommandError(f"Error controlling SMTP server: {e}")
