import logging

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class StaffRole(models.Model):
    """
    A named role that wraps a Django Group with additional metadata.

    Each StaffRole has a 1:1 relationship with a Django auth.Group.
    The Group holds the actual Django permissions, which are synced
    automatically when permission_categories are saved.
    """

    COLOR_CHOICES = [
        ("primary", _("Blue")),
        ("success", _("Green")),
        ("warning", _("Orange")),
        ("error", _("Red")),
        ("info", _("Teal")),
        ("default", _("Gray")),
    ]

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="staff_role",
        verbose_name=_("permission group"),
    )
    display_name = models.CharField(
        _("display name"),
        max_length=100,
        help_text=_("Human-readable name shown in the admin"),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("What this role is intended for"),
    )
    icon = models.CharField(
        _("icon"),
        max_length=50,
        default="fas fa-user",
        help_text=_("Font Awesome icon class"),
    )
    color = models.CharField(
        _("badge color"),
        max_length=20,
        default="primary",
        choices=COLOR_CHOICES,
    )
    is_predefined = models.BooleanField(
        _("system role"),
        default=False,
        help_text=_("Predefined roles cannot be deleted, but can be customized"),
    )
    permission_categories = models.JSONField(
        _("permission categories"),
        default=dict,
        blank=True,
        help_text=_(
            'High-level permission settings by category. Format: {"catalog": "full", "orders": "view"}'
        ),
    )
    pos_permissions = models.JSONField(
        _("POS permissions"),
        default=dict,
        blank=True,
        help_text=_("POS-specific permission flags"),
    )
    can_access_admin = models.BooleanField(
        _("can access admin panel"),
        default=True,
        help_text=_("Whether this role can log into the admin backend"),
    )
    can_access_pos = models.BooleanField(
        _("can access POS"),
        default=False,
        help_text=_("Whether this role can use POS terminals"),
    )
    sort_order = models.IntegerField(
        _("sort order"),
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Staff Role")
        verbose_name_plural = _("Staff Roles")
        ordering = ["sort_order", "display_name"]

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_permissions()

    def sync_permissions(self):
        """Sync permission_categories to Django Group permissions."""
        from staff_roles.services import resolve_category_permissions

        permissions = resolve_category_permissions(self.permission_categories)
        self.group.permissions.set(permissions)

    @property
    def member_count(self):
        """Number of users assigned to this role's group."""
        return self.group.user_set.count()

    def get_members(self):
        """Get all users assigned to this role."""
        return self.group.user_set.all()
