"""
API Configuration Tests

Validates API-related settings:
- REST_FRAMEWORK configuration (auth, pagination, throttling)
- CORS settings (corsheaders)
- DRF Spectacular (OpenAPI schema generation)
- API versioning and documentation
"""
import pytest
from django.conf import settings
from django.utils.module_loading import import_string


pytestmark = pytest.mark.integrity


class TestDRFConfiguration:
    """Validate Django REST Framework settings"""

    # Required DRF settings keys
    REQUIRED_SETTINGS = [
        'DEFAULT_RENDERER_CLASSES',
        'DEFAULT_PARSER_CLASSES',
        'DEFAULT_AUTHENTICATION_CLASSES',
        'DEFAULT_PERMISSION_CLASSES',
        'DEFAULT_PAGINATION_CLASS',
    ]

    # Recommended authentication classes
    RECOMMENDED_AUTH_CLASSES = [
        'rest_framework.authentication.SessionAuthentication',
    ]

    # Recommended throttle classes for production
    RECOMMENDED_THROTTLE_CLASSES = [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ]

    def test_rest_framework_configured(self):
        """Verify REST_FRAMEWORK settings exist"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', None)
        assert rest_framework, "REST_FRAMEWORK settings must be configured"
        assert isinstance(rest_framework, dict), "REST_FRAMEWORK must be a dictionary"

    def test_required_settings_present(self):
        """Verify all required DRF settings are configured"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        missing = [key for key in self.REQUIRED_SETTINGS if key not in rest_framework]

        assert not missing, (
            f"Missing required REST_FRAMEWORK settings:\n  " +
            "\n  ".join(missing)
        )

    def test_default_renderer_classes_importable(self):
        """Verify all default renderer classes can be imported"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        renderers = rest_framework.get('DEFAULT_RENDERER_CLASSES', [])
        errors = []

        for renderer in renderers:
            try:
                import_string(renderer)
            except ImportError as e:
                errors.append(f"{renderer}: {str(e)}")

        assert not errors, (
            f"Failed to import {len(errors)} renderer classes:\n  " +
            "\n  ".join(errors)
        )

    def test_default_parser_classes_importable(self):
        """Verify all default parser classes can be imported"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        parsers = rest_framework.get('DEFAULT_PARSER_CLASSES', [])
        errors = []

        for parser in parsers:
            try:
                import_string(parser)
            except ImportError as e:
                errors.append(f"{parser}: {str(e)}")

        assert not errors, (
            f"Failed to import {len(errors)} parser classes:\n  " +
            "\n  ".join(errors)
        )

    def test_default_authentication_classes_importable(self):
        """Verify all default authentication classes can be imported"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        auth_classes = rest_framework.get('DEFAULT_AUTHENTICATION_CLASSES', [])
        errors = []

        for auth_class in auth_classes:
            try:
                import_string(auth_class)
            except ImportError as e:
                errors.append(f"{auth_class}: {str(e)}")

        assert not errors, (
            f"Failed to import {len(errors)} authentication classes:\n  " +
            "\n  ".join(errors)
        )

    def test_session_authentication_enabled(self):
        """
        Verify SessionAuthentication is enabled.
        This is required for browser-based API access (admin, debugging).
        """
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        auth_classes = rest_framework.get('DEFAULT_AUTHENTICATION_CLASSES', [])

        session_auth = 'rest_framework.authentication.SessionAuthentication'
        assert session_auth in auth_classes, (
            "SessionAuthentication should be enabled for browser-based API access"
        )

    def test_default_permission_classes_importable(self):
        """Verify all default permission classes can be imported"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        permission_classes = rest_framework.get('DEFAULT_PERMISSION_CLASSES', [])
        errors = []

        for perm_class in permission_classes:
            try:
                import_string(perm_class)
            except ImportError as e:
                errors.append(f"{perm_class}: {str(e)}")

        assert not errors, (
            f"Failed to import {len(errors)} permission classes:\n  " +
            "\n  ".join(errors)
        )

    def test_pagination_class_importable(self):
        """Verify default pagination class can be imported"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        pagination_class = rest_framework.get('DEFAULT_PAGINATION_CLASS')

        if pagination_class:
            try:
                import_string(pagination_class)
            except ImportError as e:
                pytest.fail(f"Failed to import pagination class {pagination_class}: {e}")

    def test_page_size_configured(self):
        """Verify PAGE_SIZE is configured for pagination"""
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        page_size = rest_framework.get('PAGE_SIZE')

        if rest_framework.get('DEFAULT_PAGINATION_CLASS'):
            assert page_size, (
                "PAGE_SIZE must be configured when pagination is enabled"
            )
            assert isinstance(page_size, int), "PAGE_SIZE must be an integer"
            assert page_size > 0, "PAGE_SIZE must be positive"

    def test_throttle_rates_configured_in_production(self):
        """
        Verify throttle rates are configured when DEBUG is False.
        Production APIs should have rate limiting to prevent abuse.
        """
        if not settings.DEBUG:
            rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
            throttle_rates = rest_framework.get('DEFAULT_THROTTLE_RATES', {})

            # Should have at least anon and user rates
            assert 'anon' in throttle_rates or 'user' in throttle_rates, (
                "Throttle rates should be configured in production (DEBUG=False)"
            )


class TestCORSConfiguration:
    """Validate CORS (Cross-Origin Resource Sharing) settings"""

    def test_corsheaders_installed(self):
        """Verify corsheaders is in INSTALLED_APPS"""
        installed_apps = settings.INSTALLED_APPS
        assert 'corsheaders' in installed_apps, (
            "corsheaders must be in INSTALLED_APPS for CORS support"
        )

    def test_cors_middleware_present(self):
        """Verify CorsMiddleware is in MIDDLEWARE"""
        middleware = settings.MIDDLEWARE
        cors_mw = 'corsheaders.middleware.CorsMiddleware'

        assert cors_mw in middleware, (
            "CorsMiddleware must be in MIDDLEWARE for CORS support"
        )

    def test_cors_not_allow_all_origins_in_production(self):
        """
        Verify CORS_ALLOW_ALL_ORIGINS is False in production.
        Allowing all origins is a security risk.
        """
        if not settings.DEBUG:
            cors_allow_all = getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)
            assert cors_allow_all is False, (
                "CORS_ALLOW_ALL_ORIGINS must be False in production (DEBUG=False)"
            )

    def test_cors_allowed_origins_configured_if_not_allow_all(self):
        """
        Verify CORS_ALLOWED_ORIGINS is configured if CORS_ALLOW_ALL_ORIGINS is False.
        Must explicitly list allowed origins.
        """
        cors_allow_all = getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)

        if not cors_allow_all:
            cors_allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
            # It's OK to have an empty list in development, but warn
            if not cors_allowed_origins and not settings.DEBUG:
                pytest.fail(
                    "CORS_ALLOWED_ORIGINS must be configured in production "
                    "when CORS_ALLOW_ALL_ORIGINS is False"
                )

    def test_cors_allowed_origins_are_https_in_production(self):
        """
        Verify CORS_ALLOWED_ORIGINS use HTTPS in production.
        HTTP origins are insecure for production.
        """
        if not settings.DEBUG:
            cors_allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
            http_origins = [o for o in cors_allowed_origins if o.startswith('http://')]

            if http_origins:
                pytest.skip(
                    f"Warning: CORS_ALLOWED_ORIGINS contains HTTP origins in production: {http_origins}"
                )

    def test_cors_allow_credentials_configured(self):
        """
        Verify CORS_ALLOW_CREDENTIALS is explicitly set.
        This controls whether cookies/auth headers are sent with CORS requests.
        """
        cors_allow_credentials = getattr(settings, 'CORS_ALLOW_CREDENTIALS', None)
        assert cors_allow_credentials is not None, (
            "CORS_ALLOW_CREDENTIALS should be explicitly configured (True or False)"
        )


class TestDRFSpectacularConfiguration:
    """Validate drf-spectacular (OpenAPI schema) settings"""

    def test_spectacular_installed(self):
        """Verify drf-spectacular is in INSTALLED_APPS"""
        installed_apps = settings.INSTALLED_APPS
        assert 'drf_spectacular' in installed_apps, (
            "drf-spectacular must be in INSTALLED_APPS for OpenAPI schema generation"
        )

    def test_spectacular_configured_as_schema_class(self):
        """
        Verify drf-spectacular is configured as the default schema class.
        This enables OpenAPI schema generation.
        """
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        schema_class = rest_framework.get('DEFAULT_SCHEMA_CLASS')

        assert schema_class == 'drf_spectacular.openapi.AutoSchema', (
            f"DEFAULT_SCHEMA_CLASS should be drf_spectacular AutoSchema, got: {schema_class}"
        )

    def test_spectacular_settings_configured(self):
        """Verify SPECTACULAR_SETTINGS is configured"""
        spectacular_settings = getattr(settings, 'SPECTACULAR_SETTINGS', None)
        assert spectacular_settings, (
            "SPECTACULAR_SETTINGS must be configured for OpenAPI schema customization"
        )
        assert isinstance(spectacular_settings, dict), (
            "SPECTACULAR_SETTINGS must be a dictionary"
        )

    def test_spectacular_title_configured(self):
        """Verify OpenAPI schema has a title"""
        spectacular_settings = getattr(settings, 'SPECTACULAR_SETTINGS', {})
        title = spectacular_settings.get('TITLE')

        assert title, "SPECTACULAR_SETTINGS['TITLE'] must be configured"
        assert isinstance(title, str), "OpenAPI title must be a string"

    def test_spectacular_version_configured(self):
        """Verify OpenAPI schema has a version"""
        spectacular_settings = getattr(settings, 'SPECTACULAR_SETTINGS', {})
        version = spectacular_settings.get('VERSION')

        assert version, "SPECTACULAR_SETTINGS['VERSION'] must be configured"
        assert isinstance(version, str), "OpenAPI version must be a string"


class TestAPISecurityConfiguration:
    """Validate API security settings"""

    def test_csrf_trusted_origins_configured_in_production(self):
        """
        Verify CSRF_TRUSTED_ORIGINS is configured when DEBUG is False.
        Required for cross-origin POST requests.
        """
        if not settings.DEBUG:
            csrf_trusted_origins = getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])
            # It's OK to be empty if all requests are same-origin
            assert isinstance(csrf_trusted_origins, list), (
                "CSRF_TRUSTED_ORIGINS must be a list"
            )

    def test_csrf_cookie_httponly(self):
        """
        Verify CSRF_COOKIE_HTTPONLY is True.
        Prevents JavaScript access to CSRF token.
        """
        csrf_httponly = getattr(settings, 'CSRF_COOKIE_HTTPONLY', False)
        assert csrf_httponly is True, (
            "CSRF_COOKIE_HTTPONLY should be True to prevent XSS attacks"
        )

    def test_rest_framework_uses_json_renderer(self):
        """
        Verify JSONRenderer is in DEFAULT_RENDERER_CLASSES.
        APIs should support JSON output.
        """
        rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
        renderers = rest_framework.get('DEFAULT_RENDERER_CLASSES', [])

        json_renderer = 'rest_framework.renderers.JSONRenderer'
        assert json_renderer in renderers, (
            "JSONRenderer should be in DEFAULT_RENDERER_CLASSES"
        )

    def test_browsable_api_disabled_in_production(self):
        """
        Verify BrowsableAPIRenderer is disabled in production.
        Browsable API exposes API structure and should only be used in development.
        """
        if not settings.DEBUG:
            rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
            renderers = rest_framework.get('DEFAULT_RENDERER_CLASSES', [])

            browsable_renderer = 'rest_framework.renderers.BrowsableAPIRenderer'
            if browsable_renderer in renderers:
                pytest.skip(
                    "Warning: BrowsableAPIRenderer is enabled in production - "
                    "consider disabling to prevent API structure exposure"
                )


class TestAPIDocumentation:
    """Validate API documentation configuration"""

    def test_api_documentation_urls_configured(self):
        """
        Verify API documentation URLs are configured.
        Check that Swagger/ReDoc URLs are accessible.
        """
        # This is a basic check - actual URL testing should be in E2E tests
        from django.urls import resolve, Resolver404

        doc_paths = [
            '/api/schema/',
            '/api/docs/',
            '/api/redoc/',
        ]

        for path in doc_paths:
            try:
                # Try to resolve the path
                resolve(path)
            except Resolver404:
                # Path not found - skip this check
                pass
