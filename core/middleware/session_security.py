"""
Session Security Middleware

Ensures session is regenerated after authentication to prevent session fixation attacks.
Django's auth backend should do this automatically, but this provides defense-in-depth.
"""


class SessionSecurityMiddleware:
    """
    Regenerate session key after successful authentication.

    Prevents session fixation attacks where an attacker sets a victim's
    session cookie before login and hijacks the session after authentication.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store pre-request authentication status and session key
        was_authenticated = request.user.is_authenticated if hasattr(request, "user") else False
        old_session_key = (
            request.session.session_key
            if hasattr(request, "session") and request.session.session_key
            else None
        )

        # Process the request
        response = self.get_response(request)

        # Check if user just authenticated (wasn't before, is now)
        is_authenticated = request.user.is_authenticated if hasattr(request, "user") else False

        # If user just logged in, regenerate session key
        if not was_authenticated and is_authenticated and hasattr(request, "session"):
            # Create new session key while preserving session data
            request.session.cycle_key()
            # Save the session to ensure new key is written to response
            request.session.save()

            # Update the response cookie with new session ID
            new_session_key = request.session.session_key
            if new_session_key and old_session_key != new_session_key:
                # Django's session middleware already set the cookie, we need to update it
                from django.conf import settings

                response.set_cookie(
                    settings.SESSION_COOKIE_NAME,
                    new_session_key,
                    max_age=settings.SESSION_COOKIE_AGE,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    secure=settings.SESSION_COOKIE_SECURE,
                    httponly=settings.SESSION_COOKIE_HTTPONLY,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )

        return response
