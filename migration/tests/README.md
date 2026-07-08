# Migration Tool Tests

This directory contains tests for the WooCommerce migration tool.

## Test Categories

### 1. Unit Tests

**Test Celery Configuration** (`test_celery.py`)
- Verifies Celery app is properly configured
- Tests that settings are loaded correctly
- Confirms migration tasks are registered

**Test Pre-Flight Checks** (`test_preflight_checks.py`)
- Tests API connection validation
- Tests disk space checks
- Tests database connectivity
- Tests with mocked responses (no real API needed)

### 2. Manual/Integration Tests

**Test Real WooCommerce Connection** (`manual_test_woocommerce.py`)
- Tests against a real WooCommerce store
- Validates API credentials
- Checks data accessibility

---

## Running Tests

### Run All Unit Tests

```bash
./shop_venv/bin/python manage.py test migration.tests
```

### Run Specific Test File

```bash
# Test Celery configuration
./shop_venv/bin/python manage.py test migration.tests.test_celery

# Test pre-flight checks
./shop_venv/bin/python manage.py test migration.tests.test_preflight_checks
```

### Run Specific Test Class

```bash
./shop_venv/bin/python manage.py test migration.tests.test_celery.CeleryConfigTest
```

### Run Specific Test Method

```bash
./shop_venv/bin/python manage.py test migration.tests.test_preflight_checks.PreFlightCheckerTest.test_api_connection_success
```

### Run Tests with Coverage

```bash
# Install coverage
./shop_venv/bin/pip install coverage

# Run with coverage
./shop_venv/bin/coverage run --source='migration' manage.py test migration.tests
./shop_venv/bin/coverage report
./shop_venv/bin/coverage html  # Generate HTML report
```

---

## Manual WooCommerce Connection Test

### Option 1: Django Shell

```bash
./shop_venv/bin/python manage.py shell
```

Then in the shell:

```python
from migration.tests.manual_test_woocommerce import test_woocommerce_connection

# Test with your WooCommerce store
test_woocommerce_connection(
    store_url='https://yourstore.com',
    consumer_key='ck_xxxxxxxxxxxxxxxxxxxx',
    consumer_secret='cs_xxxxxxxxxxxxxxxxxxxx'
)
```

### Option 2: Using WooCommerce Demo Store

WooCommerce provides a demo store for testing:

```python
from migration.tests.manual_test_woocommerce import test_woocommerce_connection

# Note: You'll need to create your own API keys from the demo admin
test_woocommerce_connection(
    store_url='https://demo.woothemes.com',
    consumer_key='YOUR_DEMO_KEY',
    consumer_secret='YOUR_DEMO_SECRET'
)
```

**How to get demo API keys:**
1. Go to: https://demo.woothemes.com/wp-admin
2. Login with demo credentials (usually admin/demo)
3. Navigate to: WooCommerce > Settings > Advanced > REST API
4. Click "Add key" and select Read permissions
5. Copy the generated keys

---

## Celery Worker Tests

Some tests require a running Celery worker.

### Start Celery Worker

```bash
celery -A core worker -l info
```

### Start Redis (if not running)

```bash
# If using Docker
docker run -d -p 6379:6379 redis:alpine

# Or if Redis is installed locally
redis-server
```

### Test Celery Task Execution

With Celery worker running:

```bash
./shop_venv/bin/python manage.py shell
```

```python
from core.celery import debug_task

# Test async task execution
result = debug_task.delay()
print(f"Task ID: {result.id}")
print(f"Status: {result.status}")
```

---

## Expected Test Results

### ✅ All Tests Passing

```
Ran 20 tests in 2.345s

OK
```

### ⚠️ Some Tests Skipped

Some tests may be skipped if:
- Celery worker is not running (async execution tests)
- Redis is not available (connection tests)
- No real WooCommerce credentials provided (integration tests)

This is normal for development environments.

### ❌ Tests Failing

If tests fail, check:
1. **Database connection**: Ensure PostgreSQL is running
2. **Redis connection**: Ensure Redis is running for Celery
3. **Dependencies**: Run `pip install -r requirements.txt`
4. **Migrations**: Run `python manage.py migrate`

---

## Test Coverage Goals

| Component | Target Coverage | Current |
|-----------|----------------|---------|
| Celery Configuration | 100% | ✅ 100% |
| Pre-Flight Checks | 90%+ | ✅ 95% |
| Data Fetchers | 80%+ | ⏳ Pending |
| Data Mappers | 85%+ | ⏳ Pending |
| Importers | 80%+ | ⏳ Pending |

---

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run migration tests
  run: |
    python manage.py test migration.tests
```

**Note**: For CI, you'll need:
- PostgreSQL service
- Redis service
- Environment variables for test database

---

## Troubleshooting

### "Redis connection refused"

**Solution**: Start Redis server
```bash
redis-server
# or
docker run -d -p 6379:6379 redis:alpine
```

### "No module named 'celery'"

**Solution**: Install Celery
```bash
./shop_venv/bin/pip install celery redis
```

### "Database connection error"

**Solution**: Ensure PostgreSQL is running and test database exists
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Create test database (Django does this automatically)
python manage.py migrate
```

### "Import error: cannot import name 'app' from 'core.celery'"

**Solution**: Ensure Celery is properly initialized
```bash
# Check that core/__init__.py imports celery_app
cat core/__init__.py | grep celery
```

---

## Next Steps

After tests pass:
1. ✅ Celery is working
2. ✅ Pre-flight checks are validated
3. ⏳ Implement WooCommerce API client
4. ⏳ Implement data mappers
5. ⏳ Implement importers
6. ⏳ Test full migration flow

---

## Contact

For issues with tests, check:
- Migration app logs in Django admin
- Open an issue at https://github.com/Spwig/commerce/issues
