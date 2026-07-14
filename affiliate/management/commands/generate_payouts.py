"""
Management command to generate affiliate payouts.

Usage:
    ./manage.py generate_payouts [--min-amount 50.00] [--dry-run]

This command:
1. Finds all affiliates with approved commissions
2. Calculates total payout amount per affiliate
3. Creates Payout records for affiliates meeting minimum threshold
4. Marks commissions as 'paid'
"""

import logging
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Sum
from django.utils import timezone

from affiliate.models import Affiliate, Commission, Payout

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate payouts for affiliates with approved commissions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--min-amount", type=float, default=50.00, help="Minimum payout amount (default: 50.00)"
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Preview payouts without creating them"
        )
        parser.add_argument(
            "--affiliate-id", type=int, help="Generate payout for specific affiliate ID only"
        )

    def handle(self, *args, **options):
        min_amount = Decimal(str(options["min_amount"]))
        dry_run = options["dry_run"]
        affiliate_id = options.get("affiliate_id")

        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Affiliate Payout Generation"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(f"Minimum payout amount: ${min_amount}")
        self.stdout.write(f"Dry run: {dry_run}")
        self.stdout.write("")

        # Get approved commissions that haven't been paid
        approved_commissions = Commission.objects.filter(status="approved")

        if affiliate_id:
            approved_commissions = approved_commissions.filter(affiliate_id=affiliate_id)
            self.stdout.write(f"Filtering for affiliate ID: {affiliate_id}\n")

        # Group by affiliate and calculate totals (use amount_base for consistent currency)
        from django.db.models.functions import Coalesce

        affiliate_totals = (
            approved_commissions.values(
                "affiliate", "affiliate__user__username", "affiliate__affiliate_code"
            )
            .annotate(
                total_amount=Coalesce(Sum("amount_base"), Sum("amount")),
                commission_count=Count("id"),
            )
            .filter(total_amount__gte=min_amount)
            .order_by("-total_amount")
        )

        if not affiliate_totals:
            self.stdout.write(
                self.style.WARNING(
                    f"No affiliates found with approved commissions >= ${min_amount}"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f"Found {len(affiliate_totals)} affiliate(s) eligible for payout:\n")
        )

        # Display summary
        total_payout_amount = Decimal("0.00")
        total_commissions = 0

        for item in affiliate_totals:
            self.stdout.write(
                f"  • {item['affiliate__user__username']} "
                f"({item['affiliate__affiliate_code']}): "
                f"${item['total_amount']:.2f} "
                f"({item['commission_count']} commissions)"
            )
            total_payout_amount += item["total_amount"]
            total_commissions += item["commission_count"]

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Total payout amount: ${total_payout_amount:.2f}"))
        self.stdout.write(self.style.SUCCESS(f"Total commissions: {total_commissions}"))
        self.stdout.write("")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN - No payouts created. Remove --dry-run to execute.")
            )
            return

        # Create payouts
        created_count = 0
        failed_count = 0

        for item in affiliate_totals:
            try:
                with transaction.atomic():
                    affiliate = Affiliate.objects.get(id=item["affiliate"])

                    # Get all approved commissions for this affiliate
                    commissions = Commission.objects.filter(affiliate=affiliate, status="approved")

                    # Check if affiliate has sufficient balance (use base currency)
                    if (
                        commissions.aggregate(total=Coalesce(Sum("amount_base"), Sum("amount")))[
                            "total"
                        ]
                        < min_amount
                    ):
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ✗ Skipping {affiliate.user.username}: Insufficient balance"
                            )
                        )
                        continue

                    # Create payout in store's base currency
                    from core.models import SiteSettings

                    settings = SiteSettings.get_settings()
                    payout = Payout.objects.create(
                        affiliate=affiliate,
                        amount=item["total_amount"],
                        currency=settings.default_currency,
                        amount_base=item["total_amount"],
                        base_currency=settings.default_currency,
                        status="pending",
                        payment_method="bank_transfer",  # Default method
                        notes=f"Auto-generated payout for {item['commission_count']} commissions",
                    )

                    # Update commissions to 'paid' status
                    updated_count = commissions.update(status="paid", updated_at=timezone.now())

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Created payout #{payout.id} for {affiliate.user.username}: "
                            f"${payout.amount:.2f} ({updated_count} commissions)"
                        )
                    )

                    created_count += 1

            except Exception as e:
                failed_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"  ✗ Failed to create payout for affiliate {item['affiliate']}: {str(e)}"
                    )
                )
                logger.error(
                    f"Error creating payout for affiliate {item['affiliate']}: {str(e)}",
                    exc_info=True,
                )

        # Final summary
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Summary"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(f"✓ Payouts created: {created_count}")
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"✗ Failed: {failed_count}"))
        self.stdout.write(self.style.SUCCESS(f"Total amount: ${total_payout_amount:.2f}"))
        self.stdout.write("")
