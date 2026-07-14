from django.core.management.base import BaseCommand

from page_builder.models import Element


class Command(BaseCommand):
    help = "Remove legacy font-related properties that are now handled by the typography editor"

    def handle(self, *args, **options):
        # Properties that are now handled by the typography editor
        legacy_properties = [
            "fontSize",
            "fontWeight",
            "fontStyle",
            "textAlign",
            "lineHeight",
            "letterSpacing",
            "textTransform",
            "textIndent",
            "verticalAlign",
            "textDecoration",
            "textDecorationStyle",
            "wordSpacing",
            # Also remove old variations
            "font_size",
            "font_weight",
            "font_style",
            "text_align",
            "line_height",
            "letter_spacing",
            "text_transform",
            "text_indent",
            "vertical_align",
            "text_decoration",
            "text_decoration_style",
            "word_spacing",
            "custom_font_size",
            "custom_font_weight",
            "custom_line_height",
            "custom_letter_spacing",
        ]

        elements_updated = 0
        properties_removed = 0

        # Process all elements
        for element in Element.objects.all():
            if not element.content:
                continue

            content = element.content if isinstance(element.content, dict) else {}
            modified = False

            # Check if element has typography property
            has_typography = content.get("typography") and content["typography"] != "inherit"

            # Remove legacy properties only if typography exists
            if has_typography:
                for prop in legacy_properties:
                    if prop in content:
                        self.stdout.write(
                            f'Element {element.id}: Removing {prop}="{content[prop]}"'
                        )
                        del content[prop]
                        properties_removed += 1
                        modified = True

            if modified:
                element.content = content
                element.save()
                elements_updated += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Element {element.id} updated"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Cleanup complete: Updated {elements_updated} elements, "
                f"removed {properties_removed} legacy properties"
            )
        )
