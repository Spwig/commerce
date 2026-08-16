"""
Admin for the agentic commerce settings, agent registry, and audit log.

`AgentKey` is deliberately NOT registered — it holds encrypted private keys, and
keeping it out of the admin (and every serializer/API) is part of why a signing
private key can never reach a UI.
"""

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from agentic.models import AgentEvent, AgenticSettings, AgentIdentity, AgentPolicy, Mandate


@admin.register(AgenticSettings)
class AgenticSettingsAdmin(admin.ModelAdmin):
    """Singleton settings — one row, edited in place (SearchSettings pattern).

    The change form is fronted by a readiness dashboard (see the custom
    change_form template) that answers "can AI assistants buy from my store?"
    from live install state.
    """

    change_form_template = "admin/agentic/agenticsettings/change_form.html"

    fieldsets = (
        (
            _("Status"),
            {
                "fields": ("is_enabled", "kill_switch_engaged"),
                "description": _(
                    "Turn agentic commerce on or off. While off, the store "
                    "exposes no agent surface at all. Use the emergency stop to "
                    "halt agent activity immediately without changing settings."
                ),
            },
        ),
        (
            _("Protocols"),
            {
                "fields": ("ucp_enabled", "acp_enabled", "mcp_storefront_enabled"),
            },
        ),
        (
            _("Agent access"),
            {
                "fields": ("allow_unverified_read", "allow_unverified_checkout"),
                "description": _(
                    "Reading (discovery and browsing) is lower-risk than "
                    "checkout. A store can be discoverable without being "
                    "purchasable by unverified agents."
                ),
            },
        ),
        (
            _("Merchant details"),
            {
                "fields": (
                    "merchant_display_name",
                    "support_url",
                    "terms_url",
                    "privacy_url",
                    "return_policy_url",
                ),
                "description": _(
                    "Shown to agents in the discovery document. Blank fields "
                    "fall back to your Site Settings where possible."
                ),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # Singleton — never more than one row.
        return not AgenticSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        # Attach the live readiness summary so the template can render the
        # verdict cards above the form. Presentation only — never gates anything.
        from agentic.services import readiness_service

        extra_context = extra_context or {}
        try:
            extra_context["readiness"] = readiness_service.store_readiness()
        except Exception:  # a dashboard must never 500 the settings page
            extra_context["readiness"] = None
        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        # The list is a singleton, so go straight to editing the one row.
        obj = AgenticSettings.get_settings()
        return self.changeform_view(request, str(obj.pk), extra_context=extra_context or {})


class AgentPolicyInline(admin.StackedInline):
    """
    Edit a calling agent's spend/tender/rate-limit policy in place.

    The only editable surface on the otherwise read-only identity page. Saves are
    routed through `agent_registry_service.change_agent_policy` (see
    `AgentIdentityAdmin.save_formset`) so every change lands in the append-only
    audit log — the admin never writes a policy field directly.
    """

    model = AgentPolicy
    can_delete = False
    max_num = 1
    extra = 0
    verbose_name_plural = _("Policy (limits & allowed tenders)")
    fields = (
        "max_order_amount",
        "daily_spend_cap",
        "allow_discount_codes",
        "allow_gift_cards",
        "allow_digital_goods",
        "rate_limit_per_minute",
    )


@admin.register(AgentIdentity)
class AgentIdentityAdmin(admin.ModelAdmin):
    """
    The registry of calling agents established by trust-on-first-use.

    Read-only except for the block/unblock/verify actions and the policy inline —
    identities are created by the auth stack (a merchant never adds one), and the
    claimed fields are the agent's own untrusted assertions, so nothing else here
    should be hand-edited.
    """

    inlines = (AgentPolicyInline,)
    list_display = (
        "display_label",
        "directory",
        "trust_state",
        "request_count",
        "last_seen_at",
    )
    list_filter = ("trust_state", "directory")
    search_fields = ("directory", "key_thumbprint", "claimed_name")
    ordering = ("-last_seen_at",)
    actions = ("verify_agents", "block_agents", "unblock_agents")

    readonly_fields = (
        "directory",
        "key_thumbprint",
        "algorithm",
        "public_jwk",
        "claimed_name",
        "claimed_logo_url",
        "claimed_homepage",
        "trust_state",
        "blocked_reason",
        "blocked_at",
        "first_seen_at",
        "last_seen_at",
        "request_count",
        "created_at",
        "updated_at",
    )

    @admin.display(description=_("Assistant"))
    def display_label(self, obj):
        # Claimed name is UNTRUSTED — it is only ever a label, shown alongside
        # the durable directory host (which is the real identity).
        return obj.claimed_name or obj.directory

    def has_add_permission(self, request):
        return False

    @admin.action(description=_("Block selected assistants"))
    def block_agents(self, request, queryset):
        blocked = 0
        for agent in queryset.exclude(trust_state=AgentIdentity.TRUST_BLOCKED):
            agent.trust_state = AgentIdentity.TRUST_BLOCKED
            agent.blocked_at = timezone.now()
            agent.blocked_reason = _("Blocked from the admin.")
            agent.save(update_fields=["trust_state", "blocked_at", "blocked_reason", "updated_at"])
            AgentEvent.append(
                AgentEvent.EVENT_AGENT_BLOCKED,
                agent=agent,
                detail={"by": request.user.get_username()},
            )
            blocked += 1
        self.message_user(
            request,
            ngettext("%d assistant blocked.", "%d assistants blocked.", blocked) % blocked,
        )

    @admin.action(description=_("Unblock selected assistants"))
    def unblock_agents(self, request, queryset):
        unblocked = 0
        for agent in queryset.filter(trust_state=AgentIdentity.TRUST_BLOCKED):
            # Unblocking returns an agent to `capped`, never straight to
            # `verified` — lifting the limits is a separate, deliberate step.
            agent.trust_state = AgentIdentity.TRUST_CAPPED
            agent.blocked_at = None
            agent.blocked_reason = ""
            agent.save(update_fields=["trust_state", "blocked_at", "blocked_reason", "updated_at"])
            AgentEvent.append(
                AgentEvent.EVENT_AGENT_UNBLOCKED,
                agent=agent,
                detail={"by": request.user.get_username()},
            )
            unblocked += 1
        self.message_user(
            request,
            ngettext("%d assistant unblocked.", "%d assistants unblocked.", unblocked) % unblocked,
        )

    @admin.action(description=_("Promote to verified (remove limits)"))
    def verify_agents(self, request, queryset):
        from agentic.services.agent_registry_service import verify_agent_identity

        promoted = skipped = 0
        for agent in queryset:
            if agent.trust_state == AgentIdentity.TRUST_VERIFIED:
                continue  # already verified — no change, no noise
            try:
                verify_agent_identity(agent, actor=request.user.get_username())
                promoted += 1
            except ValueError:
                # A blocked agent can't be verified — unblock it first.
                skipped += 1
        msg = ngettext("%d assistant verified.", "%d assistants verified.", promoted) % promoted
        if skipped:
            msg += " " + (
                ngettext(
                    "%d skipped (blocked — unblock first).",
                    "%d skipped (blocked — unblock first).",
                    skipped,
                )
                % skipped
            )
        self.message_user(request, msg)

    def save_formset(self, request, form, formset, change):
        # Route AgentPolicy inline edits through the service so every change is
        # recorded in the append-only audit log; never write the policy directly.
        if formset.model is AgentPolicy:
            from agentic.services import agent_registry_service as ars

            agent = form.instance
            for pform in formset.forms:
                if not getattr(pform, "cleaned_data", None) or not pform.has_changed():
                    continue
                changes = {
                    field: pform.cleaned_data[field]
                    for field in pform.changed_data
                    if field in ars.POLICY_FIELDS
                }
                if changes:
                    ars.change_agent_policy(
                        agent, changes=changes, actor=request.user.get_username()
                    )
            # We persisted through the service instead of formset.save(), so the
            # admin's change-logging still expects these lists to exist.
            formset.new_objects = []
            formset.changed_objects = []
            formset.deleted_objects = []
            return
        super().save_formset(request, form, formset, change)


@admin.register(AgentEvent)
class AgentEventAdmin(admin.ModelAdmin):
    """
    Read-only browser over the append-only, hash-chained agent audit log.

    Nothing here can be added, edited or deleted — the model itself refuses
    those — so this is a viewer, deliberately. It is the dispute-time evidence
    trail, distinct from AdminAPIAuditLog.
    """

    list_display = ("chain_index", "event_type", "directory", "created_at")
    list_filter = ("event_type",)
    search_fields = ("directory", "key_thumbprint")
    ordering = ("-chain_index",)
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    """
    Read-only browser over issued AP2 checkout mandates — the merchant's
    signed dispute evidence. Retained (the model refuses delete()), so this is
    a viewer only.
    """

    list_display = ("id", "mandate_type", "attested_amount", "alg", "issued_at", "expires_at")
    list_filter = ("mandate_type", "alg")
    search_fields = ("ucp_checkout_id", "kid", "order__order_number")
    date_hierarchy = "issued_at"
    ordering = ("-issued_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
