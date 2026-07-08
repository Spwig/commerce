"""
Newsletter Management Views
Admin interface for creating and sending newsletters

Note: Leverages existing email_system template management infrastructure
for MJML editing, preview, and rendering. This module focuses on recipient
selection and sending logic.
"""

import logging
import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.contrib.sites.models import Site
from django.utils import timezone
from datetime import datetime

from email_system.models import EmailTemplate, EmailOutbox
from customers.models import CustomerSegment, CustomerMetrics
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


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
        site=site,
        template_type='newsletter',
        is_deleted=False
    ).order_by('-created_at')

    # Apply search filter
    search_query = request.GET.get('q', '')
    if search_query:
        newsletters = newsletters.filter(
            Q(subject__icontains=search_query)
        )

    # Get send statistics for each newsletter
    newsletter_stats = []
    for newsletter in newsletters:
        sent_count = EmailOutbox.objects.filter(
            template_type='newsletter',
            subject=newsletter.subject,
            status='sent'
        ).count()

        newsletter_stats.append({
            'template': newsletter,
            'sent_count': sent_count,
        })

    context = {
        'title': _('Newsletters'),
        'newsletter_stats': newsletter_stats,
        'search_query': search_query,
    }

    return render(request, 'admin/email_system/newsletter_list.html', context)


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

    if request.method == 'POST':
        subject = request.POST.get('subject', _('New Newsletter'))
        language_code = request.POST.get('language_code', primary_language)

        try:
            # Create blank newsletter template
            newsletter = EmailTemplate.objects.create(
                site=site,
                template_type='newsletter',
                language_code=language_code,
                subject=subject,
                html_content='''<mjml>
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
</mjml>''',
                text_content='Your newsletter content...',
                is_active=True,
                is_system=False,
                created_by=request.user
            )

            messages.success(
                request,
                _('Newsletter template created! Now customize the design.')
            )

            # Redirect to existing template editor
            return redirect('email_system:template_edit', newsletter.id)

        except Exception as e:
            logger.error(f"Error creating newsletter: {e}", exc_info=True)
            messages.error(
                request,
                _('Error creating newsletter: %(error)s') % {'error': str(e)}
            )

    # Get merchant's enabled languages only (from SiteLanguage model where is_active=True)
    context = {
        'title': _('Create Newsletter'),
        'available_languages': available_languages,
        'default_language': primary_language,
    }

    return render(request, 'admin/email_system/newsletter_create.html', context)


@staff_member_required
def newsletter_edit(request, newsletter_id):
    """
    Redirect to template editor for editing newsletter content

    Newsletter editing uses the existing template_edit infrastructure.
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type='newsletter')

    # Redirect to existing template editor
    return redirect('email_system:template_edit', newsletter.id)


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
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type='newsletter')
    site = Site.objects.get(pk=1)

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'preview_recipients':
            # Calculate recipient count based on filters
            recipient_count = _calculate_recipient_count(request.POST)
            return JsonResponse({
                'success': True,
                'recipient_count': recipient_count
            })

        elif action == 'send':
            try:
                # Get recipients based on filters
                recipients = _get_recipients(request.POST, request.FILES)

                if not recipients:
                    messages.error(request, _('No recipients selected. Please select at least one recipient.'))
                    return redirect('email_system:newsletter_send', newsletter.id)

                # Queue emails for sending
                from email_system.models import EmailAccount

                # Get default email account (or first active account)
                email_account = EmailAccount.objects.filter(
                    site=site,
                    is_active=True
                ).first()

                if not email_account:
                    messages.error(request, _('No active email account found. Please configure an email account first.'))
                    return redirect('email_system:newsletter_send', newsletter.id)

                queued_count = 0
                for recipient_email, recipient_name in recipients:
                    # Create outbox entry
                    EmailOutbox.objects.create(
                        site=site,
                        account=email_account,
                        to_email=recipient_email,
                        from_email=email_account.from_email,
                        from_name=email_account.from_name,
                        subject=newsletter.subject,
                        html_body=newsletter.html_content,
                        text_body=newsletter.text_content or '',
                        template_type='newsletter',
                        status='queued',
                        queued_at=timezone.now()
                    )
                    queued_count += 1

                messages.success(
                    request,
                    _('Newsletter queued successfully! %(count)s emails will be sent.') % {'count': queued_count}
                )

                return redirect('email_system:newsletter_list')

            except Exception as e:
                logger.error(f"Error sending newsletter {newsletter_id}: {e}", exc_info=True)
                messages.error(
                    request,
                    _('Error sending newsletter: %(error)s') % {'error': str(e)}
                )

    # Get available customer segments
    segments = CustomerSegment.objects.filter(is_active=True).order_by('priority')

    # Calculate total subscribers
    total_subscribers = User.objects.filter(
        is_active=True,
        email__isnull=False
    ).exclude(email='').count()

    context = {
        'title': _('Send Newsletter'),
        'newsletter': newsletter,
        'segments': segments,
        'total_subscribers': total_subscribers,
    }

    return render(request, 'admin/email_system/newsletter_send.html', context)


@staff_member_required
def newsletter_duplicate(request, newsletter_id):
    """
    Duplicate an existing newsletter
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type='newsletter')

    # Clone the newsletter
    new_newsletter = newsletter.clone(user=request.user, set_active=True)
    new_newsletter.subject = f"{newsletter.subject} (Copy)"
    new_newsletter.save()

    messages.success(
        request,
        _('Newsletter duplicated successfully!')
    )

    return redirect('email_system:newsletter_edit', new_newsletter.id)


