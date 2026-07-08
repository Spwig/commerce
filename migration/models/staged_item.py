"""
MigrationStagedItem Model
Staging table for items that couldn't be imported automatically.
Allows admin to review, fix, and retry individual items.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class MigrationStagedItem(models.Model):
    """
    Temporary storage for items that failed import.
    Admin can review, edit data, and retry import.
    """

    ITEM_TYPES = [
        ('product', _('Product')),
        ('category', _('Category')),
        ('customer', _('Customer')),
        ('order', _('Order')),
        ('review', _('Review')),
    ]

    FAILURE_REASONS = [
        ('missing_required', _('Missing Required Field')),
        ('invalid_data', _('Invalid Data Format')),
        ('missing_relationship', _('Missing Relationship')),
        ('transform_failed', _('Data Transformation Failed')),
        ('duplicate', _('Duplicate Entry')),
        ('validation_failed', _('Validation Failed')),
        ('unknown', _('Unknown Error')),
    ]

    # Link to migration job
    job = models.ForeignKey(
        'MigrationJob',
        on_delete=models.CASCADE,
        related_name='staged_items',
        help_text=_("Parent migration job")
    )

    # Item identification
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    external_id = models.CharField(
        max_length=100,
        help_text=_("Original ID from source platform")
    )

    # Original source data (as received from API)
    source_data = models.JSONField(
        help_text=_("Original data from WooCommerce/Shopify")
    )

    # Transformed/prepared data (what we tried to import)
    prepared_data = models.JSONField(
        blank=True,
        null=True,
        help_text=_("Data after transformation, ready for model creation")
    )

    # Error information
    failure_reason = models.CharField(
        max_length=30,
        choices=FAILURE_REASONS,
        help_text=_("Why this item failed to import")
    )

    error_message = models.TextField(
        help_text=_("Detailed error message")
    )

    error_field = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Specific field that caused the error")
    )

    # Retry tracking
    retry_count = models.IntegerField(default=0)
    last_retry_at = models.DateTimeField(null=True, blank=True)

    # Admin review
    STATUS_CHOICES = [
        ('pending_review', _('Pending Review')),
        ('in_progress', _('Being Fixed')),
        ('ready_retry', _('Ready to Retry')),
        ('imported', _('Successfully Imported')),
        ('skipped', _('Skipped by Admin')),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending_review'
    )

    admin_notes = models.TextField(
        blank=True,
        help_text=_("Admin notes about fixing this item")
    )

    # Successfully imported object (if retry succeeded)
    imported_model = models.CharField(max_length=50, blank=True)
    imported_object_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Staged Item')
        verbose_name_plural = _('Staged Items')
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['item_type', 'status']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.get_item_type_display()} #{self.external_id} ({self.get_failure_reason_display()})"

    def get_admin_url(self):
        """Get URL to edit this staged item"""
        from django.urls import reverse
        return reverse('admin:migration_stageditem_change', args=[self.pk])

    def retry_import(self):
        """
        Attempt to import this item again.
        Returns (success: bool, result: object or error_message)
        """
        from ..importers.executor import ImportExecutor
        from .step import MigrationStep

        STEP_TYPE_MAP = {
            'product': 'products',
            'category': 'categories',
            'customer': 'customers',
            'order': 'orders',
            'review': 'reviews',
        }

        TYPE_DISPATCH = {
            'product': ('_import_single_product', 'Product'),
            'category': ('_import_single_category', 'Category'),
            'customer': ('_import_single_customer', 'User'),
            'order': ('_import_single_order', 'Order'),
            'review': ('_import_single_review', 'ProductReview'),
        }

        if self.item_type not in TYPE_DISPATCH:
            return False, f"Unknown item type: {self.item_type}"

        try:
            # Create executor — __init__ handles client setup per platform
            executor = ImportExecutor(self.job)

            # Resolve default warehouse for product/variant stock items
            if self.item_type == 'product':
                from catalog.models import Warehouse
                executor.default_warehouse = Warehouse.objects.filter(is_active=True).first()

            # Get or create a MigrationStep for stats tracking
            step, _ = MigrationStep.objects.get_or_create(
                job=self.job,
                step_type=STEP_TYPE_MAP[self.item_type],
                defaults={'status': 'running', 'started_at': timezone.now()},
            )

            method_name, model_name = TYPE_DISPATCH[self.item_type]
            method = getattr(executor, method_name)
            result = method(self.source_data, step)

            if result:
                self.status = 'imported'
                self.imported_model = model_name
                self.imported_object_id = result.id
                self.save()
                return True, result

            return False, "Import returned no result"

        except Exception as e:
            self.retry_count += 1
            self.last_retry_at = timezone.now()
            self.error_message = str(e)
            self.save()
            return False, str(e)
