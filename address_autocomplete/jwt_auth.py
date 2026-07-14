"""
JWT Authentication for Address Autocomplete Service
Allows merchant installations to authenticate using JWT tokens
"""

import hashlib
import logging
from datetime import timedelta
from typing import Any

import jwt
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)


class GeocoderJWTAuth:
    """
    JWT authentication for geocoder service
    Compatible with merchant installations
    """

    def __init__(self):
        # JWT Configuration
        self.secret_key = getattr(settings, "GEOCODER_JWT_SECRET_KEY", settings.SECRET_KEY)
        self.algorithm = getattr(settings, "GEOCODER_JWT_ALGORITHM", "HS256")
        self.expiry_hours = getattr(settings, "GEOCODER_JWT_EXPIRY_HOURS", 24)
        self.issuer = getattr(settings, "GEOCODER_JWT_ISSUER", "spwig-platform")

    def generate_merchant_token(
        self,
        merchant_id: str,
        installation_uuid: str,
        tier: str = "standard",
        custom_claims: dict | None = None,
    ) -> dict[str, Any]:
        """
        Generate JWT token for a merchant installation.

        Args:
            merchant_id: Unique merchant identifier
            installation_uuid: Installation UUID
            tier: Service tier (standard, premium, enterprise)
            custom_claims: Additional claims to include

        Returns:
            Dict with token and metadata
        """
        # Token expiry
        now = timezone.now()
        exp_time = now + timedelta(hours=self.expiry_hours)

        # Build payload
        payload = {
            # Standard JWT claims
            "iss": self.issuer,  # Issuer
            "sub": merchant_id,  # Subject (merchant ID)
            "aud": "geocoder.spwig.com",  # Audience
            "exp": exp_time.timestamp(),  # Expiration
            "iat": now.timestamp(),  # Issued at
            "nbf": now.timestamp(),  # Not before
            # Custom claims
            "installation_uuid": installation_uuid,
            "tier": tier,
            "rate_limit": self._get_rate_limit(tier),
            "cache_ttl": self._get_cache_ttl(tier),
            "allowed_operations": self._get_allowed_operations(tier),
        }

        # Add any custom claims
        if custom_claims:
            payload.update(custom_claims)

        # Generate token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return {
            "token": token,
            "expires_at": exp_time.isoformat(),
            "expires_in": self.expiry_hours * 3600,
            "tier": tier,
            "rate_limit": payload["rate_limit"],
        }

    def verify_token(self, token: str) -> tuple[bool, dict | None]:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token string

        Returns:
            Tuple of (is_valid, payload)
        """
        try:
            # Check token cache (for revoked tokens)
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            if cache.get(f"revoked_token:{token_hash}"):
                logger.warning("Attempted use of revoked token")
                return False, None

            # Decode and verify
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience="geocoder.spwig.com",
                issuer=self.issuer,
            )

            # Additional validation
            if "installation_uuid" not in payload:
                logger.warning("Token missing installation_uuid")
                return False, None

            # Cache valid token for faster subsequent checks
            cache.set(
                f"valid_token:{token_hash}",
                payload,
                timeout=300,  # Cache for 5 minutes
            )

            return True, payload

        except jwt.ExpiredSignatureError:
            logger.debug("Token expired")
            return False, {"error": "Token expired"}
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid token: {e}")
            return False, {"error": "Invalid token"}
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return False, {"error": "Verification failed"}

    def revoke_token(self, token: str, reason: str = "manual"):
        """
        Revoke a JWT token by adding it to blacklist.

        Args:
            token: Token to revoke
            reason: Reason for revocation
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # Decode to get expiry
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_signature": False, "verify_exp": False},
            )
            exp = payload.get("exp", 0)
            ttl = max(0, exp - timezone.now().timestamp())

            # Add to revocation cache
            cache.set(
                f"revoked_token:{token_hash}",
                {"reason": reason, "revoked_at": timezone.now().isoformat()},
                timeout=int(ttl),
            )
            logger.info(f"Token revoked for {payload.get('sub')}: {reason}")

        except Exception as e:
            logger.error(f"Error revoking token: {e}")

    def refresh_token(self, token: str) -> dict[str, Any] | None:
        """
        Refresh an existing token if valid.

        Args:
            token: Current JWT token

        Returns:
            New token info or None if refresh failed
        """
        is_valid, payload = self.verify_token(token)

        if not is_valid:
            return None

        # Check if token is eligible for refresh (not too old)
        iat = payload.get("iat", 0)
        now = timezone.now().timestamp()
        max_refresh_age = 7 * 24 * 3600  # 7 days

        if now - iat > max_refresh_age:
            logger.warning("Token too old for refresh")
            return None

        # Generate new token with same claims
        return self.generate_merchant_token(
            merchant_id=payload["sub"],
            installation_uuid=payload["installation_uuid"],
            tier=payload.get("tier", "standard"),
        )

    def _get_rate_limit(self, tier: str) -> int:
        """Get rate limit based on tier"""
        limits = {
            "standard": 100,  # 100 requests per minute
            "premium": 500,  # 500 requests per minute
            "enterprise": 2000,  # 2000 requests per minute
        }
        return limits.get(tier, 100)

    def _get_cache_ttl(self, tier: str) -> int:
        """Get cache TTL based on tier"""
        ttls = {
            "standard": 300,  # 5 minutes
            "premium": 600,  # 10 minutes
            "enterprise": 1800,  # 30 minutes
        }
        return ttls.get(tier, 300)

    def _get_allowed_operations(self, tier: str) -> list:
        """Get allowed operations based on tier"""
        operations = {
            "standard": ["autocomplete", "validate"],
            "premium": ["autocomplete", "validate", "normalize", "reverse"],
            "enterprise": [
                "autocomplete",
                "validate",
                "normalize",
                "reverse",
                "batch",
                "analytics",
            ],
        }
        return operations.get(tier, ["autocomplete", "validate"])


class GeocoderJWTMiddleware:
    """
    Django middleware for JWT authentication on geocoder endpoints
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.auth = GeocoderJWTAuth()
        self.protected_paths = ["/geocoder/api/", "/address_autocomplete/api/"]

    def __call__(self, request):
        # Check if path requires authentication
        if any(request.path.startswith(path) for path in self.protected_paths):
            # Extract token from Authorization header
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")

            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                is_valid, payload = self.auth.verify_token(token)

                if is_valid:
                    # Attach merchant info to request
                    request.merchant_id = payload["sub"]
                    request.installation_uuid = payload["installation_uuid"]
                    request.tier = payload.get("tier", "standard")
                    request.jwt_payload = payload
                else:
                    # Return 401 Unauthorized
                    from django.http import JsonResponse

                    return JsonResponse({"error": "Invalid or expired token"}, status=401)
            else:
                # No token provided
                from django.http import JsonResponse

                return JsonResponse({"error": "Authorization required"}, status=401)

        response = self.get_response(request)
        return response
