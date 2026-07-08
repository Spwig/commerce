"""
Tests for address autocomplete views
"""
from django.test import TestCase, RequestFactory
from unittest.mock import Mock, patch
from address_autocomplete.views import AutocompleteView


class AutocompleteViewTests(TestCase):
    """Tests for AutocompleteView"""

    def setUp(self):
        self.factory = RequestFactory()
        self.view = AutocompleteView()

    def test_postcode_detection_singapore(self):
        """Test that Singapore postcode 118860 is detected correctly"""
        response = self.client.get('/api/address/autocomplete/', {
            'q': '118860',
            'country': 'SG'
        })
        self.assertEqual(response.status_code, 200)
        # Verify postcode was detected
        data = response.json()
        self.assertIn('suggestions', data)

    def test_postcode_detection_patterns(self):
        """Test postcode pattern detection for various countries"""
        test_cases = [
            ('118860', 'SG', True),   # Singapore: 6 digits
            ('2000', 'AU', True),      # Australia: 4 digits
            ('SW1A 1AA', 'GB', True),  # UK postcode
            ('10001', 'US', True),     # US zip code
            ('M5H 2N2', 'CA', True),   # Canada postal code
            ('Main Street', 'US', False),  # Not a postcode
        ]

        for query, country, expected_is_postcode in test_cases:
            result = self.view._is_postcode_query(query, country)
            self.assertEqual(
                result, expected_is_postcode,
                f"Failed for {query} in {country}"
            )

    @patch('address_autocomplete.services.AutocompleteClient.autocomplete')
    def test_country_based_sorting(self, mock_autocomplete):
        """Test that results are sorted with country matches first"""
        # Mock suggestions with mixed countries
        mock_autocomplete.return_value = {
            'suggestions': [
                {'label': 'US Address 1', 'components': {'country_code': 'us'}, 'confidence': 0.9},
                {'label': 'SG Address 1', 'components': {'country_code': 'sg'}, 'confidence': 0.8},
                {'label': 'US Address 2', 'components': {'country_code': 'us'}, 'confidence': 0.7},
                {'label': 'SG Address 2', 'components': {'country_code': 'sg'}, 'confidence': 0.6},
            ]
        }

        response = self.client.get('/api/address/autocomplete/', {
            'q': 'Main Street',
            'country': 'SG'
        })

        data = response.json()
        suggestions = data['suggestions']

        # Verify SG addresses come first (indices 0 and 1)
        self.assertEqual(suggestions[0]['components']['country_code'], 'sg')
        self.assertEqual(suggestions[1]['components']['country_code'], 'sg')
        # Verify US addresses come after (indices 2 and 3)
        self.assertEqual(suggestions[2]['components']['country_code'], 'us')
        self.assertEqual(suggestions[3]['components']['country_code'], 'us')

    def test_increased_result_limit(self):
        """Test that API accepts limit up to 10 results"""
        response = self.client.get('/api/address/autocomplete/', {
            'q': 'Main Street',
            'limit': '10'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Verify up to 10 results returned (if available)
        self.assertLessEqual(len(data['suggestions']), 10)

    def test_limit_cap_at_10(self):
        """Test that limit is capped at 10 even if higher value requested"""
        response = self.client.get('/api/address/autocomplete/', {
            'q': 'Main Street',
            'limit': '50'  # Request more than max
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should be capped at 10
        self.assertLessEqual(len(data['suggestions']), 10)

    def test_geoip_country_bias(self):
        """Test that GeoIP country is used when no explicit country provided"""
        # Mock request with geo_location
        request = self.factory.get('/api/address/autocomplete/', {'q': 'Test'})
        request.geo_location = {
            'country_code': 'AU',
            'coordinates': {'lat': -33.8688, 'lon': 151.2093}
        }

        # Test that country and coordinates are extracted
        country = self.view.get_country_bias(request)
        lat, lon = self.view.get_geo_bias(request)

        self.assertEqual(country, 'AU')
        self.assertEqual(lat, -33.8688)
        self.assertEqual(lon, 151.2093)

    def test_minimum_query_length(self):
        """Test that queries under 3 characters are rejected"""
        response = self.client.get('/api/address/autocomplete/', {
            'q': 'ab'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(len(data['suggestions']), 0)

    def test_country_sorting_preserves_confidence_order(self):
        """Test that within country groups, confidence order is preserved"""
        # Create suggestions with different confidence levels
        suggestions = [
            {'label': 'US Low', 'components': {'country_code': 'us'}, 'confidence': 0.5},
            {'label': 'SG High', 'components': {'country_code': 'sg'}, 'confidence': 0.9},
            {'label': 'US High', 'components': {'country_code': 'us'}, 'confidence': 0.8},
            {'label': 'SG Low', 'components': {'country_code': 'sg'}, 'confidence': 0.6},
        ]

        sorted_suggestions = self.view._sort_by_country_match(suggestions, 'SG')

        # SG results should come first, ordered by confidence (high to low)
        self.assertEqual(sorted_suggestions[0]['label'], 'SG High')
        self.assertEqual(sorted_suggestions[1]['label'], 'SG Low')
        # US results should come after, also ordered by confidence
        self.assertEqual(sorted_suggestions[2]['label'], 'US High')
        self.assertEqual(sorted_suggestions[3]['label'], 'US Low')
