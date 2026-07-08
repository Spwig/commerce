"""
Language Pack installer/uninstaller.

Handles installing and uninstalling language packs which deliver:
- Django .po/.mo files for admin interface translations ({% trans %} / _())
- UI string translations for frontend ({% mtrans %} via UITranslationOverride)
- Help content .md files
- SiteLanguage metadata

Language packs are distributed as ZIP archives via the update server
and follow the same component lifecycle as themes, utilities, and providers.
"""

import json
import logging
import os
import re
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from .installers import InstallError

# Built-in language codes that ship with the platform.  Language packs must
# NOT overwrite these — they have baked-in .po/.mo files maintained in-repo.
_BUILTIN_LANGUAGE_CODES = frozenset(
    code for code, _ in getattr(settings, '_BUILTIN_LANGUAGES', settings.LANGUAGES)
)

logger = logging.getLogger(__name__)

# Path to the JSON config that extends settings.LANGUAGES at startup.
# Written atomically by the installer; read by core/settings.py.
LANGUAGE_PACKS_CONFIG = Path(settings.BASE_DIR) / 'installed_language_packs.json'

# All apps that can have locale directories — mirrors the list in
# settings.get_locale_paths() so we know where to copy .po/.mo files.
LOCALE_APP_NAMES = [
    'core', 'design', 'page_builder', 'accounts', 'catalog',
    'cart', 'orders', 'shipping', 'payment_providers', 'management',
    'media_library', 'setup_wizard', 'customers', 'vouchers',
    'address_autocomplete', 'affiliate', 'announcements', 'blog',
    'component_updates', 'configurator_3d', 'custom_fields',
    'developer_portal', 'element_builder', 'email_system',
    'exchange_rates', 'form_builder', 'geoip', 'loyalty',
    'license_checkout', 'marketplace', 'marketplace_checkout', 'migration',
    'payout_providers', 'pos_app', 'product_feeds', 'referrals',
    'search', 'seo_generator', 'sms_system', 'social_sharing',
    'staff_roles', 'subscriptions', 'translations', 'webhooks',
    'domain_ssl',
]


def install_language_pack(extract_dir: Path, manifest: dict) -> dict:
    """
    Install a language pack from an extracted directory.

    Args:
        extract_dir: Path to extracted package contents
        manifest: Parsed manifest.json dict (must include 'language_code')

    Returns:
        Dict with 'success', 'language_code', 'version', and optional 'error' keys
    """
    language_code = manifest.get('language_code')
    version = manifest.get('version', '1.0.0')
    slug = manifest.get('slug', f'language-pack-{language_code}')

    if not language_code:
        return {'success': False, 'error': 'manifest.json missing language_code'}

    if language_code in _BUILTIN_LANGUAGE_CODES:
        return {
            'success': False,
            'error': (
                f"Language '{language_code}' is a built-in language. "
                f"Language packs are for adding new languages beyond the "
                f"{len(_BUILTIN_LANGUAGE_CODES)} shipped with the platform."
            ),
        }

    logger.info(f"Installing language pack: {slug} v{version} (lang={language_code})")

    # Track what we installed for rollback on failure
    installed_po_dirs = []
    installed_help_files = []

    try:
        # Use a transaction so DB changes (SiteLanguage, UITranslationOverride)
        # are rolled back automatically if any step fails.
        with transaction.atomic():
            # --- Step 1: Copy .po/.mo files ---
            locale_dir = extract_dir / 'locale'
            if locale_dir.is_dir():
                installed_po_dirs = _install_locale_files(locale_dir, language_code)
                logger.info(f"  Installed .po/.mo files for {len(installed_po_dirs)} apps")
            else:
                logger.warning("  No locale/ directory in language pack")

            # --- Step 2: Create/update SiteLanguage ---
            _install_site_language(extract_dir, language_code)

            # --- Step 3: Populate UITranslationOverride ---
            ui_strings_file = extract_dir / 'ui_strings.json'
            if ui_strings_file.exists():
                count = _install_ui_strings(ui_strings_file, language_code)
                logger.info(f"  Loaded {count} UI string translations")
            else:
                logger.warning("  No ui_strings.json in language pack")

            # --- Step 4: Install help content ---
            help_dir = extract_dir / 'help_content'
            if help_dir.is_dir():
                installed_help_files = _install_help_content(help_dir, language_code)
                logger.info(f"  Installed {len(installed_help_files)} help content files")

            # --- Step 5: Install email template translations ---
            email_dir = extract_dir / 'email_templates'
            if email_dir.is_dir():
                email_count = _install_email_templates(email_dir, language_code)
                logger.info(f"  Installed {email_count} email template translations")

            # --- Step 6: Update installed_language_packs.json ---
            meta_file = extract_dir / 'language_meta.json'
            lang_name = manifest.get('name', language_code)
            if meta_file.exists():
                with open(meta_file) as f:
                    meta = json.load(f)
                lang_name = meta.get('name', lang_name)

            _update_packs_config(language_code, lang_name, version, action='add')

            # --- Step 7: Invalidate caches ---
            cache.delete(f'ui_trans_overrides:{language_code}')

        logger.info(f"Language pack {slug} v{version} installed successfully")
        return {
            'success': True,
            'language_code': language_code,
            'version': version,
            'restart_required': True,
        }

    except Exception as e:
        logger.error(f"Language pack installation failed: {e}")
        # DB changes are rolled back by transaction.atomic().
        # Best-effort rollback of filesystem changes.
        _rollback_locale_files(installed_po_dirs)
        _rollback_help_files(installed_help_files)
        # Also rollback the config file if it was written before the error
        try:
            _update_packs_config(language_code, action='remove')
        except Exception as config_err:
            logger.warning(f"Rollback: could not clean config: {config_err}")
        return {
            'success': False,
            'language_code': language_code,
            'version': version,
            'error': str(e),
        }


