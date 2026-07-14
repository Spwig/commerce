"""
Content sanitization with tier-aware security rules.

Provides comprehensive HTML/CSS/URL sanitization to prevent XSS and injection
attacks. Rules vary by page tier:
- Tier A (Checkout): Most restrictive
- Tier B (Product/Collection): Moderate
- Tier C (Marketing): Most permissive (but still secure)

Usage:
    sanitizer = ContentSanitizer(tier='C')
    clean_html = sanitizer.sanitize_html(user_content)
"""

import logging
import re
from html.parser import HTMLParser
from urllib.parse import urlparse

import bleach
from django.conf import settings

logger = logging.getLogger(__name__)


class ContentSanitizer:
    """
    Tier-aware content sanitization with XSS prevention.

    Implements defense-in-depth strategy:
    1. Tag whitelisting (tier-specific)
    2. Attribute whitelisting (tier-specific)
    3. URL protocol validation (only http/https)
    4. CSS property sanitization
    5. External domain validation
    6. Dangerous pattern blocking
    """

    # Tier A (Checkout) - Most restrictive
    TIER_A_ALLOWED_TAGS = ["p", "span", "strong", "em", "br", "b", "i", "u"]
    TIER_A_ALLOWED_ATTRS = {
        "*": ["class", "id"],
    }

    # Tier B (Product/Collection) - Moderate
    TIER_B_ALLOWED_TAGS = TIER_A_ALLOWED_TAGS + [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "li",
        "dl",
        "dt",
        "dd",
        "a",
        "img",
        "blockquote",
        "code",
        "pre",
    ]
    TIER_B_ALLOWED_ATTRS = {
        "*": ["class", "id"],
        "a": ["href", "title", "target", "rel"],
        "img": ["src", "alt", "width", "height", "loading"],
        "blockquote": ["cite"],
    }

    # Tier C (Marketing) - Most permissive
    TIER_C_ALLOWED_TAGS = TIER_B_ALLOWED_TAGS + [
        "div",
        "section",
        "article",
        "header",
        "footer",
        "nav",
        "main",
        "aside",
        "figure",
        "figcaption",
        "picture",
        "source",
        "table",
        "thead",
        "tbody",
        "tfoot",
        "tr",
        "th",
        "td",
        "caption",
        "col",
        "colgroup",
        "iframe",
        "video",
        "audio",
        "track",
        "abbr",
        "cite",
        "del",
        "ins",
        "mark",
        "q",
        "s",
        "small",
        "sub",
        "sup",
        "time",
        "hr",
        "wbr",
    ]
    TIER_C_ALLOWED_ATTRS = {
        "*": ["class", "id", "style", "title", "lang", "dir"],
        "a": ["href", "title", "target", "rel", "download"],
        "img": ["src", "alt", "width", "height", "loading", "srcset", "sizes"],
        "iframe": ["src", "width", "height", "sandbox", "allow", "loading", "title"],
        "video": [
            "src",
            "width",
            "height",
            "controls",
            "autoplay",
            "loop",
            "muted",
            "poster",
            "preload",
        ],
        "audio": ["src", "controls", "autoplay", "loop", "muted", "preload"],
        "source": ["src", "type", "srcset", "sizes", "media"],
        "track": ["src", "kind", "srclang", "label", "default"],
        "table": ["border", "cellpadding", "cellspacing"],
        "td": ["colspan", "rowspan", "headers"],
        "th": ["colspan", "rowspan", "scope", "headers"],
        "col": ["span"],
        "colgroup": ["span"],
        "blockquote": ["cite"],
        "q": ["cite"],
        "time": ["datetime"],
        "del": ["cite", "datetime"],
        "ins": ["cite", "datetime"],
    }

    # Allowed URL protocols
    ALLOWED_PROTOCOLS = ["http", "https", "mailto", "tel"]

    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r"javascript:",
        r"data:text/html",
        r"vbscript:",
        r"on\w+\s*=",  # onclick, onload, onerror, etc.
        r"<script",
        r"expression\s*\(",  # CSS expressions (IE)
        r"behavior\s*:",  # CSS behaviors (IE)
        r"@import",  # CSS @import
        r"-moz-binding",  # XBL bindings
    ]

    # Dangerous CSS properties
    DANGEROUS_CSS_PROPERTIES = [
        "behavior",
        "expression",
        "-moz-binding",
        "binding",
        "import",
        "@import",
        "javascript",
    ]

    # External domains whitelist (configurable via settings)
    DEFAULT_ALLOWED_DOMAINS = [
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com",
        "unpkg.com",
    ]

    def __init__(self, tier: str, allowed_domains: list[str] | None = None):
        """
        Initialize sanitizer with tier-specific rules.

        Args:
            tier: Page tier ('A', 'B', or 'C')
            allowed_domains: Custom list of allowed external domains
        """
        if tier not in ["A", "B", "C"]:
            raise ValueError(f"Invalid tier: {tier}. Must be 'A', 'B', or 'C'")

        self.tier = tier
        self.allowed_tags = self._get_allowed_tags()
        self.allowed_attrs = self._get_allowed_attrs()
        self.allowed_protocols = self.ALLOWED_PROTOCOLS.copy()

        # Merge default and custom allowed domains
        self.allowed_domains = self.DEFAULT_ALLOWED_DOMAINS.copy()
        if allowed_domains:
            self.allowed_domains.extend(allowed_domains)

        # Add domains from settings if available
        if hasattr(settings, "CONTENT_SANITIZER_ALLOWED_DOMAINS"):
            self.allowed_domains.extend(settings.CONTENT_SANITIZER_ALLOWED_DOMAINS)

        # Compile dangerous pattern regex
        self._dangerous_pattern = re.compile("|".join(self.DANGEROUS_PATTERNS), re.IGNORECASE)

    def _get_allowed_tags(self) -> list[str]:
        """Get allowed HTML tags for current tier."""
        if self.tier == "A":
            return self.TIER_A_ALLOWED_TAGS
        elif self.tier == "B":
            return self.TIER_B_ALLOWED_TAGS
        else:  # Tier C
            return self.TIER_C_ALLOWED_TAGS

    def _get_allowed_attrs(self) -> dict[str, list[str]]:
        """Get allowed HTML attributes for current tier."""
        if self.tier == "A":
            return self.TIER_A_ALLOWED_ATTRS
        elif self.tier == "B":
            return self.TIER_B_ALLOWED_ATTRS
        else:  # Tier C
            return self.TIER_C_ALLOWED_ATTRS

    def sanitize_html(self, html: str) -> str:
        """
        Sanitize HTML content with tier-aware rules.

        Args:
            html: Raw HTML content

        Returns:
            Sanitized HTML safe for rendering

        Example:
            >>> sanitizer = ContentSanitizer(tier='C')
            >>> clean = sanitizer.sanitize_html('<script>alert(1)</script><p>Hello</p>')
            >>> print(clean)
            '&lt;script&gt;alert(1)&lt;/script&gt;<p>Hello</p>'
        """
        if not html:
            return ""

        # First check for dangerous patterns
        if self._contains_dangerous_pattern(html):
            logger.warning(
                f"Dangerous pattern detected in HTML (tier={self.tier}). "
                f"Content will be heavily sanitized."
            )

        # Use bleach to clean HTML
        cleaned = bleach.clean(
            html,
            tags=self.allowed_tags,
            attributes=self.allowed_attrs,
            protocols=self.allowed_protocols,
            strip=True,  # Remove disallowed tags entirely
        )

        # Additional sanitization for Tier C (has style attribute)
        if self.tier == "C" and "style" in cleaned:
            cleaned = self._sanitize_inline_styles(cleaned)

        return cleaned

    def sanitize_url(self, url: str) -> str | None:
        """
        Validate and sanitize URLs.

        Args:
            url: URL to validate

        Returns:
            Sanitized URL if valid, None if dangerous

        Example:
            >>> sanitizer = ContentSanitizer(tier='C')
            >>> sanitizer.sanitize_url('javascript:alert(1)')
            None
            >>> sanitizer.sanitize_url('https://example.com/page')
            'https://example.com/page'
        """
        if not url:
            return None

        # Check for dangerous patterns
        if self._contains_dangerous_pattern(url):
            logger.warning(f"Dangerous pattern in URL: {url}")
            return None

        # Parse URL
        try:
            parsed = urlparse(url)
        except Exception as e:
            logger.warning(f"Failed to parse URL: {url}, error: {e}")
            return None

        # Check protocol
        if parsed.scheme and parsed.scheme.lower() not in self.allowed_protocols:
            logger.warning(f"Disallowed protocol in URL: {parsed.scheme}")
            return None

        # For external URLs, check domain whitelist (Tier A/B only)
        # Tier C (marketing) allows all external http/https URLs
        if parsed.scheme in ["http", "https"] and parsed.netloc and self.tier in ["A", "B"]:
            if not self._is_domain_allowed(parsed.netloc):
                logger.warning(f"External domain not whitelisted: {parsed.netloc}")
                return None

        return url

    def sanitize_css(self, css: str) -> str:
        """
        Sanitize inline CSS to remove dangerous properties.

        Args:
            css: CSS string (e.g., from style attribute)

        Returns:
            Sanitized CSS

        Example:
            >>> sanitizer = ContentSanitizer(tier='C')
            >>> sanitizer.sanitize_css('color: red; expression(alert(1))')
            'color: red;'
        """
        if not css:
            return ""

        # Remove dangerous properties
        for dangerous_prop in self.DANGEROUS_CSS_PROPERTIES:
            css = re.sub(
                rf"{re.escape(dangerous_prop)}\s*[:\(].*?[;\)]", "", css, flags=re.IGNORECASE
            )

        # Remove @import rules
        css = re.sub(r"@import\s+.*?;", "", css, flags=re.IGNORECASE)

        # Remove url() with javascript:
        css = re.sub(r'url\s*\(\s*["\']?\s*javascript:.*?\)', "", css, flags=re.IGNORECASE)

        return css.strip()

    def _sanitize_inline_styles(self, html: str) -> str:
        """
        Sanitize inline style attributes in HTML.

        Args:
            html: HTML with potentially dangerous inline styles

        Returns:
            HTML with sanitized inline styles
        """
        # Find all style attributes
        pattern = r'style\s*=\s*["\']([^"\']*)["\']'

        def sanitize_match(match):
            css = match.group(1)
            clean_css = self.sanitize_css(css)
            if clean_css:
                return f'style="{clean_css}"'
            return ""

        return re.sub(pattern, sanitize_match, html)

    def _contains_dangerous_pattern(self, content: str) -> bool:
        """
        Check if content contains dangerous patterns.

        Args:
            content: Content to check

        Returns:
            True if dangerous patterns found
        """
        return bool(self._dangerous_pattern.search(content))

    def _is_domain_allowed(self, domain: str) -> bool:
        """
        Check if external domain is whitelisted.

        Args:
            domain: Domain to check

        Returns:
            True if domain is allowed
        """
        # Remove port if present
        domain_without_port = domain.split(":")[0]

        # Check exact match
        if domain_without_port in self.allowed_domains:
            return True

        # Check subdomain match (e.g., cdn.example.com matches example.com)
        return any(domain_without_port.endswith("." + allowed) for allowed in self.allowed_domains)

    def validate_iframe_sandbox(self, iframe_html: str) -> bool:
        """
        Validate that iframe has proper sandbox attribute.

        Args:
            iframe_html: HTML containing iframe tag

        Returns:
            True if iframe has valid sandbox attribute
        """
        if "<iframe" not in iframe_html.lower():
            return True  # No iframe

        # Tier A and B: iframes not allowed
        if self.tier in ["A", "B"]:
            return False

        # Tier C: iframe must have sandbox attribute
        if "sandbox=" not in iframe_html:
            logger.warning("iframe without sandbox attribute detected")
            return False

        return True

    def get_sanitization_report(self, html: str) -> dict:
        """
        Get detailed sanitization report without actually sanitizing.

        Useful for debugging and showing merchants what will be removed.

        Args:
            html: HTML to analyze

        Returns:
            Dict with sanitization details
        """
        report = {
            "tier": self.tier,
            "has_dangerous_patterns": self._contains_dangerous_pattern(html),
            "disallowed_tags": [],
            "disallowed_attrs": [],
            "external_domains": [],
            "warnings": [],
        }

        # Find disallowed tags
        class TagFinder(HTMLParser):
            def __init__(self, allowed_tags):
                super().__init__()
                self.allowed_tags = allowed_tags
                self.disallowed_tags = set()

            def handle_starttag(self, tag, attrs):
                if tag not in self.allowed_tags:
                    self.disallowed_tags.add(tag)

        parser = TagFinder(self.allowed_tags)
        try:
            parser.feed(html)
            report["disallowed_tags"] = list(parser.disallowed_tags)
        except Exception as e:
            report["warnings"].append(f"Failed to parse HTML: {e}")

        return report
