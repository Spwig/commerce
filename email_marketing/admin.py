"""Admin registration for the Campaign Studio.

Minimal, standard Django admin surfaces for the foundation. The rich visual
builder and merchant-facing UI arrive in a later phase; these change-lists give
staff a way to inspect and operate campaigns, segments, and subscribers now.
Access is gated by the standard Django model permissions, delegated through the
'marketing' staff-role category.
"""

import logging

from django import forms
from django.contrib import admin, messages
from django.contrib.sites.models import Site
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("email_marketing")


class _SiteScopedAdmin(admin.ModelAdmin):
    """Single-tenant helper: hide the Site FK and always set it to SITE_ID=1."""

    exclude = ("site",)

    def save_model(self, request, obj, form, change):
        if not obj.site_id:
            obj.site = Site.objects.get(pk=1)
        super().save_model(request, obj, form, change)


from .models import (
    MESSAGE_TYPE_CHOICES,
    Campaign,
    CampaignSchedule,
    CampaignSend,
    Journey,
    JourneyEnrollment,
    Segment,
    Subscriber,
    SubscriberTag,
    SuppressionEntry,
)


@admin.register(SubscriberTag)
class SubscriberTagAdmin(_SiteScopedAdmin):
    list_display = ("name", "slug", "subscriber_count", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)

    @admin.display(description=_("Subscribers"))
    def subscriber_count(self, obj):
        return obj.subscribers.count()


