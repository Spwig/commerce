"""
License synchronization service for external providers.

This service handles syncing license operations to external license management systems.
"""

import logging
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger(__name__)


class LicenseProviderService:
    """Service for syncing licenses with external providers"""

    def __init__(self, provider):
        """
        Initialize service with a provider.

        Args:
            provider: LicenseProvider model instance
        """
        self.provider = provider
        self.adapter = self._get_adapter()

    def _get_adapter(self):
        """
        Factory method to get the appropriate adapter for this provider type.

        Returns:
            Provider-specific adapter instance
        """
        # Import here to avoid circular imports
        from catalog.providers.registry import LicenseProviderRegistry

        # Get provider class from registry
        provider_class = LicenseProviderRegistry.get_provider(self.provider.provider_type)

        if not provider_class:
            logger.warning(f"No adapter found for provider type: {self.provider.provider_type}")
            return None

        # Instantiate the adapter with our provider
        try:
            return provider_class(self.provider)
        except Exception as e:
            logger.error(f"Failed to instantiate adapter for {self.provider.provider_type}: {e}")
            return None

    def create_license(self, license_key, product, order):
        """
        Create license in external system and track sync.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            ExternalLicenseSync instance
        """
        from catalog.models import ExternalLicenseSync

        # Create sync record
        sync = ExternalLicenseSync.objects.create(
            license_key=license_key,
            provider=self.provider,
            external_id="",  # Will be updated after successful sync
            sync_direction="outbound",
            sync_status="pending",
        )

        if not self.adapter:
            sync.sync_status = "failed"
            sync.error_message = (
                f"No adapter available for provider type: {self.provider.provider_type}"
            )
            sync.save()
            return sync

        try:
            # Call adapter to create license
            success, external_id, response_data = self.adapter.create_license(
                license_key, product, order
            )

            if success:
                sync.external_id = external_id
                sync.external_data = response_data
                sync.sync_status = "success"
                logger.info(
                    f"Successfully synced license {license_key.key} to {self.provider.name}"
                )
            else:
                sync.sync_status = "failed"
                sync.error_message = response_data.get("error", "Unknown error")
                logger.error(f"Failed to sync license {license_key.key}: {sync.error_message}")

        except Exception as e:
            sync.sync_status = "failed"
            sync.error_message = str(e)
            logger.exception(f"Exception syncing license {license_key.key}: {e}")

        sync.save()
        return sync

    def sync_activation(self, activation):
        """
        Sync device activation to external system.

        Args:
            activation: LicenseActivation model instance

        Returns:
            bool: Success status
        """
        if not self.adapter:
            logger.warning(f"No adapter for {self.provider.name}, skipping activation sync")
            return False

        try:
            success, activation_id, response_data = self.adapter.activate_device(
                activation.license_key, activation.device_identifier, activation.device_info
            )

            if success:
                logger.info(
                    f"Synced activation for {activation.license_key.key} to {self.provider.name}"
                )
                return True
            else:
                logger.error(f"Failed to sync activation: {response_data.get('error')}")
                return False

        except Exception as e:
            logger.exception(f"Exception syncing activation: {e}")
            return False

    def sync_deactivation(self, activation):
        """
        Sync device deactivation to external system.

        Args:
            activation: LicenseActivation model instance

        Returns:
            bool: Success status
        """
        if not self.adapter:
            logger.warning(f"No adapter for {self.provider.name}, skipping deactivation sync")
            return False

        try:
            success, response_data = self.adapter.deactivate_device(
                activation.license_key, activation.device_identifier
            )

            if success:
                logger.info(
                    f"Synced deactivation for {activation.license_key.key} to {self.provider.name}"
                )
                return True
            else:
                logger.error(f"Failed to sync deactivation: {response_data.get('error')}")
                return False

        except Exception as e:
            logger.exception(f"Exception syncing deactivation: {e}")
            return False

    def validate_license(self, key):
        """
        Validate license with external provider.

        Args:
            key: License key string

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        if not self.adapter:
            logger.warning(f"No adapter for {self.provider.name}, skipping validation")
            return False, {"error": "No adapter available"}

        try:
            return self.adapter.validate_license(key)
        except Exception as e:
            logger.exception(f"Exception validating license: {e}")
            return False, {"error": str(e)}

    def _schedule_next_retry(self, sync, now, error_message):
        """Increment the retry counter and schedule the next attempt.

        Uses exponential backoff (5min, 15min, 45min, ...) measured from the
        incremented retry count so the first retry waits 5 minutes.
        """
        sync.retry_count += 1
        sync.error_message = error_message
        delay = 5 * (3 ** (sync.retry_count - 1))
        sync.next_retry_at = now + timedelta(minutes=delay)

    def retry_failed_syncs(self, max_retries=3):
        """
        Retry failed synchronization operations.

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            int: Number of syncs successfully retried
        """
        from catalog.models import ExternalLicenseSync

        # Find failed syncs that are due for retry. Newly failed records have a
        # null next_retry_at and must also be picked up (NULL is excluded by a
        # plain <= comparison).
        now = timezone.now()
        failed_syncs = ExternalLicenseSync.objects.filter(
            Q(next_retry_at__isnull=True) | Q(next_retry_at__lte=now),
            provider=self.provider,
            sync_status="failed",
            retry_count__lt=max_retries,
        )

        retried_count = 0

        for sync in failed_syncs:
            try:
                # Attempt to recreate the license
                if self.adapter:
                    # Get required data from sync record. A license may carry an
                    # order_item without a digital_asset, so fall back to the
                    # order item's product when the asset is absent.
                    license_key = sync.license_key
                    order_item = license_key.order_item
                    if license_key.digital_asset:
                        product = license_key.digital_asset.product
                    elif order_item:
                        product = order_item.product
                    else:
                        product = None
                    order = order_item.order if order_item else None

                    if product and order:
                        success, external_id, response_data = self.adapter.create_license(
                            license_key, product, order
                        )

                        if success:
                            sync.external_id = external_id
                            sync.external_data = response_data
                            sync.sync_status = "success"
                            sync.next_retry_at = None
                            retried_count += 1
                        else:
                            self._schedule_next_retry(
                                sync, now, response_data.get("error", "Unknown error")
                            )

                        sync.save()
                    else:
                        logger.warning(
                            f"Cannot retry sync {sync.id}: license {license_key.key} is "
                            "missing product or order data"
                        )

            except Exception as e:
                logger.exception(f"Exception retrying sync {sync.id}: {e}")
                self._schedule_next_retry(sync, now, str(e))
                sync.save()

        return retried_count

    def handle_webhook(self, event_type, payload):
        """
        Handle webhook event from external provider.

        Args:
            event_type: Type of webhook event
            payload: Webhook payload data

        Returns:
            bool: Success status
        """
        if not self.adapter:
            logger.warning(f"No adapter for {self.provider.name}, cannot handle webhook")
            return False

        try:
            success, error_message = self.adapter.handle_webhook(event_type, payload)

            if success:
                logger.info(f"Successfully handled webhook: {event_type}")
            else:
                logger.error(f"Failed to handle webhook: {error_message}")

            return success

        except Exception as e:
            logger.exception(f"Exception handling webhook: {e}")
            return False
