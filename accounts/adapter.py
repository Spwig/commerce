"""
Custom allauth account adapter.

Provides role-aware login redirect: staff → admin, customers → dashboard.
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.utils.translation import get_language


class SpwigAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        """
        Redirect staff to admin, customers to their account dashboard.
        Uses the active language prefix so the destination matches the
        language the user was browsing in.
        """
        lang = get_language() or 'en'
        if request.user.is_staff:
            return f'/{lang}/admin/'
        return f'/{lang}/account/dashboard/'
