"""
Admin form + widget for API token scopes.

Renders the scope registry (``core.api_scopes``) as a grouped, CSP-safe picker:
one radio group per scope with None / Read / Read & Write options (the write
option is omitted for read-only scopes). Serialises the selection back into the
``{scope_key: level}`` dict stored on ``APIToken.scopes``.

All styling and behaviour live in external assets
(``core/admin/apitoken/scope_editor.{css,js}``) loaded via ``Media`` — no inline
styles or scripts, per the platform CSP rules.
"""

from django import forms
from django.forms import ModelForm
from django.utils.html import format_html, format_html_join, mark_safe
from django.utils.translation import gettext_lazy as _

from core.api_scopes import get_available_scopes, get_scopes_grouped
from core.models import APIToken

LEVEL_LABELS = {
    "": _("No access"),
    "read": _("Read"),
    "write": _("Read & Write"),
}


class ScopeSelectWidget(forms.Widget):
    """Grouped radio picker for API token scopes."""

    class Media:
        css = {"all": ["core/admin/apitoken/scope_editor.css"]}
        js = ["core/admin/apitoken/scope_editor.js"]

    def value_from_datadict(self, data, files, name):
        """Collect ``{name}_{scope_key}`` radio values into a level dict."""
        selection = {}
        for key in get_available_scopes():
            level = data.get(f"{name}_{key}", "")
            if level in ("read", "write"):
                selection[key] = level
        return selection

    def _radio(self, field_name, scope_key, level, current):
        checked = " checked" if current == level else ""
        input_id = f"id_{field_name}_{scope_key}_{level or 'none'}"
        return format_html(
            '<label class="scope-opt" for="{}">'
            '<input type="radio" id="{}" name="{}_{}" value="{}"{}> {}</label>',
            input_id,
            input_id,
            field_name,
            scope_key,
            level,
            mark_safe(checked),
            LEVEL_LABELS[level],
        )

    def render(self, name, value, attrs=None, renderer=None):
        value = value or {}
        groups_html = []
        for group_label, items in get_scopes_grouped():
            rows = []
            for scope_key, meta in items:
                current = value.get(scope_key, "")
                opts = [self._radio(name, scope_key, "", current)]
                opts.append(self._radio(name, scope_key, "read", current))
                if meta["supports_write"]:
                    opts.append(self._radio(name, scope_key, "write", current))
                rows.append(
                    format_html(
                        '<tr class="scope-row" data-scope-key="{}">'
                        '<td class="scope-meta"><span class="scope-label">{}</span>'
                        '<span class="scope-desc">{}</span></td>'
                        '<td class="scope-opts">{}</td></tr>',
                        scope_key,
                        meta["label"],
                        meta["description"],
                        mark_safe("".join(opts)),
                    )
                )
            groups_html.append(
                format_html(
                    '<div class="scope-group">'
                    '<div class="scope-group__head">'
                    '<span class="scope-group__title">{}</span>'
                    '<button type="button" class="scope-group__clear" '
                    'data-action="clear-group">{}</button></div>'
                    '<table class="scope-table"><tbody>{}</tbody></table></div>',
                    group_label,
                    _("Clear group"),
                    mark_safe("".join(rows)),
                )
            )
        note = format_html(
            '<div class="scope-note" role="note">'
            '<i class="fas fa-info-circle scope-note__icon" aria-hidden="true"></i>'
            '<div class="scope-note__body">'
            "<p>{}</p><p>{}</p></div></div>",
            _(
                "A token can only do what the staff member who creates it can do "
                "— and never more. Owner/superuser powers are always removed "
                "from tokens."
            ),
            _(
                "If the creating account has read-only access, any Read & Write "
                "scopes granted below will not take effect — the token will be "
                "limited to reading."
            ),
        )
        return format_html(
            '<div class="scope-editor" data-scope-editor>{}{}</div>',
            note,
            mark_safe("".join(groups_html)),
        )


class ScopeField(forms.Field):
    """Form field whose value is the ``{scope_key: level}`` dict."""

    widget = ScopeSelectWidget

    def clean(self, value):
        value = value or {}
        available = get_available_scopes()
        cleaned = {}
        for key, level in value.items():
            meta = available.get(key)
            if meta is None:
                raise forms.ValidationError(
                    _("Unknown or unavailable API scope: %(key)s"), params={"key": key}
                )
            if level == "write" and not meta["supports_write"]:
                raise forms.ValidationError(
                    _("The %(key)s scope is read-only."), params={"key": key}
                )
            if level not in ("read", "write"):
                continue
            cleaned[key] = level
        return cleaned


class APITokenAdminForm(ModelForm):
    """Token admin form with a grouped scope picker."""

    scopes = ScopeField(
        required=False,
        label=_("API Scopes"),
        help_text=_(
            "Choose which admin APIs this token may call and at what level. "
            "A token with no scopes selected cannot reach any API."
        ),
    )

    class Meta:
        model = APIToken
        fields = "__all__"


def render_scope_summary(obj):
    """
    Read-only "This token can access:" summary for the change form.

    Returns HTML listing granted scopes grouped nothing-fancy, or a hint when
    the token has no scopes.
    """
    granted = obj.granted_scopes() if obj and obj.pk else []
    if not granted:
        return format_html(
            '<div class="scope-summary scope-summary--empty">{}</div>',
            _("This token has no API access. Select one or more scopes above."),
        )
    # Level pill styled with the same admin theme variables the shared
    # .list-row-card-badge component uses, but self-contained so it needs no
    # global admin-base.css on the default change form. 'write' reads as an
    # elevated (warning) pill; 'read' as a neutral one.
    items = format_html_join(
        "",
        '<li class="scope-summary__item"><span class="scope-summary__name">{}</span>'
        '<span class="scope-summary__level scope-summary__level--{}">{}</span></li>',
        (
            (
                g["label"],
                "write" if g["level"] == "write" else "read",
                _("Read & Write") if g["level"] == "write" else _("Read"),
            )
            for g in granted
        ),
    )
    return format_html(
        '<div class="scope-summary"><div class="scope-summary__head">{}</div>'
        '<ul class="scope-summary__list">{}</ul></div>',
        _("This token can access:"),
        items,
    )
