"""
Seed the default license products for the spwig.com purchase page,
plus the License Maintenance subscription plan used for annual recurring billing.

Usage:
    python manage.py seed_license_products
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from djmoney.money import Money

from license_checkout.models import LicenseProduct


PRODUCTS = [
    {
        'slug': 'trial-core-pos',
        'name': '30-Day Free Trial',
        'product_type': 'trial',
        'price': Money(0, 'EUR'),
        'regular_price': Money(0, 'EUR'),
        'savings_amount': None,
        'features': [
            'fullPlatform',
            'posIncluded',
            'noPaymentRequired',
            'automaticExpiry',
        ],
        'includes_pos': True,
        'trial_days': 30,
        'is_featured': False,
        'note': '',
        'note_link': '',
        'sort_order': 0,
    },
    {
        'slug': 'core-license',
        'name': 'Spwig Core',
        'product_type': 'license',
        'price': Money(249, 'EUR'),
        'regular_price': Money(499, 'EUR'),
        'savings_amount': None,
        'features': [
            'fullEcommerce',
            'unlimitedProducts',
            'multiCurrency',
            'multiLanguage',
            'seoTools',
            'emailMarketing',
            'blogCms',
            'analyticsReporting',
            'perpetualLicense',
            'firstYearMaintenance',
            'selfHosted',
        ],
        'includes_pos': False,
        'trial_days': 0,
        'is_featured': False,
        'note': '',
        'note_link': '',
        'sort_order': 1,
    },
    {
        'slug': 'bundle-core-pos',
        'name': 'Spwig Core + POS',
        'product_type': 'bundle',
        'price': Money(449, 'EUR'),
        'regular_price': Money(898, 'EUR'),
        'savings_amount': Money(449, 'EUR'),
        'features': [
            'everythingInCore',
            'posTerminal',
            'dualScreenDisplay',
            'offlineMode',
            'shiftManagement',
            'thermalPrinting',
            'barcodeScanners',
            'cardReaders',
            'perpetualLicense',
            'firstYearMaintenance',
            'selfHosted',
        ],
        'includes_pos': True,
        'trial_days': 0,
        'is_featured': True,
        'note': '',
        'note_link': '',
        'sort_order': 2,
    },
    {
        'slug': 'pos-addon',
        'name': 'POS Add-on',
        'product_type': 'addon',
        'price': Money(199, 'EUR'),
        'regular_price': Money(399, 'EUR'),
        'savings_amount': None,
        'features': [
            'posTerminal',
            'dualScreenDisplay',
            'offlineMode',
            'shiftManagement',
            'thermalPrinting',
            'barcodeScanners',
            'cardReaders',
        ],
        'includes_pos': True,
        'trial_days': 0,
        'is_featured': False,
        'note': 'Requires Spwig Core license. Purchase from your admin panel.',
        'note_link': '',
        'sort_order': 3,
    },
    {
        'slug': 'dev-license',
        'name': 'Developer License',
        'product_type': 'license',
        'price': Money(50, 'EUR'),
        'regular_price': Money(100, 'EUR'),
        'savings_amount': None,
        'features': [
            'fullPlatform',
            'posIncluded',
            'betaDevChannels',
            'componentDevelopment',
        ],
        'includes_pos': True,
        'trial_days': 0,
        'is_featured': False,
        'note': 'First license free via Developer Portal',
        'note_link': '/for-developers',
        'sort_order': 4,
    },
    {
        'slug': 'maintenance-renewal',
        'name': 'Maintenance Renewal',
        'product_type': 'addon',
        'price': Money(0, 'EUR'),
        'regular_price': Money(0, 'EUR'),
        'savings_amount': None,
        'features': [
            'featureUpdates',
            'securityPatches',
            'spwigServices',
            'technicalSupport',
        ],
        'includes_pos': False,
        'trial_days': 0,
        'is_featured': False,
        'note': 'Price calculated at 25% of current license list price',
        'note_link': '',
        'sort_order': 5,
    },
]


class Command(BaseCommand):
    help = 'Seed the default license products for the purchase page'

    def handle(self, *args, **options):
        from django.conf import settings
        if not getattr(settings, 'SPWIG_IS_HQ', False):
            self.stdout.write(self.style.WARNING(
                'Skipping — this command only runs on the Spwig HQ instance.'
            ))
            return

        for product_data in PRODUCTS:
            slug = product_data['slug']
            obj, created = LicenseProduct.objects.update_or_create(
                slug=slug,
                defaults=product_data,
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(f"  {action}: {obj.name} ({obj.price})")
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {len(PRODUCTS)} license products seeded."
        ))

        # Seed the License Maintenance subscription plan
        self._seed_subscription_plan()

    def _seed_subscription_plan(self):
        """Create the License Maintenance subscription plan + annual pricing tier."""
        from subscriptions.models import SubscriptionPlan, PlanPricingTier

        plan, plan_created = SubscriptionPlan.objects.get_or_create(
            slug='license-maintenance',
            defaults={
                'name': 'License Maintenance',
                'description': (
                    'Annual maintenance subscription for Spwig license holders. '
                    'Includes platform updates, security patches, and new features. '
                    'Billed annually at 25% of license price, starting 12 months '
                    'after purchase.'
                ),
                'pricing_model': 'flat',
                'trial_period_days': 0,
                'cancellation_policy': 'end_of_period',
                'is_active': True,
            },
        )
        action = 'Created' if plan_created else 'Already exists'
        self.stdout.write(self.style.SUCCESS(
            f"  {action}: SubscriptionPlan '{plan.name}'"
        ))

        tier, tier_created = PlanPricingTier.objects.get_or_create(
            plan=plan,
            billing_cycle='annual',
            billing_interval=1,
            defaults={
                'tier_name': 'Annual Maintenance',
                'discount_percentage': Decimal('75.00'),
                'is_default': True,
            },
        )
        action = 'Created' if tier_created else 'Already exists'
        self.stdout.write(self.style.SUCCESS(
            f"  {action}: PlanPricingTier '{tier.tier_name}' "
            f"(annual, 75% discount = 25% of license price)"
        ))
