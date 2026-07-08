"""
Commerce Rules Sync Serializer

Handles export/import of commerce rule models:
- VoucherCode (with MoneyFields, M2M to products/categories)
- VoucherRestriction (nested under VoucherCode)
- Promotion (M2M to categories/brands/collections/products)
- LoyaltyTier
- LoyaltyRule (M2M to tiers)
- LoyaltyReward (FK to product/tier, ImageField)
- LoyaltyBadge (FK image → MediaAsset)
- LoyaltyCampaign (M2M target_tiers, FK target_segment)
- LoyaltySegment (segment definitions)
- SubscriptionPlan (MoneyFields)
- PlanAddon (MoneyField, FK to SubscriptionPlan)
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer
from ..file_handler import export_file_field, import_file_field

logger = logging.getLogger(__name__)

VOUCHER_FIELDS = [
    'code', 'name', 'description', 'external_id',
    'discount_type', 'discount_value',
    'application_scope',
    'start_date', 'end_date', 'days_valid',
    'max_uses_total', 'max_uses_per_customer', 'current_uses',
    'exclude_sale_items', 'cannot_combine_with_other_vouchers',
    'cannot_combine_with_sale_items', 'first_time_customers_only',
    'is_active',
]

PROMOTION_FIELDS = [
    'name', 'description',
    'discount_type', 'discount_value',
    'start_date', 'end_date',
    'apply_to', 'priority',
    'can_stack_with_product_sales', 'is_active',
]

LOYALTY_TIER_FIELDS = [
    'name', 'slug', 'description', 'icon', 'color',
    'rank', 'min_spend', 'min_orders', 'min_points_earned',
    'points_multiplier', 'has_free_shipping', 'has_early_access',
    'grace_period_days', 'is_active',
]

LOYALTY_RULE_FIELDS = [
    'name', 'description', 'rule_type', 'action_type', 'event_type',
    'scope', 'scope_filters',
    'points_rate', 'min_order_amount',
    'max_points_per_order', 'max_points_per_day', 'max_points_per_member',
    'priority', 'is_exclusive',
    'points_pending_days', 'points_expire_days',
    'start_date', 'end_date', 'is_active',
]

LOYALTY_REWARD_FIELDS = [
    'name', 'slug', 'description', 'reward_type',
    'points_cost', 'discount_type', 'discount_value',
    'min_purchase_amount', 'icon',
    'is_active', 'start_date', 'end_date',
    'quantity_total', 'quantity_remaining',
    'max_redemptions_per_member',
    'redemption_expires_days', 'featured', 'display_order', 'terms',
]

SUBSCRIPTION_PLAN_FIELDS = [
    'name', 'slug', 'description', 'translations',
    'pricing_model', 'allow_quantity',
    'minimum_quantity', 'maximum_quantity',
    'trial_period_days', 'max_billing_cycles',
    'cancellation_policy', 'minimum_commitment_cycles',
    'grace_period_days', 'reactivation_period_days',
    'upgrade_behavior', 'downgrade_behavior',
    'is_active', 'is_public',
    'provider_plan_mappings', 'metadata', 'sort_order',
]

PLAN_ADDON_FIELDS = [
    'name', 'description', 'translations',
    'billing_frequency', 'allow_quantity',
    'is_required', 'is_active', 'sort_order',
]

VOUCHER_RESTRICTION_FIELDS = [
    'restriction_type', 'restriction_value', 'is_inclusive',
]

LOYALTY_BADGE_FIELDS = [
    'name', 'slug', 'description', 'icon',
    'criteria_type', 'criteria_value',
    'points_reward', 'is_visible', 'display_order',
    'is_active', 'auto_award',
]

LOYALTY_CAMPAIGN_FIELDS = [
    'name', 'slug', 'description',
    'campaign_type', 'trigger_event', 'trigger_conditions',
    'actions', 'is_journey', 'journey_steps',
    'schedule_type', 'schedule_config',
    'target_all_members', 'max_triggers_per_member', 'cooldown_days',
    'is_ab_test', 'ab_variant', 'ab_split_percentage',
    'status', 'start_date', 'end_date', 'is_active',
]

LOYALTY_SEGMENT_FIELDS = [
    'name', 'slug', 'description',
    'criteria_type', 'criteria_config',
    'is_active',
]


def _serialize_money(data, instance, field_name):
    """Serialize a MoneyField as _amount + _currency keys."""
    val = getattr(instance, field_name, None)
    if val is not None:
        data[f'_{field_name}_amount'] = str(val.amount) if hasattr(val, 'amount') else str(val)
        data[f'_{field_name}_currency'] = str(val.currency) if hasattr(val, 'currency') else getattr(instance, f'{field_name}_currency', None)
    else:
        data[f'_{field_name}_amount'] = None
        data[f'_{field_name}_currency'] = None


def _deserialize_money(instance, item, field_name):
    """Deserialize MoneyField from _amount + _currency keys."""
    amount = item.get(f'_{field_name}_amount')
    currency = item.get(f'_{field_name}_currency')
    if amount is not None:
        setattr(instance, field_name, Decimal(str(amount)))
    else:
        setattr(instance, field_name, None)
    if currency:
        setattr(instance, f'{field_name}_currency', currency)


def _serialize_datetime(data, field_name):
    """Serialize a datetime field to ISO format."""
    val = data.get(field_name)
    if val and hasattr(val, 'isoformat'):
        data[field_name] = val.isoformat()


class CommerceRulesSerializer(CollectionSyncSerializer):
    """Serializer for commerce rules: vouchers, promotions, loyalty, and subscriptions.

    Models handled:
        - VoucherCode: Discount voucher codes and rules
        - VoucherRestriction: Advanced voucher restrictions (nested)
        - Promotion: Automatic promotion rules
        - LoyaltyTier: Loyalty program tier definitions
        - LoyaltyRule: Point earning rules
        - LoyaltyReward: Redeemable loyalty rewards
        - LoyaltyBadge: Achievement badge definitions
        - LoyaltyCampaign: Automated campaign configurations
        - LoyaltySegment: Customer segmentation definitions
        - SubscriptionPlan: Recurring subscription plan definitions
        - PlanAddon: Subscription plan add-on options
    """

    category_key = 'commerce_rules'
    natural_key_fields = ['code']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from vouchers.models import VoucherCode
        self.model_class = VoucherCode

    def get_count(self):
        from vouchers.models import VoucherCode, VoucherRestriction
        from catalog.models import Promotion
        from loyalty.models import (
            LoyaltyTier, LoyaltyRule, LoyaltyReward,
            LoyaltyBadge, LoyaltyCampaign, LoyaltySegment,
        )
        from subscriptions.models import SubscriptionPlan, PlanAddon
        return (VoucherCode.objects.count() +
                VoucherRestriction.objects.count() +
                Promotion.objects.count() +
                LoyaltyTier.objects.count() +
                LoyaltyRule.objects.count() +
                LoyaltyReward.objects.count() +
                LoyaltyBadge.objects.count() +
                LoyaltyCampaign.objects.count() +
                LoyaltySegment.objects.count() +
                SubscriptionPlan.objects.count() +
                PlanAddon.objects.count())

    def export(self, credential_mode='redact'):
        from vouchers.models import VoucherCode
        from catalog.models import Promotion
        from loyalty.models import (
            LoyaltyTier, LoyaltyRule, LoyaltyReward,
            LoyaltyBadge, LoyaltyCampaign, LoyaltySegment,
        )
        from subscriptions.models import SubscriptionPlan, PlanAddon

        items = []
        files = {}

        # Vouchers (with nested restrictions)
        for v in VoucherCode.objects.prefetch_related(
            'eligible_products', 'eligible_categories', 'restrictions',
        ).all():
            data = {f: getattr(v, f) for f in VOUCHER_FIELDS}
            data['_source_pk'] = v.pk
            data['_model'] = 'VoucherCode'

            # MoneyFields
            for mf in ['max_discount_amount', 'min_order_value', 'gift_card_balance', 'original_gift_card_value']:
                _serialize_money(data, v, mf)

            # Datetime fields
            for dt in ['start_date', 'end_date']:
                _serialize_datetime(data, dt)

            # M2M refs as portable identifiers
            data['_eligible_product_skus'] = list(v.eligible_products.values_list('sku', flat=True))
            data['_eligible_category_slugs'] = list(v.eligible_categories.values_list('slug', flat=True))

            # Nested restrictions
            data['_restrictions'] = []
            for r in v.restrictions.all():
                data['_restrictions'].append(
                    {f: getattr(r, f) for f in VOUCHER_RESTRICTION_FIELDS}
                )

            items.append(data)

        # Promotions
        for p in Promotion.objects.prefetch_related(
            'categories', 'brands', 'collections', 'products',
        ).all():
            data = {f: getattr(p, f) for f in PROMOTION_FIELDS}
            data['_source_pk'] = p.pk
            data['_model'] = 'Promotion'

            for dt in ['start_date', 'end_date']:
                _serialize_datetime(data, dt)

            data['_category_slugs'] = list(p.categories.values_list('slug', flat=True))
            data['_brand_slugs'] = list(p.brands.values_list('slug', flat=True))
            data['_collection_slugs'] = list(p.collections.values_list('slug', flat=True))
            data['_product_skus'] = list(p.products.values_list('sku', flat=True))

            items.append(data)

        # Loyalty tiers
        for tier in LoyaltyTier.objects.all():
            data = {f: getattr(tier, f) for f in LOYALTY_TIER_FIELDS}
            data['_source_pk'] = tier.pk
            data['_model'] = 'LoyaltyTier'

            # Decimal fields
            for df in ['min_spend', 'points_multiplier']:
                if data.get(df) is not None:
                    data[df] = str(data[df])

            items.append(data)

        # Loyalty rules
        for rule in LoyaltyRule.objects.prefetch_related('allowed_tiers').all():
            data = {f: getattr(rule, f) for f in LOYALTY_RULE_FIELDS}
            data['_source_pk'] = rule.pk
            data['_model'] = 'LoyaltyRule'

            for df in ['points_rate', 'min_order_amount']:
                if data.get(df) is not None:
                    data[df] = str(data[df])

            for dt in ['start_date', 'end_date']:
                _serialize_datetime(data, dt)

            data['_allowed_tier_slugs'] = list(rule.allowed_tiers.values_list('slug', flat=True))

            items.append(data)

        # Loyalty rewards
        for reward in LoyaltyReward.objects.select_related('product', 'required_tier').all():
            data = {f: getattr(reward, f) for f in LOYALTY_REWARD_FIELDS}
            data['_source_pk'] = reward.pk
            data['_model'] = 'LoyaltyReward'

            for df in ['discount_value', 'min_purchase_amount']:
                if data.get(df) is not None:
                    data[df] = str(data[df])

            for dt in ['start_date', 'end_date']:
                _serialize_datetime(data, dt)

            data['_product_sku'] = reward.product.sku if reward.product else None
            data['_required_tier_slug'] = reward.required_tier.slug if reward.required_tier else None

            file_data = export_file_field(reward, 'image')
            if file_data:
                key = f'LoyaltyReward:{reward.slug}:image'
                files[key] = file_data
                data['_image_key'] = key

            items.append(data)

        # Loyalty badges
        for badge in LoyaltyBadge.objects.select_related('image').all():
            data = {f: getattr(badge, f) for f in LOYALTY_BADGE_FIELDS}
            data['_source_pk'] = badge.pk
            data['_model'] = 'LoyaltyBadge'

            # MediaAsset FK for image (inline file export)
            if badge.image and badge.image.original_file:
                from ..file_handler import export_file_field as _eff
                file_data = _eff(badge.image, 'original_file')
                if file_data:
                    key = f'LoyaltyBadge:{badge.slug}:image'
                    files[key] = file_data
                    data['_image_file_key'] = key
                    data['_image_meta'] = {
                        'title': badge.image.title,
                        'alt_text': badge.image.alt_text,
                        'description': getattr(badge.image, 'description', ''),
                    }

            items.append(data)

        # Loyalty segments (before campaigns since campaigns FK to segment)
        for seg in LoyaltySegment.objects.all():
            data = {f: getattr(seg, f) for f in LOYALTY_SEGMENT_FIELDS}
            data['_source_pk'] = seg.pk
            data['_model'] = 'LoyaltySegment'
            items.append(data)

        # Loyalty campaigns
        for camp in LoyaltyCampaign.objects.prefetch_related('target_tiers').select_related('target_segment').all():
            data = {f: getattr(camp, f) for f in LOYALTY_CAMPAIGN_FIELDS}
            data['_source_pk'] = camp.pk
            data['_model'] = 'LoyaltyCampaign'

            for dt in ['start_date', 'end_date']:
                _serialize_datetime(data, dt)

            data['_target_tier_slugs'] = list(camp.target_tiers.values_list('slug', flat=True))
            data['_target_segment_slug'] = camp.target_segment.slug if camp.target_segment else None

            items.append(data)

        # Subscription plans
        for plan in SubscriptionPlan.objects.all():
            data = {f: getattr(plan, f) for f in SUBSCRIPTION_PLAN_FIELDS}
            data['_source_pk'] = plan.pk
            data['_model'] = 'SubscriptionPlan'

            for mf in ['setup_fee', 'trial_price']:
                _serialize_money(data, plan, mf)

            items.append(data)

        # Plan addons
        for addon in PlanAddon.objects.select_related('plan').all():
            data = {f: getattr(addon, f) for f in PLAN_ADDON_FIELDS}
            data['_source_pk'] = str(addon.addon_id)
            data['_model'] = 'PlanAddon'
            data['_plan_slug'] = addon.plan.slug

            _serialize_money(data, addon, 'price')

            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
            'files': files,
        }

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        files = data.get('files', {})
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        # Import order: dependencies first
        order_map = {
            'LoyaltyTier': 0, 'LoyaltySegment': 1,
            'SubscriptionPlan': 2,
            'VoucherCode': 3, 'Promotion': 4,
            'LoyaltyRule': 5, 'LoyaltyReward': 6,
            'LoyaltyBadge': 7, 'LoyaltyCampaign': 8,
            'PlanAddon': 9,
        }
        ordered = sorted(items, key=lambda x: order_map.get(x.get('_model', ''), 99))

        for item in ordered:
            model_type = item.get('_model')
            try:
                with transaction.atomic():
                    if model_type == 'VoucherCode':
                        self._import_voucher(item)
                    elif model_type == 'Promotion':
                        self._import_promotion(item)
                    elif model_type == 'LoyaltyTier':
                        self._import_loyalty_tier(item)
                    elif model_type == 'LoyaltyRule':
                        self._import_loyalty_rule(item)
                    elif model_type == 'LoyaltyReward':
                        self._import_loyalty_reward(item, files)
                    elif model_type == 'LoyaltyBadge':
                        self._import_loyalty_badge(item, files)
                    elif model_type == 'LoyaltyCampaign':
                        self._import_loyalty_campaign(item)
                    elif model_type == 'LoyaltySegment':
                        self._import_loyalty_segment(item)
                    elif model_type == 'SubscriptionPlan':
                        self._import_subscription_plan(item)
                    elif model_type == 'PlanAddon':
                        self._import_plan_addon(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('name') or item.get('code', 'Unknown')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_voucher(self, item):
        from vouchers.models import VoucherCode, VoucherRestriction

        existing = VoucherCode.objects.filter(code=item['code']).first()
        v = existing or VoucherCode()

        for f in VOUCHER_FIELDS:
            if f in item:
                setattr(v, f, item[f])

        for mf in ['max_discount_amount', 'min_order_value', 'gift_card_balance', 'original_gift_card_value']:
            _deserialize_money(v, item, mf)

        v.save()

        # M2M
        product_skus = item.get('_eligible_product_skus', [])
        if product_skus:
            from catalog.models import Product
            v.eligible_products.set(Product.objects.filter(sku__in=product_skus))
        else:
            v.eligible_products.clear()

        category_slugs = item.get('_eligible_category_slugs', [])
        if category_slugs:
            from catalog.models import Category
            v.eligible_categories.set(Category.objects.filter(slug__in=category_slugs))
        else:
            v.eligible_categories.clear()

        # Nested restrictions (replace all)
        if existing:
            VoucherRestriction.objects.filter(voucher=v).delete()
        for r_data in item.get('_restrictions', []):
            r = VoucherRestriction(voucher=v)
            for f in VOUCHER_RESTRICTION_FIELDS:
                if f in r_data:
                    setattr(r, f, r_data[f])
            r.save()

    def _import_promotion(self, item):
        from catalog.models import Promotion

        # Promotion has no unique field - match by name + discount_type
        existing = Promotion.objects.filter(
            name=item['name'], discount_type=item['discount_type'],
        ).first()
        p = existing or Promotion()

        for f in PROMOTION_FIELDS:
            if f in item:
                setattr(p, f, item[f])

        p.save()

        # M2M
        for m2m_field, slug_key, model_path in [
            ('categories', '_category_slugs', 'catalog.Category'),
            ('brands', '_brand_slugs', 'catalog.Brand'),
            ('products', '_product_skus', 'catalog.Product'),
        ]:
            slugs = item.get(slug_key, [])
            if slugs:
                from django.apps import apps
                app, model_name = model_path.split('.')
                Model = apps.get_model(app, model_name)
                lookup_field = 'sku' if 'sku' in slug_key else 'slug'
                getattr(p, m2m_field).set(Model.objects.filter(**{f'{lookup_field}__in': slugs}))
            else:
                getattr(p, m2m_field).clear()

        # Collections
        collection_slugs = item.get('_collection_slugs', [])
        if collection_slugs:
            from catalog.models import Collection
            p.collections.set(Collection.objects.filter(slug__in=collection_slugs))
        else:
            p.collections.clear()

    def _import_loyalty_tier(self, item):
        from loyalty.models import LoyaltyTier

        existing = LoyaltyTier.objects.filter(slug=item['slug']).first()
        tier = existing or LoyaltyTier()

        for f in LOYALTY_TIER_FIELDS:
            if f in item:
                val = item[f]
                if f in ('min_spend', 'points_multiplier') and val is not None:
                    val = Decimal(str(val))
                setattr(tier, f, val)

        tier.save()

    def _import_loyalty_rule(self, item):
        from loyalty.models import LoyaltyRule, LoyaltyTier

        # Match by name + rule_type (uuid is not portable)
        existing = LoyaltyRule.objects.filter(
            name=item['name'], rule_type=item['rule_type'],
        ).first()
        rule = existing or LoyaltyRule()

        for f in LOYALTY_RULE_FIELDS:
            if f in item:
                val = item[f]
                if f in ('points_rate', 'min_order_amount') and val is not None:
                    val = Decimal(str(val))
                setattr(rule, f, val)

        rule.save()

        tier_slugs = item.get('_allowed_tier_slugs', [])
        if tier_slugs:
            rule.allowed_tiers.set(LoyaltyTier.objects.filter(slug__in=tier_slugs))
        else:
            rule.allowed_tiers.clear()

    def _import_loyalty_reward(self, item, files):
        from loyalty.models import LoyaltyReward, LoyaltyTier

        existing = LoyaltyReward.objects.filter(slug=item['slug']).first()
        reward = existing or LoyaltyReward()

        for f in LOYALTY_REWARD_FIELDS:
            if f in item:
                val = item[f]
                if f in ('discount_value', 'min_purchase_amount') and val is not None:
                    val = Decimal(str(val))
                setattr(reward, f, val)

        # FK refs
        product_sku = item.get('_product_sku')
        if product_sku:
            from catalog.models import Product
            reward.product = Product.objects.filter(sku=product_sku).first()
        else:
            reward.product = None

        tier_slug = item.get('_required_tier_slug')
        if tier_slug:
            reward.required_tier = LoyaltyTier.objects.filter(slug=tier_slug).first()
        else:
            reward.required_tier = None

        # Image file
        file_key = item.get('_image_key')
        if file_key and file_key in files:
            import_file_field(reward, 'image', files[file_key])

        reward.save()

    def _import_loyalty_badge(self, item, files):
        from loyalty.models import LoyaltyBadge

        existing = LoyaltyBadge.objects.filter(slug=item['slug']).first()
        badge = existing or LoyaltyBadge()

        for f in LOYALTY_BADGE_FIELDS:
            if f in item:
                setattr(badge, f, item[f])

        # MediaAsset FK for badge image
        file_key = item.get('_image_file_key')
        if file_key and file_key in files:
            from media_library.models import MediaAsset
            meta = item.get('_image_meta', {})
            asset = MediaAsset(
                title=meta.get('title', f'Badge: {badge.name}'),
                alt_text=meta.get('alt_text', ''),
                description=meta.get('description', ''),
            )
            from ..file_handler import import_file_field as _iff
            _iff(asset, 'original_file', files[file_key])
            asset.save()
            badge.image = asset

        badge.save()

    def _import_loyalty_segment(self, item):
        from loyalty.models import LoyaltySegment

        existing = LoyaltySegment.objects.filter(slug=item['slug']).first()
        seg = existing or LoyaltySegment()

        for f in LOYALTY_SEGMENT_FIELDS:
            if f in item:
                setattr(seg, f, item[f])

        seg.save()

    def _import_loyalty_campaign(self, item):
        from loyalty.models import LoyaltyCampaign, LoyaltyTier, LoyaltySegment

        existing = LoyaltyCampaign.objects.filter(slug=item['slug']).first()
        camp = existing or LoyaltyCampaign()

        for f in LOYALTY_CAMPAIGN_FIELDS:
            if f in item:
                setattr(camp, f, item[f])

        # FK to segment
        seg_slug = item.get('_target_segment_slug')
        if seg_slug:
            camp.target_segment = LoyaltySegment.objects.filter(slug=seg_slug).first()
        else:
            camp.target_segment = None

        camp.save()

        # M2M target tiers
        tier_slugs = item.get('_target_tier_slugs', [])
        if tier_slugs:
            camp.target_tiers.set(LoyaltyTier.objects.filter(slug__in=tier_slugs))
        else:
            camp.target_tiers.clear()

    def _import_subscription_plan(self, item):
        from subscriptions.models import SubscriptionPlan

        existing = SubscriptionPlan.objects.filter(slug=item['slug']).first()
        plan = existing or SubscriptionPlan()

        for f in SUBSCRIPTION_PLAN_FIELDS:
            if f in item:
                setattr(plan, f, item[f])

        for mf in ['setup_fee', 'trial_price']:
            _deserialize_money(plan, item, mf)

        plan.save()

    def _import_plan_addon(self, item):
        from subscriptions.models import SubscriptionPlan, PlanAddon

        plan_slug = item.get('_plan_slug')
        plan = SubscriptionPlan.objects.filter(slug=plan_slug).first()
        if not plan:
            raise ValueError(f"SubscriptionPlan not found: {plan_slug}")

        existing = PlanAddon.objects.filter(plan=plan, name=item['name']).first()
        addon = existing or PlanAddon(plan=plan)

        for f in PLAN_ADDON_FIELDS:
            if f in item:
                setattr(addon, f, item[f])

        _deserialize_money(addon, item, 'price')

        addon.save()

    def _delete_absent(self, remote_items):
        from vouchers.models import VoucherCode
        from catalog.models import Promotion
        from loyalty.models import (
            LoyaltyTier, LoyaltyRule, LoyaltyReward,
            LoyaltyBadge, LoyaltyCampaign, LoyaltySegment,
        )
        from subscriptions.models import SubscriptionPlan, PlanAddon

        remote_voucher_codes = set()
        remote_promo_keys = set()
        remote_tier_slugs = set()
        remote_rule_keys = set()
        remote_reward_slugs = set()
        remote_badge_slugs = set()
        remote_campaign_slugs = set()
        remote_segment_slugs = set()
        remote_plan_slugs = set()
        remote_addon_keys = set()

        for item in remote_items:
            m = item.get('_model')
            if m == 'VoucherCode':
                remote_voucher_codes.add(item.get('code'))
            elif m == 'Promotion':
                remote_promo_keys.add((item.get('name'), item.get('discount_type')))
            elif m == 'LoyaltyTier':
                remote_tier_slugs.add(item.get('slug'))
            elif m == 'LoyaltyRule':
                remote_rule_keys.add((item.get('name'), item.get('rule_type')))
            elif m == 'LoyaltyReward':
                remote_reward_slugs.add(item.get('slug'))
            elif m == 'LoyaltyBadge':
                remote_badge_slugs.add(item.get('slug'))
            elif m == 'LoyaltyCampaign':
                remote_campaign_slugs.add(item.get('slug'))
            elif m == 'LoyaltySegment':
                remote_segment_slugs.add(item.get('slug'))
            elif m == 'SubscriptionPlan':
                remote_plan_slugs.add(item.get('slug'))
            elif m == 'PlanAddon':
                remote_addon_keys.add((item.get('_plan_slug'), item.get('name')))

        deleted = 0

        # Delete in reverse dependency order
        for addon in PlanAddon.objects.select_related('plan').all():
            if (addon.plan.slug, addon.name) not in remote_addon_keys:
                addon.delete()
                deleted += 1

        # Campaigns before segments (FK to segment)
        for camp in LoyaltyCampaign.objects.all():
            if camp.slug not in remote_campaign_slugs:
                camp.delete()
                deleted += 1

        for reward in LoyaltyReward.objects.all():
            if reward.slug not in remote_reward_slugs:
                reward.delete()
                deleted += 1

        for badge in LoyaltyBadge.objects.all():
            if badge.slug not in remote_badge_slugs:
                badge.delete()
                deleted += 1

        for rule in LoyaltyRule.objects.all():
            if (rule.name, rule.rule_type) not in remote_rule_keys:
                rule.delete()
                deleted += 1

        # VoucherCode CASCADE deletes restrictions
        for v in VoucherCode.objects.all():
            if v.code not in remote_voucher_codes:
                v.delete()
                deleted += 1

        for p in Promotion.objects.all():
            if (p.name, p.discount_type) not in remote_promo_keys:
                p.delete()
                deleted += 1

        for seg in LoyaltySegment.objects.all():
            if seg.slug not in remote_segment_slugs:
                try:
                    seg.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete loyalty segment {seg.slug}: {e}")

        for plan in SubscriptionPlan.objects.all():
            if plan.slug not in remote_plan_slugs:
                try:
                    plan.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete subscription plan {plan.slug}: {e}")

        for tier in LoyaltyTier.objects.all():
            if tier.slug not in remote_tier_slugs:
                try:
                    tier.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete loyalty tier {tier.slug}: {e}")

        return deleted

    def generate_diff(self, remote_data):
        from vouchers.models import VoucherCode
        from catalog.models import Promotion
        from loyalty.models import (
            LoyaltyTier, LoyaltyRule, LoyaltyReward,
            LoyaltyBadge, LoyaltyCampaign, LoyaltySegment,
        )
        from subscriptions.models import SubscriptionPlan, PlanAddon

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            name = item.get('name') or item.get('code', 'Unknown')

            if model_type == 'VoucherCode':
                existing = VoucherCode.objects.filter(code=item.get('code')).first()
                fields = VOUCHER_FIELDS
            elif model_type == 'Promotion':
                existing = Promotion.objects.filter(
                    name=item.get('name'), discount_type=item.get('discount_type'),
                ).first()
                fields = PROMOTION_FIELDS
            elif model_type == 'LoyaltyTier':
                existing = LoyaltyTier.objects.filter(slug=item.get('slug')).first()
                fields = LOYALTY_TIER_FIELDS
            elif model_type == 'LoyaltyRule':
                existing = LoyaltyRule.objects.filter(
                    name=item.get('name'), rule_type=item.get('rule_type'),
                ).first()
                fields = LOYALTY_RULE_FIELDS
            elif model_type == 'LoyaltyReward':
                existing = LoyaltyReward.objects.filter(slug=item.get('slug')).first()
                fields = LOYALTY_REWARD_FIELDS
            elif model_type == 'LoyaltyBadge':
                existing = LoyaltyBadge.objects.filter(slug=item.get('slug')).first()
                fields = LOYALTY_BADGE_FIELDS
            elif model_type == 'LoyaltyCampaign':
                existing = LoyaltyCampaign.objects.filter(slug=item.get('slug')).first()
                fields = LOYALTY_CAMPAIGN_FIELDS
            elif model_type == 'LoyaltySegment':
                existing = LoyaltySegment.objects.filter(slug=item.get('slug')).first()
                fields = LOYALTY_SEGMENT_FIELDS
            elif model_type == 'SubscriptionPlan':
                existing = SubscriptionPlan.objects.filter(slug=item.get('slug')).first()
                fields = SUBSCRIPTION_PLAN_FIELDS
            elif model_type == 'PlanAddon':
                plan = SubscriptionPlan.objects.filter(slug=item.get('_plan_slug')).first()
                existing = PlanAddon.objects.filter(plan=plan, name=item.get('name')).first() if plan else None
                fields = PLAN_ADDON_FIELDS
            else:
                continue

            if existing:
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
