"""
Extract translatable text from seeded page builder elements into JSON.

Usage:
    python manage.py extract_seed_strings --output seed_strings.json

The output JSON can be fed to a translation system (e.g. the Spwig translation
agent) and then imported back via `import_seed_translations`.
"""

import json

from django.conf import settings
from django.core.management.base import BaseCommand

# Page slugs created by seed_page_elements
SEEDED_PAGE_SLUGS = [
    "404",
    "500",
    "about",
    "contact",
    "faq",
    "privacy-policy",
    "terms-of-use",
    "cookie-policy",
    "shipping-info",
    "returns-policy",
    "home",
    "maintenance",
]

# Content fields that contain translatable text
TRANSLATABLE_FIELDS = {
    "text",
    "title",
    "subtitle",
    "description",
    "button_text",
    "cta_text",
    "placeholder",
    "success_message",
    "view_all_text",
}

# Fields that contain nested translatable structures
NESTED_TRANSLATABLE_FIELDS = {
    "items",  # FAQ accordion items: [{question, answer}, ...]
    "fields",  # Contact form fields: [{label, placeholder}, ...]
}

# Field keys within nested items that are translatable
ITEM_TRANSLATABLE_KEYS = {"question", "answer", "label", "placeholder"}


def extract_translatable_content(content):
    """Extract translatable fields from an element's content dict."""
    if not content or not isinstance(content, dict):
        return {}

    result = {}

    # Simple text fields
    for field in TRANSLATABLE_FIELDS:
        if field in content and content[field]:
            value = content[field]
            if isinstance(value, str) and value.strip():
                result[field] = value

    # Nested structures (FAQ items, form fields)
    for field in NESTED_TRANSLATABLE_FIELDS:
        if field in content and isinstance(content[field], list):
            items = []
            for item in content[field]:
                if not isinstance(item, dict):
                    continue
                translatable_item = {}
                for key in ITEM_TRANSLATABLE_KEYS:
                    if key in item and isinstance(item[key], str) and item[key].strip():
                        translatable_item[key] = item[key]
                if translatable_item:
                    items.append(translatable_item)
            if items:
                result[field] = items

    return result


class Command(BaseCommand):
    help = "Extract translatable text from seeded page builder elements into JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            "-o",
            default="seed_strings.json",
            help="Output JSON file path (default: seed_strings.json)",
        )
        parser.add_argument(
            "--pretty",
            action="store_true",
            default=True,
            help="Pretty-print JSON output (default: True)",
        )

    def handle(self, *args, **options):
        from page_builder.models import Element, Page

        target_languages = [code for code, _name in settings.LANGUAGES if code != "en"]

        output = {
            "metadata": {
                "source": "seed_page_elements",
                "source_language": "en",
                "target_languages": sorted(target_languages),
                "total_elements": 0,
                "total_strings": 0,
            },
            "pages": {},
        }

        total_elements = 0
        total_strings = 0

        for slug in SEEDED_PAGE_SLUGS:
            try:
                page = Page.objects.get(slug=slug)
            except Page.DoesNotExist:
                self.stderr.write(f'  Page "{slug}" not found, skipping')
                continue

            # Get all elements for this page (including nested children)
            element_ids = self._get_page_element_ids(page, Element)
            elements = Element.objects.filter(id__in=element_ids).order_by("order", "id")

            page_data = {"elements": []}

            for element in elements:
                fields = extract_translatable_content(element.content)
                if not fields:
                    continue

                # Count strings
                string_count = 0
                for _key, value in fields.items():
                    if isinstance(value, str):
                        string_count += 1
                    elif isinstance(value, list):
                        for item in value:
                            string_count += len(item)

                element_data = {
                    "element_name": element.name,
                    "element_type": element.element_type,
                    "fields": fields,
                }

                # Include existing translations if any (for reference)
                if element.translations:
                    element_data["existing_translations"] = list(element.translations.keys())

                page_data["elements"].append(element_data)
                total_elements += 1
                total_strings += string_count

            if page_data["elements"]:
                output["pages"][slug] = page_data

        output["metadata"]["total_elements"] = total_elements
        output["metadata"]["total_strings"] = total_strings

        # Write output
        output_path = options["output"]
        indent = 2 if options["pretty"] else None
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=indent, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Extracted {total_elements} elements with {total_strings} "
                f"translatable strings from {len(output['pages'])} pages"
            )
        )
        self.stdout.write(f"Output: {output_path}")
        self.stdout.write(f"Target languages: {', '.join(target_languages)}")

    def _get_page_element_ids(self, page, Element):
        """Get all element IDs for a page, including nested children."""
        ids = set()
        parent_ids = set(Element.objects.filter(page=page).values_list("id", flat=True))
        ids.update(parent_ids)
        for _ in range(5):  # Max 5 nesting levels
            child_ids = set(
                Element.objects.filter(parent_element_id__in=parent_ids).values_list(
                    "id", flat=True
                )
            )
            if not child_ids:
                break
            ids.update(child_ids)
            parent_ids = child_ids
        return ids
