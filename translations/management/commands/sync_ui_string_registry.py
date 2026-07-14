"""
Sync the UI string registry with existing UITranslationOverride rows.

Run after platform updates to update total_strings counts and optionally
auto-translate new strings for existing languages.

Usage:
    python manage.py sync_ui_string_registry
    python manage.py sync_ui_string_registry --auto-translate
"""

from django.core.management.base import BaseCommand

from translations.models import SiteLanguage, UITranslationOverride
from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count


class Command(BaseCommand):
    help = "Sync UI string registry with existing translation overrides"

    def add_arguments(self, parser):
        parser.add_argument(
            "--auto-translate",
            action="store_true",
            help="Auto-translate new strings for languages that have untranslated entries",
        )

    def handle(self, *args, **options):
        from translations.coverage_service import TranslationCoverageService
        from translations.templatetags.merchant_trans import BUILTIN_LANGUAGES

        total = get_total_string_count()
        self.stdout.write(f"Registry contains {total} strings")

        overrides = UITranslationOverride.objects.select_related("language").all()

        if not overrides.exists():
            self.stdout.write(self.style.WARNING("No UITranslationOverride rows found"))
            # Create override rows for all active languages
            active_langs = SiteLanguage.objects.filter(is_active=True)
            for lang in active_langs:
                if lang.code == "en":
                    continue
                UITranslationOverride.objects.get_or_create(
                    language=lang, defaults={"total_strings": total}
                )
                self.stdout.write(f"  Created override row for {lang.code}")
            overrides = UITranslationOverride.objects.select_related("language").all()

        coverage_service = TranslationCoverageService()

        for override in overrides:
            old_total = override.total_strings
            override.total_strings = total
            override.translated_count = sum(1 for v in override.overrides.values() if v)
            override.verified_count = sum(
                1 for m in override.meta_info.values() if m.get("verified")
            )
            override.save(update_fields=["total_strings", "translated_count", "verified_count"])

            new_strings = total - old_total if old_total > 0 else 0
            lang_code = override.language.code
            is_builtin = lang_code in BUILTIN_LANGUAGES and lang_code != "en"

            if is_builtin:
                effective = coverage_service._count_effective_ui_coverage(
                    lang_code, override, UI_STRING_REGISTRY
                )
                self.stdout.write(
                    f"  {lang_code}: "
                    f"{override.translated_count}/{total} overrides "
                    f"({effective}/{total} covered by shipped translations)"
                    f"{f' (+{new_strings} new strings)' if new_strings > 0 else ''}"
                )
            else:
                self.stdout.write(
                    f"  {lang_code}: "
                    f"{override.translated_count}/{total} translated"
                    f"{f' (+{new_strings} new strings)' if new_strings > 0 else ''}"
                )

        if options["auto_translate"]:
            from translations.tasks import auto_translate_ui_strings

            for override in overrides:
                lang_code = override.language.code
                is_builtin = lang_code in BUILTIN_LANGUAGES and lang_code != "en"

                if is_builtin:
                    # Built-in languages are already covered by .po translations
                    continue

                untranslated = override.total_strings - override.translated_count
                if untranslated > 0:
                    auto_translate_ui_strings.delay(override.language.id)
                    self.stdout.write(
                        f"  Queued auto-translate for {lang_code} "
                        f"({untranslated} untranslated strings)"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Synced registry ({total} strings) with {overrides.count()} language overrides"
            )
        )
