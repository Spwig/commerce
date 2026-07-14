"""
Django settings for core project.
"""

import os
from pathlib import Path

import environ
from celery.schedules import crontab
from csp.constants import NONCE

# Platform version - single source of truth in core/version.py
from core.version import __version__ as PLATFORM_VERSION

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
)

CSRF_TRUSTED_ORIGINS = env.list(
    "SPWIG_CSRF_TRUSTED_ORIGINS", default=env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SPWIG_SECRET_KEY",
    default=env("DJANGO_SECRET_KEY", default="spwig-insecure-changeme-in-production"),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

# ALLOWED_HOSTS: Check SPWIG_ALLOWED_HOSTS, ALLOWED_HOSTS, and DJANGO_ALLOWED_HOSTS for flexibility
ALLOWED_HOSTS = (
    env.list("SPWIG_ALLOWED_HOSTS", default=None)
    or env.list("ALLOWED_HOSTS", default=None)
    or env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
)

# Application definition
INSTALLED_APPS = [
    # ASGI / Channels (must be before django.contrib.staticfiles)
    "daphne",
    # Third party apps that need to be loaded first
    "modeltranslation",
    # Django contrib apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",  # Required by django-allauth
    # Other third party apps
    "rest_framework",
    "rest_framework.authtoken",  # For API token authentication
    "django_extensions",
    "django_filters",
    "corsheaders",
    "djmoney",
    "compressor",
    "django_ckeditor_5",  # Modern rich text editor for product descriptions
    "django_countries",  # Country fields and flag images
    "storages",  # Django storage backends for S3/MinIO
    "django_celery_beat",  # Database-backed periodic task scheduling
    # Django-allauth for social authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.microsoft",
    "allauth.mfa",  # Multi-Factor Authentication
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # Local apps
    "core",
    # Platform apps
    "design",
    "page_builder.apps.PageBuilderConfig",
    "component_updates.apps.ComponentUpdatesConfig",  # Component update & distribution system
    "accounts",
    "catalog",
    "cart",
    "orders",
    "providers_common",  # Shared UI components for provider browse pages
    "email_system",  # Transactional email provider system
    "shipping",  # Shipping provider management and fulfillment
    "exchange_rates",  # Multi-currency exchange rate providers
    "product_feeds",  # Product feed syndication (Google Merchant, Facebook, etc.)
    "payment_providers",  # Payment provider integrations (Stripe, PayPal, AirWallex, etc.)
    "payout_providers",  # Affiliate payout provider integrations (PayPal Payouts, Airwallex Transfers)
    "webhooks",  # Outbound webhook system for headless integrations
    "subscriptions",  # Subscription billing and recurring payments
    "management",
    "media_library",
    "setup_wizard",
    "customers",
    "vouchers",
    "translations",
    "seo_generator",  # SEO meta content generation with provider system
    "geoip",
    "affiliate",  # Affiliate program management and tracking
    "loyalty",  # Customer loyalty and rewards program
    "social_sharing",  # Social media share tracking and analytics
    "blog",  # Blog system with categories, tags, subscribers, and social auto-sharing
    "announcements",  # Merchant-managed announcements for header/footer widgets
    "search",  # Site-wide search with autocomplete, analytics, and language support
    "wallet",  # Customer store credit wallet (ledger-based)
    "referrals",  # Customer referral program with rewards
    "migration.apps.MigrationConfig",  # Data migration from WooCommerce/other platforms
    "admin_api",  # Admin API for merchant mobile app
    "form_builder",  # Custom form builder for merchants
    "element_builder",  # Visual custom element builder for data-bound UI components
    "address_autocomplete",  # Address autocomplete with geocoder integration
    "pos_app",  # Point of Sale terminal management and models
    "pos_api",  # Point of Sale REST API (license-gated)
    "configurator_3d.apps.Configurator3DConfig",  # 3D product configurator visualization
    "customizable_product.apps.CustomizableProductConfig",  # Visual product customization editor (Fabric.js)
    "sms_system",  # SMS/WhatsApp messaging system for receipts and notifications
    "staff_roles",  # Staff roles and permission management
    "marketplace",  # Component marketplace for browsing and installing extensions
    "custom_fields",  # Merchant-defined custom fields for products, orders, categories, customers
    "domain_ssl",  # Domain & SSL configuration via admin GUI
    "enterprise_sso",  # Enterprise SSO via OpenID Connect (OIDC)
]

# API Documentation (drf-spectacular)
# Provides Swagger/ReDoc API documentation for merchants building headless frontends
ENABLE_API_DOCS = env("ENABLE_API_DOCS", default=True)
if ENABLE_API_DOCS:
    INSTALLED_APPS.append("drf_spectacular")

# Component source directory (for dev/build commands only, not used at runtime)
SPWIG_COMPONENTS_DIR = env(
    "SPWIG_COMPONENTS_DIR", default=str(BASE_DIR.parent / "spwig-components")
)

# Spwig HQ Mode - Enables developer portal and marketplace management
# Only active on the spwig.com backend instance, not on merchant installations
SPWIG_IS_HQ = env.bool("SPWIG_IS_HQ", default=False)
if SPWIG_IS_HQ:
    INSTALLED_APPS.append("developer_portal")
    INSTALLED_APPS.append("marketplace_checkout")
    INSTALLED_APPS.append("license_checkout")

# Sales Bell (Pi dashboard) - shared secret for the internal events API
SALES_BELL_TOKEN = env("SALES_BELL_TOKEN", default="")

# Upgrade server settings (for developer portal publishing bridge)
UPGRADE_SERVER_URL = env("UPGRADE_SERVER_URL", default="https://updates.spwig.com")
UPGRADE_SERVER_INTERNAL_API_KEY = env("UPGRADE_SERVER_INTERNAL_API_KEY", default="")

# Hosted mode — set by merchant-ctl during provisioning.
# Enables hosted-specific features (custom domain UI, managed SSL).
IS_HOSTED = env.bool("SPWIG_HOSTED", default=False)
HOSTING_INFRA_TIER = env("HOSTING_INFRA_TIER", default="")  # 'shared' or 'dedicated'

MIDDLEWARE = [
    "core.middleware.subpath.SubpathMiddleware",  # Handle URL subpath deployments (must be first)
    "django.middleware.security.SecurityMiddleware",
    *(
        ["whitenoise.middleware.WhiteNoiseMiddleware"] if not DEBUG else []
    ),  # Static files (production only)
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # For language detection
    "core.middleware.license_acceptance.LicenseAcceptanceMiddleware",  # License agreement acceptance gate (must run before ActivationMiddleware)
    "core.middleware.activation.ActivationMiddleware",  # Activation gate (redirects to /activate/ until activated)
    "core.middleware.admin_rate_limit.AdminLoginRateLimitMiddleware",  # Admin login brute force protection (5 attempts/min)
    "core.middleware.currency.CurrencyMiddleware",  # Multi-currency support
    "domain_ssl.middleware.DynamicAllowedHostsMiddleware",  # Dynamic ALLOWED_HOSTS from DB domain config
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core.middleware.session_security.SessionSecurityMiddleware",  # Session fixation prevention (MUST be after AuthenticationMiddleware)
    "allauth.account.middleware.AccountMiddleware",  # Required by django-allauth
    "core.middleware.license.LicenseEnforcementMiddleware",  # License enforcement (must run before admin/MFA)
    "core.middleware.mfa_enforcement.MFAEnforcementMiddleware",  # 2FA enforcement for admin
    "core.middleware.admin_access.AdminAccessMiddleware",  # Role-based admin panel gate
    "django.contrib.messages.middleware.MessageMiddleware",
    "core.middleware.admin_read_only.AdminReadOnlyMiddleware",  # Read-only enforcement for view-only roles
    "core.middleware.account_status.AccountStatusMiddleware",  # Account status enforcement for hosted installations
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",  # Content-Security-Policy header
    "pos_api.middleware.POSLicenseMiddleware",  # POS API sandbox-header injector (POS itself is universally enabled — no licence gate)
    "geoip.middleware.GeoIPMiddleware",  # GeoIP location resolution
    "catalog.middleware.RegionDetectionMiddleware",  # Sales region detection (requires GeoIPMiddleware)
    "management.middleware.ManagementAccessMiddleware",  # Management tools logging
    "setup_wizard.middleware.SetupWizardMiddleware",  # Setup wizard redirection
    "referrals.middleware.RequestContextMiddleware",  # Referral request context
    "referrals.middleware.ReferralTrackingMiddleware",  # Referral click tracking
    "core.middleware.maintenance.MaintenanceModeMiddleware",  # Maintenance mode handling
    "core.sandbox.middleware.SandboxBannerMiddleware",  # Sandbox mode visual indicator
    "core.middleware.error_reporting.ErrorReportingMiddleware",  # Error capture for Spwig diagnostics
]


ROOT_URLCONF = "core.urls"

# Subpath support - set SUBPATH env var to run under a URL prefix (e.g., /shop)
# This is used when deploying Spwig at example.com/shop/ instead of shop.example.com
FORCE_SCRIPT_NAME = env("SUBPATH", default=None)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR / "components_data" / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "core.context_processors.admin_theme",
                "core.context_processors.menu_badges",  # Admin menu badge counts
                "core.context_processors.license_status",  # License status for admin banners
                "core.context_processors.site_settings",  # Site settings for all templates
                "core.context_processors.read_only_status",  # Read-only admin user flag
                "core.context_processors.spwig_hq",  # HQ-only features flag
                "core.context_processors.ssl_status",  # SSL warning banner
                "core.currency_context.currency_context",  # Multi-currency support
                "design.template_loader.theme_context_processor",  # Theme context
                "design.context_processors.design_settings",  # Global design settings (logo, etc.)
                "design.context_processors.utility_assets",  # Dynamic utility loading (design app)
                "page_builder.context_processors.utility_assets",  # Dynamic utility loading (page builder)
                "payment_providers.context_processors.payment_providers",  # Express checkout methods
                "translations.context_processors.js_ui_translations",  # JS UI translations for merchant languages
            ],
            "loaders": [
                # Theme template loader with caching
                "design.template_loader.CachedThemeTemplateLoader",
                # Default Django loaders
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

# Theme configuration
THEME_OVERRIDE_DIR = BASE_DIR / "theme_overrides"  # Directory for merchant template overrides
THEME_DEV_DIR = BASE_DIR / "theme_dev"  # Directory for SDK development themes

# Theme SDK Development Server
# Only active in DEBUG mode - allows SDK CLI to connect for live development
THEME_DEV_SERVER = {
    "ENABLED": DEBUG,
    "SESSION_EXPIRY_HOURS": 24,
    "MAX_FILE_SIZE_MB": 10,
    "ALLOWED_FILE_EXTENSIONS": [
        ".html",
        ".css",
        ".js",
        ".json",
        ".svg",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".woff",
        ".woff2",
    ],
}

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Database
# When PGBOUNCER_HOST is set (production), Django connects through PgBouncer
# with two pools: 'default' (high-priority) and 'background' (low-priority).
# When not set (local development), Django connects directly to PostgreSQL.
PGBOUNCER_HOST = env("PGBOUNCER_HOST", default="")

_db_common = {
    "ENGINE": "django.db.backends.postgresql",
    "USER": env("DB_USER", default="shop_user"),
    "PASSWORD": env("DB_PASSWORD", default="changeme"),
    "OPTIONS": {
        "connect_timeout": 10,
    },
    "TEST": {
        "NAME": env("TEST_DB_NAME", default="test_shop_db"),
    },
}

if PGBOUNCER_HOST:
    DATABASES = {
        "default": {
            **_db_common,
            "NAME": env("DB_NAME", default="spwig"),
            "HOST": PGBOUNCER_HOST,
            "PORT": env("PGBOUNCER_PORT", default="6432"),
            "CONN_MAX_AGE": 0,  # PgBouncer manages the pool
            "DISABLE_SERVER_SIDE_CURSORS": True,  # Required for transaction pooling
        },
        "background": {
            **_db_common,
            "NAME": env("DB_NAME_BG", default="spwig_bg"),
            "HOST": PGBOUNCER_HOST,
            "PORT": env("PGBOUNCER_PORT", default="6432"),
            "CONN_MAX_AGE": 0,
            "DISABLE_SERVER_SIDE_CURSORS": True,
        },
    }
    DATABASE_ROUTERS = ["core.db_router.BackgroundTaskRouter"]
else:
    DATABASES = {
        "default": {
            **_db_common,
            "NAME": env("DB_NAME", default="shop_db"),
            "HOST": env("DB_HOST", default="localhost"),
            "PORT": env("DB_PORT", default="5432"),
            "CONN_MAX_AGE": 600,
        },
    }

# Cache configuration with Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{env('REDIS_PASSWORD', default='')}@{env('REDIS_HOST', default='localhost')}:{env('REDIS_PORT', default='6379')}/{env('REDIS_DB', default='0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
            },
            # Let django-redis auto-detect the best parser (hiredis if available)
        },
        "KEY_PREFIX": "shop",
        "TIMEOUT": 300,
    }
}

