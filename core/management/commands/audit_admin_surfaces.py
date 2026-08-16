"""Audit the Django admin for capabilities that are DECLARED in code but MISSING
from the rendered UI — the "it exists in admin.py but a merchant can't reach it"
class of bug (e.g. registered actions with no actions bar, fieldset fields a
custom change_form template never emits, inlines that don't render).

The check is a *join*: for each declaration (action / field / inline) confirm its
specific control is present in the rendered HTML. Only ModelAdmins that OVERRIDE
the default template are at risk — the stock admin template renders everything —
so the field/action/inline checks are scoped to custom templates, which keeps
false positives low.

    ./manage.py audit_admin_surfaces                 # whole registry
    ./manage.py audit_admin_surfaces --app catalog   # one app (repeatable)
    ./manage.py audit_admin_surfaces --json          # machine-readable
    ./manage.py audit_admin_surfaces --fail-on-gaps  # exit 1 if gaps (CI guard)

Renders as an existing active superuser (or --user NAME) so no throwaway account
is created (creating one fires enrollment signals). GET-only; no writes.
"""

import json
import re
import sys
import types

from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.test import Client, RequestFactory

# (model_label, kind, detail) triples that are intentionally not surfaced.
# Populate as gaps are triaged so CI stays green on deliberate choices.
ALLOWLIST: set[tuple[str, str, str]] = set()

_ID = re.compile(r'id="([^"]+)"')
_NAME = re.compile(r'name="([^"]+)"')
_TOTAL_FORMS = re.compile(r'name="([\w\-]+)-TOTAL_FORMS"')


