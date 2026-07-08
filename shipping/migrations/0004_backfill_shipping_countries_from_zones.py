"""
Backfill `ShippingCountry` rows from existing `ShippingZone.countries` lists.

Until this migration, the merchant had to fill `ShippingCountry` manually
(via an admin URL we never surfaced in any menu). Without those rows,
`PaymentMethodFilter` silently filters every payment provider out at
checkout — the cocosbotanica.com Stripe-checkout outage on 2026-06-27 was
the visible symptom. This is a one-shot reconcile so existing installs
catch up the moment they upgrade.

The forward op is `get_or_create` keyed on the existing
`(site, country_code)` unique constraint, so re-running is a no-op.
The reverse op is intentionally empty: a migration rollback should not
delete production rows that may now be referenced by warehouse fallback,
fulfillment, or merchant-customised settings.
"""
from __future__ import annotations

from django.db import migrations


def backfill_shipping_countries(apps, schema_editor):
    ShippingZone = apps.get_model("shipping", "ShippingZone")
    ShippingCountry = apps.get_model("shipping", "ShippingCountry")

    for zone in ShippingZone.objects.filter(is_active=True):
        raw_codes = zone.countries or []
        seen: set[str] = set()
        for raw in raw_codes:
            if not isinstance(raw, str):
                continue
            code = raw.strip().upper()
            if not code or code in seen:
                continue
            seen.add(code)
            site_id = getattr(zone, "site_id", None) or 1
            ShippingCountry.objects.get_or_create(
                site_id=site_id,
                country_code=code,
                defaults={"is_active": True},
            )


def noop_reverse(apps, schema_editor):
    # Intentionally a no-op: see module docstring.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("shipping", "0003_alter_shippingpromotion_created_by_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_shipping_countries, noop_reverse),
    ]
