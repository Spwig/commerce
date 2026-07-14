"""
Settings Integrity Tests

Validates Django settings configuration for:
- INSTALLED_APPS (all importable, required apps present, no duplicates)
- MIDDLEWARE (all importable, correct order, no duplicates)
- Critical Django settings (TIME_ZONE, LANGUAGE_CODE, etc.)
"""

import pytest
from django.conf import settings
from django.utils.module_loading import import_string

pytestmark = pytest.mark.integrity


class TestInstalledApps:
    """Validate INSTALLED_APPS configuration"""

    # Required Django apps
    REQUIRED_DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        # Note: sitemaps not currently used
    ]

    # Required third-party apps
    REQUIRED_THIRD_PARTY_APPS = [
        "rest_framework",
        "corsheaders",
        "django_filters",
        "drf_spectacular",
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
    ]

    # Required Spwig apps (core business logic)
    REQUIRED_SPWIG_APPS = [
        "core",
        "accounts",
        "catalog",
        "cart",
        "orders",
        "design",
        "page_builder",
        "email_system",
        "component_updates",
        "media_library",
    ]

    def test_all_installed_apps_are_importable(self):
        """
        Verify all apps in INSTALLED_APPS can be imported.
        Catches typos or missing dependencies.
        """
        import importlib

        installed_apps = settings.INSTALLED_APPS
        errors = []

        for app in installed_apps:
            # Skip loading apps that have explicit AppConfig (e.g., 'page_builder.apps.PageBuilderConfig')
            if ".apps." in app and app.endswith("Config"):
                try:
                    import_string(app)
                    continue
                except ImportError as e:
                    errors.append(f"{app}: {str(e)}")
                    continue

            # For simple app names (like 'daphne', 'rest_framework'), use importlib
            try:
                # For dotted paths without '.apps.', use import_string
                if "." in app:
                    import_string(app)
                else:
                    # For simple package names, use importlib
                    importlib.import_module(app)
            except ImportError as e:
                errors.append(f"{app}: {str(e)}")

        assert not errors, f"Failed to import {len(errors)} apps:\n  " + "\n  ".join(errors)

    def test_required_django_apps_present(self):
        """Verify all required Django apps are installed"""
        installed_apps = settings.INSTALLED_APPS
        missing = [app for app in self.REQUIRED_DJANGO_APPS if app not in installed_apps]

        assert not missing, "Missing required Django apps:\n  " + "\n  ".join(missing)

    def test_required_third_party_apps_present(self):
        """Verify all required third-party apps are installed"""
        installed_apps = settings.INSTALLED_APPS
        missing = [app for app in self.REQUIRED_THIRD_PARTY_APPS if app not in installed_apps]

        assert not missing, "Missing required third-party apps:\n  " + "\n  ".join(missing)

    def test_required_spwig_apps_present(self):
        """Verify all core Spwig apps are installed"""
        installed_apps = settings.INSTALLED_APPS

        # Normalize app names (strip .apps.ConfigName suffixes)
        normalized_apps = []
        for app in installed_apps:
            if ".apps." in app and app.endswith("Config"):
                # Extract base app name from 'page_builder.apps.PageBuilderConfig'
                base_app = app.split(".apps.")[0]
                normalized_apps.append(base_app)
            else:
                normalized_apps.append(app)

        missing = [app for app in self.REQUIRED_SPWIG_APPS if app not in normalized_apps]

        assert not missing, "Missing required Spwig apps:\n  " + "\n  ".join(missing)

    def test_no_duplicate_apps(self):
        """Verify no apps are listed multiple times"""
        installed_apps = list(settings.INSTALLED_APPS)
        duplicates = [app for app in installed_apps if installed_apps.count(app) > 1]
        unique_duplicates = list(set(duplicates))

        assert not unique_duplicates, "Duplicate apps in INSTALLED_APPS:\n  " + "\n  ".join(
            unique_duplicates
        )

    def test_app_order_django_first(self):
        """
        Verify Django apps come before third-party/custom apps (allow daphne exception).
        This ensures Django's templates and static files have correct precedence.
        Exception: daphne must be first for ASGI support.
        """
        installed_apps = list(settings.INSTALLED_APPS)

        # Allow daphne as first app (ASGI requirement)
        if installed_apps and installed_apps[0] == "daphne":
            installed_apps = installed_apps[1:]

        # Allow modeltranslation early (must be before django.contrib.admin)
        if "modeltranslation" in installed_apps[:5]:
            installed_apps = [a for a in installed_apps if a != "modeltranslation"]

        # Find positions
        django_apps_end = -1
        for i, app in enumerate(installed_apps):
            if app.startswith("django.contrib."):
                django_apps_end = i

        # Find first third-party or custom app
        first_custom_app = -1
        for i, app in enumerate(installed_apps):
            if not app.startswith("django.contrib."):
                first_custom_app = i
                break

        # Django apps should be contiguous after exceptions
        if django_apps_end >= 0 and first_custom_app >= 0:
            assert first_custom_app > django_apps_end, (
                "Django apps should be listed before third-party/custom apps "
                "(after ASGI/modeltranslation exceptions). "
                f"Found custom app at index {first_custom_app}, "
                f"but Django app at index {django_apps_end}"
            )


