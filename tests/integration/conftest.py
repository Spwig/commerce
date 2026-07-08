"""
Integration test fixtures — API client setup.
"""
import pytest
from django.test import Client
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Unauthenticated API client."""
    return APIClient()


@pytest.fixture
def auth_client(customer_user):
    """Authenticated API client for customer_user."""
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client


@pytest.fixture
def admin_client(admin_user):
    """Authenticated API client for admin_user."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def customer_client(customer_user):
    """Django test client authenticated as customer_user (for view tests, not API)."""
    client = Client()
    client.force_login(customer_user)
    return client
