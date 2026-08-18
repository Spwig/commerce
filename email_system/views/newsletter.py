"""
Newsletter Management Views
Admin interface for creating and sending newsletters

Note: Leverages existing email_system template management infrastructure
for MJML editing, preview, and rendering. This module focuses on recipient
selection and sending logic.
"""

import csv
import io
import logging
from collections import Counter

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _

from customers.models import CustomerSegment
from email_system.models import EmailOutbox, EmailTemplate

User = get_user_model()
logger = logging.getLogger(__name__)

NEWSLETTER_TAG_PREFIX = "newsletter:"


def _newsletter_tag(newsletter_id):
    """Stable EmailOutbox tag identifying the newsletter template of a send.

    Aggregating sent statistics by this tag (instead of by subject) keeps each
    template's counts correct even when two newsletters share a subject or a
    subject is edited after sends have already gone out.
    """
    return f"{NEWSLETTER_TAG_PREFIX}{newsletter_id}"


@staff_member_required
def newsletter_list(request):
    """
    List all newsletters with filtering and search

    Features:
    - Filter by status (draft, sent)
    - Search by name
    - Show send statistics
    - Quick actions (edit, duplicate, delete)
    """
    site = Site.objects.get(pk=1)

    # Get all newsletter templates
    newsletters = EmailTemplate.objects.filter(
        site=site, template_type="newsletter", is_deleted=False
    ).order_by("-created_at")

    # Apply search filter
    search_query = request.GET.get("q", "")
    if search_query:
        newsletters = newsletters.filter(Q(subject__icontains=search_query))

    newsletters = list(newsletters)

    # Aggregate send statistics in a single query. New sends carry a stable
    # per-template ``newsletter:<id>`` tag, which is preferred over subject
    # matching: two newsletters can share a subject, and editing a subject would
    # otherwise reassign or hide earlier sends. Sends queued before tagging was
    # introduced have no such tag, so those legacy rows fall back to the original
    # subject-based match (keyed to the current newsletter subject) to avoid
    # regressing historical counts to zero.
    newsletter_ids = {str(newsletter.id) for newsletter in newsletters}
    subject_to_ids = {}
    for newsletter in newsletters:
        subject_to_ids.setdefault(newsletter.subject, []).append(str(newsletter.id))

    sent_counts = Counter()
    for tags, subject in EmailOutbox.objects.filter(
        template_type="newsletter", status="sent"
    ).values_list("tags", "subject"):
        tagged = False
        for tag in tags or []:
            if tag.startswith(NEWSLETTER_TAG_PREFIX):
                tagged = True
                nid = tag[len(NEWSLETTER_TAG_PREFIX) :]
                if nid in newsletter_ids:
                    sent_counts[nid] += 1
        if not tagged:
            # Legacy row (no newsletter tag): attribute by subject, mirroring the
            # previous per-newsletter subject count.
            for nid in subject_to_ids.get(subject, ()):
                sent_counts[nid] += 1

    newsletter_stats = [
        {
            "template": newsletter,
            "sent_count": sent_counts.get(str(newsletter.id), 0),
        }
        for newsletter in newsletters
    ]

    context = {
        "title": _("Newsletters"),
        "newsletter_stats": newsletter_stats,
        "search_query": search_query,
    }

    return render(request, "admin/email_system/newsletter_list.html", context)


@staff_member_required
def newsletter_create(request):
    """
    Create a new newsletter template and redirect to template editor

    This leverages the existing template_edit view for MJML editing.
    """
    from page_builder.translation_utils import get_available_languages, get_primary_language

    site = Site.objects.get(pk=1)

    # Get primary language (default) and all enabled languages from translation service
    primary_language = get_primary_language()
    available_languages = get_available_languages()

    if request.method == "POST":
        subject = request.POST.get("subject", _("New Newsletter"))
        language_code = request.POST.get("language_code", primary_language)

        try:
            # Create blank newsletter template
            newsletter = EmailTemplate.objects.create(
                site=site,
                template_type="newsletter",
                language_code=language_code,
                subject=subject,
                html_content="""<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text>
          <h1>Your Newsletter Title</h1>
          <p>Add your newsletter content here...</p>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>""",
                text_content="Your newsletter content...",
                is_active=True,
                is_system=False,
                created_by=request.user,
            )

            messages.success(request, _("Newsletter template created! Now customize the design."))

            # Redirect to existing template editor
            return redirect("email_system:template_edit", newsletter.id)

        except Exception as e:
            logger.error(f"Error creating newsletter: {e}", exc_info=True)
            messages.error(request, _("Error creating newsletter: %(error)s") % {"error": str(e)})

    # Get merchant's enabled languages only (from SiteLanguage model where is_active=True)
    context = {
        "title": _("Create Newsletter"),
        "available_languages": available_languages,
        "default_language": primary_language,
    }

    return render(request, "admin/email_system/newsletter_create.html", context)


