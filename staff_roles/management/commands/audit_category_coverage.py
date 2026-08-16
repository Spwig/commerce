"""Report admin models that no permission category covers (superuser-only).

    ./manage.py audit_category_coverage                 # fail (exit 1) on real gaps
    ./manage.py audit_category_coverage --list          # list every uncovered model
    ./manage.py audit_category_coverage --update-allowlist  # accept current uncovered set

"Real gap" = an admin-registered model that is neither slotted into a category
(so a merchant can delegate it) nor on the intentional superuser-only allowlist.
"""

from django.core.management.base import BaseCommand

from staff_roles.category_coverage import (
    find_uncovered,
    stale_allowlist,
    violations,
    write_allowlist,
)


class Command(BaseCommand):
    help = "Audit permission-category coverage of admin-registered models."

    def add_arguments(self, parser):
        parser.add_argument("--list", action="store_true", help="List all uncovered models.")
        parser.add_argument(
            "--update-allowlist",
            action="store_true",
            help="Rewrite the allowlist to the current uncovered set.",
        )

    def handle(self, *args, **options):
        if options["list"]:
            uncovered = find_uncovered()
            for m in uncovered:
                self.stdout.write(m)
            self.stdout.write(f"\n{len(uncovered)} uncovered model(s).")
            return

        if options["update_allowlist"]:
            uncovered = find_uncovered()
            write_allowlist(uncovered)
            self.stdout.write(self.style.SUCCESS(f"Allowlist updated: {len(uncovered)} models."))
            return

        gaps = violations()
        if gaps:
            self.stdout.write(
                self.style.ERROR(
                    "category-coverage: model(s) reachable only by a superuser "
                    "(add to a category in staff_roles/categories.py, or to the "
                    "allowlist if superuser-only is intended):\n"
                )
            )
            for m in gaps:
                self.stdout.write(f"    + {m}")
            raise SystemExit(1)

        stale = stale_allowlist()
        msg = "category-coverage OK — every admin model is in a category or allowlisted."
        if stale:
            msg += f" {len(stale)} allowlist entry(ies) now covered — run --update-allowlist."
        self.stdout.write(self.style.SUCCESS(msg))
