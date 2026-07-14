"""
Management command for generating translation files per component/app.
"""

import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generate translation files for specific components/apps"

    def add_arguments(self, parser):
        parser.add_argument("--app", type=str, help="Specific app to generate translations for")
        parser.add_argument(
            "--locale",
            action="append",
            dest="locales",
            help="Specific locale(s) to generate (can be used multiple times)",
        )
        parser.add_argument("--all", action="store_true", help="Generate translations for all apps")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without actually doing it",
        )

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)

        # Get list of local apps
        local_apps = [
            "core",
            "design",
            "page_builder",
            "accounts",
            "catalog",
            "cart",
            "orders",
            "shipping",
            "payment_providers",
            "management",
            "media_library",
            "setup_wizard",
            "customers",
            "vouchers",
            "address_autocomplete",
            "affiliate",
            "announcements",
            "blog",
            "component_updates",
            "configurator_3d",
            "custom_fields",
            "developer_portal",
            "element_builder",
            "email_system",
            "exchange_rates",
            "form_builder",
            "geoip",
            "loyalty",
            "marketplace",
            "marketplace_checkout",
            "migration",
            "payout_providers",
            "pos_app",
            "product_feeds",
            "referrals",
            "search",
            "seo_generator",
            "sms_system",
            "social_sharing",
            "staff_roles",
            "subscriptions",
            "translations",
            "webhooks",
        ]

        # Get supported languages from settings
        supported_locales = [lang_code for lang_code, _ in settings.LANGUAGES]
        target_locales = options.get("locales") or supported_locales

        if options["app"]:
            if options["app"] not in local_apps:
                raise CommandError(f"App '{options['app']}' not found in local apps")
            apps_to_process = [options["app"]]
        elif options["all"]:
            apps_to_process = local_apps
        else:
            self.stdout.write(self.style.ERROR("Please specify either --app <app_name> or --all"))
            return

        for app_name in apps_to_process:
            self.process_app(app_name, target_locales, base_dir, options["dry_run"])

    def process_app(self, app_name, locales, base_dir, dry_run=False):
        """Process translation generation for a specific app"""
        app_path = base_dir / app_name

        if not app_path.exists():
            self.stdout.write(
                self.style.WARNING(f"App directory {app_path} does not exist, skipping...")
            )
            return

        # Create locale directory structure if it doesn't exist
        locale_dir = app_path / "locale"

        if dry_run:
            self.stdout.write(f"[DRY RUN] Would process app: {app_name}")
            if not locale_dir.exists():
                self.stdout.write(f"[DRY RUN] Would create locale directory: {locale_dir}")
            return

        if not locale_dir.exists():
            locale_dir.mkdir(parents=True, exist_ok=True)
            self.stdout.write(f"Created locale directory: {locale_dir}")

        # Create language directories and generate .po files
        for locale in locales:
            locale_path = locale_dir / locale / "LC_MESSAGES"
            locale_path.mkdir(parents=True, exist_ok=True)

            # Run makemessages for this specific app
            manage_py_path = base_dir / "manage.py"
            python_path = base_dir / "shop_venv" / "bin" / "python"

            cmd = [
                str(python_path),
                str(manage_py_path),
                "makemessages",
                "--locale",
                locale,
                "--ignore",
                "shop_venv/*",
                "--ignore",
                "static/*",
                "--ignore",
                "media/*",
                "--no-location",
                "--keep-pot",
            ]

            try:
                # Change to app directory to limit scope
                subprocess.run(cmd, cwd=app_path, capture_output=True, text=True, check=True)

                po_file = locale_path / "django.po"
                if po_file.exists():
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Generated {locale} translations for {app_name}: {po_file}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No translations found for {app_name} in {locale}")
                    )

            except subprocess.CalledProcessError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error generating translations for {app_name} ({locale}): {e.stderr}"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Unexpected error processing {app_name} ({locale}): {str(e)}")
                )

    def get_app_translatable_strings_count(self, app_path):
        """Count translatable strings in an app"""
        try:
            # Simple grep to count translatable strings
            result = subprocess.run(
                ["grep", "-r", "--include=*.py", "--include=*.html", "_(", str(app_path)],
                capture_output=True,
                text=True,
            )
            return len(result.stdout.splitlines()) if result.stdout else 0
        except Exception:
            return 0
