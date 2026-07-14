"""
Management command to export webhook events documentation to JSON.

This command exports all webhook event definitions, including their
descriptions and categories, for use in the public API documentation site.
"""

import json

from django.core.management.base import BaseCommand, CommandError

from webhooks.events import (
    WEBHOOK_EVENTS,
    WebhookEventCategory,
    get_events_by_category,
)


class Command(BaseCommand):
    help = "Export webhook events documentation to JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            "-o",
            type=str,
            default="webhooks.json",
            help="Output file path (default: webhooks.json)",
        )
        parser.add_argument(
            "--indent", type=int, default=2, help="JSON indentation level (default: 2)"
        )
        parser.add_argument(
            "--stdout", action="store_true", help="Output to stdout instead of file"
        )

    def handle(self, *args, **options):
        output_path = options["output"]
        indent = options["indent"]
        to_stdout = options["stdout"]

        # Category display names and icons
        category_info = {
            WebhookEventCategory.ORDER: {
                "name": "Order",
                "icon": "fa-shopping-cart",
                "description": "Events related to order lifecycle",
            },
            WebhookEventCategory.PAYMENT: {
                "name": "Payment",
                "icon": "fa-credit-card",
                "description": "Events related to payment processing",
            },
            WebhookEventCategory.SHIPMENT: {
                "name": "Shipment",
                "icon": "fa-truck",
                "description": "Events related to shipping and delivery",
            },
            WebhookEventCategory.INVENTORY: {
                "name": "Inventory",
                "icon": "fa-warehouse",
                "description": "Events related to stock and inventory",
            },
            WebhookEventCategory.PRODUCT: {
                "name": "Product",
                "icon": "fa-box",
                "description": "Events related to product catalog",
            },
            WebhookEventCategory.CUSTOMER: {
                "name": "Customer",
                "icon": "fa-users",
                "description": "Events related to customer accounts",
            },
            WebhookEventCategory.SUBSCRIPTION: {
                "name": "Subscription",
                "icon": "fa-sync-alt",
                "description": "Events related to recurring subscriptions",
            },
            WebhookEventCategory.CART: {
                "name": "Cart",
                "icon": "fa-shopping-basket",
                "description": "Events related to shopping cart",
            },
            WebhookEventCategory.REFUND: {
                "name": "Refund",
                "icon": "fa-undo",
                "description": "Events related to refunds and returns",
            },
        }

        # Build export data
        events_by_category = get_events_by_category()

        export_data = {
            "events_by_category": events_by_category,
            "categories": {},
            "events": {},
            "total_events": len(WEBHOOK_EVENTS),
        }

        # Add category metadata
        for category_key, info in category_info.items():
            export_data["categories"][category_key] = {
                "name": info["name"],
                "icon": info["icon"],
                "description": info["description"],
                "event_count": len(events_by_category.get(category_key, [])),
            }

        # Add flat events list with full details
        for event_type, (description, category) in WEBHOOK_EVENTS.items():
            export_data["events"][event_type] = {
                "event": event_type,
                "description": str(description),
                "category": category,
            }

        # Output
        json_output = json.dumps(export_data, indent=indent, ensure_ascii=False)

        if to_stdout:
            self.stdout.write(json_output)
        else:
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(json_output)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully exported {len(WEBHOOK_EVENTS)} webhook events to {output_path}"
                    )
                )
            except OSError as e:
                raise CommandError(f"Failed to write output file: {e}")
