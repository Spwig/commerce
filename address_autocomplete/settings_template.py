"""
Settings Template for Address Autocomplete with License Integration
Add these settings to your Django project
"""

# ========================================
# PLATFORM LICENSE CONFIGURATION
# ========================================

# Your Spwig platform license key (REQUIRED)
PLATFORM_LICENSE_KEY = "XXXX-XXXX-XXXX-XXXX"  # Your actual license key

# Unique installation identifier (auto-generated if not set)
INSTALLATION_UUID = None  # Will be auto-generated based on hostname

# Update server URL for license validation
UPDATE_SERVER_URL = "https://updates.spwig.com"

# ========================================
# GEOCODER SERVICE CONFIGURATION
# ========================================

# Geocoder service endpoint
GEOCODER_SERVICE_URL = "https://geocoder.spwig.com"

# JWT configuration — the shared secret is provisioned automatically by the
# update server on activation and read at runtime via
# core.platform_secrets.get_geocoder_secret(). This template value is a
# placeholder; do not hardcode a real key here.
GEOCODER_JWT_SECRET_KEY = "REPLACE_ME_WITH_PROVISIONED_SECRET"
GEOCODER_JWT_ALGORITHM = "HS256"
GEOCODER_JWT_ISSUER = "spwig-platform"
GEOCODER_JWT_EXPIRY_HOURS = 24

# These will be auto-populated from license
GEOCODER_JWT_TOKEN = None  # Auto-provisioned on startup
GEOCODER_MERCHANT_ID = None  # Auto-generated from license
GEOCODER_TIER = None  # Auto-determined from license type

# ========================================
# LICENSE TIER MAPPING
# ========================================

# Maps platform license types to geocoder service tiers
LICENSE_TO_GEOCODER_TIER = {
    "trial": "standard",  # 100 req/min
    "standard": "standard",  # 100 req/min
    "professional": "premium",  # 500 req/min
    "enterprise": "enterprise",  # 2000 req/min
}

# ========================================
# CACHING CONFIGURATION
# ========================================

# Cache for storing JWT tokens and geocoder results
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "shop",
        "TIMEOUT": 300,
    }
}

# ========================================
# MIDDLEWARE CONFIGURATION
# ========================================

MIDDLEWARE = [
    # ... other middleware ...
    "address_autocomplete.license_integration.GeocoderLicenseMiddleware",
    # ... other middleware ...
]

# ========================================
# INSTALLED APPS
# ========================================

INSTALLED_APPS = [
    # ... other apps ...
    "address_autocomplete",  # Add the address autocomplete app
    # ... other apps ...
]

# ========================================
# LOGGING CONFIGURATION
# ========================================

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
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/geocoder.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "address_autocomplete": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# ========================================
# CORS CONFIGURATION
# ========================================

CORS_ALLOWED_ORIGINS = [
    "https://geocoder.spwig.com",
    "https://spwig.com",
    "https://www.spwig.com",
    # Add your shop domains here
]

# ========================================
# AUTOMATIC TOKEN PROVISIONING
# ========================================

# Enable automatic token provisioning on startup
GEOCODER_AUTO_PROVISION = True

# Refresh token when it expires within this many hours
GEOCODER_TOKEN_REFRESH_THRESHOLD = 1  # hours

# ========================================
# USAGE TRACKING
# ========================================

# Track geocoder usage for analytics
GEOCODER_TRACK_USAGE = True

# Send usage reports to platform (for billing/monitoring)
GEOCODER_REPORT_USAGE = True

# ========================================
# FALLBACK CONFIGURATION
# ========================================

# Fallback to public Nominatim if geocoder is unavailable
GEOCODER_USE_FALLBACK = False  # Disabled by default

# Public Nominatim endpoint (rate limited)
GEOCODER_FALLBACK_URL = "https://nominatim.openstreetmap.org"
