"""Strip stored HTML from ProductReview comments/titles.

Reviews are untrusted, plain-text customer content. Historically some reviews
(notably those brought in by platform migration importers, e.g. WooCommerce /
Magento) stored raw HTML in the comment. Storefront templates now strip tags at
render time, so stored HTML is already harmless to display — this command is an
optional one-off to also clean the stored data so it is plain text everywhere.

Dry-run by default; pass --apply to persist. Timestamps are preserved.
"""

from django.core.management.base import BaseCommand
from django.utils.html import strip_tags

from catalog.models import ProductReview


class Command(BaseCommand):
    help = "Strip stored HTML from ProductReview comments/titles (reviews are plain text)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Without this flag the command only reports (dry-run).",
        )

    def handle(self, *args, **options):
        apply = options["apply"]
        scanned = 0
        changed = 0

        for review in ProductReview.objects.all().iterator():
            scanned += 1
            new_comment = strip_tags(review.comment or "").strip()
            new_title = strip_tags(review.title or "").strip()
            if new_comment != (review.comment or "") or new_title != (review.title or ""):
                changed += 1
                if apply:
                    review.comment = new_comment
                    review.title = new_title
                    # Preserve updated_at — this is a cleanup, not a real edit.
                    review.save(update_fields=["comment", "title"])

        verb = "Updated" if apply else "Would update"
        self.stdout.write(
            self.style.SUCCESS(f"{verb} {changed} of {scanned} review(s) containing HTML.")
        )
        if not apply and changed:
            self.stdout.write("Re-run with --apply to persist.")
