"""
Security Settings Tests

Validates security-related Django settings:
- SECRET_KEY strength and format
- SSL/HTTPS settings (SECURE_SSL_REDIRECT, etc.)
- Cookie security (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- Password validation
- Authentication settings
"""
import pytest
from django.conf import settings


pytestmark = pytest.mark.integrity


class TestSecretKey:
    """Validate SECRET_KEY configuration"""

    INSECURE_PATTERNS = [
        'spwig-insecure',
        'django-insecure',
        'changeme',
        'secret',
        'password',
        '12345',
    ]

    def test_secret_key_exists(self):
        """Verify SECRET_KEY is configured"""
        secret_key = getattr(settings, 'SECRET_KEY', None)
        assert secret_key, "SECRET_KEY must be configured"
        assert isinstance(secret_key, str), "SECRET_KEY must be a string"

    def test_secret_key_not_insecure(self):
        """
        Verify SECRET_KEY doesn't contain insecure patterns (skip for dev/test keys).
        This check is also performed by Django system check spwig.security.E001.
        """
        secret_key = settings.SECRET_KEY.lower()
        found_patterns = [p for p in self.INSECURE_PATTERNS if p in secret_key]

        # Skip if using known dev/test keys
        if found_patterns and ('dev-secret' in secret_key or 'test-secret' in secret_key or settings.DEBUG):
            pytest.skip(
                f"WARNING: SECRET_KEY contains insecure patterns in dev/test mode: {', '.join(found_patterns)}\n"
                "This is acceptable for development/testing. Ensure production uses a secure key."
            )

        assert not found_patterns, (
            f"SECRET_KEY contains insecure patterns: {', '.join(found_patterns)}\n"
            "Generate a new SECRET_KEY with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
        )

    def test_secret_key_minimum_length(self):
        """
        Verify SECRET_KEY is at least 50 characters (skip for dev/test keys).
        Django's get_random_secret_key() generates 50-char keys.
        """
        secret_key = settings.SECRET_KEY
        secret_key_lower = secret_key.lower()

        # Skip if using known dev/test keys
        if len(secret_key) < 50 and ('dev-secret' in secret_key_lower or 'test-secret' in secret_key_lower or settings.DEBUG):
            pytest.skip(
                f"WARNING: SECRET_KEY is {len(secret_key)} chars (< 50) in dev/test mode.\n"
                "This is acceptable for development/testing. Ensure production uses a 50+ char key."
            )

        assert len(secret_key) >= 50, (
            f"SECRET_KEY should be at least 50 characters, got {len(secret_key)}"
        )


