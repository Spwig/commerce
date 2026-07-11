"""
POS is universally enabled from v1.5.8 onward.

Historically POS was a paid module gated at runtime by a signed licence
entitlement. Those gates are gone. This test file remains under the
community_edition/ suite to preserve the invariant explicitly: no matter
what edition the platform is running as, POS returns "active".

If a future change reintroduces feature gating for POS, these tests
break loudly and force a conversation before the change lands.
"""


def test_pos_license_is_valid_returns_true_regardless_of_edition():
    """``pos_license_is_valid()`` returns True under every edition."""
    from unittest.mock import patch

    from pos_app.license import pos_license_is_valid

    # Community edition — still True
    with patch("core.license.get_license_manager") as get_lm:
        get_lm.return_value.is_community.return_value = True
        assert pos_license_is_valid() is True

    # Non-community (Pro/Enterprise) — obviously still True
    with patch("core.license.get_license_manager") as get_lm:
        get_lm.return_value.is_community.return_value = False
        assert pos_license_is_valid() is True


def test_pos_status_shape_is_stable():
    """
    The status dict returned by ``get_pos_license_status`` retains the
    keys the admin dashboard expects. Values reflect universal
    activation.
    """
    from pos_app.license import get_pos_license_status

    status = get_pos_license_status()
    assert status["valid"] is True
    assert status["status"] == "active"
    assert status["license_key"] is None
    assert status["expires_at"] is None
    assert status["grace_period_ends"] is None
    assert status["days_remaining"] is None


def test_activate_pos_license_is_a_noop_success():
    """A legacy client POSTing a POS licence key gets a success reply."""
    from pos_app.license import activate_pos_license

    result = activate_pos_license("POS-1234-5678-9ABC-DEF0")
    assert result["success"] is True
    assert result["status"] == "active"