# Session configuration
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 86400 * 30  # 30 days
SESSION_COOKIE_SECURE = not DEBUG and os.environ.get("SSL_MODE", "none") not in ("none", "")
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = "en"
LANGUAGE_COOKIE_NAME = "lang"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
USE_L10N = True

# Available languages for the site (built-in)
_BUILTIN_LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
    ("fr", _("French")),
    ("de", _("German")),
    ("pt", _("Portuguese")),
    ("zh-hans", _("Simplified Chinese")),
    ("zh-hant", _("Traditional Chinese")),
    ("ja", _("Japanese")),
    ("ar", _("Arabic")),
    ("ru", _("Russian")),
    ("hi", _("Hindi")),
    ("id", _("Indonesian")),
    ("ko", _("Korean")),
    ("tr", _("Turkish")),
    ("vi", _("Vietnamese")),
    ("it", _("Italian")),
    ("th", _("Thai")),
]


def _extend_languages_from_packs(base_languages):
    """Extend LANGUAGES with installed language packs.

    Reads installed_language_packs.json (written by the language pack
    installer) and appends any additional languages not already in the
    built-in list.  This runs at startup so the file must be on disk —
    no DB access required.
    """
    import json as _json

    packs_file = BASE_DIR / "installed_language_packs.json"
    if not packs_file.exists():
        return base_languages
    try:
        with open(packs_file) as f:
            data = _json.load(f)
        extended = list(base_languages)
        existing_codes = {code for code, _ in extended}
        for code, info in data.get("packs", {}).items():
            if code not in existing_codes:
                extended.append((code, _(info["name"])))
        return extended
    except Exception:
        return base_languages


LANGUAGES = _extend_languages_from_packs(_BUILTIN_LANGUAGES)


# Path where Django will look for translation files
# Include both global locale and app-level locale directories
def get_locale_paths():
    """Automatically discover locale directories in all installed apps and page builder elements"""
    locale_paths = [BASE_DIR / "locale"]  # Global locale directory

    # Add locale directories from all local apps
    app_names = [
        "core",
        "design",
        "page_builder",
        "accounts",
        "catalog",
        "cart",
        "orders",
        "shipping",
        "payment_providers",
        "management",
        "media_library",
        "setup_wizard",
        "customers",
        "vouchers",
        "address_autocomplete",
        "affiliate",
        "announcements",
        "blog",
        "component_updates",
        "configurator_3d",
        "custom_fields",
        "developer_portal",
        "element_builder",
        "email_system",
        "exchange_rates",
        "form_builder",
        "geoip",
        "loyalty",
        "license_checkout",
        "marketplace",
        "marketplace_checkout",
        "migration",
        "payout_providers",
        "pos_app",
        "product_feeds",
        "referrals",
        "search",
        "seo_generator",
        "sms_system",
        "social_sharing",
        "staff_roles",
        "subscriptions",
        "translations",
        "webhooks",
        "domain_ssl",
    ]

    for app_name in app_names:
        app_locale_dir = BASE_DIR / app_name / "locale"
        if app_locale_dir.exists():
            locale_paths.append(app_locale_dir)

    # Add locale directories from page builder elements
    try:
        # Import here to avoid circular imports during Django setup
        from page_builder.element_registry import get_registry

        registry = get_registry()
        element_locale_paths = registry.get_element_locale_paths()
        for path in element_locale_paths:
            locale_paths.append(Path(path))
    except (ImportError, Exception):
        # During initial setup or if element registry is not available,
        # manually scan for element locale directories
        elements_dir = BASE_DIR / "page_builder" / "templates" / "page_builder" / "elements"
        if elements_dir.exists():
            for element_path in elements_dir.iterdir():
                if element_path.is_dir():
                    element_locale_dir = element_path / "locale"
                    if element_locale_dir.exists():
                        locale_paths.append(element_locale_dir)

    return locale_paths


