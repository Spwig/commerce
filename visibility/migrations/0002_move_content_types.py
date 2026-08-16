"""Preserve Django permission grants across the page_builder → visibility move.

When a model changes ``app_label``, Django's post_migrate hook creates brand-new
ContentType + Permission rows for the new label, orphaning any grants a merchant
had given a staff role against the old ``page_builder.*_rulegroup`` /
``*_visibilityrule`` permissions. That would silently strip non-superuser staff of
access to the visibility-rule admin on upgrade.

This is a pure data migration (SeparateDatabaseAndState is not involved — it only
touches contenttypes/auth rows, no schema). It handles both cases:

* **Clean upgrade** (only the old ``page_builder`` ContentType exists — the normal
  path, because data migrations run before post_migrate): rename the row's
  ``app_label`` in place. The ContentType PK, its four permissions, and every
  group/user grant are preserved untouched.
* **Reconciliation** (both old and new ContentTypes already exist — e.g. a DB
  where post_migrate already created the ``visibility`` rows): move any grants
  from the stale ``page_builder`` permissions onto the matching ``visibility``
  permissions, then delete the stale ContentType (which cascades its now-empty
  permissions).

Fresh installs never had a ``page_builder`` ContentType for these models, so this
is a no-op there.
"""

from django.conf import settings
from django.db import migrations

_MODELS = ("visibilityrule", "rulegroup", "rulegroupmember")


def _move_grants(apps, old_ct, new_ct):
    """Repoint group/user grants from old_ct's permissions to new_ct's, matched
    by codename, then drop the stale permissions with the old ContentType."""
    Permission = apps.get_model("auth", "Permission")
    Group = apps.get_model("auth", "Group")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))

    for old_perm in Permission.objects.filter(content_type=old_ct):
        new_perm = Permission.objects.filter(
            content_type=new_ct, codename=old_perm.codename
        ).first()
        if new_perm is None:
            # post_migrate will create it later; nothing to move onto yet, but we
            # must not lose the grant. Re-point the old permission's ContentType
            # instead of deleting it.
            old_perm.content_type = new_ct
            old_perm.save(update_fields=["content_type"])
            continue
        for group in Group.objects.filter(permissions=old_perm):
            group.permissions.add(new_perm)
            group.permissions.remove(old_perm)
        for user in User.objects.filter(user_permissions=old_perm):
            user.user_permissions.add(new_perm)
            user.user_permissions.remove(old_perm)


def forwards(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    for model in _MODELS:
        old_ct = ContentType.objects.filter(app_label="page_builder", model=model).first()
        if old_ct is None:
            continue  # fresh install — nothing to migrate
        new_ct = ContentType.objects.filter(app_label="visibility", model=model).first()
        if new_ct is None:
            # Clean upgrade: rename in place — keeps PK, permissions and grants.
            old_ct.app_label = "visibility"
            old_ct.save(update_fields=["app_label"])
        else:
            # Both exist: fold the stale one into the new one, then remove it.
            _move_grants(apps, old_ct, new_ct)
            old_ct.delete()


def backwards(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    for model in _MODELS:
        vis_ct = ContentType.objects.filter(app_label="visibility", model=model).first()
        if vis_ct is None:
            continue
        if ContentType.objects.filter(app_label="page_builder", model=model).exists():
            continue  # can't merge back automatically; leave as-is
        vis_ct.app_label = "page_builder"
        vis_ct.save(update_fields=["app_label"])


class Migration(migrations.Migration):

    dependencies = [
        ("visibility", "0001_initial"),
        ("page_builder", "0003_remove_rulegroupmember_rule_group_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