def uninstall_language_pack(language_code: str) -> dict:
    """
    Uninstall a language pack.

    Removes .po/.mo files, deactivates SiteLanguage (preserves content),
    removes help files, and updates the config.

    Args:
        language_code: The language code to uninstall (e.g. 'sw')

    Returns:
        Dict with 'success' and optional 'error'
    """
    logger.info(f"Uninstalling language pack for: {language_code}")

    try:
        # --- Step 1: Remove .po/.mo files from all app locale dirs ---
        removed_dirs = _remove_locale_files(language_code)
        logger.info(f"  Removed locale dirs from {len(removed_dirs)} apps")

        # --- Step 2: Deactivate SiteLanguage (don't delete) ---
        _deactivate_site_language(language_code)

        # --- Step 3: Handle UITranslationOverride ---
        _remove_pack_ui_strings(language_code)

        # --- Step 4: Remove help content files ---
        removed_help = _remove_help_content(language_code)
        logger.info(f"  Removed {len(removed_help)} help content files")

        # --- Step 5: Remove email template translations ---
        removed_emails = _remove_pack_email_templates(language_code)
        logger.info(f"  Removed {removed_emails} email template translations")

        # --- Step 6: Update config ---
        _update_packs_config(language_code, action='remove')

        # --- Step 7: Invalidate caches ---
        cache.delete(f'ui_trans_overrides:{language_code}')

        logger.info(f"Language pack for {language_code} uninstalled")
        return {'success': True, 'language_code': language_code, 'restart_required': True}

    except Exception as e:
        logger.error(f"Language pack uninstall failed: {e}")
        return {'success': False, 'language_code': language_code, 'error': str(e)}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _install_locale_files(locale_dir: Path, language_code: str) -> list:
    """
    Copy .po/.mo files from the package's locale/ directory into each
    app's locale/{lang_code}/LC_MESSAGES/.

    The package organises locale files by app name:
        locale/catalog/sw/LC_MESSAGES/django.po
        locale/catalog/sw/LC_MESSAGES/django.mo

    Returns list of destination directories that were created/written to.
    """
    base_dir = Path(settings.BASE_DIR)
    installed = []
    # Allowed app names — whitelist prevents path traversal attacks
    allowed_apps = frozenset(LOCALE_APP_NAMES) | {'locale', 'page_builder_elements'}

    for app_dir in locale_dir.iterdir():
        if not app_dir.is_dir():
            continue
        app_name = app_dir.name

        if app_name not in allowed_apps:
            logger.warning(f"  Skipping unknown app '{app_name}' in language pack locale/")
            continue

        # Find the source LC_MESSAGES directory
        src_lc = app_dir / language_code / 'LC_MESSAGES'
        if not src_lc.is_dir():
            continue

        # Determine destination based on app type
        if app_name == 'page_builder_elements':
            # Page builder element locales are nested
            _install_element_locales(app_dir / language_code, language_code, installed)
            continue

        if app_name == 'locale':
            # Global locale directory
            dest_locale = base_dir / 'locale' / language_code / 'LC_MESSAGES'
        else:
            # Standard app locale directory
            dest_locale = base_dir / app_name / 'locale' / language_code / 'LC_MESSAGES'

        # Verify destination is under BASE_DIR (belt-and-suspenders)
        try:
            dest_locale.resolve().relative_to(base_dir.resolve())
        except ValueError:
            logger.warning(f"  Skipping {app_name}: destination outside project directory")
            continue

        if app_name != 'locale' and not (base_dir / app_name).is_dir():
            logger.debug(f"  Skipping {app_name}: app directory not found")
            continue

        dest_locale.mkdir(parents=True, exist_ok=True)

        for src_file in src_lc.iterdir():
            if src_file.is_file() and src_file.suffix in ('.po', '.mo'):
                shutil.copy2(src_file, dest_locale / src_file.name)

        installed.append(str(dest_locale))

    return installed


