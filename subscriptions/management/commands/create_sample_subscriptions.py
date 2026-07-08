"""
Management command to create sample subscription plan templates.

These are subscription templates that apply discount percentages to product prices.
Actual subscription prices are calculated from the product price when a customer subscribes.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from decimal import Decimal
from moneyed import Money
from subscriptions.models import SubscriptionPlan, PlanPricingTier, PlanAddon


class Command(BaseCommand):
    help = 'Create sample subscription plans with tiered pricing and add-ons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample subscription plans...'))

        # Clear existing sample data (only if no subscriptions exist)
        from subscriptions.models import CustomerSubscription
        if CustomerSubscription.objects.exists():
            self.stdout.write(self.style.WARNING('Subscriptions exist - skipping sample data creation'))
            return

        # Delete existing plans
        SubscriptionPlan.objects.all().delete()

        # 1. Basic Plan - Simple tiered pricing, no add-ons
        self.stdout.write('Creating Basic Plan...')
        basic_plan = SubscriptionPlan.objects.create(
            name='Basic Plan',
            slug=slugify('Basic Plan'),
            description='Perfect for individuals getting started with our service',
            pricing_model='tiered',
            allow_quantity=False,
            cancellation_policy='anytime',
            is_active=True,
            is_public=True,
            trial_period_days=14,
            trial_price=Money(0, 'USD'),
        )

        # Basic Plan Tiers (discounts applied to product price)
        PlanPricingTier.objects.create(
            plan=basic_plan,
            tier_name='Monthly',
            billing_cycle='monthly',
            billing_interval=1,
            discount_percentage=Decimal('0.00'),  # Full product price
            is_default=True,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Monthly',
                    'es': 'Mensual',
                    'fr': 'Mensuel',
                }
            }
        )

        PlanPricingTier.objects.create(
            plan=basic_plan,
            tier_name='Quarterly - Save 10%',
            billing_cycle='quarterly',
            billing_interval=1,
            discount_percentage=Decimal('10.00'),  # 10% off product price
            is_default=False,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Quarterly - Save 10%',
                    'es': 'Trimestral - Ahorre 10%',
                    'fr': 'Trimestriel - Économisez 10%',
                }
            }
        )

        PlanPricingTier.objects.create(
            plan=basic_plan,
            tier_name='Annual - Save 20%',
            billing_cycle='annual',
            billing_interval=1,
            discount_percentage=Decimal('20.00'),  # 20% off product price
            is_default=False,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Annual - Save 20%',
                    'es': 'Anual - Ahorre 20%',
                    'fr': 'Annuel - Économisez 20%',
                }
            }
        )

        # 2. Pro Plan - Tiered pricing + quantity-based + add-ons
        self.stdout.write('Creating Pro Plan...')
        pro_plan = SubscriptionPlan.objects.create(
            name='Pro Plan',
            slug=slugify('Pro Plan'),
            description='For growing teams who need advanced features and collaboration',
            pricing_model='quantity_based',
            allow_quantity=True,
            minimum_quantity=1,
            maximum_quantity=50,
            cancellation_policy='end_of_period',
            is_active=True,
            is_public=True,
            trial_period_days=30,
            trial_price=Money(0, 'USD'),
        )

        # Pro Plan Tiers (discounts applied to product price, supports quantity)
        PlanPricingTier.objects.create(
            plan=pro_plan,
            tier_name='Monthly per user',
            billing_cycle='monthly',
            billing_interval=1,
            discount_percentage=Decimal('0.00'),  # Full product price
            is_default=True,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Monthly per user',
                    'es': 'Mensual por usuario',
                    'fr': 'Mensuel par utilisateur',
                }
            }
        )

        PlanPricingTier.objects.create(
            plan=pro_plan,
            tier_name='Quarterly - Save 10%',
            billing_cycle='quarterly',
            billing_interval=1,
            discount_percentage=Decimal('10.00'),  # 10% off product price
            is_default=False,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Quarterly - Save 10%',
                    'es': 'Trimestral - Ahorre 10%',
                    'fr': 'Trimestriel - Économisez 10%',
                }
            }
        )

        PlanPricingTier.objects.create(
            plan=pro_plan,
            tier_name='Annual - Save 20%',
            billing_cycle='annual',
            billing_interval=1,
            discount_percentage=Decimal('20.00'),  # 20% off product price
            is_default=False,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Annual - Save 20%',
                    'es': 'Anual - Ahorre 20%',
                    'fr': 'Annuel - Économisez 20%',
                }
            }
        )

        # Pro Plan Add-ons
        PlanAddon.objects.create(
            plan=pro_plan,
            name='Priority Support',
            description='24/7 priority support with dedicated account manager',
            price=Money(99, 'USD'),
            billing_frequency='per_cycle',
            allow_quantity=False,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'Priority Support',
                    'es': 'Soporte Prioritario',
                    'fr': 'Support Prioritaire',
                },
                'description': {
                    'en': '24/7 priority support with dedicated account manager',
                    'es': 'Soporte prioritario 24/7 con gerente de cuenta dedicado',
                    'fr': 'Support prioritaire 24h/24 et 7j/7 avec gestionnaire de compte dédié',
                }
            }
        )

        PlanAddon.objects.create(
            plan=pro_plan,
            name='Additional Storage (100GB)',
            description='Extra 100GB of storage space',
            price=Money(20, 'USD'),
            billing_frequency='per_cycle',
            allow_quantity=True,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'Additional Storage (100GB)',
                    'es': 'Almacenamiento Adicional (100GB)',
                    'fr': 'Stockage Supplémentaire (100 Go)',
                },
                'description': {
                    'en': 'Extra 100GB of storage space',
                    'es': '100 GB adicionales de espacio de almacenamiento',
                    'fr': '100 Go supplémentaires d\'espace de stockage',
                }
            }
        )

        # 3. Enterprise Plan - Advanced features + minimum commitment
        self.stdout.write('Creating Enterprise Plan...')
        enterprise_plan = SubscriptionPlan.objects.create(
            name='Enterprise Plan',
            slug=slugify('Enterprise Plan'),
            description='For large organizations requiring enterprise-grade security and support',
            pricing_model='quantity_based',
            allow_quantity=True,
            minimum_quantity=10,
            maximum_quantity=None,  # Unlimited
            cancellation_policy='minimum_commitment',
            minimum_commitment_cycles=12,  # 1 year minimum
            grace_period_days=7,
            reactivation_period_days=30,
            is_active=True,
            is_public=True,
            trial_period_days=0,  # No trial for enterprise
        )

        # Enterprise Plan Tiers (discounts applied to product price, supports quantity)
        PlanPricingTier.objects.create(
            plan=enterprise_plan,
            tier_name='Monthly per user',
            billing_cycle='monthly',
            billing_interval=1,
            discount_percentage=Decimal('0.00'),  # Full product price
            is_default=True,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Monthly per user',
                    'es': 'Mensual por usuario',
                    'fr': 'Mensuel par utilisateur',
                }
            }
        )

        PlanPricingTier.objects.create(
            plan=enterprise_plan,
            tier_name='Quarterly - Save 10%',
            billing_cycle='quarterly',
            billing_interval=1,
            discount_percentage=Decimal('10.00'),  # 10% off product price
            is_default=False,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Quarterly - Save 10%',
                    'es': 'Trimestral - Ahorre 10%',
                    'fr': 'Trimestriel - Économisez 10%',
                }
            }
        )

        PlanPricingTier.objects.create(
            plan=enterprise_plan,
            tier_name='Annual - Save 20%',
            billing_cycle='annual',
            billing_interval=1,
            discount_percentage=Decimal('20.00'),  # 20% off product price
            is_default=False,
            is_active=True,
            translations={
                'tier_name': {
                    'en': 'Annual - Save 20%',
                    'es': 'Anual - Ahorre 20%',
                    'fr': 'Annuel - Économisez 20%',
                }
            }
        )

        # Enterprise Plan Add-ons
        PlanAddon.objects.create(
            plan=enterprise_plan,
            name='Dedicated Infrastructure',
            description='Isolated infrastructure with dedicated resources',
            price=Money(500, 'USD'),
            billing_frequency='per_cycle',
            allow_quantity=False,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'Dedicated Infrastructure',
                    'es': 'Infraestructura Dedicada',
                    'fr': 'Infrastructure Dédiée',
                },
                'description': {
                    'en': 'Isolated infrastructure with dedicated resources',
                    'es': 'Infraestructura aislada con recursos dedicados',
                    'fr': 'Infrastructure isolée avec ressources dédiées',
                }
            }
        )

        PlanAddon.objects.create(
            plan=enterprise_plan,
            name='SSO Integration',
            description='Single Sign-On with SAML 2.0',
            price=Money(200, 'USD'),
            billing_frequency='one_time',
            allow_quantity=False,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'SSO Integration',
                    'es': 'Integración SSO',
                    'fr': 'Intégration SSO',
                },
                'description': {
                    'en': 'Single Sign-On with SAML 2.0',
                    'es': 'Inicio de sesión único con SAML 2.0',
                    'fr': 'Authentification unique avec SAML 2.0',
                }
            }
        )

        PlanAddon.objects.create(
            plan=enterprise_plan,
            name='Advanced Analytics',
            description='Custom dashboards and advanced reporting',
            price=Money(150, 'USD'),
            billing_frequency='per_cycle',
            allow_quantity=False,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'Advanced Analytics',
                    'es': 'Análisis Avanzados',
                    'fr': 'Analytique Avancée',
                },
                'description': {
                    'en': 'Custom dashboards and advanced reporting',
                    'es': 'Paneles personalizados e informes avanzados',
                    'fr': 'Tableaux de bord personnalisés et rapports avancés',
                }
            }
        )

        PlanAddon.objects.create(
            plan=enterprise_plan,
            name='API Access',
            description='Full API access with increased rate limits',
            price=Money(100, 'USD'),
            billing_frequency='per_cycle',
            allow_quantity=False,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'API Access',
                    'es': 'Acceso API',
                    'fr': 'Accès API',
                },
                'description': {
                    'en': 'Full API access with increased rate limits',
                    'es': 'Acceso completo a la API con límites de tasa aumentados',
                    'fr': 'Accès complet à l\'API avec limites de taux augmentées',
                }
            }
        )

        PlanAddon.objects.create(
            plan=enterprise_plan,
            name='Custom Training',
            description='On-site or virtual training for your team',
            price=Money(1000, 'USD'),
            billing_frequency='one_time',
            allow_quantity=True,
            is_required=False,
            is_active=True,
            translations={
                'name': {
                    'en': 'Custom Training',
                    'es': 'Capacitación Personalizada',
                    'fr': 'Formation Personnalisée',
                },
                'description': {
                    'en': 'On-site or virtual training for your team',
                    'es': 'Capacitación presencial o virtual para su equipo',
                    'fr': 'Formation sur site ou virtuelle pour votre équipe',
                }
            }
        )

        self.stdout.write(self.style.SUCCESS('\n✅ Sample subscription plans created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  - Basic Plan: {basic_plan.pricing_tiers.count()} tiers, {basic_plan.addons.count()} add-ons'))
        self.stdout.write(self.style.SUCCESS(f'  - Pro Plan: {pro_plan.pricing_tiers.count()} tiers, {pro_plan.addons.count()} add-ons'))
        self.stdout.write(self.style.SUCCESS(f'  - Enterprise Plan: {enterprise_plan.pricing_tiers.count()} tiers, {enterprise_plan.addons.count()} add-ons'))
