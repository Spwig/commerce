"""
Voucher import wizard + XLSX export action.

Three views back the import flow:
  1. `VoucherImportUploadView`  — page 1: upload + batch settings form
  2. `VoucherImportPreviewView` — page 2: column mapping + dup strategy
                                            (also handles the POST that
                                            actually commits the import)
  3. `VoucherImportResultView`  — page 3: post-commit summary

The actual file parsing, validation, and bulk-create work lives in
`vouchers.services.voucher_importer` so the views stay focused on
HTTP / form-binding / session handoff.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from django import forms
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from djmoney.money import Money

from migration.models import MigrationJob
from vouchers.models import VoucherCode
from vouchers.services.voucher_importer import (
    ALLOWED_EXTENSIONS,
    DUPLICATE_STRATEGIES,
    EXPORT_COLUMNS,
    MAPPABLE_FIELDS,
    MAX_UPLOAD_BYTES,
    auto_detect_mapping,
    build_preview,
    export_queryset,
    import_batch,
    parse_file,
)

logger = logging.getLogger(__name__)

#: Key under which the parsed upload + batch settings get stashed in the
#: admin's session between page 1 and page 2. One-shot — cleared on
#: successful import or when the user starts a new upload.
SESSION_KEY = "voucher_import_pending"


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

class VoucherImportSettingsForm(forms.Form):
    """Batch-level settings that apply to every imported row.

    Mirrors the `VoucherCode` add-form fields the merchant would set if
    they were creating one voucher by hand. We accept money inputs as
    plain decimal strings here (rather than a `MoneyField` widget) so
    the form layout stays compact — currency defaults to the store's
    default currency at save time via the `currency_code` hidden input
    set from the model defaults.
    """

    file = forms.FileField(
        label=_("File"),
        help_text=_("CSV or XLSX. Maximum 5 MB."),
    )

    discount_type = forms.ChoiceField(
        choices=VoucherCode.DISCOUNT_TYPES,
        initial="percentage",
        label=_("Discount type"),
    )
    discount_value = forms.DecimalField(
        max_digits=10, decimal_places=2,
        min_value=Decimal("0.01"),
        label=_("Discount value"),
        help_text=_("Percentage (0–100) or fixed amount."),
    )
    max_discount_amount = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2,
        label=_("Max discount amount"),
        help_text=_("Cap for percentage discounts. Leave blank for no cap."),
    )
    application_scope = forms.ChoiceField(
        choices=VoucherCode.APPLICATION_SCOPES,
        initial="cart",
        label=_("Application scope"),
    )

    start_date = forms.DateTimeField(
        required=False,
        label=_("Start date"),
        help_text=_("Defaults to right now."),
    )
    end_date = forms.DateTimeField(
        required=False,
        label=_("End date"),
        help_text=_("Leave blank for no fixed expiry."),
    )
    days_valid = forms.IntegerField(
        required=False, min_value=1,
        label=_("Days valid"),
        help_text=_("Days from creation. Overrides end date when set."),
    )

    max_uses_total = forms.IntegerField(
        required=False, min_value=1,
        label=_("Max uses total"),
    )
    max_uses_per_customer = forms.IntegerField(
        required=False, min_value=1,
        label=_("Max uses per customer"),
    )
    min_order_value = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2,
        label=_("Minimum order value"),
    )

    exclude_sale_items = forms.BooleanField(required=False, initial=False)
    cannot_combine_with_other_vouchers = forms.BooleanField(required=False, initial=False)
    cannot_combine_with_sale_items = forms.BooleanField(required=False, initial=False)
    first_time_customers_only = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)

    currency_code = forms.CharField(
        max_length=3, required=False,
        widget=forms.HiddenInput,
        help_text=_("ISO currency code applied to monetary settings."),
    )

    def clean_file(self):
        f = self.cleaned_data["file"]
        name = (f.name or "").lower()
        if not name.endswith(ALLOWED_EXTENSIONS):
            raise ValidationError(
                _("Unsupported file type. Upload a .csv or .xlsx file.")
            )
        if f.size > MAX_UPLOAD_BYTES:
            raise ValidationError(
                _("File is too large. Maximum upload size is 5 MB.")
            )
        return f

    def to_batch_settings(self) -> dict[str, Any]:
        """Translate cleaned form data into kwargs for `VoucherCode(...)`.

        Strips the file (handled separately), strips `currency_code`
        (consumed locally), and wraps money values in `Money` objects so
        `MoneyField` columns get a currency.
        """
        data = {k: v for k, v in self.cleaned_data.items() if k not in {"file", "currency_code"}}
        currency = self.cleaned_data.get("currency_code") or _store_default_currency()
        for money_key in ("max_discount_amount", "min_order_value"):
            value = data.get(money_key)
            if value in (None, ""):
                data.pop(money_key, None)
            else:
                data[money_key] = Money(value, currency)
        return data


def _store_default_currency() -> str:
    """Best-effort default currency lookup for batch money settings."""
    try:
        from core.utils import get_default_currency
        return str(get_default_currency())
    except Exception:
        return "USD"


# ---------------------------------------------------------------------------
# Session payload helpers — keeps the parsed file out of disk between
# pages 1 and 2 while still surviving a redirect. Capped well under the
# 5 MB upload limit because we only keep a compact dict per row, not the
# original bytes.
# ---------------------------------------------------------------------------

def _stash(request, payload: dict[str, Any]) -> None:
    request.session[SESSION_KEY] = payload
    request.session.modified = True


def _read_stash(request) -> dict[str, Any] | None:
    return request.session.get(SESSION_KEY)


def _clear_stash(request) -> None:
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]
        request.session.modified = True


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

class _AdminViewMixin:
    """Common context every page in the wizard needs to render inside
    the Django admin shell (title bar, breadcrumbs, app verbose names)."""

    title: str = ""

    def admin_context(self, **extra) -> dict[str, Any]:
        from django.contrib import admin
        site = admin.site
        return {
            "title": self.title,
            "site_title": site.site_title,
            "site_header": site.site_header,
            "site_url": site.site_url,
            "has_permission": True,
            "available_apps": site.get_app_list(self.request),
            "is_popup": False,
            "is_nav_sidebar_enabled": True,
            "opts": VoucherCode._meta,
            "app_label": VoucherCode._meta.app_label,
            "model_name": VoucherCode._meta.model_name,
            **extra,
        }


@method_decorator(staff_member_required, name="dispatch")
@method_decorator(
    permission_required("vouchers.add_vouchercode", raise_exception=True),
    name="dispatch",
)
class VoucherImportUploadView(_AdminViewMixin, View):
    """Page 1: upload + batch settings."""

    title = _("Import voucher codes")
    template_name = "admin/vouchers/vouchercode/import_upload.html"

    def get(self, request):
        form = VoucherImportSettingsForm(
            initial={"currency_code": _store_default_currency()}
        )
        return render(request, self.template_name, self.admin_context(form=form))

    def post(self, request):
        form = VoucherImportSettingsForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, self.admin_context(form=form))

        try:
            parsed = parse_file(form.cleaned_data["file"])
        except ValidationError as exc:
            form.add_error("file", exc)
            return render(request, self.template_name, self.admin_context(form=form))

        if not parsed.rows:
            form.add_error("file", _("The uploaded file is empty."))
            return render(request, self.template_name, self.admin_context(form=form))

        # Persist the parsed file + batch settings under a session key so
        # the preview page can render without a second upload round-trip.
        # Settings are serialised through `to_batch_settings` once here
        # so Money objects (etc.) don't end up in the session as
        # non-JSON-serialisable values.
        batch_settings = _settings_for_session(form.to_batch_settings())
        _stash(request, {
            "headers": parsed.headers,
            "rows": parsed.rows,
            "row_count": parsed.row_count,
            "batch_settings": batch_settings,
            "currency": form.cleaned_data.get("currency_code") or _store_default_currency(),
        })
        return redirect("admin:vouchers_vouchercode_import_preview")


@method_decorator(staff_member_required, name="dispatch")
@method_decorator(
    permission_required("vouchers.add_vouchercode", raise_exception=True),
    name="dispatch",
)
class VoucherImportPreviewView(_AdminViewMixin, View):
    """Page 2: column mapping + dup strategy + commit."""

    title = _("Preview voucher import")
    template_name = "admin/vouchers/vouchercode/import_preview.html"

    def get(self, request):
        payload = _read_stash(request)
        if not payload:
            messages.warning(
                request, _("Upload a file first to start an import.")
            )
            return redirect("admin:vouchers_vouchercode_import")

        from vouchers.services.voucher_importer import ParsedFile  # local import to avoid circular
        parsed = ParsedFile(
            headers=payload["headers"],
            rows=payload["rows"],
            row_count=payload["row_count"],
        )
        mapping = auto_detect_mapping(parsed.headers)
        preview = build_preview(parsed, mapping)

        return render(request, self.template_name, self.admin_context(
            parsed=parsed,
            preview=preview,
            mapping=mapping,
            mappable_fields=MAPPABLE_FIELDS,
            duplicate_strategies=DUPLICATE_STRATEGIES,
            preview_rows=parsed.first(20),
        ))

    def post(self, request):
        payload = _read_stash(request)
        if not payload:
            messages.warning(
                request, _("Upload a file first to start an import.")
            )
            return redirect("admin:vouchers_vouchercode_import")

        # Pull mapping + strategy off the form.
        mapping: dict[str, str] = {}
        for target in MAPPABLE_FIELDS:
            value = (request.POST.get(f"map_{target}") or "").strip()
            if value:
                mapping[target] = value
        dup_strategy = request.POST.get("duplicate_strategy", "skip")
        if dup_strategy not in DUPLICATE_STRATEGIES:
            dup_strategy = "skip"

        from vouchers.services.voucher_importer import ParsedFile
        parsed = ParsedFile(
            headers=payload["headers"],
            rows=payload["rows"],
            row_count=payload["row_count"],
        )

        batch_settings = _settings_from_session(
            payload.get("batch_settings") or {},
            payload.get("currency") or _store_default_currency(),
        )

        try:
            result = import_batch(
                parsed=parsed,
                mapping=mapping,
                batch_settings=batch_settings,
                dup_strategy=dup_strategy,
                user=request.user,
            )
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages))
            preview = build_preview(parsed, mapping)
            return render(request, self.template_name, self.admin_context(
                parsed=parsed,
                preview=preview,
                mapping=mapping,
                mappable_fields=MAPPABLE_FIELDS,
                duplicate_strategies=DUPLICATE_STRATEGIES,
                preview_rows=parsed.first(20),
                selected_strategy=dup_strategy,
            ))

        _clear_stash(request)
        messages.success(
            request,
            _("Imported {imported}, updated {updated}, skipped {skipped}.").format(
                imported=result.imported,
                updated=result.updated,
                skipped=result.skipped_duplicate + result.skipped_invalid,
            ),
        )
        return redirect(
            "admin:vouchers_vouchercode_import_result",
            job_id=result.migration_job_id,
        )


@method_decorator(staff_member_required, name="dispatch")
@method_decorator(
    permission_required("vouchers.view_vouchercode", raise_exception=True),
    name="dispatch",
)
class VoucherImportResultView(_AdminViewMixin, View):
    """Page 3: post-commit summary."""

    title = _("Voucher import complete")
    template_name = "admin/vouchers/vouchercode/import_result.html"

    def get(self, request, job_id):
        try:
            job = MigrationJob.objects.get(id=job_id)
        except MigrationJob.DoesNotExist:
            messages.error(request, _("Import job not found."))
            return redirect("admin:vouchers_vouchercode_changelist")

        return render(request, self.template_name, self.admin_context(
            job=job,
            vouchers_url=reverse("admin:vouchers_vouchercode_changelist"),
        ))


# ---------------------------------------------------------------------------
# XLSX export — wired up as an admin action in vouchers.admin
# ---------------------------------------------------------------------------

def export_vouchers_xlsx(modeladmin, request, queryset):
    """Admin action: download selected vouchers as an XLSX matching the
    importer's column shape (so the file round-trips)."""
    return export_queryset(queryset, fmt="xlsx", filename="vouchers_export")


