"""
Public ``.well-known`` discovery views.

Mounted in the FIRST urlpatterns block of core/urls.py — before the activation,
licence, and setup-wizard middleware — so a discovery request is never answered
with a redirect to /activate/. nginx passes everything under /.well-known/
except acme-challenge through to Django, so no web-server change is needed.
"""

from __future__ import annotations

from django.http import JsonResponse

from agentic.gating import require_agentic, require_protocol
from agentic.services.profile_service import build_ucp_profile


def ucp_discovery(request):
    """
    Serve ``/.well-known/ucp``.

    404 when agentic commerce (or the UCP surface) is off — off is invisible, a
    crawler cannot tell an opted-out store from one that lacks the feature. When
    on, returns the UCP discovery profile. Cacheable: unlike the per-agent API
    surface, this document is the same for everyone.
    """
    require_agentic()
    require_protocol("ucp")

    profile = build_ucp_profile(request)
    response = JsonResponse(profile)
    response["Cache-Control"] = "public, max-age=300"
    return response
