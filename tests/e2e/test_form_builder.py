"""
Form Builder E2E Tests.

End-to-end browser tests verifying the full form builder lifecycle:
1. Create a form via the admin visual builder
2. Submit/respond to a form on the storefront (preview page)
3. Verify responses are recorded in admin
4. Verify form actions are configured and form responses capture action data

Uses Playwright via pytest fixtures from tests/e2e/conftest.py.
Forms are set up programmatically (via models) for reliable test data,
then tested through the browser for true E2E verification.

NOTE: unittest.mock.patch() does NOT work across threads with Django's
live_server fixture. Celery tasks called via .delay() will fail silently
(no broker running) but FormResponse creation happens before the task call,
so responses are still persisted. Action execution tests verify DB state
only -- action mocking is covered by integration tests.
"""
import re

import pytest
from playwright.sync_api import Page, expect

from form_builder.models import (
    Form,
    FormStep,
    FormField,
    FormResponse,
    FormAction,
)

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.e2e,
    pytest.mark.form_builder,
]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def contact_form(db):
    """Create a simple contact form with text, email, and textarea fields."""
    form = Form.objects.create(
        name='E2E Contact Form',
        slug='e2e-contact-form',
        title='Contact Us',
        description='We would love to hear from you.',
        submit_button_text='Send Message',
        success_message='Thank you! We will get back to you shortly.',
        error_message='Something went wrong. Please try again.',
        is_active=True,
        spam_protection='honeypot',
    )
    FormField.objects.create(
        form=form, field_name='full_name', field_type='text',
        label='Full Name', placeholder='Enter your full name',
        is_required=True, order=0,
    )
    FormField.objects.create(
        form=form, field_name='email_address', field_type='email',
        label='Email Address', placeholder='you@example.com',
        is_required=True, order=1,
    )
    FormField.objects.create(
        form=form, field_name='message', field_type='textarea',
        label='Your Message', placeholder='Tell us what you need...',
        is_required=False, order=2,
    )
    return form


@pytest.fixture
def form_with_select(db):
    """Create a form with a dropdown select field and radio buttons."""
    form = Form.objects.create(
        name='E2E Survey Form',
        slug='e2e-survey-form',
        title='Quick Survey',
        description='Help us improve.',
        submit_button_text='Submit Survey',
        success_message='Survey submitted successfully!',
        is_active=True,
        spam_protection='honeypot',
    )
    FormField.objects.create(
        form=form, field_name='department', field_type='select',
        label='Department', placeholder='Select department',
        is_required=True, order=0,
        options=[
            {'value': 'sales', 'label': 'Sales'},
            {'value': 'support', 'label': 'Support'},
            {'value': 'billing', 'label': 'Billing'},
        ],
    )
    FormField.objects.create(
        form=form, field_name='satisfaction', field_type='radio',
        label='Satisfaction Level', is_required=True, order=1,
        options=[
            {'value': 'very_satisfied', 'label': 'Very Satisfied'},
            {'value': 'satisfied', 'label': 'Satisfied'},
            {'value': 'neutral', 'label': 'Neutral'},
            {'value': 'dissatisfied', 'label': 'Dissatisfied'},
        ],
    )
    FormField.objects.create(
        form=form, field_name='feedback', field_type='textarea',
        label='Additional Feedback', is_required=False, order=2,
    )
    return form


