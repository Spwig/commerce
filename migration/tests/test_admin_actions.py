"""
Regression tests for the migration wizard's state-changing admin actions.

`delete_migration`, `cancel_migration` and `retry_migration` used to be plain
GET links rendered into the changelist. Any authenticated staff member could
be made to destroy a migration record by loading an image tag, and a crawler
or link prefetcher could do it by accident. They are now POST-only, CSRF
protected, and gated on the model's admin permissions.

The tests below are written so that a regression is caught by a *state*
assertion, not only by a status code: a handler that returned 405 while still
mutating the row would pass a status-only test. Every rejection path therefore
re-reads the job from the database and asserts it is untouched.
"""

from datetime import timedelta
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from migration.models import MigrationJob, MigrationLog, MigrationStep
from migration.tasks import MIGRATION_HARD_TIME_LIMIT

# Length of an unmasked CSRF secret. Used only as a sanity check on the token
# the admin hands out, so that a future change which starts returning an empty
# or truncated cookie fails loudly here rather than quietly turning every
# "POST with CSRF" test into a "POST without CSRF" test that still passes.
_CSRF_SECRET_LENGTH = 32


class MigrationAdminActionTestCase(TestCase):
    """Shared fixtures for the three action endpoints."""

    def setUp(self):
        # Role/read-only decisions are cached in the process-wide cache, which
        # (unlike the DB) isn't rolled back between tests — clear it so a pk
        # reused across tests doesn't inherit a stale access decision.
        from django.core.cache import cache

        cache.clear()

        # The currency middleware calls SiteSettings.get_settings(), which
        # get_or_create(pk=1)s and then full_clean()s on save. Without a row
        # carrying a non-blank admin_email every request in this module would
        # 500 on {'admin_email': ['This field cannot be blank.']} — an
        # unrelated failure that would mask whatever we are actually testing.
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "Test Store",
                "admin_email": "admin@test.spwig.invalid",
                "default_currency": "USD",
                "default_language": "en",
            },
        )

        from django.contrib.sites.models import Site

        Site.objects.get_or_create(id=1, defaults={"domain": "testserver", "name": "Test Site"})

        self.superuser = User.objects.create_superuser(
            "test-superuser", "superuser@test.spwig.invalid", "not-a-real-password"
        )

        # Staff, can reach the admin at all, but holds no migration
        # permissions. This is the user the permission gate must stop.
        #
        # Under deny-by-default (AdminAccessMiddleware + AdminReadOnlyMiddleware)
        # a role-less staff user is redirected off the admin and blocked from
        # every write, which would stop these POSTs before the per-model
        # permission gate we're actually testing ever runs. Give them a role
        # that grants admin access and write (so they reach the gate) but that
        # carries no migration permissions — the gate must still stop them until
        # the specific migration perm is granted per-test.
        from django.contrib.auth.models import Group

        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        self.staff_without_perms = User.objects.create_user(
            "test-staff-noperms",
            "staff@test.spwig.invalid",
            "not-a-real-password",
            is_staff=True,
        )
        admin_access_group = Group.objects.create(name="test-admin-access-nomigration")
        StaffRole.objects.create(
            group=admin_access_group,
            display_name="Admin Access (no migration perms)",
            can_access_admin=True,
            permission_categories={"orders": "full"},
        )
        self.staff_without_perms.groups.add(admin_access_group)
        invalidate_user_cache(self.staff_without_perms)

        self.owner = User.objects.create_user(
            "test-job-owner", "owner@test.spwig.invalid", "not-a-real-password"
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def make_job(self, status="failed", **overrides):
        """Create a MigrationJob. `created_by`, `platform`, `method` are required."""
        fields = {
            "created_by": self.owner,
            "platform": "woocommerce",
            "method": "api",
            "status": status,
            "connection_config": {
                "store_url": "https://example.invalid",
                "consumer_key": "placeholder-key",
                "consumer_secret": "placeholder-secret",
            },
        }
        fields.update(overrides)
        return MigrationJob.objects.create(**fields)

    def csrf_client(self, user):
        """
        Return a CSRF-enforcing client logged in as `user`, plus a valid token.

        The token is taken from the cookie the admin index hands out, so these
        tests exercise the same handshake a browser performs rather than
        reaching into Django's CSRF internals.
        """
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        client.get(reverse("admin:index"))
        cookie = client.cookies.get("csrftoken")
        self.assertIsNotNone(
            cookie,
            "admin index did not set a csrftoken cookie; the CSRF tests below "
            "would silently degrade into 'posting without a token'",
        )
        token = cookie.value
        self.assertGreaterEqual(len(token), _CSRF_SECRET_LENGTH)
        return client, token

    def post_with_csrf(self, user, url, data=None):
        client, token = self.csrf_client(user)
        payload = {"csrfmiddlewaretoken": token}
        if data:
            payload.update(data)
        return client.post(url, payload, HTTP_X_CSRFTOKEN=token)

    def snapshot(self, job):
        """Fields the three actions would mutate, for non-mutation assertions."""
        return {
            "status": job.status,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "duration_seconds": job.duration_seconds,
            "progress_percent": job.progress_percent,
            "error_summary": job.error_summary,
            "current_step": job.current_step,
        }

    def assert_unchanged(self, job, before, msg=""):
        """Re-read the job and assert nothing an action touches has moved."""
        exists = MigrationJob.objects.filter(pk=job.pk).exists()
        self.assertTrue(exists, f"job was deleted {msg}".strip())
        job.refresh_from_db()
        self.assertEqual(self.snapshot(job), before, f"job was mutated {msg}".strip())


class ActionUrlShapeTests(MigrationAdminActionTestCase):
    """The action URLs live inside i18n_patterns, so they carry a lang prefix."""

    def test_action_urls_are_language_prefixed_under_admin(self):
        job = self.make_job()
        for name, suffix in (
            ("admin:migration_job_delete", "delete"),
            ("admin:migration_job_cancel", "cancel"),
            ("admin:migration_job_retry", "retry"),
        ):
            with self.subTest(action=name):
                url = reverse(name, args=[job.pk])
                self.assertEqual(url, f"/en/admin/migration/migrationjob/{job.pk}/{suffix}/")


class GetRequestIsRejectedTests(MigrationAdminActionTestCase):
    """
    The actual regression: these endpoints used to *perform the action* on GET.

    Status code alone is not enough — assert the job survived untouched.
    """

    def test_delete_rejects_get_and_does_not_delete(self):
        job = self.make_job(status="failed")
        url = reverse("admin:migration_job_delete", args=[job.pk])
        before = self.snapshot(job)

        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        self.assertIn("POST", response["Allow"])
        self.assert_unchanged(job, before, "by a GET to delete_migration")

    def test_cancel_rejects_get_and_does_not_cancel(self):
        job = self.make_job(status="running", started_at=timezone.now())
        url = reverse("admin:migration_job_cancel", args=[job.pk])
        before = self.snapshot(job)

        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        self.assertIn("POST", response["Allow"])
        self.assert_unchanged(job, before, "by a GET to cancel_migration")
        # cancel_migration writes an audit log line; none should exist.
        self.assertEqual(MigrationLog.objects.filter(job=job).count(), 0)

    def test_retry_rejects_get_and_does_not_restart(self):
        job = self.make_job(status="failed", error_summary="original failure")
        MigrationStep.objects.create(job=job, step_type="products", status="failed")
        url = reverse("admin:migration_job_retry", args=[job.pk])
        before = self.snapshot(job)

        self.client.force_login(self.superuser)
        with patch("migration.tasks.run_migration_job") as mock_task:
            response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        self.assertIn("POST", response["Allow"])
        self.assert_unchanged(job, before, "by a GET to retry_migration")
        mock_task.delay.assert_not_called()
        # retry_migration wipes prior steps before restarting; it must not have.
        self.assertEqual(MigrationStep.objects.filter(job=job).count(), 1)


class MissingCsrfTokenIsRejectedTests(MigrationAdminActionTestCase):
    """A POST without a CSRF token is refused and leaves the job alone."""

    def _post_without_token(self, url):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.superuser)
        return client.post(url, {})

    def test_delete_rejects_post_without_csrf_token(self):
        job = self.make_job(status="failed")
        before = self.snapshot(job)

        response = self._post_without_token(reverse("admin:migration_job_delete", args=[job.pk]))

        self.assertEqual(response.status_code, 403)
        self.assert_unchanged(job, before, "by a CSRF-less POST to delete_migration")

    def test_cancel_rejects_post_without_csrf_token(self):
        job = self.make_job(status="running", started_at=timezone.now())
        before = self.snapshot(job)

        response = self._post_without_token(reverse("admin:migration_job_cancel", args=[job.pk]))

        self.assertEqual(response.status_code, 403)
        self.assert_unchanged(job, before, "by a CSRF-less POST to cancel_migration")
        self.assertEqual(MigrationLog.objects.filter(job=job).count(), 0)

    def test_retry_rejects_post_without_csrf_token(self):
        job = self.make_job(status="failed")
        before = self.snapshot(job)

        with patch("migration.tasks.run_migration_job") as mock_task:
            response = self._post_without_token(reverse("admin:migration_job_retry", args=[job.pk]))

        self.assertEqual(response.status_code, 403)
        self.assert_unchanged(job, before, "by a CSRF-less POST to retry_migration")
        mock_task.delay.assert_not_called()


