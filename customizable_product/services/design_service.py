from decimal import Decimal


class DesignPricingService:
    """Calculates pricing for a product design based on its elements and the config rules."""

    @staticmethod
    def calculate(design_config, design_data):
        """
        Calculate price breakdown for a design.

        Args:
            design_config: ProductDesignConfig instance
            design_data: Design JSON data with surfaces and canvas objects

        Returns:
            dict with pricing breakdown
        """
        surfaces = design_data.get("surfaces", {})

        # Count elements across all surfaces
        surfaces_used = 0
        total_text_elements = 0
        total_image_uploads = 0
        total_clipart_elements = 0

        for _surface_slug, surface_data in surfaces.items():
            canvas_json = surface_data.get("canvas_json", {})
            objects = canvas_json.get("objects", [])

            if objects:
                surfaces_used += 1

            for obj in objects:
                obj_type = obj.get("type", "")
                if obj_type in ("i-text", "textbox", "text"):
                    total_text_elements += 1
                elif obj_type == "image":
                    # Distinguish uploads from clipart via custom property
                    if obj.get("custom_type") == "clipart":
                        total_clipart_elements += 1
                    else:
                        total_image_uploads += 1

        # Calculate fees
        base_fee = (
            Decimal(str(design_config.base_design_fee.amount))
            if design_config.base_design_fee
            else Decimal("0")
        )
        surface_fee_rate = (
            Decimal(str(design_config.per_surface_fee.amount))
            if design_config.per_surface_fee
            else Decimal("0")
        )
        upload_fee_rate = (
            Decimal(str(design_config.per_upload_fee.amount))
            if design_config.per_upload_fee
            else Decimal("0")
        )
        text_fee_rate = (
            Decimal(str(design_config.per_text_fee.amount))
            if design_config.per_text_fee
            else Decimal("0")
        )

        # Base design fee (applied when any elements exist)
        has_elements = surfaces_used > 0
        design_fee = base_fee if has_elements else Decimal("0")

        # Per-surface fee (first surface free, additional surfaces charged)
        extra_surfaces = max(0, surfaces_used - 1)
        surface_fees = surface_fee_rate * extra_surfaces

        # Per-upload fee
        upload_fees = upload_fee_rate * total_image_uploads

        # Per-text fee
        text_fees = text_fee_rate * total_text_elements

        total = design_fee + surface_fees + upload_fees + text_fees

        return {
            "base_design_fee": str(design_fee),
            "surface_fees": str(surface_fees),
            "upload_fees": str(upload_fees),
            "text_fees": str(text_fees),
            "total": str(total),
            "breakdown": {
                "surfaces_used": surfaces_used,
                "extra_surfaces": extra_surfaces,
                "text_elements": total_text_elements,
                "image_uploads": total_image_uploads,
                "clipart_elements": total_clipart_elements,
            },
        }
