"""
Shipping Promotion Configuration Wizard Views
Multi-step wizard for creating and configuring shipping promotions
"""

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from djmoney.money import Money

from cart.models import ShippingMethod
from catalog.models import Category, Product
from core.utils import get_default_currency
from shipping.models import ShippingPromotion, ShippingZone


@method_decorator(staff_member_required, name="dispatch")
class RuleWizardStep1View(TemplateView):
    """
    Step 1: Rule Basics
    Rule name, description, type, value, and active status
    """

    template_name = "admin/shipping/promotion_wizard/step1_basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = 1
        context["rule_data"] = self.request.session.get("promotion_wizard_data", {})
        context["rule_types"] = ShippingPromotion.PROMOTION_TYPES
        return context

    def post(self, request, *args, **kwargs):
        # Store step 1 data in session
        wizard_data = request.session.get("promotion_wizard_data", {})

        rule_type = request.POST.get("rule_type", "")
        rule_value = request.POST.get("rule_value", "")

        wizard_data.update(
            {
                "name": request.POST.get("name", ""),
                "description": request.POST.get("description", ""),
                "rule_type": rule_type,
                "rule_value": rule_value if rule_type != "free_shipping" else "",
                "is_active": request.POST.get("is_active") == "on",
            }
        )
        request.session["promotion_wizard_data"] = wizard_data

        # Redirect to step 2
        return redirect("shipping:promotion_wizard_step2")


@method_decorator(staff_member_required, name="dispatch")
class RuleWizardStep2View(TemplateView):
    """
    Step 2: Cart Conditions
    Configure cart value, weight, and item count conditions
    """

    template_name = "admin/shipping/promotion_wizard/step2_conditions.html"

    def get(self, request, *args, **kwargs):
        # Check if step 1 was completed
        rule_data = request.session.get("promotion_wizard_data", {})
        if not rule_data.get("name"):
            messages.warning(request, _("Please complete Step 1 first"))
            return redirect("shipping:promotion_wizard_step1")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = 2
        context["rule_data"] = self.request.session.get("promotion_wizard_data", {})
        return context

    def post(self, request, *args, **kwargs):
        # Store step 2 data in session
        wizard_data = request.session.get("promotion_wizard_data", {})

        # Parse cart value conditions
        min_cart_value = request.POST.get("min_cart_value", "").strip()
        max_cart_value = request.POST.get("max_cart_value", "").strip()

        # Parse weight conditions
        min_cart_weight = request.POST.get("min_cart_weight", "").strip()
        max_cart_weight = request.POST.get("max_cart_weight", "").strip()

        # Parse item count conditions
        min_item_count = request.POST.get("min_item_count", "").strip()
        max_item_count = request.POST.get("max_item_count", "").strip()

        wizard_data.update(
            {
                "min_cart_value": min_cart_value,
                "max_cart_value": max_cart_value,
                "min_cart_weight": min_cart_weight,
                "max_cart_weight": max_cart_weight,
                "min_item_count": min_item_count,
                "max_item_count": max_item_count,
            }
        )
        request.session["promotion_wizard_data"] = wizard_data

        # Redirect to step 3
        return redirect("shipping:promotion_wizard_step3")


@method_decorator(staff_member_required, name="dispatch")
class RuleWizardStep3View(TemplateView):
    """
    Step 3: Geographic & Method Restrictions
    Configure zones and shipping methods
    """

    template_name = "admin/shipping/promotion_wizard/step3_restrictions.html"

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed
        rule_data = request.session.get("promotion_wizard_data", {})
        if not rule_data.get("name"):
            messages.warning(request, _("Please complete the wizard steps"))
            return redirect("shipping:promotion_wizard_step1")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = 3
        rule_data = self.request.session.get("promotion_wizard_data", {})
        context["rule_data"] = rule_data

        # Get all available zones and methods
        context["all_zones"] = ShippingZone.objects.all().order_by("name")
        context["all_methods"] = ShippingMethod.objects.all().order_by("name")

        # Parse selected zones and methods from session
        context["selected_zone_ids"] = rule_data.get("zones", [])
        context["selected_method_ids"] = rule_data.get("shipping_methods", [])

        return context

    def post(self, request, *args, **kwargs):
        # Store step 3 data in session
        wizard_data = request.session.get("promotion_wizard_data", {})

        # Parse selected zones and methods (IDs)
        selected_zones = request.POST.getlist("zones")
        selected_methods = request.POST.getlist("shipping_methods")

        wizard_data.update(
            {
                "zones": selected_zones,
                "shipping_methods": selected_methods,
            }
        )
        request.session["promotion_wizard_data"] = wizard_data

        # Redirect to step 4
        return redirect("shipping:promotion_wizard_step4")


