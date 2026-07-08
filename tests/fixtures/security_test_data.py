"""
Shared Security Test Data Fixtures
API-based test data factory for security scenarios
Used by both functional tests and pentest scanner
"""

import random
import string
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import requests


@dataclass
class SecurityTestAccount:
    """Test account for security testing"""
    email: str
    password: str
    first_name: str
    last_name: str
    csrf_token: Optional[str] = None
    session_cookie: Optional[str] = None


@dataclass
class SecurityTestProduct:
    """Test product for security testing"""
    id: int
    slug: str
    name: str
    price: str
    sku: str


class SecurityTestDataFactory:
    """Factory for creating security test data via API"""

    def __init__(self, base_url: str, admin_email: str = "admin@example.com", admin_password: str = "admin123"):
        """
        Initialize test data factory

        Args:
            base_url: Base URL of the shop (e.g., http://localhost:8000)
            admin_email: Admin account email
            admin_password: Admin account password
        """
        self.base_url = base_url.rstrip('/')
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.session = requests.Session()

    def _random_string(self, length: int = 10) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _random_email(self) -> str:
        """Generate random email"""
        return f"test_{self._random_string(8)}@example.com"

    def _get_csrf_token(self, url: str) -> Optional[str]:
        """Extract CSRF token from a page"""
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                # Try to find CSRF token in cookies
                csrf_token = self.session.cookies.get('csrftoken')
                if csrf_token:
                    return csrf_token

                # Try to find in HTML
                import re
                match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.text)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return None

    def create_test_account(
        self,
        email: Optional[str] = None,
        password: str = "TestPass123!",
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> SecurityTestAccount:
        """
        Create a test customer account via API

        Args:
            email: Account email (random if not provided)
            password: Account password
            first_name: First name (random if not provided)
            last_name: Last name (random if not provided)

        Returns:
            SecurityTestAccount with credentials
        """
        email = email or self._random_email()
        first_name = first_name or f"Test{self._random_string(5)}"
        last_name = last_name or f"User{self._random_string(5)}"

        # Get CSRF token from signup page
        signup_url = f"{self.base_url}/en/accounts/signup/"
        csrf_token = self._get_csrf_token(signup_url)

        # Create account via signup API
        data = {
            'email': email,
            'password1': password,
            'password2': password,
            'first_name': first_name,
            'last_name': last_name,
            'csrfmiddlewaretoken': csrf_token,
        }

        response = self.session.post(
            signup_url,
            data=data,
            headers={'Referer': signup_url},
            allow_redirects=False,
        )

        # Account created successfully if redirected
        if response.status_code in (200, 302):
            session_cookie = self.session.cookies.get('sessionid')
            return SecurityTestAccount(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                csrf_token=csrf_token,
                session_cookie=session_cookie,
            )

        raise Exception(f"Failed to create account: {response.status_code}")

    def create_sql_injection_payloads(self) -> List[str]:
        """
        Generate SQL injection test payloads

        Returns:
            List of SQL injection strings to test
        """
        return [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin' --",
            "admin' #",
            "admin'/*",
            "' OR 1=1--",
            "') OR ('1'='1",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL, NULL--",
            "1' AND '1'='1",
            "1' AND '1'='2",
            "' AND 1=0 UNION ALL SELECT '', '', '', '', '', '', ''--",
            # Time-based blind
            "' OR SLEEP(5)--",
            "'; WAITFOR DELAY '00:00:05'--",
            # Boolean-based blind
            "' AND (SELECT COUNT(*) FROM auth_user) > 0--",
        ]

    def create_xss_payloads(self) -> List[str]:
        """
        Generate XSS test payloads

        Returns:
            List of XSS strings to test
        """
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<body onload=alert('XSS')>",
            "<input type='text' value='XSS' onfocus='alert(document.cookie)'>",
            "<details open ontoggle=alert('XSS')>",
            # Encoded
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            # DOM-based
            "#<img src=x onerror=alert('XSS')>",
            # Event handlers
            "' autofocus onfocus=alert('XSS') '",
            # Template injection
            "{{constructor.constructor('alert(1)')()}}",
            "${alert('XSS')}",
        ]

    def create_path_traversal_payloads(self) -> List[str]:
        """
        Generate path traversal test payloads

        Returns:
            List of path traversal strings to test
        """
        return [
            "../",
            "../../",
            "../../../",
            "../../../../etc/passwd",
            "..\\..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            # Null byte injection
            "../../../etc/passwd%00",
            # URL encoded
            "..%252f..%252f..%252fetc%252fpasswd",
        ]

    def create_auth_bypass_payloads(self) -> List[Dict[str, str]]:
        """
        Generate authentication bypass test credentials

        Returns:
            List of credential dictionaries to test
        """
        return [
            # SQL injection in username
            {'email': "admin' OR '1'='1' --", 'password': 'anything'},
            {'email': "admin'/*", 'password': 'anything'},
            # Empty/null password
            {'email': 'admin@example.com', 'password': ''},
            # Special characters
            {'email': 'admin@example.com', 'password': '\''},
            {'email': 'admin@example.com', 'password': '\"'},
            # Boolean bypass
            {'email': 'admin@example.com', 'password': '1\' OR \'1\'=\'1'},
            # Unicode bypass
            {'email': 'admin@example.com', 'password': '\u0000'},
        ]

    def create_idor_test_ids(self) -> List[Any]:
        """
        Generate IDOR (Insecure Direct Object Reference) test IDs

        Returns:
            List of IDs to test for IDOR vulnerabilities
        """
        return [
            # Sequential IDs
            1, 2, 3, 100, 999, 1000,
            # Negative IDs
            -1, -2, -100,
            # Large IDs
            999999, 9999999,
            # String IDs (if UUIDs)
            '00000000-0000-0000-0000-000000000001',
            'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            # SQL injection in ID
            "1' OR '1'='1",
            # Path traversal in ID
            '../1',
            # Null/empty
            '', None, 'null', 'undefined',
        ]

    def create_csrf_bypass_attempts(self) -> List[Dict[str, Any]]:
        """
        Generate CSRF bypass test scenarios

        Returns:
            List of CSRF bypass scenarios to test
        """
        return [
            # No CSRF token
            {'csrf_token': None},
            # Empty CSRF token
            {'csrf_token': ''},
            # Invalid CSRF token
            {'csrf_token': 'invalid_token_12345'},
            # Reused CSRF token from different session
            {'csrf_token': 'reused_csrf_token', 'reused': True},
            # Null byte in token
            {'csrf_token': 'token\x00'},
        ]

    def create_rate_limit_test_config(self, endpoint: str) -> Dict[str, Any]:
        """
        Generate rate limit testing configuration

        Args:
            endpoint: API endpoint to test

        Returns:
            Rate limit test configuration
        """
        return {
            'endpoint': endpoint,
            'requests_per_minute': 100,  # Expected limit
            'test_requests': 150,  # Requests to send
            'concurrent_requests': 10,  # Parallel requests
            'expected_429_after': 100,  # Expect 429 after this many requests
        }

    def create_payment_manipulation_payloads(self) -> List[Dict[str, Any]]:
        """
        Generate payment amount manipulation test payloads

        Returns:
            List of payment manipulation scenarios
        """
        return [
            # Negative amounts
            {'amount': -100},
            {'amount': -0.01},
            # Zero amount
            {'amount': 0},
            # Very small amounts
            {'amount': 0.01},
            # Very large amounts
            {'amount': 999999999.99},
            # Overflow attempts
            {'amount': 2147483647},  # Max 32-bit int
            # String manipulation
            {'amount': '1.00', 'tampered_amount': '0.01'},
            # Currency mismatch
            {'amount': 100, 'currency': 'USD', 'tampered_currency': 'EUR'},
            # Precision attacks
            {'amount': 1.001},
            {'amount': 1.999999},
        ]

    def create_file_upload_payloads(self) -> List[Dict[str, Any]]:
        """
        Generate malicious file upload test payloads

        Returns:
            List of file upload scenarios
        """
        return [
            # PHP webshell
            {
                'filename': 'shell.php',
                'content': '<?php system($_GET["cmd"]); ?>',
                'mime': 'application/x-php',
            },
            # HTML with JavaScript
            {
                'filename': 'xss.html',
                'content': '<script>alert("XSS")</script>',
                'mime': 'text/html',
            },
            # SVG with JavaScript
            {
                'filename': 'xss.svg',
                'content': '<svg onload="alert(\'XSS\')"></svg>',
                'mime': 'image/svg+xml',
            },
            # Double extension
            {
                'filename': 'image.jpg.php',
                'content': '<?php phpinfo(); ?>',
                'mime': 'image/jpeg',
            },
            # Null byte injection
            {
                'filename': 'image.php\x00.jpg',
                'content': '<?php phpinfo(); ?>',
                'mime': 'image/jpeg',
            },
            # MIME type mismatch
            {
                'filename': 'image.jpg',
                'content': '<?php phpinfo(); ?>',
                'mime': 'image/jpeg',
            },
            # Oversized file (DOS)
            {
                'filename': 'huge.jpg',
                'content': 'A' * (100 * 1024 * 1024),  # 100MB
                'mime': 'image/jpeg',
            },
            # Path traversal in filename
            {
                'filename': '../../../etc/passwd',
                'content': 'test',
                'mime': 'text/plain',
            },
        ]

    def cleanup_test_account(self, account: SecurityTestAccount) -> bool:
        """
        Clean up a test account

        Args:
            account: SecurityTestAccount to delete

        Returns:
            True if cleanup successful
        """
        try:
            # In a real implementation, this would call an admin API to delete the account
            # For now, we just clear the session
            self.session.cookies.clear()
            return True
        except Exception:
            return False


# Singleton instance for easy import
_factory_instance: Optional[SecurityTestDataFactory] = None


def get_security_test_factory(base_url: str = "http://localhost:8000") -> SecurityTestDataFactory:
    """
    Get or create singleton SecurityTestDataFactory instance

    Args:
        base_url: Base URL of the shop

    Returns:
        SecurityTestDataFactory instance
    """
    global _factory_instance
    if _factory_instance is None or _factory_instance.base_url != base_url:
        _factory_instance = SecurityTestDataFactory(base_url)
    return _factory_instance