class SubscriberImportForm(forms.Form):
    """Upload step for the CSV/XLSX subscriber import."""

    file = forms.FileField(
        label=_("CSV or Excel file"),
        help_text=_("A .csv or .xlsx file with an email column (up to 5 MB)."),
    )
    duplicate_strategy = forms.ChoiceField(
        label=_("For contacts already on your list"),
        choices=[
            ("skip", _("Leave them unchanged")),
            ("update", _("Update their name / language")),
        ],
        initial="skip",
        required=False,
    )
    tag = forms.ModelChoiceField(
        label=_("Tag imported contacts as"),
        queryset=SubscriberTag.objects.none(),
        required=False,
        help_text=_("Optional — apply a tag to everyone in this import."),
    )
    consent_confirmed = forms.BooleanField(
        label=_("These contacts have agreed to receive marketing email from me"),
        help_text=_(
            "Required. Import only contacts who have opted in — it's the law in most places."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tag"].queryset = SubscriberTag.objects.filter(
            site=Site.objects.get(pk=1)
        ).order_by("name")

    def clean_file(self):
        from .services.subscriber_importer import ALLOWED_EXTENSIONS, MAX_UPLOAD_BYTES

        f = self.cleaned_data["file"]
        if not (f.name or "").lower().endswith(ALLOWED_EXTENSIONS):
            raise forms.ValidationError(_("Unsupported file type. Upload a .csv or .xlsx file."))
        if f.size > MAX_UPLOAD_BYTES:
            raise forms.ValidationError(_("File is too large. Maximum upload size is 5 MB."))
        return f


@admin.register(Subscriber)
class SubscriberAdmin(_SiteScopedAdmin):
    list_display = ("email", "status", "source", "user", "marketing_verified", "created_at")
    list_filter = ("status", "source", "marketing_opt_in", "marketing_verified", "tags")
    search_fields = ("email",)
    readonly_fields = ("unsubscribe_token", "verification_token", "created_at", "updated_at")
    autocomplete_fields = ("user", "tags")
    ordering = ("-created_at",)
    actions = ("add_tag_action", "remove_tag_action")

    @admin.action(description=_("Add tag to selected…"), permissions=["change"])
    def add_tag_action(self, request, queryset):
        return self._tag_action(request, queryset, add=True)

    @admin.action(description=_("Remove tag from selected…"), permissions=["change"])
    def remove_tag_action(self, request, queryset):
        return self._tag_action(request, queryset, add=False)

    def _tag_action(self, request, queryset, *, add):
        """Two-step tag action: first render a tag picker, then apply on submit."""
        from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
        from django.shortcuts import render

        site = Site.objects.get(pk=1)
        if request.POST.get("apply_tag"):
            tag = SubscriberTag.objects.filter(pk=request.POST.get("tag"), site=site).first()
            if not tag:
                self.message_user(request, _("Please choose a tag."), level=messages.WARNING)
                return None
            for subscriber in queryset:
                if add:
                    subscriber.tags.add(tag)
                else:
                    subscriber.tags.remove(tag)
            verb = _("Tagged") if add else _("Untagged")
            self.message_user(
                request,
                _("%(verb)s %(n)d subscriber(s) with “%(tag)s”.")
                % {"verb": verb, "n": queryset.count(), "tag": tag.name},
            )
            return None

        context = {
            **self.admin_site.each_context(request),
            "title": _("Add tag") if add else _("Remove tag"),
            "subscribers": queryset,
            "tags": SubscriberTag.objects.filter(site=site).order_by("name"),
            "action": "add_tag_action" if add else "remove_tag_action",
            "add": add,
            "selected": request.POST.getlist(ACTION_CHECKBOX_NAME),
            "opts": self.model._meta,
        }
        return render(request, "admin/email_marketing/subscriber/tag_action.html", context)

    def changelist_view(self, request, extra_context=None):
        from datetime import timedelta

        from django.utils import timezone

        qs = Subscriber.objects.filter(site=Site.objects.get(pk=1))
        since = timezone.now() - timedelta(days=30)
        extra_context = {
            **(extra_context or {}),
            "total_subscribers": qs.count(),
            "active_subscribers": qs.filter(status=Subscriber.STATUS_ACTIVE).count(),
            "unsubscribed_subscribers": qs.filter(status=Subscriber.STATUS_UNSUBSCRIBED).count(),
            "new_subscribers": qs.filter(created_at__gte=since).count(),
            "status_choices": Subscriber.STATUS_CHOICES,
            "source_choices": Subscriber.SOURCE_CHOICES,
            "tag_choices": list(
                SubscriberTag.objects.filter(site_id=1).order_by("name").values_list("slug", "name")
            ),
            "show_import_button": True,
        }
        return super().changelist_view(request, extra_context)

    # --- CSV import (upload → preview → import) -------------------------------

    _IMPORT_SESSION_KEY = "email_marketing_subscriber_import"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "import/",
                self.admin_site.admin_view(self.import_view),
                name="email_marketing_subscriber_import",
            ),
        ]
        return custom + urls

    def import_view(self, request):
        """Two-step CSV import: upload + settings, preview, then confirm."""
        from django.core.exceptions import ValidationError
        from django.shortcuts import redirect, render

        from .services import subscriber_importer as imp

        if not self.has_add_permission(request):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied

        site = Site.objects.get(pk=1)
        base_ctx = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": _("Import subscribers"),
        }

        # Step 2 — confirm: import the rows stashed on the session.
        if request.method == "POST" and request.POST.get("confirm"):
            stash = request.session.get(self._IMPORT_SESSION_KEY)
            if not stash:
                self.message_user(
                    request,
                    _("Your import session expired — please upload again."),
                    level=messages.WARNING,
                )
                return redirect("..")
            tag = (
                SubscriberTag.objects.filter(pk=stash.get("tag_id"), site=site).first()
                if stash.get("tag_id")
                else None
            )
            try:
                result = imp.import_batch(
                    site,
                    stash["rows"],
                    duplicate_strategy=stash.get("duplicate_strategy", "skip"),
                    tag=tag,
                )
            except Exception:  # noqa: BLE001 — a bad row must not 500 the whole import
                logger.exception("Subscriber CSV import failed")
                self.message_user(
                    request,
                    _("Something went wrong importing that file — nothing was changed."),
                    level=messages.ERROR,
                )
                return redirect("..")
            finally:
                request.session.pop(self._IMPORT_SESSION_KEY, None)
            self.message_user(
                request,
                _(
                    "Imported %(created)d new subscriber(s); %(updated)d updated, %(skipped)d skipped."
                )
                % {"created": result.created, "updated": result.updated, "skipped": result.skipped},
            )
            return redirect("..")

        # Step 1 — upload: parse, preview, and stash the valid rows.
        if request.method == "POST":
            form = SubscriberImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    parsed = imp.parse_file(form.cleaned_data["file"])
                    mapping = imp.validate_mapping(
                        imp.auto_detect_mapping(parsed.headers), parsed.headers
                    )
                    preview = imp.build_preview(site, parsed, mapping)
                except ValidationError as exc:
                    form.add_error("file" if "email" not in str(exc) else None, exc)
                else:
                    tag = form.cleaned_data.get("tag")
                    # Stash only the compact valid rows (not the raw file bytes).
                    valid_rows, _invalid = imp.partition_rows(parsed.rows, mapping)
                    request.session[self._IMPORT_SESSION_KEY] = {
                        "rows": valid_rows,
                        "duplicate_strategy": form.cleaned_data.get("duplicate_strategy") or "skip",
                        "tag_id": str(tag.pk) if tag else None,
                    }
                    request.session.modified = True
                    return render(
                        request,
                        "admin/email_marketing/subscriber/import_preview.html",
                        {
                            **base_ctx,
                            "preview": preview,
                            "invalid_sample": preview.invalid_rows[:10],
                            "tag": tag,
                            "duplicate_strategy": form.cleaned_data.get("duplicate_strategy"),
                        },
                    )
        else:
            form = SubscriberImportForm()

        return render(
            request,
            "admin/email_marketing/subscriber/import_upload.html",
            {**base_ctx, "form": form},
        )


