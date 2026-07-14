"""
Django management command to poll tracking updates from shipping providers.

This command is a workaround for providers that don't support webhooks (like FedEx REST API).
It should be run periodically via cron/celery beat to keep tracking information up-to-date.

Usage:
    ./manage.py update_shipment_tracking [--provider fedex] [--limit 100] [--dry-run]

Examples:
    # Update all active shipments from all providers
    ./manage.py update_shipment_tracking

    # Update only FedEx shipments
    ./manage.py update_shipment_tracking --provider fedex

    # Dry run to see what would be updated
    ./manage.py update_shipment_tracking --dry-run

    # Limit to 50 shipments
    ./manage.py update_shipment_tracking --limit 50

Recommended cron schedule:
    # Every hour for in-transit/out-for-delivery shipments
    0 * * * * cd /path/to/shop && ./shop_venv/bin/python manage.py update_shipment_tracking
"""

import logging

from django.core.management.base import BaseCommand

from shipping.models import Shipment, TrackingEvent
from shipping.providers.registry import ProviderRegistry
from shipping.utils.encryption import decrypt_credentials

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Poll tracking updates from shipping providers (for providers without webhook support)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            help="Only update shipments from specific provider (e.g., fedex)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Maximum number of shipments to update (default: 100)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be updated without making changes",
        )

    def handle(self, *args, **options):
        provider_filter = options["provider"]
        limit = options["limit"]
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("[DRY RUN MODE - No changes will be saved]"))

        self.stdout.write(f"Polling tracking updates (limit={limit})...")

        # Get active shipments that need tracking updates
        # Only poll shipments in statuses that can change
        shipments_query = Shipment.objects.filter(
            provider_account__isnull=False,  # Only API shipments
            provider_account__is_active=True,
            tracking_id__isnull=False,
            status__in=["labeled", "in_transit", "out_for_delivery", "exception"],
        ).select_related("provider_account", "provider_account__component", "order")

        # Filter by provider if specified
        if provider_filter:
            shipments_query = shipments_query.filter(
                provider_account__component__slug=provider_filter
            )

        # Limit results
        shipments = shipments_query[:limit]

        if not shipments:
            self.stdout.write(self.style.WARNING("No shipments found to update"))
            return

        self.stdout.write(f"Found {len(shipments)} shipments to check")

        # Track statistics
        stats = {
            "checked": 0,
            "updated": 0,
            "errors": 0,
            "new_events": 0,
        }

        # Process each shipment
        for shipment in shipments:
            stats["checked"] += 1

            try:
                result = self._update_shipment_tracking(shipment, dry_run)
                if result["updated"]:
                    stats["updated"] += 1
                stats["new_events"] += result["new_events"]

            except Exception as e:
                stats["errors"] += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"[ERROR] Shipment {shipment.id} ({shipment.tracking_id}): {e}"
                    )
                )
                logger.error(
                    f"Failed to update tracking for shipment {shipment.id}: {e}", exc_info=True
                )

        # Print summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("SUMMARY"))
        self.stdout.write("=" * 80)
        self.stdout.write(f"Shipments checked:  {stats['checked']}")
        self.stdout.write(f"Shipments updated:  {stats['updated']}")
        self.stdout.write(f"New events created: {stats['new_events']}")
        self.stdout.write(f"Errors:             {stats['errors']}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY RUN - No changes were saved]"))

    def _update_shipment_tracking(self, shipment, dry_run=False):
        """
        Update tracking for a single shipment.

        Returns:
            dict: {
                'updated': bool,  # Whether status changed
                'new_events': int  # Number of new events created
            }
        """
        result = {"updated": False, "new_events": 0}

        # Get provider instance
        provider_class = ProviderRegistry.get_provider(shipment.provider_account.component.slug)
        if not provider_class:
            raise ValueError(f"Provider '{shipment.provider_account.component.slug}' not found")

        # Decrypt credentials
        credentials = decrypt_credentials(shipment.provider_account.credentials_encrypted)

        # Initialize provider
        provider = provider_class(
            credentials=credentials, config=shipment.provider_account.settings
        )

        # Get tracking info (will use cache if available)
        tracking_info = provider.get_tracking(shipment.tracking_id)

        # Check if status changed
        old_status = shipment.status
        new_status = tracking_info["status"]

        if old_status != new_status:
            self.stdout.write(f"[UPDATE] {shipment.tracking_id}: {old_status} -> {new_status}")
            if not dry_run:
                shipment.status = new_status
                shipment.save(update_fields=["status", "updated_at"])
            result["updated"] = True
        else:
            self.stdout.write(
                self.style.SUCCESS(f"[OK] {shipment.tracking_id}: {old_status} (no change)")
            )

        # Process tracking events
        # Get existing event timestamps to avoid duplicates
        existing_events = set(
            TrackingEvent.objects.filter(shipment=shipment).values_list("occurred_at", flat=True)
        )

        for event_data in tracking_info.get("events", []):
            event_time = event_data["timestamp"]
            if event_time and event_time not in existing_events:
                self.stdout.write(f"  [NEW EVENT] {event_time}: {event_data['description']}")
                if not dry_run:
                    TrackingEvent.objects.create(
                        shipment=shipment,
                        status=event_data["status"],
                        description=event_data["description"],
                        location=event_data["location"],
                        occurred_at=event_time,
                        raw={"event_data": event_data},
                    )
                result["new_events"] += 1

        # Update order tracking number if not set
        if not dry_run and shipment.order and not shipment.order.tracking_number:
            shipment.order.tracking_number = shipment.tracking_id
            shipment.order.save(update_fields=["tracking_number"])

        return result
