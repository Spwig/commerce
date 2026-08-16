"""Regression: every admin-registered model is delegatable via a category.

A model that no permission category covers is superuser-only — a merchant can't
grant it to a staff role. This fails when a new admin model ships without being
slotted into a category (staff_roles/categories.py) or explicitly marked
superuser-only (staff_roles/category_coverage_allowlist.txt). No DB needed — it
reads the admin registry + the category catalog.
"""

from django.test import SimpleTestCase

from staff_roles.category_coverage import violations


class CategoryCoverageTest(SimpleTestCase):
    def test_no_admin_model_is_superuser_only_by_accident(self):
        gaps = violations()
        self.assertEqual(
            gaps,
            [],
            "These admin models are reachable only by a superuser. Add each to a "
            "category in staff_roles/categories.py so merchants can delegate it, or "
            "to staff_roles/category_coverage_allowlist.txt if superuser-only is "
            "intended:\n  " + "\n  ".join(gaps),
        )
