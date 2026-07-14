"""
Django system checks for production readiness

Registered via AppConfig.ready() in core/apps.py
Run with: python manage.py check --deploy
"""

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


@register(Tags.security, deploy=True)
def check_secret_key(app_configs, **kwargs):
    """Verify SECRET_KEY is not using default insecure value"""
    errors = []

    if "spwig-insecure" in settings.SECRET_KEY:
        errors.append(
            Error(
                "SECRET_KEY uses default insecure value",
                hint="Set SPWIG_SECRET_KEY environment variable to a strong random value",
                id="spwig.security.E001",
            )
        )

    if len(settings.SECRET_KEY) < 50:
        errors.append(
            Warning(
                f"SECRET_KEY is too short ({len(settings.SECRET_KEY)} chars, recommended 50+)",
                hint='Generate a longer key: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"',
                id="spwig.security.W001",
            )
        )

    return errors


@register(Tags.security)
def check_license_public_key(app_configs, **kwargs):
    """Verify the license public key exists and is a valid PEM file"""
    from pathlib import Path

    errors = []
    public_key_path = Path(__file__).parent / "keys" / "license-public-key.pem"

    if not public_key_path.exists():
        errors.append(
            Error(
                "License public key not found",
                hint=f"Expected at {public_key_path}. License signature verification will fail without this file.",
                id="spwig.license.E001",
            )
        )
    else:
        try:
            content = public_key_path.read_text()
            if "-----BEGIN PUBLIC KEY-----" not in content:
                errors.append(
                    Error(
                        "License public key is not a valid PEM file",
                        hint=f"File at {public_key_path} does not contain a valid PEM public key.",
                        id="spwig.license.E002",
                    )
                )
        except Exception as e:
            errors.append(
                Error(
                    f"Cannot read license public key: {e}",
                    hint=f"Check file permissions on {public_key_path}",
                    id="spwig.license.E003",
                )
            )

    return errors


@register(Tags.security, deploy=True)
def check_debug_setting(app_configs, **kwargs):
    """Verify DEBUG is False in production"""
    errors = []

    if settings.DEBUG:
        # Check if other indicators suggest production
        if "localhost" not in settings.ALLOWED_HOSTS and "127.0.0.1" not in settings.ALLOWED_HOSTS:
            errors.append(
                Error(
                    "DEBUG=True in production environment",
                    hint="Set DEBUG=False in .env file",
                    id="spwig.security.E002",
                )
            )

    return errors


@register(Tags.security, deploy=True)
def check_allowed_hosts(app_configs, **kwargs):
    """Verify ALLOWED_HOSTS is properly configured"""
    errors = []

    if not settings.DEBUG:
        if not settings.ALLOWED_HOSTS:
            errors.append(
                Error(
                    "ALLOWED_HOSTS is empty in production",
                    hint="Set SPWIG_ALLOWED_HOSTS environment variable",
                    id="spwig.security.E003",
                )
            )

        if settings.ALLOWED_HOSTS == ["*"]:
            errors.append(
                Error(
                    "ALLOWED_HOSTS set to wildcard (*) in production",
                    hint="Specify explicit hostnames in SPWIG_ALLOWED_HOSTS",
                    id="spwig.security.E004",
                )
            )

    return errors


@register(Tags.database, deploy=True)
def check_database_engine(app_configs, **kwargs):
    """Verify PostgreSQL is used (not SQLite)"""
    errors = []

    engine = settings.DATABASES["default"]["ENGINE"]

    if "sqlite" in engine and not settings.DEBUG:
        errors.append(
            Error(
                "SQLite database used in production",
                hint="Configure PostgreSQL via DB_NAME, DB_USER, DB_PASSWORD environment variables",
                id="spwig.database.E001",
            )
        )

    if "postgresql" not in engine:
        errors.append(
            Warning(
                f"Non-PostgreSQL database engine: {engine}",
                hint="Spwig is tested with PostgreSQL. Other engines may have issues.",
                id="spwig.database.W001",
            )
        )

    return errors


@register(Tags.caches, deploy=True)
def check_cache_backend(app_configs, **kwargs):
    """Verify Redis cache is configured"""
    errors = []

    backend = settings.CACHES["default"]["BACKEND"]

    if "redis" not in backend.lower() and not settings.DEBUG:
        errors.append(
            Error(
                f"Non-Redis cache backend in production: {backend}",
                hint="Configure Redis via REDIS_HOST, REDIS_PORT, REDIS_PASSWORD environment variables",
                id="spwig.cache.E001",
            )
        )

    return errors


@register(Tags.security, deploy=True)
def check_ssl_settings(app_configs, **kwargs):
    """Verify SSL/HTTPS settings for production"""
    errors = []

    if not settings.DEBUG:
        if not getattr(settings, "SECURE_SSL_REDIRECT", False):
            errors.append(
                Warning(
                    "SECURE_SSL_REDIRECT is False",
                    hint="Set SECURE_SSL_REDIRECT=True to redirect HTTP to HTTPS",
                    id="spwig.security.W002",
                )
            )

        if not getattr(settings, "SESSION_COOKIE_SECURE", False):
            errors.append(
                Warning(
                    "SESSION_COOKIE_SECURE is False",
                    hint="Set SESSION_COOKIE_SECURE=True to prevent session hijacking",
                    id="spwig.security.W003",
                )
            )

        if not getattr(settings, "CSRF_COOKIE_SECURE", False):
            errors.append(
                Warning(
                    "CSRF_COOKIE_SECURE is False",
                    hint="Set CSRF_COOKIE_SECURE=True to prevent CSRF attacks",
                    id="spwig.security.W004",
                )
            )

    return errors


@register(Tags.security)
def check_cors_configuration(app_configs, **kwargs):
    """Verify CORS is not set to allow all origins"""
    errors = []

    if getattr(settings, "CORS_ALLOW_ALL_ORIGINS", False):
        errors.append(
            Error(
                "CORS_ALLOW_ALL_ORIGINS is True",
                hint="Set CORS_ALLOW_ALL_ORIGINS=False and whitelist specific origins in CORS_ALLOWED_ORIGINS",
                id="spwig.security.E005",
            )
        )

    return errors