@staff_member_required
def newsletter_edit(request, newsletter_id):
    """
    Redirect to template editor for editing newsletter content

    Newsletter editing uses the existing template_edit infrastructure.
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type="newsletter")

    # Redirect to existing template editor
    return redirect("email_system:template_edit", newsletter.id)


@staff_member_required
def newsletter_send(request, newsletter_id):
    """
    Send newsletter to selected recipients

    Features:
    - Select recipients by segment
    - Filter by customer status
    - Manual email list upload (CSV)
    - Preview recipient count
    - Schedule or send immediately
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type="newsletter")
    site = Site.objects.get(pk=1)

    if request.method == "POST":
        action = request.POST.get("action", "")

        if action == "preview_recipients":
            # Preview must count exactly what a send would queue, so route through
            # the same recipient selection (including any uploaded CSV) rather than
            # a separate DB-only count that ignores request.FILES.
            recipient_count = len(_get_recipients(request.POST, request.FILES))
            return JsonResponse({"success": True, "recipient_count": recipient_count})

        elif action == "send":
            try:
                # Get recipients based on filters
                recipients = _get_recipients(request.POST, request.FILES)

                if not recipients:
                    messages.error(
                        request, _("No recipients selected. Please select at least one recipient.")
                    )
                    return redirect("email_system:newsletter_send", newsletter.id)

                # Queue emails for sending
                from email_system.models import EmailAccount

                # Get default email account (or first active account)
                email_account = EmailAccount.objects.filter(site=site, is_active=True).first()

                if not email_account:
                    messages.error(
                        request,
                        _(
                            "No active email account found. Please configure an email account first."
                        ),
                    )
                    return redirect("email_system:newsletter_send", newsletter.id)

                from email_system.services.template_renderer import TemplateRenderer

                renderer = TemplateRenderer()
                newsletter_tag = _newsletter_tag(newsletter.id)

                # Build the whole batch first (rendering the stored MJML into the
                # final HTML/subject/text per recipient) so nothing is written
                # until every recipient is prepared.
                outbox_entries = []
                for recipient_email, recipient_name in recipients:
                    render_context = {
                        "customer_name": recipient_name or recipient_email,
                        "recipient_email": recipient_email,
                    }
                    subject, html_body, text_body = renderer.render_template(
                        newsletter,
                        render_context,
                        language=newsletter.language_code,
                        enable_tracking=False,
                    )
                    outbox_entries.append(
                        EmailOutbox(
                            site=site,
                            account=email_account,
                            to_email=recipient_email,
                            from_email=email_account.from_email,
                            from_name=email_account.from_name,
                            subject=subject,
                            html_body=html_body,
                            text_body=text_body,
                            template_type="newsletter",
                            tags=[newsletter_tag],
                            status="queued",
                            queued_at=timezone.now(),
                        )
                    )

                # Create the batch atomically: if any row fails (e.g. an
                # over-length address), the whole batch rolls back instead of
                # leaving a partial, re-sendable set queued.
                with transaction.atomic():
                    EmailOutbox.objects.bulk_create(outbox_entries)
                queued_count = len(outbox_entries)

                messages.success(
                    request,
                    _("Newsletter queued successfully! %(count)s emails will be sent.")
                    % {"count": queued_count},
                )

                return redirect("email_system:newsletter_list")

            except Exception as e:
                logger.error(f"Error sending newsletter {newsletter_id}: {e}", exc_info=True)
                messages.error(
                    request, _("Error sending newsletter: %(error)s") % {"error": str(e)}
                )

    # Get available customer segments
    segments = CustomerSegment.objects.filter(is_active=True).order_by("priority")

    # Total marketing-opted-in subscribers (what a store-wide blast can reach),
    # not every active account — keeps the figure honest post consent-gating.
    total_subscribers = len(_get_recipients(QueryDict(), {}))

    context = {
        "title": _("Send Newsletter"),
        "newsletter": newsletter,
        "segments": segments,
        "total_subscribers": total_subscribers,
    }

    return render(request, "admin/email_system/newsletter_send.html", context)