class TestMiddleware:
    """Validate MIDDLEWARE configuration"""

    # Required middleware (must be present)
    REQUIRED_MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # Middleware that must come first/early
    EARLY_MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "corsheaders.middleware.CorsMiddleware",
    ]

    # Middleware that depends on sessions (must come after SessionMiddleware)
    SESSION_DEPENDENT_MIDDLEWARE = [
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "allauth.account.middleware.AccountMiddleware",
    ]

    def test_all_middleware_are_importable(self):
        """
        Verify all middleware classes can be imported.
        Catches typos or missing dependencies.
        """
        middleware = settings.MIDDLEWARE
        errors = []

        for mw in middleware:
            try:
                import_string(mw)
            except ImportError as e:
                errors.append(f"{mw}: {str(e)}")

        assert not errors, f"Failed to import {len(errors)} middleware:\n  " + "\n  ".join(errors)

    def test_required_middleware_present(self):
        """Verify all required middleware are installed"""
        middleware = settings.MIDDLEWARE
        missing = [mw for mw in self.REQUIRED_MIDDLEWARE if mw not in middleware]

        assert not missing, "Missing required middleware:\n  " + "\n  ".join(missing)

    def test_no_duplicate_middleware(self):
        """Verify no middleware are listed multiple times"""
        middleware = list(settings.MIDDLEWARE)
        duplicates = [mw for mw in middleware if middleware.count(mw) > 1]
        unique_duplicates = list(set(duplicates))

        assert not unique_duplicates, "Duplicate middleware in MIDDLEWARE:\n  " + "\n  ".join(
            unique_duplicates
        )

    def test_security_middleware_comes_first(self):
        """
        Verify SecurityMiddleware is first (or second after SubpathMiddleware).
        SubpathMiddleware must be first to handle URL subpath deployments.
        """
        middleware = list(settings.MIDDLEWARE)
        security_mw = "django.middleware.security.SecurityMiddleware"
        subpath_mw = "core.middleware.subpath.SubpathMiddleware"

        if security_mw in middleware:
            security_idx = middleware.index(security_mw)

            # Allow SubpathMiddleware to be first (handles URL subpath deployments)
            if middleware[0] == subpath_mw:
                assert security_idx == 1, (
                    f"SecurityMiddleware should be second (after SubpathMiddleware), "
                    f"but found at index {security_idx}"
                )
            else:
                assert security_idx == 0, (
                    f"SecurityMiddleware should be first, but found at index {security_idx}"
                )

    def test_session_middleware_before_auth(self):
        """
        Verify SessionMiddleware comes before AuthenticationMiddleware.
        Auth depends on sessions being available.
        """
        middleware = list(settings.MIDDLEWARE)
        session_mw = "django.contrib.sessions.middleware.SessionMiddleware"
        auth_mw = "django.contrib.auth.middleware.AuthenticationMiddleware"

        if session_mw in middleware and auth_mw in middleware:
            session_idx = middleware.index(session_mw)
            auth_idx = middleware.index(auth_mw)

            assert session_idx < auth_idx, (
                f"SessionMiddleware (index {session_idx}) must come before "
                f"AuthenticationMiddleware (index {auth_idx})"
            )

    def test_csrf_middleware_before_auth(self):
        """
        Verify CsrfViewMiddleware comes before AuthenticationMiddleware.
        CSRF protection should be applied before auth.
        """
        middleware = list(settings.MIDDLEWARE)
        csrf_mw = "django.middleware.csrf.CsrfViewMiddleware"
        auth_mw = "django.contrib.auth.middleware.AuthenticationMiddleware"

        if csrf_mw in middleware and auth_mw in middleware:
            csrf_idx = middleware.index(csrf_mw)
            auth_idx = middleware.index(auth_mw)

            assert csrf_idx < auth_idx, (
                f"CsrfViewMiddleware (index {csrf_idx}) must come before "
                f"AuthenticationMiddleware (index {auth_idx})"
            )

    def test_cors_middleware_comes_early(self):
        """
        Verify CorsMiddleware comes before CommonMiddleware.
        CORS headers should be added early.
        """
        middleware = list(settings.MIDDLEWARE)
        cors_mw = "corsheaders.middleware.CorsMiddleware"
        common_mw = "django.middleware.common.CommonMiddleware"

        if cors_mw in middleware and common_mw in middleware:
            cors_idx = middleware.index(cors_mw)
            common_idx = middleware.index(common_mw)

            assert cors_idx < common_idx, (
                f"CorsMiddleware (index {cors_idx}) should come before "
                f"CommonMiddleware (index {common_idx})"
            )


