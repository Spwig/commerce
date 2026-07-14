"""
Email Tracking Service
Implements open and click tracking for emails using pixels and URL rewriting
"""

import logging
import re
import uuid
from urllib.parse import quote

from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


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

        # Rewrite links for click tracking
        html_with_tracking = self._add_link_tracking(html_with_pixel, tracking_id)

        logger.debug(f"Added tracking for email_outbox_id={email_outbox_id}")
        return html_with_tracking

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

    def _add_link_tracking(self, html_body: str, tracking_id: str) -> str:
        """
        Rewrite all links to go through tracking redirect

        Preserves original URL as parameter
        Skips unsubscribe links and anchor links
        """
        # Pattern to match href attributes
        # Matches: href="url" or href='url'
        link_pattern = r'href=(["\'])([^"\']+)\1'

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

            # Build tracking URL
            tracking_path = reverse("email_tracking:track_click", args=[tracking_id])
            tracking_url = self._get_absolute_url(tracking_path)

            # Add original URL as query parameter
            full_tracking_url = f"{tracking_url}?url={quote(original_url)}"

            return f"href={quote_char}{full_tracking_url}{quote_char}"

        # Replace all links
        html_with_tracking = re.sub(link_pattern, replace_link, html_body)

        return html_with_tracking

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
