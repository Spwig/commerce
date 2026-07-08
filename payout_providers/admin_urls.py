"""
Payout Provider Admin AJAX URLs

Filter endpoints for admin list views.
Included inside i18n_patterns as:
    path('admin/payout-providers/', include('payout_providers.admin_urls'))
"""

from django.urls import path
from . import admin_views

app_name = 'payout_providers_admin'

urlpatterns = [
    path('accounts/filter/', admin_views.filter_providers, name='filter_providers'),
]