@method_decorator(staff_member_required, name="dispatch")
class RuleWizardStep4View(TemplateView):
    """
    Step 4: Product & Customer Restrictions
    Configure product, category, and customer group restrictions
    """

    template_name = "admin/shipping/promotion_wizard/step4_customers.html"

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed
        rule_data = request.session.get("promotion_wizard_data", {})
        if not rule_data.get("name"):
            messages.warning(request, _("Please complete the wizard steps"))
            return redirect("shipping:promotion_wizard_step1")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = 4
        rule_data = self.request.session.get("promotion_wizard_data", {})
        context["rule_data"] = rule_data

        # Get all available products, categories, and customer groups
        context["all_products"] = Product.objects.all().order_by("name")
        context["all_categories"] = Category.objects.all().order_by("name")
        context["all_customer_groups"] = Group.objects.all().order_by("name")

        # Parse selected items from session
        context["selected_requires_product_ids"] = rule_data.get("requires_products", [])
        context["selected_requires_category_ids"] = rule_data.get("requires_categories", [])
        context["selected_excludes_product_ids"] = rule_data.get("excludes_products", [])
        context["selected_excludes_category_ids"] = rule_data.get("excludes_categories", [])
        context["selected_customer_group_ids"] = rule_data.get("customer_groups", [])
        context["first_time_customers_only"] = rule_data.get("first_time_customers_only", False)

        return context

    def post(self, request, *args, **kwargs):
        # Store step 4 data in session
        wizard_data = request.session.get("promotion_wizard_data", {})

        # Parse product/category requirements and exclusions
        requires_products = request.POST.getlist("requires_products")
        requires_categories = request.POST.getlist("requires_categories")
        excludes_products = request.POST.getlist("excludes_products")
        excludes_categories = request.POST.getlist("excludes_categories")

        # Parse customer restrictions
        customer_groups = request.POST.getlist("customer_groups")
        first_time_customers_only = request.POST.get("first_time_customers_only") == "on"

        wizard_data.update(
            {
                "requires_products": requires_products,
                "requires_categories": requires_categories,
                "excludes_products": excludes_products,
                "excludes_categories": excludes_categories,
                "customer_groups": customer_groups,
                "first_time_customers_only": first_time_customers_only,
            }
        )
        request.session["promotion_wizard_data"] = wizard_data

        # Redirect to step 5
        return redirect("shipping:promotion_wizard_step5")


