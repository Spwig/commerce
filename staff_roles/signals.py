"""
Delete a StaffRole's wrapped auth Group when the role itself is deleted.

A StaffRole 1:1-wraps a Django ``auth.Group`` that holds the actual permissions
and the member (user) assignments. The relationship cascades group→role (deleting
the Group deletes its StaffRole) but NOT role→group, so deleting a StaffRole — most
importantly a *bulk* delete from the Django admin, which calls ``QuerySet.delete()``
and never ``Model.delete()`` — used to leave the Group behind. That orphaned
permission group kept its members, silently preserving the deleted role's access.

This ``post_delete`` receiver removes the wrapped Group so the role, its
permissions, and its member assignments all disappear together. It is wired from
``StaffRolesConfig.ready()``.
"""

from django.contrib.auth.models import Group
from django.db.models.signals import post_delete
from django.dispatch import receiver

from staff_roles.models import StaffRole


@receiver(post_delete, sender=StaffRole)
def delete_wrapped_group(sender, instance, **kwargs):
    """
    Remove the Group a deleted StaffRole wrapped.

    Uses a filter-delete rather than ``instance.group.delete()`` so the reverse
    case — the Group being deleted first, cascading the role away — finds the
    group already gone and is a harmless no-op instead of a ``DoesNotExist``.
    """
    group_id = instance.group_id
    if group_id is not None:
        Group.objects.filter(pk=group_id).delete()
