"""
Label Service - Purchase shipping labels from providers.

Orchestrates the complete label purchase workflow:
1. Retrieve provider instance from ProviderAccount
2. Build provider-specific options from Shipment data
3. Call provider buy_label() API
4. Update Shipment with tracking number and label URL
5. Create TrackingEvent audit record
6. Update Order.tracking_number if this is the first shipment
"""

import logging
from typing import Any

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from shipping.models import Shipment, TrackingEvent
from shipping.providers.registry import ProviderRegistry
from shipping.utils.encryption import decrypt_credentials

logger = logging.getLogger(__name__)


class LabelService:
    """Service for purchasing shipping labels from providers."""

    @staticmethod
    def buy_label(
        shipment: Shipment,
        rate: dict[str, Any],
        label_format: str = "PDF",
        label_size: str = "4x6",
    ) -> dict[str, Any]:
        """
        Purchase shipping label for a shipment.

        Args:
            shipment: Shipment instance to purchase label for
            rate: Rate dictionary from get_rates() (contains service_code, carrier, rate)
            label_format: Label format (PDF, PNG, ZPLII, EPL2)
            label_size: Label size (4x6, 4x8, letter)

        Returns:
            Dictionary with label information:
            {
                'tracking_number': '1Z999AA10123456784',
                'label_url': 'https://...' or 'data:application/pdf;base64,...',
                'label_format': 'PDF',
                'cost': Decimal('12.50'),
                'currency': 'USD',
                'carrier': 'FedEx',
                'service': 'FedEx Ground'
            }

        Raises:
            ValueError: If shipment has no provider_account or invalid parameters
            ConnectionError: If provider API call fails
        """
        # Validate shipment has provider account
        if not shipment.provider_account:
            raise ValueError(_("Shipment must have a provider_account to purchase label"))

        if not shipment.provider_account.is_active:
            raise ValueError(_("Provider account is not active"))

        # Get provider instance
        provider_class = ProviderRegistry.get_provider(shipment.provider_account.component.slug)
        if not provider_class:
            raise ValueError(
                _("Provider '%(provider)s' not found or not registered")
                % {"provider": shipment.provider_account.component.slug}
            )

        # Decrypt credentials
        credentials = decrypt_credentials(shipment.provider_account.credentials_encrypted)

        # Initialize provider
        provider = provider_class(
            credentials=credentials, config=shipment.provider_account.settings
        )

        # Build options from shipment data
        options = LabelService._build_label_options(shipment, label_format, label_size)

        # Call provider API
        logger.info(f"Purchasing label for shipment {shipment.id} via {provider.provider_name}")

        try:
            label_info = provider.buy_label(
                shipment_id=str(shipment.id), rate=rate, options=options
            )

            # Update shipment with atomic transaction
            with transaction.atomic():
                LabelService._update_shipment(shipment, label_info)
                LabelService._create_tracking_event(shipment, label_info)
                LabelService._sync_order_tracking(shipment)

            logger.info(
                f"Label purchased successfully for shipment {shipment.id}. "
                f"Tracking: {label_info['tracking_number']}"
            )

            return label_info

        except Exception as e:
            logger.error(f"Failed to purchase label for shipment {shipment.id}: {e}", exc_info=True)
            raise

    @staticmethod
    def _build_label_options(
        shipment: Shipment, label_format: str, label_size: str
    ) -> dict[str, Any]:
        """
        Build provider-specific options from shipment data.

        Args:
            shipment: Shipment instance
            label_format: Label format
            label_size: Label size

        Returns:
            Dictionary of options for provider buy_label()
        """
        # Get order data
        order = shipment.order

        # Build origin address
        # TODO: Get warehouse/origin address from store settings
        # For now, use placeholder - will be enhanced in future phase
        origin = {
            "country": shipment.origin_country,
            "postal_code": "10001",  # TODO: Get from store settings
            "state": "NY",
            "city": "New York",
            "address1": "123 Main St",  # TODO: Get from store settings
        }

        # Build destination address from order
        destination = {
            "country": shipment.dest_country,
            "postal_code": order.shipping_address.get("postal_code", ""),
            "state": order.shipping_address.get("state", ""),
            "city": order.shipping_address.get("city", ""),
            "address1": order.shipping_address.get("address1", ""),
            "address2": order.shipping_address.get("address2", ""),
        }

        # Build parcels from shipment.packages
        parcels = shipment.packages if shipment.packages else []

        # Build shipper information
        # TODO: Get from store settings
        shipper_name = "Your Store Name"  # TODO: Get from site settings
        shipper_phone = "+12125551234"  # TODO: Get from site settings

        # Build recipient information from order
        recipient_name = (
            order.customer_name
            or f"{order.shipping_address.get('first_name', '')} {order.shipping_address.get('last_name', '')}".strip()
        )
        recipient_phone = order.shipping_address.get("phone", "")
        recipient_email = order.customer_email

        options = {
            "origin": origin,
            "destination": destination,
            "parcels": parcels,
            "shipper_name": shipper_name,
            "shipper_phone": shipper_phone,
            "shipper_email": "shipping@example.com",  # TODO: Get from settings
            "recipient_name": recipient_name,
            "recipient_phone": recipient_phone,
            "recipient_email": recipient_email,
            "label_format": label_format,
            "label_size": label_size,
        }

        return options

    @staticmethod
    def _update_shipment(shipment: Shipment, label_info: dict[str, Any]) -> None:
        """
        Update shipment with label information.

        Args:
            shipment: Shipment instance to update
            label_info: Label information from provider
        """
        shipment.tracking_id = label_info["tracking_number"]
        shipment.label_url = label_info["label_url"]
        shipment.status = "labeled"

        # Update carrier cost if provided
        if "cost" in label_info and "currency" in label_info:
            shipment.carrier_cost = label_info["cost"]
            shipment.carrier_cost_currency = label_info["currency"]

        # Store provider reference if provided
        if "external_shipment_id" in label_info:
            shipment.provider_reference = label_info["external_shipment_id"]

        # Add to audit log
        shipment.audit_log.append(
            {
                "timestamp": timezone.now().isoformat(),
                "action": "label_purchased",
                "tracking_number": label_info["tracking_number"],
                "carrier": label_info.get("carrier", ""),
                "service": label_info.get("service", ""),
                "cost": str(label_info.get("cost", "")),
            }
        )

        shipment.save()

    @staticmethod
    def _create_tracking_event(shipment: Shipment, label_info: dict[str, Any]) -> None:
        """
        Create initial tracking event for label purchase.

        Args:
            shipment: Shipment instance
            label_info: Label information from provider
        """
        TrackingEvent.objects.create(
            shipment=shipment,
            status="info_received",
            description=_("Shipping label created"),
            location="",
            occurred_at=timezone.now(),
            raw={"label_info": label_info},
        )

    @staticmethod
    def _sync_order_tracking(shipment: Shipment) -> None:
        """
        Update Order.tracking_number with first shipment's tracking ID.

        Args:
            shipment: Shipment instance
        """
        order = shipment.order

        # Only update if order doesn't have a tracking number yet
        if not order.tracking_number and shipment.tracking_id:
            order.tracking_number = shipment.tracking_id
            order.save(update_fields=["tracking_number"])

            logger.info(
                f"Updated order {order.order_number} with tracking number: {shipment.tracking_id}"
            )