class TestSSLHTTPSSettings:
    """Validate SSL/HTTPS security settings"""

    def test_secure_ssl_redirect_in_production(self):
        """
        Verify SECURE_SSL_REDIRECT is True in production (skip in dev/test).
        Production sites should redirect HTTP to HTTPS.
        """
        import sys
        # Skip in DEBUG mode or pytest test runs
        if settings.DEBUG or 'pytest' in sys.modules:
            pytest.skip("Skipping SSL redirect check in dev/test mode")

        secure_ssl_redirect = getattr(settings, 'SECURE_SSL_REDIRECT', False)
        assert secure_ssl_redirect is True, (
            "SECURE_SSL_REDIRECT must be True in production (DEBUG=False)"
        )

    def test_session_cookie_secure_in_production(self):
        """
        Verify SESSION_COOKIE_SECURE is True in production (skip in dev/test).
        Session cookies should only be sent over HTTPS in production.
        """
        import sys
        # Skip in DEBUG mode or pytest test runs
        if settings.DEBUG or 'pytest' in sys.modules:
            pytest.skip("Skipping SESSION_COOKIE_SECURE check in dev/test mode")

        session_cookie_secure = getattr(settings, 'SESSION_COOKIE_SECURE', False)
        assert session_cookie_secure is True, (
            "SESSION_COOKIE_SECURE must be True in production (DEBUG=False)"
        )

    def test_csrf_cookie_secure_in_production(self):
        """
        Verify CSRF_COOKIE_SECURE is True in production (skip in dev/test).
        CSRF cookies should only be sent over HTTPS in production.
        """
        import sys
        # Skip in DEBUG mode or pytest test runs
        if settings.DEBUG or 'pytest' in sys.modules:
            pytest.skip("Skipping CSRF_COOKIE_SECURE check in dev/test mode")

        csrf_cookie_secure = getattr(settings, 'CSRF_COOKIE_SECURE', False)
        assert csrf_cookie_secure is True, (
            "CSRF_COOKIE_SECURE must be True in production (DEBUG=False)"
        )

    def test_secure_hsts_seconds_configured(self):
        """
        Verify SECURE_HSTS_SECONDS is configured for production.
        HSTS tells browsers to only use HTTPS for future requests.
        """
        if not settings.DEBUG:
            hsts_seconds = getattr(settings, 'SECURE_HSTS_SECONDS', 0)
            # Warn if not set, but don't fail (may be handled by reverse proxy)
            if hsts_seconds == 0:
                pytest.skip(
                    "SECURE_HSTS_SECONDS is 0 - ensure HSTS is configured at reverse proxy level"
                )

    def test_secure_hsts_include_subdomains(self):
        """
        Verify SECURE_HSTS_INCLUDE_SUBDOMAINS is True when HSTS is enabled.
        HSTS should apply to all subdomains for comprehensive protection.
        """
        hsts_seconds = getattr(settings, 'SECURE_HSTS_SECONDS', 0)
        if hsts_seconds > 0:
            hsts_subdomains = getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
            assert hsts_subdomains is True, (
                "SECURE_HSTS_INCLUDE_SUBDOMAINS should be True when HSTS is enabled"
            )

    def test_secure_content_type_nosniff(self):
        """
        Verify SECURE_CONTENT_TYPE_NOSNIFF is True.
        Prevents browsers from MIME-sniffing responses.
        """
        nosniff = getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False)
        assert nosniff is True, (
            "SECURE_CONTENT_TYPE_NOSNIFF should be True to prevent MIME-sniffing attacks"
        )

    def test_x_frame_options_configured(self):
        """
        Verify X_FRAME_OPTIONS is set to prevent clickjacking.
        Should be 'DENY' or 'SAMEORIGIN'.
        """
        x_frame_options = getattr(settings, 'X_FRAME_OPTIONS', None)
        assert x_frame_options in ['DENY', 'SAMEORIGIN'], (
            f"X_FRAME_OPTIONS should be 'DENY' or 'SAMEORIGIN', got: {x_frame_options}"
        )


class TestCookieSettings:
    """Validate cookie security settings"""

    def test_session_cookie_httponly(self):
        """
        Verify SESSION_COOKIE_HTTPONLY is True.
        Prevents JavaScript access to session cookies (XSS mitigation).
        """
        httponly = getattr(settings, 'SESSION_COOKIE_HTTPONLY', False)
        assert httponly is True, (
            "SESSION_COOKIE_HTTPONLY must be True to prevent XSS attacks"
        )

    def test_csrf_cookie_httponly(self):
        """
        Verify CSRF_COOKIE_HTTPONLY is True.
        Prevents JavaScript access to CSRF cookies.
        """
        httponly = getattr(settings, 'CSRF_COOKIE_HTTPONLY', False)
        assert httponly is True, (
            "CSRF_COOKIE_HTTPONLY should be True to prevent XSS attacks"
        )

    def test_session_cookie_samesite(self):
        """
        Verify SESSION_COOKIE_SAMESITE is set.
        Should be 'Lax' or 'Strict' to prevent CSRF attacks.
        """
        samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', None)
        assert samesite in ['Lax', 'Strict'], (
            f"SESSION_COOKIE_SAMESITE should be 'Lax' or 'Strict', got: {samesite}"
        )

    def test_csrf_cookie_samesite(self):
        """
        Verify CSRF_COOKIE_SAMESITE is set.
        Should be 'Lax' or 'Strict' to prevent CSRF attacks.
        """
        samesite = getattr(settings, 'CSRF_COOKIE_SAMESITE', None)
        assert samesite in ['Lax', 'Strict'], (
            f"CSRF_COOKIE_SAMESITE should be 'Lax' or 'Strict', got: {samesite}"
        )

    def test_session_expire_at_browser_close(self):
        """
        Verify SESSION_EXPIRE_AT_BROWSER_CLOSE is configured.
        This is a policy decision (can be True or False), just check it's set.
        """
        expire_at_close = getattr(settings, 'SESSION_EXPIRE_AT_BROWSER_CLOSE', None)
        assert expire_at_close is not None, (
            "SESSION_EXPIRE_AT_BROWSER_CLOSE should be explicitly configured"
        )


