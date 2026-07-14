"""
Management command to start the built-in SMTP server.

Usage:
    ./manage.py start_smtp_server
    ./manage.py start_smtp_server --host 127.0.0.1 --port 2525
    ./manage.py start_smtp_server --postfix-host 127.0.0.1 --postfix-port 25
"""

import signal
import sys

from django.core.management.base import BaseCommand

from email_system.smtp_server.server import SMTPServerManager


class Command(BaseCommand):
    help = "Start the built-in SMTP server for email sending"

    def add_arguments(self, parser):
        parser.add_argument(
            "--host",
            type=str,
            default="127.0.0.1",
            help="SMTP server listen address (default: 127.0.0.1 - localhost only for security)",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=2525,
            help="SMTP server listen port (default: 2525 - non-privileged port)",
        )
        parser.add_argument(
            "--postfix-host",
            type=str,
            default="127.0.0.1",
            help="Postfix relay server address (default: 127.0.0.1)",
        )
        parser.add_argument(
            "--postfix-port", type=int, default=25, help="Postfix relay server port (default: 25)"
        )
        parser.add_argument(
            "--dev-mode",
            action="store_true",
            help="Development mode - log emails instead of sending via Postfix",
        )

    def handle(self, *args, **options):
        host = options["host"]
        port = options["port"]
        postfix_host = options["postfix_host"]
        postfix_port = options["postfix_port"]
        dev_mode = options.get("dev_mode", False)

        # Security warning if binding to non-localhost
        if host != "127.0.0.1" and host != "localhost":
            self.stdout.write(self.style.WARNING("\n⚠️  WARNING: Binding to non-localhost address!"))
            self.stdout.write(
                self.style.WARNING(
                    "This SMTP server has no authentication and should only be used on localhost."
                )
            )
            self.stdout.write(
                self.style.WARNING("Binding to a public interface is a SECURITY RISK.\n")
            )

        # Create server manager
        manager = SMTPServerManager(
            host=host,
            port=port,
            postfix_host=postfix_host,
            postfix_port=postfix_port,
            dev_mode=dev_mode,
        )

        # Setup signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            self.stdout.write(self.style.WARNING("\n\nShutting down SMTP server..."))
            manager.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Display startup info
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(self.style.SUCCESS("Spwig Built-in SMTP Server"))
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(f"\n  Listen Address: {host}:{port}")
        if dev_mode:
            self.stdout.write("  Mode: Development (emails logged, not sent)")
        else:
            self.stdout.write(f"  Relay to: {postfix_host}:{postfix_port}")
        self.stdout.write("  DKIM Signing: Enabled\n")
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write("\nStarting server... (Press CTRL+C to stop)\n")

        try:
            # Start the server (this blocks)
            manager.start()

            # Keep the process alive
            import time

            while manager.is_running():
                time.sleep(1)

                # Optionally print stats periodically
                # stats = manager.get_stats()
                # self.stdout.write(f"Stats: {stats}")

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n\nReceived interrupt signal"))
            manager.stop()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n\nError: {e}"))
            manager.stop()
            raise

        self.stdout.write(self.style.SUCCESS("\nSMTP server stopped"))
