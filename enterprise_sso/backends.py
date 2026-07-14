import logging

from django.contrib.auth.backends import ModelBackend
from mozilla_django_oidc.utils import import_from_settings

logger = logging.getLogger(__name__)


def _get_db_setting(attr, *args):
    """Read OIDC settings from the database SSOProviderConfig singleton."""
    from .models import SSOProviderConfig

    config = SSOProviderConfig.get_config()
    db_map = {
        "OIDC_RP_CLIENT_ID": config.oidc_client_id,
        "OIDC_RP_CLIENT_SECRET": config.get_client_secret(),
        "OIDC_OP_AUTHORIZATION_ENDPOINT": config.oidc_authorization_endpoint,
        "OIDC_OP_TOKEN_ENDPOINT": config.oidc_token_endpoint,
        "OIDC_OP_USER_ENDPOINT": config.oidc_userinfo_endpoint,
        "OIDC_OP_JWKS_ENDPOINT": config.oidc_jwks_endpoint or None,
        "OIDC_RP_SIGN_ALGO": "RS256",
        "OIDC_RP_SCOPES": config.oidc_scopes or "openid email profile",
        "OIDC_CREATE_USER": config.auto_create_users,
    }
    if attr in db_map:
        return db_map[attr]
    # Fall back to Django settings for anything not in our DB map
    return import_from_settings(attr, *args)


def _is_sso_configured():
    """Check if SSO is configured and enabled."""
    try:
        from core.models import SiteSettings

        from .models import SSOProviderConfig

        settings = SiteSettings.get_settings()
        if not settings.admin_sso_enabled:
            return False
        config = SSOProviderConfig.get_config()
        return config.is_configured
    except Exception:
        return False


class SpwigOIDCBackend(ModelBackend):
    """
    OIDC authentication backend that reads configuration from the database.

    Extends ModelBackend (not OIDCAuthenticationBackend) to avoid the parent's
    __init__ raising ImproperlyConfigured when SSO is not yet configured.
    Delegates actual OIDC authentication to mozilla-django-oidc internals.
    """

    def authenticate(self, request, **kwargs):
        """Authenticate via OIDC code flow, only if SSO is configured."""
        if not request:
            return None

        # Only handle OIDC callback requests (have code + state params)
        code = request.GET.get("code")
        state = request.GET.get("state")
        if not code or not state:
            return None

        if not _is_sso_configured():
            return None

        # Dynamically import and use the OIDC backend for actual auth
        from mozilla_django_oidc.auth import OIDCAuthenticationBackend

        class _DynamicOIDCBackend(OIDCAuthenticationBackend):
            @staticmethod
            def get_settings(attr, *args):
                return _get_db_setting(attr, *args)

            def filter_users_by_claims(self, claims):
                from .models import SSOProviderConfig

                config = SSOProviderConfig.get_config()
                email = claims.get(config.claim_email, "")
                if not email:
                    return self.UserModel.objects.none()
                return self.UserModel.objects.filter(email__iexact=email)

            def verify_claims(self, claims):
                from .models import SSOProviderConfig

                config = SSOProviderConfig.get_config()
                return bool(claims.get(config.claim_email))

            def create_user(self, claims):
                from .models import SSOProviderConfig

                config = SSOProviderConfig.get_config()
                if not config.auto_create_users:
                    logger.info(
                        "SSO login denied: auto_create_users is disabled and no matching user found"
                    )
                    return None

                email = claims.get(config.claim_email, "")
                first_name = claims.get(config.claim_first_name, "")
                last_name = claims.get(config.claim_last_name, "")
                username = self.get_username(claims)

                user = self.UserModel.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                logger.info("SSO auto-created user: %s (%s)", username, email)
                _apply_role_mapping(user, claims, config)
                return user

            def update_user(self, user, claims):
                from .models import SSOProviderConfig

                config = SSOProviderConfig.get_config()
                changed = False

                first_name = claims.get(config.claim_first_name, "")
                last_name = claims.get(config.claim_last_name, "")
                if first_name and user.first_name != first_name:
                    user.first_name = first_name
                    changed = True
                if last_name and user.last_name != last_name:
                    user.last_name = last_name
                    changed = True

                if _apply_role_mapping(user, claims, config):
                    changed = True

                if changed:
                    user.save()

                if config.restrict_to_staff and not user.is_staff:
                    logger.warning(
                        "SSO login denied: user %s is not staff (restrict_to_staff=True)",
                        user.email,
                    )
                    return None

                return user

        try:
            backend = _DynamicOIDCBackend()
            nonce = kwargs.pop("nonce", None)
            code_verifier = kwargs.pop("code_verifier", None)
            user = backend.authenticate(request, nonce=nonce, code_verifier=code_verifier)
            if user:
                # Set the backend path so Django knows which backend authenticated
                user.backend = "enterprise_sso.backends.SpwigOIDCBackend"
            return user
        except Exception:
            logger.exception("OIDC authentication failed")
            return None


def _apply_role_mapping(user, claims, config):
    """Map IdP group claims to Django staff/superuser status."""
    if not config.claim_groups:
        return False

    user_groups = claims.get(config.claim_groups, [])
    if isinstance(user_groups, str):
        user_groups = [user_groups]

    changed = False

    staff_groups = {g.strip() for g in config.staff_groups.split(",") if g.strip()}
    superuser_groups = {g.strip() for g in config.superuser_groups.split(",") if g.strip()}

    if staff_groups:
        should_be_staff = bool(set(user_groups) & staff_groups)
        if user.is_staff != should_be_staff:
            user.is_staff = should_be_staff
            changed = True
            logger.info("SSO role mapping: user %s is_staff=%s", user.email, should_be_staff)

    if superuser_groups:
        should_be_superuser = bool(set(user_groups) & superuser_groups)
        if user.is_superuser != should_be_superuser:
            user.is_superuser = should_be_superuser
            changed = True
            logger.info(
                "SSO role mapping: user %s is_superuser=%s", user.email, should_be_superuser
            )

    return changed
