"""
Custom MFA Views

Extends django-allauth MFA views to add trusted device functionality.
"""

from allauth.account import app_settings as account_settings
from allauth.account.stages import LoginStageController
from allauth.mfa import app_settings
from allauth.mfa.forms import AuthenticateForm
from allauth.mfa.models import Authenticator
from allauth.mfa.stages import AuthenticateStage
from allauth.mfa.utils import is_mfa_enabled
from allauth.utils import get_form_class
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView

from core.models import SiteSettings, TrustedDevice


class TrustedDeviceAuthenticateForm(AuthenticateForm):
    """Extended MFA authenticate form with 'remember this device' option"""

    def __init__(self, *args, **kwargs):
        self.remember_device = kwargs.pop("remember_device", False)
        super().__init__(*args, **kwargs)


class CustomAuthenticateView(FormView):
    """
    Custom MFA authenticate view with trusted device support.

    Extends allauth's AuthenticateView to add a "Remember this device"
    checkbox that creates a trusted device token when checked.
    """

    form_class = AuthenticateForm
    template_name = "mfa/authenticate." + account_settings.TEMPLATE_EXTENSION

    def dispatch(self, request, *args, **kwargs):
        self.stage = LoginStageController.enter(request, AuthenticateStage.key)
        if not self.stage or not is_mfa_enabled(self.stage.login.user, [Authenticator.Type.TOTP]):
            return HttpResponseRedirect(reverse("account_login"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if trusted devices are enabled
        try:
            settings = SiteSettings.get_settings()
            context["allow_trusted_devices"] = settings.allow_trusted_devices
            context["trusted_device_duration"] = settings.trusted_device_duration_days
        except Exception:
            context["allow_trusted_devices"] = False
            context["trusted_device_duration"] = 30
        return context

    def get_form_kwargs(self):
        ret = super().get_form_kwargs()
        ret["user"] = self.stage.login.user
        return ret

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "authenticate", self.form_class)

    def form_valid(self, form):
        # Save the form (performs allauth MFA authentication)
        form.save()

        # Check if "remember this device" was checked
        remember_device = self.request.POST.get("remember_device") == "on"

        if remember_device:
            try:
                settings = SiteSettings.get_settings()
                if settings.allow_trusted_devices:
                    # Create trusted device token
                    token, device = TrustedDevice.create_trusted_device(
                        user=self.stage.login.user,
                        request=self.request,
                        duration_days=settings.trusted_device_duration_days,
                    )

                    # Store token in session to set cookie after login completes
                    self.request.session["_trusted_device_token"] = token
            except Exception:
                # Don't fail the login if trusted device creation fails
                pass

        # Exit the stage (completes login)
        response = self.stage.exit()

        # If we have a pending trusted device token, set the cookie
        token = self.request.session.pop("_trusted_device_token", None)
        if token:
            try:
                settings = SiteSettings.get_settings()
                max_age = settings.trusted_device_duration_days * 24 * 60 * 60
                response.set_cookie(
                    "trusted_device_token",
                    token,
                    max_age=max_age,
                    httponly=True,
                    secure=self.request.is_secure(),
                    samesite="Lax",
                )
            except Exception:
                pass

        return response


authenticate = CustomAuthenticateView.as_view()
