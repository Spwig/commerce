"""
Specific tests for Singapore postcode 118860 (39 Pasir Panjang Hill)
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase

from address_autocomplete.services import AutocompleteClient


class SingaporePostcodeServiceTests(TestCase):
    """Tests for AutocompleteClient service methods with Singapore postcodes"""

    @patch("address_autocomplete.services.httpx.Client")
    def test_singapore_postcode_118860(self, mock_client_class):
        """Test that postcode 118860 returns correct address"""
        from django.core.cache import cache

        cache.clear()  # Clear cache to ensure mock is called

        # Configure mock httpx.Client instance
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        # Mock external geocoder response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "suggestions": [
                {
                    "label": "39 Pasir Panjang Hill, Singapore 118860",
                    "components": {
                        "house_number": "39",
                        "road": "Pasir Panjang Hill",
                        "postcode": "118860",
                        "city": "Singapore",
                        "country": "Singapore",
                        "country_code": "sg",
                    },
                    "confidence": 0.95,
                }
            ]
        }
        mock_instance.post.return_value = mock_response

        # NOW create client (uses mocked httpx.Client)
        client = AutocompleteClient()

        # Call method
        result = client.autocomplete(query="118860", country_bias="SG", is_postcode=True)

        self.assertEqual(len(result["suggestions"]), 1)
        self.assertIn("39 Pasir Panjang Hill", result["suggestions"][0]["label"])
        self.assertEqual(result["suggestions"][0]["components"]["postcode"], "118860")

        # Verify that the request included postcode parameters
        call_args = mock_instance.post.call_args
        request_data = call_args.kwargs["json"]
        self.assertIn("postalcode", request_data)
        self.assertEqual(request_data["postalcode"], "118860")
        self.assertIn("addressdetails", request_data)
        self.assertEqual(request_data["addressdetails"], 1)

    @patch("address_autocomplete.services.httpx.Client")
    def test_postcode_with_country_bias(self, mock_client_class):
        """Test that postcode lookup includes country bias"""
        from django.core.cache import cache

        cache.clear()  # Clear cache to ensure mock is called

        # Configure mock httpx.Client instance
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"suggestions": []}
        mock_instance.post.return_value = mock_response

        # Create client AFTER mock is set up
        client = AutocompleteClient()

        client.autocomplete(query="118860", country_bias="SG", is_postcode=True)

        call_args = mock_instance.post.call_args
        request_data = call_args.kwargs["json"]
        self.assertEqual(request_data["country_bias"], "SG")

    @patch("address_autocomplete.services.httpx.Client")
    def test_postcode_caching(self, mock_client_class):
        """Test that postcode results are cached"""
        from django.core.cache import cache

        # Clear cache first
        cache.clear()

        # Configure mock httpx.Client instance
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "suggestions": [
                {
                    "label": "39 Pasir Panjang Hill, Singapore 118860",
                    "components": {"postcode": "118860", "country_code": "sg"},
                }
            ]
        }
        mock_instance.post.return_value = mock_response

        # Create client AFTER mock is set up
        client = AutocompleteClient()

        # First call - should hit the API
        result1 = client.autocomplete(query="118860", country_bias="SG", is_postcode=True)
        self.assertEqual(mock_instance.post.call_count, 1)

        # Second call - should use cache
        result2 = client.autocomplete(query="118860", country_bias="SG", is_postcode=True)
        # Call count should still be 1 (cache hit)
        self.assertEqual(mock_instance.post.call_count, 1)

        # Results should be identical
        self.assertEqual(result1, result2)

    @patch("address_autocomplete.services.httpx.Client")
    def test_partial_postcode_search(self, mock_client_class):
        """Test searching with partial postcode"""
        from django.core.cache import cache

        cache.clear()  # Clear cache to ensure mock is called

        # Configure mock httpx.Client instance
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "suggestions": [
                {
                    "label": "39 Pasir Panjang Hill, Singapore 118860",
                    "components": {"postcode": "118860", "country_code": "sg"},
                },
                {
                    "label": "Different Address, Singapore 118861",
                    "components": {"postcode": "118861", "country_code": "sg"},
                },
            ]
        }
        mock_instance.post.return_value = mock_response

        # Create client AFTER mock is set up
        client = AutocompleteClient()

        # Search with partial postcode (not detected as full postcode)
        result = client.autocomplete(
            query="1188",
            country_bias="SG",
            is_postcode=False,  # Won't be detected as complete postcode
        )

        self.assertEqual(len(result["suggestions"]), 2)


class SingaporePostcodeViewTests(TestCase):
    """Tests for API endpoints with Singapore postcodes"""

    @patch("address_autocomplete.services.AutocompleteClient.autocomplete")
    def test_postcode_detection_api_endpoint(self, mock_autocomplete):
        """Test that the API endpoint detects postcodes correctly"""
        # Mock service response for Singapore postcode
        mock_autocomplete.return_value = {
            "suggestions": [
                {
                    "label": "39 Pasir Panjang Hill, Singapore 118860",
                    "components": {"postcode": "118860", "country_code": "sg"},
                }
            ]
        }

        # Singapore 6-digit postcode
        response = self.client.get("/api/address/autocomplete/", {"q": "118860", "country": "SG"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("suggestions", data)

        # Verify postcode was detected
        call_args = mock_autocomplete.call_args
        self.assertTrue(call_args.kwargs.get("is_postcode"))

        # Mock response for Australian postcode
        mock_autocomplete.return_value = {"suggestions": []}

        # Australia 4-digit postcode
        response = self.client.get("/api/address/autocomplete/", {"q": "2000", "country": "AU"})
        self.assertEqual(response.status_code, 200)
