# Manual migration: Rename ShippingRule -> ShippingPromotion, rename fields,
# add controls_visibility, clean up ShippingRateTable

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('cart', '0005_remove_shippingmethod_max_order_value_and_more'),
        ('catalog', '0004_producttag_product_tags'),
        ('shipping', '0001_initial'),
    ]

    operations = [
        # =============================================
        # ShippingRateTable cleanup
        # =============================================
        migrations.RemoveField(
            model_name='shippingratetable',
            name='zones',
        ),
        migrations.AlterField(
            model_name='shippingratetable',
            name='shipping_method',
            field=models.ForeignKey(
                help_text='Shipping method this table provides pricing for',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rate_tables',
                to='cart.shippingmethod',
                verbose_name='shipping method',
            ),
        ),

        # =============================================
        # Rename ShippingRule -> ShippingPromotion
        # =============================================
        migrations.RenameModel(
            old_name='ShippingRule',
            new_name='ShippingPromotion',
        ),

        # Rename fields
        migrations.RenameField(
            model_name='shippingpromotion',
            old_name='rule_type',
            new_name='promotion_type',
        ),
        migrations.RenameField(
            model_name='shippingpromotion',
            old_name='rule_value',
            new_name='promotion_value',
        ),
        migrations.RenameField(
            model_name='shippingpromotion',
            old_name='rule_value_currency',
            new_name='promotion_value_currency',
        ),
        migrations.RenameField(
            model_name='shippingpromotion',
            old_name='stop_further_rules',
            new_name='stop_further_promotions',
        ),

        # Add new field
        migrations.AddField(
            model_name='shippingpromotion',
            name='controls_visibility',
            field=models.BooleanField(
                default=False,
                help_text="When enabled, linked shipping methods are only shown at checkout when this promotion's conditions are met",
                verbose_name='controls method visibility',
            ),
        ),

        # Update verbose names and help texts via AlterField
        migrations.AlterField(
            model_name='shippingpromotion',
            name='name',
            field=models.CharField(
                help_text='Internal name for this promotion',
                max_length=200,
                verbose_name='promotion name',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='description',
            field=models.TextField(
                blank=True,
                help_text='Optional description of what this promotion does',
                verbose_name='description',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='promotion_type',
            field=models.CharField(
                choices=[
                    ('discount_percentage', 'Percentage Discount'),
                    ('discount_fixed', 'Fixed Amount Discount'),
                    ('override_cost', 'Override Cost'),
                    ('free_shipping', 'Free Shipping'),
                    ('surcharge_fixed', 'Fixed Surcharge'),
                    ('surcharge_percentage', 'Percentage Surcharge'),
                ],
                max_length=30,
                verbose_name='promotion type',
            ),
        ),

        # Update Meta
        migrations.AlterModelOptions(
            name='shippingpromotion',
            options={
                'ordering': ['-priority', 'name'],
                'verbose_name': 'shipping promotion',
                'verbose_name_plural': 'shipping promotions',
            },
        ),

        # Update related names on M2M fields
        migrations.AlterField(
            model_name='shippingpromotion',
            name='zones',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion only applies to these zones (empty = all zones)',
                related_name='shipping_promotions',
                to='shipping.shippingzone',
                verbose_name='shipping zones',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='shipping_methods',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion only applies to these shipping methods (empty = all methods)',
                related_name='shipping_promotions',
                to='cart.shippingmethod',
                verbose_name='shipping methods',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='requires_products',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion only applies if cart contains these products',
                related_name='required_for_shipping_promotions',
                to='catalog.product',
                verbose_name='requires products',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='requires_categories',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion only applies if cart contains products from these categories',
                related_name='required_for_shipping_promotions',
                to='catalog.category',
                verbose_name='requires categories',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='excludes_products',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion does not apply if cart contains these products',
                related_name='excluded_from_shipping_promotions',
                to='catalog.product',
                verbose_name='excludes products',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='excludes_categories',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion does not apply if cart contains products from these categories',
                related_name='excluded_from_shipping_promotions',
                to='catalog.category',
                verbose_name='excludes categories',
            ),
        ),
        migrations.AlterField(
            model_name='shippingpromotion',
            name='customer_groups',
            field=models.ManyToManyField(
                blank=True,
                help_text='Promotion only applies to these customer groups (empty = all customers)',
                related_name='shipping_promotions',
                to='auth.group',
                verbose_name='customer groups',
            ),
        ),
    ]