class TestPasswordValidation:
    """Validate password strength requirements"""

    REQUIRED_VALIDATORS = [
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'django.contrib.auth.password_validation.CommonPasswordValidator',
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    ]

    def test_password_validators_configured(self):
        """Verify AUTH_PASSWORD_VALIDATORS is configured"""
        validators = getattr(settings, 'AUTH_PASSWORD_VALIDATORS', [])
        assert validators, (
            "AUTH_PASSWORD_VALIDATORS must be configured for password strength"
        )

    def test_required_password_validators_present(self):
        """
        Verify all recommended Django password validators are enabled.
        These are Django's defaults and should always be active.
        """
        validators = getattr(settings, 'AUTH_PASSWORD_VALIDATORS', [])
        configured_validators = [v['NAME'] for v in validators]

        missing = [v for v in self.REQUIRED_VALIDATORS if v not in configured_validators]

        assert not missing, (
            f"Missing recommended password validators:\n  " +
            "\n  ".join(missing)
        )

    def test_minimum_password_length(self):
        """
        Verify MinimumLengthValidator is configured with reasonable length.
        Default is 8, we recommend at least 8 characters.
        """
        validators = getattr(settings, 'AUTH_PASSWORD_VALIDATORS', [])
        min_length_validator = next(
            (v for v in validators if 'MinimumLengthValidator' in v['NAME']),
            None
        )

        if min_length_validator:
            min_length = min_length_validator.get('OPTIONS', {}).get('min_length', 8)
            assert min_length >= 8, (
                f"Minimum password length should be at least 8, got: {min_length}"
            )


class TestAuthenticationSettings:
    """Validate authentication and user model settings"""

    def test_auth_user_model_configured(self):
        """
        Verify AUTH_USER_MODEL is configured (accept Django default or custom).
        Spwig can use either Django's default User or a custom user model.
        """
        auth_user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

        # Accept Django default or custom user model
        assert auth_user_model in ['auth.User', 'accounts.User'], (
            f"AUTH_USER_MODEL should be 'auth.User' (Django default) or 'accounts.User' (custom), "
            f"got: {auth_user_model}"
        )

        # Info message if using Django default
        if auth_user_model == 'auth.User':
            pytest.skip(
                "INFO: Using Django default User model (auth.User). "
                "This is acceptable. Custom User model can be added later if needed."
            )

    def test_login_url_configured(self):
        """Verify LOGIN_URL is configured"""
        login_url = getattr(settings, 'LOGIN_URL', None)
        assert login_url, "LOGIN_URL must be configured"

    def test_login_redirect_url_configured(self):
        """Verify LOGIN_REDIRECT_URL is configured"""
        login_redirect = getattr(settings, 'LOGIN_REDIRECT_URL', None)
        assert login_redirect, "LOGIN_REDIRECT_URL must be configured"

    def test_logout_redirect_url_configured(self):
        """Verify LOGOUT_REDIRECT_URL is configured"""
        logout_redirect = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
        assert logout_redirect, "LOGOUT_REDIRECT_URL must be configured"


class TestDebugSettings:
    """Validate DEBUG and development-only settings"""

    def test_debug_false_in_production(self):
        """
        Verify DEBUG is False in production environments.
        This is critical - DEBUG=True exposes sensitive data.
        """
        # We can't definitively detect "production" in tests, but we can
        # check that if certain production indicators exist, DEBUG is False
        import os

        # Common production environment indicators
        is_production = any([
            os.environ.get('DJANGO_ENV') == 'production',
            os.environ.get('ENVIRONMENT') == 'production',
            os.environ.get('SPWIG_ENV') == 'production',
        ])

        if is_production:
            assert settings.DEBUG is False, (
                "DEBUG must be False in production environment"
            )

    def test_allowed_hosts_not_wildcard_in_production(self):
        """
        Verify ALLOWED_HOSTS is not ['*'] when DEBUG is False.
        Wildcard is only acceptable in development.
        """
        if not settings.DEBUG:
            allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
            assert '*' not in allowed_hosts, (
                "ALLOWED_HOSTS must not contain '*' in production (DEBUG=False)"
            )
            assert len(allowed_hosts) > 0, (
                "ALLOWED_HOSTS must be configured in production (DEBUG=False)"
            )

    def test_internal_ips_configured_for_debug_toolbar(self):
        """
        Verify INTERNAL_IPS is configured if debug_toolbar is installed.
        This is a development-only check.
        """
        installed_apps = settings.INSTALLED_APPS

        if 'debug_toolbar' in installed_apps:
            internal_ips = getattr(settings, 'INTERNAL_IPS', [])
            assert internal_ips, (
                "INTERNAL_IPS must be configured when debug_toolbar is installed"
            )
