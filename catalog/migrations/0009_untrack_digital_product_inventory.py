from django.db import migrations


def untrack_digital_products(apps, schema_editor):
    """
    Plain digital products must not be stock-gated (they are delivered as
    downloads/licences, and the admin hides the Inventory fieldset and
    StockItemInline for them). ``Product.save()`` now forces
    ``track_inventory=False`` for ``product_type="digital"``, but that only
    runs on write — existing digital rows created before the fix still carry
    the ``track_inventory=True`` field default and would keep failing
    add-to-cart with "Insufficient stock". Flip them here.
    """
    Product = apps.get_model("catalog", "Product")
    Product.objects.filter(product_type="digital", track_inventory=True).update(
        track_inventory=False
    )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_product_agent_visible_product_condition"),
    ]

    operations = [
        # Reverse is a no-op: re-tracking would reintroduce the bug, and the
        # pre-fix value is not recoverable per-row anyway.
        migrations.RunPython(untrack_digital_products, migrations.RunPython.noop),
    ]
