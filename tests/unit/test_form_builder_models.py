"""
Form Builder Model Unit Tests.

Comprehensive tests covering:
- Form model: CRUD, __str__, soft delete, translations, properties
- FormStep model: CRUD, ordering, unique_together, translations
- FormField model: field types, validation, translations, ordering
- FormResponse model: CRUD, status, display_data
- FormConditionalRule model: all 14 operators, clean() validation
- FormAction model: CRUD, action types, config schema
"""

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from form_builder.models import (
    Form,
    FormAction,
    FormConditionalRule,
    FormField,
    FormResponse,
    FormStep,
)
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.form_builder]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def form(db):
    """Active form with default settings."""
    return Form.objects.create(
        name="Contact Form",
        slug="contact-form",
        title="Contact Us",
        description="Get in touch with us",
        submit_button_text="Send",
        success_message="Thanks!",
        error_message="Oops!",
        is_active=True,
    )


@pytest.fixture
def inactive_form(db):
    """Inactive form."""
    return Form.objects.create(
        name="Draft Form",
        slug="draft-form",
        title="Draft",
        is_active=False,
    )


@pytest.fixture
def multi_step_form(db):
    """Multi-step form with steps."""
    form = Form.objects.create(
        name="Survey",
        slug="survey",
        title="Customer Survey",
        is_active=True,
        is_multi_step=True,
    )
    return form


@pytest.fixture
def step(form):
    """Step belonging to the default form."""
    return FormStep.objects.create(
        form=form,
        title="Step 1",
        description="First step",
        order=0,
    )


@pytest.fixture
def text_field(form, step):
    """Text field."""
    return FormField.objects.create(
        form=form,
        step=step,
        field_name="full_name",
        field_type="text",
        label="Full Name",
        is_required=True,
        order=0,
    )


@pytest.fixture
def email_field(form, step):
    """Email field."""
    return FormField.objects.create(
        form=form,
        step=step,
        field_name="email",
        field_type="email",
        label="Email Address",
        is_required=True,
        order=1,
    )


@pytest.fixture
def select_field(form, step):
    """Select field with options."""
    return FormField.objects.create(
        form=form,
        step=step,
        field_name="reason",
        field_type="select",
        label="Contact Reason",
        options=[
            {"value": "support", "label": "Support"},
            {"value": "sales", "label": "Sales"},
            {"value": "other", "label": "Other"},
        ],
        order=2,
    )


@pytest.fixture
def response(form, user):
    """Completed form response."""
    return FormResponse.objects.create(
        form=form,
        user=user,
        data={"full_name": "John Doe", "email": "john@example.com"},
        status="completed",
        ip_address="127.0.0.1",
        submitted_at=timezone.now(),
        completed_at=timezone.now(),
    )


# ============================================================
# Form Model Tests
# ============================================================


class TestFormModel:
    """Tests for the Form model."""

    def test_str(self, form):
        assert str(form) == "Contact Form"

    def test_default_values(self, db):
        form = Form.objects.create(name="Test", slug="test", title="Test")
        assert form.is_active is True
        assert form.is_multi_step is False
        assert form.require_login is False
        assert form.save_partial_responses is False
        assert form.spam_protection == "honeypot"
        assert form.submit_button_text == "Submit"

    def test_timestamps(self, form):
        assert form.created_at is not None
        assert form.updated_at is not None

    def test_slug_unique(self, form, db):
        with pytest.raises(IntegrityError), transaction.atomic():
            Form.objects.create(
                name="Duplicate",
                slug="contact-form",
                title="Duplicate",
            )

    def test_field_count(self, form, text_field, email_field):
        assert form.field_count == 2

    def test_step_count_single_step(self, form):
        assert form.step_count == 1

    def test_step_count_multi_step(self, multi_step_form):
        FormStep.objects.create(form=multi_step_form, title="S1", order=0)
        FormStep.objects.create(form=multi_step_form, title="S2", order=1)
        assert multi_step_form.step_count == 2

    def test_response_count(self, form, response):
        assert form.response_count == 1

    def test_response_count_excludes_draft(self, form, user):
        FormResponse.objects.create(form=form, user=user, data={}, status="draft")
        assert form.response_count == 0

    def test_cascade_delete_steps(self, form, step):
        pk = form.pk
        assert FormStep.objects.filter(form_id=pk).count() == 1
        form.hard_delete()
        assert FormStep.objects.filter(form_id=pk).count() == 0

    def test_cascade_delete_fields(self, form, text_field, email_field):
        pk = form.pk
        assert FormField.objects.filter(form_id=pk).count() == 2
        form.hard_delete()
        assert FormField.objects.filter(form_id=pk).count() == 0