def _install_element_locales(elements_lang_dir: Path, language_code: str, installed: list):
    """
    Install locale files for page builder elements.

    Package structure:
        locale/page_builder_elements/{lang}/hero/LC_MESSAGES/django.{po,mo}

    Destination:
        page_builder/templates/page_builder/elements/hero/locale/{lang}/LC_MESSAGES/
    """
    base_dir = Path(settings.BASE_DIR)
    elements_base = base_dir / 'page_builder' / 'templates' / 'page_builder' / 'elements'

    for element_dir in elements_lang_dir.iterdir():
        if not element_dir.is_dir():
            continue
        element_name = element_dir.name
        src_lc = element_dir / 'LC_MESSAGES'
        if not src_lc.is_dir():
            continue

        dest_element = elements_base / element_name / 'locale' / language_code / 'LC_MESSAGES'
        if not (elements_base / element_name).is_dir():
            logger.debug(f"  Skipping element {element_name}: not found")
            continue

        dest_element.mkdir(parents=True, exist_ok=True)
        for src_file in src_lc.iterdir():
            if src_file.is_file() and src_file.suffix in ('.po', '.mo'):
                shutil.copy2(src_file, dest_element / src_file.name)

        installed.append(str(dest_element))


def _install_site_language(extract_dir: Path, language_code: str):
    """Create or update the SiteLanguage record from language_meta.json."""
    from translations.models import SiteLanguage

    meta_file = extract_dir / 'language_meta.json'
    if not meta_file.exists():
        logger.warning("No language_meta.json — creating minimal SiteLanguage")
        SiteLanguage.objects.update_or_create(
            code=language_code,
            defaults={'is_active': True}
        )
        return

    with open(meta_file) as f:
        meta = json.load(f)

    defaults = {
        'name': meta.get('name', language_code),
        'native_name': meta.get('native_name', meta.get('name', language_code)),
        'is_active': True,
        'rtl': meta.get('rtl', False),
        'flag': meta.get('flag', ''),
    }

    # Optional fields
    for field in ('date_format', 'time_format', 'm2m100_support', 'nllb_support', 'requires_nllb'):
        if field in meta:
            defaults[field] = meta[field]

    SiteLanguage.objects.update_or_create(
        code=language_code,
        defaults=defaults,
    )
    logger.info(f"  SiteLanguage '{language_code}' created/updated")