@admin.register(Segment)
class SegmentAdmin(_SiteScopedAdmin):
    list_display = ("name", "kind", "cached_count", "is_active", "last_built_at")
    list_filter = ("kind", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("cached_count", "last_built_at", "created_at", "updated_at")
    actions = ("rebuild_segments",)
    # Visual rule-builder replaces raw JSON editing of `rules`.
    change_form_template = "admin/email_marketing/segment/change_form.html"

    @admin.action(description=_("Rebuild member counts"), permissions=["change"])
    def rebuild_segments(self, request, queryset):
        for segment in queryset:
            segment.rebuild()
        self.message_user(request, _("Rebuilt %(n)d segment(s).") % {"n": queryset.count()})

    def _rule_builder_context(self):
        from django.urls import reverse

        from .services.segmentation import OPERATOR_LABELS, available_rule_fields

        return {
            "rule_fields": available_rule_fields(),
            "operator_labels": OPERATOR_LABELS,
            "segment_count_url": reverse("email_marketing_api:preview_segment_count"),
        }

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = {**(extra_context or {}), **self._rule_builder_context()}
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = {**(extra_context or {}), **self._rule_builder_context()}
        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Refresh the cached member count from the (possibly new) rules.
        obj.rebuild()

    def changelist_view(self, request, extra_context=None):
        qs = Segment.objects.filter(site=Site.objects.get(pk=1))
        extra_context = {
            **(extra_context or {}),
            "total_segments": qs.count(),
            "dynamic_segments": qs.filter(kind=Segment.KIND_DYNAMIC).count(),
            "static_segments": qs.filter(kind=Segment.KIND_STATIC).count(),
            "active_segments": qs.filter(is_active=True).count(),
            "kind_choices": Segment.KIND_CHOICES,
        }
        return super().changelist_view(request, extra_context)


class CampaignScheduleForm(forms.ModelForm):
    """Schedule form with a friendly A/B-subjects textarea (one subject per line)."""

    ab_test_subjects = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label=_("A/B subject lines"),
        help_text=_(
            "Optional: enter 2–4 subject lines, one per line, to A/B test each "
            "occurrence — every send splits the audience, tries each subject, and "
            "auto-sends the winner to the rest. Leave blank to send normally."
        ),
    )

    class Meta:
        model = CampaignSchedule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        # Always seed the textarea with a normalised string — never the raw list.
        # An empty default ([]) would otherwise render as literal "[]", which an
        # unchanged save then parses as one subject and rejects, blocking normal
        # (non-A/B) recurring schedules.
        self.initial["ab_test_subjects"] = "\n".join(instance.ab_subjects) if instance else ""

    def clean_ab_test_subjects(self):
        subjects = [ln.strip() for ln in self.cleaned_data.get("ab_test_subjects", "").splitlines()]
        subjects = [s for s in subjects if s]
        if len(subjects) == 1:
            raise forms.ValidationError(
                _("Enter at least two subject lines to A/B test, or leave this blank.")
            )
        return subjects[:4]


class CampaignScheduleInline(admin.StackedInline):
    model = CampaignSchedule
    form = CampaignScheduleForm
    extra = 0
    max_num = 1
    can_delete = True
    verbose_name = _("Schedule")
    verbose_name_plural = _("Schedule")
    fields = (
        "is_active",
        ("cadence", "interval"),
        ("weekday", "day_of_month"),
        ("send_time", "timezone"),
        ("freshness_policy", "hold_days"),
        "ab_test_subjects",
        ("ab_sample_percent", "ab_test_window_hours"),
        ("ab_winner_metric", "ab_auto_send_winner"),
        "next_run_at",
        "last_run_at",
        "occurrences_sent",
    )
    readonly_fields = ("next_run_at", "last_run_at", "occurrences_sent")


class CampaignSendInline(admin.TabularInline):
    model = CampaignSend
    extra = 0
    can_delete = False
    fields = ("subscriber", "status", "skip_reason", "opened", "clicked")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Campaign)
