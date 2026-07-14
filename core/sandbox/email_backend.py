"""
Sandbox Email Backend

Wraps the actual email backend to enforce sandbox restrictions:
- In sandbox mode, only deliver emails to whitelisted addresses
- Non-whitelisted recipients have their emails logged but never sent
- Whitelisted emails get [SANDBOX] prefix and banner for clarity
- The admin email is always implicitly whitelisted

In production mode, all emails pass through unchanged.
"""

import logging
import re

from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend

from core.license import is_sandbox_mode

logger = logging.getLogger(__name__)


SANDBOX_BANNER_HTML = (
    '<div style="background:#ff6b35;color:#fff;padding:12px 20px;margin-bottom:20px;'
    "border-radius:4px;font-family:system-ui,-apple-system,sans-serif;font-size:14px;"
    'font-weight:600;text-align:center;">'
    "&#9888; SANDBOX MODE &mdash; This email was generated in a sandbox/testing environment."
    '<br><span style="font-weight:400;font-size:12px;">'
    "Original recipient: {original_to}</span>"
    "</div>"
)


class SandboxEmailBackend(BaseEmailBackend):
    """
    Email backend that enforces sandbox email restrictions.
    In production mode, passes through to the real backend with zero overhead.

    In sandbox mode:
    - Emails to whitelisted addresses are delivered with [SANDBOX] prefix
    - Emails to non-whitelisted addresses are silently dropped (logged only)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        actual_backend = getattr(
            settings,
            "SANDBOX_ACTUAL_EMAIL_BACKEND",
            "django.core.mail.backends.console.EmailBackend",
        )
        self._connection = get_connection(backend=actual_backend, fail_silently=self.fail_silently)

    def open(self):
        return self._connection.open()

    def close(self):
        return self._connection.close()

    def send_messages(self, email_messages):
        if not is_sandbox_mode():
            return self._connection.send_messages(email_messages)

        from core.sandbox.email_guard import sandbox_filter_recipient

        deliverable = []

        for msg in email_messages:
            original_to = ", ".join(msg.to)

            # Check each recipient against the whitelist
            allowed_to = []
            blocked_to = []
            for recipient in msg.to:
                action, _ = sandbox_filter_recipient(recipient)
                if action == "send":
                    allowed_to.append(recipient)
                else:
                    blocked_to.append(recipient)

            # Also filter CC and BCC
            allowed_cc = []
            for recipient in msg.cc or []:
                action, _ = sandbox_filter_recipient(recipient)
                if action == "send":
                    allowed_cc.append(recipient)

            allowed_bcc = []
            for recipient in msg.bcc or []:
                action, _ = sandbox_filter_recipient(recipient)
                if action == "send":
                    allowed_bcc.append(recipient)

            if blocked_to:
                logger.info(
                    f"[SANDBOX] Email blocked for non-whitelisted recipients: "
                    f"{', '.join(blocked_to)}, subject={msg.subject}"
                )

            if not allowed_to:
                # No whitelisted recipients — log and skip entirely
                logger.info(
                    f"[SANDBOX] Email dropped (no whitelisted recipients): "
                    f"to={original_to}, subject={msg.subject}"
                )
                continue

            # Update recipients to only whitelisted addresses
            msg.to = allowed_to
            msg.cc = allowed_cc
            msg.bcc = allowed_bcc

            # Prefix subject
            if not msg.subject.startswith("[SANDBOX]"):
                msg.subject = f"[SANDBOX] {msg.subject}"

            # Add sandbox banner to HTML alternatives
            if hasattr(msg, "alternatives"):
                new_alts = []
                for content, mimetype in msg.alternatives:
                    if mimetype == "text/html":
                        banner = SANDBOX_BANNER_HTML.format(original_to=original_to)
                        if "<body>" in content.lower():
                            content = re.sub(
                                r"(<body[^>]*>)",
                                r"\1" + banner,
                                content,
                                count=1,
                                flags=re.IGNORECASE,
                            )
                        else:
                            content = banner + content
                    new_alts.append((content, mimetype))
                msg.alternatives = new_alts

            # Add sandbox note to plain text body
            msg.body = f"[SANDBOX MODE] Original recipient: {original_to}\n{'=' * 50}\n\n{msg.body}"

            deliverable.append(msg)

        if deliverable:
            return self._connection.send_messages(deliverable)

        return 0