def _install_ui_strings(ui_strings_file: Path, language_code: str) -> int:
    """
    Populate UITranslationOverride from ui_strings.json.

    Merges with existing merchant customizations — pack strings only fill
    empty slots; merchant-edited overrides are preserved.

    Returns the number of strings loaded from the pack.
    """
    from translations.models import SiteLanguage, UITranslationOverride
    from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count

    with open(ui_strings_file) as f:
        data = json.load(f)

    pack_strings = data.get('strings', {})
    if not pack_strings:
        return 0

    site_lang = SiteLanguage.objects.filter(code=language_code).first()
    if not site_lang:
        raise InstallError(f"SiteLanguage '{language_code}' not found — install language_meta first")

    override, created = UITranslationOverride.objects.get_or_create(
        language=site_lang,
        defaults={'total_strings': get_total_string_count()}
    )

    existing_overrides = override.overrides or {}
    existing_meta = override.meta_info or {}
    now_str = timezone.now().isoformat()
    loaded = 0

    for string_key, translated_text in pack_strings.items():
        if string_key not in UI_STRING_REGISTRY:
            continue  # Skip keys that don't exist in current platform version
        if not translated_text:
            continue

        # Preserve merchant customizations: only fill if empty or from a previous pack
        existing_value = existing_overrides.get(string_key)
        existing_source = (existing_meta.get(string_key) or {}).get('source')

        if not existing_value or existing_source == 'language_pack':
            existing_overrides[string_key] = translated_text
            existing_meta[string_key] = {
                'auto': False,
                'verified': True,
                'source': 'language_pack',
                'translated_at': now_str,
            }
            loaded += 1

    override.overrides = existing_overrides
    override.meta_info = existing_meta
    override.total_strings = get_total_string_count()
    override.translated_count = sum(1 for v in existing_overrides.values() if v)
    override.verified_count = sum(
        1 for m in existing_meta.values() if m.get('verified')
    )
    override.save()

    return loaded


def _install_help_content(help_dir: Path, language_code: str) -> list:
    """
    Copy translated help .md files into the help_content/ directory.

    Returns list of installed file paths.
    """
    base_help = Path(settings.BASE_DIR) / 'help_content'
    installed = []

    for src_file in help_dir.rglob(f'*.{language_code}.md'):
        # Preserve directory structure (e.g. topics/migration/full-system-migration.sw.md)
        relative = src_file.relative_to(help_dir)
        dest = base_help / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest)
        installed.append(str(dest))

    # Also look for files using hyphenated codes (e.g. zh-hans)
    hyphen_code = language_code.replace('_', '-')
    if hyphen_code != language_code:
        for src_file in help_dir.rglob(f'*.{hyphen_code}.md'):
            relative = src_file.relative_to(help_dir)
            dest = base_help / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest)
            installed.append(str(dest))

    return installed