@staff_member_required
def newsletter_delete(request, newsletter_id):
    """
    Soft delete a newsletter
    """
    newsletter = get_object_or_404(EmailTemplate, id=newsletter_id, template_type='newsletter')

    if request.method == 'POST':
        newsletter.delete(user=request.user)  # Soft delete

        messages.success(
            request,
            _('Newsletter deleted successfully!')
        )

        return redirect('email_system:newsletter_list')

    context = {
        'title': _('Delete Newsletter'),
        'newsletter': newsletter,
    }

    return render(request, 'admin/email_system/newsletter_delete_confirm.html', context)


def _calculate_recipient_count(post_data):
    """
    Calculate number of recipients based on filters

    Args:
        post_data: POST data with filter parameters

    Returns:
        int: Number of recipients
    """
    recipients = User.objects.filter(
        is_active=True,
        email__isnull=False
    ).exclude(email='')

    # Filter by segment
    segment_ids = post_data.getlist('segments[]')
    if segment_ids:
        # Get users in selected segments
        segment_user_ids = CustomerMetrics.objects.filter(
            segment_id__in=segment_ids
        ).values_list('user_id', flat=True)
        recipients = recipients.filter(id__in=segment_user_ids)

    # Filter by customer status
    customer_status = post_data.get('customer_status', '')
    if customer_status == 'has_orders':
        recipients = recipients.filter(orders__isnull=False).distinct()
    elif customer_status == 'no_orders':
        recipients = recipients.filter(orders__isnull=True)

    return recipients.count()


def _get_recipients(post_data, files):
    """
    Get list of recipients based on filters or CSV upload

    Args:
        post_data: POST data with filter parameters
        files: FILES data with CSV upload

    Returns:
        list: List of tuples (email, name)
    """
    recipients = []

    # Check if CSV was uploaded
    csv_file = files.get('csv_file')
    if csv_file:
        # Parse CSV file
        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(decoded_file))

            for row in csv_reader:
                email = row.get('email', '').strip()
                name = row.get('name', '').strip()
                if email:
                    recipients.append((email, name))
        except Exception as e:
            logger.error(f"Error parsing CSV: {e}", exc_info=True)
            raise Exception(_('Error parsing CSV file: %(error)s') % {'error': str(e)})
    else:
        # Get recipients from database based on filters
        users = User.objects.filter(
            is_active=True,
            email__isnull=False
        ).exclude(email='')

        # Filter by segment
        segment_ids = post_data.getlist('segments[]')
        if segment_ids:
            segment_user_ids = CustomerMetrics.objects.filter(
                segment_id__in=segment_ids
            ).values_list('user_id', flat=True)
            users = users.filter(id__in=segment_user_ids)

        # Filter by customer status
        customer_status = post_data.get('customer_status', '')
        if customer_status == 'has_orders':
            users = users.filter(orders__isnull=False).distinct()
        elif customer_status == 'no_orders':
            users = users.filter(orders__isnull=True)

        # Build recipient list
        for user in users:
            name = user.get_full_name() or user.username
            recipients.append((user.email, name))

    return recipients
