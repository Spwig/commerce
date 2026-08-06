from django.db import migrations


def set_region_modes(apps, schema_editor):
    """
    Back-fill ``region_restriction_mode`` from the pre-existing
    ``ProductRegionVisibility`` rows (which were a pure allowlist).

    - A product with any ``is_visible=True`` row was visible only in those
      regions -> ``only_in``. Its ``is_visible=False`` rows were dead weight
      (they hid nothing and only forced allowlist mode), so drop them; the
      remaining rows become the allow list.
    - A product whose rows are *all* ``is_visible=False`` was hidden in every
      region (a footgun). The merchant plainly meant "not available in these",
      so interpret it as the intended blocklist -> ``all_except``.
    - Products with no rows keep the default ``all``.

    After this, a row simply means "this region is selected"; the ``is_visible``
    column is no longer read (kept only to avoid a destructive migration) and is
    normalised to True.
    """
    Product = apps.get_model("catalog", "Product")
    ProductRegionVisibility = apps.get_model("catalog", "ProductRegionVisibility")

    product_ids = list(
        ProductRegionVisibility.objects.values_list("product_id", flat=True).distinct()
    )
    for pid in product_ids:
        rows = ProductRegionVisibility.objects.filter(product_id=pid)
        if rows.filter(is_visible=True).exists():
            rows.filter(is_visible=False).delete()
            Product.objects.filter(pk=pid).update(region_restriction_mode="only_in")
        else:
            Product.objects.filter(pk=pid).update(region_restriction_mode="all_except")
        # Remaining rows are membership markers now.
        ProductRegionVisibility.objects.filter(product_id=pid).update(is_visible=True)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0010_product_region_restriction_mode"),
    ]

    operations = [
        migrations.RunPython(set_region_modes, migrations.RunPython.noop),
    ]
