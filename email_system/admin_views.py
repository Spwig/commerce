"""
Email System Admin AJAX Views.
Provides AJAX filter endpoints for admin change list pages.
"""

import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from staff_roles.decorators import requires_permission

from .models import EmailAccount, EmailOutbox

logger = logging.getLogger(__name__)


@staff_member_required
@require_GET
def filter_email_outbox(request):
    """AJAX filter endpoint for EmailOutbox entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = EmailOutbox.objects.select_related("account").all()

    # Search filter (subject, to_email, or from_email)
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(subject__icontains=search)
            | Q(to_email__icontains=search)
            | Q(from_email__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    # Template type filter
    template_type = request.GET.get("template_type", "").strip()
    if template_type:
        queryset = queryset.filter(template_type=template_type)

    # Get total count before limiting
    total_count = queryset.count()

    # Order by most recent first, limit to 100 for performance
    emails = queryset.order_by("-created_at")[:100]

    html = render_to_string(
        "admin/email_system/partials/emailoutbox_cards.html", {"emails": emails}, request=request
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )


# ============================================================================
# Email Account AJAX Actions
# ============================================================================


@staff_member_required
@requires_permission("email_system.change_emailaccount", ajax=True)
@require_POST
def toggle_account_active(request, account_id):
    """Toggle email account active/inactive status."""
    try:
        account = EmailAccount.objects.get(id=account_id)

        if account.is_active and account.is_default:
            return JsonResponse(
                {
                    "success": False,
                    "message": _(
                        "Cannot deactivate the default email account. "
                        "Set another account as default first."
                    ),
                },
                status=400,
            )

        account.is_active = not account.is_active
        # Don't let disabling this account strand the store without a transactional
        # sending identity (order confirmations / password resets). clean() enforces the
        # same rule on the change form; this path saves directly, so check explicitly.
        if account.would_orphan_transactional():
            return JsonResponse(
                {"success": False, "message": EmailAccount.NO_TRANSACTIONAL_ACCOUNT_ERROR},
                status=400,
            )
        account.save(update_fields=["is_active", "updated_at"])

        return JsonResponse(
            {
                "success": True,
                "is_active": account.is_active,
                "message": _("Account enabled") if account.is_active else _("Account disabled"),
            }
        )
    except EmailAccount.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Account not found")}, status=404)
    except Exception as e:
        logger.error(f"Error toggling account {account_id}: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
@requires_permission("email_system.change_emailaccount", ajax=True)
@require_POST
def set_account_default(request, account_id):
    """Set an email account as the default sender."""
    from django.db import transaction

    try:
        with transaction.atomic():
            account = EmailAccount.objects.select_for_update().get(id=account_id)

            if not account.is_active:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Cannot set an inactive account as default"),
                    },
                    status=400,
                )

            # Clear existing default for this site
            EmailAccount.objects.filter(site=account.site, is_default=True).update(is_default=False)

            # Set new default
            account.is_default = True
            account.save(update_fields=["is_default", "updated_at"])

        return JsonResponse(
            {
                "success": True,
                "message": _("Default account updated to %(email)s")
                % {"email": account.from_email},
            }
        )
    except EmailAccount.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Account not found")}, status=404)
    except Exception as e:
        logger.error(f"Error setting default account {account_id}: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
@requires_permission("email_system.change_emailaccount", ajax=True)
@require_POST
def test_account_connection(request, account_id):
    """Test email account connection via provider healthcheck."""
    try:
        account = EmailAccount.objects.get(id=account_id)
        provider = account.get_provider_instance()

        result = provider.healthcheck()

        # Update connection status
        if result.get("success"):
            account.connection_status = "connected"
            account.connection_error = ""
            account.last_tested_at = timezone.now()
        else:
            account.connection_status = "error"
            account.connection_error = result.get("message", _("Connection test failed"))
            account.last_tested_at = timezone.now()

        account.save(
            update_fields=["connection_status", "connection_error", "last_tested_at", "updated_at"]
        )

        return JsonResponse(
            {
                "success": result.get("success", False),
                "connection_status": account.connection_status,
                "message": result.get("message", _("Connection test completed")),
            }
        )
    except EmailAccount.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Account not found")}, status=404)
    except Exception as e:
        logger.error(f"Error testing connection for account {account_id}: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
@requires_permission("email_system.delete_emailaccount", ajax=True)
@require_POST
def delete_account(request, account_id):
    """Delete an email account."""
    try:
        account = EmailAccount.objects.get(id=account_id)
        email = account.from_email

        if account.is_default:
            return JsonResponse(
                {
                    "success": False,
                    "message": _(
                        "Cannot delete the default email account. Set another account as default first."
                    ),
                },
                status=400,
            )

        # Don't delete the last active transactional-capable account (deletion bypasses
        # clean()): transactional mail must keep a sending identity.
        remaining_transactional = (
            EmailAccount.objects.filter(
                is_active=True,
                purpose__in=[EmailAccount.PURPOSE_TRANSACTIONAL, EmailAccount.PURPOSE_BOTH],
            )
            .exclude(id=account_id)
            .exists()
        )
        if not remaining_transactional:
            return JsonResponse(
                {"success": False, "message": EmailAccount.NO_TRANSACTIONAL_ACCOUNT_ERROR},
                status=400,
            )

        account.delete()

        return JsonResponse(
            {
                "success": True,
                "message": _("Account %(email)s deleted") % {"email": email},
            }
        )
    except EmailAccount.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Account not found")}, status=404)
    except Exception as e:
        logger.error(f"Error deleting account {account_id}: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
@requires_permission("email_system.change_emailaccount", ajax=True)
@require_POST
def bulk_account_action(request):
    """Handle bulk actions on email accounts."""
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            return JsonResponse(
                {"success": False, "message": _("Invalid request data")}, status=400
            )
        action = data.get("action")
        account_ids = data.get("account_ids", [])

        if not action or not account_ids:
            return JsonResponse(
                {
                    "success": False,
                    "message": _("Action and account selection are required"),
                },
                status=400,
            )

        accounts = EmailAccount.objects.filter(id__in=account_ids)
        count = accounts.count()

        if count == 0:
            return JsonResponse(
                {
                    "success": False,
                    "message": _("No accounts found"),
                },
                status=404,
            )

        if action == "enable":
            accounts.update(is_active=True, updated_at=timezone.now())
            message = _("%(count)d account(s) enabled") % {"count": count}
        elif action == "disable":
            if accounts.filter(is_default=True).exists():
                return JsonResponse(
                    {
                        "success": False,
                        "message": _(
                            "Cannot disable the default email account. Remove it from "
                            "selection or set another account as default first."
                        ),
                    },
                    status=400,
                )
            # Refuse if disabling the selection would leave no active transactional-capable
            # account (order confirmations / password resets would then have nowhere to go).
            remaining_transactional = (
                EmailAccount.objects.filter(
                    is_active=True,
                    purpose__in=[EmailAccount.PURPOSE_TRANSACTIONAL, EmailAccount.PURPOSE_BOTH],
                )
                .exclude(id__in=account_ids)
                .exists()
            )
            if not remaining_transactional:
                return JsonResponse(
                    {"success": False, "message": EmailAccount.NO_TRANSACTIONAL_ACCOUNT_ERROR},
                    status=400,
                )
            accounts.update(is_active=False, updated_at=timezone.now())
            message = _("%(count)d account(s) disabled") % {"count": count}
        elif action == "test_connection":
            # Test each account individually
            success_count = 0
            for account in accounts:
                try:
                    provider = account.get_provider_instance()
                    result = provider.healthcheck()
                    if result.get("success"):
                        account.connection_status = "connected"
                        account.connection_error = ""
                        success_count += 1
                    else:
                        account.connection_status = "error"
                        account.connection_error = result.get("message", "")
                    account.last_tested_at = timezone.now()
                    account.save(
                        update_fields=[
                            "connection_status",
                            "connection_error",
                            "last_tested_at",
                            "updated_at",
                        ]
                    )
                except Exception as exc:
                    logger.warning(
                        "Connection test failed for account %s: %s",
                        account.id,
                        exc,
                        exc_info=True,
                    )
                    account.connection_status = "error"
                    account.connection_error = str(exc) or _("Connection test failed")
                    account.last_tested_at = timezone.now()
                    account.save(
                        update_fields=[
                            "connection_status",
                            "connection_error",
                            "last_tested_at",
                            "updated_at",
                        ]
                    )
            message = _("%(success)d of %(total)d connection tests passed") % {
                "success": success_count,
                "total": count,
            }
        elif action == "delete":
            if not request.user.has_perm("email_system.delete_emailaccount"):
                return JsonResponse({"error": "forbidden"}, status=403)
            # Don't allow deleting default account
            default_in_selection = accounts.filter(is_default=True).exists()
            if default_in_selection:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _(
                            "Cannot delete the default email account. Remove it from selection or change the default first."
                        ),
                    },
                    status=400,
                )
            remaining_transactional = (
                EmailAccount.objects.filter(
                    is_active=True,
                    purpose__in=[EmailAccount.PURPOSE_TRANSACTIONAL, EmailAccount.PURPOSE_BOTH],
                )
                .exclude(id__in=account_ids)
                .exists()
            )
            if not remaining_transactional:
                return JsonResponse(
                    {"success": False, "message": EmailAccount.NO_TRANSACTIONAL_ACCOUNT_ERROR},
                    status=400,
                )
            accounts.delete()
            message = _("%(count)d account(s) deleted") % {"count": count}
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": _("Unknown action: %(action)s") % {"action": action},
                },
                status=400,
            )

        return JsonResponse({"success": True, "message": message})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": _("Invalid request data")}, status=400)
    except Exception as e:
        logger.error(f"Error in bulk account action: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": str(e)}, status=500)
