"""
Email Sending Service

Handles email sending through provider accounts with queue management.
"""

import logging
from typing import Any

from django.db import transaction
from django.utils import timezone

from core.license import is_sandbox_mode
from email_system.models import EmailAccount, EmailOutbox
from email_system.providers.base import EmailMessage, EmailRecipientsRefused, SendResult

logger = logging.getLogger(__name__)


class EmailSendingService:
    """
    Service for sending emails through configured provider accounts.

    Handles:
    - Provider selection (default or specific account)
    - Queue management
    - Error handling and retry logic
    - Provider-specific message formatting
    """

    @staticmethod
    def get_default_account(site=None) -> EmailAccount | None:
        """
        Get the default email account for a site.

        Args:
            site: Site instance (uses current site if None)

        Returns:
            Default EmailAccount or None
        """
        queryset = EmailAccount.objects.filter(is_active=True)

        if site:
            queryset = queryset.filter(site=site)

        # Try to get default account first
        account = queryset.filter(is_default=True).first()

        # Fall back to any active account
        if not account:
            account = queryset.first()

        return account

    @staticmethod
    def queue_email(
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
        reply_to: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        headers: dict[str, str] | None = None,
        tags: list[str] | None = None,
        attachments: list[dict] | None = None,
        template_type: str | None = None,
        account: EmailAccount | None = None,
        site=None,
        priority: int = 5,
        attribution_campaign: str = "",
    ) -> EmailOutbox:
        """
        Queue an email for sending.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body (optional)
            from_email: Sender email (uses account default if None)
            from_name: Sender name (uses account default if None)
            reply_to: Reply-to address (optional)
            cc: CC recipients list (optional)
            bcc: BCC recipients list (optional)
            headers: Custom headers dict (optional)
            tags: Email tags list (optional)
            attachments: Attachments list (optional)
            template_type: Template type identifier (optional)
            account: Specific EmailAccount to use (uses default if None)
            site: Site instance (uses current site if None)
            priority: Priority (1-10, lower is higher priority)
            attribution_campaign: utm_campaign slug for revenue attribution
                (blank for transactional mail; stamped on tracked links)

        Returns:
            Created EmailOutbox instance

        Raises:
            ValueError: If no active email account is available
        """
        # Check communication preferences if template_type provided
        if template_type:
            from django.contrib.auth import get_user_model

            from accounts.constants import TRANSACTIONAL_EMAIL_TYPES
            from accounts.services.preference_service import PreferenceService

            User = get_user_model()

            try:
                # Try to find user by email
                user = User.objects.get(email=to_email)

                # Check if user should receive this email type
                if not PreferenceService.check_email_permission(user, template_type):
                    logger.info(
                        f"Skipping email to {to_email} - preference disabled for {template_type}"
                    )

                    # Get site
                    if not site:
                        from django.contrib.sites.models import Site

                        site = Site.objects.get_current()

                    # Create skipped outbox entry for tracking
                    return EmailOutbox.objects.create(
                        site=site,
                        account=account or EmailSendingService.get_default_account(site=site),
                        to_email=to_email,
                        from_email=from_email or "",
                        subject=subject,
                        html_body="",
                        text_body="",
                        template_type=template_type or "",
                        status="skipped",
                        skip_reason="user_preference_disabled",
                        queued_at=timezone.now(),
                    )

            except User.DoesNotExist:
                # Guest user - send email (transactional only should reach guests)
                pass

            # Add unsubscribe footer for marketing emails
            if template_type not in TRANSACTIONAL_EMAIL_TYPES:
                html_body = EmailSendingService._add_unsubscribe_footer(
                    html_body, to_email, template_type
                )
                if text_body:
                    text_body = EmailSendingService._add_unsubscribe_footer_text(
                        text_body, to_email, template_type
                    )

        # Get account
        if not account:
            account = EmailSendingService.get_default_account(site=site)

        if not account:
            raise ValueError("No active email account available")

        # Use account defaults if not provided
        if not from_email:
            from_email = account.from_email
        if not from_name:
            from_name = account.from_name
        if not reply_to and account.reply_to:
            reply_to = account.reply_to

        # Delivery mode and test redirect
        from core.models import SiteSettings

        site_settings = SiteSettings.get_settings()
        delivery_mode = site_settings.email_delivery_mode

        # Determine outbox status based on delivery mode
        if delivery_mode == "log_only":
            outbox_status = "logged"
        elif delivery_mode == "paused":
            outbox_status = "held"
        else:
            outbox_status = "queued"

        # Test redirect: merchant-controlled redirect to test address
        if site_settings.email_test_redirect_address:
            original_to = to_email
            to_email = site_settings.email_test_redirect_address
            if not subject.startswith("[TEST]"):
                subject = f"[TEST] {subject}"
            test_banner = (
                '<div style="background:#2196F3;color:#fff;padding:12px 20px;'
                "margin-bottom:20px;border-radius:4px;font-family:system-ui,"
                "-apple-system,sans-serif;font-size:14px;font-weight:600;"
                'text-align:center;">'
                "TEST REDIRECT &mdash; This email was redirected for testing.<br>"
                '<span style="font-weight:400;font-size:12px;">'
                f"Original recipient: {original_to}</span></div>"
            )
            html_body = test_banner + html_body
            if text_body:
                text_body = (
                    f"[TEST REDIRECT] Original recipient: {original_to}\n{'=' * 50}\n\n{text_body}"
                )
            cc = []
            bcc = []
            logger.info(
                f"[TEST REDIRECT] Email redirected: to={original_to} -> {to_email}, "
                f"subject={subject}"
            )

        # Sandbox mode: enforce email whitelist (license-enforced, takes priority)
        from core.sandbox.email_guard import sandbox_filter_recipient

        action, to_email = sandbox_filter_recipient(to_email)
        if action == "log":
            # Non-whitelisted recipient — record in outbox but never send
            if not subject.startswith("[SANDBOX]"):
                subject = f"[SANDBOX] {subject}"

            if not site:
                from django.contrib.sites.models import Site

                site = Site.objects.get_current()

            outbox = EmailOutbox.objects.create(
                site=site,
                account=account or EmailSendingService.get_default_account(site=site),
                to_email=to_email,
                from_email=from_email or "",
                from_name=from_name or "",
                subject=subject,
                html_body=html_body,
                text_body=text_body or "",
                template_type=template_type or "",
                attribution_campaign=attribution_campaign or "",
                status="sandbox_logged",
                priority=priority,
                queued_at=timezone.now(),
            )
            logger.info(
                f"[SANDBOX] Email to {to_email} sandbox-logged "
                f"(not whitelisted), outbox_id={outbox.id}"
            )
            return outbox

        if action == "send" and is_sandbox_mode():
            # Whitelisted recipient — deliver but mark as sandbox
            if not subject.startswith("[SANDBOX]"):
                subject = f"[SANDBOX] {subject}"
            cc = []
            bcc = []

        # Get site
        if not site:
            from django.contrib.sites.models import Site

            site = Site.objects.get_current()

        # Create outbox entry
        outbox = EmailOutbox.objects.create(
            site=site,
            account=account,
            to_email=to_email,
            from_email=from_email,
            from_name=from_name or "",
            reply_to=reply_to or "",
            cc=cc or [],
            bcc=bcc or [],
            subject=subject,
            html_body=html_body,
            text_body=text_body or "",
            headers=headers or {},
            tags=tags or [],
            attachments=attachments or [],
            template_type=template_type or "",
            attribution_campaign=attribution_campaign or "",
            status=outbox_status,
            priority=priority,
            queued_at=timezone.now(),
        )

        if outbox_status == "logged":
            logger.info(f"Logged email {outbox.id} to {to_email} (log_only mode)")
        elif outbox_status == "held":
            logger.info(f"Held email {outbox.id} to {to_email} (paused mode)")
        else:
            logger.info(f"Queued email {outbox.id} to {to_email}")

        return outbox

    @staticmethod
    def send_email(outbox_id: str) -> bool:
        """
        Send a queued email.

        IMPORTANT: call this in autocommit, NOT inside an open ``transaction.atomic()``
        block. The claim (queued -> sending) must commit before the slow SMTP call so
        peers see it; if it is held open and the surrounding transaction rolls back
        after the provider accepted the message, the row reverts to "queued" and the
        sweep re-sends it (double-send). The transactional flows dispatch via
        ``on_commit`` -> a separate task, which is safe.

        Args:
            outbox_id: EmailOutbox UUID

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            outbox = EmailOutbox.objects.get(id=outbox_id)

            # Check if already sent
            if outbox.status == "sent":
                logger.warning(f"Email {outbox_id} already sent")
                return True

            # Don't send held, logged, or sandbox-logged emails
            if outbox.status in ("held", "logged", "sandbox_logged"):
                logger.warning(f"Email {outbox_id} has status '{outbox.status}' - cannot send")
                return False

            # Check retry limit
            if outbox.retry_count >= outbox.max_retries:
                logger.error(f"Email {outbox_id} exceeded max retries")
                outbox.status = "failed"
                outbox.failed_at = timezone.now()
                outbox.error_message = "Exceeded maximum retry attempts"
                outbox.save()
                return False

            # Honour the merchant's delivery-mode kill switch on ALREADY-queued rows,
            # not just at queue time: flipping to paused / log_only mid-blast must stop
            # in-flight mail too (the async dispatch, the sweep, and the campaign
            # drainer all pass through here). Move a queued row to held/logged rather
            # than delivering it. (Mirrors the queue-time check in send_template_email.)
            from core.models import SiteSettings

            delivery_mode = SiteSettings.get_settings().email_delivery_mode
            if delivery_mode != "live":
                new_status = "held" if delivery_mode == "paused" else "logged"
                EmailOutbox.objects.filter(id=outbox_id, status__in=("queued", "failed")).update(
                    status=new_status, updated_at=timezone.now()
                )
                logger.info(
                    f"Email {outbox_id} not sent: delivery mode is '{delivery_mode}' "
                    f"(-> {new_status})"
                )
                return False

            # Atomically claim the row (queued/failed -> sending). This is the ONE
            # guard against two concurrent workers both delivering the same message
            # to a customer: exactly one UPDATE matches, the loser backs off. The
            # claim commits immediately (short/autocommit) so peers see "sending"
            # before the slow SMTP call. All send paths funnel through here (the async
            # task, the pending sweep, the campaign drainer, the inline callers, and
            # retry_failed_emails), so this single claim protects every one of them.
            # "failed" is claimable so the retry path can re-send (the retry-exhausted
            # guard above already turns away rows with no attempts left); "bounced"/
            # "skipped"/"held"/"logged" are intentionally excluded.
            claimed = EmailOutbox.objects.filter(
                id=outbox_id, status__in=("queued", "failed")
            ).update(status="sending", updated_at=timezone.now())
            if claimed != 1:
                outbox.refresh_from_db()
                if outbox.status == "sent":
                    return True
                logger.info(f"Email {outbox_id} not claimable (status={outbox.status}); skipping")
                return False
            # Remember the pre-claim status so a budget defer can restore it exactly
            # (a retry claims a "failed" row; reverting it to "queued" would lose that).
            pre_claim_status = outbox.status
            # Reflect the claim on the in-memory instance for the rest of this call.
            outbox.status = "sending"

            # Marketing throughput gate (single chokepoint for EVERY send path): a
            # marketing-band row may only send while the account's per-minute budget
            # has marketing headroom; otherwise DEFER — revert the claim to its prior
            # state and let it retry on a later tick. try_marketing_send only consumes
            # budget when it allows, so a defer costs nothing. Reserving here (post-claim)
            # means only the claim winner reserves, so a re-dispatch can't double-consume.
            # Transactional rows are never gated (they always send and are counted below).
            if outbox.priority >= EmailOutbox.PRIORITY_MARKETING:
                from email_system.services import send_budget

                if not send_budget.try_marketing_send(outbox.account_id):
                    EmailOutbox.objects.filter(id=outbox_id, status="sending").update(
                        status=pre_claim_status, updated_at=timezone.now()
                    )
                    logger.info(f"Email {outbox_id} deferred by send budget (marketing)")
                    return False

            # Get provider instance
            try:
                provider = outbox.account.get_provider_instance()
            except Exception as e:
                logger.error(f"Failed to get provider instance for {outbox_id}: {e}")
                outbox.status = "failed"
                outbox.failed_at = timezone.now()
                outbox.error_message = f"Provider initialization failed: {str(e)}"
                outbox.retry_count += 1
                outbox.save()
                return False

            # Build email message
            email_message: EmailMessage = {
                "message_id": str(outbox.id),
                "from_email": outbox.from_email,
                "from_name": outbox.from_name if outbox.from_name else None,
                "to": [outbox.to_email],
                "cc": outbox.cc if outbox.cc else [],
                "bcc": outbox.bcc if outbox.bcc else [],
                "reply_to": outbox.reply_to if outbox.reply_to else None,
                "subject": outbox.subject,
                "html": outbox.html_body,
                "text": outbox.text_body if outbox.text_body else "",
                "headers": outbox.headers if outbox.headers else {},
                "return_path": outbox.from_email,
                "attachments": outbox.attachments if outbox.attachments else [],
                "inline_images": [],
                "tags": outbox.tags if outbox.tags else [],
                "metadata": {
                    "outbox_id": str(outbox.id),
                    "template_type": outbox.template_type if outbox.template_type else "",
                },
            }

            # Send via provider
            try:
                result: SendResult = provider.send(email_message)

                if result["accepted"]:
                    # Success
                    outbox.status = "sent"
                    outbox.sent_at = timezone.now()
                    outbox.provider_message_id = result.get("provider_message_id", "")
                    outbox.error_message = ""
                    outbox.save()

                    # Count transactional sends against the per-account budget so
                    # marketing (which reserves against the same counter) yields more
                    # headroom when transactional is busy. Marketing sends are counted
                    # at their reserve point (try_marketing_send), so don't double-count.
                    if outbox.priority < EmailOutbox.PRIORITY_MARKETING:
                        from email_system.services import send_budget

                        send_budget.note_transactional_send(outbox.account_id)

                    logger.info(f"Successfully sent email {outbox_id}")
                    return True
                else:
                    # Provider rejected
                    outbox.status = "failed"
                    outbox.failed_at = timezone.now()
                    outbox.error_message = result.get("error", "Provider rejected email")
                    outbox.retry_count += 1
                    outbox.save()

                    logger.error(f"Provider rejected email {outbox_id}: {result.get('error')}")
                    return False

            except EmailRecipientsRefused as e:
                # A per-recipient rejection at submission. Classify on THIS outbox's
                # recipient, not the message-level aggregate: a multi-recipient message
                # could pair a soft 4xx for one address with a hard 5xx for another, and
                # the aggregate verdict would wrongly bounce+suppress a merely-deferred
                # address. 5xx → permanent bounce (record + don't retry); 4xx → transient
                # (greylisting): keep the failed+retry path so legitimate mail isn't
                # silently dropped.
                bounce_type = getattr(e, "bounce_type", "hard")
                rcpt = (getattr(e, "recipients", None) or {}).get(outbox.to_email)
                if rcpt and isinstance(rcpt[0], int):
                    bounce_type = "hard" if 500 <= rcpt[0] < 600 else "soft"
                outbox.failed_at = timezone.now()
                outbox.error_message = str(e)[:500]
                if bounce_type == "hard":
                    outbox.status = "bounced"
                else:
                    outbox.status = "failed"
                    outbox.retry_count += 1
                outbox.save()
                # Record the event either way (observability + soft-bounce threshold);
                # the rollup only suppresses on a HARD bounce.
                EmailSendingService._record_bounce_event(
                    outbox, bounce_type=bounce_type, reason=str(e)
                )
                logger.warning(f"Recipient refused ({bounce_type}) for {outbox_id}: {e}")
                return False

            except Exception as e:
                # Sending error
                logger.error(f"Error sending email {outbox_id}: {e}", exc_info=True)

                outbox.status = "failed"
                outbox.failed_at = timezone.now()
                outbox.error_message = str(e)
                outbox.retry_count += 1
                outbox.save()

                return False

        except EmailOutbox.DoesNotExist:
            logger.error(f"Email outbox {outbox_id} not found")
            return False

        except Exception as e:
            logger.error(f"Unexpected error sending email {outbox_id}: {e}", exc_info=True)
            return False

    @staticmethod
    def _dispatch_send(outbox_id) -> None:
        """Schedule async delivery of a queued outbox after the current txn commits.

        Best-effort: a broker outage must never propagate to the caller (e.g. order
        creation). The pending-outbox sweep re-delivers anything a lost dispatch
        dropped. Gated by ``EMAIL_AUTO_DISPATCH`` so delivery can be turned off
        without a code change.
        """
        from django.conf import settings as dj_settings

        if not getattr(dj_settings, "EMAIL_AUTO_DISPATCH", True):
            return

        oid = str(outbox_id)

        def _fire():
            try:
                from email_system.tasks import send_outbox_email

                send_outbox_email.delay(oid)
            except Exception:  # noqa: BLE001 — broker hiccup must not break the caller
                logger.warning(
                    "Async email dispatch failed for %s; the pending sweep will recover it",
                    oid,
                    exc_info=True,
                )

        transaction.on_commit(_fire)

    @staticmethod
    def _record_bounce_event(outbox, bounce_type="hard", reason=""):
        """Record a bounce ``EmailEvent`` so list-hygiene can suppress the address.

        ``email_system`` stays unaware of suppression — an ``email_marketing``
        signal receiver reacts to the event. Best-effort: a recording failure must
        never break the send path.
        """
        from email_system.models import EmailEvent

        try:
            EmailEvent.objects.create(
                email=outbox,
                event_type="bounced",
                bounce_type=bounce_type,
                bounce_reason=(reason or "")[:2000],
                event_data={"source": "smtp_reject"},
            )
        except Exception:  # noqa: BLE001 — event recording is best-effort
            logger.warning("Failed to record bounce event for %s", outbox.id, exc_info=True)

    @staticmethod
    def send_immediate(
        to_email: str, subject: str, html_body: str, text_body: str | None = None, **kwargs
    ) -> dict[str, Any]:
        """
        Queue and immediately send an email.

        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML body
            text_body: Plain text body (optional)
            **kwargs: Additional arguments passed to queue_email()

        Returns:
            Dictionary with:
                - success: bool
                - outbox_id: str (UUID)
                - message: str
                - provider_message_id: str (if sent)

        Example:
            result = EmailSendingService.send_immediate(
                to_email='customer@example.com',
                subject='Order Confirmation',
                html_body='<p>Thank you for your order!</p>',
                template_type='order_confirmation'
            )
        """
        try:
            # Queue email
            outbox = EmailSendingService.queue_email(
                to_email=to_email,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
                **kwargs,
            )

            # Only attempt delivery if email was actually queued for sending
            if outbox.status == "queued":
                success = EmailSendingService.send_email(str(outbox.id))
                outbox.refresh_from_db()
                return {
                    "success": success,
                    "outbox_id": str(outbox.id),
                    "message": "Email sent successfully" if success else outbox.error_message,
                    "provider_message_id": outbox.provider_message_id if success else None,
                }
            else:
                # Email was held, logged, or skipped - not an error
                return {
                    "success": True,
                    "outbox_id": str(outbox.id),
                    "message": f"Email {outbox.status}",
                    "provider_message_id": None,
                }

        except Exception as e:
            logger.error(f"Error in send_immediate: {e}", exc_info=True)
            return {
                "success": False,
                "outbox_id": None,
                "message": str(e),
                "provider_message_id": None,
            }

    @staticmethod
    def send_template_email(
        to_email: str,
        template_type: str,
        context: dict,
        language: str | None = None,
        from_email: str | None = None,
        account: EmailAccount | None = None,
        enable_tracking: bool = True,
        dispatch: bool = True,
        **kwargs,
    ) -> EmailOutbox:
        """
        Send email using template system

        Args:
            to_email: Recipient email address
            template_type: Template type (e.g., 'order_confirmation')
            context: Template variables (e.g., {'customer_name': 'John', 'order_number': '12345'})
            language: Language code (optional, defaults to current)
            from_email: Sender email (optional, uses account default)
            account: EmailAccount to send from (optional, uses default)
            enable_tracking: Enable open/click tracking
            **kwargs: Additional arguments passed to queue_email()

        Returns:
            EmailOutbox instance (queued for sending)

        Example:
            outbox = EmailSendingService.send_template_email(
                to_email='customer@example.com',
                template_type='order_confirmation',
                context={
                    'customer_name': 'John Smith',
                    'order_number': 'ORD-12345',
                    'order_total': '$99.99',
                    ...
                },
                language='en'
            )
        """
        # Block HQ-only templates on non-HQ installations
        from django.conf import settings as django_settings

        if not getattr(django_settings, "SPWIG_IS_HQ", False):
            from email_system.models import EmailTemplate

            if EmailTemplate.is_hq_only_type(template_type):
                logger.warning(
                    "Blocked HQ-only template '%s' on non-HQ installation", template_type
                )
                return None

        # Get site
        site = kwargs.get("site")
        if not site:
            from django.contrib.sites.models import Site

            site = Site.objects.get_current()

        # Check communication preferences before rendering template
        from django.contrib.auth import get_user_model

        from accounts.services.preference_service import PreferenceService

        User = get_user_model()

        try:
            # Get user by email - use filter().first() to handle multiple guest users with same email
            user = User.objects.filter(email=to_email).order_by("-date_joined").first()

            # Check if user should receive this email type
            if user and not PreferenceService.check_email_permission(user, template_type):
                logger.info(
                    f"Skipping template email '{template_type}' to {to_email} - preference disabled"
                )

                # Get account
                if not account:
                    account = EmailSendingService.get_default_account()

                # Create skipped outbox entry for tracking
                return EmailOutbox.objects.create(
                    site=site,
                    account=account,
                    to_email=to_email,
                    from_email=from_email or (account.from_email if account else ""),
                    template_type=template_type,
                    status="skipped",
                    skip_reason="user_preference_disabled",
                    queued_at=timezone.now(),
                )

        except User.DoesNotExist:
            # Guest user - continue with sending
            pass

        # Get account
        if not account:
            account = EmailSendingService.get_default_account()

        if not account:
            raise ValueError("No active email account available")

        outbox = EmailOutbox.objects.create(
            site=site,
            account=account,
            to_email=to_email,
            from_email=from_email or account.from_email,
            from_name=account.from_name or "",
            template_type=template_type,
            # send_template_email is the transactional API — stamp high priority so it
            # is never throttled behind marketing on a shared SMTP account.
            priority=EmailOutbox.PRIORITY_TRANSACTIONAL,
            status="pending",
        )

        try:
            # Render template
            from email_system.services.template_renderer import TemplateRenderer

            renderer = TemplateRenderer()

            subject, html_body, plain_text_body = renderer.render(
                template_type=template_type,
                context=context,
                language=language,
                email_outbox_id=str(outbox.id),
                enable_tracking=enable_tracking,
            )

            # Determine final status based on delivery mode
            from core.models import SiteSettings

            site_settings = SiteSettings.get_settings()
            delivery_mode = site_settings.email_delivery_mode

            if delivery_mode == "log_only":
                final_status = "logged"
            elif delivery_mode == "paused":
                final_status = "held"
            else:
                final_status = "queued"

            # Apply test redirect if configured
            if site_settings.email_test_redirect_address:
                original_to = outbox.to_email
                outbox.to_email = site_settings.email_test_redirect_address
                if not subject.startswith("[TEST]"):
                    subject = f"[TEST] {subject}"
                test_banner = (
                    '<div style="background:#2196F3;color:#fff;padding:12px 20px;'
                    "margin-bottom:20px;border-radius:4px;font-family:system-ui,"
                    "-apple-system,sans-serif;font-size:14px;font-weight:600;"
                    'text-align:center;">'
                    "TEST REDIRECT &mdash; This email was redirected for testing.<br>"
                    '<span style="font-weight:400;font-size:12px;">'
                    f"Original recipient: {original_to}</span></div>"
                )
                html_body = test_banner + html_body
                if plain_text_body:
                    plain_text_body = (
                        f"[TEST REDIRECT] Original recipient: {original_to}\n"
                        f"{'=' * 50}\n\n{plain_text_body}"
                    )
                logger.info(
                    f"[TEST REDIRECT] Template email redirected: "
                    f"to={original_to} -> {outbox.to_email}"
                )

            # Sandbox mode: enforce email whitelist (overrides delivery mode)
            from core.sandbox.email_guard import sandbox_filter_recipient

            action, _ = sandbox_filter_recipient(outbox.to_email)
            if action == "log":
                final_status = "sandbox_logged"
            elif action == "send" and is_sandbox_mode():
                if not subject.startswith("[SANDBOX]"):
                    subject = f"[SANDBOX] {subject}"

            # Update outbox entry with rendered content
            outbox.subject = subject
            outbox.html_body = html_body
            outbox.text_body = plain_text_body
            outbox.status = final_status
            outbox.queued_at = timezone.now()
            outbox.save()

            if final_status == "sandbox_logged":
                logger.info(
                    f"[SANDBOX] Template email '{template_type}' to {outbox.to_email} "
                    f"sandbox-logged (not whitelisted, outbox_id={outbox.id})"
                )
            elif final_status == "logged":
                logger.info(
                    f"Logged template email '{template_type}' to {outbox.to_email} "
                    f"(log_only mode, outbox_id={outbox.id})"
                )
            elif final_status == "held":
                logger.info(
                    f"Held template email '{template_type}' to {outbox.to_email} "
                    f"(paused mode, outbox_id={outbox.id})"
                )
            else:
                logger.info(
                    f"Queued template email '{template_type}' to {outbox.to_email} "
                    f"(outbox_id={outbox.id})"
                )

            # Transactional fast lane: once the surrounding transaction commits,
            # deliver this row asynchronously (seconds latency, off the request
            # thread). Only send_template_email — the transactional API — auto-
            # dispatches; campaigns/journeys go through queue_email + the throttled
            # drainer and must NOT. A broker hiccup can never break the caller; the
            # pending sweep is the recovery path.
            if dispatch and outbox.status == "queued":
                EmailSendingService._dispatch_send(outbox.id)

            return outbox

        except Exception as e:
            outbox.status = "failed"
            outbox.error_message = str(e)
            outbox.failed_at = timezone.now()
            outbox.save()
            logger.error(f"Failed to render template email: {e}", exc_info=True)
            raise

    @staticmethod
    def retry_failed_emails(max_emails: int = 100) -> dict[str, int]:
        """
        Retry failed emails that haven't exceeded retry limit.

        Args:
            max_emails: Maximum number of emails to retry

        Returns:
            Dictionary with counts:
                - attempted: int
                - succeeded: int
                - failed: int
        """
        # Skip retries if delivery mode is not live
        from core.models import SiteSettings

        site_settings = SiteSettings.get_settings()
        if site_settings.email_delivery_mode != "live":
            logger.info(
                f"Skipping email retry - delivery mode is '{site_settings.email_delivery_mode}'"
            )
            return {"attempted": 0, "succeeded": 0, "failed": 0}

        # Get failed emails that can be retried, but only ones that have waited out
        # the backoff since their last attempt — so running this on a schedule can't
        # hammer a flaky/greylisting recipient every tick.
        from datetime import timedelta

        from django.conf import settings as dj_settings
        from django.db.models import F

        backoff_minutes = int(getattr(dj_settings, "EMAIL_RETRY_BACKOFF_MINUTES", 15))
        cutoff = timezone.now() - timedelta(minutes=backoff_minutes)
        # Transactional rows only. Marketing (campaign) failures are owned by the
        # campaign drainer + its CampaignSend bookkeeping; re-sending a failed campaign
        # outbox here would deliver the email while its CampaignSend stays FAILED (no
        # outbox->CampaignSend sync), desyncing per-campaign metrics — and a budget
        # defer would flap it forever without progressing retry_count.
        failed_emails = EmailOutbox.objects.filter(
            status="failed",
            retry_count__lt=F("max_retries"),
            failed_at__lte=cutoff,
            priority__lt=EmailOutbox.PRIORITY_MARKETING,
        ).order_by("failed_at")[:max_emails]

        attempted = 0
        succeeded = 0
        failed = 0

        for email in failed_emails:
            attempted += 1
            if EmailSendingService.send_email(str(email.id)):
                succeeded += 1
            else:
                failed += 1

        logger.info(
            f"Retry completed: {attempted} attempted, {succeeded} succeeded, {failed} failed"
        )

        return {"attempted": attempted, "succeeded": succeeded, "failed": failed}

    @staticmethod
    def release_held_emails(send_now: bool = False) -> dict[str, int]:
        """
        Release all held emails by transitioning them to 'queued'.

        Args:
            send_now: If True, immediately attempt delivery after releasing.

        Returns:
            Dictionary with counts: released, sent (if send_now), failed (if send_now)
        """
        held_emails = EmailOutbox.objects.filter(status="held")
        released_count = held_emails.count()

        if released_count == 0:
            return {"released": 0, "sent": 0, "failed": 0}

        held_ids = list(held_emails.values_list("id", flat=True))
        EmailOutbox.objects.filter(id__in=held_ids).update(
            status="queued", queued_at=timezone.now()
        )

        logger.info(f"Released {released_count} held emails")

        result = {"released": released_count, "sent": 0, "failed": 0}

        if send_now:
            for outbox_id in held_ids:
                if EmailSendingService.send_email(str(outbox_id)):
                    result["sent"] += 1
                else:
                    result["failed"] += 1

        return result

    @staticmethod
    def _add_unsubscribe_footer(html_body: str, to_email: str, template_type: str) -> str:
        """
        Add unsubscribe footer to HTML email body.

        Args:
            html_body: Original HTML body
            to_email: Recipient email address
            template_type: Email template type

        Returns:
            HTML body with unsubscribe footer appended
        """
        from django.contrib.auth import get_user_model

        from accounts.models import CommunicationPreference

        User = get_user_model()

        try:
            user = User.objects.get(email=to_email)
            prefs = CommunicationPreference.objects.get(user=user)

            # Get unsubscribe URL
            from django.contrib.sites.models import Site

            site = Site.objects.get_current()
            unsubscribe_url = f"https://{site.domain}/accounts/unsubscribe/{prefs.unsubscribe_token}/?type={template_type}"

            # Skip if the body already contains an unsubscribe link (template
            # author added one, or footer was applied earlier in the pipeline).
            if "/accounts/unsubscribe/" in html_body:
                return html_body

            # Create footer HTML
            footer_html = f"""
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-family: system-ui, -apple-system, sans-serif; font-size: 12px; color: #666; text-align: center;">
                <p style="margin: 0 0 10px 0;">
                    You received this email because you are subscribed to our communications.
                </p>
                <p style="margin: 0;">
                    <a href="{unsubscribe_url}" style="color: #0066cc; text-decoration: underline;">
                        Unsubscribe from this type of email
                    </a>
                    &nbsp;|&nbsp;
                    <a href="https://{site.domain}/accounts/preferences/" style="color: #0066cc; text-decoration: underline;">
                        Manage all communication preferences
                    </a>
                </p>
            </div>
            """

            # Append footer before closing </body> tag if exists, otherwise append to end
            if "</body>" in html_body:
                html_body = html_body.replace("</body>", f"{footer_html}</body>")
            else:
                html_body = html_body + footer_html

        except (User.DoesNotExist, CommunicationPreference.DoesNotExist):
            # Guest user or no preferences - skip footer
            pass

        return html_body

    @staticmethod
    def _add_unsubscribe_footer_text(text_body: str, to_email: str, template_type: str) -> str:
        """
        Add unsubscribe footer to plain text email body.

        Args:
            text_body: Original text body
            to_email: Recipient email address
            template_type: Email template type

        Returns:
            Text body with unsubscribe footer appended
        """
        from django.contrib.auth import get_user_model

        from accounts.models import CommunicationPreference

        User = get_user_model()

        try:
            user = User.objects.get(email=to_email)
            prefs = CommunicationPreference.objects.get(user=user)

            # Get unsubscribe URL
            from django.contrib.sites.models import Site

            site = Site.objects.get_current()
            unsubscribe_url = f"https://{site.domain}/accounts/unsubscribe/{prefs.unsubscribe_token}/?type={template_type}"
            preferences_url = f"https://{site.domain}/accounts/preferences/"

            # Skip if the body already contains an unsubscribe link.
            if "/accounts/unsubscribe/" in text_body:
                return text_body

            # Create footer text
            footer_text = f"""

---
You received this email because you are subscribed to our communications.

Unsubscribe from this type of email: {unsubscribe_url}
Manage all communication preferences: {preferences_url}
"""

            text_body = text_body + footer_text

        except (User.DoesNotExist, CommunicationPreference.DoesNotExist):
            # Guest user or no preferences - skip footer
            pass

        return text_body