@method_decorator(staff_member_required, name="dispatch")
class RuleWizardStep5View(TemplateView):
    """
    Step 5: Advanced Settings & Review
    Configure priority, time restrictions, stop flag, and review all settings
    """

    template_name = "admin/shipping/promotion_wizard/step5_review.html"

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed
        rule_data = request.session.get("promotion_wizard_data", {})
        if not rule_data.get("name"):
            messages.warning(request, _("Please complete the wizard steps"))
            return redirect("shipping:promotion_wizard_step1")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = 5
        rule_data = self.request.session.get("promotion_wizard_data", {})
        context["rule_data"] = rule_data

        # Get display names for review
        zone_ids = rule_data.get("zones", [])
        if zone_ids:
            context["selected_zones"] = ShippingZone.objects.filter(id__in=zone_ids)

        method_ids = rule_data.get("shipping_methods", [])
        if method_ids:
            context["selected_methods"] = ShippingMethod.objects.filter(id__in=method_ids)

        # Products and categories
        requires_product_ids = rule_data.get("requires_products", [])
        if requires_product_ids:
            context["requires_products"] = Product.objects.filter(id__in=requires_product_ids)

        requires_category_ids = rule_data.get("requires_categories", [])
        if requires_category_ids:
            context["requires_categories"] = Category.objects.filter(id__in=requires_category_ids)

        excludes_product_ids = rule_data.get("excludes_products", [])
        if excludes_product_ids:
            context["excludes_products"] = Product.objects.filter(id__in=excludes_product_ids)

        excludes_category_ids = rule_data.get("excludes_categories", [])
        if excludes_category_ids:
            context["excludes_categories"] = Category.objects.filter(id__in=excludes_category_ids)

        # Customer groups
        customer_group_ids = rule_data.get("customer_groups", [])
        if customer_group_ids:
            context["customer_groups"] = Group.objects.filter(id__in=customer_group_ids)

        return context

    def post(self, request, *args, **kwargs):
        wizard_data = request.session.get("promotion_wizard_data", {})

        # Get advanced settings from form
        priority = request.POST.get("priority", "0")
        stop_further_promotions = request.POST.get("stop_further_promotions") == "on"
        start_date = request.POST.get("start_date", "").strip()
        end_date = request.POST.get("end_date", "").strip()

        try:
            # Create the promotion
            rule = ShippingPromotion(
                name=wizard_data.get("name", ""),
                description=wizard_data.get("description", ""),
                promotion_type=wizard_data.get("rule_type", ""),
                is_active=wizard_data.get("is_active", True),
                priority=int(priority),
                stop_further_promotions=stop_further_promotions,
                created_by=request.user,
            )

            # Set promotion value if not free shipping
            if rule.promotion_type != "free_shipping" and wizard_data.get("rule_value"):
                rule.promotion_value = Money(wizard_data.get("rule_value"), get_default_currency())

            # Set cart conditions
            if wizard_data.get("min_cart_value"):
                rule.min_cart_value = Money(
                    wizard_data.get("min_cart_value"), get_default_currency()
                )
            if wizard_data.get("max_cart_value"):
                rule.max_cart_value = Money(
                    wizard_data.get("max_cart_value"), get_default_currency()
                )
            if wizard_data.get("min_cart_weight"):
                rule.min_cart_weight = wizard_data.get("min_cart_weight")
            if wizard_data.get("max_cart_weight"):
                rule.max_cart_weight = wizard_data.get("max_cart_weight")
            if wizard_data.get("min_item_count"):
                rule.min_item_count = wizard_data.get("min_item_count")
            if wizard_data.get("max_item_count"):
                rule.max_item_count = wizard_data.get("max_item_count")

            # Set time restrictions
            if start_date:
                from django.utils.dateparse import parse_datetime

                rule.start_date = parse_datetime(start_date)
            if end_date:
                from django.utils.dateparse import parse_datetime

                rule.end_date = parse_datetime(end_date)

            # Set customer restrictions
            rule.first_time_customers_only = wizard_data.get("first_time_customers_only", False)

            # Save the rule first
            rule.save()

            # Set many-to-many relationships after saving
            if wizard_data.get("zones"):
                rule.zones.set(wizard_data.get("zones"))
            if wizard_data.get("shipping_methods"):
                rule.shipping_methods.set(wizard_data.get("shipping_methods"))
            if wizard_data.get("requires_products"):
                rule.requires_products.set(wizard_data.get("requires_products"))
            if wizard_data.get("requires_categories"):
                rule.requires_categories.set(wizard_data.get("requires_categories"))
            if wizard_data.get("excludes_products"):
                rule.excludes_products.set(wizard_data.get("excludes_products"))
            if wizard_data.get("excludes_categories"):
                rule.excludes_categories.set(wizard_data.get("excludes_categories"))
            if wizard_data.get("customer_groups"):
                rule.customer_groups.set(wizard_data.get("customer_groups"))

            # Clear wizard data from session
            if "promotion_wizard_data" in request.session:
                del request.session["promotion_wizard_data"]

            messages.success(
                request,
                _('Shipping promotion "%(name)s" created successfully!') % {"name": rule.name},
            )

            # Redirect to promotion admin list
            return redirect("admin:shipping_shippingpromotion_changelist")

        except Exception as e:
            messages.error(request, _("Failed to create promotion: %(error)s") % {"error": str(e)})
            return redirect("shipping:promotion_wizard_step5")
