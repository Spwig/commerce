"""
Affiliate Data Importer.

Imports affiliate data from WordPress (via Spwig Migration Bridge plugin)
into the Spwig affiliate system. Handles programs, affiliates, commissions,
and payouts with dependency ordering and date preservation.
"""

import logging
from decimal import Decimal, InvalidOperation

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from tqdm import tqdm

from accounts.models import CustomerProfile
from affiliate.models import Affiliate, AffiliateProgramMembership, Commission, Payout, Program
from core.utils import get_default_currency
from migration.fetchers.spwig_bridge_api import SpwigBridgeAPIClient
from migration.utils.transformers import parse_woocommerce_datetime
from orders.models import Order

User = get_user_model()
logger = logging.getLogger(__name__)


class AffiliateImporter:
    """
    Import affiliate data from WordPress via Spwig Migration Bridge.

    Import order (dependency-driven):
    1. Plans → Program
    2. Affiliates → User + Affiliate + AffiliateProgramMembership
    3. Commissions → Commission (requires Order via external_id)
    4. Payouts → Payout (M2M to Commission)
    """

    def __init__(
        self,
        bridge_client: SpwigBridgeAPIClient,
        migration_job=None,
        merchant_user=None,
    ):
        self.client = bridge_client
        self.job = migration_job
        self.merchant_user = merchant_user or self._get_merchant_user()

        # ID mappings (source_id → Spwig object)
        self.plan_map = {}  # source plan ID → Program
        self.affiliate_map = {}  # source affiliate ID → Affiliate
        self.commission_map = {}  # source referral ID → Commission

        # Stats
        self.stats = {
            "programs": {"created": 0, "skipped": 0, "errors": 0},
            "affiliates": {"created": 0, "skipped": 0, "errors": 0},
            "commissions": {
                "created": 0,
                "skipped": 0,
                "errors": 0,
                "orders_linked": 0,
                "orders_unlinked": 0,
            },
            "payouts": {"created": 0, "skipped": 0, "errors": 0},
        }

        # Track IDs for rollback
        self.imported_ids = {
            "program_ids": [],
            "affiliate_ids": [],
            "commission_ids": [],
            "payout_ids": [],
        }

    def _get_merchant_user(self):
        """Get the first superuser as the merchant/program owner."""
        return User.objects.filter(is_superuser=True).first()

    def import_all(self, progress_bar=True, step=None):
        """
        Run the full affiliate import pipeline.

        Args:
            progress_bar: Whether to show TQDM progress bars
            step: Optional MigrationStep for progress tracking

        Returns:
            dict: Import statistics
        """
        logger.info("Starting affiliate data import...")

        # Step 1: Import plans → Programs
        self._import_plans(progress_bar=progress_bar)

        # Step 2: Import affiliates → Users + Affiliates
        self._import_affiliates(progress_bar=progress_bar)

        # Step 3: Import commissions (requires orders to exist)
        self._import_commissions(progress_bar=progress_bar)

        # Step 4: Import payouts
        self._import_payouts(progress_bar=progress_bar)

        # Store rollback IDs in job config
        if self.job:
            config = self.job.connection_config or {}
            config["affiliate_rollback_ids"] = self.imported_ids
            self.job.connection_config = config
            self.job.save(update_fields=["connection_config"])

        logger.info(
            f"Affiliate import complete: "
            f"{self.stats['programs']['created']} programs, "
            f"{self.stats['affiliates']['created']} affiliates, "
            f"{self.stats['commissions']['created']} commissions, "
            f"{self.stats['payouts']['created']} payouts"
        )

        return self.stats

    # --- Step 1: Plans → Programs ---

    def _import_plans(self, progress_bar=True):
        """Import commission plans as Programs."""
        plans = self.client.fetch_all_plans()

        if not plans:
            logger.info("No plans to import, creating default program")
            self._create_default_program()
            return

        iterator = tqdm(plans, desc="📋 Affiliate Plans", unit="plan", disable=not progress_bar)

        for source_plan in iterator:
            try:
                self._import_single_plan(source_plan)
            except Exception as e:
                self.stats["programs"]["errors"] += 1
                logger.error(f"Failed to import plan {source_plan.get('source_id')}: {e}")

    def _import_single_plan(self, source):
        """Import a single plan as a Program."""
        source_id = str(source.get("source_id", ""))
        name = source.get("name", "Imported Program")

        # Map commission type
        commission_type = source.get("commission_type", "percentage")
        if commission_type not in ("percentage", "fixed"):
            commission_type = "percentage"

        try:
            commission_value = Decimal(str(source.get("commission_value", 10)))
        except (InvalidOperation, ValueError):
            commission_value = Decimal("10")

        # Generate unique slug
        base_slug = slugify(name) or "imported-program"
        slug = base_slug
        counter = 1
        while Program.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Parse date
        created_at = self._parse_date(source.get("created_at"))

        program = Program.objects.create(
            name=name,
            slug=slug,
            merchant=self.merchant_user,
            description=f"Imported from WordPress ({source.get('source_plugin', 'unknown')})",
            commission_type=commission_type,
            commission_value=commission_value,
            status="active",
            created_at=created_at or timezone.now(),
        )

        self.plan_map[source_id] = program
        self.imported_ids["program_ids"].append(program.id)
        self.stats["programs"]["created"] += 1

    def _create_default_program(self):
        """Create a default program when no plans exist in source."""
        slug = "imported-default"
        counter = 1
        while Program.objects.filter(slug=slug).exists():
            slug = f"imported-default-{counter}"
            counter += 1

        program = Program.objects.create(
            name="Imported Default Program",
            slug=slug,
            merchant=self.merchant_user,
            description="Default program for imported affiliates",
            commission_type="percentage",
            commission_value=Decimal("10"),
            status="active",
        )

        self.plan_map["default"] = program
        self.imported_ids["program_ids"].append(program.id)
        self.stats["programs"]["created"] += 1

    # --- Step 2: Affiliates → Users + Affiliates ---

    def _import_affiliates(self, progress_bar=True):
        """Import affiliate profiles."""
        affiliates = self.client.fetch_all_affiliates()

        if not affiliates:
            logger.info("No affiliates to import")
            return

        iterator = tqdm(affiliates, desc="👥 Affiliates", unit="aff", disable=not progress_bar)

        for source_affiliate in iterator:
            try:
                self._import_single_affiliate(source_affiliate)
            except Exception as e:
                self.stats["affiliates"]["errors"] += 1
                logger.error(f"Failed to import affiliate {source_affiliate.get('source_id')}: {e}")

    def _import_single_affiliate(self, source):
        """Import a single affiliate profile."""
        source_id = str(source.get("source_id", ""))
        str(source.get("wp_user_id", ""))
        email = source.get("email", "").strip().lower()

        if not email:
            logger.warning(f"Skipping affiliate {source_id}: no email")
            self.stats["affiliates"]["skipped"] += 1
            return

        # Step 1: Find or create User
        user = self._find_or_create_user(source)
        if not user:
            self.stats["affiliates"]["skipped"] += 1
            return

        # Step 2: Check if user already has an affiliate profile
        if hasattr(user, "affiliate_profile"):
            logger.info(f"User {user.email} already has affiliate profile, skipping")
            self.affiliate_map[source_id] = user.affiliate_profile
            self.stats["affiliates"]["skipped"] += 1
            return

        # Step 3: Create Affiliate
        payment_email = source.get("payment_email") or email
        status_map = {
            "active": "active",
            "pending": "pending",
            "inactive": "suspended",
            "rejected": "rejected",
        }
        status = status_map.get(source.get("status", "active"), "active")

        created_at = self._parse_date(source.get("registered_date"))

        affiliate = Affiliate.objects.create(
            user=user,
            payment_email=payment_email,
            status=status,
            website=source.get("website", "") or "",
            created_at=created_at or timezone.now(),
        )

        self.affiliate_map[source_id] = affiliate
        self.imported_ids["affiliate_ids"].append(affiliate.id)
        self.stats["affiliates"]["created"] += 1

        # Step 4: Create program membership for first available program
        program = self._get_default_program(source)
        if program:
            AffiliateProgramMembership.objects.create(
                affiliate=affiliate,
                program=program,
                status="approved",
                applied_at=created_at or timezone.now(),
                approved_at=created_at or timezone.now(),
            )

    def _find_or_create_user(self, source):
        """Find existing user by email/external_id or create new one."""
        email = source.get("email", "").strip().lower()
        wp_user_id = str(source.get("wp_user_id", ""))

        # Try matching by email first
        try:
            user = User.objects.get(email__iexact=email)
            return user
        except User.DoesNotExist:
            pass

        # Try matching via CustomerProfile external_id (WP user ID)
        if wp_user_id:
            try:
                profile = CustomerProfile.objects.get(external_id=wp_user_id)
                return profile.user
            except CustomerProfile.DoesNotExist:
                pass

        # Create new user
        first_name = source.get("first_name", "")
        last_name = source.get("last_name", "")

        # Generate unique username from email
        base_username = email.split("@")[0][:30]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        date_joined = self._parse_date(source.get("registered_date"))

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_joined=date_joined or timezone.now(),
            is_active=True,
        )

        return user

    def _get_default_program(self, source):
        """Get the best matching program for an affiliate."""
        # Try to match by source plan_id if available
        plan_id = str(source.get("plan_id", ""))
        if plan_id and plan_id in self.plan_map:
            return self.plan_map[plan_id]

        # Return first available program
        if self.plan_map:
            return next(iter(self.plan_map.values()))

        return None

    # --- Step 3: Commissions ---

    def _import_commissions(self, progress_bar=True):
        """Import referrals as Commissions."""
        referrals = self.client.fetch_all_referrals()

        if not referrals:
            logger.info("No commissions to import")
            return

        iterator = tqdm(referrals, desc="💰 Commissions", unit="comm", disable=not progress_bar)

        for source_referral in iterator:
            try:
                self._import_single_commission(source_referral)
            except Exception as e:
                self.stats["commissions"]["errors"] += 1
                logger.error(f"Failed to import commission {source_referral.get('source_id')}: {e}")

    def _import_single_commission(self, source):
        """Import a single referral as a Commission."""
        source_id = str(source.get("source_id", ""))
        affiliate_source_id = str(source.get("affiliate_id", ""))
        order_id = str(source.get("order_id", ""))

        # Look up affiliate
        affiliate = self.affiliate_map.get(affiliate_source_id)
        if not affiliate:
            logger.warning(
                f"Commission {source_id}: affiliate {affiliate_source_id} not found, skipping"
            )
            self.stats["commissions"]["skipped"] += 1
            return

        # Look up order by external_id (required FK)
        order = None
        if order_id:
            try:
                order = Order.objects.get(external_id=order_id)
                self.stats["commissions"]["orders_linked"] += 1
            except Order.DoesNotExist:
                pass

        if not order:
            logger.warning(
                f"Commission {source_id}: order {order_id} not migrated, "
                f"skipping (Commission.order is required)"
            )
            self.stats["commissions"]["orders_unlinked"] += 1
            self.stats["commissions"]["skipped"] += 1
            return

        # Parse amount
        try:
            amount = Decimal(str(source.get("amount", 0)))
        except (InvalidOperation, ValueError):
            amount = Decimal("0")

        if amount < 0:
            logger.warning(f"Commission {source_id}: negative amount {amount}, skipping")
            self.stats["commissions"]["skipped"] += 1
            return

        # Map status
        status_map = {
            "pending": "pending",
            "approved": "approved",
            "paid": "paid",
            "rejected": "rejected",
        }
        status = status_map.get(source.get("status", "pending"), "pending")

        # Get program
        program = self._get_program_for_commission(source)
        if not program:
            logger.warning(f"Commission {source_id}: no program available, skipping")
            self.stats["commissions"]["skipped"] += 1
            return

        # Parse dates
        created_at = self._parse_date(source.get("created_at"))
        approved_at = None
        paid_at = None
        if status in ("approved", "paid"):
            approved_at = created_at
        if status == "paid":
            paid_at = self._parse_date(source.get("paid_at")) or created_at

        commission = Commission.objects.create(
            affiliate=affiliate,
            program=program,
            order=order,
            amount=amount,
            status=status,
            notes=f"Imported from WordPress (source ID: {source_id})",
            created_at=created_at or timezone.now(),
            approved_at=approved_at,
            paid_at=paid_at,
        )

        self.commission_map[source_id] = commission
        self.imported_ids["commission_ids"].append(commission.id)
        self.stats["commissions"]["created"] += 1

    def _get_program_for_commission(self, source):
        """Get program for a commission from plan_id or default."""
        plan_id = str(source.get("plan_id", ""))
        if plan_id and plan_id in self.plan_map:
            return self.plan_map[plan_id]
        if self.plan_map:
            return next(iter(self.plan_map.values()))
        return None

    # --- Step 4: Payouts ---

    def _import_payouts(self, progress_bar=True):
        """Import payouts."""
        payouts = self.client.fetch_all_payouts()

        if not payouts:
            logger.info("No payouts to import")
            return

        iterator = tqdm(payouts, desc="💸 Payouts", unit="pay", disable=not progress_bar)

        for source_payout in iterator:
            try:
                self._import_single_payout(source_payout)
            except Exception as e:
                self.stats["payouts"]["errors"] += 1
                logger.error(f"Failed to import payout {source_payout.get('source_id')}: {e}")

    def _import_single_payout(self, source):
        """Import a single payout."""
        source_id = str(source.get("source_id", ""))
        affiliate_source_id = str(source.get("affiliate_id", ""))

        # Look up affiliate
        affiliate = self.affiliate_map.get(affiliate_source_id)
        if not affiliate:
            logger.warning(
                f"Payout {source_id}: affiliate {affiliate_source_id} not found, skipping"
            )
            self.stats["payouts"]["skipped"] += 1
            return

        # Parse amount
        try:
            amount = Decimal(str(source.get("amount", 0)))
        except (InvalidOperation, ValueError):
            amount = Decimal("0")

        if amount <= 0:
            self.stats["payouts"]["skipped"] += 1
            return

        # Parse dates
        created_at = self._parse_date(source.get("created_at"))

        payout = Payout.objects.create(
            affiliate=affiliate,
            amount=amount,
            method=source.get("method", "manual") or "manual",
            status="completed",
            currency=source.get("currency") or get_default_currency(),
            reference=f"WP import: {source_id}",
            notes=f"Imported from WordPress (source ID: {source_id})",
            created_at=created_at or timezone.now(),
            completed_at=created_at or timezone.now(),
        )

        # Link commissions if referral_ids provided
        referral_ids = source.get("referral_ids", [])
        if referral_ids:
            linked_commissions = []
            for ref_id in referral_ids:
                commission = self.commission_map.get(str(ref_id))
                if commission:
                    linked_commissions.append(commission)
            if linked_commissions:
                payout.commissions.set(linked_commissions)

        self.imported_ids["payout_ids"].append(payout.id)
        self.stats["payouts"]["created"] += 1

    # --- Utilities ---

    def _parse_date(self, date_string):
        """Parse a date string from the bridge API into a timezone-aware datetime."""
        if not date_string:
            return None
        # Use the existing WooCommerce date parser (handles ISO format)
        return parse_woocommerce_datetime(date_string)
