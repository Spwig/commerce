# Backfill the issued currency for existing vouchers.
#
# Product decision (2026-07-21): vouchers and gift cards are only redeemable
# in the currency they were issued in. Existing vouchers infer that currency
# from their monetary fields where one is set, else the store default.

from django.db import migrations


def backfill_currency(apps, schema_editor):
    VoucherCode = apps.get_model("vouchers", "VoucherCode")

    # Store default currency, straight from site settings if available
    default_currency = "USD"
    try:
        SiteSettings = apps.get_model("core", "SiteSettings")
        settings = SiteSettings.objects.first()
        if settings and settings.default_currency:
            default_currency = settings.default_currency
    except LookupError:
        pass

    for voucher in VoucherCode.objects.filter(currency="").iterator():
        currency = None
        # MoneyField companion currency columns are only meaningful when the
        # amount itself is set (the currency column keeps its default even
        # for NULL amounts)
        for amount_field, currency_field in (
            ("original_gift_card_value", "original_gift_card_value_currency"),
            ("min_order_value", "min_order_value_currency"),
            ("max_discount_amount", "max_discount_amount_currency"),
        ):
            if getattr(voucher, amount_field) is not None:
                currency = getattr(voucher, currency_field)
                break
        voucher.currency = currency or default_currency
        voucher.save(update_fields=["currency"])


class Migration(migrations.Migration):
    dependencies = [
        ("vouchers", "0003_vouchercode_currency"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(backfill_currency, migrations.RunPython.noop),
    ]
