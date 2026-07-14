from functools import wraps


def allow_iframe_sameorigin(view_func):
    """
    Allow same-origin iframe embedding with both X-Frame-Options and CSP.

    Sets X-Frame-Options: SAMEORIGIN and overrides CSP frame-ancestors
    from the global 'none' to 'self' for both enforcement and report-only
    policies. Uses django-csp 4.0 response attributes.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response["X-Frame-Options"] = "SAMEORIGIN"
        response._csp_replace = {"frame-ancestors": ["'self'"]}
        response._csp_replace_ro = {"frame-ancestors": ["'self'"]}
        return response

    return _wrapped