class TestCriticalSettings:
    """Validate critical Django settings"""

    def test_time_zone_configured(self):
        """Verify TIME_ZONE is set to a valid timezone"""
        time_zone = settings.TIME_ZONE
        assert time_zone, "TIME_ZONE must be configured"

        # Try to import pytz to validate timezone
        try:
            import pytz

            assert time_zone in pytz.all_timezones, f"Invalid TIME_ZONE: {time_zone}"
        except ImportError:
            # If pytz not available, just check it's not empty
            pass

    def test_language_code_configured(self):
        """Verify LANGUAGE_CODE is set"""
        language_code = settings.LANGUAGE_CODE
        assert language_code, "LANGUAGE_CODE must be configured"
        assert isinstance(language_code, str), "LANGUAGE_CODE must be a string"

    def test_use_i18n_enabled(self):
        """Verify USE_I18N is enabled for multi-language support"""
        assert settings.USE_I18N is True, "USE_I18N must be True for internationalization support"

    def test_use_tz_enabled(self):
        """Verify USE_TZ is enabled for timezone-aware datetimes"""
        assert settings.USE_TZ is True, "USE_TZ must be True for timezone-aware datetime handling"

    def test_default_auto_field_configured(self):
        """Verify DEFAULT_AUTO_FIELD is set to BigAutoField"""
        default_auto_field = settings.DEFAULT_AUTO_FIELD
        assert default_auto_field == "django.db.models.BigAutoField", (
            f"DEFAULT_AUTO_FIELD should be BigAutoField, got: {default_auto_field}"
        )

    def test_site_id_is_one(self):
        """
        Verify SITE_ID is 1 (single-tenant architecture).
        Spwig is single-tenant - each merchant gets their own installation.
        """
        assert settings.SITE_ID == 1, (
            f"SITE_ID must be 1 for single-tenant architecture, got: {settings.SITE_ID}"
        )

    def test_static_url_configured(self):
        """Verify STATIC_URL is configured"""
        static_url = settings.STATIC_URL
        assert static_url, "STATIC_URL must be configured"
        assert static_url.endswith("/"), "STATIC_URL must end with /"

    def test_media_url_configured(self):
        """Verify MEDIA_URL is configured"""
        media_url = settings.MEDIA_URL
        assert media_url, "MEDIA_URL must be configured"
        assert media_url.endswith("/"), "MEDIA_URL must end with /"

    def test_templates_configured(self):
        """Verify TEMPLATES is properly configured"""
        templates = settings.TEMPLATES
        assert templates, "TEMPLATES must be configured"
        assert len(templates) > 0, "At least one template engine must be configured"

        # Check Django template engine
        django_engine = next(
            (
                t
                for t in templates
                if t["BACKEND"] == "django.template.backends.django.DjangoTemplates"
            ),
            None,
        )
        assert django_engine is not None, "Django template engine must be configured"

        # Verify app template discovery is enabled
        # Either via APP_DIRS=True OR app_directories.Loader in custom loaders
        app_dirs = django_engine.get("APP_DIRS", False)
        custom_loaders = django_engine.get("OPTIONS", {}).get("loaders", [])

        has_app_dirs = (
            app_dirs or "django.template.loaders.app_directories.Loader" in custom_loaders
        )

        assert has_app_dirs, (
            "App template discovery must be enabled via APP_DIRS=True or "
            "'django.template.loaders.app_directories.Loader' in OPTIONS['loaders']"
        )

    def test_databases_configured(self):
        """Verify DATABASES is configured"""
        databases = settings.DATABASES
        assert databases, "DATABASES must be configured"
        assert "default" in databases, "Default database must be configured"

        default_db = databases["default"]
        assert default_db.get("ENGINE"), "Database ENGINE must be configured"
        assert default_db.get("NAME"), "Database NAME must be configured"
