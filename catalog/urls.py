"""
Storefront (non-API) URLs for the catalog app.

Lives inside i18n_patterns — these are localised customer pages, so they carry
the language prefix (/en/gift-cards/balance/), unlike the JSON endpoints at
/api/catalog/ which never do.
"""

from django.urls import path
from django.views.generic import RedirectView

from .views import storefront as catalog_views

app_name = "catalog"

urlpatterns = [
    # The gift card balance page. The delivery email has pointed customers at
    # a balance URL since P2.3; until now nothing was routed there, so every
    # email sent carried a 404 about real money.
    path(
        "gift-cards/balance/",
        catalog_views.gift_card_balance_page,
        name="gift_card_balance",
    ),
    # Sent emails are immutable: everything already delivered says
    # /gift-cards/check-balance/, so that spelling redirects forever.
    path(
        "gift-cards/check-balance/",
        RedirectView.as_view(pattern_name="catalog:gift_card_balance", permanent=True),
    ),
]