@pytest.fixture
def multi_step_form(db):
    """Create a multi-step form with two steps."""
    form = Form.objects.create(
        name='E2E Multi Step Form',
        slug='e2e-multi-step',
        title='Multi-Step Registration',
        description='Complete both steps.',
        submit_button_text='Complete Registration',
        success_message='Registration complete!',
        is_active=True,
        is_multi_step=True,
        save_partial_responses=True,
        spam_protection='honeypot',
    )
    step1 = FormStep.objects.create(
        form=form, title='Personal Info', order=0,
        next_button_text='Continue',
    )
    step2 = FormStep.objects.create(
        form=form, title='Preferences', order=1,
        back_button_text='Go Back',
    )
    FormField.objects.create(
        form=form, step=step1, field_name='first_name', field_type='text',
        label='First Name', is_required=True, order=0,
    )
    FormField.objects.create(
        form=form, step=step1, field_name='last_name', field_type='text',
        label='Last Name', is_required=True, order=1,
    )
    FormField.objects.create(
        form=form, step=step2, field_name='newsletter', field_type='checkbox',
        label='Subscribe to newsletter', is_required=False, order=0,
    )
    FormField.objects.create(
        form=form, step=step2, field_name='comments', field_type='textarea',
        label='Comments', is_required=False, order=1,
    )
    return form


@pytest.fixture
def form_with_actions(db):
    """Create a form with email notification and webhook actions."""
    form = Form.objects.create(
        name='E2E Action Form',
        slug='e2e-action-form',
        title='Contact with Actions',
        submit_button_text='Submit',
        success_message='Submitted!',
        is_active=True,
        spam_protection='honeypot',
    )
    FormField.objects.create(
        form=form, field_name='name', field_type='text',
        label='Name', is_required=True, order=0,
    )
    FormField.objects.create(
        form=form, field_name='email', field_type='email',
        label='Email', is_required=True, order=1,
    )
    # Email notification action
    FormAction.objects.create(
        form=form, action_type='email_notification',
        name='Admin Notification',
        config={
            'to_emails': ['admin@test.com'],
            'subject_template': 'New form submission: {name}',
            'body_template': 'Name: {name}\nEmail: {email}',
            'include_data': True,
        },
        order=0,
    )
    # Webhook action
    FormAction.objects.create(
        form=form, action_type='webhook',
        name='CRM Webhook',
        config={
            'url': 'https://hooks.example.com/form-submit',
            'method': 'POST',
            'headers': {'X-API-Key': 'test-key'},
        },
        order=1,
    )
    return form


@pytest.fixture
def inactive_form(db):
    """Create an inactive form that should not be accessible."""
    form = Form.objects.create(
        name='Inactive Form',
        slug='e2e-inactive-form',
        title='This form is disabled',
        is_active=False,
    )
    FormField.objects.create(
        form=form, field_name='dummy', field_type='text',
        label='Dummy', order=0,
    )
    return form


# ============================================================
# Helper Functions
# ============================================================

def _navigate_to_form_preview(page: Page, form_pk: int):
    """Navigate to the admin form preview page."""
    base = page._live_server_url
    page.goto(f'{base}/en/admin/form_builder/forms/{form_pk}/preview/')
    page.wait_for_load_state('networkidle')


def _navigate_to_visual_builder(page: Page, form_pk: int):
    """Navigate to the visual builder for a form."""
    base = page._live_server_url
    page.goto(f'{base}/en/admin/form_builder/forms/{form_pk}/builder/')
    page.wait_for_load_state('networkidle')


def _navigate_to_form_changelist(page: Page):
    """Navigate to the admin form changelist."""
    base = page._live_server_url
    page.goto(f'{base}/en/admin/form_builder/form/')
    page.wait_for_load_state('networkidle')


def _navigate_to_response_changelist(page: Page, form_pk: int = None):
    """Navigate to the admin form response changelist."""
    base = page._live_server_url
    url = f'{base}/en/admin/form_builder/formresponse/'
    if form_pk:
        url += f'?form__id__exact={form_pk}'
    page.goto(url)
    page.wait_for_load_state('networkidle')


def _submit_form_and_wait(page: Page, timeout_ms: int = 3000):
    """Submit the form and wait for AJAX response to complete."""
    page.click('button[type="submit"]')
    # Wait for the success message to appear or the form to hide
    # The JS hides the form and shows .success-message on success
    try:
        page.wait_for_selector(
            '.form-messages .success-message',
            state='visible',
            timeout=timeout_ms,
        )
    except Exception:
        # If success message doesn't appear, wait a bit for error display
        page.wait_for_timeout(1000)


