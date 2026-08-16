"""
Deleting a StaffRole must take its wrapped auth Group with it.

A StaffRole 1:1-wraps a Group that holds the real permissions and the member
assignments. The FK cascades group→role but not role→group, so before the
``post_delete`` cleanup (staff_roles/signals.py) deleting a role left an orphaned
group whose members silently kept the deleted role's access. These pin that the
group is removed with the role — including via the admin's bulk delete, which
goes through ``QuerySet.delete()`` — while the reverse cascade still works.
"""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from staff_roles.models import StaffRole

pytestmark = pytest.mark.django_db


def _role(name):
    group = Group.objects.create(name=name)
    return StaffRole.objects.create(group=group, display_name=name)


def test_deleting_a_staff_role_deletes_its_wrapped_group():
    role = _role("Editors")
    group_id = role.group_id
    assert Group.objects.filter(pk=group_id).exists()

    role.delete()

    assert not Group.objects.filter(pk=group_id).exists(), (
        "The wrapped Group was left orphaned when the StaffRole was deleted."
    )


def test_bulk_queryset_delete_also_removes_the_wrapped_groups():
    # The admin's bulk delete uses QuerySet.delete(), which never calls
    # Model.delete() but DOES fire post_delete — the reason the cleanup is a
    # signal rather than a delete() override.
    r1 = _role("Editors")
    r2 = _role("Viewers")
    group_ids = [r1.group_id, r2.group_id]

    StaffRole.objects.filter(pk__in=[r1.pk, r2.pk]).delete()

    assert not Group.objects.filter(pk__in=group_ids).exists()


def test_members_lose_the_group_when_the_role_is_deleted():
    # The security point: a user assigned to the deleted role's group no longer
    # carries that group (and its permissions) afterwards.
    role = _role("Managers")
    user = get_user_model().objects.create_user(
        username="m1", email="m1@test.spwig.com", password="pw-123456!"
    )
    user.groups.add(role.group)
    assert user.groups.filter(pk=role.group_id).exists()

    role.delete()

    assert not user.groups.filter(name="Managers").exists()


def test_deleting_the_group_still_cascades_to_the_role():
    # Control: the reverse direction is unchanged and the signal's no-op guard
    # keeps a group-first deletion from erroring.
    role = _role("Temp")
    role_pk = role.pk
    group = role.group

    group.delete()

    assert not StaffRole.objects.filter(pk=role_pk).exists()