LOCALE_PATHS = get_locale_paths()

# Enable language prefix in URLs
PREFIX_DEFAULT_LANGUAGE = True

# Static files (CSS, JavaScript, Images)
# When using FORCE_SCRIPT_NAME (subpath mode), prepend the subpath to URLs
_subpath = (FORCE_SCRIPT_NAME or "").rstrip("/")
STATIC_URL = f"{_subpath}/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Collected static files go here
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Project-wide static files
    # components_data/ handled by custom finders that skip old version directories
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "component_updates.finders.ComponentStaticFinder",  # components_data/static/
    "component_updates.finders.IntegrationStaticFinder",  # components_data/integrations/
]

# WhiteNoise configuration for static files (Django 5.1+ STORAGES format)
# NonStrictManifestStorage: hashes filenames for cache busting +
# pre-compresses to .gz/.br for nginx brotli_static/gzip_static.
# Non-strict mode tolerates CSS url() references to missing files
# (e.g. vendor libraries with image assets excluded from Docker build).
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "core.storage.NonStrictManifestStorage",
        },
    }

# Media files
# Include subpath prefix for proper URL generation
MEDIA_URL = f"{_subpath}/media/"
MEDIA_ROOT = BASE_DIR / "media"

# MinIO / S3-compatible Object Storage Configuration
# Used for digital assets (eBooks, software, etc.) and optionally for media files
MINIO_ENDPOINT = env("MINIO_ENDPOINT", default="localhost:9000")
MINIO_ACCESS_KEY = env("MINIO_ACCESS_KEY", default="minioadmin")
MINIO_SECRET_KEY = env("MINIO_SECRET_KEY", default="minioadmin")
MINIO_USE_SSL = env.bool("MINIO_USE_SSL", default=False)
MINIO_DIGITAL_ASSETS_BUCKET = env("MINIO_DIGITAL_ASSETS_BUCKET", default="digital-assets")
MINIO_MEDIA_BUCKET = env("MINIO_MEDIA_BUCKET", default="media")
MINIO_REGION = env("MINIO_REGION", default="us-east-1")

# AWS S3 / MinIO Storage Configuration (for django-storages)
AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_DIGITAL_ASSETS_BUCKET
AWS_S3_ENDPOINT_URL = f"{'https' if MINIO_USE_SSL else 'http'}://{MINIO_ENDPOINT}"
AWS_S3_REGION_NAME = MINIO_REGION
AWS_S3_USE_SSL = MINIO_USE_SSL
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_ADDRESSING_STYLE = "path"  # Required for MinIO
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None  # Use bucket policy instead
AWS_QUERYSTRING_AUTH = True  # Generate signed URLs
AWS_QUERYSTRING_EXPIRE = 3600  # Signed URL expiration (1 hour default)

# Django Compressor settings
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.rCSSMinFilter",
]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.rJSMinFilter"]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-modeltranslation configuration
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_TRANSLATION_REGISTRY = "translation"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en", "es", "fr")
MODELTRANSLATION_PREPOPULATE_LANGUAGE = "en"

# CORS settings
# Never allow all origins, even in DEBUG mode (security risk)
CORS_ALLOW_ALL_ORIGINS = False

# Explicitly allowed origins (can be overridden via environment variable)
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
)

# Allow flexible localhost ports in development only
CORS_ALLOWED_ORIGIN_REGEXES = (
    [
        r"^http://localhost:\d+$",
        r"^http://127\.0\.0\.1:\d+$",
    ]
    if DEBUG
    else []
)

# HTTP methods allowed for CORS requests
# Headless frontends need PATCH/PUT/DELETE for cart updates, address management, etc.
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Disable credentials for CORS requests (more secure)
# If specific origins need credentials, use a strict whitelist
CORS_ALLOW_CREDENTIALS = False

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "admin_api.authentication.MobileTokenAuthentication",  # Mobile app Bearer tokens
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]
    if DEBUG
    else ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    # Throttling configuration for API security
    "DEFAULT_THROTTLE_CLASSES": [
        "core.api.throttling.BurstRateThrottle",
        "core.api.throttling.SustainedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        # General rate limits
        "burst": "60/minute",  # Allow short bursts of activity
        "sustained": "1000/hour",  # Sustained rate for anonymous users
        "user": "5000/hour",  # Authenticated users get higher limits
        "user_burst": "120/minute",  # Authenticated user burst limit
        # Endpoint-specific strict limits (security-critical)
        "public_write": "20/hour",  # Very restrictive for public write operations
        "voucher_validation": "10/minute",  # Prevent voucher code enumeration
        "referral_tracking": "30/hour",  # Prevent token enumeration
        "social_tracking": "50/hour",  # Prevent spam in social tracking (authenticated)
        "social_tracking_anonymous": "20/hour",  # Stricter limit for anonymous guest share tracking
        "geoip": "100/hour",  # Prevent abuse as free IP lookup service
        # Admin API rate limits (merchant mobile app)
        "admin_auth": "5/minute",  # Login attempts (strict to prevent brute force)
        "admin_api": "300/minute",  # General admin API calls
        "admin_sensitive": "30/minute",  # Stock changes, status updates
        # Marketplace checkout rate limits (HQ only)
        "marketplace_checkout": "10/hour",  # Financial operations: user/cart/order/intent creation
        "marketplace_status": "60/hour",  # Payment status polling
        "hosting_webhook": "30/minute",  # Hosting provisioning webhooks from update server
        # POS API rate limits
        "pos_auth": "5/minute",  # POS login attempts (strict to prevent brute force)
        "pos_pin": "10/minute",  # PIN verification attempts (manager/cashier PINs)
    },
}

# Mobile App Admin API Settings
MOBILE_API_SETTINGS = {
    "ACCESS_TOKEN_LIFETIME_MINUTES": 30,  # Short-lived access tokens
    "REFRESH_TOKEN_LIFETIME_DAYS": 14,  # Long-lived refresh tokens
    "ROTATE_REFRESH_TOKENS": True,  # Issue new refresh token on use
    "MAX_DEVICES_PER_USER": 5,  # Maximum devices per staff user
    "MOBILE_APP_API_KEY": env(
        "MOBILE_APP_API_KEY", default=""
    ),  # App-level key for pre-auth endpoints
    "IOS_APP_ID": env(
        "IOS_APP_ID", default="RQ37N3FGPQ.com.spwig.Spwig"
    ),  # Apple App ID for Universal Links
}

# Push Notification Service Configuration
# Push notifications are sent via the centralized push.spwig.com service
# Authentication uses JWT secrets issued by the license server (stored in PlatformSecrets)
PUSH_SERVICE_URL = env("PUSH_SERVICE_URL", default="https://push.spwig.com")

