"""Celery tasks for the customizable product app."""

import logging

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(name="customizable_product.render_design_snapshot")
def render_design_snapshot(snapshot_id):
    """
    Render high-resolution fulfillment images for a design snapshot.

    This task runs asynchronously after an order is placed,
    generating print-ready composite images for each surface.
    """
    from .models import DesignSnapshot, ProductDesignConfig
    from .services.render_service import DesignRenderService

    try:
        snapshot = DesignSnapshot.objects.select_related("order_item__product").get(pk=snapshot_id)
    except DesignSnapshot.DoesNotExist:
        logger.error(f"DesignSnapshot {snapshot_id} not found")
        return

    if snapshot.is_rendered:
        logger.info(f"DesignSnapshot {snapshot_id} already rendered, skipping")
        return

    product = snapshot.order_item.product

    try:
        design_config = product.design_config
    except ProductDesignConfig.DoesNotExist:
        logger.error(f"No design config for product {product.id}")
        return

    design_data = snapshot.design_data
    surfaces_data = design_data.get("surfaces", {})
    fulfillment_files = {}

    for surface_slug, surface_data in surfaces_data.items():
        canvas_json = surface_data.get("canvas_json", {})
        if not canvas_json.get("objects"):
            continue

        try:
            surface = design_config.surfaces.get(slug=surface_slug)
        except Exception:
            logger.warning(f"Surface {surface_slug} not found for product {product.id}")
            continue

        # Render the composite image
        composite = DesignRenderService.render_surface(
            surface,
            canvas_json,
            output_dpi=surface.recommended_dpi,
        )

        if composite:
            import io

            from django.core.files.base import ContentFile

            from media_library.models import MediaAsset

            # Save as PNG
            buffer = io.BytesIO()
            composite.save(buffer, format="PNG", quality=95)
            buffer.seek(0)

            filename = f"fulfillment_{product.slug}_{surface_slug}_{snapshot.id}.png"
            asset = MediaAsset(
                title=f"Fulfillment: {product.name} - {surface.name}",
                alt_text=f"Print-ready design for {product.name} {surface.name}",
            )
            asset.original_file.save(filename, ContentFile(buffer.read()), save=True)

            fulfillment_files[surface_slug] = asset.id
            logger.info(f"Rendered surface {surface_slug} for snapshot {snapshot_id}")

    snapshot.fulfillment_files = fulfillment_files
    snapshot.is_rendered = True
    snapshot.render_completed_at = timezone.now()
    snapshot.save()

    logger.info(
        f"DesignSnapshot {snapshot_id} fully rendered with {len(fulfillment_files)} surfaces"
    )


@shared_task(name="customizable_product.cleanup_expired_drafts")
def cleanup_expired_drafts():
    """Remove expired DesignDraft records to prevent database bloat."""
    from .models import DesignDraft

    expired_count, _ = DesignDraft.objects.filter(expires_at__lt=timezone.now()).delete()

    if expired_count:
        logger.info(f"Cleaned up {expired_count} expired design drafts")
