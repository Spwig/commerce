import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger(__name__)

# Reuse the session key from MFA enforcement middleware
MFA_VERIFIED_SESSION_KEY = "mfa_verified_at"


@receiver(user_logged_in)
def bypass_mfa_for_sso(sender, request, user, **kwargs):
    """
    Automatically mark MFA as verified when a user signs in via OIDC SSO.

    Enterprise identity providers enforce their own MFA policies (Azure AD
    Conditional Access, Google 2-Step Verification, etc.), so re-challenging
    with Spwig's TOTP would be redundant and disruptive.
    """
    backend = getattr(user, "backend", "")
    if "SpwigOIDCBackend" not in backend:
        return

    if not user.is_staff:
        return

    request.session[MFA_VERIFIED_SESSION_KEY] = timezone.now().isoformat()
    request.session.modified = True
    logger.info("SSO login: MFA verification bypassed for staff user %s", user.email)
