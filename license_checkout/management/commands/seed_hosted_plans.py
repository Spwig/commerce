"""
Seed the hosted subscription plans for the spwig.com pricing page.

Creates/updates the 4 plan tiers and validates their presence.
Plans map 1:1 to SubscriptionPlan records on the update server by slug.

Usage:
    python manage.py seed_hosted_plans
"""

from django.core.management.base import BaseCommand
from djmoney.money import Money

from license_checkout.models import HostedPlan


PLANS = [
    {
        'slug': 'starter',
        'name': 'Starter',
        'tagline': 'Everything you need to launch your online store',
        'monthly_price': Money(69, 'EUR'),
        'annual_price': Money(59, 'EUR'),
        'infra_tier': 'shared',
        'max_products': 1000,
        'max_staff': 3,
        'storage_gb': 25,
        'emails_monthly': 3000,
        'includes_pos': False,
        'includes_api': False,
        'includes_sla': False,
        'includes_custom_domain': True,
        'features': [
            'upTo1000Products',
            'threeStaffAccounts',
            'twentyFiveGbStorage',
            'customDomain',
            'aiTranslations',
            'basicReporting',
            'emailSupport48h',
            'zeroTransactionFees',
        ],
        'is_featured': False,
        'intro_monthly_discount_percent': 50,
        'intro_monthly_discount_cycles': 3,
        'intro_annual_discount_percent': 30,
        'intro_annual_discount_cycles': 1,
        'sort_order': 0,
    },
    {
        'slug': 'growth',
        'name': 'Growth',
        'tagline': 'Scale your business with advanced tools and integrations',
        'monthly_price': Money(99, 'EUR'),
        'annual_price': Money(89, 'EUR'),
        'infra_tier': 'shared',
        'max_products': 5000,
        'max_staff': 10,
        'storage_gb': 100,
        'emails_monthly': 10000,
        'includes_pos': False,
        'includes_api': True,
        'includes_sla': False,
        'includes_custom_domain': True,
        'features': [
            'upTo5000Products',
            'tenStaffAccounts',
            'hundredGbStorage',
            'customDomain',
            'aiTranslations',
            'apiAccess',
            'advancedReporting',
            'emailSupport24h',
            'zeroTransactionFees',
        ],
        'is_featured': True,
        'intro_monthly_discount_percent': 50,
        'intro_monthly_discount_cycles': 3,
        'intro_annual_discount_percent': 30,
        'intro_annual_discount_cycles': 1,
        'sort_order': 1,
    },
    {
        'slug': 'pro',
        'name': 'Pro',
        'tagline': 'Dedicated performance for established businesses',
        'monthly_price': Money(169, 'EUR'),
        'annual_price': Money(149, 'EUR'),
        'infra_tier': 'dedicated',
        'max_products': 0,  # unlimited
        'max_staff': 25,
        'storage_gb': 250,
        'emails_monthly': 25000,
        'includes_pos': False,
        'includes_api': True,
        'includes_sla': False,
        'includes_custom_domain': True,
        'features': [
            'unlimitedProducts',
            'twentyFiveStaffAccounts',
            'twoFiftyGbStorage',
            'dedicatedResources',
            'customDomain',
            'aiTranslations',
            'apiAccess',
            'fullReporting',
            'prioritySupport12h',
            'zeroTransactionFees',
        ],
        'is_featured': False,
        'intro_monthly_discount_percent': 50,
        'intro_monthly_discount_cycles': 3,
        'intro_annual_discount_percent': 30,
        'intro_annual_discount_cycles': 1,
        'sort_order': 2,
    },
    {
        'slug': 'pro-plus',
        'name': 'Pro Plus',
        'tagline': 'Mission-critical hosting with SLA and POS included',
        'monthly_price': Money(269, 'EUR'),
        'annual_price': Money(229, 'EUR'),
        'infra_tier': 'premium',
        'max_products': 0,  # unlimited
        'max_staff': 0,  # unlimited
        'storage_gb': 500,
        'emails_monthly': 50000,
        'includes_pos': True,
        'includes_api': True,
        'includes_sla': True,
        'includes_custom_domain': True,
        'features': [
            'unlimitedProducts',
            'unlimitedStaff',
            'fiveHundredGbStorage',
            'premiumDedicatedResources',
            'customDomain',
            'aiTranslations',
            'apiAccess',
            'fullReportingExports',
            'posIncluded',
            'slaUptime',
            'prioritySupportSla',
            'zeroTransactionFees',
        ],
        'is_featured': False,
        'intro_monthly_discount_percent': 50,
        'intro_monthly_discount_cycles': 3,
        'intro_annual_discount_percent': 30,
        'intro_annual_discount_cycles': 1,
        'sort_order': 3,
    },
]


class Command(BaseCommand):
    help = 'Seed the hosted subscription plans for the pricing page'

    def handle(self, *args, **options):
        from django.conf import settings
        if not getattr(settings, 'SPWIG_IS_HQ', False):
            self.stdout.write(self.style.WARNING(
                'Skipping — this command only runs on the Spwig HQ instance.'
            ))
            return

        for plan_data in PLANS:
            slug = plan_data['slug']
            defaults = {k: v for k, v in plan_data.items() if k != 'slug'}
            obj, created = HostedPlan.objects.update_or_create(
                slug=slug,
                defaults=defaults,
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(
                f"  {action}: {obj.name} "
                f"(EUR {obj.annual_price.amount}/mo annual, "
                f"EUR {obj.monthly_price.amount}/mo monthly)"
            ))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {len(PLANS)} hosted plans seeded."
        ))
        self.stdout.write(self.style.NOTICE(
            "\nReminder: Ensure matching SubscriptionPlan records exist on the "
            "update server with the same slugs (starter, growth, pro, pro-plus)."
        ))
