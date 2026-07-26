"""
Settings singleton and the gating logic.

`agentic.gating` is the only module anything reads to decide on/off, so its
behaviour is worth pinning directly: master switch, emergency stop, and the
per-protocol surfaces.
"""

import pytest
from django.http import Http404

from agentic import gating
from agentic.models import AgenticSettings

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


class TestSettingsSingleton:
    def test_get_settings_creates_one_row_at_pk_1(self):
        s = AgenticSettings.get_settings()
        assert s.pk == 1
        # Idempotent — never a second row.
        again = AgenticSettings.get_settings()
        assert again.pk == 1
        assert AgenticSettings.objects.count() == 1

    def test_defaults_are_off(self):
        s = AgenticSettings.get_settings()
        assert s.is_enabled is False
        assert s.kill_switch_engaged is False
        assert s.allow_unverified_checkout is False

    def test_save_pins_pk_to_1(self):
        s = AgenticSettings(is_enabled=True)
        s.save()
        assert s.pk == 1


class TestGating:
    def test_disabled_by_default(self):
        assert gating.agentic_is_enabled() is False

    def test_enabled_when_switched_on(self):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.save()
        assert gating.agentic_is_enabled() is True

    def test_kill_switch_overrides_master(self):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.kill_switch_engaged = True
        s.save()
        assert gating.agentic_is_enabled() is False

    def test_protocol_is_enabled_requires_master_on(self):
        s = AgenticSettings.get_settings()
        s.is_enabled = False
        s.ucp_enabled = True
        s.save()
        # UCP flag is on, but the master switch is off.
        assert gating.protocol_is_enabled("ucp") is False

    def test_protocol_flags_respected_when_on(self):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.ucp_enabled = True
        s.acp_enabled = False
        s.save()
        assert gating.protocol_is_enabled("ucp") is True
        assert gating.protocol_is_enabled("acp") is False
        assert gating.protocol_is_enabled("unknown") is False

    def test_require_agentic_raises_when_off(self):
        with pytest.raises(Http404):
            gating.require_agentic()

    def test_require_agentic_passes_when_on(self):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.save()
        # Must not raise.
        gating.require_agentic()

    def test_status_never_raises_and_reflects_state(self):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.kill_switch_engaged = True
        s.save()
        status = gating.agentic_status()
        assert status["enabled"] is False  # kill switch wins
        assert status["is_enabled"] is True
        assert status["kill_switch_engaged"] is True
        assert status["protocols"]["ucp"] is True
