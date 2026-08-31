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
from bleach.css_sanitizer import CSSSanitizer
from django.conf import settings

logger = logging.getLogger(__name__)

# Matches a genuine ``sandbox`` attribute on an iframe's opening tag and captures
# its value. The required leading whitespace stops the substring ``sandbox=``
# inside another attribute's value (e.g. ``title="sandbox=x"``) from satisfying
# the presence check.
_IFRAME_SANDBOX_ATTR_RE = re.compile(
    r"""\ssandbox(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]*)))?""",
    re.IGNORECASE,
)
_IFRAME_OPEN_TAG_RE = re.compile(r"<iframe\b[^>]*>", re.IGNORECASE)

# Granting both ``allow-scripts`` and ``allow-same-origin`` lets framed content
# run script with same-origin access and thereby remove its own sandbox — the
# standard sandbox escape. An iframe requesting both is treated as unsandboxed.
_SANDBOX_ESCAPE_TOKENS = frozenset({"allow-scripts", "allow-same-origin"})

# Individually dangerous sandbox tokens: any one of these lets framed content
# reach outside its frame (redirect the top window to a phishing page, spawn a
# non-sandboxed popup, trigger downloads, or open modal dialogs). Merchant
# marketing embeds have no need for them, so an iframe requesting any is dropped.
_SANDBOX_FORBIDDEN_TOKENS = frozenset(
    {
        "allow-top-navigation",
        "allow-top-navigation-by-user-activation",
        "allow-top-navigation-to-custom-protocols",
        "allow-popups-to-escape-sandbox",
        "allow-downloads",
        "allow-modals",
    }
)


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

    # Inline CSS properties Bleach is allowed to keep on a `style` attribute.
    # Anything outside this allow-list (including the dangerous properties
    # above) is dropped by the CSS sanitizer.
    ALLOWED_CSS_PROPERTIES = [
        "color",
        "background",
        "background-color",
        "background-image",
        "background-position",
        "background-repeat",
        "background-size",
        "font",
        "font-family",
        "font-size",
        "font-style",
        "font-weight",
        "line-height",
        "letter-spacing",
        "word-spacing",
        "text-align",
        "text-decoration",
        "text-transform",
        "text-shadow",
        "text-indent",
        "white-space",
        "vertical-align",
        "list-style",
        "list-style-type",
        "list-style-position",
        "margin",
        "margin-top",
        "margin-right",
        "margin-bottom",
        "margin-left",
        "padding",
        "padding-top",
        "padding-right",
        "padding-bottom",
        "padding-left",
        "border",
        "border-top",
        "border-right",
        "border-bottom",
        "border-left",
        "border-color",
        "border-style",
        "border-width",
        "border-radius",
        "box-shadow",
        "width",
        "height",
        "max-width",
        "max-height",
        "min-width",
        "min-height",
        "display",
        "flex",
        "flex-direction",
        "flex-wrap",
        "justify-content",
        "align-items",
        "align-content",
        "align-self",
        "gap",
        "grid-template-columns",
        "grid-template-rows",
        "grid-gap",
        "position",
        "top",
        "right",
        "bottom",
        "left",
        "float",
        "clear",
        "overflow",
        "opacity",
        "cursor",
        "transform",
        "transition",
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

        # Bleach 6.x strips every `style` value unless a CSS sanitizer is
        # supplied; this keeps safe merchant styling while dropping dangerous
        # properties via the allow-list above.
        self.css_sanitizer = CSSSanitizer(allowed_css_properties=self.ALLOWED_CSS_PROPERTIES)

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

        # Use bleach to clean HTML. The CSS sanitizer keeps allow-listed
        # inline style properties instead of Bleach blanking every value.
        cleaned = bleach.clean(
            html,
            tags=self.allowed_tags,
            attributes=self.allowed_attrs,
            protocols=self.allowed_protocols,
            css_sanitizer=self.css_sanitizer,
            strip=True,  # Remove disallowed tags entirely
        )

        # Tier C keeps iframes; drop any that lack the mandatory sandbox
        # attribute enforced by validate_iframe_sandbox().
        if self.tier == "C":
            cleaned = self._enforce_iframe_sandbox(cleaned)

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

    def _enforce_iframe_sandbox(self, html: str) -> str:
        """
        Remove iframe elements that lack an acceptable sandbox attribute.

        Bleach keeps whitelisted iframe tags verbatim, so unsandboxed iframes
        would otherwise survive even though validate_iframe_sandbox() rejects
        them. Each iframe element is re-validated and dropped if unsafe.

        Args:
            html: Cleaned HTML that may contain iframe elements

        Returns:
            HTML with unsandboxed iframes removed
        """
        if "<iframe" not in html.lower():
            return html

        def drop_unsandboxed(match):
            element = match.group(0)
            if self.validate_iframe_sandbox(element):
                return element
            logger.warning("Removing iframe without acceptable sandbox attribute")
            return ""

        return re.sub(
            r"<iframe\b[^>]*>.*?</iframe>",
            drop_unsandboxed,
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

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

        # Tier C: require a genuine sandbox attribute on the opening tag and
        # forbid the allow-scripts + allow-same-origin escape combination.
        # Scope the search to the opening tag so inner content can't spoof it,
        # and require the attribute proper (not a substring in another value).
        open_tag_match = _IFRAME_OPEN_TAG_RE.search(iframe_html)
        open_tag = open_tag_match.group(0) if open_tag_match else iframe_html

        sandbox_match = _IFRAME_SANDBOX_ATTR_RE.search(open_tag)
        if not sandbox_match:
            logger.warning("iframe without a real sandbox attribute detected")
            return False

        value = sandbox_match.group(1) or sandbox_match.group(2) or sandbox_match.group(3) or ""
        tokens = {token.lower() for token in value.split()}
        if _SANDBOX_ESCAPE_TOKENS.issubset(tokens):
            logger.warning(
                "iframe sandbox grants both allow-scripts and allow-same-origin "
                "(sandbox escape); treating as unsandboxed"
            )
            return False
        forbidden = tokens & _SANDBOX_FORBIDDEN_TOKENS
        if forbidden:
            logger.warning(
                "iframe sandbox grants frame-escaping token(s) %s; dropping",
                ", ".join(sorted(forbidden)),
            )
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
