# Generated manually for Magento migration support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migration', '0005_add_activity_log_and_extra_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='migrationmapping',
            name='transform_type',
            field=models.CharField(choices=[('none', 'No Transformation'), ('string', 'Convert to String'), ('integer', 'Convert to Integer'), ('decimal', 'Convert to Decimal'), ('boolean', 'Convert to Boolean'), ('json', 'Parse JSON'), ('date', 'Parse Date'), ('url', 'Validate URL'), ('email', 'Validate Email'), ('money', 'Convert to Money'), ('integer_nullable', 'Integer (allow null)'), ('decimal_nullable', 'Decimal (allow null)'), ('woocommerce_status', 'WooCommerce Status'), ('woocommerce_type', 'WooCommerce Product Type'), ('woocommerce_backorders', 'WooCommerce Backorders'), ('meta_array', 'Meta Data Array'), ('category_array', 'Category Array'), ('image_array', 'Image Array'), ('category_parent', 'Category Parent Resolution'), ('custom', 'Custom Function'), ('shopify_status', 'Shopify Product Status'), ('shopify_order_status', 'Shopify Order Status'), ('shopify_discount_type', 'Shopify Discount Type'), ('shopify_discount_value', 'Shopify Discount Value'), ('shopify_inventory_tracked', 'Shopify Inventory Tracked'), ('shopify_inventory_policy', 'Shopify Inventory Policy'), ('comma_separated', 'Comma-Separated to List'), ('magento_status', 'Magento Product Status'), ('magento_visibility', 'Magento Product Visibility'), ('magento_order_status', 'Magento Order Status'), ('magento_discount_type', 'Magento Discount Type')], default='none', help_text='Data transformation to apply', max_length=30),
        ),
    ]
