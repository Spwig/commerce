"""
Page Builder Admin Views
Admin-specific views for AJAX endpoints
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from .models import Page, PageTemplate, RuleGroup, RuleGroupMember, VisibilityRule


@staff_member_required
def filter_pages(request):
    """
    AJAX endpoint for filtering pages in admin

    Query Parameters:
    - search: Search by title or slug
    - page_type: Filter by page type
    - status: Filter by status (draft/published/archived)
    - theme: Filter by theme (use 'none' for no theme)
    - is_default: Filter by default page (yes/no)
    - requires_auth: Filter by requires authentication (yes/no)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all pages
    pages = Page.objects.select_related("theme", "created_by").prefetch_related("elements")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        pages = pages.filter(
            Q(title__icontains=search)
            | Q(slug__icontains=search)
            | Q(meta_title__icontains=search)
            | Q(meta_description__icontains=search)
        )

    # Page type filter
    page_type = request.GET.get("page_type", "")
    if page_type:
        pages = pages.filter(page_type=page_type)

    # Status filter
    status = request.GET.get("status", "")
    if status:
        pages = pages.filter(status=status)

    # Theme filter
    theme = request.GET.get("theme", "")
    if theme == "none":
        pages = pages.filter(theme__isnull=True)
    elif theme:
        try:
            theme_id = int(theme)
            pages = pages.filter(theme_id=theme_id)
        except ValueError:
            pass

    # Default page filter
    is_default = request.GET.get("is_default", "")
    if is_default == "yes":
        pages = pages.filter(is_default_for_type=True)
    elif is_default == "no":
        pages = pages.filter(is_default_for_type=False)

    # Requires auth filter
    requires_auth = request.GET.get("requires_auth", "")
    if requires_auth == "yes":
        pages = pages.filter(requires_auth=True)
    elif requires_auth == "no":
        pages = pages.filter(requires_auth=False)

    # Order by updated_at descending
    pages = pages.order_by("-updated_at")

    # Render partial template
    html = render_to_string(
        "admin/page_builder/partials/page_cards.html", {"pages": pages, "request": request}
    )

    return JsonResponse({"html": html, "count": pages.count()})


