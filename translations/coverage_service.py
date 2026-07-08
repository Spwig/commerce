"""
Translation coverage calculation service.

Calculates how much of a merchant's site content has been translated,
across all registered content types, email templates, and UI strings.

"""
import logging
from django.apps import apps
from django.core.cache import cache

from .content_registry import get_all_content_types, get_model_class

logger = logging.getLogger(__name__)

COVERAGE_CACHE_KEY = 'translation_coverage_v1'
COVERAGE_CACHE_TTL = 600  # 10 minutes


class TranslationCoverageService:
    """Calculates translation coverage across all content types."""

    def get_site_coverage(self, language_codes=None, use_cache=True):
        """
        Return overall site translation coverage.

        Args:
            language_codes: Optional list of language codes to check.
                           If None, uses all active non-default SiteLanguages.
            use_cache: Whether to use cached results.

        Returns:
            dict with overall_percentage, languages, content_types breakdown.
        """
        if use_cache:
            cached = cache.get(COVERAGE_CACHE_KEY)
            if cached is not None:
                return cached

        target_languages = self._get_target_languages(language_codes)
        if not target_languages:
            return {
                'overall_percentage': 0,
                'total_fields': 0,
                'translated_fields': 0,
                'languages': [],
                'content_types': [],
                'has_languages': False,
            }

        # Per-language totals
        lang_totals = {lang['code']: {'total': 0, 'translated': 0} for lang in target_languages}
        content_results = []

        # JSONField-based models
        for ct in get_all_content_types():
            result = self._calculate_jsonfield_coverage(ct, target_languages)
            if result:
                content_results.append(result)
                for lang in target_languages:
                    code = lang['code']
                    by_lang = result['by_language'].get(code, {})
                    lang_totals[code]['total'] += by_lang.get('total', 0)
                    lang_totals[code]['translated'] += by_lang.get('translated', 0)

        # Email templates
        email_result = self._calculate_email_coverage(target_languages)
        if email_result:
            content_results.append(email_result)
            for lang in target_languages:
                code = lang['code']
                by_lang = email_result['by_language'].get(code, {})
                lang_totals[code]['total'] += by_lang.get('total', 0)
                lang_totals[code]['translated'] += by_lang.get('translated', 0)

        # UI strings
        ui_result = self._calculate_ui_string_coverage(target_languages)
        if ui_result:
            content_results.append(ui_result)
            for lang in target_languages:
                code = lang['code']
                by_lang = ui_result['by_language'].get(code, {})
                lang_totals[code]['total'] += by_lang.get('total', 0)
                lang_totals[code]['translated'] += by_lang.get('translated', 0)

        # Aggregate
        grand_total = sum(lt['total'] for lt in lang_totals.values())
        grand_translated = sum(lt['translated'] for lt in lang_totals.values())
        overall_pct = round((grand_translated / grand_total * 100), 1) if grand_total > 0 else 0

        languages_summary = []
        for lang in target_languages:
            code = lang['code']
            lt = lang_totals[code]
            pct = round((lt['translated'] / lt['total'] * 100), 1) if lt['total'] > 0 else 0
            languages_summary.append({
                'code': code,
                'name': lang['name'],
                'flag': lang.get('flag', ''),
                'total': lt['total'],
                'translated': lt['translated'],
                'percentage': pct,
            })

        result = {
            'overall_percentage': overall_pct,
            'total_fields': grand_total,
            'translated_fields': grand_translated,
            'languages': languages_summary,
            'content_types': content_results,
            'has_languages': True,
        }

        if use_cache:
            cache.set(COVERAGE_CACHE_KEY, result, COVERAGE_CACHE_TTL)

        return result

    def _get_target_languages(self, language_codes=None):
        """Get active non-default SiteLanguages as dicts."""
        from .models import SiteLanguage

        qs = SiteLanguage.objects.filter(is_active=True, is_default=False)
        if language_codes:
            qs = qs.filter(code__in=language_codes)

        return [
            {'code': sl.code, 'name': sl.name, 'flag': sl.flag}
            for sl in qs.order_by('order', 'name')
        ]

    def _calculate_jsonfield_coverage(self, ct_entry, target_languages):
        """
        Calculate coverage for a model with translations JSONField.

        Handles both nested format ({"es": {"name": "Nombre"}})
        and simple format ({"es": "Tamaño"}).
        """
        model_class = get_model_class(ct_entry['key'])
        if model_class is None:
            return None

        fields = ct_entry['fields']
        is_simple = ct_entry.get('format') == 'simple'

        # Build the list of source field names to check for content
        source_field_names = []
        for f in fields:
            try:
                model_class._meta.get_field(f)
                source_field_names.append(f)
            except Exception:
                source_field_names.append(None)

        # Query all instances with translations + source fields
        try:
            qs = model_class.objects.all()
            values_fields = ['pk', 'translations'] + [f for f in source_field_names if f]
            rows = list(qs.values_list(*values_fields))
        except Exception as e:
            logger.warning(f"Coverage: failed to query {ct_entry['key']}: {e}")
            return None

        if not rows:
            return {
                'key': ct_entry['key'],
                'label': ct_entry['label'],
                'icon': ct_entry['icon'],
                'priority': ct_entry['priority'],
                'item_count': 0,
                'total_fields': 0,
                'translated_fields': 0,
                'percentage': 0,
                'by_language': {lang['code']: {'total': 0, 'translated': 0, 'pct': 0} for lang in target_languages},
            }

        by_language = {lang['code']: {'total': 0, 'translated': 0} for lang in target_languages}

        for row in rows:
            pk = row[0]
            translations = row[1] or {}
            # Source field values start at index 2
            source_values = row[2:]

            for field_idx, field_name in enumerate(fields):
                # Get source value — check if this field has content
                src_field_idx = source_field_names.index(field_name) if field_name in source_field_names else None
                if src_field_idx is not None:
                    # offset by the pk and translations columns
                    val_idx = src_field_idx  # index within source_values
                    source_val = source_values[val_idx] if val_idx < len(source_values) else None
                else:
                    source_val = None

                # Skip fields with no source content
                if not source_val:
                    continue

                for lang in target_languages:
                    code = lang['code']
                    by_language[code]['total'] += 1

                    if is_simple:
                        # Simple format: translations[lang] is the value directly
                        trans_val = translations.get(code)
                        if trans_val and isinstance(trans_val, str) and trans_val.strip():
                            by_language[code]['translated'] += 1
                    else:
                        # Nested format: translations[lang][field]
                        lang_data = translations.get(code)
                        if isinstance(lang_data, dict):
                            trans_val = lang_data.get(field_name)
                            if trans_val and isinstance(trans_val, str) and trans_val.strip():
                                by_language[code]['translated'] += 1

        # Aggregate across languages
        total_fields = sum(bl['total'] for bl in by_language.values())
        translated_fields = sum(bl['translated'] for bl in by_language.values())
        pct = round((translated_fields / total_fields * 100), 1) if total_fields > 0 else 0

        # Per-language percentages
        for code in by_language:
            bl = by_language[code]
            bl['pct'] = round((bl['translated'] / bl['total'] * 100), 1) if bl['total'] > 0 else 0

        return {
            'key': ct_entry['key'],
            'label': ct_entry['label'],
            'icon': ct_entry['icon'],
            'priority': ct_entry['priority'],
            'item_count': len(rows),
            'total_fields': total_fields,
            'translated_fields': translated_fields,
            'percentage': pct,
            'by_language': by_language,
        }

    def _calculate_email_coverage(self, target_languages):
        """
        Calculate coverage for email templates.

        Email templates use a separate model (EmailTemplateTranslation)
        rather than a JSONField.
        """
        try:
            EmailTemplate = apps.get_model('email_system', 'EmailTemplate')
            EmailTemplateTranslation = apps.get_model('email_system', 'EmailTemplateTranslation')
        except LookupError:
            return None

        # Get active system English templates (base templates)
        base_templates = list(
            EmailTemplate.objects.filter(
                is_system=True, is_active=True, language_code='en'
            ).values_list('pk', flat=True)
        )

        if not base_templates:
            return {
                'key': 'email_system.emailtemplate',
                'label': 'Email Templates',
                'icon': 'fas fa-envelope',
                'priority': 2,
                'item_count': 0,
                'total_fields': 0,
                'translated_fields': 0,
                'percentage': 0,
                'by_language': {lang['code']: {'total': 0, 'translated': 0, 'pct': 0} for lang in target_languages},
            }

        # For each language, check which base templates have translations
        existing_translations = set(
            EmailTemplateTranslation.objects.filter(
                template_id__in=base_templates
            ).values_list('template_id', 'language_code')
        )

        by_language = {}
        for lang in target_languages:
            code = lang['code']
            total = len(base_templates)
            translated = sum(
                1 for tid in base_templates
                if (tid, code) in existing_translations
            )
            by_language[code] = {
                'total': total,
                'translated': translated,
                'pct': round((translated / total * 100), 1) if total > 0 else 0,
            }

        total_fields = sum(bl['total'] for bl in by_language.values())
        translated_fields = sum(bl['translated'] for bl in by_language.values())
        pct = round((translated_fields / total_fields * 100), 1) if total_fields > 0 else 0

        return {
            'key': 'email_system.emailtemplate',
            'label': 'Email Templates',
            'icon': 'fas fa-envelope',
            'priority': 2,
            'item_count': len(base_templates),
            'total_fields': total_fields,
            'translated_fields': translated_fields,
            'percentage': pct,
            'by_language': by_language,
        }

    def _calculate_ui_string_coverage(self, target_languages):
        """
        Calculate coverage for UI storefront strings.

        For built-in languages (those with .po files): counts strings covered
        by either a merchant override OR a .po translation.
        For non-builtin languages: counts only merchant overrides.
        """
        from .models import UITranslationOverride
        from .ui_string_registry import get_total_string_count, UI_STRING_REGISTRY
        from .templatetags.merchant_trans import BUILTIN_LANGUAGES

        total_strings = get_total_string_count()
        if total_strings == 0:
            return None

        overrides = {
            o.language.code: o
            for o in UITranslationOverride.objects.select_related('language').all()
        }

        by_language = {}
        for lang in target_languages:
            code = lang['code']
            override = overrides.get(code)

            if code in BUILTIN_LANGUAGES and code != 'en':
                translated = self._count_effective_ui_coverage(
                    code, override, UI_STRING_REGISTRY
                )
            else:
                translated = override.translated_count if override else 0

            by_language[code] = {
                'total': total_strings,
                'translated': translated,
                'pct': round((translated / total_strings * 100), 1) if total_strings > 0 else 0,
            }

        total_fields = sum(bl['total'] for bl in by_language.values())
        translated_fields = sum(bl['translated'] for bl in by_language.values())
        pct = round((translated_fields / total_fields * 100), 1) if total_fields > 0 else 0

        return {
            'key': 'translations.uistrings',
            'label': 'UI Strings',
            'icon': 'fas fa-font',
            'priority': 2,
            'item_count': total_strings,
            'total_fields': total_fields,
            'translated_fields': translated_fields,
            'percentage': pct,
            'by_language': by_language,
        }

    def _count_effective_ui_coverage(self, language_code, override_obj, registry):
        """
        For a built-in language, count UI strings covered by either
        a merchant override OR a .po translation.
        """
        from django.utils.translation import override as translation_override
        from django.utils.translation import gettext

        override_keys = set()
        if override_obj and override_obj.overrides:
            override_keys = {k for k, v in override_obj.overrides.items() if v}

        count = 0
        with translation_override(language_code):
            for key, english_source in registry.items():
                if key in override_keys:
                    count += 1
                    continue
                po_val = gettext(english_source)
                if po_val and po_val != english_source:
                    count += 1
        return count


def invalidate_coverage_cache():
    """Invalidate the coverage cache. Call after translations are saved."""
    cache.delete(COVERAGE_CACHE_KEY)
