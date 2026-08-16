"""Visibility engine — shared rule models used by page content AND navigation.

Extracted from ``page_builder`` so that both ``page_builder`` (page elements) and
``design`` (header/footer/menu items) can gate content by the same rules without
depending on each other. The database tables are unchanged (see ``Meta.db_table``
on each model) — this app owns the models, not new tables.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

_VISIBILITY_VERSION_KEY = "pb_visibility_config_version"


def visibility_config_version():
    """Version stamp for cached visibility-config lookups (e.g. a page's
    temporal-rule flag). Bumping it invalidates those caches immediately when a
    rule/group/membership changes — see visibility.signals."""
    from django.core.cache import cache

    version = cache.get(_VISIBILITY_VERSION_KEY)
    if version is None:
        version = 1
        cache.add(_VISIBILITY_VERSION_KEY, version, timeout=None)
    return version


def bump_visibility_config_version():
    """Invalidate every cached visibility-config lookup (rule/group/membership
    change). Never expires so long-lived derived flags can't be resurrected."""
    from django.core.cache import cache

    visibility_config_version()  # ensure the stamp exists so incr can't miss
    try:
        cache.incr(_VISIBILITY_VERSION_KEY)
    except ValueError:
        cache.set(_VISIBILITY_VERSION_KEY, 2, timeout=None)