@staff_member_required
def filter_page_templates(request):
    """
    AJAX endpoint for filtering page templates in admin

    Query Parameters:
    - search: Search by name or description
    - page_type: Filter by page type
    - category: Filter by category
    - is_public: Filter by public visibility (yes/no)
    - is_premium: Filter by premium status (yes/no)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all templates
    templates = PageTemplate.objects.select_related("created_by")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        templates = templates.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Page type filter
    page_type = request.GET.get("page_type", "")
    if page_type:
        templates = templates.filter(page_type=page_type)

    # Category filter
    category = request.GET.get("category", "")
    if category:
        templates = templates.filter(category=category)

    # Public filter
    is_public = request.GET.get("is_public", "")
    if is_public == "yes":
        templates = templates.filter(is_public=True)
    elif is_public == "no":
        templates = templates.filter(is_public=False)

    # Premium filter
    is_premium = request.GET.get("is_premium", "")
    if is_premium == "yes":
        templates = templates.filter(is_premium=True)
    elif is_premium == "no":
        templates = templates.filter(is_premium=False)

    # Order by usage_count descending, then by created_at
    templates = templates.order_by("-usage_count", "-created_at")

    # Render partial template
    html = render_to_string(
        "admin/page_builder/partials/pagetemplate_cards.html",
        {"templates": templates, "request": request},
    )

    return JsonResponse({"html": html, "count": templates.count()})


@staff_member_required
def filter_visibility_rules(request):
    """
    AJAX endpoint for filtering visibility rules in admin

    Query Parameters:
    - search: Search by name or description
    - category: Filter by rule category (geo, user, device, time, behavioral, ecommerce, language)
    - rule_type: Filter by specific rule type
    - operator: Filter by operator
    - status: Filter by active status (active/inactive)
    - priority: Filter by priority level (high/medium/low)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all rules
    rules = VisibilityRule.objects.all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        rules = rules.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Category filter (maps to rule_type prefixes)
    category = request.GET.get("category", "")
    if category:
        category_mappings = {
            "geo": ["geo_country", "geo_region", "geo_city", "geo_timezone"],
            "user": [
                "user_logged_in",
                "user_group",
                "user_segment",
                "user_lifetime_value",
                "user_order_count",
            ],
            "device": [
                "device_type",
                "browser",
                "operating_system",
                "screen_size",
                "connection_speed",
            ],
            "time": ["date_range", "time_range", "day_of_week", "business_hours"],
            "behavioral": [
                "first_visit",
                "visit_count",
                "page_views",
                "time_on_site",
                "referrer",
                "utm_campaign",
            ],
            "ecommerce": [
                "cart_value",
                "cart_items",
                "has_purchased",
                "abandoned_cart",
                "wishlist_items",
            ],
            "language": ["browser_language", "selected_language", "selected_currency"],
        }
        if category in category_mappings:
            rules = rules.filter(rule_type__in=category_mappings[category])

    # Rule type filter
    rule_type = request.GET.get("rule_type", "")
    if rule_type:
        rules = rules.filter(rule_type=rule_type)

    # Operator filter
    operator = request.GET.get("operator", "")
    if operator:
        rules = rules.filter(operator=operator)

    # Status filter
    status = request.GET.get("status", "")
    if status == "active":
        rules = rules.filter(is_active=True)
    elif status == "inactive":
        rules = rules.filter(is_active=False)

    # Priority filter
    priority = request.GET.get("priority", "")
    if priority == "high":
        rules = rules.filter(priority__lte=3)
    elif priority == "medium":
        rules = rules.filter(priority__gte=4, priority__lte=7)
    elif priority == "low":
        rules = rules.filter(priority__gte=8)

    # Order by priority, then by name
    rules = rules.order_by("priority", "name")

    # Render partial template
    html = render_to_string(
        "admin/page_builder/visibilityrule/partials/rule_cards.html",
        {"rules": rules, "request": request},
    )

    return JsonResponse({"html": html, "count": rules.count()})


@staff_member_required
@require_http_methods(["POST"])
def toggle_visibility_rule_status(request, rule_id):
    """
    AJAX endpoint to toggle visibility rule active status
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        rule = VisibilityRule.objects.get(pk=rule_id)

        # Parse the request body to get the desired state
        try:
            data = json.loads(request.body)
            is_active = data.get("is_active", not rule.is_active)
        except (json.JSONDecodeError, KeyError):
            # Toggle if no specific value provided
            is_active = not rule.is_active

        rule.is_active = is_active
        rule.save(update_fields=["is_active"])

        return JsonResponse(
            {
                "success": True,
                "is_active": rule.is_active,
                "message": f'Rule "{rule.name}" is now {"active" if rule.is_active else "inactive"}',
            }
        )

    except VisibilityRule.DoesNotExist:
        return JsonResponse({"error": "Rule not found"}, status=404)


@staff_member_required
def filter_rule_groups(request):
    """
    AJAX endpoint for filtering rule groups in admin

    Query Parameters:
    - search: Search by name or description
    - logic_operator: Filter by logic operator (AND/OR)
    - status: Filter by active status (active/inactive)
    - parent_type: Filter by parent type (root/nested)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all groups
    groups = RuleGroup.objects.prefetch_related(
        "rules", "child_groups", "rulegroupmember_set__rule"
    ).select_related("parent_group")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        groups = groups.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Logic operator filter
    logic_operator = request.GET.get("logic_operator", "")
    if logic_operator:
        groups = groups.filter(logic_operator=logic_operator)

    # Status filter
    status = request.GET.get("status", "")
    if status == "active":
        groups = groups.filter(is_active=True)
    elif status == "inactive":
        groups = groups.filter(is_active=False)

    # Parent type filter
    parent_type = request.GET.get("parent_type", "")
    if parent_type == "root":
        groups = groups.filter(parent_group__isnull=True)
    elif parent_type == "nested":
        groups = groups.filter(parent_group__isnull=False)

    # Order by name
    groups = groups.order_by("name")

    # Render partial template
    html = render_to_string(
        "admin/page_builder/rulegroup/partials/group_cards.html",
        {"groups": groups, "request": request},
    )

    return JsonResponse({"html": html, "count": groups.count()})


