"""
Test pre-flight checks
"""

from unittest.mock import MagicMock, patch

import requests
from django.contrib.auth.models import User
from django.test import TestCase

from migration.models import MigrationJob
from migration.validators.connection import PreFlightChecker


class PreFlightCheckerTest(TestCase):
    """Test pre-flight checks"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user("test", "test@test.com", "password")

        self.job = MigrationJob.objects.create(
            created_by=self.user,
            platform="woocommerce",
            method="api",
            connection_config={
                "store_url": "https://example.com",
                "consumer_key": "ck_test123",
                "consumer_secret": "cs_test456",
            },
        )

        self.checker = PreFlightChecker(self.job)

    def test_checker_initialization(self):
        """Test that checker initializes correctly"""
        self.assertEqual(self.checker.job, self.job)
        self.assertEqual(self.checker.config, self.job.connection_config)

    @patch("requests.get")
    def test_api_connection_success(self, mock_get):
        """Test successful API connection"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "environment": {"wp_version": "6.0"},
            "database": {"wc_version": "8.0"},
        }
        mock_get.return_value = mock_response

        result = self.checker.check_api_connection()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["name"], "API Connection")
        self.assertIn("Successfully connected", result["message"])

    @patch("requests.get")
    def test_api_connection_auth_failure(self, mock_get):
        """Test API connection with authentication failure"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result = self.checker.check_api_connection()

        self.assertEqual(result["status"], "critical")
        self.assertIn("Authentication failed", result["message"])

    @patch("requests.get")
    def test_api_connection_not_found(self, mock_get):
        """Test API connection when WooCommerce is not installed"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.checker.check_api_connection()

        self.assertEqual(result["status"], "critical")
        self.assertIn("not found", result["message"])

    @patch("requests.get")
    def test_api_connection_timeout(self, mock_get):
        """Test API connection timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()

        result = self.checker.check_api_connection()

        self.assertEqual(result["status"], "warning")
        self.assertIn("timed out", result["message"])

    @patch("requests.get")
    def test_api_connection_error(self, mock_get):
        """Test API connection error"""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        result = self.checker.check_api_connection()

        self.assertEqual(result["status"], "critical")
        self.assertIn("Could not connect", result["message"])

    @patch("requests.get")
    def test_api_permissions_all_accessible(self, mock_get):
        """Test API permissions when all endpoints are accessible"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.checker.check_api_permissions()

        self.assertEqual(result["status"], "success")
        self.assertIn("all required endpoints", result["message"])

    @patch("requests.get")
    def test_api_permissions_limited_access(self, mock_get):
        """Test API permissions with limited access"""
        # First call succeeds, others fail
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200

        mock_response_fail = MagicMock()
        mock_response_fail.status_code = 403

        mock_get.side_effect = [
            mock_response_success,  # products
            mock_response_fail,  # customers
            mock_response_fail,  # orders
            mock_response_fail,  # categories
        ]

        result = self.checker.check_api_permissions()

        self.assertEqual(result["status"], "warning")
        self.assertIn("limited access", result["message"])

    @patch("psutil.disk_usage")
    def test_disk_space_sufficient(self, mock_disk_usage):
        """Test disk space check with sufficient space"""
        mock_usage = MagicMock()
        mock_usage.free = 100 * 1024**3  # 100 GB free
        mock_usage.percent = 20.0
        mock_disk_usage.return_value = mock_usage

        result = self.checker.check_disk_space()

        self.assertEqual(result["status"], "success")
        self.assertIn("Sufficient disk space", result["message"])

    @patch("psutil.disk_usage")
    def test_disk_space_limited(self, mock_disk_usage):
        """Test disk space check with limited space"""
        mock_usage = MagicMock()
        mock_usage.free = 10 * 1024**3  # 10 GB free (borderline)
        mock_usage.percent = 80.0
        mock_disk_usage.return_value = mock_usage

        result = self.checker.check_disk_space()

        self.assertEqual(result["status"], "warning")
        self.assertIn("Limited disk space", result["message"])

    @patch("psutil.disk_usage")
    def test_disk_space_insufficient(self, mock_disk_usage):
        """Test disk space check with insufficient space"""
        mock_usage = MagicMock()
        mock_usage.free = 1 * 1024**3  # 1 GB free (too low)
        mock_usage.percent = 95.0
        mock_disk_usage.return_value = mock_usage

        result = self.checker.check_disk_space()

        self.assertEqual(result["status"], "critical")
        self.assertIn("Insufficient disk space", result["message"])

    def test_database_connection_success(self):
        """Test database connection check"""
        result = self.checker.check_database()

        self.assertEqual(result["status"], "success")
        self.assertIn("Database connection successful", result["message"])

    @patch("requests.head")
    def test_estimate_duration(self, mock_head):
        """Test duration estimation"""
        mock_response = MagicMock()
        mock_response.headers = {"X-WP-Total": "500"}
        mock_head.return_value = mock_response

        result = self.checker.estimate_duration()

        self.assertEqual(result["status"], "info")
        self.assertIn("500 products", result["message"])
        self.assertIn("estimated_products", result["details"])
        self.assertEqual(result["details"]["estimated_products"], 500)

    def test_run_all_checks_structure(self):
        """Test that run_all_checks returns proper structure"""
        with patch("requests.get") as mock_get, patch("psutil.disk_usage") as mock_disk:
            # Mock successful responses
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            mock_usage = MagicMock()
            mock_usage.free = 100 * 1024**3
            mock_usage.percent = 20.0
            mock_disk.return_value = mock_usage

            results = self.checker.run_all_checks()

            # Check structure
            self.assertIn("critical_failures", results)
            self.assertIn("warnings", results)
            self.assertIn("info", results)
            self.assertIn("all_passed", results)

            # Check types
            self.assertIsInstance(results["critical_failures"], list)
            self.assertIsInstance(results["warnings"], list)
            self.assertIsInstance(results["info"], list)
            self.assertIsInstance(results["all_passed"], bool)

    def test_run_all_checks_with_failures(self):
        """Test that critical failures set all_passed to False"""
        with patch("requests.get") as mock_get:
            # Mock 401 authentication failure
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            results = self.checker.run_all_checks()

            # Should have critical failures
            self.assertGreater(len(results["critical_failures"]), 0)
            self.assertFalse(results["all_passed"])


class PreFlightCheckerCSVTest(TestCase):
    """Test pre-flight checks for CSV imports"""

    def setUp(self):
        """Set up CSV import job"""
        self.user = User.objects.create_user("test", "test@test.com", "password")

        self.job = MigrationJob.objects.create(
            created_by=self.user, platform="woocommerce", method="csv", connection_config={}
        )

        self.checker = PreFlightChecker(self.job)

    def test_csv_checks_skip_api(self):
        """Test that CSV imports skip API checks"""
        results = self.checker.run_all_checks()

        # Should only check disk and database, not API
        all_check_names = [
            check["name"]
            for check in results["critical_failures"] + results["warnings"] + results["info"]
        ]

        self.assertNotIn("API Connection", all_check_names)
        self.assertNotIn("API Permissions", all_check_names)
