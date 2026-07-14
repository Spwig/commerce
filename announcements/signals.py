from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Announcement


@receiver([post_save, post_delete], sender=Announcement)
def invalidate_announcement_cache(sender, **kwargs):
    """Clear the active announcements cache when any announcement is modified."""
    cache.delete("active_announcements")