@staff_member_required
@require_http_methods(["POST"])
def toggle_rule_group_status(request, group_id):
    """
    AJAX endpoint to toggle rule group active status
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        group = RuleGroup.objects.get(pk=group_id)

        # Parse the request body to get the desired state
        try:
            data = json.loads(request.body)
            is_active = data.get("is_active", not group.is_active)
        except (json.JSONDecodeError, KeyError):
            # Toggle if no specific value provided
            is_active = not group.is_active

        group.is_active = is_active
        group.save(update_fields=["is_active"])

        return JsonResponse(
            {
                "success": True,
                "is_active": group.is_active,
                "message": f'Group "{group.name}" is now {"active" if group.is_active else "inactive"}',
            }
        )

    except RuleGroup.DoesNotExist:
        return JsonResponse({"error": "Group not found"}, status=404)


@staff_member_required
def rule_builder_view(request, group_id=None):
    """
    Rule Builder admin view - Visual drag-and-drop rule builder

    Can be accessed in two modes:
    - New: /admin/page_builder/rulegroup/builder/
    - Edit: /admin/page_builder/rulegroup/builder/<group_id>/
    """
    from django.contrib import admin

    # Get existing group if editing
    rule_group = None
    rules_tree = []

    if group_id:
        rule_group = get_object_or_404(RuleGroup, id=group_id)
        rules_tree = _build_rules_tree(rule_group)

    # Get all saved rule groups for library
    all_groups = (
        RuleGroup.objects.filter(parent_group__isnull=True)
        .prefetch_related("rules")
        .order_by("name")
    )

    # Get all saved rules (active ones)
    saved_rules = VisibilityRule.objects.filter(is_active=True).order_by("name")

    # Rule types configuration for the library panel
    rule_types_by_category = {
        "geo": {
            "label": str(_("Geographic")),
            "icon": "fas fa-globe",
            "types": [
                {"id": "geo_country", "label": str(_("Country"))},
                {"id": "geo_region", "label": str(_("Region/State"))},
                {"id": "geo_city", "label": str(_("City"))},
                {"id": "geo_timezone", "label": str(_("Timezone"))},
            ],
        },
        "user": {
            "label": str(_("User")),
            "icon": "fas fa-user",
            "types": [
                {"id": "user_logged_in", "label": str(_("User Logged In"))},
                {"id": "user_group", "label": str(_("User Group"))},
                {"id": "user_segment", "label": str(_("Customer Segment"))},
                {"id": "user_lifetime_value", "label": str(_("Lifetime Value"))},
                {"id": "user_order_count", "label": str(_("Order Count"))},
            ],
        },
        "device": {
            "label": str(_("Device")),
            "icon": "fas fa-mobile-alt",
            "types": [
                {"id": "device_type", "label": str(_("Device Type"))},
                {"id": "browser", "label": str(_("Browser"))},
                {"id": "operating_system", "label": str(_("Operating System"))},
                {"id": "screen_size", "label": str(_("Screen Size"))},
                {"id": "connection_speed", "label": str(_("Connection Speed"))},
            ],
        },
        "time": {
            "label": str(_("Time")),
            "icon": "fas fa-clock",
            "types": [
                {"id": "date_range", "label": str(_("Date Range"))},
                {"id": "time_range", "label": str(_("Time Range"))},
                {"id": "day_of_week", "label": str(_("Day of Week"))},
                {"id": "business_hours", "label": str(_("Business Hours"))},
            ],
        },
        "behavioral": {
            "label": str(_("Behavioral")),
            "icon": "fas fa-chart-line",
            "types": [
                {"id": "first_visit", "label": str(_("First Visit"))},
                {"id": "visit_count", "label": str(_("Visit Count"))},
                {"id": "page_views", "label": str(_("Page Views"))},
                {"id": "time_on_site", "label": str(_("Time on Site"))},
                {"id": "referrer", "label": str(_("Referrer"))},
                {"id": "utm_campaign", "label": str(_("UTM Campaign"))},
            ],
        },
        "ecommerce": {
            "label": str(_("E-commerce")),
            "icon": "fas fa-shopping-cart",
            "types": [
                {"id": "cart_value", "label": str(_("Cart Value"))},
                {"id": "cart_items", "label": str(_("Cart Items Count"))},
                {"id": "has_purchased", "label": str(_("Has Purchased"))},
                {"id": "abandoned_cart", "label": str(_("Abandoned Cart"))},
                {"id": "wishlist_items", "label": str(_("Wishlist Items"))},
            ],
        },
        "language": {
            "label": str(_("Language")),
            "icon": "fas fa-language",
            "types": [
                {"id": "browser_language", "label": str(_("Browser Language"))},
                {"id": "selected_language", "label": str(_("Selected Language"))},
                {"id": "selected_currency", "label": str(_("Selected Currency"))},
            ],
        },
    }

    # Operators configuration
    operators = [
        {"id": "equals", "label": str(_("Equals")), "symbol": "="},
        {"id": "not_equals", "label": str(_("Not Equals")), "symbol": "≠"},
        {"id": "contains", "label": str(_("Contains")), "symbol": "⊃"},
        {"id": "not_contains", "label": str(_("Not Contains")), "symbol": "⊅"},
        {"id": "greater_than", "label": str(_("Greater Than")), "symbol": ">"},
        {"id": "less_than", "label": str(_("Less Than")), "symbol": "<"},
        {"id": "greater_or_equal", "label": str(_("Greater or Equal")), "symbol": "≥"},
        {"id": "less_or_equal", "label": str(_("Less or Equal")), "symbol": "≤"},
        {"id": "in_list", "label": str(_("In List")), "symbol": "∈"},
        {"id": "not_in_list", "label": str(_("Not in List")), "symbol": "∉"},
        {"id": "between", "label": str(_("Between")), "symbol": "↔"},
        {"id": "is_true", "label": str(_("Is True")), "symbol": "✓"},
        {"id": "is_false", "label": str(_("Is False")), "symbol": "✗"},
    ]

    # Build saved rules JSON for JavaScript
    saved_rules_data = [
        {
            "id": rule.id,
            "name": rule.name,
            "description": rule.description,
            "rule_type": rule.rule_type,
            "operator": rule.operator,
            "value": rule.value,
            "is_active": rule.is_active,
            "priority": rule.priority,
        }
        for rule in saved_rules
    ]

    context = {
        **admin.site.each_context(request),
        "title": _("Rule Builder") + (f" - {rule_group.name}" if rule_group else ""),
        "rule_group": rule_group,
        "all_groups": all_groups,
        "saved_rules": saved_rules,
        "saved_rules_json": json.dumps(saved_rules_data),
        "rules_tree_json": json.dumps(rules_tree),
        "rule_types_json": json.dumps(rule_types_by_category),
        "operators_json": json.dumps(operators),
        "rule_types": rule_types_by_category,
        "opts": RuleGroup._meta,
    }

    return TemplateResponse(request, "admin/page_builder/rulegroup/builder.html", context)


def _build_rules_tree(group):
    """Build a nested tree structure for a rule group"""
    members = RuleGroupMember.objects.filter(group=group).select_related("rule").order_by("order")

    tree = {
        "id": group.id,
        "type": "group",
        "name": group.name,
        "description": group.description,
        "logic_operator": group.logic_operator,
        "is_active": group.is_active,
        "priority": group.priority,
        "children": [],
    }

    # Add rules
    for member in members:
        rule = member.rule
        tree["children"].append(
            {
                "id": rule.id,
                "type": "rule",
                "name": rule.name,
                "description": rule.description,
                "rule_type": rule.rule_type,
                "operator": rule.operator,
                "value": rule.value,
                "is_active": rule.is_active,
                "priority": rule.priority,
                "order": member.order,
            }
        )

    # Add child groups recursively
    for child_group in group.child_groups.all().order_by("priority", "name"):
        tree["children"].append(_build_rules_tree(child_group))

    return tree


@staff_member_required
def rule_builder_popup_view(request, group_id=None):
    """
    Rule Builder popup view for Page Builder integration

    Accessed from within the visual page builder when configuring
    element visibility rules. Returns a simpler layout optimized
    for popup display.
    """

    # Get existing group if editing
    rule_group = None
    rules_tree = []

    if group_id:
        rule_group = get_object_or_404(RuleGroup, id=group_id)
        rules_tree = _build_rules_tree(rule_group)

    # Get all saved rule groups for quick selection
    all_groups = (
        RuleGroup.objects.filter(parent_group__isnull=True)
        .prefetch_related("rules")
        .order_by("name")
    )

    # Get all saved rules (active ones)
    saved_rules = VisibilityRule.objects.filter(is_active=True).order_by("name")

    # Rule types configuration
    rule_types_by_category = {
        "geo": {
            "label": str(_("Geographic")),
            "icon": "fas fa-globe",
            "types": [
                {"id": "geo_country", "label": str(_("Country"))},
                {"id": "geo_region", "label": str(_("Region/State"))},
                {"id": "geo_city", "label": str(_("City"))},
                {"id": "geo_timezone", "label": str(_("Timezone"))},
            ],
        },
        "user": {
            "label": str(_("User")),
            "icon": "fas fa-user",
            "types": [
                {"id": "user_logged_in", "label": str(_("User Logged In"))},
                {"id": "user_group", "label": str(_("User Group"))},
                {"id": "user_segment", "label": str(_("Customer Segment"))},
                {"id": "user_lifetime_value", "label": str(_("Lifetime Value"))},
                {"id": "user_order_count", "label": str(_("Order Count"))},
            ],
        },
        "device": {
            "label": str(_("Device")),
            "icon": "fas fa-mobile-alt",
            "types": [
                {"id": "device_type", "label": str(_("Device Type"))},
                {"id": "browser", "label": str(_("Browser"))},
                {"id": "operating_system", "label": str(_("Operating System"))},
                {"id": "screen_size", "label": str(_("Screen Size"))},
                {"id": "connection_speed", "label": str(_("Connection Speed"))},
            ],
        },
        "time": {
            "label": str(_("Time")),
            "icon": "fas fa-clock",
            "types": [
                {"id": "date_range", "label": str(_("Date Range"))},
                {"id": "time_range", "label": str(_("Time Range"))},
                {"id": "day_of_week", "label": str(_("Day of Week"))},
                {"id": "business_hours", "label": str(_("Business Hours"))},
            ],
        },
        "behavioral": {
            "label": str(_("Behavioral")),
            "icon": "fas fa-chart-line",
            "types": [
                {"id": "first_visit", "label": str(_("First Visit"))},
                {"id": "visit_count", "label": str(_("Visit Count"))},
                {"id": "page_views", "label": str(_("Page Views"))},
                {"id": "time_on_site", "label": str(_("Time on Site"))},
                {"id": "referrer", "label": str(_("Referrer"))},
                {"id": "utm_campaign", "label": str(_("UTM Campaign"))},
            ],
        },
        "ecommerce": {
            "label": str(_("E-commerce")),
            "icon": "fas fa-shopping-cart",
            "types": [
                {"id": "cart_value", "label": str(_("Cart Value"))},
                {"id": "cart_items", "label": str(_("Cart Items Count"))},
                {"id": "has_purchased", "label": str(_("Has Purchased"))},
                {"id": "abandoned_cart", "label": str(_("Abandoned Cart"))},
                {"id": "wishlist_items", "label": str(_("Wishlist Items"))},
            ],
        },
        "language": {
            "label": str(_("Language")),
            "icon": "fas fa-language",
            "types": [
                {"id": "browser_language", "label": str(_("Browser Language"))},
                {"id": "selected_language", "label": str(_("Selected Language"))},
                {"id": "selected_currency", "label": str(_("Selected Currency"))},
            ],
        },
    }

    # Operators configuration
    operators = [
        {"id": "equals", "label": str(_("Equals")), "symbol": "="},
        {"id": "not_equals", "label": str(_("Not Equals")), "symbol": "≠"},
        {"id": "contains", "label": str(_("Contains")), "symbol": "⊃"},
        {"id": "not_contains", "label": str(_("Not Contains")), "symbol": "⊅"},
        {"id": "greater_than", "label": str(_("Greater Than")), "symbol": ">"},
        {"id": "less_than", "label": str(_("Less Than")), "symbol": "<"},
        {"id": "greater_or_equal", "label": str(_("Greater or Equal")), "symbol": "≥"},
        {"id": "less_or_equal", "label": str(_("Less or Equal")), "symbol": "≤"},
        {"id": "in_list", "label": str(_("In List")), "symbol": "∈"},
        {"id": "not_in_list", "label": str(_("Not in List")), "symbol": "∉"},
        {"id": "between", "label": str(_("Between")), "symbol": "↔"},
        {"id": "is_true", "label": str(_("Is True")), "symbol": "✓"},
        {"id": "is_false", "label": str(_("Is False")), "symbol": "✗"},
    ]

    context = {
        "title": _("Select Visibility Rules"),
        "rule_group": rule_group,
        "all_groups": all_groups,
        "saved_rules": saved_rules,
        "rules_tree_json": json.dumps(rules_tree),
        "rule_types_json": json.dumps(rule_types_by_category),
        "operators_json": json.dumps(operators),
        "rule_types": rule_types_by_category,
        "is_popup": True,
    }

    return TemplateResponse(request, "admin/page_builder/rulegroup/builder_popup.html", context)


@staff_member_required
def visibility_rule_wizard_view(request, rule_id=None):
    """
    Visibility Rule Wizard - Step-by-step interface for creating/editing rules

    Replaces the default Django admin add form with a guided wizard experience.
    URL: /admin/page_builder/visibilityrule/wizard/
    Edit: /admin/page_builder/visibilityrule/wizard/<rule_id>/
    """
    from django.contrib import admin, messages
    from django.shortcuts import redirect

    # Get existing rule if editing
    rule = None
    if rule_id:
        rule = get_object_or_404(VisibilityRule, id=rule_id)

    # Handle form submission
    if request.method == "POST":
        try:
            # Parse form data
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            rule_type = request.POST.get("rule_type", "")
            operator = request.POST.get("operator", "equals")
            value_json = request.POST.get("value_json", "{}")
            priority = int(request.POST.get("priority", 5))
            cache_duration = int(request.POST.get("cache_duration", 300))
            is_active = request.POST.get("is_active") == "on"

            # Parse value from JSON
            try:
                value = json.loads(value_json)
            except json.JSONDecodeError:
                value = value_json

            # Validate required fields
            if not name:
                raise ValueError(_("Rule name is required"))
            if not rule_type:
                raise ValueError(_("Rule type is required"))

            # Create or update rule
            if rule:
                rule.name = name
                rule.description = description
                rule.rule_type = rule_type
                rule.operator = operator
                rule.value = value
                rule.priority = priority
                rule.cache_duration = cache_duration
                rule.is_active = is_active
                rule.save()
                messages.success(request, _('Rule "{}" updated successfully.').format(name))
            else:
                rule = VisibilityRule.objects.create(
                    name=name,
                    description=description,
                    rule_type=rule_type,
                    operator=operator,
                    value=value,
                    priority=priority,
                    cache_duration=cache_duration,
                    is_active=is_active,
                )
                messages.success(request, _('Rule "{}" created successfully.').format(name))

            # Redirect to change list
            return redirect("admin:page_builder_visibilityrule_changelist")

        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, _("Error saving rule: {}").format(str(e)))

    context = {
        **admin.site.each_context(request),
        "title": _("Edit Visibility Rule") if rule else _("Create Visibility Rule"),
        "rule": rule,
        "opts": VisibilityRule._meta,
    }

    return TemplateResponse(request, "admin/page_builder/visibilityrule/wizard.html", context)
