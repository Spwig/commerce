"""
Form Builder Integration Tests.

Comprehensive tests covering:
- Admin views: change list, AJAX filters, recycle bin
- Visual builder views: create, save, field/step/rule/action CRUD
- API endpoints: form detail, submit, partial save, file upload
- Admin actions: duplicate, export, reorder
- Security: staff_member_required, AJAX header validation
- Template CSP compliance: no inline styles
"""
import json
import re
from pathlib import Path
from unittest.mock import patch

import pytest
from django.contrib.admin.sites import AdminSite
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from form_builder.models import (
    Form,
    FormStep,
    FormField,
    FormResponse,
    FormConditionalRule,
    FormAction,
)
from form_builder.admin import FormAdmin
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.form_builder]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(autouse=True)
def _setup_site(site_settings):
    """Ensure SiteSettings exists for all tests (required by admin templates)."""
    return site_settings


@pytest.fixture
def admin_user(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username='fb_test_admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'fb_admin@test.com'},
    )
    user.set_password('testpass123')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def regular_user(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username='fb_regular_user',
        defaults={'email': 'fb_regular@test.com'},
    )
    return user


@pytest.fixture
def staff_client(admin_user):
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def anon_client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_api_client(regular_user):
    client = APIClient()
    client.force_authenticate(user=regular_user)
    return client


@pytest.fixture
def admin_api_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def form(db):
    return Form.objects.create(
        name='Contact Form',
        slug='contact-form',
        title='Contact Us',
        description='Get in touch',
        is_active=True,
    )


@pytest.fixture
def form_with_fields(form):
    step = FormStep.objects.create(form=form, title='Main', order=0)
    FormField.objects.create(
        form=form, step=step, field_name='name',
        field_type='text', label='Name', is_required=True, order=0,
    )
    FormField.objects.create(
        form=form, step=step, field_name='email',
        field_type='email', label='Email', is_required=True, order=1,
    )
    FormField.objects.create(
        form=form, step=step, field_name='message',
        field_type='textarea', label='Message', is_required=False, order=2,
    )
    return form


@pytest.fixture
def login_required_form(db):
    return Form.objects.create(
        name='Members Form',
        slug='members-form',
        title='Members Only',
        is_active=True,
        require_login=True,
    )


@pytest.fixture
def multi_step_form(db):
    form = Form.objects.create(
        name='Survey',
        slug='survey',
        title='Survey',
        is_active=True,
        is_multi_step=True,
        save_partial_responses=True,
    )
    s1 = FormStep.objects.create(form=form, title='Part 1', order=0)
    s2 = FormStep.objects.create(form=form, title='Part 2', order=1)
    FormField.objects.create(
        form=form, step=s1, field_name='q1',
        field_type='text', label='Question 1', order=0,
    )
    FormField.objects.create(
        form=form, step=s2, field_name='q2',
        field_type='text', label='Question 2', order=0,
    )
    return form


# ============================================================
# Admin Change List Tests
# ============================================================

class TestFormAdminChangeList:
    """Tests for form admin change list page."""

    def test_changelist_loads(self, staff_client):
        resp = staff_client.get('/en/admin/form_builder/form/')
        assert resp.status_code == 200

    def test_changelist_requires_staff(self, anon_client):
        resp = anon_client.get('/en/admin/form_builder/form/')
        assert resp.status_code == 302  # Redirect to login

    def test_changelist_context_has_stats(self, staff_client, form):
        resp = staff_client.get('/en/admin/form_builder/form/')
        assert 'total_forms' in resp.context
        assert 'active_forms' in resp.context
        assert 'total_responses' in resp.context

    def test_changelist_shows_deleted_count(self, staff_client, form, admin_user):
        form.delete(user=admin_user)
        resp = staff_client.get('/en/admin/form_builder/form/')
        assert resp.context.get('deleted_count', 0) == 1