# Configure drf-spectacular for API documentation
if ENABLE_API_DOCS:
    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

    # API Documentation settings (Swagger/ReDoc)
    SPECTACULAR_SETTINGS = {
        "TITLE": _("Spwig eCommerce API Documentation"),
        "DESCRIPTION": _("""## Spwig API Documentation

Welcome to the Spwig eCommerce Platform API documentation. This API enables you to build custom headless storefronts, mobile apps, and integrations.

### Authentication

Most endpoints require authentication using one of these methods:

- **Token Authentication**: Include `Authorization: Token <your-token>` header
- **Session Authentication**: Use Spwig session cookies (for browser-based apps)

Public endpoints (like product catalog) allow anonymous access.

### API Standards

- **Pagination**: List endpoints return 20 items per page by default. Use `?page=N` to navigate.
- **Filtering**: Most list endpoints support query parameter filtering
- **Multi-language**: Set `Accept-Language` header for localized responses
- **Multi-currency**: Currency information included in price responses

### Response Format

All endpoints return JSON with a consistent format:
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional status message"
}
```

### Rate Limiting

Public endpoints may be rate-limited. Authenticated requests have higher limits."""),
        "VERSION": PLATFORM_VERSION,
        "SERVE_INCLUDE_SCHEMA": False,  # Don't include schema endpoint in UI
        "COMPONENT_SPLIT_REQUEST": True,  # Split request/response schemas
        "SWAGGER_UI_SETTINGS": {
            "deepLinking": True,
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True,
            "tagsSorter": "alpha",
            "operationsSorter": "alpha",
        },
        "PREPROCESSING_HOOKS": [],
        "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
        "SERVERS": [],
        "TAGS": [
            {"name": "Accounts", "description": _("User authentication and profiles")},
            {"name": "Admin", "description": _("Admin API for merchant mobile app")},
            {"name": "Affiliate", "description": _("Affiliate marketing program")},
            {
                "name": "Announcements",
                "description": _("Store announcements for headers and footers"),
            },
            {"name": "Blog", "description": _("Blog posts, categories, tags, and subscriptions")},
            {"name": "Design", "description": _("Header/footer builder and design system APIs")},
            {"name": "Cart", "description": _("Shopping cart operations")},
            {"name": "Catalog", "description": _("Product catalog management")},
            {"name": "Checkout", "description": _("Checkout process and sessions")},
            {"name": "Custom Fields", "description": _("Custom field definitions and metadata")},
            {"name": "Customers", "description": _("Customer analytics and insights")},
            {"name": "Exchange Rates", "description": _("Multi-currency support")},
            {"name": "Help System", "description": _("Help documentation and admin metadata")},
            {"name": "Loyalty", "description": _("Customer loyalty program and rewards")},
            {
                "name": "Marketplace",
                "description": _("Marketplace checkout and purchases (HQ only)"),
            },
            {"name": "Media Library", "description": _("Media asset management")},
            {"name": "Messages", "description": _("Customer messages and contact form")},
            {"name": "Orders", "description": _("Order management")},
            {"name": "Store", "description": _("Store information and settings")},
            {"name": "Page Builder", "description": _("Content management and pages")},
            {"name": "Payments", "description": _("Payment methods and processing")},
            {"name": "Referrals", "description": _("Customer referral program")},
            {"name": "Reviews", "description": _("Product reviews and ratings")},
            {"name": "Shipping", "description": _("Shipping and fulfillment")},
            {"name": "Tax", "description": _("Tax rate management and calculation")},
            {"name": "Social Sharing", "description": _("Social media integration")},
            {"name": "Translations", "description": _("Translation service endpoints")},
            {"name": "Vouchers", "description": _("Discount codes and promotions")},
            {"name": "Wallet", "description": _("Customer store credit wallet")},
            {"name": "Webhooks", "description": _("Outbound webhook management")},
        ],
        "ENUM_NAME_OVERRIDES": {
            "ProductSerializer.status": "ProductStatusEnum",
            "SystemUpdateSerializer.status": "SystemUpdateStatusEnum",
            "MediaProcessingJobSerializer.status": "MediaProcessingJobStatusEnum",
            "OrderSerializer.status": "OrderStatusEnum",
            "ReturnRequestSerializer.status": "ReturnRequestStatusEnum",
            "PageSerializer.status": "PageStatusEnum",
            "ShipmentSerializer.status": "ShipmentStatusEnum",
            "GiftCardSerializer.status": "GiftCardStatusEnum",
        },
    }

# Help System - Admin Metadata API Token
# Used by the help autopilot system to fetch admin metadata
# Set this to a secure random token in production
ADMIN_METADATA_API_TOKEN = env("ADMIN_METADATA_API_TOKEN", default="")

# Email configuration
# The sandbox email backend wraps the real backend, intercepting emails in sandbox mode
SANDBOX_ACTUAL_EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_BACKEND = "core.sandbox.email_backend.SandboxEmailBackend"
if SANDBOX_ACTUAL_EMAIL_BACKEND != "django.core.mail.backends.console.EmailBackend":
    EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = env("EMAIL_PORT", default=587)
    EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=True)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@shop.com")

# django-money settings
# Note: Currencies are now managed dynamically via django-money's CURRENCIES
# See core.utils.currency_helpers for currency utilities
# Multi-currency configuration is managed via SiteSettings model

# Media Library Settings
MEDIA_LIBRARY_SETTINGS = {
    "AUTO_WEBP": True,
    "WEBP_QUALITY": 85,
    # Thumbnail sizes are now managed via ImageSizePreset model in media_library
    # Run `python manage.py setup_system_presets` to create system presets
    "MAX_UPLOAD_SIZE": 100 * 1024 * 1024,  # 100MB for videos
    # SVG removed from allowed extensions due to XSS risk
    # HTML/HTM files are blocked at validation layer
    "ALLOWED_IMAGE_EXTENSIONS": ["jpg", "jpeg", "png", "gif", "webp"],
    "BLOCKED_EXTENSIONS": ["html", "htm", "xhtml", "svg", "svgz"],  # Security: XSS risk
    "BLOCKED_MIME_TYPES": [
        "text/html",
        "application/xhtml+xml",
        "image/svg+xml",
    ],  # Security: XSS risk
    "ALLOWED_VIDEO_EXTENSIONS": ["mp4", "webm", "mov", "avi", "mkv"],
    "ENABLE_FACE_DETECTION": False,  # Set to True if opencv is installed
    "AUTO_GENERATE_THUMBNAILS": True,
    "OPTIMIZE_ON_UPLOAD": True,
    # Video-specific settings
    "VIDEO_FORMATS": {
        "webm_av1": {
            "container": "webm",
            "video_codec": "libsvtav1",
            "audio_codec": "libopus",
            "crf": 30,  # Quality (0-63, lower is better)
            "preset": 6,  # Speed (0-13, higher is faster)
        },
        "webm_vp9": {  # Fallback if AV1 not available
            "container": "webm",
            "video_codec": "libvpx-vp9",
            "audio_codec": "libopus",
            "crf": 30,
        },
        "mp4_h264": {  # For compatibility
            "container": "mp4",
            "video_codec": "libx264",
            "audio_codec": "aac",
            "crf": 23,  # Quality (0-51, lower is better)
            "preset": "medium",
        },
    },
    "VIDEO_THUMBNAIL_TIME": "00:00:02",  # Extract thumbnail at 2 seconds
    "VIDEO_RESOLUTIONS": {
        "1080p": "1920x1080",
        "720p": "1280x720",
        "480p": "854x480",
    },
    "AUTO_CONVERT_VIDEOS": True,  # Automatically convert uploaded videos
    "VIDEO_CONVERSION_FORMAT": "webm_av1",  # webm_av1, webm_vp9, mp4_h265
    "VIDEO_CRF": 30,  # Quality setting (lower = better, 20-40 typical)
    "VIDEO_PRESET": 6,  # AV1 encoding speed (0-13, higher = faster)
    "VIDEO_GENERATE_POSTER": True,  # Generate poster image from video
}

# Referrer policy — YouTube embeds require the referrer header.
# Django's SecurityMiddleware defaults to 'same-origin' which strips it,
# causing YouTube Error 153. 'strict-origin-when-cross-origin' is the
# browser default and is safe for both dev and production.
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Security settings for production
if not DEBUG:
    # Only enforce SSL redirect when SSL is actually configured
    _ssl_mode = os.environ.get("SSL_MODE", "none")
    _ssl_enabled = _ssl_mode not in ("none", "")
    SECURE_SSL_REDIRECT = _ssl_enabled
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    if _ssl_enabled:
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True
        CSRF_COOKIE_SECURE = True
    else:
        SECURE_HSTS_SECONDS = 0
        CSRF_COOKIE_SECURE = False
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    CSRF_COOKIE_HTTPONLY = True  # Prevent XSS attacks on CSRF tokens
else:
    # Development mode security settings
    CSRF_COOKIE_HTTPONLY = True  # Prevent XSS even in development
    X_FRAME_OPTIONS = "SAMEORIGIN"  # Allow same-origin framing in dev

