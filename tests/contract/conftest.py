"""
Contract test fixtures and utilities
"""
import pytest
import json
from pathlib import Path
from typing import Dict, Any
from rest_framework.test import APIClient


# Schema baseline directory
SCHEMA_DIR = Path(__file__).parent / "schemas"


@pytest.fixture
def contract_client(db):
    """API client for contract testing"""
    client = APIClient()
    return client


@pytest.fixture
def auth_contract_client(db, customer_user):
    """Authenticated API client for contract testing"""
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client


@pytest.fixture
def admin_contract_client(db, admin_user):
    """Admin API client for contract testing"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


def load_schema_baseline(api_module: str, serializer_name: str, version: str = "v1") -> Dict[str, Any]:
    """
    Load baseline schema from version-controlled JSON file

    Args:
        api_module: Module name (e.g., 'catalog', 'cart')
        serializer_name: Serializer class name (e.g., 'ProductListSerializer')
        version: API version (default: 'v1')

    Returns:
        Dict containing the baseline schema

    Raises:
        FileNotFoundError: If baseline schema file doesn't exist
    """
    schema_path = SCHEMA_DIR / api_module / version / f"{serializer_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(
            f"Baseline schema not found: {schema_path}\n"
            f"Run: python scripts/generate_contract_baselines.py --module {api_module} "
            f"--serializer {serializer_name}"
        )

    with open(schema_path, 'r') as f:
        return json.load(f)


def save_schema_baseline(
    api_module: str,
    serializer_name: str,
    schema: Dict[str, Any],
    version: str = "v1"
):
    """
    Save schema as baseline (only run when updating contracts)

    Args:
        api_module: Module name (e.g., 'catalog', 'cart')
        serializer_name: Serializer class name
        schema: Schema dict to save
        version: API version (default: 'v1')
    """
    schema_dir = SCHEMA_DIR / api_module / version
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_path = schema_dir / f"{serializer_name}.json"
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2, sort_keys=True)