class CampaignAdmin(_SiteScopedAdmin):
    # Site is auto-set (single-tenant); parent is engine-managed (set when a
    # recurring template spawns an occurrence), so keep it off the form.
    exclude = ("site", "parent")
    list_display = (
        "name",
        "campaign_type",
        "status",
        "message_type",
        "segment",
        "total_recipients",
        "sent_count",
        "failed_count",
        "created_at",
    )
    list_filter = ("campaign_type", "status", "message_type")
    search_fields = ("name", "subject")
    autocomplete_fields = ("segment",)
    inlines = (CampaignScheduleInline,)
    readonly_fields = (
        "open_builder",
        "occurrence_history",
        "attribution_slug",  # engine-managed, set once at first send (not editable)
        "total_recipients",
        "sent_count",
        "failed_count",
        "skipped_count",
        "sent_at",
        "created_at",
        "updated_at",
    )

    def get_inline_instances(self, request, obj=None):
        # The schedule only applies to a recurring template — hide it otherwise.
        instances = super().get_inline_instances(request, obj)
        if not (obj and obj.campaign_type == Campaign.TYPE_RECURRING):
            instances = [i for i in instances if not isinstance(i, CampaignScheduleInline)]
        return instances

    def add_view(self, request, form_url="", extra_context=None):
        # Route "Add campaign" through the guided wizard instead of the raw form.
        from django.shortcuts import redirect

        return redirect("email_marketing_admin:campaign_wizard")

    def changelist_view(self, request, extra_context=None):
        # Count only real campaigns — exclude engine-managed children (A/B variants,
        # winner sends, recurring occurrences) so the dashboard cards match the list.
        qs = Campaign.objects.filter(site=Site.objects.get(pk=1), parent__isnull=True)
        extra_context = {
            **(extra_context or {}),
            "total_campaigns": qs.count(),
            "sent_campaigns": qs.filter(status=Campaign.STATUS_SENT).count(),
            "scheduled_campaigns": qs.filter(status=Campaign.STATUS_SCHEDULED).count(),
            "draft_campaigns": qs.filter(status=Campaign.STATUS_DRAFT).count(),
            "status_choices": Campaign.STATUS_CHOICES,
            "type_choices": Campaign.TYPE_CHOICES,
            "message_type_choices": MESSAGE_TYPE_CHOICES,
        }
        return super().changelist_view(request, extra_context)

    @admin.display(description=_("Occurrence history"))
    def occurrence_history(self, obj):
        from .models import ABTest

        if not obj or obj.campaign_type != Campaign.TYPE_RECURRING:
            return _("Occurrences appear here once this recurring campaign starts sending.")
        occurrences = list(obj.occurrences.order_by("-created_at")[:10])
        if not occurrences:
            return _("No occurrences sent yet.")
        # An A/B occurrence links to its results hub; a plain one to its change page.
        ab_by_campaign = {
            t.campaign_id: t
            for t in ABTest.objects.filter(campaign_id__in=[o.pk for o in occurrences])
        }
        items = []
        for o in occurrences:
            ab = ab_by_campaign.get(o.pk)
            if ab is not None:
                url = reverse("email_marketing_admin:ab_test_detail", args=[ab.id])
                detail = format_html("<em>{}</em> · {}", _("A/B"), ab.get_status_display())
            else:
                url = reverse("admin:email_marketing_campaign_change", args=[o.pk])
                detail = format_html("{} · {} {}", o.get_status_display(), o.sent_count, _("sent"))
            items.append((url, o.name, detail))
        rows = format_html_join("", '<li><a href="{}">{}</a> — {}</li>', items)
        return format_html("<ul>{}</ul>", rows)

    @admin.display(description=_("Visual builder"))
    def open_builder(self, obj):
        if not obj or not obj.pk:
            return _("Save the campaign first to open the builder.")
        url = reverse("email_marketing_admin:campaign_builder", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}"><i class="fas fa-wand-magic-sparkles"></i> {}</a>',
            url,
            _("Open visual builder"),
        )

    ordering = ("-created_at",)
    actions = ("send_now",)

    @admin.action(description=_("Send campaign now"), permissions=["change"])
    def send_now(self, request, queryset):
        from .services.campaigns import send_campaign

        for campaign in queryset:
            if campaign.parent_id is not None:
                # A/B variants, winner sends and recurring occurrences are engine
                # managed — sending one directly would blast it outside its flow
                # (a variant has no segment, so it would go to every subscriber).
                self.message_user(
                    request,
                    _(
                        "'%(name)s' is part of an A/B test or recurring series and can't be sent directly."
                    )
                    % {"name": campaign.name},
                    level=messages.WARNING,
                )
                continue
            if campaign.status not in (campaign.STATUS_DRAFT, campaign.STATUS_SCHEDULED):
                self.message_user(
                    request,
                    _("'%(name)s' is %(status)s and was skipped.")
                    % {"name": campaign.name, "status": campaign.get_status_display()},
                    level=messages.WARNING,
                )
                continue
            result = send_campaign(campaign)
            self.message_user(
                request,
                _("'%(name)s': %(queued)d queued, %(skipped)d skipped.")
                % {
                    "name": campaign.name,
                    "queued": result.get("queued", 0),
                    "skipped": result.get("skipped", 0),
                },
            )

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CampaignSend)
class CampaignSendAdmin(admin.ModelAdmin):
    list_display = ("campaign", "subscriber", "status", "opened", "clicked", "created_at")
    list_filter = ("status", "opened", "clicked")
    search_fields = ("subscriber__email", "campaign__name")
    readonly_fields = tuple(f.name for f in CampaignSend._meta.fields)
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False