class Command(BaseCommand):
    help = "Find admin capabilities declared in code but missing from the rendered UI."

    def add_arguments(self, parser):
        parser.add_argument("--app", action="append", help="Limit to app label(s); repeatable.")
        parser.add_argument("--json", action="store_true", help="Emit JSON.")
        parser.add_argument("--fail-on-gaps", action="store_true", help="Exit 1 if gaps found.")
        parser.add_argument("--user", help="Username of the staff user to render as.")
        parser.add_argument(
            "--host", default="localhost", help="ALLOWED_HOSTS value to render under."
        )

    def handle(self, *args, **opts):
        User = get_user_model()
        if opts["user"]:
            user = User.objects.filter(username=opts["user"]).first()
            if user is None:
                raise CommandError(f"No user named {opts['user']!r}.")
        else:
            user = User.objects.filter(is_superuser=True, is_active=True).first()
            if user is None:
                raise CommandError("No active superuser to render as; pass --user NAME.")

        host = opts["host"]
        apps_filter = set(opts["app"]) if opts["app"] else None
        client = Client(raise_request_exception=False)
        client.force_login(user)
        rf = RequestFactory()

        def mkreq():
            r = rf.get("/")
            r.user = user
            # Several ModelAdmins read request.resolver_match.kwargs in
            # get_form/formfield_for_* — RequestFactory leaves it None.
            r.resolver_match = types.SimpleNamespace(kwargs={})
            return r

        findings = []
        scanned = 0

        def record(label, kind, detail, severity):
            if (label, kind, detail) in ALLOWLIST:
                severity = "ignored"
            findings.append({"model": label, "kind": kind, "detail": detail, "severity": severity})

        registry = sorted(
            admin.site._registry.items(),
            key=lambda kv: (kv[0]._meta.app_label, kv[0].__name__),
        )
        for model, ma in registry:
            meta = model._meta
            if apps_filter and meta.app_label not in apps_filter:
                continue
            scanned += 1
            label = f"{meta.app_label}.{meta.model_name}"
            req = mkreq()
            try:
                obj = model.objects.first()
            except Exception as e:  # noqa: BLE001  unmigrated / missing table, etc.
                record(label, "scan-error", f"objects.first(): {str(e)[:90]}", "info")
                continue
            base = f"/en/admin/{meta.app_label}/{meta.model_name}"
            custom_cl = bool(getattr(ma, "change_list_template", None))
            custom_cf = bool(getattr(ma, "change_form_template", None))
            overrides_content = self._overrides_content(ma) if custom_cl else False

            # ---- actions declared but not surfaced (custom changelist only) ----
            if custom_cl:
                try:
                    actions = list(ma.get_actions(req).keys())
                except Exception as e:  # noqa: BLE001
                    actions = []
                    record(label, "actions-introspect-error", str(e)[:120], "info")
                # Render once, only to catch changelists that crash.
                r = client.get(base + "/", SERVER_NAME=host)
                if r.status_code >= 500:
                    record(
                        label,
                        "changelist-500",
                        f"changelist crashes (HTTP {r.status_code})",
                        "high",
                    )
                if actions:
                    # Decide the gap STATICALLY from the template source: is the
                    # Django actions form wired in? Runtime rendering is
                    # unreliable — Django hides the actions bar when the table is
                    # empty, which would false-flag a template that has the form.
                    src = self._template_source(ma.change_list_template) or ""
                    # Present if the bar is inline, pulled in via the shared
                    # include, or inherited from the default changelist through
                    # {{ block.super }} inside the content block.
                    has_form = bool(
                        re.search(r'action_form\.action|name="action"|bulk_actions_open', src)
                    ) or self._content_uses_block_super(src)
                    if not has_form:
                        if overrides_content:
                            try:
                                rows = model.objects.exists()
                            except Exception:  # noqa: BLE001
                                rows = None
                            record(
                                label,
                                "actions-bar-missing",
                                f"{len(actions)} action(s) unreachable (rows={rows}): {actions}",
                                "high",
                            )
                        else:
                            record(
                                label,
                                "actions-bar-absent-nontemplate",
                                "no actions form; inherits default bar (data-gated at runtime)",
                                "info",
                            )

            # ---- fields / inlines declared but not rendered (custom change form only) ----
            if custom_cf:
                bound = None
                fields = None
                try:
                    form_cls = ma.get_form(req, obj=obj)
                    bound = form_cls(instance=obj) if obj is not None else form_cls()
                    fields = list(form_cls.base_fields.keys())
                except Exception:  # noqa: BLE001
                    try:
                        declared = flatten_fieldsets(ma.get_fieldsets(req, obj))
                        readonly = set(ma.get_readonly_fields(req, obj))
                        model_fields = {f.name for f in meta.get_fields()}
                        fields = [f for f in declared if f not in readonly and f in model_fields]
                    except Exception as e:  # noqa: BLE001
                        record(label, "form-introspect-error", str(e)[:120], "info")

                target = f"{base}/{obj.pk}/change/" if obj is not None else f"{base}/add/"
                r = client.get(target, SERVER_NAME=host)
                if r.status_code >= 500:
                    record(
                        label,
                        "changeform-500",
                        f"change form crashes (HTTP {r.status_code})",
                        "high",
                    )
                elif r.status_code != 200:
                    record(
                        label,
                        "changeform-not-rendered",
                        f"{target} -> HTTP {r.status_code}",
                        "info",
                    )
                else:
                    page = r.content.decode("utf-8", "ignore")
                    for name in fields or []:
                        if not self._field_present(name, bound, page):
                            record(label, "field-not-rendered", name, "high")
                    try:
                        inlines = ma.get_inline_instances(req, obj=obj)
                    except Exception:  # noqa: BLE001
                        inlines = []
                    present = set(_TOTAL_FORMS.findall(page))
                    for inl in inlines:
                        try:
                            prefix = inl.get_formset(req, obj).get_default_prefix()
                        except Exception:  # noqa: BLE001
                            prefix = None
                        if prefix is None or not any(
                            p == prefix or p.startswith(prefix + "-") or p.startswith(prefix)
                            for p in present
                        ):
                            record(
                                label,
                                "inline-not-rendered",
                                f"{inl.model.__name__} (prefix={prefix})",
                                "high",
                            )

        self._output(scanned, findings, opts)
        gaps = [f for f in findings if f["severity"] in ("high", "medium")]
        if opts["fail_on_gaps"] and gaps:
            sys.exit(1)

    # ---- helpers ----
    @staticmethod
    def _template_source(name):
        try:
            from django.template.loader import get_template

            return get_template(name).template.source
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _content_uses_block_super(src):
        """True if the template's {% block content %} renders {{ block.super }} —
        i.e. it inherits the default changelist (table + actions bar + checkboxes)."""
        m = re.search(r"{%\s*block\s+content\s*%}(.*?){%\s*endblock", src, re.S)
        return bool(m and "block.super" in m.group(1))

    @classmethod
    def _overrides_content(cls, ma):
        """Does the ModelAdmin's changelist template override {% block content %}?

        If it does and the actions form isn't wired in, that's a genuine gap. If
        it only tweaks object-tools/extrahead, the default content (with the
        actions bar) still renders and an absent bar is just data-driven.
        """
        src = cls._template_source(ma.change_list_template) or ""
        return bool(re.search(r"{%\s*block\s+content\s*%}", src))

    @staticmethod
    def _field_present(name, bound, page):
        """Is the field's actual widget present in the rendered page?

        Prefer rendering the bound field to learn its real ids/names (handles
        MoneyField -> id_x_0/id_x_1, split widgets, custom widgets); fall back to
        substring matching with a trailing-underscore variant for multiwidgets.
        """
        if bound is not None:
            try:
                widget_html = str(bound[name])
                ids = [f'id="{i}"' for i in _ID.findall(widget_html)]
                names = [f'name="{n}"' for n in _NAME.findall(widget_html)]
                tokens = ids + names
                if tokens:
                    return any(t in page for t in tokens)
            except Exception:  # noqa: BLE001
                pass
        return (
            f'id="id_{name}"' in page
            or f'id="id_{name}_' in page
            or f'name="{name}"' in page
            or f'name="{name}_' in page
        )

    def _output(self, scanned, findings, opts):
        if opts["json"]:
            self.stdout.write(json.dumps({"scanned": scanned, "findings": findings}, indent=2))
            return
        custom_note = ""
        self.stdout.write("\n===== ADMIN SURFACE AUDIT =====")
        self.stdout.write(f"ModelAdmins scanned: {scanned}{custom_note}")
        gaps = [f for f in findings if f["severity"] in ("high", "medium")]
        info = [f for f in findings if f["severity"] == "info"]
        ignored = [f for f in findings if f["severity"] == "ignored"]
        if not gaps:
            self.stdout.write(self.style.SUCCESS("\nNo gaps found."))
        else:
            by_kind = {}
            for f in gaps:
                by_kind.setdefault(f["kind"], []).append(f)
            order = [
                "actions-bar-missing",
                "action-not-in-dropdown",
                "field-not-rendered",
                "inline-not-rendered",
            ]
            self.stdout.write(self.style.WARNING(f"\n{len(gaps)} gap(s):"))
            for kind in order + [k for k in by_kind if k not in order]:
                for f in by_kind.get(kind, []):
                    self.stdout.write(f"  [{kind}] {f['model']:34} {f['detail']}")
        if info:
            self.stdout.write(f"\n{len(info)} render/introspect note(s) (not gaps):")
            for f in info:
                self.stdout.write(f"  [{f['kind']}] {f['model']:34} {f['detail']}")
        if ignored:
            self.stdout.write(f"\n{len(ignored)} allowlisted (suppressed).")