# Content-Security-Policy configuration (django-csp 4.0)
# Nonce-based enforcement: no 'unsafe-inline' in script-src.
# Merchant custom JS (page.html, custom widget) uses nonce="{{ request.csp_nonce }}".
# All other inline scripts were extracted to external .js files during CSP migration.
#
# To temporarily revert to report-only mode (monitor without blocking):
#   1. Rename CONTENT_SECURITY_POLICY → CONTENT_SECURITY_POLICY_REPORT_ONLY
#   2. Restart Django
_CSP_DIRECTIVES = {
    "default-src": ["'self'"],
    "script-src": [
        "'self'",
        NONCE,  # Per-request nonce for merchant custom JS
        "'wasm-unsafe-eval'",  # POS barcode scanner (WebAssembly)
        "https://cdnjs.cloudflare.com",  # Monaco Editor (admin email template editor)
        "https://cdn.jsdelivr.net",  # ReDoc (API developer docs)
        "https://static.cloudflareinsights.com",  # Cloudflare Web Analytics beacon
    ],
    # Style — unsafe-inline required for dynamic theme CSS variables & inline styles
    "style-src": [
        "'self'",
        "'unsafe-inline'",
        "https://cdnjs.cloudflare.com",  # Monaco Editor CSS
        "https://cdn.jsdelivr.net",  # Swagger UI CSS (API docs)
        "https://fonts.googleapis.com",
    ],
    "img-src": ["'self'", "data:", "https:", "blob:"],
    "media-src": ["'self'", UPGRADE_SERVER_URL],
    "font-src": [
        "'self'",
        "https://cdnjs.cloudflare.com",  # Monaco Editor fonts
        "https://fonts.gstatic.com",
        "data:",
    ],
    "connect-src": [
        "'self'",
        "blob:",  # model-viewer (Three.js GLTFLoader) blob texture URLs
        "https://www.gstatic.com",  # Draco WASM decoder for compressed GLB/glTF models
        "https://cloudflareinsights.com",  # Cloudflare Web Analytics beacon reporting
    ],
    "frame-src": [
        "'self'",
        # Video & media embeds (page builder video element + CKEditor mediaEmbed)
        "https://www.youtube.com",  # YouTube embeds
        "https://www.youtube-nocookie.com",  # YouTube privacy-enhanced embeds
        "https://player.vimeo.com",  # Vimeo embeds
        "https://www.dailymotion.com",  # Dailymotion embeds
        "https://open.spotify.com",  # Spotify embeds
        "https://www.google.com",  # Google Maps embeds
        "https://maps.google.com",  # Google Maps alt domain
        "https://www.instagram.com",  # Instagram embeds
        "https://www.facebook.com",  # Facebook embeds
        "https://platform.twitter.com",  # Twitter/X embeds
        "https://www.flickr.com",  # Flickr embeds
    ],
    "worker-src": [
        "'self'",
        "blob:",  # Draco decoder creates blob workers for mesh decompression
    ],
    "frame-ancestors": ["'none'"],
    "form-action": ["'self'"],
    "report-uri": ["/api/csp-report/"],
}

# Enforce CSP (blocks violations)
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": _CSP_DIRECTIVES,
}

# Also send report-only header to catch edge cases during rollout
CONTENT_SECURITY_POLICY_REPORT_ONLY = {
    "DIRECTIVES": _CSP_DIRECTIVES,
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if not DEBUG else "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "csp": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# AWS S3 settings (optional)
if env("USE_S3", default=False):
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
        # CORS headers for canvas image analysis in admin
        "ACL": "public-read",
    }
    # Enable CORS for S3 bucket (allows canvas to analyze logo images)
    AWS_S3_CORS = [
        {
            "AllowedOrigins": ["*"],
            "AllowedMethods": ["GET", "HEAD"],
            "AllowedHeaders": ["*"],
            "MaxAgeSeconds": 3000,
        }
    ]
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.StaticS3Boto3Storage",
        },
    }
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# Sentry error tracking (optional)
SENTRY_DSN = env("SENTRY_DSN", default=None)
# License Configuration
# Path to license file - /opt/shop-platform/license for Docker with read-only mount
LICENSE_PATH = env("LICENSE_PATH", default="/opt/shop-platform/license/license.json")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment="production" if not DEBUG else "development",
    )

# Django-allauth configuration
SITE_ID = 1

# Authentication URLs
LOGOUT_REDIRECT_URL = "/"  # Redirect to homepage after logout

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "enterprise_sso.backends.SpwigOIDCBackend",  # Enterprise SSO via OIDC
    "django.contrib.auth.backends.ModelBackend",  # Default Django auth (email/password)
    "allauth.account.auth_backends.AuthenticationBackend",  # Social auth
]

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = "optional"  # Don't require email verification for social accounts
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False  # We use email as primary identifier
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_ADAPTER = "accounts.adapter.SpwigAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = True  # Automatically create accounts via social login
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True

# Social account provider settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "FETCH_USERINFO": True,
    },
    "apple": {
        "SCOPE": [
            "name",
            "email",
        ],
    },
    "microsoft": {
        "SCOPE": [
            "User.Read",
        ],
        "TENANT": "common",  # Allow personal and work accounts
    },
}

# Multi-Factor Authentication (MFA) Settings
# Provides TOTP (Time-based One-Time Password) support for enhanced security
MFA_ENABLED = True  # Enable MFA support in allauth
MFA_ADAPTER = "allauth.mfa.adapter.DefaultMFAAdapter"
MFA_TOTP_PERIOD = 30  # Codes valid for 30 seconds
MFA_TOTP_DIGITS = 6  # 6-digit codes
MFA_TOTP_ISSUER = "Spwig E-Commerce"  # Shows in authenticator apps
MFA_RECOVERY_CODE_COUNT = 10  # Number of one-time backup codes
MFA_SUPPORTED_TYPES = ["totp", "recovery_codes"]  # Available MFA methods
MFA_PASSKEY_LOGIN_ENABLED = False  # WebAuthn/FIDO2 not yet supported

# Enterprise SSO (OIDC) — most settings are read from DB via SpwigOIDCBackend.get_settings()
# These minimal settings are required at import time by mozilla-django-oidc
OIDC_RP_CLIENT_ID = ""  # Overridden from DB
OIDC_RP_CLIENT_SECRET = ""  # Overridden from DB
OIDC_OP_AUTHORIZATION_ENDPOINT = ""  # Overridden from DB
OIDC_OP_TOKEN_ENDPOINT = ""  # Overridden from DB
OIDC_OP_USER_ENDPOINT = ""  # Overridden from DB
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_CREATE_USER = False  # Controlled by DB setting (auto_create_users)
LOGIN_REDIRECT_URL = "/en/admin/"
LOGIN_REDIRECT_URL_FAILURE = "/en/admin/login/"
ALLOW_LOGOUT_GET_METHOD = True
OIDC_CALLBACK_CLASS = "enterprise_sso.views.SpwigOIDCCallbackView"
OIDC_AUTHENTICATE_CLASS = "enterprise_sso.views.SpwigOIDCAuthenticateView"

# Custom MFA forms - override to check only PRIMARY email verification
# Default allauth blocks 2FA if ANY email is unverified; we only care about primary
MFA_FORMS = {
    "activate_totp": "accounts.forms.ActivateTOTPForm",
}

# Django Channels (WebSocket support for POS customer display)
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (env("REDIS_HOST", default="localhost"), int(env("REDIS_PORT", default="6379")))
            ],
            "prefix": "pos-display",
        },
    },
}

# Celery Configuration
CELERY_BROKER_URL = f"redis://:{env('REDIS_PASSWORD', default='')}@{env('REDIS_HOST', default='localhost')}:{env('REDIS_PORT', default='6379')}/{env('REDIS_DB', default='0')}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes max per task
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes soft limit (warning)
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Fetch one task at a time
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000  # Restart worker after 1000 tasks
CELERY_TASK_IGNORE_RESULT = True  # Don't store results in Redis (no code uses AsyncResult)
CELERY_RESULT_EXPIRES = 3600  # Safety net: expire any stored results after 1 hour
CELERY_BEAT_MAX_LOOP_INTERVAL = 30  # DatabaseScheduler DB poll interval (default: 5s)

