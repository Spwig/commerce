"""
Cache invalidation signals for custom field definitions.

When field definitions or groups change, we clear the cached versions
so the next request fetches fresh data from the database.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import CustomFieldDefinition, CustomFieldGroup


@receiver(post_save, sender=CustomFieldDefinition)
@receiver(post_delete, sender=CustomFieldDefinition)
def invalidate_field_cache(sender, instance, **kwargs):
    """Clear cached field definitions when a definition changes."""
    if instance.content_type_id:
        CustomFieldDefinition.invalidate_cache(instance.content_type)


@receiver(post_save, sender=CustomFieldGroup)
@receiver(post_delete, sender=CustomFieldGroup)
def invalidate_group_cache(sender, instance, **kwargs):
    """Clear cached groups when a group changes."""
    if instance.content_type_id:
        CustomFieldDefinition.invalidate_cache(instance.content_type)
