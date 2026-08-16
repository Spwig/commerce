"""Grant the new ``analytics`` category to roles that already have ``marketing``.

The Insights sidebar group (Revenue Attribution) gates on the new ``analytics``
category. Existing custom staff roles don't have it, so without this they'd lose
sight of attribution. Superusers are unaffected (they bypass category checks);
this keeps existing marketing-capable staff seeing the dashboard. New roles grant
it via the role admin as usual.

``has_category_access`` reads ``permission_categories`` directly, so updating the
JSON is sufficient for sidebar + view access; the precise Django group
permissions for attribution models sync on the role's next save.
"""

from django.db import migrations


def grant_analytics(apps, schema_editor):
    StaffRole = apps.get_model("staff_roles", "StaffRole")
    for role in StaffRole.objects.all():
        cats = role.permission_categories or {}
        if "marketing" in cats and "analytics" not in cats:
            cats["analytics"] = "view"
            role.permission_categories = cats
            role.save(update_fields=["permission_categories"])


class Migration(migrations.Migration):
    dependencies = [
        ("staff_roles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(grant_analytics, migrations.RunPython.noop),
    ]