class TestFormTranslations:
    """Tests for Form translation functionality."""

    def test_get_translated_field_fallback(self, form):
        """Falls back to original field when no translations."""
        assert form.get_translated_field("title") == "Contact Us"

    def test_get_translated_field_exact_match(self, form):
        form.translations = {"de": {"title": "Kontaktiere uns"}}
        form.save()
        assert form.get_translated_field("title", "de") == "Kontaktiere uns"

    def test_get_translated_field_base_language(self, form):
        """en-us falls back to en."""
        form.translations = {"en": {"title": "Contact (EN)"}}
        form.save()
        assert form.get_translated_field("title", "en-us") == "Contact (EN)"

    def test_translated_properties(self, form):
        form.translations = {
            "de": {
                "title": "Kontakt",
                "description": "Beschreibung",
                "submit_button_text": "Senden",
                "success_message": "Danke!",
                "error_message": "Fehler!",
            }
        }
        form.save()
        assert form.get_translated_field("title", "de") == "Kontakt"
        assert form.get_translated_field("description", "de") == "Beschreibung"
        assert form.get_translated_field("submit_button_text", "de") == "Senden"
        assert form.get_translated_field("success_message", "de") == "Danke!"
        assert form.get_translated_field("error_message", "de") == "Fehler!"


class TestFormSoftDelete:
    """Tests for Form soft delete (SoftDeleteModel) integration."""

    def test_soft_delete(self, form, user):
        form.delete(user=user)
        assert form.is_deleted is True
        assert form.deleted_at is not None
        assert form.deleted_by == user

    def test_soft_deleted_excluded_from_default_manager(self, form, user):
        form.delete(user=user)
        assert Form.objects.filter(pk=form.pk).count() == 0

    def test_soft_deleted_visible_in_all_objects(self, form, user):
        form.delete(user=user)
        assert Form.all_objects.filter(pk=form.pk).count() == 1

    def test_restore(self, form, user):
        form.delete(user=user)
        form.restore()
        assert form.is_deleted is False
        assert form.deleted_at is None
        assert form.deleted_by is None
        assert Form.objects.filter(pk=form.pk).count() == 1

    def test_hard_delete(self, form):
        pk = form.pk
        form.hard_delete()
        assert Form.all_objects.filter(pk=pk).count() == 0

    def test_is_active_independent_of_is_deleted(self, form, user):
        """is_active (accepting submissions) is separate from is_deleted (recycle bin)."""
        form.is_active = True
        form.save()
        form.delete(user=user)
        # Form is in recycle bin but was active
        assert form.is_deleted is True
        # The BooleanField value is preserved
        assert Form.all_objects.get(pk=form.pk).is_active is True


# ============================================================
# FormStep Model Tests
# ============================================================


