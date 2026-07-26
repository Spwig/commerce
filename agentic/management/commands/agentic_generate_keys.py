"""Generate the merchant's agentic signing keys if they don't already exist."""

from django.core.management.base import BaseCommand

from agentic.identity.keys import ensure_keys


class Command(BaseCommand):
    help = "Ensure the store has an active Ed25519 transport key and ECDSA AP2 key."

    def handle(self, *args, **options):
        created = ensure_keys()
        for purpose, made in created.items():
            if made:
                self.stdout.write(self.style.SUCCESS(f"Generated {purpose} key."))
            else:
                self.stdout.write(f"{purpose} key already present — left as is.")