@staff_member_required
def newsletter_duplicate(request, newsletter_id):
    """
    Duplicate an existing newsletter
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type="newsletter")

    if request.method == "POST":
        # Only mutate on POST so the clone can't be triggered by a CSRF-exempt GET
        # (e.g. an attacker-planted <img src>), matching newsletter_delete.
        new_newsletter = newsletter.clone(user=request.user, set_active=True)
        new_newsletter.subject = f"{newsletter.subject} (Copy)"
        new_newsletter.save()

        messages.success(request, _("Newsletter duplicated successfully!"))

        return redirect("email_system:newsletter_edit", new_newsletter.id)

    context = {
        "title": _("Duplicate Newsletter"),
        "newsletter": newsletter,
    }

    return render(request, "admin/email_system/newsletter_duplicate_confirm.html", context)


@staff_member_required
def newsletter_delete(request, newsletter_id):
    """
    Soft delete a newsletter
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type="newsletter")

    if request.method == "POST":
        newsletter.delete(user=request.user)  # Soft delete

        messages.success(request, _("Newsletter deleted successfully!"))

        return redirect("email_system:newsletter_list")

    context = {
        "title": _("Delete Newsletter"),
        "newsletter": newsletter,
    }

    return render(request, "admin/email_system/newsletter_delete_confirm.html", context)


def _newsletter_consent_by_email(emails):
    """Map lowercased email -> whether that user may receive the newsletter.

    A newsletter is a marketing message, so ``should_send_email('newsletter')``
    enforces marketing opt-in (and double opt-in confirmation when the store
    requires it). Emails with no matching account are absent from the map.
    """
    from accounts.models import CommunicationPreference

    consent = {}
    prefs_qs = CommunicationPreference.objects.filter(user__email__in=emails).select_related("user")
    for prefs in prefs_qs:
        if prefs.user and prefs.user.email:
            consent[prefs.user.email.lower()] = prefs.should_send_email("newsletter")
    return consent


def _get_recipients(post_data, files):
    """
    Get list of recipients based on filters or CSV upload, filtered by consent.

    Recipients without marketing consent (or, when the store requires double
    opt-in, an unconfirmed address) are suppressed so newsletter blasts honour
    the same opt-in rules as every other marketing email.

    Args:
        post_data: POST data with filter parameters
        files: FILES data with CSV upload

    Returns:
        list: List of tuples (email, name)
    """
    candidates = []

    # Check if CSV was uploaded
    csv_file = files.get("csv_file")
    if csv_file:
        # Cap the upload so a huge file can't be read wholesale into memory.
        max_bytes = 5 * 1024 * 1024  # 5 MB
        if getattr(csv_file, "size", 0) and csv_file.size > max_bytes:
            raise Exception(_("CSV file is too large (max 5 MB)."))
        # Parse CSV file
        try:
            decoded_file = csv_file.read().decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(decoded_file))

            seen = set()
            for row in csv_reader:
                email = row.get("email", "").strip()
                name = row.get("name", "").strip()
                if not email:
                    continue
                # Deduplicate case-insensitively so a repeated address is not
                # queued (and delivered) more than once. Keep the first row.
                key = email.lower()
                if key in seen:
                    continue
                seen.add(key)
                candidates.append((email, name))
        except Exception as e:
            logger.error(f"Error parsing CSV: {e}", exc_info=True)
            raise Exception(_("Error parsing CSV file: %(error)s") % {"error": str(e)})

        # Suppress uploaded emails that belong to an account which has opted out
        # or not confirmed. Emails with no account are left to merchant judgement.
        consent = _newsletter_consent_by_email([e for e, _n in candidates])
        recipients = [
            (email, name) for email, name in candidates if consent.get(email.lower(), True)
        ]
    else:
        # Get recipients from database based on filters
        users = User.objects.filter(is_active=True, email__isnull=False).exclude(email="")

        # Filter by segment. Segment membership is computed dynamically via
        # CustomerSegment.determine_segment_for_user (there is no persisted
        # segment_id on CustomerMetrics to filter against).
        segment_ids = post_data.getlist("segments[]")
        if segment_ids:
            wanted_segments = {str(sid) for sid in segment_ids}
            matched_user_ids = [
                user.id
                for user in users
                if (segment := CustomerSegment.determine_segment_for_user(user))
                and str(segment.id) in wanted_segments
            ]
            users = users.filter(id__in=matched_user_ids)

        # Filter by customer status
        customer_status = post_data.get("customer_status", "")
        if customer_status == "has_orders":
            users = users.filter(orders__isnull=False).distinct()
        elif customer_status == "no_orders":
            users = users.filter(orders__isnull=True)

        # Build recipient list, gated on marketing consent. Users with no
        # preference record have never opted in, so they are excluded.
        from accounts.models import CommunicationPreference

        users = users.select_related("communication_preferences")
        recipients = []
        for user in users:
            try:
                prefs = user.communication_preferences
            except CommunicationPreference.DoesNotExist:
                continue
            if prefs.should_send_email("newsletter"):
                name = user.get_full_name() or user.username
                recipients.append((user.email, name))

    suppressed = len(candidates) - len(recipients) if csv_file else None
    if suppressed:
        logger.info("Newsletter: suppressed %s recipient(s) without marketing consent", suppressed)

    return recipients
