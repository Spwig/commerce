"""
Account Creation Service
Handles account creation at different checkout timing points with transaction safety
"""

import logging
import uuid
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _

User = get_user_model()
logger = logging.getLogger(__name__)


class AccountCreationService:
    """Service for creating user accounts during checkout flow"""

    @staticmethod
    def _normalize_email(email: str) -> str:
        """Normalize email for consistent lookup: lowercase + strip whitespace"""
        return email.lower().strip() if email else ""

    @staticmethod
    def create_guest_user(email: str, first_name: str = "", last_name: str = "") -> User:
        """
        Get or create a guest user account by normalized email.

        If a guest user with the same email already exists, reuses that user
        (updating name fields if provided). This ensures all guest orders for
        the same email accumulate on one User record.

        Args:
            email: Customer email
            first_name: Customer first name (optional)
            last_name: Customer last name (optional)

        Returns:
            User instance with unusable password
        """
        normalized_email = AccountCreationService._normalize_email(email)

        # Look for existing guest user with this email
        existing_guest = (
            User.objects.filter(email__iexact=normalized_email, username__startswith="guest_")
            .order_by("-date_joined")
            .first()
        )

        if existing_guest:
            # Update name if provided and currently empty
            updated = False
            if first_name and not existing_guest.first_name:
                existing_guest.first_name = first_name
                updated = True
            if last_name and not existing_guest.last_name:
                existing_guest.last_name = last_name
                updated = True
            if updated:
                existing_guest.save(update_fields=["first_name", "last_name"])

            logger.info(
                f"Reused existing guest user: {existing_guest.username} ({normalized_email})"
            )
            return existing_guest

        # No existing guest — create new one
        username = f"guest_{uuid.uuid4().hex[:12]}"

        user = User.objects.create_user(
            username=username,
            email=normalized_email,
            first_name=first_name,
            last_name=last_name,
        )

        # Set unusable password (guest accounts can't login)
        user.set_unusable_password()
        user.save()

        logger.info(f"Created guest user: {user.username} ({normalized_email})")
        return user

    @staticmethod
    @transaction.atomic
    def convert_guest_to_full_account(
        user: User, password: str, send_confirmation_email: bool = True
    ) -> tuple[bool, str]:
        """
        Convert guest user to full account with password

        Args:
            user: Guest User instance
            password: New password
            send_confirmation_email: Send email verification

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not user.username.startswith("guest_"):
            return False, _("User is not a guest account")

        try:
            # Merge any other guest users with the same email first
            # This ensures all historical orders end up on this account
            if user.email:
                other_guests = list(
                    User.objects.filter(
                        email__iexact=user.email, username__startswith="guest_"
                    ).exclude(pk=user.pk)
                )
                if other_guests:
                    merge_stats = AccountCreationService.merge_guest_users(user, other_guests)
                    logger.info(f"Pre-conversion merge for {user.email}: {merge_stats}")

            # Use full email as username to avoid collisions
            user.username = user.email.lower()
            user.set_password(password)
            user.save()

            # Send email verification if enabled
            if send_confirmation_email:
                try:
                    from allauth.account.models import EmailAddress
                    from allauth.account.utils import send_email_confirmation

                    # Create/update email address record
                    email_address, created = EmailAddress.objects.get_or_create(
                        user=user, email=user.email, defaults={"primary": True, "verified": False}
                    )

                    if not email_address.verified:
                        from django.http import HttpRequest

                        # Create a minimal request object for send_email_confirmation
                        request = HttpRequest()
                        send_email_confirmation(request, user, email=user.email)
                except Exception as e:
                    logger.warning(f"Failed to send confirmation email: {e}")
                    # Don't fail the whole operation if email fails

            logger.info(f"Converted guest user to full account: {user.username}")
            return True, _("Account created successfully!")

        except Exception as e:
            logger.error(f"Failed to convert guest to full account: {e}")
            return False, _("Failed to create account. Please try again.")

    @staticmethod
    @transaction.atomic
    def create_account_during_checkout(
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        send_confirmation: bool = True,
    ) -> tuple[bool, str, User | None]:
        """
        Create full account during checkout (timing: during_checkout or before_checkout)

        Args:
            email: Customer email
            password: Account password
            first_name: Customer first name
            last_name: Customer last name
            send_confirmation: Send verification email

        Returns:
            Tuple of (success: bool, message: str, user: User or None)
        """
        # Check if a registered (non-guest) account already exists with this email
        normalized_email = AccountCreationService._normalize_email(email)
        if (
            User.objects.filter(email__iexact=normalized_email)
            .exclude(username__startswith="guest_")
            .exists()
        ):
            return False, _("An account with this email already exists"), None

        try:
            # Check if a guest user exists — convert them instead of creating new
            existing_guest = (
                User.objects.filter(email__iexact=normalized_email, username__startswith="guest_")
                .order_by("-date_joined")
                .first()
            )

            if existing_guest:
                # Merge any duplicates and convert the guest
                if first_name:
                    existing_guest.first_name = first_name
                if last_name:
                    existing_guest.last_name = last_name
                existing_guest.save(update_fields=["first_name", "last_name"])

                success, message = AccountCreationService.convert_guest_to_full_account(
                    user=existing_guest,
                    password=password,
                    send_confirmation_email=send_confirmation,
                )
                if success:
                    return True, message, existing_guest
                return False, message, None

            # No guest exists — create fresh account
            # Generate username from email
            base_username = email.split("@")[0] if email else "user"
            username = base_username
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Create user
            user = User.objects.create_user(
                username=username,
                email=normalized_email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            # Setup email verification
            if send_confirmation:
                try:
                    from allauth.account.models import EmailAddress
                    from allauth.account.utils import send_email_confirmation
                    from django.http import HttpRequest

                    EmailAddress.objects.create(
                        user=user, email=email, primary=True, verified=False
                    )

                    # Create minimal request for email sending
                    request = HttpRequest()
                    send_email_confirmation(request, user, email=email)
                except Exception as e:
                    logger.warning(f"Failed to send confirmation email: {e}")
                    # Don't fail account creation if email fails

            logger.info(f"Created account during checkout: {username}")
            return True, _("Account created successfully!"), user

        except Exception as e:
            logger.error(f"Failed to create account during checkout: {e}")
            return False, _("Failed to create account. Please try again."), None

    @staticmethod
    @transaction.atomic
    def merge_guest_users(canonical_user: "User", duplicate_users: list) -> dict[str, Any]:
        """
        Merge duplicate guest users into a single canonical user.

        Reassigns all orders, addresses, and related records from duplicate
        users to the canonical user, then deletes the duplicates.

        Args:
            canonical_user: The guest User to keep (all records merge into this)
            duplicate_users: List of duplicate guest Users to merge and delete

        Returns:
            Dict with merge statistics: orders_moved, addresses_moved, users_deleted
        """
        from orders.models import Address, Order

        stats = {"orders_moved": 0, "addresses_moved": 0, "users_deleted": 0}

        for dup_user in duplicate_users:
            if dup_user.pk == canonical_user.pk:
                continue

            # Reassign orders
            orders_moved = Order.objects.filter(user=dup_user).update(user=canonical_user)
            stats["orders_moved"] += orders_moved

            # Reassign addresses
            addresses_moved = Address.objects.filter(user=dup_user).update(user=canonical_user)
            stats["addresses_moved"] += addresses_moved

            # Delete OneToOne related records (they can't be reassigned if canonical already has them)
            try:
                if hasattr(dup_user, "profile"):
                    dup_user.profile.delete()
            except Exception:
                pass

            try:
                if hasattr(dup_user, "communication_preferences"):
                    dup_user.communication_preferences.delete()
            except Exception:
                pass

            # Delete the duplicate user
            logger.info(
                f"Merging guest user {dup_user.username} (pk={dup_user.pk}) "
                f"into {canonical_user.username} (pk={canonical_user.pk}): "
                f"{orders_moved} orders, {addresses_moved} addresses"
            )
            dup_user.delete()
            stats["users_deleted"] += 1

        return stats

    @staticmethod
    def merge_all_guests_for_email(email: str) -> tuple[Optional["User"], dict[str, Any]]:
        """
        Find all guest users for an email and merge them into one canonical user.

        Picks the most recently created guest as canonical (most likely to
        have current name/address info).

        Args:
            email: Email address to consolidate

        Returns:
            Tuple of (canonical_user or None, merge_stats)
        """
        normalized_email = AccountCreationService._normalize_email(email)
        guest_users = list(
            User.objects.filter(
                email__iexact=normalized_email, username__startswith="guest_"
            ).order_by("-date_joined")
        )

        if len(guest_users) <= 1:
            return (guest_users[0] if guest_users else None), {
                "orders_moved": 0,
                "addresses_moved": 0,
                "users_deleted": 0,
            }

        canonical = guest_users[0]  # Most recent
        duplicates = guest_users[1:]

        stats = AccountCreationService.merge_guest_users(canonical, duplicates)
        logger.info(
            f"Merged {len(duplicates)} duplicate guest(s) for {normalized_email} "
            f"into {canonical.username}"
        )
        return canonical, stats

    @staticmethod
    def get_account_creation_context(user: User | None = None) -> dict[str, Any]:
        """
        Get context data for account creation UI

        Args:
            user: Optional user for pre-filling data

        Returns:
            Dictionary with context data including social auth providers
        """
        from core.utils import get_site_settings

        settings = get_site_settings()

        # Get enabled social auth providers
        social_providers = []
        if settings.show_social_auth_on_account_creation:
            try:
                from allauth.socialaccount import providers

                provider_list = providers.registry.get_list()
                social_providers = [
                    {"provider": p.id, "display_name": p.name} for p in provider_list
                ]
            except Exception as e:
                logger.warning(f"Failed to get social providers: {e}")

        return {
            "account_creation_message": settings.effective_account_creation_message,
            "show_social_auth": settings.show_social_auth_on_account_creation,
            "social_providers": social_providers,
            "prefill_email": user.email if user else "",
            "prefill_first_name": user.first_name if user else "",
            "prefill_last_name": user.last_name if user else "",
        }
