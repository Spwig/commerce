"""
Test Celery configuration and task execution
"""
from django.test import TestCase
from core.celery import app as celery_app, debug_task
from migration.tasks import run_migration_job, rollback_migration_task, cleanup_old_jobs


class CeleryConfigTest(TestCase):
    """Test Celery configuration"""

    def test_celery_app_configured(self):
        """Test that Celery app is properly configured"""
        self.assertIsNotNone(celery_app)
        self.assertEqual(celery_app.main, 'shop')

    def test_celery_settings(self):
        """Test that Celery settings are loaded"""
        # Check broker URL is configured
        self.assertIsNotNone(celery_app.conf.broker_url)
        self.assertIn('redis://', celery_app.conf.broker_url)

        # Check result backend
        self.assertIsNotNone(celery_app.conf.result_backend)

        # Check serialization
        self.assertEqual(celery_app.conf.task_serializer, 'json')
        self.assertEqual(celery_app.conf.result_serializer, 'json')
        self.assertIn('json', celery_app.conf.accept_content)

        # Check time limits
        self.assertEqual(celery_app.conf.task_time_limit, 30 * 60)
        self.assertEqual(celery_app.conf.task_soft_time_limit, 25 * 60)

    def test_debug_task_registered(self):
        """Test that debug task is registered"""
        self.assertIn('core.celery.debug_task', celery_app.tasks)

    def test_migration_tasks_registered(self):
        """Test that migration tasks are registered"""
        # Check tasks are registered
        self.assertIn('migration.run_migration_job', celery_app.tasks)
        self.assertIn('migration.rollback_migration', celery_app.tasks)
        self.assertIn('migration.cleanup_old_jobs', celery_app.tasks)

    def test_migration_task_has_generous_time_limit(self):
        """Migration task needs extended time for large imports"""
        self.assertEqual(run_migration_job.soft_time_limit, 14400)  # 4 hours
        self.assertEqual(run_migration_job.time_limit, 14700)  # 4h 5min


class CeleryTaskExecutionTest(TestCase):
    """Test Celery task execution (requires Celery worker running)"""

    def test_debug_task_synchronous(self):
        """Test debug task execution synchronously"""
        # Execute task synchronously (no worker needed)
        result = debug_task.apply()
        self.assertTrue(result.successful())

    # Note: The following tests require a running Celery worker
    # Run with: celery -A core worker -l info
    #
    # def test_debug_task_async(self):
    #     """Test debug task execution asynchronously"""
    #     result = debug_task.delay()
    #     self.assertIsNotNone(result.id)
    #
    # def test_migration_task_structure(self):
    #     """Test migration task can be called (structure test)"""
    #     from migration.models import MigrationJob
    #     from django.contrib.auth.models import User
    #
    #     # Create test user
    #     user = User.objects.create_user('test', 'test@test.com', 'password')
    #
    #     # Create test job
    #     job = MigrationJob.objects.create(
    #         created_by=user,
    #         platform='woocommerce',
    #         method='api',
    #         connection_config={}
    #     )
    #
    #     # Task should be callable (won't complete without worker)
    #     result = run_migration_job.delay(str(job.id))
    #     self.assertIsNotNone(result.id)