class TestFormAdminAjaxFilter:
    """Tests for AJAX filter endpoint."""

    def test_filter_requires_ajax_header(self, staff_client):
        resp = staff_client.get('/en/admin/form_builder/forms/filter/')
        assert resp.status_code == 400

    def test_filter_requires_staff(self, anon_client):
        resp = anon_client.get(
            '/en/admin/form_builder/forms/filter/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 302

    def test_filter_returns_forms(self, staff_client, form):
        resp = staff_client.get(
            '/en/admin/form_builder/forms/filter/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data['count'] >= 1
        assert 'html' in data

    def test_filter_by_search(self, staff_client, form):
        resp = staff_client.get(
            '/en/admin/form_builder/forms/filter/?search=Contact',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 1

    def test_filter_by_search_no_results(self, staff_client, form):
        resp = staff_client.get(
            '/en/admin/form_builder/forms/filter/?search=NonExistent',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 0

    def test_filter_by_status_active(self, staff_client, form):
        Form.objects.create(name='Inactive', slug='inactive', title='X', is_active=False)
        resp = staff_client.get(
            '/en/admin/form_builder/forms/filter/?status=active',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 1  # Only the active form

    def test_filter_by_multistep(self, staff_client, form, multi_step_form):
        resp = staff_client.get(
            '/en/admin/form_builder/forms/filter/?multistep=multi',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 1  # Only multi-step form

    def test_filter_by_description(self, staff_client, form):
        resp = staff_client.get(
            '/en/admin/form_builder/forms/filter/?search=touch',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = resp.json()
        assert data['count'] == 1  # Matches description "Get in touch"


# ============================================================
# Recycle Bin Tests
# ============================================================

class TestRecycleBin:
    """Tests for the recycle bin view."""

    def test_recycle_bin_loads(self, staff_client):
        resp = staff_client.get('/en/admin/form_builder/forms/recycle-bin/')
        assert resp.status_code == 200

    def test_recycle_bin_requires_staff(self, anon_client):
        resp = anon_client.get('/en/admin/form_builder/forms/recycle-bin/')
        assert resp.status_code == 302

    def test_recycle_bin_shows_deleted_forms(self, staff_client, form, admin_user):
        form.delete(user=admin_user)
        resp = staff_client.get('/en/admin/form_builder/forms/recycle-bin/')
        assert resp.status_code == 200
        assert b'Contact Form' in resp.content

    def test_recycle_bin_empty(self, staff_client):
        resp = staff_client.get('/en/admin/form_builder/forms/recycle-bin/')
        assert resp.status_code == 200
        # Should show empty state

    def test_restore_form(self, staff_client, form, admin_user):
        form.delete(user=admin_user)
        resp = staff_client.post('/en/admin/form_builder/forms/recycle-bin/', {
            'action': 'restore',
            'form_ids': [form.pk],
        })
        assert resp.status_code == 200
        form.refresh_from_db()
        assert form.is_deleted is False

    def test_permanent_delete(self, staff_client, form, admin_user):
        form.delete(user=admin_user)
        pk = form.pk
        resp = staff_client.post('/en/admin/form_builder/forms/recycle-bin/', {
            'action': 'permanent_delete',
            'form_ids': [pk],
        })
        assert resp.status_code == 200
        assert Form.all_objects.filter(pk=pk).count() == 0

    def test_empty_bin(self, staff_client, admin_user):
        f1 = Form.objects.create(name='F1', slug='f1', title='F1')
        f2 = Form.objects.create(name='F2', slug='f2', title='F2')
        f1.delete(user=admin_user)
        f2.delete(user=admin_user)
        resp = staff_client.post('/en/admin/form_builder/forms/recycle-bin/', {
            'action': 'empty_bin',
        })
        assert resp.status_code == 200
        assert Form.all_objects.filter(is_deleted=True).count() == 0


# ============================================================
# Visual Builder Tests
# ============================================================

class TestVisualBuilder:
    """Tests for the visual builder views."""

    def test_create_form_redirects_to_builder(self, staff_client):
        """create_form is GET-only - auto-creates a form and redirects to builder."""
        count_before = Form.objects.count()
        resp = staff_client.get('/en/admin/form_builder/forms/create/')
        assert resp.status_code == 302
        assert Form.objects.count() == count_before + 1

    def test_create_form_rejects_post(self, staff_client):
        resp = staff_client.post('/en/admin/form_builder/forms/create/')
        assert resp.status_code == 405

    def test_visual_builder_loads(self, staff_client, form):
        resp = staff_client.get(f'/en/admin/form_builder/forms/{form.pk}/builder/')
        assert resp.status_code == 200

    def test_visual_builder_requires_staff(self, anon_client, form):
        resp = anon_client.get(f'/en/admin/form_builder/forms/{form.pk}/builder/')
        assert resp.status_code == 302


class TestFieldCRUD:
    """Tests for field CRUD operations in visual builder."""

    def test_add_field(self, staff_client, form):
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form.pk}/builder/fields/add/',
            data=json.dumps({
                'field_type': 'text',
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get('success') is True
        assert data['field']['field_type'] == 'text'
        assert FormField.objects.filter(form=form).count() == 1

    def test_update_field(self, staff_client, form_with_fields):
        field = form_with_fields.fields.first()
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form_with_fields.pk}/builder/fields/{field.pk}/update/',
            data=json.dumps({'label': 'Updated Label'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        field.refresh_from_db()
        assert field.label == 'Updated Label'

    def test_delete_field(self, staff_client, form_with_fields):
        field = form_with_fields.fields.first()
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form_with_fields.pk}/builder/fields/{field.pk}/delete/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert not FormField.objects.filter(pk=field.pk).exists()


class TestStepCRUD:
    """Tests for step CRUD operations."""

    def test_add_step(self, staff_client, form):
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form.pk}/builder/steps/add/',
            data=json.dumps({'title': 'New Step'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert FormStep.objects.filter(form=form, title='New Step').exists()

    def test_delete_step(self, staff_client, multi_step_form):
        step = multi_step_form.steps.first()
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{multi_step_form.pk}/builder/steps/{step.pk}/delete/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert not FormStep.objects.filter(pk=step.pk).exists()


class TestRuleCRUD:
    """Tests for conditional rule CRUD operations."""

    @pytest.fixture
    def form_with_rule_setup(self, form):
        step = FormStep.objects.create(form=form, title='S1', order=0)
        source = FormField.objects.create(
            form=form, step=step, field_name='color',
            field_type='select', label='Color', order=0,
        )
        target = FormField.objects.create(
            form=form, step=step, field_name='details',
            field_type='text', label='Details', order=1,
        )
        return form, source, target

    def test_list_rules(self, staff_client, form_with_rule_setup):
        form, source, target = form_with_rule_setup
        FormConditionalRule.objects.create(
            form=form, source_field=source, operator='equals',
            value={'value': 'red'}, action='show_field', target_field=target,
        )
        resp = staff_client.get(
            f'/en/admin/form_builder/forms/{form.pk}/builder/rules/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data.get('rules', [])) == 1

    def test_add_rule(self, staff_client, form_with_rule_setup):
        form, source, target = form_with_rule_setup
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form.pk}/builder/rules/add/',
            data=json.dumps({
                'source_field_id': source.pk,
                'operator': 'equals',
                'value': {'value': 'blue'},
                'action': 'show_field',
                'target_field_id': target.pk,
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert FormConditionalRule.objects.filter(form=form).count() == 1

    def test_delete_rule(self, staff_client, form_with_rule_setup):
        form, source, target = form_with_rule_setup
        rule = FormConditionalRule.objects.create(
            form=form, source_field=source, operator='equals',
            value={'value': 'x'}, action='show_field', target_field=target,
        )
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form.pk}/builder/rules/{rule.pk}/delete/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert not FormConditionalRule.objects.filter(pk=rule.pk).exists()


class TestActionCRUD:
    """Tests for form action CRUD operations."""

    def test_list_actions(self, staff_client, form):
        FormAction.objects.create(
            form=form, action_type='email_notification',
            name='Notify', config={'to_emails': ['a@b.com']},
        )
        resp = staff_client.get(
            f'/en/admin/form_builder/forms/{form.pk}/builder/actions/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data.get('actions', [])) == 1

    def test_add_action(self, staff_client, form):
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form.pk}/builder/actions/add/',
            data=json.dumps({
                'action_type': 'webhook',
                'name': 'Send Webhook',
                'config': {'url': 'https://example.com/hook'},
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert FormAction.objects.filter(form=form, name='Send Webhook').exists()

    def test_delete_action(self, staff_client, form):
        action = FormAction.objects.create(
            form=form, action_type='webhook', name='Test',
        )
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form.pk}/builder/actions/{action.pk}/delete/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200
        assert not FormAction.objects.filter(pk=action.pk).exists()


# ============================================================
# Form Admin Actions Tests
# ============================================================

class TestFormAdminActions:
    """Tests for form admin actions (duplicate, export, reorder)."""

    def test_duplicate_form(self, staff_client, form_with_fields):
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form_with_fields.pk}/duplicate/'
        )
        assert resp.status_code == 302
        assert Form.objects.filter(name__contains='Copy').exists()
        copy = Form.objects.get(name__contains='Copy')
        assert copy.fields.count() == form_with_fields.fields.count()
        assert copy.is_active is False  # Copy starts inactive

    def test_duplicate_requires_post(self, staff_client, form):
        resp = staff_client.get(f'/en/admin/form_builder/forms/{form.pk}/duplicate/')
        assert resp.status_code == 405

    def test_export_responses(self, staff_client, form_with_fields):
        FormResponse.objects.create(
            form=form_with_fields,
            data={'name': 'John', 'email': 'john@test.com', 'message': 'Hi'},
            status='completed',
            submitted_at=timezone.now(),
        )
        resp = staff_client.get(
            f'/en/admin/form_builder/responses/{form_with_fields.pk}/export/'
        )
        assert resp.status_code == 200
        assert resp['Content-Type'] == 'text/csv'

    def test_reorder_fields(self, staff_client, form_with_fields):
        fields = list(form_with_fields.fields.all().order_by('order'))
        # Reverse order
        new_order = [f.pk for f in reversed(fields)]
        resp = staff_client.post(
            f'/en/admin/form_builder/forms/{form_with_fields.pk}/fields/reorder/',
            data=json.dumps({'field_ids': new_order}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        assert resp.status_code == 200


# ============================================================
# API Tests: Form Detail
# ============================================================

class TestFormDetailAPI:
    """Tests for GET /api/form-builder/forms/<slug>/"""

    def test_get_form_detail(self, api_client, form_with_fields):
        resp = api_client.get(f'/api/form-builder/forms/{form_with_fields.slug}/')
        assert resp.status_code == 200
        data = resp.json()
        assert data['slug'] == 'contact-form'
        assert data['title'] == 'Contact Us'
        assert len(data['fields']) == 3

    def test_inactive_form_returns_404(self, api_client):
        Form.objects.create(name='X', slug='x', title='X', is_active=False)
        resp = api_client.get('/api/form-builder/forms/x/')
        assert resp.status_code == 404

    def test_login_required_form_unauthenticated(self, api_client, login_required_form):
        resp = api_client.get(f'/api/form-builder/forms/{login_required_form.slug}/')
        assert resp.status_code == 401

    def test_login_required_form_authenticated(self, auth_api_client, login_required_form):
        resp = auth_api_client.get(f'/api/form-builder/forms/{login_required_form.slug}/')
        assert resp.status_code == 200

    def test_form_detail_includes_fields(self, api_client, form_with_fields):
        resp = api_client.get(f'/api/form-builder/forms/{form_with_fields.slug}/')
        data = resp.json()
        field_names = [f['field_name'] for f in data['fields']]
        assert 'name' in field_names
        assert 'email' in field_names
        assert 'message' in field_names

    def test_form_detail_includes_validation(self, api_client, form_with_fields):
        resp = api_client.get(f'/api/form-builder/forms/{form_with_fields.slug}/')
        data = resp.json()
        name_field = next(f for f in data['fields'] if f['field_name'] == 'name')
        assert name_field['is_required'] is True

    def test_multi_step_form_includes_steps(self, api_client, multi_step_form):
        resp = api_client.get(f'/api/form-builder/forms/{multi_step_form.slug}/')
        data = resp.json()
        assert data['is_multi_step'] is True
        assert len(data['steps']) == 2

    def test_form_detail_includes_conditional_rules(self, api_client, form_with_fields):
        source = form_with_fields.fields.first()
        target = form_with_fields.fields.last()
        FormConditionalRule.objects.create(
            form=form_with_fields, source_field=source, operator='equals',
            value={'value': 'test'}, action='show_field', target_field=target,
        )
        resp = api_client.get(f'/api/form-builder/forms/{form_with_fields.slug}/')
        data = resp.json()
        assert len(data['rules']) == 1


# ============================================================
# API Tests: Form Submit
# ============================================================

class TestFormSubmitAPI:
    """Tests for POST /api/form-builder/forms/<slug>/submit/"""

    def test_submit_form(self, api_client, form_with_fields):
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_fields.slug}/submit/',
            data={'name': 'Jane', 'email': 'jane@test.com', 'message': 'Hello'},
            format='json',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        assert data['response_id'] is not None
        assert FormResponse.objects.filter(form=form_with_fields).count() == 1

    def test_submit_missing_required_field(self, api_client, form_with_fields):
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_fields.slug}/submit/',
            data={'message': 'Hello'},  # Missing required name and email
            format='json',
        )
        assert resp.status_code == 400
        data = resp.json()
        assert 'name' in data['errors']
        assert 'email' in data['errors']

    def test_submit_inactive_form_404(self, api_client):
        Form.objects.create(name='Dead', slug='dead', title='Dead', is_active=False)
        resp = api_client.post(
            '/api/form-builder/forms/dead/submit/',
            data={},
            format='json',
        )
        assert resp.status_code == 404

    def test_submit_login_required_unauthenticated(self, api_client, login_required_form):
        resp = api_client.post(
            f'/api/form-builder/forms/{login_required_form.slug}/submit/',
            data={},
            format='json',
        )
        assert resp.status_code == 401

    @patch('form_builder.tasks.execute_form_actions')
    def test_submit_triggers_actions(self, mock_task, api_client, form_with_fields):
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_fields.slug}/submit/',
            data={'name': 'Jane', 'email': 'j@t.com'},
            format='json',
        )
        assert resp.status_code == 200
        mock_task.delay.assert_called_once()

    def test_submit_records_metadata(self, api_client, form_with_fields):
        api_client.post(
            f'/api/form-builder/forms/{form_with_fields.slug}/submit/',
            data={'name': 'Jane', 'email': 'j@t.com'},
            format='json',
            HTTP_USER_AGENT='TestBot/1.0',
        )
        response = FormResponse.objects.first()
        assert response.user_agent == 'TestBot/1.0'
        assert response.status == 'completed'
        assert response.submitted_at is not None


# ============================================================
# API Tests: Save Partial Response
# ============================================================

class TestSavePartialAPI:
    """Tests for POST /api/form-builder/forms/<slug>/partial/"""

    def test_save_partial(self, api_client, multi_step_form):
        resp = api_client.post(
            f'/api/form-builder/forms/{multi_step_form.slug}/partial/',
            data={'current_step': 1, 'data': {'q1': 'answer 1'}},
            format='json',
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        assert data['response_id'] is not None

    def test_update_partial(self, api_client, multi_step_form):
        # Create initial partial
        resp1 = api_client.post(
            f'/api/form-builder/forms/{multi_step_form.slug}/partial/',
            data={'current_step': 1, 'data': {'q1': 'answer 1'}},
            format='json',
        )
        response_id = resp1.json()['response_id']

        # Update it
        resp2 = api_client.post(
            f'/api/form-builder/forms/{multi_step_form.slug}/partial/',
            data={
                'response_id': response_id,
                'current_step': 2,
                'data': {'q2': 'answer 2'},
            },
            format='json',
        )
        assert resp2.status_code == 200
        response = FormResponse.objects.get(pk=response_id)
        assert response.current_step == 2
        assert 'q2' in response.data

    def test_partial_disabled_form(self, api_client, form_with_fields):
        """Form without save_partial_responses returns error."""
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_fields.slug}/partial/',
            data={'current_step': 1, 'data': {}},
            format='json',
        )
        assert resp.status_code == 400


# ============================================================
# API Tests: File Upload
# ============================================================

class TestFileUploadAPI:
    """Tests for POST /api/form-builder/forms/<slug>/upload/"""

    @pytest.fixture
    def form_with_file_field(self, form):
        step = FormStep.objects.create(form=form, title='Files', order=0)
        FormField.objects.create(
            form=form, step=step, field_name='attachment',
            field_type='file', label='Attachment', order=0,
            file_config={'max_size_mb': 1, 'allowed_types': ['pdf', 'jpg']},
        )
        return form

    def test_upload_no_file(self, api_client, form_with_file_field):
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_file_field.slug}/upload/',
            data={'field_name': 'attachment'},
        )
        assert resp.status_code == 400

    def test_upload_invalid_field(self, api_client, form_with_file_field):
        from django.core.files.uploadedfile import SimpleUploadedFile
        f = SimpleUploadedFile('test.pdf', b'%PDF-1.4', content_type='application/pdf')
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_file_field.slug}/upload/',
            data={'field_name': 'nonexistent', 'file': f},
            format='multipart',
        )
        assert resp.status_code == 400

    def test_upload_disallowed_type(self, api_client, form_with_file_field):
        from django.core.files.uploadedfile import SimpleUploadedFile
        f = SimpleUploadedFile('test.exe', b'\x00\x01', content_type='application/octet-stream')
        resp = api_client.post(
            f'/api/form-builder/forms/{form_with_file_field.slug}/upload/',
            data={'field_name': 'attachment', 'file': f},
            format='multipart',
        )
        assert resp.status_code == 400
        assert 'not allowed' in resp.json()['error']


# ============================================================
# API Tests: Form List for Selector
# ============================================================

class TestFormListForSelectorAPI:
    """Tests for GET /api/form-builder/forms/list/ (admin only)."""

    def test_list_requires_admin(self, api_client):
        resp = api_client.get('/api/form-builder/forms/list/')
        assert resp.status_code in (401, 403)

    def test_list_returns_active_forms(self, admin_api_client, form):
        resp = admin_api_client.get('/api/form-builder/forms/list/')
        assert resp.status_code == 200
        data = resp.json()
        assert len(data['forms']) >= 1
        assert 'create_url' in data

    def test_list_excludes_inactive(self, admin_api_client, form):
        Form.objects.create(name='Dead', slug='dead', title='Dead', is_active=False)
        resp = admin_api_client.get('/api/form-builder/forms/list/')
        slugs = [f['slug'] for f in resp.json()['forms']]
        assert 'dead' not in slugs


# ============================================================
# Template CSP Compliance Tests
# ============================================================

class TestCSPCompliance:
    """Verify no inline styles remain in admin templates."""

    ADMIN_TEMPLATES = [
        'form_builder/templates/admin/form_builder/form/change_list.html',
        'form_builder/templates/admin/form_builder/form/change_form.html',
        'form_builder/templates/admin/form_builder/form/recycle_bin.html',
        'form_builder/templates/admin/form_builder/formresponse/change_list.html',
        'form_builder/templates/admin/form_builder/formresponse/change_form.html',
    ]

    STOREFRONT_TEMPLATES = [
        'form_builder/templates/form_builder/form_render.html',
        'form_builder/templates/form_builder/fields/field.html',
    ]

    def _check_no_inline_styles(self, filepath):
        full_path = PROJECT_ROOT / filepath
        if not full_path.exists():
            pytest.skip(f'{filepath} does not exist')
        content = full_path.read_text()
        # Check for style="" attributes (excluding CSS custom properties like --star-color)
        style_attrs = re.findall(r'style="[^"]*"', content)
        # Filter out dynamic CSS custom properties which are acceptable
        violations = [s for s in style_attrs if '--' not in s]
        assert violations == [], f'Inline styles found in {filepath}: {violations}'

    def _check_no_style_tags(self, filepath):
        full_path = PROJECT_ROOT / filepath
        if not full_path.exists():
            pytest.skip(f'{filepath} does not exist')
        content = full_path.read_text()
        assert '<style' not in content, f'<style> tag found in {filepath}'

    @pytest.mark.parametrize('template', ADMIN_TEMPLATES)
    def test_admin_no_inline_styles(self, template):
        self._check_no_inline_styles(template)

    @pytest.mark.parametrize('template', ADMIN_TEMPLATES)
    def test_admin_no_style_tags(self, template):
        self._check_no_style_tags(template)

    @pytest.mark.parametrize('template', STOREFRONT_TEMPLATES)
    def test_storefront_no_inline_styles(self, template):
        self._check_no_inline_styles(template)


# ============================================================
# Admin Soft Delete Integration Tests
# ============================================================

class TestAdminSoftDelete:
    """Tests for soft delete integration in FormAdmin."""

    def test_delete_model_uses_soft_delete(self, admin_user):
        form = Form.objects.create(name='To Delete', slug='to-delete', title='X')
        site = AdminSite()
        admin_obj = FormAdmin(Form, site)
        request = RequestFactory().post('/')
        request.user = admin_user

        admin_obj.delete_model(request, form)

        form.refresh_from_db()
        assert form.is_deleted is True
        assert form.deleted_by == admin_user

    def test_delete_queryset_uses_soft_delete(self, admin_user):
        f1 = Form.objects.create(name='F1', slug='f1', title='F1')
        f2 = Form.objects.create(name='F2', slug='f2', title='F2')
        site = AdminSite()
        admin_obj = FormAdmin(Form, site)
        request = RequestFactory().post('/')
        request.user = admin_user

        admin_obj.delete_queryset(request, Form.objects.all())

        assert Form.objects.count() == 0  # Default manager excludes deleted
        assert Form.all_objects.filter(is_deleted=True).count() == 2


# ============================================================
# Form Actions Execution Tests
# ============================================================

class TestFormActionsExecution:
    """Tests for form action execution."""

    @patch('form_builder.actions.email.EmailMultiAlternatives')
    def test_email_notification_action(self, MockEmail, form_with_fields):
        mock_msg = MockEmail.return_value
        mock_msg.send.return_value = 1

        action = FormAction.objects.create(
            form=form_with_fields,
            action_type='email_notification',
            name='Notify',
            config={
                'to_emails': ['admin@test.com'],
                'subject_template': 'New submission',
                'body_template': 'Form submitted.',
                'include_data': True,
            },
        )

        response = FormResponse.objects.create(
            form=form_with_fields,
            data={'name': 'Test', 'email': 'test@test.com'},
            status='completed',
        )

        from form_builder.actions.email import EmailNotificationAction
        executor = EmailNotificationAction(action, response)
        result = executor.execute()
        assert result['status'] == 'sent'
        assert result['recipients'] == ['admin@test.com']

    @patch('form_builder.actions.webhook.requests')
    def test_webhook_action(self, mock_requests, form_with_fields):
        mock_response = mock_requests.request.return_value
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.text = 'OK'

        action = FormAction.objects.create(
            form=form_with_fields,
            action_type='webhook',
            name='Hook',
            config={
                'url': 'https://example.com/hook',
                'method': 'POST',
            },
        )

        response = FormResponse.objects.create(
            form=form_with_fields,
            data={'name': 'Test'},
            status='completed',
        )

        from form_builder.actions.webhook import WebhookAction
        executor = WebhookAction(action, response)
        result = executor.execute()
        assert result['status'] == 'sent'
        assert result['http_status'] == 200
        mock_requests.request.assert_called_once()


# ============================================================
# i18n Tests
# ============================================================

class TestI18nCompliance:
    """Verify all model verbose_name fields use gettext_lazy."""

    def test_form_verbose_names(self):
        meta = Form._meta
        assert str(meta.verbose_name) == 'Form'
        assert str(meta.verbose_name_plural) == 'Forms'

    def test_formstep_verbose_names(self):
        meta = FormStep._meta
        assert str(meta.verbose_name) == 'Form Step'

    def test_formfield_verbose_names(self):
        meta = FormField._meta
        assert str(meta.verbose_name) == 'Form Field'

    def test_formresponse_verbose_names(self):
        meta = FormResponse._meta
        assert str(meta.verbose_name) == 'Form Response'

    def test_formconditionalrule_verbose_names(self):
        meta = FormConditionalRule._meta
        assert str(meta.verbose_name) == 'Conditional Rule'

    def test_formaction_verbose_names(self):
        meta = FormAction._meta
        assert str(meta.verbose_name) == 'Form Action'
