"""
Custom set_language view that supports any active SiteLanguage,
not just those in settings.LANGUAGES.
"""

import re
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

# Matches a language prefix like /en/, /es/, /zh-hans/ at the start of a path.
_LANG_PREFIX_RE = re.compile(r"^/([a-z]{2,3}(?:-[a-z]{1,8})*)/(.*)$", re.IGNORECASE)


@csrf_protect
@require_POST
def merchant_set_language(request):
    """
    Set the user's language preference.

    Like Django's set_language but also accepts language codes from
    SiteLanguage records (not just settings.LANGUAGES).
    """
    next_url = request.POST.get("next", request.GET.get("next"))
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get("HTTP_REFERER")
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = "/"

    lang_code = request.POST.get("language")

    # Check if language is valid: either in LANGUAGES or in active SiteLanguage
    if lang_code and _is_valid_language(lang_code):
        # Ensure it's in settings.LANGUAGES for Django's URL resolver
        _ensure_in_settings_languages(lang_code)

        # Activate the language
        activate(lang_code)

        # Translate the URL to the new language
        original_url = next_url
        next_url = translate_url(next_url, lang_code)

        # Fallback: if translate_url returned the URL unchanged, manually
        # swap the language prefix. This covers cases where the URL resolver
        # cannot reverse the current path.
        if next_url == original_url:
            next_url = _swap_language_prefix(next_url, lang_code)

        response = HttpResponseRedirect(next_url)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE or 365 * 24 * 60 * 60,
            path=settings.LANGUAGE_COOKIE_PATH or "/",
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE or "Lax",
        )

        return response

    return HttpResponseRedirect(next_url)


def _ensure_in_settings_languages(lang_code):
    """Ensure the language code is in settings.LANGUAGES for Django's resolver."""
    existing_codes = {code for code, _ in settings.LANGUAGES}
    if lang_code not in existing_codes:
        from translations.models import SiteLanguage

        try:
            sl = SiteLanguage.objects.get(code=lang_code, is_active=True)
            settings.LANGUAGES.append((sl.code, sl.name))
        except SiteLanguage.DoesNotExist:
            pass


def _swap_language_prefix(url, lang_code):
    """
    Replace the language prefix in a URL path with the given language code.

    Falls back to prepending the language prefix if none is found.
    Preserves query strings and fragments.
    """
    parsed = urlsplit(url)
    path = parsed.path

    known_codes = {code.lower() for code, _ in settings.LANGUAGES}

    match = _LANG_PREFIX_RE.match(path)
    if match:
        existing_code = match.group(1).lower()
        rest = match.group(2)
        if existing_code in known_codes or existing_code == lang_code.lower():
            new_path = f"/{lang_code}/{rest}"
        else:
            new_path = f"/{lang_code}{path}"
    else:
        # No language prefix found; prepend one (with or without extra slash)
        new_path = f"/{lang_code}{path}" if path.startswith("/") else f"/{lang_code}/{path}"

    return urlunsplit((parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment))


def _is_valid_language(lang_code):
    """Check if a language code is valid (in LANGUAGES or active SiteLanguage)."""
    # Check settings.LANGUAGES first
    for code, _ in settings.LANGUAGES:
        if code == lang_code:
            return True

    # Check active SiteLanguage records
    try:
        from translations.models import SiteLanguage

        return SiteLanguage.objects.filter(code=lang_code, is_active=True).exists()
    except Exception:
        return False
