"""
Shipping Configuration Sync Serializer

Handles export/import of shipping-related models:
- ProviderAccount (credentials via credential_handler)
- ShippingZone
- ShippingMethod (from cart app, with MoneyFields and M2M)
- ShippingPromotion (MoneyFields, M2M to zones/methods/products/categories)
- ShippingRateTable (with nested ShippingRateTier children)
- ShippingPackage (MoneyField)
- CarrierPreset (FileField for logo)
- Location (M2M to zones)
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer
from ..credential_handler import (
    decrypt_credentials_for_export, encrypt_credentials_for_import,
    redact_credentials,
)
from ..file_handler import export_file_field, import_file_field

logger = logging.getLogger(__name__)

PROVIDER_ACCOUNT_FIELDS = [
    'display_name', 'settings', 'signup_url',
    'is_active', 'is_default', 'connection_status', 'connection_error',
]

SHIPPING_ZONE_FIELDS = [
    'name', 'description', 'countries', 'states',
    'postal_code_patterns', 'priority', 'is_active',
]

SHIPPING_METHOD_FIELDS = [
    'name', 'description', 'method_type',
    'min_weight', 'max_weight',
    'min_delivery_days', 'max_delivery_days',
    'icon', 'sort_order', 'is_active',
    'carrier', 'carrier_service_code',
    'template_variant', 'css_classes', 'layout_config',
    'style_overrides', 'responsive_config', 'inherit_parent_theme',
]

SHIPPING_PROMOTION_FIELDS = [
    'name', 'description', 'promotion_type',
    'min_cart_weight', 'max_cart_weight',
    'min_item_count', 'max_item_count',
    'first_time_customers_only',
    'start_date', 'end_date',
    'priority', 'stop_further_promotions', 'is_active',
]

RATE_TABLE_FIELDS = [
    'name', 'description', 'basis_type', 'is_active',
]

RATE_TIER_FIELDS = [
    'min_value', 'max_value', 'is_active',
]

SHIPPING_PACKAGE_FIELDS = [
    'name', 'description',
    'length', 'width', 'height', 'wall_thickness',
    'max_weight', 'tare_weight',
    'priority', 'is_active',
]

CARRIER_PRESET_FIELDS = [
    'name', 'slug', 'tracking_url_template',
    'country_of_operation', 'description',
    'is_default', 'is_active', 'is_system',
    'tracking_url_template_override',
]

LOCATION_FIELDS = [
    'name', 'code', 'location_type',
    'address1', 'address2', 'city', 'state', 'postal_code', 'country',
    'latitude', 'longitude', 'phone', 'email',
    'operating_hours', 'pickup_instructions', 'delivery_notes',
    'is_active', 'accepts_pickup', 'accepts_delivery_dispatch',
    'max_daily_pickups', 'pickup_preparation_time', 'delivery_radius',
]


def _serialize_money(data, instance, field_name):
    val = getattr(instance, field_name, None)
    if val is not None:
        data[f'_{field_name}_amount'] = str(val.amount) if hasattr(val, 'amount') else str(val)
        data[f'_{field_name}_currency'] = str(val.currency) if hasattr(val, 'currency') else getattr(instance, f'{field_name}_currency', None)
    else:
        data[f'_{field_name}_amount'] = None
        data[f'_{field_name}_currency'] = None


def _deserialize_money(instance, item, field_name):
    amount = item.get(f'_{field_name}_amount')
    currency = item.get(f'_{field_name}_currency')
    if amount is not None:
        setattr(instance, field_name, Decimal(str(amount)))
    else:
        setattr(instance, field_name, None)
    if currency:
        setattr(instance, f'{field_name}_currency', currency)


def _serialize_datetime(data, field_name):
    val = data.get(field_name)
    if val and hasattr(val, 'isoformat'):
        data[field_name] = val.isoformat()


def _serialize_decimal(data, field_name):
    val = data.get(field_name)
    if val is not None:
        data[field_name] = str(val)


class ShippingConfigSerializer(CollectionSyncSerializer):
    """Serializer for shipping configuration and provider accounts.

    Models handled:
        - ProviderAccount: Shipping provider connection settings
        - ShippingZone: Geographic shipping zones
        - ShippingMethod: Shipping methods with pricing (from cart app)
        - ShippingPromotion: Promotions for shipping calculation
        - ShippingRateTable: Rate tables with nested tiers
        - ShippingPackage: Package dimensions and weight
        - CarrierPreset: Carrier service presets
        - Location: Warehouse/fulfillment locations
    """

    category_key = 'shipping_config'
    natural_key_fields = ['name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from shipping.models import ShippingZone
        self.model_class = ShippingZone

    def get_count(self):
        from shipping.models import (
            ProviderAccount, ShippingZone, ShippingPromotion,
            ShippingRateTable, ShippingPackage, CarrierPreset, Location,
        )
        from cart.models import ShippingMethod
        return (ProviderAccount.objects.count() +
                ShippingZone.objects.count() +
                ShippingMethod.objects.count() +
                ShippingPromotion.objects.count() +
                ShippingRateTable.objects.count() +
                ShippingPackage.objects.count() +
                CarrierPreset.objects.count() +
                Location.objects.count())

    def export(self, credential_mode='redact'):
        from shipping.models import (
            ProviderAccount, ShippingZone, ShippingPromotion,
            ShippingRateTable, ShippingRateTier, ShippingPackage,
            CarrierPreset, Location,
        )
        from cart.models import ShippingMethod

        items = []
        files = {}

        # Provider accounts
        for account in ProviderAccount.objects.select_related('component').all():
            data = {f: getattr(account, f) for f in PROVIDER_ACCOUNT_FIELDS}
            data['_source_pk'] = str(account.pk)
            data['_model'] = 'ProviderAccount'
            data['_component_slug'] = account.component.slug if account.component else None

            if credential_mode == 'decrypt':
                creds = decrypt_credentials_for_export(
                    'shipping_config', 'ProviderAccount', account
                )
                if creds:
                    data['_credentials'] = creds
            elif credential_mode == 'redact':
                creds = decrypt_credentials_for_export(
                    'shipping_config', 'ProviderAccount', account
                )
                if creds:
                    data['_credentials_redacted'] = redact_credentials(creds)

            items.append(data)

        # Carrier presets
        for preset in CarrierPreset.objects.all():
            data = {f: getattr(preset, f) for f in CARRIER_PRESET_FIELDS}
            data['_source_pk'] = str(preset.pk)
            data['_model'] = 'CarrierPreset'
            # country_of_operation may be a Country object
            if data.get('country_of_operation'):
                data['country_of_operation'] = str(data['country_of_operation'])

            file_data = export_file_field(preset, 'logo')
            if file_data:
                key = f'CarrierPreset:{preset.slug}:logo'
                files[key] = file_data
                data['_logo_key'] = key

            items.append(data)

        # Shipping zones
        for zone in ShippingZone.objects.all():
            data = {f: getattr(zone, f) for f in SHIPPING_ZONE_FIELDS}
            data['_source_pk'] = str(zone.pk)
            data['_model'] = 'ShippingZone'
            items.append(data)

        # Shipping packages
        for pkg in ShippingPackage.objects.all():
            data = {f: getattr(pkg, f) for f in SHIPPING_PACKAGE_FIELDS}
            data['_source_pk'] = str(pkg.pk)
            data['_model'] = 'ShippingPackage'
            for df in ['length', 'width', 'height', 'wall_thickness', 'max_weight', 'tare_weight']:
                _serialize_decimal(data, df)
            _serialize_money(data, pkg, 'cost')
            items.append(data)

        # Shipping methods
        for method in ShippingMethod.objects.prefetch_related('zones', 'pickup_locations').all():
            data = {f: getattr(method, f) for f in SHIPPING_METHOD_FIELDS}
            data['_source_pk'] = method.pk
            data['_model'] = 'ShippingMethod'

            for mf in ['flat_rate_cost', 'min_order_value', 'max_order_value']:
                _serialize_money(data, method, mf)

            for df in ['min_weight', 'max_weight']:
                _serialize_decimal(data, df)

            data['_zone_names'] = list(method.zones.values_list('name', flat=True))
            data['_pickup_location_codes'] = list(method.pickup_locations.values_list('code', flat=True))

            items.append(data)

        # Shipping promotions
        for rule in ShippingPromotion.objects.prefetch_related(
            'zones', 'shipping_methods', 'requires_products',
            'requires_categories', 'excludes_products',
            'excludes_categories', 'customer_groups',
        ).all():
            data = {f: getattr(rule, f) for f in SHIPPING_PROMOTION_FIELDS}
            data['_source_pk'] = str(rule.pk)
            data['_model'] = 'ShippingPromotion'

            for mf in ['promotion_value', 'min_cart_value', 'max_cart_value']:
                _serialize_money(data, rule, mf)

            for df in ['min_cart_weight', 'max_cart_weight']:
                _serialize_decimal(data, df)

            for dt in ['start_date', 'end_date']:
                _serialize_datetime(data, dt)

            data['_zone_names'] = list(rule.zones.values_list('name', flat=True))
            data['_method_names'] = list(rule.shipping_methods.values_list('name', flat=True))
            data['_requires_product_skus'] = list(rule.requires_products.values_list('sku', flat=True))
            data['_requires_category_slugs'] = list(rule.requires_categories.values_list('slug', flat=True))
            data['_excludes_product_skus'] = list(rule.excludes_products.values_list('sku', flat=True))
            data['_excludes_category_slugs'] = list(rule.excludes_categories.values_list('slug', flat=True))
            data['_customer_group_names'] = list(rule.customer_groups.values_list('name', flat=True))

            items.append(data)

        # Rate tables with tiers
        for table in ShippingRateTable.objects.select_related('shipping_method').prefetch_related('zones', 'tiers').all():
            data = {f: getattr(table, f) for f in RATE_TABLE_FIELDS}
            data['_source_pk'] = str(table.pk)
            data['_model'] = 'ShippingRateTable'
            data['_method_name'] = table.shipping_method.name if table.shipping_method else None
            data['_zone_names'] = list(table.zones.values_list('name', flat=True))

            # Nested tiers
            data['_tiers'] = []
            for tier in table.tiers.all().order_by('min_value'):
                td = {f: getattr(tier, f) for f in RATE_TIER_FIELDS}
                for df in ['min_value', 'max_value']:
                    if td.get(df) is not None:
                        td[df] = str(td[df])
                _serialize_money(td, tier, 'rate')
                data['_tiers'].append(td)

            items.append(data)

        # Locations
        for loc in Location.objects.prefetch_related('zones').all():
            data = {f: getattr(loc, f) for f in LOCATION_FIELDS}
            data['_source_pk'] = str(loc.pk)
            data['_model'] = 'Location'
            for df in ['latitude', 'longitude', 'delivery_radius']:
                _serialize_decimal(data, df)
            data['_zone_names'] = list(loc.zones.values_list('name', flat=True))
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

        # Import order: ProviderAccount -> CarrierPreset -> Zone -> Package ->
        #               Method -> Rule -> RateTable -> Location
        order_map = {
            'ProviderAccount': 0, 'CarrierPreset': 1,
            'ShippingZone': 2, 'ShippingPackage': 3,
            'ShippingMethod': 4, 'ShippingPromotion': 5,
            'ShippingRateTable': 6, 'Location': 7,
        }
        ordered = sorted(items, key=lambda x: order_map.get(x.get('_model', ''), 99))

        for item in ordered:
            model_type = item.get('_model')
            try:
                with transaction.atomic():
                    if model_type == 'ProviderAccount':
                        self._import_provider_account(item)
                    elif model_type == 'CarrierPreset':
                        self._import_carrier_preset(item, files)
                    elif model_type == 'ShippingZone':
                        self._import_zone(item)
                    elif model_type == 'ShippingPackage':
                        self._import_package(item)
                    elif model_type == 'ShippingMethod':
                        self._import_method(item)
                    elif model_type == 'ShippingPromotion':
                        self._import_promotion(item)
                    elif model_type == 'ShippingRateTable':
                        self._import_rate_table(item)
                    elif model_type == 'Location':
                        self._import_location(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('name') or item.get('slug', 'Unknown')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_provider_account(self, item):
        from shipping.models import ProviderAccount
        from django.contrib.auth import get_user_model
        User = get_user_model()

        component_slug = item.get('_component_slug')
        component = None
        if component_slug:
            try:
                from component_updates.models import ComponentRegistry
                component = ComponentRegistry.objects.get(slug=component_slug)
            except Exception:
                logger.warning(f"Shipping component not found: {component_slug}")

        lookup = {'display_name': item.get('display_name', '')}
        if component:
            lookup['component'] = component

        existing = ProviderAccount.objects.filter(**lookup).first()

        if existing:
            account = existing
            for f in PROVIDER_ACCOUNT_FIELDS:
                if f in item:
                    setattr(account, f, item[f])
        else:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise ValueError("No admin user for shipping provider account")
            account = ProviderAccount(user=admin_user)
            if component:
                account.component = component
            for f in PROVIDER_ACCOUNT_FIELDS:
                if f in item:
                    setattr(account, f, item[f])

        if '_credentials' in item and item['_credentials']:
            encrypted = encrypt_credentials_for_import(
                'shipping_config', 'ProviderAccount', item['_credentials']
            )
            if encrypted:
                account.credentials_encrypted = encrypted

        account.save()

    def _import_carrier_preset(self, item, files):
        from shipping.models import CarrierPreset

        existing = CarrierPreset.objects.filter(slug=item['slug']).first()
        preset = existing or CarrierPreset()

        for f in CARRIER_PRESET_FIELDS:
            if f in item:
                setattr(preset, f, item[f])

        file_key = item.get('_logo_key')
        if file_key and file_key in files:
            import_file_field(preset, 'logo', files[file_key])

        preset.save()

    def _import_zone(self, item):
        from shipping.models import ShippingZone

        # Zones have no unique field - match by name
        existing = ShippingZone.objects.filter(name=item['name']).first()
        zone = existing or ShippingZone()

        for f in SHIPPING_ZONE_FIELDS:
            if f in item:
                setattr(zone, f, item[f])

        zone.save()

    def _import_package(self, item):
        from shipping.models import ShippingPackage

        existing = ShippingPackage.objects.filter(name=item['name']).first()
        pkg = existing or ShippingPackage()

        for f in SHIPPING_PACKAGE_FIELDS:
            if f in item:
                val = item[f]
                if f in ('length', 'width', 'height', 'wall_thickness', 'max_weight', 'tare_weight') and val is not None:
                    val = Decimal(str(val))
                setattr(pkg, f, val)

        _deserialize_money(pkg, item, 'cost')

        pkg.save()

    def _import_method(self, item):
        from cart.models import ShippingMethod
        from shipping.models import ShippingZone, Location

        existing = ShippingMethod.objects.filter(name=item['name']).first()
        method = existing or ShippingMethod()

        for f in SHIPPING_METHOD_FIELDS:
            if f in item:
                val = item[f]
                if f in ('min_weight', 'max_weight') and val is not None:
                    val = Decimal(str(val))
                setattr(method, f, val)

        for mf in ['flat_rate_cost', 'min_order_value', 'max_order_value']:
            _deserialize_money(method, item, mf)

        method.save()

        # M2M zones
        zone_names = item.get('_zone_names', [])
        if zone_names:
            method.zones.set(ShippingZone.objects.filter(name__in=zone_names))
        else:
            method.zones.clear()

        # M2M pickup locations
        loc_codes = item.get('_pickup_location_codes', [])
        if loc_codes:
            method.pickup_locations.set(Location.objects.filter(code__in=loc_codes))
        else:
            method.pickup_locations.clear()

    def _import_promotion(self, item):
        from shipping.models import ShippingPromotion, ShippingZone
        from cart.models import ShippingMethod
        from django.contrib.auth.models import Group

        existing = ShippingPromotion.objects.filter(name=item['name']).first()
        rule = existing or ShippingPromotion()

        for f in SHIPPING_PROMOTION_FIELDS:
            if f in item:
                val = item[f]
                if f in ('min_cart_weight', 'max_cart_weight') and val is not None:
                    val = Decimal(str(val))
                setattr(rule, f, val)

        for mf in ['promotion_value', 'min_cart_value', 'max_cart_value']:
            _deserialize_money(rule, item, mf)

        rule.save()

        # M2M relationships
        zone_names = item.get('_zone_names', [])
        if zone_names:
            rule.zones.set(ShippingZone.objects.filter(name__in=zone_names))
        else:
            rule.zones.clear()

        method_names = item.get('_method_names', [])
        if method_names:
            rule.shipping_methods.set(ShippingMethod.objects.filter(name__in=method_names))
        else:
            rule.shipping_methods.clear()

        # Product/category M2M
        for m2m_field, key, model_import, lookup in [
            ('requires_products', '_requires_product_skus', 'catalog.Product', 'sku'),
            ('requires_categories', '_requires_category_slugs', 'catalog.Category', 'slug'),
            ('excludes_products', '_excludes_product_skus', 'catalog.Product', 'sku'),
            ('excludes_categories', '_excludes_category_slugs', 'catalog.Category', 'slug'),
        ]:
            values = item.get(key, [])
            if values:
                from django.apps import apps
                app, model_name = model_import.split('.')
                Model = apps.get_model(app, model_name)
                getattr(rule, m2m_field).set(Model.objects.filter(**{f'{lookup}__in': values}))
            else:
                getattr(rule, m2m_field).clear()

        group_names = item.get('_customer_group_names', [])
        if group_names:
            rule.customer_groups.set(Group.objects.filter(name__in=group_names))
        else:
            rule.customer_groups.clear()

    def _import_rate_table(self, item):
        from shipping.models import ShippingRateTable, ShippingRateTier, ShippingZone
        from cart.models import ShippingMethod

        existing = ShippingRateTable.objects.filter(name=item['name']).first()
        table = existing or ShippingRateTable()

        for f in RATE_TABLE_FIELDS:
            if f in item:
                setattr(table, f, item[f])

        # FK to ShippingMethod
        method_name = item.get('_method_name')
        if method_name:
            table.shipping_method = ShippingMethod.objects.filter(name=method_name).first()
        else:
            table.shipping_method = None

        table.save()

        # M2M zones
        zone_names = item.get('_zone_names', [])
        if zone_names:
            table.zones.set(ShippingZone.objects.filter(name__in=zone_names))
        else:
            table.zones.clear()

        # Replace tiers
        table.tiers.all().delete()
        for td in item.get('_tiers', []):
            tier = ShippingRateTier(rate_table=table)
            for f in RATE_TIER_FIELDS:
                if f in td:
                    val = td[f]
                    if f in ('min_value', 'max_value') and val is not None:
                        val = Decimal(str(val))
                    setattr(tier, f, val)
            _deserialize_money(tier, td, 'rate')
            tier.save()

    def _import_location(self, item):
        from shipping.models import Location, ShippingZone

        existing = Location.objects.filter(code=item['code']).first()
        loc = existing or Location()

        for f in LOCATION_FIELDS:
            if f in item:
                val = item[f]
                if f in ('latitude', 'longitude', 'delivery_radius') and val is not None:
                    val = Decimal(str(val))
                setattr(loc, f, val)

        loc.save()

        zone_names = item.get('_zone_names', [])
        if zone_names:
            loc.zones.set(ShippingZone.objects.filter(name__in=zone_names))
        else:
            loc.zones.clear()

    def _delete_absent(self, remote_items):
        from shipping.models import (
            ProviderAccount, ShippingZone, ShippingPromotion,
            ShippingRateTable, ShippingPackage, CarrierPreset, Location,
        )
        from cart.models import ShippingMethod

        remote = {
            'ProviderAccount': set(), 'CarrierPreset': set(),
            'ShippingZone': set(), 'ShippingPackage': set(),
            'ShippingMethod': set(), 'ShippingPromotion': set(),
            'ShippingRateTable': set(), 'Location': set(),
        }

        for item in remote_items:
            m = item.get('_model')
            if m == 'ProviderAccount':
                remote[m].add(item.get('display_name', ''))
            elif m == 'CarrierPreset':
                remote[m].add(item.get('slug'))
            elif m == 'ShippingZone':
                remote[m].add(item.get('name'))
            elif m == 'ShippingPackage':
                remote[m].add(item.get('name'))
            elif m == 'ShippingMethod':
                remote[m].add(item.get('name'))
            elif m == 'ShippingPromotion':
                remote[m].add(item.get('name'))
            elif m == 'ShippingRateTable':
                remote[m].add(item.get('name'))
            elif m == 'Location':
                remote[m].add(item.get('code'))

        deleted = 0

        # Delete in reverse dependency order
        for rule in ShippingPromotion.objects.all():
            if rule.name not in remote['ShippingPromotion']:
                rule.delete()
                deleted += 1

        for table in ShippingRateTable.objects.all():
            if table.name not in remote['ShippingRateTable']:
                table.delete()
                deleted += 1

        for method in ShippingMethod.objects.all():
            if method.name not in remote['ShippingMethod']:
                try:
                    method.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete shipping method {method.name}: {e}")

        for loc in Location.objects.all():
            if loc.code not in remote['Location']:
                loc.delete()
                deleted += 1

        for pkg in ShippingPackage.objects.all():
            if pkg.name not in remote['ShippingPackage']:
                pkg.delete()
                deleted += 1

        for zone in ShippingZone.objects.all():
            if zone.name not in remote['ShippingZone']:
                try:
                    zone.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete shipping zone {zone.name}: {e}")

        for preset in CarrierPreset.objects.all():
            if preset.slug not in remote['CarrierPreset']:
                preset.delete()
                deleted += 1

        for account in ProviderAccount.objects.all():
            if account.display_name not in remote['ProviderAccount']:
                account.delete()
                deleted += 1

        return deleted

    def generate_diff(self, remote_data):
        from shipping.models import (
            ProviderAccount, ShippingZone, ShippingPromotion,
            ShippingRateTable, ShippingPackage, CarrierPreset, Location,
        )
        from cart.models import ShippingMethod

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            name = item.get('name') or item.get('slug') or item.get('code', 'Unknown')

            existing = None
            fields = []

            if model_type == 'ProviderAccount':
                existing = ProviderAccount.objects.filter(display_name=item.get('display_name', '')).first()
                fields = PROVIDER_ACCOUNT_FIELDS
            elif model_type == 'CarrierPreset':
                existing = CarrierPreset.objects.filter(slug=item.get('slug')).first()
                fields = CARRIER_PRESET_FIELDS
            elif model_type == 'ShippingZone':
                existing = ShippingZone.objects.filter(name=item.get('name')).first()
                fields = SHIPPING_ZONE_FIELDS
            elif model_type == 'ShippingPackage':
                existing = ShippingPackage.objects.filter(name=item.get('name')).first()
                fields = SHIPPING_PACKAGE_FIELDS
            elif model_type == 'ShippingMethod':
                existing = ShippingMethod.objects.filter(name=item.get('name')).first()
                fields = SHIPPING_METHOD_FIELDS
            elif model_type == 'ShippingPromotion':
                existing = ShippingPromotion.objects.filter(name=item.get('name')).first()
                fields = SHIPPING_PROMOTION_FIELDS
            elif model_type == 'ShippingRateTable':
                existing = ShippingRateTable.objects.filter(name=item.get('name')).first()
                fields = RATE_TABLE_FIELDS
            elif model_type == 'Location':
                existing = Location.objects.filter(code=item.get('code')).first()
                fields = LOCATION_FIELDS
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