class TestFormStepModel:
    def test_str(self, form, step):
        assert str(step) == "Contact Form - Step 1: Step 1"

    def test_default_values(self, form):
        step = FormStep.objects.create(form=form, title="Test", order=1)
        assert step.is_skippable is False
        assert step.next_button_text == "Next"
        assert step.back_button_text == "Back"

    def test_unique_together_form_order(self, form, step):
        with pytest.raises(IntegrityError), transaction.atomic():
            FormStep.objects.create(form=form, title="Dup", order=0)

    def test_ordering(self, form):
        s2 = FormStep.objects.create(form=form, title="Second", order=2)
        s1 = FormStep.objects.create(form=form, title="First", order=1)
        steps = list(FormStep.objects.filter(form=form))
        assert steps[0].order < steps[1].order

    def test_cascade_delete(self, form, step, text_field):
        """Deleting a step sets field.step to NULL (SET_NULL)."""
        step_pk = step.pk
        step.delete()
        text_field.refresh_from_db()
        assert text_field.step is None

    def test_translations(self, form):
        step = FormStep.objects.create(
            form=form,
            title="Personal Info",
            order=1,
            translations={"de": {"title": "Persoenliche Daten"}},
        )
        assert step.get_translated_field("title", "de") == "Persoenliche Daten"
        assert step.translated_title == "Personal Info"  # Default language fallback

    def test_timestamps(self, step):
        assert step.created_at is not None
        assert step.updated_at is not None


# ============================================================
# FormField Model Tests
# ============================================================


class TestFormFieldModel:
    def test_str(self, text_field):
        assert str(text_field) == "Contact Form - Full Name"

    def test_all_field_types(self, form):
        """Verify all field types can be created."""
        field_types = [
            "text",
            "textarea",
            "email",
            "phone",
            "number",
            "url",
            "date",
            "time",
            "datetime",
            "select",
            "checkbox",
            "checkbox_group",
            "radio",
            "file",
            "product_select",
            "rating_stars",
            "rating_likert",
            "rating_nps",
            "heading",
            "paragraph",
            "divider",
            "hidden",
        ]
        for i, ft in enumerate(field_types):
            FormField.objects.create(
                form=form,
                field_name=f"field_{ft}",
                field_type=ft,
                label=f"Test {ft}",
                order=i,
            )
        assert form.fields.count() == len(field_types)

    def test_width_choices(self, form):
        for width in ["full", "half", "third"]:
            f = FormField.objects.create(
                form=form,
                field_name=f"w_{width}",
                field_type="text",
                label="W",
                width=width,
                order=0,
            )
            assert f.width == width

    def test_options_json(self, select_field):
        assert len(select_field.options) == 3
        assert select_field.options[0]["value"] == "support"

    def test_rating_config_json(self, form):
        field = FormField.objects.create(
            form=form,
            field_name="stars",
            field_type="rating_stars",
            label="Rating",
            rating_config={"max_stars": 5, "icon": "star"},
            order=0,
        )
        assert field.rating_config["max_stars"] == 5

    def test_file_config_json(self, form):
        field = FormField.objects.create(
            form=form,
            field_name="upload",
            field_type="file",
            label="Upload",
            file_config={"max_size_mb": 10, "allowed_types": ["pdf", "jpg"]},
            order=0,
        )
        assert field.file_config["max_size_mb"] == 10

    def test_translations(self, text_field):
        text_field.translations = {
            "de": {"label": "Vollstaendiger Name", "placeholder": "Ihr Name"}
        }
        text_field.save()
        assert text_field.get_translated_field("label", "de") == "Vollstaendiger Name"
        assert text_field.get_translated_field("placeholder", "de") == "Ihr Name"

    def test_timestamps(self, text_field):
        assert text_field.created_at is not None
        assert text_field.updated_at is not None


# ============================================================
# FormResponse Model Tests
# ============================================================


class TestFormResponseModel:
    def test_str_with_user(self, response):
        assert response.user.email in str(response)

    def test_str_anonymous(self, form):
        r = FormResponse.objects.create(form=form, data={}, status="submitted")
        assert "Anonymous" in str(r)

    def test_get_field_value(self, response):
        assert response.get_field_value("full_name") == "John Doe"
        assert response.get_field_value("nonexistent") is None

    def test_get_display_data(self, form, text_field, email_field, response):
        display = response.get_display_data()
        labels = [d["label"] for d in display]
        assert "Full Name" in labels
        assert "Email Address" in labels

    def test_status_choices(self, form):
        for st in ["draft", "submitted", "processing", "completed", "failed"]:
            r = FormResponse.objects.create(form=form, data={}, status=st)
            assert r.status == st

    def test_multi_step_progress(self, form):
        r = FormResponse.objects.create(
            form=form,
            data={},
            status="draft",
            current_step=2,
            completed_steps=[1],
        )
        assert r.current_step == 2
        assert r.completed_steps == [1]

    def test_action_results(self, form):
        r = FormResponse.objects.create(
            form=form,
            data={},
            status="completed",
            action_results={"email_notification": {"success": True, "sent_to": "admin@test.com"}},
        )
        assert r.action_results["email_notification"]["success"] is True