@admin.register(Journey)
class JourneyAdmin(_SiteScopedAdmin):
    list_display = (
        "name",
        "trigger_event",
        "status",
        "email_count",
        "enrolled_count",
        "completed_count",
        "created_at",
    )
    list_filter = ("trigger_event", "status")
    search_fields = ("name",)
    autocomplete_fields = ("target_segment",)
    readonly_fields = ("enrolled_count", "completed_count", "created_at", "updated_at")
    ordering = ("-created_at",)

    @admin.display(description=_("Emails"))
    def email_count(self, obj):
        from .models import JourneyNode

        return obj.nodes.filter(node_type=JourneyNode.TYPE_SEND_EMAIL).count()

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        """After creating a journey, go straight into the flowchart builder."""
        from django.shortcuts import redirect

        if "_addanother" not in request.POST and "_continue" not in request.POST:
            return redirect("email_marketing_admin:journey_builder", journey_id=obj.id)
        return super().response_add(request, obj, post_url_continue)

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Sum

        qs = Journey.objects.filter(site=Site.objects.get(pk=1))
        agg = qs.aggregate(e=Sum("enrolled_count"), c=Sum("completed_count"))
        extra_context = {
            **(extra_context or {}),
            "total_journeys": qs.count(),
            "active_journeys": qs.filter(status=Journey.STATUS_ACTIVE).count(),
            "total_enrolled": agg["e"] or 0,
            "total_completed": agg["c"] or 0,
            "status_choices": Journey.STATUS_CHOICES,
            "trigger_choices": Journey.TRIGGER_CHOICES,
        }
        return super().changelist_view(request, extra_context)


@admin.register(JourneyEnrollment)
class JourneyEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "subscriber",
        "journey",
        "current_node",
        "status",
        "next_step_at",
        "started_at",
    )
    list_filter = ("status", "journey")
    search_fields = ("subscriber__email", "journey__name")
    readonly_fields = tuple(f.name for f in JourneyEnrollment._meta.fields)
    ordering = ("-started_at",)

    def has_add_permission(self, request):
        return False


@admin.register(SuppressionEntry)
class SuppressionEntryAdmin(_SiteScopedAdmin):
    """The do-not-mail list — addresses suppressed by a hard bounce, a spam
    complaint, or a manual block. Removing an entry (soft-delete) lets the address
    receive mail again."""

    list_display = ("email", "reason", "source", "created_at")
    list_filter = ("reason", "source", "created_at")
    search_fields = ("email", "detail")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def save_model(self, request, obj, form, change):
        from email_marketing.services import suppression

        # Route through the service so a hand-added entry gets the same treatment as an
        # ingested one: an idempotent upsert that restores a released (soft-deleted) row
        # rather than colliding on the (site, email) unique constraint, AND subscriber
        # reflection — a manual complaint / hard-bounce reason flips the matching
        # Subscriber, exactly as a bounce event would.
        obj.email = (obj.email or "").strip().lower()
        entry = suppression.suppress(
            Site.objects.get(pk=1),
            obj.email,
            obj.reason or SuppressionEntry.REASON_MANUAL,
            source=obj.source or SuppressionEntry.SOURCE_MANUAL,
            detail=obj.detail,
        )
        if entry is not None:
            obj.pk = entry.pk
