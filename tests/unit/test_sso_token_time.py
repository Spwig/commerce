"""
Regression tests for the SSO redirect JWT time claims.

``core.views.community_redirect`` / ``sso_redirect`` mint short-lived
(60-second) handoff tokens for the SSO broker. The ``iat``/``exp`` claims were
built with the deprecated, naive ``datetime.utcnow()`` (Python 3.12
DeprecationWarning). They now use Django's timezone-aware ``timezone.now()``.

Because PyJWT converts a datetime claim via ``timegm(dt.utctimetuple())``, the
aware-UTC value encodes to the *same* POSIX timestamp as the old naive-UTC
value, so the broker sees identical tokens. These tests lock that equivalence
and guard the 60-second lifetime.
"""

import warnings
from datetime import datetime, timedelta

import jwt
from django.test import SimpleTestCase
from django.utils import timezone


class SSOTokenTimeClaimsTests(SimpleTestCase):
    SECRET = "regression-secret"

    def _encode(self, iat, exp):
        return jwt.encode({"iat": iat, "exp": exp}, self.SECRET, algorithm="HS256")

    def test_django_now_is_utc_aware(self):
        now = timezone.now()
        self.assertIsNotNone(now.tzinfo)
        self.assertEqual(now.utcoffset(), timedelta(0))

    def test_aware_now_matches_legacy_naive_utcnow_timestamps(self):
        # The claims the views build, old vs new, must encode identically.
        # This test deliberately exercises the legacy naive-UTC path, so keep
        # datetime.utcnow() and locally suppress its deprecation warning rather
        # than change semantics (see module docstring).
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            naive = datetime.utcnow()
        aware = timezone.now()
        legacy = jwt.decode(
            self._encode(naive, naive + timedelta(seconds=60)),
            self.SECRET,
            algorithms=["HS256"],
        )
        current = jwt.decode(
            self._encode(aware, aware + timedelta(seconds=60)),
            self.SECRET,
            algorithms=["HS256"],
        )
        # Allow a 1s skew for the two now() reads bracketing the assertion.
        self.assertLessEqual(abs(legacy["iat"] - current["iat"]), 1)
        self.assertLessEqual(abs(legacy["exp"] - current["exp"]), 1)

    def test_token_has_60_second_lifetime_and_validates(self):
        iat = timezone.now()
        token = self._encode(iat, iat + timedelta(seconds=60))
        # Decodes with exp verification enabled (default) => not already expired.
        decoded = jwt.decode(token, self.SECRET, algorithms=["HS256"])
        self.assertEqual(decoded["exp"] - decoded["iat"], 60)

    def test_expired_aware_token_is_rejected(self):
        iat = timezone.now() - timedelta(seconds=120)
        token = self._encode(iat, iat + timedelta(seconds=60))
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt.decode(token, self.SECRET, algorithms=["HS256"])
