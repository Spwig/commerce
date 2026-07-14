"""
Django Settings for Secured Address Autocomplete Service
Add these to your settings.py or settings/production.py
"""

# ============================================
# ADDRESS AUTOCOMPLETE CONFIGURATION
# ============================================

# Service URL (use HTTPS in production)
ADDRESS_AUTOCOMPLETE_URL = "http://geocoder.spwig.com"  # Change to https:// when SSL is configured

# API Key Authentication (required if API key is enabled on server)
# Generate with: openssl rand -hex 32
ADDRESS_AUTOCOMPLETE_API_KEY = None  # Set this to your API key when enabled

# Security Settings
ADDRESS_AUTOCOMPLETE_REQUIRE_HTTPS = False  # Set to True in production with SSL
ADDRESS_AUTOCOMPLETE_VERIFY_SSL = True  # Set to False only for self-signed certs

# Performance Settings
ADDRESS_AUTOCOMPLETE_TIMEOUT = 5.0  # Request timeout in seconds
ADDRESS_AUTOCOMPLETE_CACHE_TTL = 300  # Cache results for 5 minutes

# Rate Limiting by User Tier
ADDRESS_AUTOCOMPLETE_RATE_LIMITS = {
    "anonymous": 60,  # 60 requests per minute for anonymous users
    "registered": 300,  # 300 requests per minute for registered users
    "premium": 1000,  # 1000 requests per minute for premium users
}

# Feature Flags
ADDRESS_AUTOCOMPLETE_ENABLED = True  # Master switch to enable/disable feature
ADDRESS_AUTOCOMPLETE_REQUIRE_AUTH = False  # Require user authentication
ADDRESS_AUTOCOMPLETE_LOG_USAGE = True  # Log usage for analytics

# Widget Configuration
ADDRESS_AUTOCOMPLETE_WIDGET = {
    "min_chars": 3,  # Minimum characters before triggering autocomplete
    "delay": 300,  # Milliseconds to wait after typing stops
    "max_suggestions": 5,  # Maximum number of suggestions to show
    "auto_select_single": True,  # Auto-select if only one result
    "show_coordinates": False,  # Show lat/lon in suggestions
}

# Geo-biasing Configuration
ADDRESS_AUTOCOMPLETE_GEO_BIAS = {
    "use_geoip": True,  # Use GeoIP to bias results to user's country
    "default_country": "SG",  # Default country code if GeoIP fails
    "search_radius_km": 50,  # Bias results within this radius when coordinates available
}

# ============================================
# EXAMPLE PRODUCTION CONFIGURATION
# ============================================
"""
# Production settings with full security

# Use HTTPS
ADDRESS_AUTOCOMPLETE_URL = 'https://geocoder.spwig.com'

# Strong API key (generate with: openssl rand -hex 32)
ADDRESS_AUTOCOMPLETE_API_KEY = 'your-generated-api-key-here'

# Enforce HTTPS
ADDRESS_AUTOCOMPLETE_REQUIRE_HTTPS = True
ADDRESS_AUTOCOMPLETE_VERIFY_SSL = True

# Production cache settings (using Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'shop',
        'TIMEOUT': 300,
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/shop/geocoder.log',
        },
    },
    'loggers': {
        'address_autocomplete': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
"""

# ============================================
# TESTING CONFIGURATION
# ============================================
"""
# For testing the secured service

from address_autocomplete.services_secured import SecuredAddressEnhancer

def test_geocoder_access():
    enhancer = SecuredAddressEnhancer()
    status = enhancer.verify_service_access()

    if status['accessible']:
        print("✓ Geocoder service is accessible")
        if status['authenticated']:
            print("✓ Authentication successful")
        else:
            print("✗ Authentication failed:", status['error'])
    else:
        print("✗ Service not accessible:", status['error'])

    return status

# Run in Django shell:
# python manage.py shell
# >>> from myapp.settings import test_geocoder_access
# >>> test_geocoder_access()
"""
