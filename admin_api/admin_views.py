import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Case, IntegerField, Q, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from .models import CustomerMessage, MessageReadReceipt

logger = logging.getLogger(__name__)


@staff_member_required
@require_GET
def filter_messages(request):
    """AJAX filter endpoint for CustomerMessage entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = CustomerMessage.objects.select_related("order", "read_by", "replied_by")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(email__icontains=search) | Q(subject__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    # Message type filter
    message_type = request.GET.get("message_type", "").strip()
    if message_type:
        queryset = queryset.filter(message_type=message_type)

    # Order: unread first, then by newest
    queryset = queryset.order_by(
        Case(
            When(status="unread", then=0),
            When(status="read", then=1),
            When(status="replied", then=2),
            When(status="archived", then=3),
            default=4,
            output_field=IntegerField(),
        ),
        "-created_at",
    )

    total_count = queryset.count()
    messages = queryset[:100]

    html = render_to_string(
        "admin/admin_api/partials/customermessage_cards.html",
        {"messages": messages},
        request=request,
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )


@staff_member_required
@require_POST
def reply_to_message(request, message_id):
    """AJAX endpoint for replying to a customer message."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    message = get_object_or_404(CustomerMessage, pk=message_id)

    if message.status == "replied":
        return JsonResponse(
            {
                "success": False,
                "error": _("This message has already been replied to."),
            },
            status=400,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": _("Invalid request data."),
            },
            status=400,
        )

    reply_text = data.get("reply_text", "").strip()
    if not reply_text:
        return JsonResponse(
            {
                "success": False,
                "error": _("Reply text is required."),
            },
            status=400,
        )

    send_email = data.get("send_email", True)

    # Save the reply and record per-user read receipt
    message.mark_as_replied(user=request.user, reply_text=reply_text)
    MessageReadReceipt.objects.get_or_create(
        source="contact_form",
        object_id=message.pk,
        user=request.user,
    )

    email_sent = False
    email_error = None

    # Send email if requested
    if send_email and message.email:
        try:
            from email_system.services.email_sender import EmailSendingService

            email_subject = f"Re: {message.subject}"

            html_body = (
                '<div style="font-family: Arial, sans-serif; max-width: 600px;">'
                f"<p>{reply_text.replace(chr(10), '<br>')}</p>"
                '<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">'
                '<p style="color: #666; font-size: 0.9em;">'
                "<strong>Original Message:</strong><br>"
                f"From: {message.name} &lt;{message.email}&gt;<br>"
                f"Subject: {message.subject}<br>"
                f"Date: {message.created_at.strftime('%B %d, %Y at %I:%M %p')}"
                "</p>"
                '<blockquote style="margin: 10px 0; padding: 10px; '
                'border-left: 3px solid #e0e0e0; color: #666;">'
                f"{message.message.replace(chr(10), '<br>')}"
                "</blockquote>"
                "</div>"
            )

            result = EmailSendingService.send_immediate(
                to_email=message.email,
                subject=email_subject,
                html_body=html_body,
                text_body=reply_text,
                template_type="message_reply",
                tags=["message_reply", f"message_{message.id}"],
            )

            email_sent = result.get("success", False)
            if not email_sent:
                email_error = result.get("message", "Failed to send email")

        except Exception as e:
            logger.error("Failed to send reply email for message %s: %s", message.id, e)
            email_error = str(e)

    response_data = {
        "success": True,
        "email_sent": email_sent,
        "message": _("Reply sent successfully.") if email_sent else _("Reply saved successfully."),
    }

    if email_error:
        response_data["email_error"] = email_error

    return JsonResponse(response_data)