export_vouchers_xlsx.short_description = _("Export selected vouchers to XLSX")


# ---------------------------------------------------------------------------
# Session (de)serialisation
# ---------------------------------------------------------------------------

def _settings_for_session(settings: dict[str, Any]) -> dict[str, Any]:
    """Translate the form's cleaned data into a JSON-safe dict."""
    out: dict[str, Any] = {}
    for key, value in settings.items():
        if isinstance(value, Money):
            out[key] = {"__money__": str(value.amount), "currency": str(value.currency)}
        elif isinstance(value, Decimal):
            out[key] = str(value)
        elif isinstance(value, datetime):
            out[key] = value.isoformat()
        elif isinstance(value, bool) or value is None or isinstance(value, (int, str)):
            out[key] = value
        else:
            out[key] = str(value)
    return out


def _settings_from_session(serialised: dict[str, Any], default_currency: str) -> dict[str, Any]:
    """Inverse of `_settings_for_session` — restores `Money`, `Decimal`,
    and `datetime` types so `import_batch` can drop the dict straight
    into `VoucherCode(**settings)`."""
    out: dict[str, Any] = {}
    decimal_keys = {"discount_value"}
    datetime_keys = {"start_date", "end_date"}
    for key, value in serialised.items():
        if isinstance(value, dict) and "__money__" in value:
            out[key] = Money(Decimal(value["__money__"]), value.get("currency") or default_currency)
        elif key in decimal_keys and isinstance(value, str):
            try:
                out[key] = Decimal(value)
            except InvalidOperation:
                continue
        elif key in datetime_keys and isinstance(value, str):
            try:
                out[key] = datetime.fromisoformat(value)
            except ValueError:
                continue
        else:
            out[key] = value
    return out
