"""
Email Tracking Service
Implements open and click tracking for emails using pixels and URL rewriting
"""

import logging
import re
import uuid
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse

from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)

# Email template types that are marketing / re-engagement and therefore safe to
# tag for revenue attribution. Tagging TRANSACTIONAL email links (order/shipping
# confirmations, password reset, etc.) would create spurious "email" touches
# that misattribute a customer's *next* order to email, so anything not listed
# here — including a blank template_type — is deliberately NOT tagged.
#
# There is no marketing/transactional flag on the model; classification lives
# here. Extend this set (or the prefixes) when adding new marketing email types.
# All cart_abandoned* variants (1h/24h/48h/discount) are re-engagement, so a
# prefix is safe here. back_in_stock is NOT prefixed: the family includes the
# transactional back_in_stock_waitlist_confirmation, so its marketing members
# are listed explicitly instead.
_MARKETING_TEMPLATE_PREFIXES = ("cart_abandoned",)

# A transactional acknowledgement is never marketing, even under a marketing
# prefix — this guards against over-tagging *_confirmation / *_receipt types.
_TRANSACTIONAL_SUFFIXES = ("_confirmation", "_confirmed", "_receipt")

_MARKETING_TEMPLATE_TYPES = frozenset(
    {
        # Cart recovery
        "cart_recovered_thank_you",
        # Back-in-stock re-engagement (NOT back_in_stock_waitlist_confirmation)
        "back_in_stock",
        "back_in_stock_low_stock_warning",
        # Wishlist re-engagement (NOT wishlist_shared_confirmation, which is transactional)
        "wishlist_back_in_stock",
        "wishlist_price_drop",
        "wishlist_low_stock_warning",
        "wishlist_reminder_weekly",
        # Newsletter
        "newsletter",
        # Loyalty re-engagement
        "loyalty_points_expiring",
        "loyalty_birthday_bonus",
        "loyalty_anniversary_bonus",
        "loyalty_referral_bonus",
        "loyalty_double_points_event",
        # Content, review, welcome (broader scope)
        "blog_digest_weekly",
        "blog_post_published",
        "review_request",
        "account_welcome",
        "blog_subscriber_welcome",
    }
)


def is_marketing_template_type(template_type: str) -> bool:
    """True if emails of this template type should carry attribution UTM tags."""
    if not template_type:
        return False
    if template_type.endswith(_TRANSACTIONAL_SUFFIXES):
        return False
    if template_type in _MARKETING_TEMPLATE_TYPES:
        return True
    return any(template_type.startswith(p) for p in _MARKETING_TEMPLATE_PREFIXES)


