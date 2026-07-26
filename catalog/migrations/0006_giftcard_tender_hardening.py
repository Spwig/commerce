"""
Harden GiftCard for use as a payment tender.

Adds `uuid` in three steps rather than one. A `UUIDField(unique=True,
default=uuid4)` added in a single AddField gives every pre-existing row the
*same* generated default, which violates the unique constraint the moment the
table is non-empty. So: add it nullable and unconstrained, fill it per row,
then apply uniqueness.

Also switches GiftCardTransaction.gift_card from CASCADE to PROTECT. That
ledger records movements of real customer money; deleting a card should not
take its financial history with it, and a card holding value should not be
deletable at all.
"""

import uuid

import django.db.models.deletion
from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    """Give every existing card its own uuid."""
    GiftCard = apps.get_model("catalog", "GiftCard")
    # Chunked rather than one big list: this runs during an upgrade, and the
    # upgrader gives migrations a hard 300s budget.
    for card in GiftCard.objects.filter(uuid__isnull=True).iterator(chunk_size=1000):
        GiftCard.objects.filter(pk=card.pk).update(uuid=uuid.uuid4())


def noop_reverse(apps, schema_editor):
    """Reversing drops the column; nothing to restore."""


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_add_product_requires_shipping"),
    ]

    operations = [
        migrations.AddField(
            model_name="giftcard",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        # Step 1: nullable, not unique — safe against existing rows.
        migrations.AddField(
            model_name="giftcard",
            name="uuid",
            field=models.UUIDField(
                null=True,
                editable=False,
                verbose_name="UUID",
                help_text="Stable public identifier — safe to expose where the code is not",
            ),
        ),
        # Step 2: one value per row.
        migrations.RunPython(populate_uuids, noop_reverse),
        # Step 3: now that values are distinct, enforce it.
        migrations.AlterField(
            model_name="giftcard",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                db_index=True,
                verbose_name="UUID",
                help_text="Stable public identifier — safe to expose where the code is not",
            ),
        ),
        migrations.AlterField(
            model_name="giftcardtransaction",
            name="gift_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="transactions",
                to="catalog.giftcard",
                verbose_name="Gift Card",
            ),
        ),
    ]