def _parse_email_template_md(filepath: Path) -> dict:
    """
    Parse an email template markdown file.

    Returns dict with: template_type, category, subject, html_content, text_content.
    Returns dict with 'error' key on failure.
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return {'error': f'Failed to read file: {e}'}

    result = {}

    # Extract YAML frontmatter
    yaml_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if yaml_match:
        frontmatter = yaml_match.group(1)
        type_match = re.search(r'template_type:\s*(.+)', frontmatter)
        if type_match:
            result['template_type'] = type_match.group(1).strip()
        cat_match = re.search(r'category:\s*(.+)', frontmatter)
        if cat_match:
            result['category'] = cat_match.group(1).strip()
    else:
        return {'error': 'Missing YAML frontmatter'}

    # Extract subject
    subject_match = re.search(
        r'## Subject\s*\n(.+?)(?=\n\n|\n##)', content, re.DOTALL
    )
    if subject_match:
        result['subject'] = subject_match.group(1).strip()
    else:
        return {'error': 'Missing ## Subject section'}

    # Extract HTML content
    html_match = re.search(
        r'## HTML Content\s*\n(.+?)(?=\n## (?:Text Content|Variables|Notes)|$)',
        content, re.DOTALL,
    )
    if html_match:
        result['html_content'] = html_match.group(1).strip()
    else:
        return {'error': 'Missing ## HTML Content section'}

    # Extract text content (optional)
    text_match = re.search(
        r'## Text Content\s*\n(.+?)(?=\n## (?:Variables|Notes)|$)',
        content, re.DOTALL,
    )
    result['text_content'] = text_match.group(1).strip() if text_match else ''

    return result


def _install_email_templates(email_dir: Path, language_code: str) -> int:
    """
    Install email template translations from the language pack.

    The pack's email_templates/ directory contains translated markdown files
    following the same format as email_templates_for_translation/:
        email_templates/{template_name}.{lang_code}.md

    For each file, we parse the markdown and create/update an
    EmailTemplateTranslation record linked to the matching English
    base EmailTemplate.

    Returns the number of templates installed.
    """
    from django.contrib.sites.models import Site
    from email_system.models import EmailTemplate, EmailTemplateTranslation

    site = Site.objects.get(pk=1)
    installed = 0

    # Find all markdown files for this language code
    patterns = [f'*.{language_code}.md']
    hyphen_code = language_code.replace('_', '-')
    if hyphen_code != language_code:
        patterns.append(f'*.{hyphen_code}.md')

    for pattern in patterns:
        for md_file in email_dir.glob(pattern):
            parsed = _parse_email_template_md(md_file)
            if 'error' in parsed:
                logger.warning(
                    f"  Skipping {md_file.name}: {parsed['error']}"
                )
                continue

            template_type = parsed.get('template_type')
            if not template_type:
                logger.warning(f"  Skipping {md_file.name}: no template_type")
                continue

            # Find the English base template
            base_template = EmailTemplate.objects.filter(
                site=site,
                template_type=template_type,
                language_code='en',
                is_system=True,
                is_active=True,
            ).first()

            if not base_template:
                logger.debug(
                    f"  Skipping {md_file.name}: no base template "
                    f"for type '{template_type}'"
                )
                continue

            # Create or update the translation record.
            # Only fill slots that aren't already merchant-customized.
            existing = EmailTemplateTranslation.objects.filter(
                template=base_template,
                language_code=language_code,
            ).first()

            if existing and existing.translation_job_id:
                # Translation was created by merchant's AI translation job —
                # don't overwrite their customization.
                logger.debug(
                    f"  Skipping {md_file.name}: merchant translation exists"
                )
                continue

            EmailTemplateTranslation.objects.update_or_create(
                template=base_template,
                language_code=language_code,
                defaults={
                    'subject': parsed['subject'],
                    'html_content': parsed['html_content'],
                    'text_content': parsed.get('text_content', ''),
                    'base_template_version': base_template.version,
                    'is_verified': True,
                    'quality_score': 1.0,
                },
            )
            installed += 1

    return installed


def _update_packs_config(language_code: str, name: str = '', version: str = '', action: str = 'add'):
    """
    Atomically update installed_language_packs.json.

    Uses write-to-temp-then-rename for atomic updates.
    """
    data = {'packs': {}}
    if LANGUAGE_PACKS_CONFIG.exists():
        try:
            with open(LANGUAGE_PACKS_CONFIG) as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {'packs': {}}

    if action == 'add':
        data['packs'][language_code] = {
            'name': name,
            'version': version,
            'installed_at': timezone.now().isoformat(),
        }
    elif action == 'remove':
        data['packs'].pop(language_code, None)

    # Atomic write: write to temp file, then rename
    fd, tmp_path = tempfile.mkstemp(
        dir=str(LANGUAGE_PACKS_CONFIG.parent),
        suffix='.json.tmp',
    )
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, str(LANGUAGE_PACKS_CONFIG))
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Uninstall helpers
# ---------------------------------------------------------------------------

def _remove_locale_files(language_code: str) -> list:
    """Remove {lang_code}/LC_MESSAGES/ dirs from all app locale directories."""
    base_dir = Path(settings.BASE_DIR)
    removed = []

    for app_name in LOCALE_APP_NAMES:
        lc_dir = base_dir / app_name / 'locale' / language_code
        if lc_dir.is_dir():
            shutil.rmtree(lc_dir)
            removed.append(str(lc_dir))

    # Also remove from page builder elements
    elements_base = base_dir / 'page_builder' / 'templates' / 'page_builder' / 'elements'
    if elements_base.is_dir():
        for element_dir in elements_base.iterdir():
            if element_dir.is_dir():
                lang_dir = element_dir / 'locale' / language_code
                if lang_dir.is_dir():
                    shutil.rmtree(lang_dir)
                    removed.append(str(lang_dir))

    # Global locale directory
    global_lang = base_dir / 'locale' / language_code
    if global_lang.is_dir():
        shutil.rmtree(global_lang)
        removed.append(str(global_lang))

    return removed


def _deactivate_site_language(language_code: str):
    """Deactivate the SiteLanguage record (preserve for content references)."""
    from translations.models import SiteLanguage
    SiteLanguage.objects.filter(code=language_code).update(is_active=False)
    logger.info(f"  SiteLanguage '{language_code}' deactivated")


def _remove_pack_ui_strings(language_code: str):
    """
    Remove UI strings that were installed by the language pack.

    Only removes strings with source='language_pack' in meta_info.
    Merchant-edited strings are preserved.
    """
    from translations.models import SiteLanguage, UITranslationOverride

    site_lang = SiteLanguage.objects.filter(code=language_code).first()
    if not site_lang:
        return

    try:
        override = UITranslationOverride.objects.get(language=site_lang)
    except UITranslationOverride.DoesNotExist:
        return

    overrides = override.overrides or {}
    meta = override.meta_info or {}
    keys_to_remove = []

    for key, meta_entry in meta.items():
        if isinstance(meta_entry, dict) and meta_entry.get('source') == 'language_pack':
            keys_to_remove.append(key)

    for key in keys_to_remove:
        overrides.pop(key, None)
        meta.pop(key, None)

    override.overrides = overrides
    override.meta_info = meta
    override.translated_count = sum(1 for v in overrides.values() if v)
    override.verified_count = sum(1 for m in meta.values() if isinstance(m, dict) and m.get('verified'))
    override.save()

    logger.info(f"  Removed {len(keys_to_remove)} pack UI strings (preserved merchant edits)")


def _remove_help_content(language_code: str) -> list:
    """Remove translated help .md files for the given language."""
    help_base = Path(settings.BASE_DIR) / 'help_content'
    removed = []

    if not help_base.is_dir():
        return removed

    # Match both underscore and hyphen variants
    patterns = [f'*.{language_code}.md']
    hyphen_code = language_code.replace('_', '-')
    if hyphen_code != language_code:
        patterns.append(f'*.{hyphen_code}.md')

    for pattern in patterns:
        for md_file in help_base.rglob(pattern):
            md_file.unlink()
            removed.append(str(md_file))

    return removed


def _remove_pack_email_templates(language_code: str) -> int:
    """
    Remove email template translations installed by a language pack.

    Only removes translations that were NOT created by a merchant's AI
    translation job (i.e. those with translation_job=None and is_verified=True
    and quality_score=1.0, which is the signature of a language pack import).
    """
    from email_system.models import EmailTemplateTranslation

    deleted_count, _ = EmailTemplateTranslation.objects.filter(
        language_code=language_code,
        translation_job__isnull=True,
        is_verified=True,
        quality_score=1.0,
    ).delete()

    return deleted_count


# ---------------------------------------------------------------------------
# Rollback helpers (used on installation failure)
# ---------------------------------------------------------------------------

def _rollback_locale_files(installed_dirs: list):
    """Remove .po/.mo files that were just installed."""
    for dir_path in installed_dirs:
        try:
            p = Path(dir_path)
            if p.is_dir():
                shutil.rmtree(p)
        except Exception as e:
            logger.warning(f"Rollback: could not remove {dir_path}: {e}")


def _rollback_help_files(installed_files: list):
    """Remove help .md files that were just installed."""
    for file_path in installed_files:
        try:
            p = Path(file_path)
            if p.is_file():
                p.unlink()
        except Exception as e:
            logger.warning(f"Rollback: could not remove {file_path}: {e}")