class TrackingService:
    """
    Handles email open and click tracking
    """

    def add_tracking(self, html_body: str, email_outbox_id: str) -> str:
        """
        Add tracking pixel and rewrite links for tracking

        Args:
            html_body: HTML email body
            email_outbox_id: EmailOutbox UUID

        Returns:
            HTML with tracking added
        """
        # Generate tracking ID
        tracking_id = self._generate_tracking_id(email_outbox_id)

        # Add open tracking pixel
        html_with_pixel = self._add_open_tracking_pixel(html_body, tracking_id)

        # Derive the attribution campaign (None for transactional emails, which
        # must not be tagged).
        utm_campaign = self._attribution_campaign(email_outbox_id)

        # Rewrite links for click tracking (and attribution-tag internal
        # marketing links).
        html_with_tracking = self._add_link_tracking(html_with_pixel, tracking_id, utm_campaign)

        logger.debug(f"Added tracking for email_outbox_id={email_outbox_id}")
        return html_with_tracking

    def _attribution_campaign(self, email_outbox_id) -> str | None:
        """utm_campaign for this email, or None if it should not be attributed.

        Prefers the specific campaign slug the sender stamped on the outbox
        (``attribution_campaign`` — set by Campaign Studio so revenue credits the
        exact campaign). Falls back to the coarse ``template_type`` for other
        marketing / re-engagement emails (see ``is_marketing_template_type``).
        Best-effort: any lookup failure returns None so tracking is never affected.
        """
        try:
            from email_system.models import EmailOutbox

            row = (
                EmailOutbox.objects.filter(id=email_outbox_id)
                .values("attribution_campaign", "template_type")
                .first()
            )
            if not row:
                return None
            if row["attribution_campaign"]:
                # Backstop against future drift: never attribution-tag transactional
                # mail even if a slug was somehow stamped on it — a stray "email" touch
                # would misattribute the recipient's next order. (Marketing types incl.
                # promotional_offers pass; only truly transactional types are blocked.)
                from accounts.constants import TRANSACTIONAL_EMAIL_TYPES

                if row["template_type"] in TRANSACTIONAL_EMAIL_TYPES:
                    return None
                return row["attribution_campaign"]
            template_type = row["template_type"]
            return template_type if is_marketing_template_type(template_type) else None
        except Exception:
            logger.debug("attribution: could not resolve email campaign", exc_info=True)
            return None

    def _generate_tracking_id(self, email_outbox_id: str) -> str:
        """
        Generate unique tracking ID

        Format: {email_outbox_id}-{random_token}
        The random token helps prevent tracking pixel caching
        """
        random_token = uuid.uuid4().hex[:16]
        return f"{email_outbox_id}-{random_token}"

    def _add_open_tracking_pixel(self, html_body: str, tracking_id: str) -> str:
        """
        Add 1x1 transparent tracking pixel to email

        Pixel is added before closing </body> tag
        """
        # Build pixel URL (relative path, will be absolute in production)
        pixel_path = reverse("email_tracking:track_open", args=[tracking_id])

        # Use absolute URL with site domain
        pixel_url = self._get_absolute_url(pixel_path)

        # Create pixel image tag
        pixel_html = (
            f'<img src="{pixel_url}" '
            f'width="1" height="1" '
            f'style="display:none;width:1px;height:1px" '
            f'alt="" />'
        )

        # Insert before </body>
        if "</body>" in html_body.lower():
            # Case-insensitive replace
            html_body = re.sub(r"</body>", f"{pixel_html}</body>", html_body, flags=re.IGNORECASE)
        else:
            # No body tag, append to end
            html_body += pixel_html

        return html_body

    def _add_link_tracking(self, html_body: str, tracking_id: str, utm_campaign: str = None) -> str:
        """
        Rewrite all links to go through tracking redirect

        Preserves original URL as parameter
        Skips unsubscribe links and anchor links

        When ``utm_campaign`` is set (marketing emails only), internal storefront
        links additionally carry ``utm_source=email&utm_medium=email&utm_campaign``
        so the eventual landing is captured as an email touch by the attribution
        engine. External links and links that already carry UTM are left alone.
        """
        # Pattern to match href attributes
        # Matches: href="url" or href='url'
        link_pattern = r'href=(["\'])([^"\']+)\1'

        # Resolve the store host once (not per-link) for the internal check.
        site_host = self._site_host()

        def replace_link(match):
            quote_char = match.group(1)  # Preserve quote style
            original_url = match.group(2)

            # Skip anchor links (#)
            if original_url.startswith("#"):
                return match.group(0)

            # Skip mailto: links
            if original_url.startswith("mailto:"):
                return match.group(0)

            # Skip javascript: links
            if original_url.startswith("javascript:"):
                return match.group(0)

            # Skip tracking URLs (prevent double-wrapping)
            if "/track/click/" in original_url:
                return match.group(0)

            # Attribution-tag internal marketing links (no-op otherwise).
            original_url = self._append_attribution_utm(original_url, utm_campaign, site_host)

            # Build tracking URL
            tracking_path = reverse("email_tracking:track_click", args=[tracking_id])
            tracking_url = self._get_absolute_url(tracking_path)

            # Add original URL as query parameter
            full_tracking_url = f"{tracking_url}?url={quote(original_url)}"

            return f"href={quote_char}{full_tracking_url}{quote_char}"

        # Replace all links
        html_with_tracking = re.sub(link_pattern, replace_link, html_body)

        return html_with_tracking

    def _site_host(self) -> str:
        """The store's own hostname, for the internal-link check."""
        try:
            return urlparse(self._get_absolute_url("/")).hostname or ""
        except Exception:
            return ""

    def _is_internal_url(self, url: str, site_host: str) -> bool:
        """Relative URLs, or absolute URLs on the store's own host, are internal."""
        try:
            parsed = urlparse(url)
        except Exception:
            return False
        if not parsed.scheme and not parsed.netloc:
            return True  # relative path
        return bool(parsed.hostname) and parsed.hostname == site_host

    def _append_attribution_utm(self, url: str, utm_campaign: str, site_host: str) -> str:
        """Append email attribution UTM to an internal URL.

        No-op when there is no campaign, the URL is external, or it already
        carries UTM (never double-tag). Existing query params are preserved.
        """
        if not utm_campaign or not self._is_internal_url(url, site_host):
            return url
        try:
            parsed = urlparse(url)
            # Keep the pair list (not a dict) so repeated query keys — e.g.
            # ?filter=a&filter=b on a category link — are preserved, not collapsed.
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
            if any(key == "utm_source" for key, _ in pairs):
                return url  # already tagged upstream — respect it
            pairs = pairs + [
                ("utm_source", "email"),
                ("utm_medium", "email"),
                ("utm_campaign", utm_campaign),
            ]
            return urlunparse(parsed._replace(query=urlencode(pairs)))
        except Exception:
            return url

    def _get_absolute_url(self, path: str) -> str:
        """
        Convert relative path to absolute URL

        Uses SITE_URL from settings or constructs from current site
        """
        # Try to get site URL from settings
        site_url = getattr(settings, "SITE_URL", None)

        if not site_url:
            # Try to get from current site
            try:
                from django.contrib.sites.models import Site

                current_site = Site.objects.get_current()
                protocol = "https" if getattr(settings, "SECURE_SSL_REDIRECT", False) else "http"
                site_url = f"{protocol}://{current_site.domain}"
            except Exception as e:
                logger.warning(f"Could not determine site URL: {e}")
                # Fallback to localhost for development
                site_url = "http://localhost:8000"

        # Ensure path starts with /
        if not path.startswith("/"):
            path = f"/{path}"

        return f"{site_url}{path}"

    def parse_tracking_id(self, tracking_id: str) -> str | None:
        """
        Parse tracking ID to extract email_outbox_id

        Args:
            tracking_id: Tracking ID in format {uuid}-{16_char_token}

        Returns:
            email_outbox_id UUID or None if invalid format
        """
        try:
            # Tracking ID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxx
            # UUID is 36 chars, token is 16 chars, separator is 1 char = 53 total
            # Split from the right to get the last 16 chars (token)
            if len(tracking_id) < 53:
                return None

            # Email outbox ID is everything except the last -token part
            email_outbox_id = tracking_id[:-17]  # Remove -xxxxxxxxxxxxxxxx
            return email_outbox_id
        except Exception as e:
            logger.error(f"Error parsing tracking ID '{tracking_id}': {e}")
            return None
