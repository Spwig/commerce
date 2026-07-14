"""
Ensure a licence file exists at LICENSE_PATH.

Runs at app startup and is safe to invoke manually. If a licence file already
exists (Community or paid), it is left untouched. If no licence file exists,
the pre-signed Community template is copied into place.

The bootstrap is idempotent and does not touch the database.
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

COMMUNITY_LICENCE_TEMPLATE = (
    Path(__file__).resolve().parent.parent.parent / "data" / "community_licence.json"
)


class Command(BaseCommand):
    help = "Install the Community licence at LICENSE_PATH if no licence exists."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite any existing licence file. Use with caution.",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Suppress info output. Errors still print.",
        )

    def handle(self, *args, **options):
        target = Path(settings.LICENSE_PATH)
        force = options["force"]
        quiet = options["quiet"]

        if target.exists() and not force:
            if not quiet:
                self.stdout.write(f"Licence already exists at {target}; leaving untouched.")
            return

        if not COMMUNITY_LICENCE_TEMPLATE.exists():
            self.stderr.write(
                f"Community licence template not found at {COMMUNITY_LICENCE_TEMPLATE}. "
                "Run tools/oss/sign_community_licence.py to generate it."
            )
            return

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(COMMUNITY_LICENCE_TEMPLATE, target)

        if not quiet:
            self.stdout.write(f"Community licence installed at {target}.")
