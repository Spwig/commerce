import logging

logger = logging.getLogger(__name__)


class SetupWizardMiddleware:
    """
    Middleware placeholder for setup wizard.

    The setup wizard is now embedded as a modal on the Shop Dashboard,
    so this middleware no longer redirects to a standalone wizard page.
    Kept as a pass-through to avoid breaking MIDDLEWARE setting.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
