"""
Promote Product.requires_shipping from a @property to a real column.

The property returned ``product_type not in ("digital", "booking")``, but
``cart/models.py`` filters on ``product__requires_shipping=True`` — which the
ORM cannot resolve against a property, so that query raised FieldError on the
shippable-cart path.

The backfill replays the property exactly, so no product changes behaviour.
"""

from django.db import migrations, models

# Types the old property treated as non-shippable.
NON_SHIPPABLE_TYPES = ("digital", "booking")


def backfill_requires_shipping(apps, schema_editor):
    """Replay the old property's result onto the new column."""
    Product = apps.get_model("catalog", "Product")
    Product.objects.filter(product_type__in=NON_SHIPPABLE_TYPES).update(
        requires_shipping=False
    )
    Product.objects.exclude(product_type__in=NON_SHIPPABLE_TYPES).update(
        requires_shipping=True
    )


def noop_reverse(apps, schema_editor):
    """Reversing just drops the column; nothing to restore."""


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_producttag_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='requires_shipping',
            field=models.BooleanField(db_index=True, default=True, help_text='Whether this product needs to be shipped to the customer. Turn off for downloads, services and bookings.', verbose_name='Requires Shipping'),
        ),
        migrations.RunPython(backfill_requires_shipping, noop_reverse),
    ]
