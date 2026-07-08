"""
Active Subscriptions Sync Serializer

Handles export/import of subscription data:
- PlanPricingTier
- CustomerSubscription
- PaymentToken
- CustomerSubscriptionAddon
- SubscriptionDiscount
- BillingCycleLog
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer
from ..credential_handler import redact_credentials

logger = logging.getLogger(__name__)

PRICING_TIER_FIELDS = [
    'tier_name', 'billing_cycle', 'billing_interval',
    'discount_percentage', 'is_default', 'is_active', 'sort_order',
]

SUBSCRIPTION_FIELDS = [
    'quantity', 'provider_mode', 'provider_subscription_id',
    'status', 'billing_cycle_count', 'last_billing_status',
    'cancellation_type', 'cancellation_reason',
    'pause_reason', 'scheduled_plan_change',
]

SUBSCRIPTION_DATETIME_FIELDS = [
    'current_period_start', 'current_period_end',
    'next_billing_date', 'trial_end_date',
    'canceled_at', 'minimum_commitment_end_date',
    'paused_at', 'auto_resume_date',
    'grace_period_end_date', 'reactivation_deadline',
    'last_billing_date',
]

PAYMENT_TOKEN_FIELDS = [
    'payment_method_type', 'card_brand', 'card_last4',
    'card_exp_month', 'card_exp_year',
    'billing_address_line1', 'billing_address_line2',
    'billing_city', 'billing_state', 'billing_postal_code', 'billing_country',
    'is_default', 'is_active', 'is_verified',
]

ADDON_FIELDS = ['quantity', 'is_active']

DISCOUNT_FIELDS = [
    'coupon_code', 'discount_type', 'value',
    'duration_type', 'duration_months', 'remaining_cycles', 'is_active',
]

BILLING_CYCLE_FIELDS = [
    'cycle_number', 'status', 'billing_breakdown',
    'retry_count', 'max_retries', 'error_message', 'error_code',
]

# MoneyField amounts serialized separately (str conversion)
BILLING_MONEY_FIELDS = [
    'base_amount', 'quantity_amount', 'addons_amount',
    'discount_amount', 'tax_amount', 'proration_amount', 'total_amount',
]


class SubscriptionsActiveSerializer(CollectionSyncSerializer):
    category_key = 'subscriptions_active'
    natural_key_fields = ['_user_email', '_plan_slug']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from subscriptions.models import CustomerSubscription
        self.model_class = CustomerSubscription

    def get_count(self):
        from subscriptions.models import (
            PlanPricingTier, CustomerSubscription, PaymentToken,
            CustomerSubscriptionAddon, SubscriptionDiscount, BillingCycleLog,
        )
        return (
            PlanPricingTier.objects.count()
            + CustomerSubscription.objects.count()
            + PaymentToken.objects.count()
            + CustomerSubscriptionAddon.objects.count()
            + SubscriptionDiscount.objects.count()
            + BillingCycleLog.objects.count()
        )

    def export(self, credential_mode='redact'):
        from subscriptions.models import (
            PlanPricingTier, CustomerSubscription, PaymentToken,
            CustomerSubscriptionAddon, SubscriptionDiscount, BillingCycleLog,
        )

        items = []

        # Pricing Tiers
        for tier in PlanPricingTier.objects.select_related('plan').all():
            data = {f: getattr(tier, f) for f in PRICING_TIER_FIELDS}
            data['_source_pk'] = str(tier.pk)
            data['_model'] = 'PlanPricingTier'
            data['_plan_slug'] = tier.plan.slug
            # Convert Decimal
            if data.get('discount_percentage') is not None:
                data['discount_percentage'] = str(data['discount_percentage'])
            items.append(data)

        # Active Subscriptions
        for sub in CustomerSubscription.objects.select_related(
            'user', 'plan', 'pricing_tier', 'product', 'variant',
            'payment_provider_account', 'payment_token',
        ).all():
            data = {f: getattr(sub, f) for f in SUBSCRIPTION_FIELDS}
            data['_source_pk'] = sub.pk
            data['_model'] = 'CustomerSubscription'
            data['_subscription_id'] = str(sub.subscription_id)
            data['_user_email'] = sub.user.email
            data['_plan_slug'] = sub.plan.slug
            data['_product_sku'] = sub.product.sku if sub.product else None
            data['_variant_sku'] = sub.variant.sku if sub.variant else None

            # FK references
            if sub.payment_provider_account:
                data['_payment_provider_name'] = sub.payment_provider_account.display_name
            if sub.payment_token:
                data['_payment_token_id'] = str(sub.payment_token.token_id)

            # Proration credit (MoneyField)
            if sub.proration_credit:
                data['_proration_credit'] = str(sub.proration_credit.amount)
                data['_proration_credit_currency'] = str(sub.proration_credit.currency)

            # Datetime fields
            for dt in SUBSCRIPTION_DATETIME_FIELDS:
                val = getattr(sub, dt, None)
                if val and hasattr(val, 'isoformat'):
                    data[f'_{dt}'] = val.isoformat()

            items.append(data)

        # Payment Tokens
        for token in PaymentToken.objects.select_related(
            'user', 'provider_account',
        ).filter(is_active=True):
            data = {f: getattr(token, f) for f in PAYMENT_TOKEN_FIELDS}
            data['_source_pk'] = str(token.pk)
            data['_model'] = 'PaymentToken'
            data['_token_id'] = str(token.token_id)
            data['_user_email'] = token.user.email
            data['_provider_name'] = token.provider_account.display_name

            # gateway_customer_id and gateway_token_id are credentials
            if credential_mode == 'decrypt':
                data['_credentials'] = {
                    'gateway_customer_id': token.gateway_customer_id,
                    'gateway_token_id': token.gateway_token_id,
                }
            elif credential_mode == 'redact':
                data['_credentials_redacted'] = redact_credentials({
                    'gateway_customer_id': token.gateway_customer_id,
                    'gateway_token_id': token.gateway_token_id,
                })

            items.append(data)

        # Customer Subscription Addons
        for addon in CustomerSubscriptionAddon.objects.select_related(
            'subscription__user', 'subscription__plan', 'addon',
        ).all():
            data = {f: getattr(addon, f) for f in ADDON_FIELDS}
            data['_source_pk'] = str(addon.pk)
            data['_model'] = 'CustomerSubscriptionAddon'
            data['_subscription_id'] = str(addon.subscription.subscription_id)
            data['_addon_name'] = addon.addon.name
            data['_plan_slug'] = addon.addon.plan.slug

            # Datetime fields
            if addon.deactivated_at:
                data['_deactivated_at'] = addon.deactivated_at.isoformat()

            items.append(data)

        # Subscription Discounts
        for disc in SubscriptionDiscount.objects.select_related(
            'subscription__user', 'subscription__plan',
        ).all():
            data = {f: getattr(disc, f) for f in DISCOUNT_FIELDS}
            data['_source_pk'] = str(disc.pk)
            data['_model'] = 'SubscriptionDiscount'
            data['_subscription_id'] = str(disc.subscription.subscription_id)

            # Convert Decimal
            if data.get('value') is not None:
                data['value'] = str(data['value'])

            # Datetime
            if disc.expires_at:
                data['_expires_at'] = disc.expires_at.isoformat()

            items.append(data)

        # Billing Cycle Logs
        for log in BillingCycleLog.objects.select_related(
            'subscription__user', 'subscription__plan',
        ).all():
            data = {f: getattr(log, f) for f in BILLING_CYCLE_FIELDS}
            data['_source_pk'] = str(log.pk)
            data['_model'] = 'BillingCycleLog'
            data['_subscription_id'] = str(log.subscription.subscription_id)

            # Serialize MoneyField amounts as strings
            for mf in BILLING_MONEY_FIELDS:
                val = getattr(log, mf, None)
                data[f'_{mf}'] = str(val.amount) if val else '0.00'
                data[f'_{mf}_currency'] = str(val.currency) if val else 'USD'

            # Datetime fields
            if log.billing_date:
                data['_billing_date'] = log.billing_date.isoformat()
            if log.next_retry_date:
                data['_next_retry_date'] = log.next_retry_date.isoformat()

            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        order_map = {
            'PlanPricingTier': 0,
            'CustomerSubscription': 1,
            'PaymentToken': 2,
            'CustomerSubscriptionAddon': 3,
            'SubscriptionDiscount': 4,
            'BillingCycleLog': 5,
        }
        sorted_items = sorted(items, key=lambda x: order_map.get(x.get('_model'), 99))

        for item in sorted_items:
            model_type = item.get('_model')
            try:
                with transaction.atomic():
                    if model_type == 'PlanPricingTier':
                        self._import_pricing_tier(item)
                    elif model_type == 'CustomerSubscription':
                        self._import_subscription(item)
                    elif model_type == 'PaymentToken':
                        self._import_payment_token(item)
                    elif model_type == 'CustomerSubscriptionAddon':
                        self._import_addon(item)
                    elif model_type == 'SubscriptionDiscount':
                        self._import_discount(item)
                    elif model_type == 'BillingCycleLog':
                        self._import_billing_cycle(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type}: {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_pricing_tier(self, item):
        from subscriptions.models import SubscriptionPlan, PlanPricingTier

        plan = SubscriptionPlan.objects.filter(slug=item['_plan_slug']).first()
        if not plan:
            raise ValueError(f"Plan not found: {item['_plan_slug']}")

        existing = PlanPricingTier.objects.filter(
            plan=plan,
            billing_cycle=item.get('billing_cycle', ''),
            billing_interval=item.get('billing_interval', 1),
        ).first()
        obj = existing or PlanPricingTier(plan=plan)

        for f in PRICING_TIER_FIELDS:
            if f in item:
                val = item[f]
                if f == 'discount_percentage' and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)
        obj.save()

    def _import_subscription(self, item):
        from subscriptions.models import (
            SubscriptionPlan, PlanPricingTier, CustomerSubscription, PaymentToken,
        )
        from payment_providers.models import PaymentProviderAccount
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        from djmoney.money import Money
        User = get_user_model()

        user = User.objects.filter(email=item['_user_email']).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        plan = SubscriptionPlan.objects.filter(slug=item['_plan_slug']).first()
        if not plan:
            raise ValueError(f"Plan not found: {item['_plan_slug']}")

        # Find or create
        sub_id = item.get('_subscription_id')
        existing = None
        if sub_id:
            existing = CustomerSubscription.objects.filter(
                subscription_id=sub_id,
            ).first()
        if not existing:
            existing = CustomerSubscription.objects.filter(
                user=user, plan=plan,
            ).first()

        sub = existing or CustomerSubscription(user=user, plan=plan)

        for f in SUBSCRIPTION_FIELDS:
            if f in item:
                setattr(sub, f, item[f])

        # Resolve pricing tier
        pricing_tier = PlanPricingTier.objects.filter(plan=plan).first()
        if pricing_tier:
            sub.pricing_tier = pricing_tier

        # Product/variant
        if item.get('_product_sku'):
            from catalog.models import Product
            sub.product = Product.objects.filter(sku=item['_product_sku']).first()
        if item.get('_variant_sku'):
            from catalog.models import ProductVariant
            sub.variant = ProductVariant.objects.filter(sku=item['_variant_sku']).first()

        # Payment provider and token references
        if item.get('_payment_provider_name'):
            provider = PaymentProviderAccount.objects.filter(
                display_name=item['_payment_provider_name'],
            ).first()
            if provider:
                sub.payment_provider_account = provider
        if item.get('_payment_token_id'):
            token = PaymentToken.objects.filter(
                token_id=item['_payment_token_id'],
            ).first()
            if token:
                sub.payment_token = token

        # Proration credit (MoneyField)
        if item.get('_proration_credit') is not None:
            currency = item.get('_proration_credit_currency', 'USD')
            sub.proration_credit = Money(Decimal(str(item['_proration_credit'])), currency)

        # Datetime fields
        for dt in SUBSCRIPTION_DATETIME_FIELDS:
            val = item.get(f'_{dt}')
            if val:
                parsed = parse_datetime(val)
                if parsed:
                    setattr(sub, dt, parsed)

        sub.save()

    def _import_payment_token(self, item):
        from subscriptions.models import PaymentToken
        from payment_providers.models import PaymentProviderAccount
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.filter(email=item['_user_email']).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        provider = PaymentProviderAccount.objects.filter(
            display_name=item['_provider_name'],
        ).first()
        if not provider:
            raise ValueError(f"Payment provider not found: {item['_provider_name']}")

        # Credentials
        creds = item.get('_credentials', {})
        gateway_token_id = creds.get('gateway_token_id', '')
        gateway_customer_id = creds.get('gateway_customer_id', '')

        if not gateway_token_id:
            raise ValueError("PaymentToken requires gateway_token_id in credentials")

        existing = PaymentToken.objects.filter(
            user=user,
            provider_account=provider,
            gateway_token_id=gateway_token_id,
        ).first()
        obj = existing or PaymentToken(
            user=user,
            provider_account=provider,
            gateway_token_id=gateway_token_id,
        )

        for f in PAYMENT_TOKEN_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        if gateway_customer_id:
            obj.gateway_customer_id = gateway_customer_id

        obj.save()

    def _import_addon(self, item):
        from subscriptions.models import (
            CustomerSubscription, CustomerSubscriptionAddon, PlanAddon,
        )
        from django.utils.dateparse import parse_datetime

        sub = CustomerSubscription.objects.filter(
            subscription_id=item['_subscription_id'],
        ).first()
        if not sub:
            raise ValueError(f"Subscription not found: {item['_subscription_id']}")

        addon = PlanAddon.objects.filter(
            plan__slug=item.get('_plan_slug', ''),
            name=item['_addon_name'],
        ).first()
        if not addon:
            raise ValueError(f"PlanAddon not found: {item['_addon_name']}")

        existing = CustomerSubscriptionAddon.objects.filter(
            subscription=sub, addon=addon,
        ).first()
        obj = existing or CustomerSubscriptionAddon(subscription=sub, addon=addon)

        for f in ADDON_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        deactivated = item.get('_deactivated_at')
        if deactivated:
            parsed = parse_datetime(deactivated)
            if parsed:
                obj.deactivated_at = parsed

        obj.save()

    def _import_discount(self, item):
        from subscriptions.models import CustomerSubscription, SubscriptionDiscount
        from django.utils.dateparse import parse_datetime

        sub = CustomerSubscription.objects.filter(
            subscription_id=item['_subscription_id'],
        ).first()
        if not sub:
            raise ValueError(f"Subscription not found: {item['_subscription_id']}")

        # Match by subscription + coupon_code (or subscription + discount_type for non-coupon)
        coupon = item.get('coupon_code', '')
        if coupon:
            existing = SubscriptionDiscount.objects.filter(
                subscription=sub, coupon_code=coupon,
            ).first()
        else:
            existing = SubscriptionDiscount.objects.filter(
                subscription=sub,
                discount_type=item.get('discount_type', ''),
                coupon_code='',
            ).first()

        obj = existing or SubscriptionDiscount(subscription=sub)

        for f in DISCOUNT_FIELDS:
            if f in item:
                val = item[f]
                if f == 'value' and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)

        expires = item.get('_expires_at')
        if expires:
            parsed = parse_datetime(expires)
            if parsed:
                obj.expires_at = parsed

        obj.save()

    def _import_billing_cycle(self, item):
        from subscriptions.models import CustomerSubscription, BillingCycleLog
        from django.utils.dateparse import parse_datetime
        from djmoney.money import Money

        sub = CustomerSubscription.objects.filter(
            subscription_id=item['_subscription_id'],
        ).first()
        if not sub:
            raise ValueError(f"Subscription not found: {item['_subscription_id']}")

        cycle_number = item.get('cycle_number')
        if cycle_number is None:
            raise ValueError("BillingCycleLog requires cycle_number")

        existing = BillingCycleLog.objects.filter(
            subscription=sub, cycle_number=cycle_number,
        ).first()
        obj = existing or BillingCycleLog(subscription=sub, cycle_number=cycle_number)

        for f in BILLING_CYCLE_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        # MoneyField amounts
        for mf in BILLING_MONEY_FIELDS:
            amount_str = item.get(f'_{mf}')
            currency = item.get(f'_{mf}_currency', 'USD')
            if amount_str is not None:
                setattr(obj, mf, Money(Decimal(str(amount_str)), currency))

        # Datetime fields
        billing_date = item.get('_billing_date')
        if billing_date:
            parsed = parse_datetime(billing_date)
            if parsed:
                obj.billing_date = parsed

        next_retry = item.get('_next_retry_date')
        if next_retry:
            parsed = parse_datetime(next_retry)
            if parsed:
                obj.next_retry_date = parsed

        obj.save()

    def generate_diff(self, remote_data):
        from subscriptions.models import (
            PlanPricingTier, CustomerSubscription, PaymentToken,
            CustomerSubscriptionAddon, SubscriptionDiscount, BillingCycleLog,
            SubscriptionPlan, PlanAddon,
        )
        from django.contrib.auth import get_user_model
        User = get_user_model()

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            existing = None
            fields = []
            name = '?'

            if model_type == 'PlanPricingTier':
                plan = SubscriptionPlan.objects.filter(slug=item.get('_plan_slug', '')).first()
                if plan:
                    existing = PlanPricingTier.objects.filter(
                        plan=plan,
                        billing_cycle=item.get('billing_cycle', ''),
                        billing_interval=item.get('billing_interval', 1),
                    ).first()
                name = f"{item.get('_plan_slug', '?')} / {item.get('tier_name', '?')}"
                fields = PRICING_TIER_FIELDS

            elif model_type == 'CustomerSubscription':
                user = User.objects.filter(email=item.get('_user_email', '')).first()
                plan = SubscriptionPlan.objects.filter(slug=item.get('_plan_slug', '')).first()
                if user and plan:
                    existing = CustomerSubscription.objects.filter(user=user, plan=plan).first()
                name = f"{item.get('_user_email', '?')} / {item.get('_plan_slug', '?')}"
                fields = SUBSCRIPTION_FIELDS

            elif model_type == 'PaymentToken':
                name = f"{item.get('_user_email', '?')} / {item.get('payment_method_type', '?')}"
                fields = PAYMENT_TOKEN_FIELDS

            elif model_type == 'CustomerSubscriptionAddon':
                sub = CustomerSubscription.objects.filter(
                    subscription_id=item.get('_subscription_id', ''),
                ).first()
                addon = PlanAddon.objects.filter(
                    plan__slug=item.get('_plan_slug', ''),
                    name=item.get('_addon_name', ''),
                ).first()
                if sub and addon:
                    existing = CustomerSubscriptionAddon.objects.filter(
                        subscription=sub, addon=addon,
                    ).first()
                name = f"{item.get('_addon_name', '?')}"
                fields = ADDON_FIELDS

            elif model_type == 'SubscriptionDiscount':
                sub = CustomerSubscription.objects.filter(
                    subscription_id=item.get('_subscription_id', ''),
                ).first()
                coupon = item.get('coupon_code', '')
                if sub and coupon:
                    existing = SubscriptionDiscount.objects.filter(
                        subscription=sub, coupon_code=coupon,
                    ).first()
                name = coupon or item.get('discount_type', '?')
                fields = DISCOUNT_FIELDS

            elif model_type == 'BillingCycleLog':
                sub = CustomerSubscription.objects.filter(
                    subscription_id=item.get('_subscription_id', ''),
                ).first()
                if sub and item.get('cycle_number') is not None:
                    existing = BillingCycleLog.objects.filter(
                        subscription=sub, cycle_number=item['cycle_number'],
                    ).first()
                name = f"Cycle {item.get('cycle_number', '?')}"
                fields = BILLING_CYCLE_FIELDS

            else:
                continue

            if existing and fields:
                field_changes = self._compute_field_diff(existing, item, fields)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': model_type,
                        'name': name, 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': model_type,
                    'name': name,
                    'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                })

        adds = sum(1 for c in changes if c['type'] == 'add')
        mods = sum(1 for c in changes if c['type'] == 'modify')
        parts = []
        if adds:
            parts.append(f'{adds} addition(s)')
        if mods:
            parts.append(f'{mods} modification(s)')

        return {
            'changes': changes,
            'warnings': [],
            'summary': ', '.join(parts) if parts else 'No changes',
        }

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