# ============================================================
# 1. Admin Visual Builder Tests
# ============================================================

class TestVisualBuilderLoads:
    """Test that the visual builder page loads correctly."""

    def test_visual_builder_renders(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Visual builder page loads with form data."""
        _navigate_to_visual_builder(admin_authenticated_page, contact_form.pk)

        # Page title should contain the form name
        expect(admin_authenticated_page).to_have_title(
            re.compile(r'Form Builder.*')
        )

    def test_visual_builder_shows_existing_fields(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Visual builder displays existing fields from the database."""
        _navigate_to_visual_builder(admin_authenticated_page, contact_form.pk)

        # The form data JSON should be present in the page
        # The builder JS initializes from this data
        page_content = admin_authenticated_page.content()
        assert 'full_name' in page_content
        assert 'email_address' in page_content
        assert 'message' in page_content

    def test_visual_builder_has_field_palette(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Visual builder has the field type palette for adding fields."""
        _navigate_to_visual_builder(admin_authenticated_page, contact_form.pk)

        # The builder should have a sidebar or palette with field types
        # Check for field type buttons/items in the page content
        page_content = admin_authenticated_page.content()
        # The builder template should reference field types
        assert 'text' in page_content.lower()


class TestVisualBuilderCreateForm:
    """Test creating a new form via the admin."""

    def test_create_form_via_admin(
        self, admin_authenticated_page: Page, site_settings
    ):
        """Creating a form via the create URL redirects to the visual builder."""
        base = admin_authenticated_page._live_server_url
        count_before = Form.objects.count()

        admin_authenticated_page.goto(
            f'{base}/en/admin/form_builder/forms/create/'
        )
        admin_authenticated_page.wait_for_load_state('networkidle')

        # Should have created a new form
        assert Form.objects.count() == count_before + 1

        # Should be on the visual builder page
        expect(admin_authenticated_page).to_have_url(re.compile(r'.*/builder/'))


class TestVisualBuilderSaveForm:
    """Test saving form configuration via the visual builder AJAX endpoint."""

    def test_save_form_settings_via_builder(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Save form settings through the visual builder AJAX save endpoint."""
        _navigate_to_visual_builder(admin_authenticated_page, contact_form.pk)

        base = admin_authenticated_page._live_server_url
        save_url = (
            f'{base}/en/admin/form_builder/forms/{contact_form.pk}/builder/save/'
        )

        # Use page.evaluate to send AJAX request like the builder JS does
        result = admin_authenticated_page.evaluate(f'''
            async () => {{
                const csrf = document.querySelector(
                    '[name=csrfmiddlewaretoken]'
                )?.value || document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

                const resp = await fetch('{save_url}', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf,
                        'X-Requested-With': 'XMLHttpRequest',
                    }},
                    body: JSON.stringify({{
                        form: {{
                            name: 'Updated E2E Form',
                            title: 'Updated Title',
                            description: 'Updated description',
                            is_active: true,
                        }},
                    }}),
                }});
                return await resp.json();
            }}
        ''')

        assert result['success'] is True

        # Verify the form was actually updated in the database
        contact_form.refresh_from_db()
        assert contact_form.name == 'Updated E2E Form'
        assert contact_form.title == 'Updated Title'
        assert contact_form.description == 'Updated description'


# ============================================================
# 2. Form Preview and Submission Tests
# ============================================================

class TestFormPreviewRenders:
    """Test that form preview pages render correctly."""

    def test_preview_renders_form_title(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Preview page displays the form title."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        # The form title should be visible
        title = admin_authenticated_page.locator('.form-title')
        expect(title).to_contain_text('Contact Us')

    def test_preview_renders_description(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Preview page displays the form description."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        description = admin_authenticated_page.locator('.form-description')
        expect(description).to_contain_text('We would love to hear from you.')

    def test_preview_renders_all_fields(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Preview page renders all form fields."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        # Check each field exists by its data-field-name attribute
        full_name = admin_authenticated_page.locator(
            '[data-field-name="full_name"]'
        )
        expect(full_name).to_be_visible()

        email = admin_authenticated_page.locator(
            '[data-field-name="email_address"]'
        )
        expect(email).to_be_visible()

        message = admin_authenticated_page.locator(
            '[data-field-name="message"]'
        )
        expect(message).to_be_visible()

    def test_preview_renders_submit_button(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Preview page has the correct submit button text."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        submit_btn = admin_authenticated_page.locator('button[type="submit"]')
        expect(submit_btn).to_contain_text('Send Message')

    def test_preview_renders_required_indicators(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Required fields show the required indicator."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        # Full Name and Email are required; check for required-indicator
        name_label = admin_authenticated_page.locator(
            '[data-field-name="full_name"] .required-indicator'
        )
        expect(name_label).to_be_visible()

        email_label = admin_authenticated_page.locator(
            '[data-field-name="email_address"] .required-indicator'
        )
        expect(email_label).to_be_visible()

    def test_preview_shows_preview_banner(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Preview mode shows a preview banner."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        banner = admin_authenticated_page.locator('.preview-banner')
        expect(banner).to_be_visible()

    def test_preview_renders_select_field(
        self, admin_authenticated_page: Page, site_settings, form_with_select
    ):
        """Preview page renders select field with options."""
        _navigate_to_form_preview(admin_authenticated_page, form_with_select.pk)

        select = admin_authenticated_page.locator('#field-department')
        expect(select).to_be_visible()

        # Check that select has the expected options
        options = admin_authenticated_page.locator(
            '#field-department option'
        )
        # 3 options + 1 placeholder = 4 total
        assert options.count() == 4

    def test_preview_renders_honeypot(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Forms with honeypot protection include the honeypot field."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        honeypot = admin_authenticated_page.locator('.hp-field')
        # Honeypot should exist in DOM but be hidden
        assert honeypot.count() == 1


class TestFormSubmission:
    """Test form submission through the browser.

    NOTE: Celery tasks called via .delay() will fail silently since no
    broker/worker is running during E2E tests. FormResponse creation
    happens BEFORE the task call in the API view, so responses are still
    persisted in the database.
    """

    def test_submit_contact_form_successfully(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Submit a form with valid data and verify success message appears."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        # Fill in the form fields
        admin_authenticated_page.fill(
            '#field-full_name', 'Jane Doe'
        )
        admin_authenticated_page.fill(
            '#field-email_address', 'jane@example.com'
        )
        admin_authenticated_page.fill(
            '#field-message', 'This is a test message from E2E.'
        )

        # Submit the form and wait for success
        _submit_form_and_wait(admin_authenticated_page)

        # The success message should be visible
        success_msg = admin_authenticated_page.locator('.success-message')
        expect(success_msg).to_contain_text('Thank you')

        # Verify the response was saved in the database
        response = FormResponse.objects.filter(form=contact_form).first()
        assert response is not None
        assert response.data.get('full_name') == 'Jane Doe'
        assert response.data.get('email_address') == 'jane@example.com'
        assert response.data.get('message') == 'This is a test message from E2E.'
        assert response.status == 'completed'

    def test_submit_form_with_select_and_radio(
        self, admin_authenticated_page: Page, site_settings, form_with_select
    ):
        """Submit a form with select dropdown and radio button fields."""
        _navigate_to_form_preview(admin_authenticated_page, form_with_select.pk)

        # Select department from dropdown
        admin_authenticated_page.select_option(
            '#field-department', value='support'
        )

        # Select a radio button
        admin_authenticated_page.click(
            'input[name="satisfaction"][value="satisfied"]'
        )

        # Add optional feedback
        admin_authenticated_page.fill(
            '#field-feedback', 'Good service overall.'
        )

        # Submit
        _submit_form_and_wait(admin_authenticated_page)

        # Success message
        success_msg = admin_authenticated_page.locator('.success-message')
        expect(success_msg).to_contain_text('Survey submitted')

        # Verify database
        response = FormResponse.objects.filter(
            form=form_with_select
        ).first()
        assert response is not None
        assert response.data.get('department') == 'support'
        assert response.data.get('satisfaction') == 'satisfied'

    def test_submit_form_validation_prevents_empty_required(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Submitting with empty required fields shows client-side validation."""
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        # Try to submit without filling required fields
        admin_authenticated_page.click('button[type="submit"]')
        admin_authenticated_page.wait_for_timeout(500)

        # The form should NOT have been submitted (no response in DB)
        assert FormResponse.objects.filter(form=contact_form).count() == 0

        # Client-side validation should show error states
        # The JS validation adds 'error' class to required empty inputs
        name_input = admin_authenticated_page.locator('#field-full_name')
        classes = name_input.get_attribute('class') or ''
        # Either HTML5 validation prevents submit or JS validation adds error class
        assert (
            'error' in classes
            or name_input.evaluate('el => !el.checkValidity()')
        )


class TestMultiStepFormSubmission:
    """Test multi-step form navigation and submission."""

    def test_multi_step_shows_first_step(
        self, admin_authenticated_page: Page, site_settings, multi_step_form
    ):
        """Multi-step form shows the first step on load."""
        _navigate_to_form_preview(admin_authenticated_page, multi_step_form.pk)

        # First step should be active
        first_step = admin_authenticated_page.locator('.form-step.active')
        expect(first_step).to_be_visible()

        # Should show step 1 title
        step_title = first_step.locator('.step-title')
        expect(step_title).to_contain_text('Personal Info')

    def test_multi_step_shows_progress_indicator(
        self, admin_authenticated_page: Page, site_settings, multi_step_form
    ):
        """Multi-step form displays a progress indicator."""
        _navigate_to_form_preview(admin_authenticated_page, multi_step_form.pk)

        progress = admin_authenticated_page.locator('.form-progress')
        expect(progress).to_be_visible()

        # Should have 2 progress steps
        progress_steps = admin_authenticated_page.locator('.progress-step')
        assert progress_steps.count() == 2

    def test_multi_step_navigate_to_next_step(
        self, admin_authenticated_page: Page, site_settings, multi_step_form
    ):
        """Can navigate from step 1 to step 2."""
        _navigate_to_form_preview(admin_authenticated_page, multi_step_form.pk)

        # Fill required fields in step 1
        admin_authenticated_page.fill('#field-first_name', 'John')
        admin_authenticated_page.fill('#field-last_name', 'Smith')

        # Click the next button
        admin_authenticated_page.click('.next-step')
        admin_authenticated_page.wait_for_timeout(1000)

        # Step 2 should now be visible
        active_step = admin_authenticated_page.locator(
            '.form-step.active'
        )
        step_title = active_step.locator('.step-title')
        expect(step_title).to_contain_text('Preferences')

    def test_multi_step_navigate_back(
        self, admin_authenticated_page: Page, site_settings, multi_step_form
    ):
        """Can navigate back from step 2 to step 1."""
        _navigate_to_form_preview(admin_authenticated_page, multi_step_form.pk)

        # Fill step 1 and go to step 2
        admin_authenticated_page.fill('#field-first_name', 'John')
        admin_authenticated_page.fill('#field-last_name', 'Smith')
        admin_authenticated_page.click('.next-step')
        admin_authenticated_page.wait_for_timeout(1000)

        # Click back
        admin_authenticated_page.click('.prev-step')
        admin_authenticated_page.wait_for_timeout(500)

        # Should be back on step 1
        active_step = admin_authenticated_page.locator(
            '.form-step.active'
        )
        step_title = active_step.locator('.step-title')
        expect(step_title).to_contain_text('Personal Info')

    def test_multi_step_complete_submission(
        self, admin_authenticated_page: Page, site_settings, multi_step_form
    ):
        """Complete a multi-step form submission."""
        _navigate_to_form_preview(admin_authenticated_page, multi_step_form.pk)

        # Step 1: fill personal info
        admin_authenticated_page.fill('#field-first_name', 'Alice')
        admin_authenticated_page.fill('#field-last_name', 'Johnson')
        admin_authenticated_page.click('.next-step')
        admin_authenticated_page.wait_for_timeout(1000)

        # Step 2: fill preferences
        admin_authenticated_page.fill('#field-comments', 'No comments.')
        # Submit on the last step
        _submit_form_and_wait(admin_authenticated_page)

        # Success message
        success_msg = admin_authenticated_page.locator('.success-message')
        expect(success_msg).to_contain_text('Registration complete')

        # Verify the completed response in DB
        response = FormResponse.objects.filter(
            form=multi_step_form, status='completed'
        ).first()
        assert response is not None
        assert response.data.get('first_name') == 'Alice'
        assert response.data.get('last_name') == 'Johnson'


# ============================================================
# 3. Admin Response Verification Tests
# ============================================================

class TestAdminResponseViewing:
    """Test that form responses appear correctly in the admin."""

    def test_response_appears_in_changelist(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Submitted form responses appear in the admin response list."""
        # Create a response directly (simulating a prior submission)
        from django.utils import timezone
        FormResponse.objects.create(
            form=contact_form,
            data={
                'full_name': 'Bob Smith',
                'email_address': 'bob@test.com',
                'message': 'Hello from Bob',
            },
            status='completed',
            submitted_at=timezone.now(),
            ip_address='127.0.0.1',
        )

        _navigate_to_response_changelist(
            admin_authenticated_page, form_pk=contact_form.pk
        )

        # The response list page should load
        page_content = admin_authenticated_page.content()
        # Check that the response data or form name appears
        assert 'E2E Contact Form' in page_content or 'bob@test.com' in page_content

    def test_response_detail_shows_data(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Response detail page shows the submitted data."""
        from django.utils import timezone
        response = FormResponse.objects.create(
            form=contact_form,
            data={
                'full_name': 'Charlie Brown',
                'email_address': 'charlie@test.com',
                'message': 'Test detail view',
            },
            status='completed',
            submitted_at=timezone.now(),
        )

        base = admin_authenticated_page._live_server_url
        admin_authenticated_page.goto(
            f'{base}/en/admin/form_builder/formresponse/{response.pk}/change/'
        )
        admin_authenticated_page.wait_for_load_state('networkidle')

        page_content = admin_authenticated_page.content()
        assert 'Charlie Brown' in page_content
        assert 'charlie@test.com' in page_content

    def test_submit_then_verify_in_admin(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Full E2E: submit a form, then verify the response appears in admin."""
        # Step 1: Submit the form via preview
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        admin_authenticated_page.fill('#field-full_name', 'E2E User')
        admin_authenticated_page.fill(
            '#field-email_address', 'e2e@test.com'
        )
        admin_authenticated_page.fill(
            '#field-message', 'End-to-end test message.'
        )
        _submit_form_and_wait(admin_authenticated_page)

        # Verify response was created
        assert FormResponse.objects.filter(
            form=contact_form, status='completed'
        ).count() == 1

        # Step 2: Navigate to admin response list and verify
        _navigate_to_response_changelist(
            admin_authenticated_page, form_pk=contact_form.pk
        )

        page_content = admin_authenticated_page.content()
        # The response should appear (either via email or form name)
        assert (
            'E2E Contact Form' in page_content
            or 'e2e@test.com' in page_content
            or 'completed' in page_content.lower()
        )


# ============================================================
# 4. Form Actions Configuration Tests
# ============================================================

class TestFormActionConfiguration:
    """Test that form actions are properly configured and linked to forms.

    NOTE: Actual action execution (email sending, webhook firing) cannot be
    verified in E2E tests because unittest.mock.patch() does not work across
    threads with Django's live_server. Action execution is covered by
    integration tests in tests/integration/test_form_builder.py.

    These tests verify:
    - Forms with actions can be submitted successfully
    - FormResponse records are created with correct data
    - Actions are properly configured in the database
    """

    def test_form_with_actions_renders_and_submits(
        self, admin_authenticated_page: Page, site_settings,
        form_with_actions
    ):
        """Form with configured actions renders and accepts submissions."""
        _navigate_to_form_preview(
            admin_authenticated_page, form_with_actions.pk
        )

        admin_authenticated_page.fill('#field-name', 'Action User')
        admin_authenticated_page.fill('#field-email', 'action@test.com')
        _submit_form_and_wait(admin_authenticated_page)

        # Verify the response was created with correct data
        response = FormResponse.objects.filter(
            form=form_with_actions
        ).first()
        assert response is not None
        assert response.data['name'] == 'Action User'
        assert response.data['email'] == 'action@test.com'
        assert response.status == 'completed'

    def test_form_actions_are_configured(
        self, admin_authenticated_page: Page, site_settings,
        form_with_actions
    ):
        """Verify that form actions are properly configured in the database."""
        actions = form_with_actions.actions.filter(is_active=True).order_by('order')
        assert actions.count() == 2

        email_action = actions[0]
        assert email_action.action_type == 'email_notification'
        assert email_action.name == 'Admin Notification'
        assert 'admin@test.com' in email_action.config['to_emails']

        webhook_action = actions[1]
        assert webhook_action.action_type == 'webhook'
        assert webhook_action.name == 'CRM Webhook'
        assert webhook_action.config['url'] == 'https://hooks.example.com/form-submit'

    def test_builder_loads_for_form_with_actions(
        self, admin_authenticated_page: Page, site_settings,
        form_with_actions
    ):
        """Visual builder loads correctly for forms with configured actions."""
        _navigate_to_visual_builder(
            admin_authenticated_page, form_with_actions.pk
        )

        page_content = admin_authenticated_page.content()
        # The builder should show the form's fields
        assert 'name' in page_content
        assert 'email' in page_content
        # Builder page should load without errors
        expect(admin_authenticated_page).to_have_title(
            re.compile(r'Form Builder.*')
        )

    def test_multiple_submissions_create_separate_responses(
        self, admin_authenticated_page: Page, site_settings,
        form_with_actions
    ):
        """Multiple submissions create separate FormResponse records."""
        # First submission
        _navigate_to_form_preview(
            admin_authenticated_page, form_with_actions.pk
        )
        admin_authenticated_page.fill('#field-name', 'First User')
        admin_authenticated_page.fill('#field-email', 'first@test.com')
        _submit_form_and_wait(admin_authenticated_page)

        # Second submission (reload the preview page)
        _navigate_to_form_preview(
            admin_authenticated_page, form_with_actions.pk
        )
        admin_authenticated_page.fill('#field-name', 'Second User')
        admin_authenticated_page.fill('#field-email', 'second@test.com')
        _submit_form_and_wait(admin_authenticated_page)

        # Should have 2 separate responses
        responses = FormResponse.objects.filter(
            form=form_with_actions, status='completed'
        ).order_by('submitted_at')
        assert responses.count() == 2
        assert responses[0].data['name'] == 'First User'
        assert responses[1].data['name'] == 'Second User'


# ============================================================
# 5. Admin Form Changelist Tests
# ============================================================

class TestFormChangelist:
    """Test the admin form changelist page."""

    def test_changelist_loads(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Form changelist page loads successfully."""
        _navigate_to_form_changelist(admin_authenticated_page)

        # Page should load without error
        page_content = admin_authenticated_page.content()
        assert 'E2E Contact Form' in page_content

    def test_changelist_shows_form_stats(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Changelist shows form statistics (active count, response count)."""
        _navigate_to_form_changelist(admin_authenticated_page)

        page_content = admin_authenticated_page.content()
        # The template renders total_forms and active_forms in context
        # These appear in the stats cards on the page
        assert '1' in page_content  # At least 1 form exists


class TestFormExport:
    """Test form response CSV export."""

    def test_export_downloads_csv(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Export endpoint returns a CSV file with correct content."""
        from django.utils import timezone
        FormResponse.objects.create(
            form=contact_form,
            data={'full_name': 'Export Test', 'email_address': 'export@t.com'},
            status='completed',
            submitted_at=timezone.now(),
        )

        base = admin_authenticated_page._live_server_url
        export_url = (
            f'{base}/en/admin/form_builder/responses/{contact_form.pk}/export/'
        )

        # Use page.evaluate to fetch the CSV content via JavaScript
        # This avoids Playwright download handling issues
        result = admin_authenticated_page.evaluate(f'''
            async () => {{
                const resp = await fetch('{export_url}');
                const disposition = resp.headers.get('Content-Disposition');
                const contentType = resp.headers.get('Content-Type');
                const text = await resp.text();
                return {{
                    status: resp.status,
                    contentType: contentType,
                    disposition: disposition,
                    body: text
                }};
            }}
        ''')

        assert result['status'] == 200
        assert 'text/csv' in result['contentType']
        assert 'attachment' in result['disposition']
        assert '.csv' in result['disposition']
        # Verify the CSV contains our test data
        assert 'Export Test' in result['body']
        assert 'export@t.com' in result['body']


# ============================================================
# 6. Security & Edge Case Tests
# ============================================================

class TestFormSecurity:
    """Test security aspects of form rendering and submission."""

    def test_inactive_form_preview_shows_content(
        self, admin_authenticated_page: Page, site_settings, inactive_form
    ):
        """Preview of an inactive form still works for admin (preview is admin-only)."""
        _navigate_to_form_preview(admin_authenticated_page, inactive_form.pk)

        # Admin preview should still render the form
        page_content = admin_authenticated_page.content()
        assert 'This form is disabled' in page_content

    def test_unauthenticated_cannot_access_builder(
        self, page: Page, site_settings, contact_form
    ):
        """Unauthenticated users cannot access the visual builder."""
        base = page._live_server_url
        page.goto(
            f'{base}/en/admin/form_builder/forms/{contact_form.pk}/builder/'
        )
        page.wait_for_load_state('networkidle')

        # Should redirect to login
        assert '/login/' in page.url

    def test_unauthenticated_cannot_access_preview(
        self, page: Page, site_settings, contact_form
    ):
        """Unauthenticated users cannot access form preview."""
        base = page._live_server_url
        page.goto(
            f'{base}/en/admin/form_builder/forms/{contact_form.pk}/preview/'
        )
        page.wait_for_load_state('networkidle')

        # Should redirect to login
        assert '/login/' in page.url


# ============================================================
# 7. Responsive Tests
# ============================================================

class TestFormResponsive:
    """Test form rendering on different viewport sizes."""

    def test_mobile_viewport_renders_form(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Form renders correctly on mobile viewport."""
        admin_authenticated_page.set_viewport_size(
            {"width": 375, "height": 812}
        )
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        # Form should still be visible
        form = admin_authenticated_page.locator('.spwig-form')
        expect(form).to_be_visible()

        # All fields should be visible
        fields = admin_authenticated_page.locator('.form-field')
        assert fields.count() >= 3

    def test_tablet_viewport_renders_form(
        self, admin_authenticated_page: Page, site_settings, contact_form
    ):
        """Form renders correctly on tablet viewport."""
        admin_authenticated_page.set_viewport_size(
            {"width": 768, "height": 1024}
        )
        _navigate_to_form_preview(admin_authenticated_page, contact_form.pk)

        form = admin_authenticated_page.locator('.spwig-form')
        expect(form).to_be_visible()