class PermissionGateTests(MigrationAdminActionTestCase):
    """
    Staff access to the admin is not authority over migration records.

    `delete_migration` requires the delete permission; `cancel_migration` and
    `retry_migration` require change. A staff user with neither is refused,
    and each test also proves the *matching* permission is what unblocks it —
    otherwise a handler that ignored permissions entirely would still pass the
    positive cases in the other classes.
    """

    def grant(self, user, codename):
        user.user_permissions.add(
            Permission.objects.get(codename=codename, content_type__app_label="migration")
        )
        # Permissions are cached on the user object for the life of a request;
        # re-fetch so the next login sees the new grant.
        return User.objects.get(pk=user.pk)

    def test_delete_denied_for_staff_without_delete_permission(self):
        job = self.make_job(status="failed")
        before = self.snapshot(job)

        response = self.post_with_csrf(
            self.staff_without_perms,
            reverse("admin:migration_job_delete", args=[job.pk]),
        )

        self.assertIn(response.status_code, (302, 403))
        if response.status_code == 302:
            self.assertIn("login", response["Location"])
        self.assert_unchanged(job, before, "by an unprivileged delete_migration POST")

    def test_delete_allowed_once_delete_permission_granted(self):
        job = self.make_job(status="failed")
        user = self.grant(self.staff_without_perms, "delete_migrationjob")

        response = self.post_with_csrf(user, reverse("admin:migration_job_delete", args=[job.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(MigrationJob.objects.filter(pk=job.pk).exists())

    def test_cancel_denied_for_staff_without_change_permission(self):
        job = self.make_job(status="running", started_at=timezone.now())
        before = self.snapshot(job)

        response = self.post_with_csrf(
            self.staff_without_perms,
            reverse("admin:migration_job_cancel", args=[job.pk]),
        )

        self.assertIn(response.status_code, (302, 403))
        self.assert_unchanged(job, before, "by an unprivileged cancel_migration POST")
        self.assertEqual(MigrationLog.objects.filter(job=job).count(), 0)

    def test_cancel_allowed_once_change_permission_granted(self):
        job = self.make_job(status="running", started_at=timezone.now())
        user = self.grant(self.staff_without_perms, "change_migrationjob")

        response = self.post_with_csrf(user, reverse("admin:migration_job_cancel", args=[job.pk]))

        self.assertEqual(response.status_code, 302)
        job.refresh_from_db()
        # Cancellation is cooperative: the request is recorded, and the worker
        # writes the terminal status when it stops.
        self.assertTrue(job.cancel_requested)

    def test_retry_denied_for_staff_without_change_permission(self):
        job = self.make_job(status="failed")
        before = self.snapshot(job)

        with patch("migration.tasks.run_migration_job") as mock_task:
            response = self.post_with_csrf(
                self.staff_without_perms,
                reverse("admin:migration_job_retry", args=[job.pk]),
            )

        self.assertIn(response.status_code, (302, 403))
        self.assert_unchanged(job, before, "by an unprivileged retry_migration POST")
        mock_task.delay.assert_not_called()

    def test_retry_allowed_once_change_permission_granted(self):
        job = self.make_job(status="failed")
        user = self.grant(self.staff_without_perms, "change_migrationjob")

        with patch("migration.tasks.run_migration_job") as mock_task:
            mock_task.delay.return_value = MagicMock(id="placeholder-task-id")
            response = self.post_with_csrf(
                user, reverse("admin:migration_job_retry", args=[job.pk])
            )

        self.assertEqual(response.status_code, 302)
        job.refresh_from_db()
        self.assertEqual(job.status, "running")

    def test_delete_permission_does_not_authorise_cancel(self):
        """Delete rights must not be read as change rights."""
        job = self.make_job(status="running", started_at=timezone.now())
        user = self.grant(self.staff_without_perms, "delete_migrationjob")
        before = self.snapshot(job)

        response = self.post_with_csrf(user, reverse("admin:migration_job_cancel", args=[job.pk]))

        self.assertIn(response.status_code, (302, 403))
        self.assert_unchanged(job, before, "by a delete-only user calling cancel")

    def test_change_permission_does_not_authorise_delete(self):
        """Change rights must not be read as delete rights."""
        job = self.make_job(status="failed")
        user = self.grant(self.staff_without_perms, "change_migrationjob")
        before = self.snapshot(job)

        response = self.post_with_csrf(user, reverse("admin:migration_job_delete", args=[job.pk]))

        self.assertIn(response.status_code, (302, 403))
        self.assert_unchanged(job, before, "by a change-only user calling delete")


class DeleteMigrationStateGuardTests(MigrationAdminActionTestCase):
    """
    Which jobs `delete_migration` will and will not remove.

    Two independent reasons a job may be undeletable:

    * a `running` job may still have a live Celery worker holding it, and
      because the PK carries a default, Django turns an UPDATE matching zero
      rows into an INSERT — so the worker's next save() would re-create the
      row we just deleted, as "completed" and with no provenance;
    * a `completed` job is the anchor rollback reads to know what the import
      created. Deleting it severs that link permanently.

    A `running` job is refused *regardless of age*. Elapsed time cannot be
    used to infer that the worker is dead, because `started_at` is stamped
    when the task is enqueued rather than when it begins executing, so a queue
    backlog makes a live job look expired. The operator path out of a stuck
    `running` job is cancel-then-delete, which the refusal message names and
    `test_cancel_then_delete_is_the_documented_escape_hatch` exercises.
    """

    def url(self, job):
        return reverse("admin:migration_job_delete", args=[job.pk])

    def test_refuses_running_job_started_recently(self):
        job = self.make_job(status="running", started_at=timezone.now() - timedelta(minutes=5))
        before = self.snapshot(job)

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assert_unchanged(job, before, "— a live running job was deleted")

    def test_refuses_running_job_far_older_than_celery_hard_time_limit(self):
        """
        Age is not an escape hatch.

        A job whose `started_at` long predates Celery's hard `time_limit` looks
        abandoned, but the enqueue-vs-execute gap means it may not be. The
        threshold is derived from the real task constant rather than a literal
        so this test tracks the limit if it is ever retuned.
        """
        long_dead = timedelta(seconds=MIGRATION_HARD_TIME_LIMIT) * 10
        job = self.make_job(status="running", started_at=timezone.now() - long_dead)
        before = self.snapshot(job)

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assert_unchanged(
            job, before, "— an apparently-abandoned running job was deleted on age alone"
        )

    def test_refuses_running_job_with_no_started_at(self):
        job = self.make_job(status="running", started_at=None)
        before = self.snapshot(job)

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assert_unchanged(job, before, "— a running job with no start time was deleted")

    def test_cancel_then_delete_is_the_documented_escape_hatch(self):
        """
        The refusal message tells the operator to cancel first. That route must
        actually work, or a stuck job would be permanently undeletable.

        Under cooperative cancellation it takes two beats: the request is
        recorded, and the job only becomes deletable once the worker has
        acknowledged it by writing "cancelled". That ordering is deliberate —
        deleting while the worker is alive lets its next save re-INSERT the row,
        because the primary key carries a default.
        """
        job = self.make_job(status="running", started_at=timezone.now())

        refused = self.post_with_csrf(self.superuser, self.url(job))
        self.assertEqual(refused.status_code, 302)
        self.assertTrue(MigrationJob.objects.filter(pk=job.pk).exists())

        cancelled = self.post_with_csrf(
            self.superuser, reverse("admin:migration_job_cancel", args=[job.pk])
        )
        self.assertEqual(cancelled.status_code, 302)
        job.refresh_from_db()
        self.assertTrue(job.cancel_requested)

        # Still not deletable: the worker has not stopped yet.
        still_refused = self.post_with_csrf(self.superuser, self.url(job))
        self.assertEqual(still_refused.status_code, 302)
        self.assertTrue(
            MigrationJob.objects.filter(pk=job.pk).exists(),
            "a job whose worker may still be writing must not be deletable",
        )

        # The worker acknowledges the stop (or the reaper does, if it died).
        MigrationJob.objects.filter(pk=job.pk).update(status="cancelled")

        deleted = self.post_with_csrf(self.superuser, self.url(job))
        self.assertEqual(deleted.status_code, 302)
        self.assertFalse(MigrationJob.objects.filter(pk=job.pk).exists())

    def test_refuses_completed_job(self):
        """Completed jobs are the provenance anchor for rollback."""
        job = self.make_job(
            status="completed",
            started_at=timezone.now() - timedelta(hours=2),
            completed_at=timezone.now() - timedelta(hours=1),
            products_imported=42,
            products_total=42,
        )
        before = self.snapshot(job)

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assert_unchanged(job, before, "— a completed job was deleted")

    def test_refuses_rolled_back_job(self):
        job = self.make_job(status="rolled_back")
        before = self.snapshot(job)

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assert_unchanged(job, before, "— a rolled_back job was deleted")

    def test_deletes_failed_job(self):
        job = self.make_job(status="failed", error_summary="import blew up")
        MigrationStep.objects.create(job=job, step_type="products", status="failed")
        MigrationLog.objects.create(
            job=job, level="error", message="boom", source_type="system", source_id="x"
        )

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(MigrationJob.objects.filter(pk=job.pk).exists())
        # Steps and logs cascade with the job record.
        self.assertEqual(MigrationStep.objects.filter(job_id=job.pk).count(), 0)
        self.assertEqual(MigrationLog.objects.filter(job_id=job.pk).count(), 0)

    def test_deletes_pending_job(self):
        job = self.make_job(status="pending")

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(MigrationJob.objects.filter(pk=job.pk).exists())


class CancelMigrationStateGuardTests(MigrationAdminActionTestCase):
    """`cancel_migration` acts on `running` jobs and nothing else."""

    def url(self, job):
        return reverse("admin:migration_job_cancel", args=[job.pk])

    def test_cancels_running_job(self):
        """Cancel records the request; the worker is what stops.

        Cancellation is cooperative. The admin sets cancel_requested and leaves
        the status alone — the executor writes "cancelled" once it has actually
        unwound at its next batch boundary. Asserting the status flipped here
        would be asserting the old cosmetic behaviour, where the dashboard
        claimed the import had stopped while it kept writing for hours.
        """
        started = timezone.now() - timedelta(minutes=10)
        job = self.make_job(status="running", started_at=started)

        response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        job.refresh_from_db()
        self.assertTrue(job.cancel_requested, "the stop request must be recorded")
        self.assertEqual(
            job.status,
            "running",
            "status stays running until the worker acknowledges the stop",
        )
        # An audit line naming the operator is written.
        logs = MigrationLog.objects.filter(job=job)
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].level, "warning")
        self.assertIn(self.superuser.username, logs[0].message)

    def test_does_not_cancel_non_running_jobs(self):
        for status in ("pending", "completed", "failed", "rolled_back", "paused"):
            with self.subTest(status=status):
                job = self.make_job(status=status)
                before = self.snapshot(job)

                response = self.post_with_csrf(self.superuser, self.url(job))

                self.assertEqual(response.status_code, 302)
                self.assert_unchanged(job, before, f"— cancel acted on a {status} job")
                self.assertEqual(MigrationLog.objects.filter(job=job).count(), 0)


class RetryMigrationStateGuardTests(MigrationAdminActionTestCase):
    """`retry_migration` acts on `failed` jobs and nothing else."""

    def url(self, job):
        return reverse("admin:migration_job_retry", args=[job.pk])

    def test_retries_failed_job(self):
        job = self.make_job(
            status="failed",
            error_summary="import blew up",
            progress_percent=63,
            current_step="products",
            completed_at=timezone.now(),
            duration_seconds=120,
            products_imported=7,
            products_failed=3,
        )
        MigrationStep.objects.create(job=job, step_type="products", status="failed")
        MigrationLog.objects.create(
            job=job, level="error", message="boom", source_type="system", source_id="x"
        )

        with patch("migration.tasks.run_migration_job") as mock_task:
            mock_task.delay.return_value = MagicMock(id="placeholder-task-id")
            response = self.post_with_csrf(self.superuser, self.url(job))

        self.assertEqual(response.status_code, 302)
        mock_task.delay.assert_called_once_with(str(job.pk))

        job.refresh_from_db()
        self.assertEqual(job.status, "running")
        self.assertIsNotNone(job.started_at)
        self.assertIsNone(job.completed_at)
        self.assertIsNone(job.duration_seconds)
        self.assertEqual(job.progress_percent, 0)
        self.assertEqual(job.current_step, "")
        self.assertEqual(job.error_summary, "")
        # Counters from the failed attempt are reset.
        self.assertEqual(job.products_imported, 0)
        self.assertEqual(job.products_failed, 0)
        # Prior steps and logs are cleared so the rerun starts clean.
        self.assertEqual(MigrationStep.objects.filter(job=job).count(), 0)
        self.assertEqual(MigrationLog.objects.filter(job=job).count(), 0)
        self.assertEqual(job.connection_config["celery_task_id"], "placeholder-task-id")

    def test_does_not_retry_non_failed_jobs(self):
        for status in ("pending", "running", "completed", "rolled_back", "paused"):
            with self.subTest(status=status):
                job = self.make_job(
                    status=status,
                    started_at=timezone.now() if status == "running" else None,
                )
                MigrationStep.objects.create(job=job, step_type="products", status="completed")
                before = self.snapshot(job)

                with patch("migration.tasks.run_migration_job") as mock_task:
                    response = self.post_with_csrf(self.superuser, self.url(job))

                self.assertEqual(response.status_code, 302)
                self.assert_unchanged(job, before, f"— retry acted on a {status} job")
                mock_task.delay.assert_not_called()
                # The step-wipe must not have run either.
                self.assertEqual(MigrationStep.objects.filter(job=job).count(), 1)