# Task routing - route shipping tasks to dedicated queue
CELERY_TASK_ROUTES = {
    "shipping.*": {"queue": "shipping"},
}

# =============================================================================
# Upgrader Service (Docker container orchestrator)
# =============================================================================
UPGRADER_URL = env("UPGRADER_URL", default="http://upgrader:8080")
FLEET_INSTANCE_NAME = env("FLEET_INSTANCE_NAME", default="")

# Celery Beat schedule for periodic tasks
# Anonymous deployment telemetry — sends a small once-daily payload to the
# update server (installation UUID + version + edition + coarse metrics)
# so we can see adoption across the OSS release. Opt out with
# `SPWIG_TELEMETRY=0` — that flips SPWIG_TELEMETRY_ENABLED below and the
# task exits early. See README's Privacy section for the exact payload.
SPWIG_TELEMETRY_ENABLED = env.bool("SPWIG_TELEMETRY", default=True)

CELERY_BEAT_SCHEDULE = {
    "send-daily-telemetry": {
        "task": "core.telemetry.tasks.send_daily_telemetry",
        "schedule": crontab(hour=1, minute=0),  # once daily; task jitters up to 1h
        "options": {"expires": 3600},
    },
    "refresh-hosted-service-usage": {
        # Poll /usage/ on each hosted service every 5 min and cache the
        # snapshot. This is the ONLY place the request happens — admin
        # request threads read the snapshot from cache. No-op for paid.
        "task": "core.hosted_services.tasks.refresh_hosted_service_usage",
        "schedule": 300.0,
        "options": {"expires": 240.0},
    },
    "check-hosted-service-quotas": {
        # Community-tier quota watcher. Emails the admin once per calendar
        # month per service when any of GeoIP/Geocoder/Push crosses 90%.
        "task": "core.hosted_services.tasks.check_hosted_service_quotas",
        "schedule": crontab(hour=7, minute=0),  # once daily at 07:00 UTC
        "options": {"expires": 3600},
    },
    "process-pending-translation-callbacks": {
        "task": "translations.tasks.process_pending_translation_callbacks",
        "schedule": 300.0,  # Run every 5 minutes (300 seconds)
        "options": {
            "expires": 240.0,  # Task expires after 4 minutes if not executed
        },
    },
    "flush-error-reports": {
        "task": "core.error_reporting.flush_error_reports",
        "schedule": 300.0,  # Every 5 minutes
        "options": {
            "expires": 240.0,
        },
    },
    # Loyalty Campaign Tasks
    "process-scheduled-campaigns": {
        "task": "loyalty.process_scheduled_campaigns",
        "schedule": 120.0,  # Run every 2 minutes
        "options": {
            "expires": 100.0,
        },
    },
    "process-campaign-journey-steps": {
        "task": "loyalty.process_campaign_journey_steps",
        "schedule": 300.0,  # Run every 5 minutes
        "options": {
            "expires": 240.0,
        },
    },
    "trigger-birthday-campaigns": {
        "task": "loyalty.trigger_birthday_campaigns",
        "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    "trigger-expiring-points-campaigns": {
        "task": "loyalty.trigger_expiring_points_campaigns",
        "schedule": crontab(hour=10, minute=0),  # Daily at 10 AM
    },
    "refresh-segment-memberships": {
        "task": "loyalty.refresh_segment_memberships",
        "schedule": 3600.0,  # Run every hour
        "options": {
            "expires": 3000.0,
        },
    },
    "calculate-campaign-statistics": {
        "task": "loyalty.calculate_campaign_statistics",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    # Referral Program Tasks
    "send-reward-expiry-reminders": {
        "task": "referrals.send_reward_expiry_reminders",
        "schedule": crontab(hour=10, minute=0),  # Daily at 10 AM
    },
    "expire-old-rewards": {
        "task": "referrals.expire_old_rewards",
        "schedule": crontab(hour=1, minute=0),  # Daily at 1 AM
    },
    "expire-old-attributions": {
        "task": "referrals.expire_old_attributions",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    "update-referrer-stats": {
        "task": "referrals.update_referrer_stats",
        "schedule": 21600.0,  # Run every 6 hours
        "options": {
            "expires": 18000.0,  # Expires after 5 hours
        },
    },
    "fraud-check-batch-process": {
        "task": "referrals.fraud_check_batch_process",
        "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    "cleanup-old-referral-events": {
        "task": "referrals.cleanup_old_events",
        "schedule": crontab(hour=4, minute=0, day_of_week=0),  # Weekly on Sunday at 4 AM
    },
    # POS
    "cleanup-expired-parked-carts": {
        # ParkedCart.expires_at defaults to now() + 24h at creation. Sweep
        # hourly at :15 so expired carts don't linger past their TTL by
        # more than an hour. Cleanup only touches carts that were never
        # restored (`restored_at IS NULL`) — resumed carts are cleared by
        # the checkout flow itself.
        "task": "pos_app.cleanup_expired_parked_carts",
        "schedule": crontab(minute=15),  # Hourly at :15 UTC
        "options": {
            "expires": 3300.0,  # Skip if not picked up within 55 min
        },
    },
    # License Refresh
    "refresh-license": {
        "task": "component_updates.refresh_license",
        "schedule": crontab(hour=3, minute=30),  # Daily at 3:30 AM
        "options": {
            "expires": 3600.0,  # Task expires after 1 hour
        },
    },
    # Hotfix Check
    "check-hotfixes": {
        "task": "component_updates.check_hotfixes",
        "schedule": 21600.0,  # Every 6 hours
        "options": {
            "expires": 21000.0,
        },
    },
    # System Metrics Collection Tasks
    "collect-system-metrics": {
        "task": "management.collect_system_metrics",
        "schedule": 600.0,  # Run every 10 minutes (600 seconds)
        "options": {
            "expires": 540.0,  # Task expires after 9 minutes if not executed
        },
    },
    "cleanup-old-metrics": {
        "task": "management.cleanup_old_metrics",
        "schedule": crontab(hour=5, minute=0),  # Daily at 5 AM
    },
    # Deployment Dashboard Tasks
    "collect-system-status": {
        "task": "management.collect_system_status",
        "schedule": 300.0,  # Run every 5 minutes
        "options": {
            "expires": 240.0,
        },
    },
    "check-scheduled-backups": {
        "task": "management.run_scheduled_backup",
        "schedule": crontab(minute=0),  # Every hour at minute 0
    },
    "cleanup-old-backups": {
        "task": "management.cleanup_old_backups",
        "schedule": crontab(hour=4, minute=0),  # Daily at 4 AM
    },
    # Subscription Billing Tasks
    "process-due-subscriptions": {
        "task": "subscriptions.process_due_subscriptions",
        "schedule": 3600.0,  # Run every hour (3600 seconds)
        "options": {
            "expires": 3300.0,  # Task expires after 55 minutes if not executed
        },
    },
    "process-trial-expirations": {
        "task": "subscriptions.process_trial_expirations",
        "schedule": crontab(hour=0, minute=30),  # Daily at 12:30 AM
    },
    "process-subscription-expirations": {
        "task": "subscriptions.process_subscription_expirations",
        "schedule": crontab(hour=0, minute=45),  # Daily at 12:45 AM
    },
    "process-auto-resume": {
        "task": "subscriptions.process_auto_resume",
        "schedule": crontab(hour=1, minute=0),  # Daily at 1:00 AM
    },
    "cleanup-old-billing-logs": {
        "task": "subscriptions.cleanup_old_billing_logs",
        "schedule": crontab(hour=3, minute=30, day_of_week=0),  # Weekly on Sunday at 3:30 AM
    },
    "retry-skipped-subscription-events": {
        "task": "subscriptions.retry_skipped_webhook_events",
        "schedule": 300.0,  # Every 5 minutes
        "options": {
            "expires": 240.0,
        },
    },
    # Subscription Email Notification Tasks
    "send-trial-ending-reminders": {
        "task": "subscriptions.send_trial_ending_reminders",
        "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    "send-renewal-reminders": {
        "task": "subscriptions.send_renewal_reminders",
        "schedule": crontab(hour=9, minute=15),  # Daily at 9:15 AM
    },
    "send-payment-method-expiry-warnings": {
        "task": "subscriptions.send_payment_method_expiry_warnings",
        "schedule": crontab(hour=9, minute=30),  # Daily at 9:30 AM
    },
    # Subscription Dunning & Grace Period Tasks
    "process-dunning-retries": {
        "task": "subscriptions.process_dunning_retries",
        "schedule": 21600.0,  # Every 6 hours
    },
    "process-grace-period-expirations": {
        "task": "subscriptions.process_grace_period_expirations",
        "schedule": crontab(hour=1, minute=15),  # Daily at 1:15 AM
    },
    "send-dunning-final-notices": {
        "task": "subscriptions.send_dunning_final_notices",
        "schedule": crontab(hour=9, minute=45),  # Daily at 9:45 AM
    },
    # Subscription Plan Change Tasks
    "process-scheduled-plan-changes": {
        "task": "subscriptions.process_scheduled_plan_changes",
        "schedule": crontab(hour=0, minute=15),  # Daily at 12:15 AM (before billing)
    },
    # Customer LTV Calculation Tasks
    "calculate-all-customer-ltv": {
        "task": "customers.calculate_all_customer_ltv",
        "schedule": crontab(hour=2, minute=30),  # Daily at 2:30 AM
        "options": {
            "expires": 7200,  # Task expires after 2 hours if not executed
        },
    },
    "rebuild-cohorts-weekly": {
        "task": "customers.rebuild_cohorts",
        "schedule": crontab(hour=3, minute=0, day_of_week=1),  # Weekly on Monday at 3 AM
        "options": {
            "expires": 3600,  # Task expires after 1 hour if not executed
        },
    },
    # Affiliate Payout Status Sync (fallback for webhook failures)
    "sync-pending-payout-statuses": {
        "task": "payout_providers.sync_pending_payout_statuses",
        "schedule": 3600.0,  # Run every hour (3600 seconds)
        "options": {
            "expires": 3000.0,  # Task expires after 50 minutes if not executed
        },
    },
    # Platform Secrets Refresh (license server JWT tokens)
    "refresh-platform-secrets": {
        "task": "core.refresh_platform_secrets",
        "schedule": 1800.0,  # Run every 30 minutes (1800 seconds)
        "options": {
            "expires": 1500.0,  # Task expires after 25 minutes if not executed
        },
    },
    # 2FA Trusted Device Cleanup
    "cleanup-expired-trusted-devices": {
        "task": "core.cleanup_expired_trusted_devices",
        "schedule": crontab(hour=4, minute=30),  # Daily at 4:30 AM
    },
    # Communication Preference Audit Log Cleanup (GDPR)
    "cleanup-old-preference-logs": {
        "task": "accounts.cleanup_old_preference_logs",
        "schedule": crontab(hour=3, minute=0),  # Daily at 3:00 AM UTC
        "kwargs": {"days": 90},  # Retain logs for 90 days (GDPR best practice)
    },
    # SMS Verification Code Cleanup (Security)
    "cleanup-expired-sms-codes": {
        "task": "accounts.cleanup_expired_sms_codes",
        "schedule": 3600.0,  # Run every 60 minutes (3600 seconds)
        "options": {
            "expires": 3300.0,  # Expires after 55 minutes if not executed
        },
    },
    # Affiliate Monthly Reports
    "send-affiliate-monthly-reports": {
        "task": "affiliate.send_affiliate_monthly_reports",
        "schedule": crontab(minute=0),  # Run every hour at :00 (checks day/hour internally)
        "options": {
            "expires": 3000.0,  # Expires after 50 minutes if not executed
        },
    },
    # Log Viewer Tasks
    "collect-docker-logs": {
        "task": "management.collect_docker_logs",
        "schedule": 60.0,  # Run every 60 seconds
        "options": {
            "expires": 50.0,  # Task expires after 50 seconds if not executed
        },
    },
    "archive-logs-to-db": {
        "task": "management.archive_logs_to_db",
        "schedule": 300.0,  # Run every 5 minutes (300 seconds)
        "options": {
            "expires": 240.0,  # Task expires after 4 minutes if not executed
        },
    },
    "cleanup-old-logs": {
        "task": "management.cleanup_old_logs",
        "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    # Gift Card Scheduled Email Delivery
    "send-scheduled-gift-card-emails": {
        "task": "catalog.send_scheduled_gift_card_emails",
        "schedule": 300.0,  # Run every 5 minutes (300 seconds)
        "options": {
            "expires": 240.0,  # Task expires after 4 minutes if not executed
        },
    },
    # Stock Reservation Cleanup
    "release-expired-stock-reservations": {
        "task": "catalog.release_expired_stock_reservations",
        "schedule": 120.0,  # Run every 2 minutes
        "options": {
            "expires": 100.0,
        },
    },
    # POS License Validation (daily against update server)
    # Booking Slot Reservation Cleanup
    "release-expired-booking-slot-reservations": {
        "task": "catalog.release_expired_booking_slot_reservations",
        "schedule": 120.0,  # Run every 2 minutes
        "options": {
            "expires": 100.0,
        },
    },
    # Booking Reminders
    "send-booking-reminders": {
        "task": "catalog.send_booking_reminders",
        "schedule": 900.0,  # Run every 15 minutes
        "options": {
            "expires": 840.0,
        },
    },
    "update-exchange-rates": {
        "task": "exchange_rates.tasks.update_exchange_rates",
        "schedule": 900.0,  # Every 15 minutes; task checks if sync interval warrants it
        "options": {
            "expires": 840.0,
        },
    },
    # SSL Certificate Renewal Check
    "check-certificate-renewal": {
        "task": "domain_ssl.tasks.check_certificate_renewal",
        "schedule": 43200.0,  # Every 12 hours (43200 seconds)
        "options": {
            "expires": 42000.0,  # Expires after ~11.5 hours if not executed
        },
    },
    # Help Embeddings Self-Healing
    # Loads pre-computed embeddings if missing (e.g. after first boot when
    # Celery wasn't available during seed). No-op when already loaded.
    "load-help-embeddings-if-missing": {
        "task": "core.load_help_embeddings",
        "schedule": 600.0,  # Every 10 minutes
        "kwargs": {"fixture_path": "core/fixtures/help_embeddings.jsonl.gz"},
        "options": {
            "expires": 540.0,
        },
    },
    # Visitor Analytics — daily aggregation and cleanup
    "geoip-aggregate-daily-stats": {
        "task": "geoip.aggregate_daily_page_stats",
        "schedule": crontab(hour=3, minute=0),
    },
    "geoip-cleanup-old-pageviews": {
        "task": "geoip.cleanup_old_pageviews",
        "schedule": crontab(hour=4, minute=0),
    },
    "geoip-cleanup-old-visitors": {
        "task": "geoip.cleanup_old_visitors",
        "schedule": crontab(hour=4, minute=30),
    },
}

# Developer Portal Analytics Sync (only active on spwig.com when SPWIG_IS_HQ=True)
if SPWIG_IS_HQ:
    CELERY_BEAT_SCHEDULE["sync-developer-analytics"] = {
        "task": "developer_portal.sync_developer_analytics",
        "schedule": 300.0,  # Every 5 minutes
        "options": {"expires": 240.0},
    }
    CELERY_BEAT_SCHEDULE["sync-developer-reviews"] = {
        "task": "developer_portal.sync_developer_reviews",
        "schedule": 300.0,  # Every 5 minutes
        "options": {"expires": 240.0},
    }
    CELERY_BEAT_SCHEDULE["sync-developer-components"] = {
        "task": "developer_portal.sync_developer_components",
        "schedule": 300.0,  # Every 5 minutes
        "options": {"expires": 240.0},
    }
    CELERY_BEAT_SCHEDULE["send-developer-review-digests"] = {
        "task": "developer_portal.send_review_digests",
        "schedule": 3600.0,  # Every hour (sends at ~8:00 UTC)
        "options": {"expires": 3000.0},
    }
    CELERY_BEAT_SCHEDULE["process-scheduled-emails"] = {
        "task": "email_system.tasks.process_scheduled_emails",
        "schedule": 300.0,  # Every 5 minutes
        "options": {"expires": 240.0},
    }
    # Hosted subscription billing
    CELERY_BEAT_SCHEDULE["hosted-process-billing"] = {
        "task": "hosted.process_due_billing",
        "schedule": 3600.0,  # Every hour
        "options": {"expires": 3000.0},
    }
    CELERY_BEAT_SCHEDULE["hosted-process-grace-periods"] = {
        "task": "hosted.process_grace_periods",
        "schedule": crontab(hour=3, minute=0),
    }
    CELERY_BEAT_SCHEDULE["hosted-process-terminations"] = {
        "task": "hosted.process_terminations",
        "schedule": crontab(hour=4, minute=0),
    }
    CELERY_BEAT_SCHEDULE["hosted-termination-warnings"] = {
        "task": "hosted.send_termination_warnings",
        "schedule": crontab(hour=5, minute=0),
    }
    CELERY_BEAT_SCHEDULE["hosted-escalate-suspended"] = {
        "task": "hosted.escalate_suspended",
        "schedule": crontab(hour=6, minute=0),
    }

# =============================================================================
# GeoIP Configuration - Spwig GeoIP Service
# =============================================================================
# Spwig GeoIP service with BGP routing data for 98% accuracy
GEOIP_SERVICE_URL = env("GEOIP_SERVICE_URL", default="https://geoip.spwig.com")

# Use the same JWT secret as the geocoder service for platform consistency
GEOIP_JWT_SECRET_KEY = env(
    "GEOIP_JWT_SECRET_KEY", default=env("GEOCODER_JWT_SECRET_KEY", default=SECRET_KEY)
)

# GeoIP service tier and configuration
GEOIP_TIER = env("GEOIP_TIER", default="standard")  # standard, premium, enterprise

# Configure Spwig as the default provider
GEOIP_CONFIG = {
    "PROVIDERS": [
        "geoip.providers.SpwigProvider",  # Primary provider with BGP data
        "geoip.providers.EdgeHeaderProvider",  # Fallback to CDN headers
        "geoip.providers.BrowserHintProvider",  # Fallback to browser hints
    ],
    "PROVIDER_CONFIG": {
        "cache_timeout": 3600,  # 1 hour cache
        "fallback_enabled": True,
        "timeout": 5,  # 5 second timeout for API calls
    },
}

# =============================================================================
# Address Autocomplete Configuration - Spwig Geocoder Service
# =============================================================================
# Spwig address autocomplete service using OpenStreetMap/Nominatim
ADDRESS_AUTOCOMPLETE_URL = env("ADDRESS_AUTOCOMPLETE_URL", default="https://geocoder.spwig.com")

# Autocomplete service configuration
ADDRESS_AUTOCOMPLETE_CONFIG = {
    "cache_timeout": 300,  # 5 minutes cache
    "request_timeout": 5,  # 5 second timeout
    "max_suggestions": 10,  # Maximum suggestions to return
}

# JWT configuration for geocoder authentication (prevent anonymous abuse).
# The shop signs its own JWTs with a shared secret set by the update server
# and persisted via core.platform_secrets. Empty by default — if the platform
# hasn't yet fetched the secret from the licence server, the geocoder client
# will simply skip the call rather than sign with a compromised default.
GEOCODER_JWT_SECRET_KEY = env("GEOCODER_JWT_SECRET_KEY", default="")
GEOCODER_JWT_ALGORITHM = env("GEOCODER_JWT_ALGORITHM", default="HS256")
GEOCODER_JWT_ISSUER = env("GEOCODER_JWT_ISSUER", default="spwig-platform")
GEOCODER_JWT_EXPIRY_HOURS = env.int("GEOCODER_JWT_EXPIRY_HOURS", default=24)

# =============================================================================
# Shipping Configuration
# =============================================================================
# Encryption key for storing API credentials securely
# Generate with: from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())
SHIPPING_ENCRYPTION_KEY = env("SHIPPING_ENCRYPTION_KEY", default=None)
EMAIL_ENCRYPTION_KEY = env("EMAIL_ENCRYPTION_KEY", default=None)

# Default origin country for shipping calculations
SHIPPING_ORIGIN_COUNTRY = env("SHIPPING_ORIGIN_COUNTRY", default="US")

# Webhook timeout for provider callbacks
SHIPPING_WEBHOOK_TIMEOUT = 30  # seconds
EMAIL_WEBHOOK_TIMEOUT = 30  # seconds

# Rate cache TTL (time to live)
SHIPPING_RATE_CACHE_TTL = 300  # 5 minutes

# Provider API timeouts
SHIPPING_PROVIDER_TIMEOUT = 10  # seconds for provider API calls

# Tracking update interval
SHIPPING_TRACKING_UPDATE_INTERVAL = 3600  # 1 hour (in seconds)

# =============================================================================
# Community / Discourse SSO Configuration
# =============================================================================
# SSO Broker URL (handles authentication federation to Discourse)
SSO_BROKER_URL = env("SSO_BROKER_URL", default="https://sso.spwig.com")

# Shared secret for auto-registration with SSO broker (must match broker's SSO_REGISTRATION_SECRET)
SSO_REGISTRATION_SECRET = env("SSO_REGISTRATION_SECRET", default="")

# Community forum URL (for direct links in documentation/help)
COMMUNITY_URL = env("COMMUNITY_URL", default="https://community.spwig.com")

# =============================================================================
# CKEditor 5 Configuration
# =============================================================================
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "licenseKey": "GPL",  # GPL v2+ license for self-hosted open source usage
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
        ],
    },
    "extends": {
        "licenseKey": "GPL",  # GPL v2+ license for self-hosted open source usage
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "imageUpload",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
    },
    "product_short": {
        "licenseKey": "GPL",
        "toolbar": [
            "bold",
            "italic",
            "link",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "removeFormat",
        ],
        "removePlugins": ["ImageToolbar", "ImageUpload", "ImageInsert"],
        "height": 150,
    },
    "content_rich": {
        "licenseKey": "GPL",
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "link",
            "|",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "insertImage",
            "mediaEmbed",
            "|",
            "insertTable",
            "|",
            "fontSize",
            "fontColor",
            "|",
            "sourceEditing",
            "removeFormat",
        ],
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph"},
                {"model": "heading2", "view": "h2", "title": "Heading 2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4"},
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "toggleImageCaption",
                "|",
                "imageStyle:inline",
                "imageStyle:wrapText",
                "imageStyle:breakText",
                "|",
                "resizeImage",
            ],
            "resizeOptions": [
                {"name": "resizeImage:original", "label": "Original"},
                {"name": "resizeImage:25", "value": "25", "label": "25%"},
                {"name": "resizeImage:50", "value": "50", "label": "50%"},
                {"name": "resizeImage:75", "value": "75", "label": "75%"},
            ],
            "styles": {
                "options": [
                    "inline",
                    "alignLeft",
                    "alignRight",
                    "alignCenter",
                    "alignBlockLeft",
                    "alignBlockRight",
                    "block",
                    "side",
                ]
            },
        },
        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
        "mediaEmbed": {
            "previewsInData": True,
        },
        "height": 500,
    },
    "announcement_basic": {
        "licenseKey": "GPL",
        "toolbar": ["bold", "italic", "|", "fontColor", "|", "removeFormat"],
        "removePlugins": ["ImageToolbar", "TableToolbar"],
        "height": 100,
    },
}

# Upload path for CKEditor 5 images
CKEDITOR_5_UPLOAD_PATH = "uploads/ckeditor/"

# Route CKEditor uploads through the Media Library for WebP conversion, thumbnails, and tracking
CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "ckeditor_media_library_upload"

# Load storefront theme CSS into CKEditor editing areas for WYSIWYG preview
# This endpoint dynamically serves the active theme's typography variables
# scoped to .ck-content so merchants see what their content will look like
CKEDITOR_5_CUSTOM_CSS = "/theme/css/editor-content.css"
