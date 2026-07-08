"""
Tests for ShippingZone model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Q

from shipping.models import ShippingZone


User = get_user_model()


class ShippingZoneModelTest(TestCase):
    """Test ShippingZone model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_zone_minimal(self):
        """Test creating a minimal shipping zone"""
        zone = ShippingZone.objects.create(
            name='Test Zone',
            priority=0,
            is_active=True,
            created_by=self.user,
        )

        self.assertEqual(zone.name, 'Test Zone')
        self.assertEqual(zone.priority, 0)
        self.assertTrue(zone.is_active)
        self.assertEqual(zone.countries, [])
        self.assertEqual(zone.states, {})
        self.assertEqual(zone.postal_code_patterns, [])

    def test_create_zone_with_countries(self):
        """Test creating a zone with country restrictions"""
        zone = ShippingZone.objects.create(
            name='North America',
            description='US, Canada, Mexico',
            priority=5,
            is_active=True,
            countries=['US', 'CA', 'MX'],
            created_by=self.user,
        )

        self.assertEqual(zone.name, 'North America')
        self.assertIn('US', zone.countries)
        self.assertIn('CA', zone.countries)
        self.assertIn('MX', zone.countries)
        self.assertEqual(len(zone.countries), 3)

    def test_create_zone_with_states(self):
        """Test creating a zone with state restrictions"""
        zone = ShippingZone.objects.create(
            name='West Coast',
            priority=10,
            is_active=True,
            countries=['US'],
            states={'US': ['CA', 'OR', 'WA']},
            created_by=self.user,
        )

        self.assertIn('US', zone.states)
        self.assertEqual(zone.states['US'], ['CA', 'OR', 'WA'])
        self.assertEqual(zone.get_state_count(), 3)

    def test_create_zone_with_postal_patterns(self):
        """Test creating a zone with postal code patterns"""
        zone = ShippingZone.objects.create(
            name='NYC Metro',
            priority=15,
            is_active=True,
            countries=['US'],
            postal_code_patterns=[r'^10\d{3}$', r'^11\d{3}$'],
            created_by=self.user,
        )

        self.assertEqual(len(zone.postal_code_patterns), 2)
        self.assertIn(r'^10\d{3}$', zone.postal_code_patterns)

    def test_zone_str(self):
        """Test __str__ method"""
        zone = ShippingZone.objects.create(
            name='Europe Zone',
            priority=0,
            created_by=self.user,
        )
        self.assertEqual(str(zone), 'Europe Zone')

    def test_matches_address_no_restrictions(self):
        """Test zone with no restrictions matches all addresses"""
        zone = ShippingZone.objects.create(
            name='Worldwide',
            priority=99,
            is_active=True,
        )

        # Should match any address
        self.assertTrue(zone.matches_address({'country': 'US'}))
        self.assertTrue(zone.matches_address({'country': 'GB'}))
        self.assertTrue(zone.matches_address({'country': 'JP', 'state': 'Tokyo', 'postal_code': '100-0001'}))

    def test_matches_address_country_match(self):
        """Test zone matches by country code"""
        zone = ShippingZone.objects.create(
            name='USA Only',
            priority=0,
            is_active=True,
            countries=['US'],
        )

        # Should match US addresses
        self.assertTrue(zone.matches_address({'country': 'US'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '90210'}))

        # Should not match other countries
        self.assertFalse(zone.matches_address({'country': 'CA'}))
        self.assertFalse(zone.matches_address({'country': 'GB'}))

    def test_matches_address_country_no_match(self):
        """Test zone doesn't match wrong country"""
        zone = ShippingZone.objects.create(
            name='Europe',
            priority=0,
            is_active=True,
            countries=['GB', 'FR', 'DE'],
        )

        self.assertTrue(zone.matches_address({'country': 'GB'}))
        self.assertTrue(zone.matches_address({'country': 'FR'}))
        self.assertFalse(zone.matches_address({'country': 'US'}))

    def test_matches_address_state_match(self):
        """Test zone matches by state/province"""
        zone = ShippingZone.objects.create(
            name='West Coast',
            priority=0,
            is_active=True,
            countries=['US'],
            states={'US': ['CA', 'OR', 'WA']},
        )

        # Should match west coast states
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'OR'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'WA'}))

        # Should not match other US states
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'NY'}))
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'TX'}))

        # Should not match other countries even with state
        self.assertFalse(zone.matches_address({'country': 'CA', 'state': 'BC'}))

    def test_matches_address_state_no_match(self):
        """Test zone doesn't match wrong state"""
        zone = ShippingZone.objects.create(
            name='California Only',
            priority=0,
            is_active=True,
            countries=['US'],
            states={'US': ['CA']},
        )

        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '90210'}))
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': '10001'}))

    def test_matches_address_postal_pattern_match(self):
        """Test zone matches by postal code pattern"""
        zone = ShippingZone.objects.create(
            name='NYC Metro',
            priority=0,
            is_active=True,
            countries=['US'],
            postal_code_patterns=[r'^10\d{3}$', r'^11\d{3}$'],
        )

        # Should match NYC zip codes
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': '10001'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': '10018'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': '11201'}))

        # Should not match other zip codes
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '90210'}))
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': '12345'}))

    def test_matches_address_postal_pattern_no_match(self):
        """Test zone doesn't match wrong postal pattern"""
        zone = ShippingZone.objects.create(
            name='Canadian Prairies',
            priority=0,
            is_active=True,
            countries=['CA'],
            postal_code_patterns=[r'^R\d[A-Z]\s?\d[A-Z]\d$'],  # Manitoba pattern
        )

        self.assertTrue(zone.matches_address({'country': 'CA', 'state': 'MB', 'postal_code': 'R3T 2N2'}))
        self.assertFalse(zone.matches_address({'country': 'CA', 'state': 'ON', 'postal_code': 'M5V 3A8'}))

    def test_matches_address_multiple_patterns(self):
        """Test zone with multiple postal patterns"""
        zone = ShippingZone.objects.create(
            name='Multiple Patterns',
            priority=0,
            is_active=True,
            countries=['US'],
            postal_code_patterns=[
                r'^90\d{3}$',  # LA area
                r'^94\d{3}$',  # SF area
            ],
        )

        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '90210'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '94102'}))
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '92101'}))

    def test_matches_address_combined_restrictions(self):
        """Test zone with country, state, and postal restrictions"""
        zone = ShippingZone.objects.create(
            name='California Metros',
            priority=0,
            is_active=True,
            countries=['US'],
            states={'US': ['CA']},
            postal_code_patterns=[r'^9[0-4]\d{3}$'],
        )

        # Must match ALL restrictions
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '90210'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '94102'}))

        # Wrong state
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': '90210'}))

        # Wrong postal pattern
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'CA', 'postal_code': '95000'}))

        # Wrong country
        self.assertFalse(zone.matches_address({'country': 'CA', 'state': 'BC', 'postal_code': '90210'}))

    def test_matches_address_invalid_postal_pattern(self):
        """Test zone with invalid regex pattern doesn't crash"""
        zone = ShippingZone.objects.create(
            name='Bad Pattern Zone',
            priority=0,
            is_active=True,
            countries=['US'],
            postal_code_patterns=['[invalid(regex'],
        )

        # Should return False gracefully on regex error
        self.assertFalse(zone.matches_address({'country': 'US', 'postal_code': '90210'}))

    def test_get_coverage_summary_no_restrictions(self):
        """Test coverage summary for unrestricted zone"""
        zone = ShippingZone.objects.create(
            name='Worldwide',
            priority=0,
        )

        summary = zone.get_coverage_summary()
        self.assertEqual(summary, 'All countries')

    def test_get_coverage_summary_countries_only(self):
        """Test coverage summary with only countries"""
        zone = ShippingZone.objects.create(
            name='North America',
            priority=0,
            countries=['US', 'CA', 'MX'],
        )

        summary = zone.get_coverage_summary()
        self.assertEqual(summary, '3 countries')

    def test_get_coverage_summary_single_country(self):
        """Test coverage summary with single country"""
        zone = ShippingZone.objects.create(
            name='USA',
            priority=0,
            countries=['US'],
        )

        summary = zone.get_coverage_summary()
        self.assertEqual(summary, '1 country')

    def test_get_coverage_summary_with_states(self):
        """Test coverage summary with states"""
        zone = ShippingZone.objects.create(
            name='West Coast',
            priority=0,
            countries=['US'],
            states={'US': ['CA', 'OR', 'WA']},
        )

        summary = zone.get_coverage_summary()
        self.assertIn('country', summary)  # "1 country"
        self.assertIn('state', summary)    # "3 states"

    def test_get_coverage_summary_with_postal_patterns(self):
        """Test coverage summary with postal patterns"""
        zone = ShippingZone.objects.create(
            name='NYC',
            priority=0,
            countries=['US'],
            postal_code_patterns=[r'^10\d{3}$'],
        )

        summary = zone.get_coverage_summary()
        self.assertIn('postal', summary)

    def test_get_state_count_no_states(self):
        """Test state count with no states"""
        zone = ShippingZone.objects.create(
            name='Test Zone',
            priority=0,
        )

        self.assertEqual(zone.get_state_count(), 0)

    def test_get_state_count_single_country(self):
        """Test state count with single country"""
        zone = ShippingZone.objects.create(
            name='US West',
            priority=0,
            states={'US': ['CA', 'OR', 'WA']},
        )

        self.assertEqual(zone.get_state_count(), 3)

    def test_get_state_count_multiple_countries(self):
        """Test state count with multiple countries"""
        zone = ShippingZone.objects.create(
            name='Multi Country',
            priority=0,
            states={
                'US': ['CA', 'NY'],
                'CA': ['ON', 'BC', 'AB'],
            },
        )

        self.assertEqual(zone.get_state_count(), 5)

    def test_zone_ordering_by_priority(self):
        """Test zones are ordered by priority"""
        zone_low = ShippingZone.objects.create(
            name='Low Priority',
            priority=100,
        )
        zone_high = ShippingZone.objects.create(
            name='High Priority',
            priority=0,
        )
        zone_medium = ShippingZone.objects.create(
            name='Medium Priority',
            priority=50,
        )

        zones = list(ShippingZone.objects.all())

        # Should be ordered by priority (0 = highest)
        self.assertEqual(zones[0], zone_high)
        self.assertEqual(zones[1], zone_medium)
        self.assertEqual(zones[2], zone_low)

    def test_active_zones_only(self):
        """Test filtering active zones"""
        active_zone = ShippingZone.objects.create(
            name='Active Zone',
            priority=0,
            is_active=True,
        )
        inactive_zone = ShippingZone.objects.create(
            name='Inactive Zone',
            priority=0,
            is_active=False,
        )

        active_zones = ShippingZone.objects.filter(is_active=True)

        self.assertIn(active_zone, active_zones)
        self.assertNotIn(inactive_zone, active_zones)

    def test_zone_priority_range(self):
        """Test priority values are within expected range"""
        zone = ShippingZone.objects.create(
            name='Test Zone',
            priority=50,
        )

        self.assertGreaterEqual(zone.priority, 0)
        self.assertLessEqual(zone.priority, 100)

    def test_zone_created_timestamp(self):
        """Test created_at is auto-populated"""
        zone = ShippingZone.objects.create(
            name='Test Zone',
            priority=0,
        )

        self.assertIsNotNone(zone.created_at)

    def test_zone_updated_timestamp(self):
        """Test updated_at is auto-updated"""
        zone = ShippingZone.objects.create(
            name='Test Zone',
            priority=0,
        )

        original_updated = zone.updated_at
        zone.name = 'Updated Zone'
        zone.save()
        zone.refresh_from_db()

        self.assertGreater(zone.updated_at, original_updated)

    def test_matches_address_case_sensitive_country(self):
        """Test country matching is case-sensitive"""
        zone = ShippingZone.objects.create(
            name='USA',
            priority=0,
            countries=['US'],
        )

        # Current implementation is case-sensitive
        self.assertFalse(zone.matches_address({'country': 'us'}))
        self.assertTrue(zone.matches_address({'country': 'US'}))

    def test_matches_address_case_sensitive_state(self):
        """Test state matching is case-sensitive"""
        zone = ShippingZone.objects.create(
            name='California',
            priority=0,
            countries=['US'],
            states={'US': ['CA']},
        )

        # Current implementation is case-sensitive
        self.assertFalse(zone.matches_address({'country': 'US', 'state': 'ca'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'CA'}))

    def test_empty_postal_code_with_pattern(self):
        """Test empty postal code with patterns - implementation allows empty postal codes"""
        zone = ShippingZone.objects.create(
            name='NYC',
            priority=0,
            countries=['US'],
            postal_code_patterns=[r'^10\d{3}$'],
        )

        # Current implementation: patterns only checked if postal_code is truthy
        # So empty postal code passes through
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'NY'}))
        self.assertTrue(zone.matches_address({'country': 'US', 'state': 'NY', 'postal_code': ''}))

    def test_none_values_in_matches_address(self):
        """Test matches_address handles None values gracefully"""
        zone = ShippingZone.objects.create(
            name='Test Zone',
            priority=0,
            countries=['US'],
        )

        # None state should still match if country matches
        self.assertTrue(zone.matches_address({'country': 'US'}))

    def test_whitespace_in_postal_code(self):
        """Test postal code matching handles whitespace"""
        zone = ShippingZone.objects.create(
            name='Canadian Zone',
            priority=0,
            countries=['CA'],
            postal_code_patterns=[r'^[KLMNPRST]\d[A-Z]\s?\d[A-Z]\d$'],
        )

        # Should match with or without space
        self.assertTrue(zone.matches_address({'country': 'CA', 'state': 'ON', 'postal_code': 'M5V 3A8'}))
        self.assertTrue(zone.matches_address({'country': 'CA', 'state': 'ON', 'postal_code': 'M5V3A8'}))
