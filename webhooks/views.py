"""
Webhook views for admin filtering, wizard, and documentation.
"""

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .events import WebhookEventCategory, get_events_by_category
from .models import WebhookEndpoint


@staff_member_required
def endpoint_wizard(request):
    """
    Wizard view for creating a new webhook endpoint.
    """
    if request.method == "POST":
        # Process form submission
        name = request.POST.get("name", "").strip()
        url = request.POST.get("url", "").strip()
        description = request.POST.get("description", "").strip()
        max_retries = int(request.POST.get("max_retries", 5))
        timeout_seconds = int(request.POST.get("timeout_seconds", 30))
        is_active = request.POST.get("is_active") == "on"

        # Handle events selection
        all_events = request.POST.get("all_events") == "true"
        events = ["*"] if all_events else request.POST.getlist("events")

        # Validate
        errors = []
        if not name:
            errors.append(_("Endpoint name is required"))
        if not url:
            errors.append(_("Webhook URL is required"))
        if not events:
            errors.append(_("At least one event must be selected"))

        if errors:
            messages.error(request, " ".join(errors))
            return redirect("webhooks:endpoint_wizard")

        # Create endpoint
        endpoint = WebhookEndpoint.objects.create(
            name=name,
            url=url,
            description=description,
            events=events,
            max_retries=max_retries,
            timeout_seconds=timeout_seconds,
            is_active=is_active,
        )

        # Show success message with secret (only shown once)
        messages.success(
            request,
            _(
                'Webhook endpoint "%(name)s" created successfully. '
                "Secret: %(secret)s - Save this now, it will not be shown again!"
            )
            % {"name": endpoint.name, "secret": endpoint.secret},
        )

        return redirect("admin:webhooks_webhookendpoint_changelist")

    # GET request - show wizard
    events_by_category = get_events_by_category()

    # Category icons mapping
    category_icons = {
        "order": "fa-shopping-cart",
        "payment": "fa-credit-card",
        "shipment": "fa-truck",
        "inventory": "fa-warehouse",
        "product": "fa-box",
        "customer": "fa-users",
        "subscription": "fa-sync-alt",
        "cart": "fa-shopping-basket",
        "refund": "fa-undo",
    }

    context = {
        "events_by_category": events_by_category,
        "category_icons": category_icons,
        "title": _("Create Webhook Endpoint"),
    }

    return render(request, "admin/webhooks/webhookendpoint/wizard.html", context)


@staff_member_required
def filter_endpoints(request):
    """
    AJAX endpoint for filtering webhook endpoints.
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    health = request.GET.get("health", "")

    queryset = WebhookEndpoint.objects.all()

    # Search filter
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(url__icontains=search) | Q(description__icontains=search)
        )

    # Status filter
    if status == "active":
        queryset = queryset.filter(is_active=True, is_disabled_by_failures=False)
    elif status == "inactive":
        queryset = queryset.filter(is_active=False)
    elif status == "disabled":
        queryset = queryset.filter(is_disabled_by_failures=True)

    # Health filter
    if health == "healthy":
        queryset = queryset.filter(consecutive_failures=0, is_disabled_by_failures=False)
    elif health == "degraded":
        queryset = queryset.filter(consecutive_failures__gt=0, is_disabled_by_failures=False)
    elif health == "unhealthy":
        queryset = queryset.filter(is_disabled_by_failures=True)

    # Order by name
    queryset = queryset.order_by("name")

    html = render_to_string(
        "admin/webhooks/partials/endpoint_cards.html", {"endpoints": queryset, "request": request}
    )

    return JsonResponse({"html": html, "count": queryset.count()})


@staff_member_required
def webhook_documentation(request):
    """
    Developer documentation page for webhooks.

    Displays comprehensive documentation including:
    - All available event types with descriptions
    - Payload schemas for each event category
    - Signature verification instructions with code examples
    - Headers sent with each webhook
    - Retry and failure policies
    """
    from core.version import __version__ as PLATFORM_VERSION

    from .openapi_webhooks import (
        CustomerWebhookData,
        InventoryWebhookData,
        OrderWebhookData,
        ProductWebhookData,
        ShipmentWebhookData,
        SubscriptionWebhookData,
    )

    def serializer_to_schema(serializer):
        """Convert a serializer to a simple schema dict for documentation."""
        schema = {}
        for field_name, field in serializer.fields.items():
            field_info = {
                "type": field.__class__.__name__.replace("Field", "").lower(),
                "required": field.required,
            }
            if hasattr(field, "help_text") and field.help_text:
                field_info["description"] = str(field.help_text)
            if hasattr(field, "allow_null"):
                field_info["nullable"] = field.allow_null
            schema[field_name] = field_info
        return schema

    # Build payload schemas
    payload_schemas = {
        "order": {
            "description": _("Payload for order-related events"),
            "fields": serializer_to_schema(OrderWebhookData()),
        },
        "product": {
            "description": _("Payload for product-related events"),
            "fields": serializer_to_schema(ProductWebhookData()),
        },
        "customer": {
            "description": _("Payload for customer-related events"),
            "fields": serializer_to_schema(CustomerWebhookData()),
        },
        "shipment": {
            "description": _("Payload for shipment-related events"),
            "fields": serializer_to_schema(ShipmentWebhookData()),
        },
        "inventory": {
            "description": _("Payload for inventory-related events"),
            "fields": serializer_to_schema(InventoryWebhookData()),
        },
        "subscription": {
            "description": _("Payload for subscription-related events"),
            "fields": serializer_to_schema(SubscriptionWebhookData()),
        },
    }

    # Category icons mapping
    category_icons = {
        WebhookEventCategory.ORDER: "fa-shopping-cart",
        WebhookEventCategory.PAYMENT: "fa-credit-card",
        WebhookEventCategory.SHIPMENT: "fa-truck",
        WebhookEventCategory.INVENTORY: "fa-warehouse",
        WebhookEventCategory.PRODUCT: "fa-box",
        WebhookEventCategory.CUSTOMER: "fa-users",
        WebhookEventCategory.SUBSCRIPTION: "fa-sync-alt",
        WebhookEventCategory.CART: "fa-shopping-basket",
        WebhookEventCategory.REFUND: "fa-undo",
    }

    context = {
        "title": _("Webhook Developer Documentation"),
        "version": PLATFORM_VERSION,
        "events_by_category": get_events_by_category(),
        "payload_schemas": payload_schemas,
        "category_icons": category_icons,
    }

    return render(request, "admin/webhooks/documentation.html", context)