class VisibilityRule(models.Model):
    """
    Advanced visibility rules for page elements
    Allows conditional display based on various criteria
    """

    # Rule Types
    RULE_TYPES = [
        # Geographic
        ("geo_country", _("Country")),
        ("geo_region", _("Region/State")),
        ("geo_city", _("City")),
        ("geo_timezone", _("Time Zone")),
        # User & Authentication
        ("user_logged_in", _("Logged In Status")),
        ("user_group", _("User Group")),
        ("user_segment", _("Customer Segment")),
        ("user_lifetime_value", _("Customer Lifetime Value")),
        ("user_order_count", _("Order Count")),
        # Device & Technical
        ("device_type", _("Device Type")),
        ("browser", _("Browser")),
        ("operating_system", _("Operating System")),
        ("screen_size", _("Screen Size")),
        ("connection_speed", _("Connection Speed")),
        # Time-Based
        ("date_range", _("Date Range")),
        ("time_range", _("Time of Day")),
        ("day_of_week", _("Day of Week")),
        ("business_hours", _("Business Hours")),
        # Behavioral
        ("first_visit", _("First Time Visitor")),
        ("visit_count", _("Visit Count")),
        ("page_views", _("Page Views in Session")),
        ("time_on_site", _("Time on Site")),
        ("referrer", _("Referrer Source")),
        ("utm_campaign", _("UTM Campaign")),
        # E-commerce
        ("cart_value", _("Cart Value")),
        ("cart_items", _("Cart Item Count")),
        ("has_purchased", _("Has Purchased Before")),
        ("abandoned_cart", _("Has Abandoned Cart")),
        ("wishlist_items", _("Has Wishlist Items")),
        # Language & Localization
        ("browser_language", _("Browser Language")),
        ("selected_language", _("Selected Language")),
        ("selected_currency", _("Selected Currency")),
    ]

    # Operators
    OPERATORS = [
        ("equals", _("Equals")),
        ("not_equals", _("Not Equals")),
        ("contains", _("Contains")),
        ("not_contains", _("Does Not Contain")),
        ("greater_than", _("Greater Than")),
        ("less_than", _("Less Than")),
        ("in_list", _("In List")),
        ("not_in_list", _("Not In List")),
        ("is_true", _("Is True")),
        ("is_false", _("Is False")),
        ("between", _("Between")),
        ("regex", _("Matches Regex")),
    ]

    # Logic Operators for combining rules
    LOGIC_OPERATORS = [
        ("AND", _("All conditions must match")),
        ("OR", _("Any condition matches")),
    ]

    # Render-stage taxonomy — which rendering pass a rule can be evaluated in:
    #   SHELL     deterministic per (market, language, currency) → server-rendered
    #             into the cacheable page shell (SEO-safe, same HTML for everyone
    #             incl. crawlers at a given URL).
    #   TEMPORAL  visitor-independent but time-varying → shell-rendered with a
    #             cache TTL bounded by the time window.
    #   DEFERRED  per-visitor (auth, cart, device, precise geo, behaviour) → must
    #             never be baked into the cached shell; resolved by the
    #             personalization pass instead.
    RENDER_STAGE_SHELL = "shell"
    RENDER_STAGE_TEMPORAL = "temporal"
    RENDER_STAGE_DEFERRED = "deferred"

    RENDER_STAGES = {
        # Shell — deterministic per market / language / currency.
        "geo_region": RENDER_STAGE_SHELL,  # matches the SalesRegion (market) code
        "selected_language": RENDER_STAGE_SHELL,
        "selected_currency": RENDER_STAGE_SHELL,
        # Temporal — same for every visitor at a given instant.
        "date_range": RENDER_STAGE_TEMPORAL,
        "time_range": RENDER_STAGE_TEMPORAL,
        "day_of_week": RENDER_STAGE_TEMPORAL,
        "business_hours": RENDER_STAGE_TEMPORAL,
        # Everything else — precise geo_country/geo_city/geo_timezone, device,
        # auth, cart, behaviour, utm, browser_language — varies per individual
        # visitor and is resolved by the deferred pass (RENDER_STAGES.get default).
    }

    name = models.CharField(max_length=200, help_text=_("Descriptive name for this rule"))

    description = models.TextField(
        blank=True, help_text=_("Optional description of what this rule does")
    )

    # Rule configuration
    rule_type = models.CharField(
        max_length=50, choices=RULE_TYPES, help_text=_("Type of condition to check")
    )

    operator = models.CharField(
        max_length=20, choices=OPERATORS, default="equals", help_text=_("How to compare the value")
    )

    # Value to compare against (stored as JSON for flexibility)
    value = models.JSONField(default=dict, help_text=_("Value or values to compare against"))

    # Additional configuration
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(
        default=0, help_text=_("Higher priority rules are evaluated first")
    )

    # Caching
    cache_duration = models.IntegerField(
        default=300, help_text=_("How long to cache rule evaluation results (seconds)")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Preserve the original table (model moved out of page_builder without a
        # data migration — see visibility/migrations/0001).
        db_table = "page_builder_visibilityrule"
        verbose_name = _("Visibility Rule")
        verbose_name_plural = _("Visibility Rules")
        ordering = ["-priority", "name"]
        indexes = [
            models.Index(fields=["rule_type", "is_active"]),
            models.Index(fields=["priority", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"

    def evaluate(self, context):
        """
        Evaluate this rule against the provided context
        Returns True if the rule matches, False otherwise
        """
        from .evaluator import RuleEvaluator

        evaluator = RuleEvaluator()
        return evaluator.evaluate_single_rule(self, context)

    @property
    def render_stage(self):
        """Which rendering pass this rule can be evaluated in (see RENDER_STAGES)."""
        return self.RENDER_STAGES.get(self.rule_type, self.RENDER_STAGE_DEFERRED)

    @property
    def is_deferred(self):
        """True when this rule is per-visitor and must be resolved after the shell."""
        return self.render_stage == self.RENDER_STAGE_DEFERRED

    @property
    def is_temporal(self):
        """True when this rule is time-based (its result changes over time)."""
        return self.render_stage == self.RENDER_STAGE_TEMPORAL

    def short_label(self):
        """A compact human label for this rule, for the builder canvas chip
        indicator (e.g. "NZ", "Members", "Cart ≥ 50"). Falls back to the rule
        type's display name.
        """
        rt = self.rule_type
        value = self.value

        def _v():
            v = value
            # The rule builder persists values as {"value": n}, {"values": [...]},
            # or {"min": a, "max": b} (between) — unwrap those to the real gate.
            if isinstance(v, dict):
                if "value" in v:
                    v = v["value"]
                elif "values" in v:
                    v = v["values"]
                elif "min" in v or "max" in v:
                    return f"{v.get('min', '')}–{v.get('max', '')}".strip("–")
                else:
                    return "…"
            if isinstance(v, list):
                return ", ".join(str(x) for x in v)
            return str(v)

        if rt in ("geo_region", "geo_country"):
            return _v().upper()
        if rt == "geo_city":
            return _v().title()
        if rt == "user_logged_in":
            raw = value.get("value", value) if isinstance(value, dict) else value
            truthy = (
                raw
                if isinstance(raw, bool)
                else str(raw).strip().lower()
                in (
                    "true",
                    "1",
                    "yes",
                )
            )
            members = {"is_true": True, "is_false": False}.get(self.operator)
            if members is None:  # equals / not_equals target a boolean value
                members = (not truthy) if self.operator == "not_equals" else truthy
            return _("Members") if members else _("Guests")
        if rt in ("user_group", "user_segment"):
            return _v()
        if rt == "device_type":
            return _v().title()
        if rt in ("selected_currency", "selected_language", "browser_language"):
            return _v().upper()
        if rt in (
            "cart_value",
            "cart_items",
            "user_lifetime_value",
            "user_order_count",
            "visit_count",
            "page_views",
        ):
            op = {"greater_than": "≥", "less_than": "≤", "equals": "=", "between": "∈"}.get(
                self.operator, ""
            )
            noun = {
                "cart_value": _("Cart"),
                "cart_items": _("Cart items"),
                "user_lifetime_value": _("LTV"),
                "user_order_count": _("Orders"),
                "visit_count": _("Visits"),
                "page_views": _("Views"),
            }.get(rt, "")
            return f"{noun} {op} {_v()}".strip()
        if rt == "business_hours":
            return _("Business hours")
        if rt in ("date_range", "time_range", "day_of_week"):
            return _("Scheduled")
        if rt == "has_purchased":
            return _("Returning")
        return str(self.get_rule_type_display())


class RuleGroup(models.Model):
    """
    Groups multiple visibility rules with logic operators
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # How to combine rules in this group
    logic_operator = models.CharField(
        max_length=3,
        choices=VisibilityRule.LOGIC_OPERATORS,
        default="AND",
        help_text=_("How to combine rules in this group"),
    )

    # Rules in this group
    rules = models.ManyToManyField(VisibilityRule, related_name="groups", through="RuleGroupMember")

    # Nested groups support
    parent_group = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="child_groups"
    )

    # Authoring/display order within a parent (lower first). Does not affect
    # AND/OR evaluation — it only orders sibling groups in the rule builder.
    priority = models.IntegerField(
        default=0, help_text=_("Order among sibling groups in the builder (lower shown first)")
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Preserve the original table (see visibility/migrations/0001).
        db_table = "page_builder_rulegroup"
        verbose_name = _("Rule Group")
        verbose_name_plural = _("Rule Groups")
        ordering = ["name"]

    def __str__(self):
        operator_display = "ALL" if self.logic_operator == "AND" else "ANY"
        return f"{self.name} ({operator_display})"

    def evaluate(self, context):
        """
        Evaluate all rules in this group against the context
        """
        from .evaluator import RuleEvaluator

        evaluator = RuleEvaluator()
        return evaluator.evaluate_rule_group(self, context)

    def _contains_rule(self, predicate, _visited=None):
        """True if this group — or any nested child group — holds a rule matching
        ``predicate`` (a callable taking a VisibilityRule). ``_visited`` guards
        against a cyclic child-group graph (admin-editable data) recursing forever.
        """
        if _visited is None:
            _visited = set()
        if self.pk in _visited:
            return False
        _visited.add(self.pk)

        # Only active rules/groups count — mirror evaluate_rule_group, or a
        # disabled deferred rule would wrongly force an otherwise shell-safe
        # element into the deferred path (blank for crawlers / no-JS).
        if any(predicate(rule) for rule in self.rules.filter(is_active=True)):
            return True
        return any(
            child._contains_rule(predicate, _visited)
            for child in self.child_groups.filter(is_active=True)
        )

    def contains_deferred_rule(self):
        """True if this group (or a nested child) holds a per-visitor (deferred)
        rule — such an element can't be baked into the cacheable shell.
        """
        return self._contains_rule(lambda rule: rule.is_deferred)

    def contains_temporal_rule(self):
        """True if this group (or a nested child) holds a time-based rule — a page
        using it must not be cached past the temporal boundary.
        """
        return self._contains_rule(lambda rule: rule.is_temporal)

    def rule_labels(self, _visited=None):
        """Compact labels for every active rule in this group (and nested child
        groups), for the builder canvas chip indicator."""
        if _visited is None:
            _visited = set()
        if self.pk in _visited:
            return []
        _visited.add(self.pk)

        labels = [rule.short_label() for rule in self.rules.filter(is_active=True)]
        for child in self.child_groups.filter(is_active=True):
            labels.extend(child.rule_labels(_visited))
        return labels


class RuleGroupMember(models.Model):
    """
    Through model for rule group membership with ordering
    """

    rule_group = models.ForeignKey(RuleGroup, on_delete=models.CASCADE)
    rule = models.ForeignKey(VisibilityRule, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        # Preserve the original table (see visibility/migrations/0001).
        db_table = "page_builder_rulegroupmember"
        ordering = ["order"]
        unique_together = ["rule_group", "rule"]

    def __str__(self):
        return f"{self.rule_group} → {self.rule} (order={self.order})"
