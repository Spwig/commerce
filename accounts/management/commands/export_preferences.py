"""
Management command to export communication preferences.

Usage:
    python manage.py export_preferences --user EMAIL
    python manage.py export_preferences --all --output-dir /tmp/exports
    python manage.py export_preferences --format csv
"""

import json
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from accounts.services.preference_export_service import PreferenceExportService

User = get_user_model()


class Command(BaseCommand):
    help = "Export communication preferences for GDPR compliance"

    def add_arguments(self, parser):
        parser.add_argument("--user", type=str, help="Email of user to export")
        parser.add_argument("--all", action="store_true", help="Export all users")
        parser.add_argument(
            "--output-dir",
            type=str,
            default="/tmp/preference_exports",
            help="Output directory for export files (default: /tmp/preference_exports)",
        )
        parser.add_argument(
            "--format",
            type=str,
            default="json",
            choices=["json", "csv"],
            help="Export format (default: json)",
        )

    def handle(self, *args, **options):
        user_email = options.get("user")
        export_all = options.get("all")
        output_dir = options.get("output_dir")
        export_format = options.get("format")

        # Validation
        if not user_email and not export_all:
            raise CommandError("Please specify --user EMAIL or --all")

        if user_email and export_all:
            raise CommandError("Cannot use both --user and --all")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        self.stdout.write(f"Exporting preferences to: {output_dir}")
        self.stdout.write(f"Format: {export_format}")

        # Export single user
        if user_email:
            try:
                user = User.objects.get(email=user_email)
                self._export_user(user, output_dir, export_format)
                self.stdout.write(self.style.SUCCESS(f"✓ Exported preferences for {user.email}"))
            except User.DoesNotExist:
                raise CommandError(f"User not found: {user_email}")
            except Exception as e:
                raise CommandError(f"Export failed: {e}")

        # Export all users
        elif export_all:
            users = User.objects.all()
            total = users.count()

            self.stdout.write(f"Exporting {total} users...")

            success_count = 0
            error_count = 0

            for i, user in enumerate(users, 1):
                try:
                    self._export_user(user, output_dir, export_format)
                    success_count += 1

                    # Progress indicator
                    if i % 100 == 0:
                        self.stdout.write(
                            f"  Progress: {i}/{total} ({success_count} successful, {error_count} errors)"
                        )

                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.WARNING(f"✗ Error exporting {user.email}: {e}"))

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Export complete: {success_count} successful, {error_count} errors"
                )
            )

    def _export_user(self, user, output_dir, export_format):
        """Export a single user's preferences to file."""
        # Get export data
        data = PreferenceExportService.export_user_preferences(user)

        # Generate filename
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user.username}_{timestamp}.{export_format}"
        filepath = os.path.join(output_dir, filename)

        # Write file
        if export_format == "json":
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
        elif export_format == "csv":
            # Flatten and write CSV
            import csv

            flattened = PreferenceExportService._flatten_for_csv(data)

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Field", "Value"])
                for key, value in flattened.items():
                    writer.writerow([key, value])

        return filepath
