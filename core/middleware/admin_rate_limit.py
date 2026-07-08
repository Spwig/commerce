"""
Admin Login Rate Limiting Middleware

Prevents brute force attacks on the Django admin login page by limiting
the number of login attempts per IP address.

Uses django-ratelimit with Redis cache backend for distributed rate limiting.
"""
from django.http import HttpResponse


class AdminLoginRateLimitMiddleware:
    """
    Rate limit admin login attempts to prevent brute force attacks.

    Configuration:
    - Rate: 5 attempts per minute per IP address
    - Method: POST only (GET requests for login page are not limited)
    - Cache: Uses default Redis cache backend
    - Response: HTTP 429 with plain text message when rate limit exceeded

    Installation:
    Add to MIDDLEWARE in settings.py after SessionMiddleware:
        'core.middleware.admin_rate_limit.AdminLoginRateLimitMiddleware',
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only rate limit POST requests to admin login
        # GET requests are for displaying the login form
        if request.path.endswith('/admin/login/') and request.method == 'POST':
            from django_ratelimit.core import is_ratelimited

            # Check if this IP has exceeded the rate limit
            ratelimited = is_ratelimited(
                request=request,
                group='admin_login',  # REQUIRED: provide group name
                key='ip',  # Rate limit by IP address
                rate='5/m',  # 5 attempts per minute
                method='POST',  # Only POST requests
                increment=True  # Increment the counter
            )

            if ratelimited:
                # Return HTTP 429 Too Many Requests
                return HttpResponse(
                    'Too many login attempts. Please try again in 1 minute.',
                    status=429,
                    content_type='text/plain'
                )

        # Continue processing the request
        return self.get_response(request)
