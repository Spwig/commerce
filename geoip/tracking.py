"""
Shared visitor tracking utility.

Used by both the GeoIP middleware (direct Django page views) and
the resolve_location() API view (headless frontend page views).
"""

import logging
import re
from urllib.parse import urlparse

from user_agents import parse as parse_user_agent

from .models import PageView, VisitorLocation

logger = logging.getLogger(__name__)

# Known bot user-agent substrings (lowercase).
# Shared single source of truth — middleware references this too.
BOT_UA_PATTERNS = (
    "bot",
    "crawl",
    "spider",
    "slurp",
    "scraper",
    "headlesschrome",
    "phantomjs",
    "selenium",
    "puppeteer",
    "playwright",
    "wget",
    "curl",
    "python-requests",
    "python-urllib",
    "httpx",
    "aiohttp",
    "go-http-client",
    "java/",
    "libwww",
    "okhttp",
    "googlebot",
    "bingbot",
    "yandexbot",
    "baiduspider",
    "facebookexternalhit",
    "twitterbot",
    "linkedinbot",
    "whatsapp",
    "telegrambot",
    "discordbot",
    "applebot",
    "duckduckbot",
    "semrushbot",
    "ahrefsbot",
    "mj12bot",
    "dotbot",
    "petalbot",
    "bytespider",
    "zgrab",
    "masscan",
    "nikto",
    "censys",
    "shodan",
    "nmap",
    "sqlmap",
    "nuclei",
)

# Regex to strip locale prefix from URL paths (e.g., /en/, /zh-hans/)
_LOCALE_PREFIX_RE = re.compile(r"^/[a-z]{2}(?:-[a-z]+)?/")


def detect_bot(user_agent_string: str) -> bool:
    """Return True if the user-agent looks like a bot or automated tool."""
    if not user_agent_string:
        return True  # No UA = treat as bot
    ua_lower = user_agent_string.lower()
    return any(pattern in ua_lower for pattern in BOT_UA_PATTERNS)


def detect_device_type(user_agent_string: str) -> str:
    """Return 'desktop', 'mobile', 'tablet', or 'unknown'."""
    if not user_agent_string:
        return "unknown"
    try:
        ua = parse_user_agent(user_agent_string)
        if ua.is_mobile:
            return "mobile"
        if ua.is_tablet:
            return "tablet"
        if ua.is_pc:
            return "desktop"
    except Exception:
        pass
    return "unknown"


def normalize_url_path(url: str) -> str:
    """
    Strip locale prefix and query parameters to get a canonical path.

    Examples:
        /en/pricing?utm_source=google  →  /pricing
        /fr/features/                  →  /features/
        /zh-hans/about/                →  /about/
        /pricing                       →  /pricing
        /                              →  /
    """
    # Strip query params
    path = urlparse(url).path if "?" in url or "#" in url else url

    # Strip locale prefix
    stripped = _LOCALE_PREFIX_RE.sub("/", path)

    return stripped or "/"


def track_page_view(request, page_url: str, source: str = "middleware"):
    """
    Create/update VisitorLocation and create a PageView record.

    Called from:
    - The resolve_location() API view with source='headless'
    - The GeoIP middleware with source='middleware'
    """
    try:
        # Ensure we have a session
        if not hasattr(request, "session"):
            return
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            if not session_key:
                return

        from .utils.ip_utils import get_client_ip

        ip = get_client_ip(request)
        if not ip:
            return

        user_agent_string = request.META.get("HTTP_USER_AGENT", "")
        is_bot = detect_bot(user_agent_string)
        device_type = detect_device_type(user_agent_string) if not is_bot else "unknown"

        # Build defaults for VisitorLocation
        defaults = {
            "ip_address": ip,
            "user_agent": user_agent_string,
            "accept_language": request.META.get("HTTP_ACCEPT_LANGUAGE", "")[:200],
            "device_type": device_type,
            "is_bot": is_bot,
            "is_admin_traffic": False,
        }

        # Capture UTM parameters (first-touch attribution)
        utm_source = request.GET.get("utm_source", "")
        utm_medium = request.GET.get("utm_medium", "")
        utm_campaign = request.GET.get("utm_campaign", "")
        utm_term = request.GET.get("utm_term", "")
        utm_content = request.GET.get("utm_content", "")
        referrer = request.META.get("HTTP_X_PAGE_REFERRER") or request.META.get("HTTP_REFERER", "")

        if utm_source:
            defaults["utm_source"] = utm_source[:255]
        if utm_medium:
            defaults["utm_medium"] = utm_medium[:255]
        if utm_campaign:
            defaults["utm_campaign"] = utm_campaign[:255]
        if utm_term:
            defaults["utm_term"] = utm_term[:255]
        if utm_content:
            defaults["utm_content"] = utm_content[:255]
        if referrer:
            defaults["referrer_url"] = referrer[:2048]

        # Get or create VisitorLocation
        visitor, created = VisitorLocation.objects.get_or_create(
            session_key=session_key,
            defaults=defaults,
        )

        updated_fields = []

        # Update with resolved geo location if available
        geo_location = getattr(request, "geo_location", None)
        if geo_location and isinstance(geo_location, dict):
            country = geo_location.get("country_code") or geo_location.get("country", "")
            region = geo_location.get("region_name", "")
            city = geo_location.get("city", "") or geo_location.get("city_name", "")
            if country and not visitor.resolved_country:
                visitor.resolved_country = country
                updated_fields.append("resolved_country")
            if region and not visitor.resolved_region:
                visitor.resolved_region = region
                updated_fields.append("resolved_region")
            if city and not visitor.resolved_city:
                visitor.resolved_city = city
                updated_fields.append("resolved_city")

        if not created:
            visitor.page_views += 1
            updated_fields.extend(["page_views", "last_seen"])
            if visitor.ip_address != ip:
                visitor.ip_address = ip
                updated_fields.append("ip_address")
            if is_bot and not visitor.is_bot:
                visitor.is_bot = True
                updated_fields.append("is_bot")

        if updated_fields:
            visitor.save(update_fields=updated_fields if not created else None)

        # Determine if this is the first page view in this session
        is_entry = created  # New session = entry page

        # Create PageView record
        url_path = normalize_url_path(page_url)
        PageView.objects.create(
            visitor=visitor,
            session_key=session_key,
            url=page_url[:2048],
            url_path=url_path,
            referrer=referrer[:2048] if referrer else "",
            is_entry_page=is_entry,
            is_bot=is_bot,
            source=source,
        )

    except Exception as e:
        logger.error(f"Failed to track page view: {e}")
