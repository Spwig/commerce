"""
Address Service - Business logic for address operations
"""

from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from ..models import Address


class AddressService:
    """Service class for address operations"""

    @staticmethod
    def get_user_addresses(
        user, address_type: str | None = None, active_only: bool = True
    ) -> QuerySet:
        """
        Get addresses for user

        Args:
            user: User instance
            address_type: Filter by address type (optional)
            active_only: Only return active addresses (default: True)

        Returns:
            QuerySet of Address objects
        """
        queryset = Address.objects.filter(user=user)

        if active_only:
            queryset = queryset.filter(is_active=True)

        if address_type:
            queryset = queryset.filter(address_type=address_type)

        return queryset.order_by("-is_default", "-created_at")

    @staticmethod
    @transaction.atomic
    def create_address(
        user,
        address_type: str,
        name: str,
        address1: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
        company: str = "",
        address2: str = "",
        phone: str = "",
        is_default: bool = False,
    ) -> tuple[bool, str, Address | None]:
        """
        Create new address for user

        Args:
            user: User instance
            address_type: Type of address (shipping, billing, both)
            name: Recipient name
            address1: Address line 1
            city: City
            state: State/province
            postal_code: Postal/ZIP code
            country: Country
            company: Company name (optional)
            address2: Address line 2 (optional)
            phone: Phone number (optional)
            is_default: Set as default address (optional)

        Returns:
            Tuple of (success: bool, message: str, address: Address)
        """
        # Validate address type
        valid_types = [t[0] for t in Address.ADDRESS_TYPES]
        if address_type not in valid_types:
            return False, _("Invalid address type"), None

        # Create address
        address = Address.objects.create(
            user=user,
            address_type=address_type,
            name=name,
            company=company,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            phone=phone,
            is_default=is_default,
        )

        # The Address.save() method handles ensuring only one default per type

        return True, _("Address created successfully"), address

    @staticmethod
    @transaction.atomic
    def update_address(address: Address, user, **kwargs) -> tuple[bool, str, Address | None]:
        """
        Update existing address with versioning for audit trail.
        If address has been used in orders, creates a new version instead of editing.

        Args:
            address: Address instance to update
            user: User instance (for permission check)
            **kwargs: Fields to update

        Returns:
            Tuple of (success: bool, message: str, address: Address)
        """
        from django.db.models import Q
        from django.utils import timezone

        # Check permission
        if address.user != user:
            return False, _("You don't have permission to update this address"), None

        # Check if address has been used in any orders
        from ..models import Order

        used_in_orders = Order.objects.filter(
            Q(shipping_address_ref=address) | Q(billing_address_ref=address)
        ).exists()

        # Update allowed fields
        allowed_fields = [
            "address_type",
            "name",
            "company",
            "address1",
            "address2",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
            "is_default",
        ]

        # Filter to only allowed fields that are provided
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_data:
            return False, _("No valid fields to update"), None

        if used_in_orders:
            # Address has been used - create new version for audit trail
            root_address = address.original_address or address

            # Lock the whole version family so concurrent updates can't each
            # spawn a competing active version.
            family = list(
                Address.objects.select_for_update().filter(
                    Q(pk=root_address.pk) | Q(original_address=root_address)
                )
            )

            # Always update the latest active version of the family, never a
            # stale/superseded record the client may have supplied. Editing an
            # already-superseded id must resolve to (and supersede) the current
            # active version, not fork a second active branch.
            active_versions = [a for a in family if a.is_active]
            current = max(active_versions, key=lambda a: a.version) if active_versions else None
            if current is None:
                return False, _("This address has no active version to update"), None

            # Get the highest version number from all versions (including root)
            new_version_number = max(a.version for a in family) + 1

            # Create new version with updated data, copied from the current
            # active version rather than the (possibly superseded) input.
            new_address = Address.objects.create(
                user=user,
                original_address=root_address,
                version=new_version_number,
                # Copy all current fields
                address_type=current.address_type,
                name=current.name,
                company=current.company,
                address1=current.address1,
                address2=current.address2,
                city=current.city,
                state=current.state,
                postal_code=current.postal_code,
                country=current.country,
                phone=current.phone,
                is_default=current.is_default,
                is_active=True,
            )

            # Apply updates to new version
            for field, value in update_data.items():
                setattr(new_address, field, value)
            new_address.save()

            # Mark the current active version as inactive
            current.is_active = False
            current.edited_at = timezone.now()
            current.is_default = False  # New version is now the default if it was set
            current.save(update_fields=["is_active", "edited_at", "is_default"])

            return True, _("Address updated (new version created for audit trail)"), new_address

        else:
            # Address not used in orders yet - safe to edit directly
            updated_fields = []
            for field, value in update_data.items():
                setattr(address, field, value)
                updated_fields.append(field)

            address.save(update_fields=updated_fields + ["updated_at"])
            return True, _("Address updated successfully"), address

    @staticmethod
    @transaction.atomic
    def delete_address(address: Address, user) -> tuple[bool, str]:
        """
        Delete address

        Args:
            address: Address instance to delete
            user: User instance (for permission check)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check permission
        if address.user != user:
            return False, _("You don't have permission to delete this address")

        # Check if address is used in any orders
        from ..models import Order

        Order.objects.filter(
            user=user,
            shipping_name=address.name,
            shipping_address1=address.address1,
            shipping_postal_code=address.postal_code,
        ).exists()

        # We can still delete it, just inform the user
        # (Orders store address data, not references)

        address.delete()
        return True, _("Address deleted successfully")

    @staticmethod
    @transaction.atomic
    def set_default_address(
        address: Address, user, address_type: str | None = None
    ) -> tuple[bool, str]:
        """
        Set address as default for its type

        Args:
            address: Address instance to set as default
            user: User instance (for permission check)
            address_type: Optional override for address type

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check permission
        if address.user != user:
            return False, _("You don't have permission to update this address")

        # Only active addresses can be set as default (an inactive/superseded
        # version must never become the default)
        if not address.is_active:
            return False, _("Cannot set an inactive address as default")

        # Use provided address_type or the address's current type
        target_type = address_type if address_type else address.address_type

        # Validate address type
        valid_types = [t[0] for t in Address.ADDRESS_TYPES]
        if target_type not in valid_types:
            return False, _("Invalid address type")

        # Update address type if changed
        if address_type and address.address_type != address_type:
            address.address_type = address_type

        # Set as default
        address.is_default = True
        address.save()

        # The Address.save() method handles ensuring only one default per type

        return True, _("Default address updated")

    @staticmethod
    def get_default_address(user, address_type: str = "both") -> Address | None:
        """
        Get default address for user

        Args:
            user: User instance
            address_type: Address type to get default for

        Returns:
            Address instance or None
        """
        try:
            return Address.objects.get(
                user=user, address_type=address_type, is_default=True, is_active=True
            )
        except Address.DoesNotExist:
            # Fall back to a default address of a compatible type only
            return Address.objects.filter(
                user=user,
                is_default=True,
                is_active=True,
                address_type__in=[address_type, "both"],
            ).first()

    @staticmethod
    def validate_address(address_data: dict[str, Any]) -> tuple[bool, list]:
        """
        Validate address data

        Args:
            address_data: Dict with address fields

        Returns:
            Tuple of (is_valid: bool, errors: list)
        """
        errors = []

        # Required fields
        required_fields = ["name", "address1", "city", "state", "postal_code", "country"]
        for field in required_fields:
            if not address_data.get(field):
                errors.append(
                    _("{field} is required").format(field=field.replace("_", " ").title())
                )

        # Validate address type
        if address_data.get("address_type"):
            valid_types = [t[0] for t in Address.ADDRESS_TYPES]
            if address_data["address_type"] not in valid_types:
                errors.append(_("Invalid address type"))

        # Validate postal code format (basic validation)
        postal_code = address_data.get("postal_code", "")
        if postal_code and len(postal_code) > 20:
            errors.append(_("Postal code is too long"))

        # Validate phone format (basic validation)
        phone = address_data.get("phone", "")
        if phone and len(phone) > 20:
            errors.append(_("Phone number is too long"))

        return len(errors) == 0, errors

    @staticmethod
    def format_address(address: Address, include_name: bool = True) -> str:
        """
        Format address as a single string

        Args:
            address: Address instance
            include_name: Include recipient name (default: True)

        Returns:
            Formatted address string
        """
        parts = []

        if include_name:
            parts.append(address.name)
            if address.company:
                parts.append(address.company)

        parts.append(address.address1)
        if address.address2:
            parts.append(address.address2)

        parts.append(f"{address.city}, {address.state} {address.postal_code}")
        parts.append(address.country)

        if address.phone:
            parts.append(f"Phone: {address.phone}")

        return "\n".join(parts)

    @staticmethod
    def get_address_with_usage(user) -> QuerySet:
        """
        Get user addresses with usage counts annotated.
        Only returns active addresses.

        Args:
            user: User instance

        Returns:
            QuerySet of Address objects with 'order_count' annotation
        """
        from django.db.models import Count, IntegerField, OuterRef, Q, Subquery, Value
        from django.db.models.functions import Coalesce

        from ..models import Order

        # Count unique Order rows referencing this address as either shipping or
        # billing, so an order that reuses the same address for both is counted
        # once (matching Address.get_order_count()).
        order_count_subquery = (
            Order.objects.filter(
                Q(shipping_address_ref=OuterRef("pk")) | Q(billing_address_ref=OuterRef("pk"))
            )
            .order_by()
            .values(group=Value(1))
            .annotate(count=Count("pk"))
            .values("count")
        )

        return (
            Address.objects.filter(user=user, is_active=True)
            .annotate(
                order_count=Coalesce(
                    Subquery(order_count_subquery, output_field=IntegerField()),
                    0,
                )
            )
            .order_by("-is_default", "-created_at")
        )
