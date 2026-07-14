"""
Webhook action executor for form builder.
Posts form data to external URLs with optional HMAC signing.
"""

import hashlib
import hmac
import json
import logging

import requests

from .base import BaseAction

logger = logging.getLogger(__name__)


class WebhookAction(BaseAction):
    """
    POST form data to an external webhook URL.

    Config schema:
    {
        "url": "https://example.com/webhook",
        "method": "POST",
        "headers": {"X-Custom": "value"},
        "include_fields": [],  # empty = all fields
        "secret": "optional-hmac-secret"
    }
    """

    TIMEOUT = 30  # seconds

    def execute(self):
        url = self.config.get("url", "")
        if not url:
            logger.warning("WebhookAction: No URL configured for action %s", self.action.pk)
            return {"status": "skipped", "reason": "No webhook URL configured"}

        method = self.config.get("method", "POST").upper()
        custom_headers = self.config.get("headers", {})
        include_fields = self.config.get("include_fields", [])
        secret = self.config.get("secret", "")

        # Build payload
        payload = self._build_payload(include_fields)
        payload_json = json.dumps(payload, default=str)

        # Build headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Spwig-FormBuilder/1.0",
        }
        headers.update(custom_headers)

        # Add HMAC signature if secret is configured
        if secret:
            signature = hmac.new(
                secret.encode("utf-8"), payload_json.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            headers["X-Signature-256"] = f"sha256={signature}"

        try:
            response = requests.request(
                method=method,
                url=url,
                data=payload_json,
                headers=headers,
                timeout=self.TIMEOUT,
            )

            result = {
                "status": "sent",
                "http_status": response.status_code,
                "url": url,
            }

            if not response.ok:
                result["status"] = "error"
                result["response_body"] = response.text[:500]
                logger.warning(
                    "WebhookAction: HTTP %s from %s for response %s",
                    response.status_code,
                    url,
                    self.form_response.pk,
                )
            else:
                logger.info(
                    "WebhookAction: HTTP %s to %s for response %s",
                    response.status_code,
                    url,
                    self.form_response.pk,
                )

            return result

        except requests.Timeout:
            logger.error("WebhookAction: Timeout for %s (response %s)", url, self.form_response.pk)
            return {"status": "error", "error": f"Timeout after {self.TIMEOUT}s", "url": url}

        except requests.RequestException as e:
            logger.error(
                "WebhookAction: Failed for %s (response %s): %s", url, self.form_response.pk, e
            )
            return {"status": "error", "error": str(e), "url": url}

    def _build_payload(self, include_fields):
        """Build the webhook payload from form response data."""
        payload = {
            "event": "form_submission",
            "form": {
                "id": self.form_response.form.pk,
                "slug": self.form_response.form.slug,
                "name": self.form_response.form.name,
            },
            "response": {
                "id": self.form_response.pk,
                "submitted_at": str(self.form_response.submitted_at or ""),
                "status": self.form_response.status,
            },
            "data": {},
        }

        # Filter fields if include_fields is specified
        if include_fields:
            for field_name in include_fields:
                if field_name in self.form_response.data:
                    payload["data"][field_name] = self.form_response.data[field_name]
        else:
            payload["data"] = dict(self.form_response.data)

        # Add user info if available
        if self.form_response.user:
            payload["response"]["user_email"] = self.form_response.user.email

        return payload
