"""
Provider Template Integrity Tests

Built-in provider templates are rendered by ``email_system/views/wizard.py``
with ``Template(...)`` / ``template.render(...)`` rather than through the
normal loader, so a broken one is not caught by the usual template checks.
Step 4 of the email wizard swallows the failure in a broad ``except`` and
redirects the merchant back to step 3, which makes the breakage look like a
navigation quirk instead of a template bug.

Two failure modes are covered here, because both have shipped before:

1. **Compile failure** — e.g. ``{% static %}`` used above the ``{% load
   static %}`` that registers it. Django registers ``{% load %}``
   sequentially at compile time, so the position of the load tag matters.
   Regression for the builtin ``dns_requirements.html`` fix.

2. **Render-only failure** — Django's ``tag_re`` has no ``re.DOTALL``, so a
   ``{# ... #}`` comment spanning a newline is *not* a comment. Templates
   carrying that bug compile cleanly and only leak in rendered output, so
   compiling alone is not a sufficient check.

Scope is the tracked ``email_system/providers/`` tree only. Installed
marketplace components live under ``components_data/``, which is gitignored
install state and absent in a fresh clone or CI.
"""

import json
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.template import Context, Template

pytestmark = [pytest.mark.integrity]


PROVIDERS_DIR = Path(settings.BASE_DIR) / "email_system" / "providers"

# Leftover reference copies are kept beside the live templates for diffing
# intent; they are never rendered, so they are not held to this standard.
EXCLUDED_SUFFIXES = ("_OLD.html",)

# Superset of the context the wizard builds, so a template can be rendered
# without standing up DNS lookups or an EmailAccount. Django templates treat
# missing keys as empty, so extra keys are harmless; the point is that every
# key a provider template dereferences resolves to something renderable.
RENDER_CONTEXT = {
    "domain": "example.com",
    "from_email": "hello@example.com",
    "account_name": "Test Account",
    "server_ip": "203.0.113.5",
    "mx_hostname": "mail.example.com",
    "dkim_selector": "spwig",
    "dkim_dns_hostname": "spwig._domainkey.example.com",
    "dkim_dns_record": "v=DKIM1; k=rsa; p=TESTKEY",
    "dkim_keys_exist": True,
    "spf_recommendation": "v=spf1 a mx ~all",
    "dmarc_recommendation": "v=DMARC1; p=none; aspf=r; adkim=r",
    "dns_results": {},
    "dns_provider": "cloudflare",
    "dns_provider_display": "Cloudflare",
    "dns_nameservers": ["ns1.cloudflare.com"],
    "dns_confidence": "high",
}

# Anything surviving into rendered output means a tag was not parsed as a tag.
UNRENDERED_MARKERS = ("{%", "%}", "{#", "#}", "{{", "}}")


def _provider_templates():
    """Every provider HTML template the wizard may render."""
    return sorted(
        p for p in PROVIDERS_DIR.rglob("*.html") if not p.name.endswith(EXCLUDED_SUFFIXES)
    )


def _template_ids():
    return [str(p.relative_to(PROVIDERS_DIR)) for p in _provider_templates()]


def test_provider_templates_exist():
    """Guard against the parametrised tests silently covering nothing."""
    assert _provider_templates(), f"No provider templates found under {PROVIDERS_DIR}"


@pytest.mark.parametrize("path", _provider_templates(), ids=_template_ids())
def test_provider_template_compiles(path):
    """Template compiles — catches load-order and unknown-filter errors."""
    Template(path.read_text(encoding="utf-8"))


@pytest.mark.django_db
@pytest.mark.parametrize("path", _provider_templates(), ids=_template_ids())
def test_provider_template_renders_without_leaking_tags(path):
    """Template renders and leaves no template syntax in the output.

    Compiling is not enough: a multi-line ``{# #}`` comment compiles fine and
    leaks verbatim into what the merchant sees.

    Needs the DB because these templates ``{% include %}`` wizard partials,
    and ``design.template_loader`` resolves those against the active Theme.
    """
    rendered = Template(path.read_text(encoding="utf-8")).render(Context(RENDER_CONTEXT))

    leaked = [marker for marker in UNRENDERED_MARKERS if marker in rendered]
    assert not leaked, f"{path.name} leaked unrendered template syntax: {leaked}"


@pytest.mark.django_db
@pytest.mark.parametrize("path", _provider_templates(), ids=_template_ids())
def test_provider_template_json_blocks_parse(path):
    """Any embedded application/json block must survive rendering as valid JSON.

    These blocks feed the wizard's client-side JS; a leaked tag or an
    unescaped value breaks them at runtime rather than at render time.
    """
    rendered = Template(path.read_text(encoding="utf-8")).render(Context(RENDER_CONTEXT))

    blocks = re.findall(
        r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
        rendered,
        re.DOTALL,
    )
    for block in blocks:
        json.loads(block)


def test_builtin_dns_requirements_loads_static_before_use():
    """Regression: ``{% static %}`` at line 7 with ``{% load static %}`` at line 600.

    Django registers ``{% load %}`` sequentially at compile time, so a load tag
    below its first use raises "Invalid block tag ... 'static'". That broke
    wizard step 4 for the builtin SMTP provider, which redirected the merchant
    back to step 3 with a raw framework error.
    """
    path = PROVIDERS_DIR / "builtin" / "dns_requirements.html"
    lines = path.read_text(encoding="utf-8").splitlines()

    first_load = next(
        (i for i, line in enumerate(lines) if "{% load" in line and "static" in line),
        None,
    )
    first_use = next((i for i, line in enumerate(lines) if "{% static" in line), None)

    assert first_use is not None, "Expected the builtin template to use {% static %}"
    assert first_load is not None, "{% load static %} is missing"
    assert first_load < first_use, (
        f"{{% load static %}} on line {first_load + 1} must come before the first "
        f"{{% static %}} use on line {first_use + 1}"
    )