# ============================================================
# FormConditionalRule Model Tests
# ============================================================


class TestFormConditionalRuleModel:
    @pytest.fixture
    def source_field(self, form, step):
        return FormField.objects.create(
            form=form,
            step=step,
            field_name="rating",
            field_type="number",
            label="Rating",
            order=10,
        )

    @pytest.fixture
    def target_field(self, form, step):
        return FormField.objects.create(
            form=form,
            step=step,
            field_name="feedback",
            field_type="textarea",
            label="Feedback",
            order=11,
        )

    @pytest.fixture
    def rule(self, form, source_field, target_field):
        return FormConditionalRule.objects.create(
            form=form,
            name="Show feedback for low ratings",
            source_field=source_field,
            operator="less_than",
            value={"value": "3"},
            action="show_field",
            target_field=target_field,
        )

    def test_str_with_name(self, rule):
        assert "Show feedback for low ratings" in str(rule)

    def test_str_without_name(self, form, source_field, target_field):
        rule = FormConditionalRule.objects.create(
            form=form,
            source_field=source_field,
            operator="equals",
            value={"value": "test"},
            action="show_field",
            target_field=target_field,
        )
        assert f"Rule #{rule.pk}" in str(rule)

    def test_clean_field_action_requires_target_field(self, form, source_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="equals",
            value={"value": "1"},
            action="show_field",
            target_field=None,
        )
        with pytest.raises(ValidationError):
            rule.clean()

    def test_clean_step_action_requires_target_step(self, form, source_field, step):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="equals",
            value={"value": "1"},
            action="skip_to_step",
            target_step=None,
        )
        with pytest.raises(ValidationError):
            rule.clean()

    # ---- Operator evaluation tests ----

    def test_evaluate_equals(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="equals",
            value={"value": "hello"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("hello") is True
        assert rule.evaluate("Hello") is True  # case insensitive
        assert rule.evaluate("world") is False

    def test_evaluate_not_equals(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="not_equals",
            value={"value": "hello"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("world") is True
        assert rule.evaluate("hello") is False

    def test_evaluate_contains(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="contains",
            value={"value": "world"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("hello world") is True
        assert rule.evaluate("hello") is False

    def test_evaluate_not_contains(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="not_contains",
            value={"value": "world"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("hello") is True
        assert rule.evaluate("hello world") is False

    def test_evaluate_starts_with(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="starts_with",
            value={"value": "hel"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("hello") is True
        assert rule.evaluate("world") is False

    def test_evaluate_ends_with(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="ends_with",
            value={"value": "lo"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("hello") is True
        assert rule.evaluate("world") is False

    def test_evaluate_greater_than(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="greater_than",
            value={"value": "5"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("6") is True
        assert rule.evaluate("5") is False
        assert rule.evaluate("4") is False

    def test_evaluate_less_than(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="less_than",
            value={"value": "5"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("4") is True
        assert rule.evaluate("5") is False
        assert rule.evaluate("6") is False

    def test_evaluate_greater_than_or_equal(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="greater_than_or_equal",
            value={"value": "5"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("5") is True
        assert rule.evaluate("6") is True
        assert rule.evaluate("4") is False

    def test_evaluate_less_than_or_equal(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="less_than_or_equal",
            value={"value": "5"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("5") is True
        assert rule.evaluate("4") is True
        assert rule.evaluate("6") is False

    def test_evaluate_is_empty(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="is_empty",
            value={},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate(None) is True
        assert rule.evaluate("") is True
        assert rule.evaluate([]) is True
        assert rule.evaluate("something") is False

    def test_evaluate_is_not_empty(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="is_not_empty",
            value={},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("something") is True
        assert rule.evaluate(None) is False
        assert rule.evaluate("") is False

    def test_evaluate_in_list(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="in_list",
            value={"list": ["apple", "banana", "cherry"]},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("apple") is True
        assert rule.evaluate("BANANA") is True  # case insensitive
        assert rule.evaluate("grape") is False

    def test_evaluate_not_in_list(self, form, source_field, target_field):
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="not_in_list",
            value={"list": ["apple", "banana"]},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("grape") is True
        assert rule.evaluate("apple") is False

    def test_evaluate_numeric_fallback_non_numeric(self, form, source_field, target_field):
        """Non-numeric values return False for numeric operators."""
        rule = FormConditionalRule(
            form=form,
            source_field=source_field,
            operator="greater_than",
            value={"value": "5"},
            action="show_field",
            target_field=target_field,
        )
        assert rule.evaluate("not_a_number") is False

    def test_get_action_display_text(self, rule):
        text = rule.get_action_display_text()
        assert "Rating" in text
        assert "Feedback" in text


# ============================================================
# FormAction Model Tests
# ============================================================


class TestFormActionModel:
    def test_str(self, form):
        action = FormAction.objects.create(
            form=form,
            action_type="email_notification",
            name="Notify Admin",
            config={"to_emails": ["admin@example.com"]},
        )
        assert str(action) == "Contact Form - Notify Admin"

    def test_action_types(self, form):
        for at in ["email_notification", "auto_reply", "webhook"]:
            a = FormAction.objects.create(
                form=form,
                action_type=at,
                name=f"Action {at}",
                order=0,
            )
            assert a.action_type == at

    def test_email_notification_config(self, form):
        action = FormAction.objects.create(
            form=form,
            action_type="email_notification",
            name="Notify",
            config={
                "to_emails": ["admin@test.com"],
                "subject_template": "New submission: {{ form_name }}",
                "body_template": "Data: {{ data }}",
                "include_data": True,
            },
        )
        assert action.config["to_emails"] == ["admin@test.com"]
        assert action.config["include_data"] is True

    def test_webhook_config(self, form):
        action = FormAction.objects.create(
            form=form,
            action_type="webhook",
            name="Send to API",
            config={
                "url": "https://api.example.com/webhook",
                "method": "POST",
                "headers": {"Authorization": "Bearer token"},
                "secret": "hmac_secret",
            },
        )
        assert action.config["url"] == "https://api.example.com/webhook"

    def test_auto_reply_config(self, form):
        action = FormAction.objects.create(
            form=form,
            action_type="auto_reply",
            name="Thank You",
            config={
                "email_field": "email",
                "subject": "Thanks for contacting us",
                "body_template": "We received your message.",
            },
        )
        assert action.config["email_field"] == "email"

    def test_ordering(self, form):
        a2 = FormAction.objects.create(
            form=form,
            action_type="webhook",
            name="Second",
            order=2,
        )
        a1 = FormAction.objects.create(
            form=form,
            action_type="email_notification",
            name="First",
            order=1,
        )
        actions = list(FormAction.objects.filter(form=form))
        assert actions[0].order < actions[1].order

    def test_cascade_delete(self, form):
        FormAction.objects.create(
            form=form,
            action_type="webhook",
            name="Test",
            order=0,
        )
        assert FormAction.objects.filter(form=form).count() == 1
        form.hard_delete()
        assert FormAction.objects.count() == 0

    def test_is_active_default(self, form):
        action = FormAction.objects.create(
            form=form,
            action_type="webhook",
            name="Test",
            order=0,
        )
        assert action.is_active is True

    def test_timestamps(self, form):
        action = FormAction.objects.create(
            form=form,
            action_type="webhook",
            name="Test",
            order=0,
        )
        assert action.created_at is not None
        assert action.updated_at is not None
