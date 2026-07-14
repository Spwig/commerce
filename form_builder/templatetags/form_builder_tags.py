"""
Form Builder Template Tags

Template tags for rendering Form Builder forms in templates.
"""

import json

from django import template
from django.utils.safestring import mark_safe

from form_builder.models import Form

register = template.Library()


@register.simple_tag(takes_context=True)
def get_form_data(context, form_slug):
    """
    Get form data for rendering in templates.

    Usage:
        {% get_form_data form_slug as form_data %}

    Returns a dictionary with form structure, fields, steps, and rules
    suitable for JavaScript initialization.
    """
    if not form_slug:
        return None

    try:
        form = Form.objects.get(slug=form_slug, is_active=True)
    except Form.DoesNotExist:
        return None

    request = context.get("request")
    language_code = None
    if request:
        language_code = getattr(request, "LANGUAGE_CODE", None)

    # Build fields data
    fields_data = []
    for field in form.fields.all().select_related("step").order_by("step__order", "order"):
        field_data = {
            "id": field.pk,
            "field_name": field.field_name,
            "field_type": field.field_type,
            "label": field.get_translated_field("label", language_code) or field.label,
            "placeholder": field.get_translated_field("placeholder", language_code)
            or field.placeholder,
            "help_text": field.get_translated_field("help_text", language_code) or field.help_text,
            "is_required": field.is_required,
            "width": field.width,
            "order": field.order,
            "default_value": field.default_value,
            "css_class": field.css_class,
        }

        # Add validation rules
        if field.min_length:
            field_data["min_length"] = field.min_length
        if field.max_length:
            field_data["max_length"] = field.max_length
        if field.min_value:
            field_data["min_value"] = float(field.min_value)
        if field.max_value:
            field_data["max_value"] = float(field.max_value)
        if field.validation_regex:
            field_data["pattern"] = field.validation_regex
            field_data["pattern_message"] = field.validation_message

        # Add options for selection fields
        if field.options:
            field_data["options"] = field.options

        # Add rating config
        if field.rating_config:
            field_data["rating_config"] = field.rating_config

        # Add file config
        if field.file_config:
            field_data["file_config"] = field.file_config

        # Add product config
        if field.product_config:
            field_data["product_config"] = field.product_config

        # Add step info
        if field.step:
            field_data["step_id"] = field.step.pk
            field_data["step_order"] = field.step.order
        else:
            field_data["step_id"] = None
            field_data["step_order"] = 0

        fields_data.append(field_data)

    # Build steps data
    steps_data = []
    if form.is_multi_step:
        for step in form.steps.all().order_by("order"):
            steps_data.append(
                {
                    "id": step.pk,
                    "title": step.get_translated_field("title", language_code) or step.title,
                    "description": step.get_translated_field("description", language_code)
                    or step.description,
                    "order": step.order,
                    "is_skippable": step.is_skippable,
                    "next_button_text": step.get_translated_field("next_button_text", language_code)
                    or step.next_button_text,
                    "back_button_text": step.get_translated_field("back_button_text", language_code)
                    or step.back_button_text,
                }
            )

    # Build conditional rules data
    rules_data = []
    for rule in form.rules.filter(is_active=True).select_related(
        "source_field", "target_field", "target_step"
    ):
        rule_data = {
            "id": rule.pk,
            "source_field_id": rule.source_field_id,
            "source_field_name": rule.source_field.field_name if rule.source_field else None,
            "operator": rule.operator,
            "value": rule.value,
            "action": rule.action,
            "priority": rule.priority,
        }

        if rule.target_field:
            rule_data["target_field_id"] = rule.target_field_id
            rule_data["target_field_name"] = rule.target_field.field_name
        if rule.target_step:
            rule_data["target_step_id"] = rule.target_step_id
            rule_data["target_step_order"] = rule.target_step.order

        if rule.action_value:
            rule_data["action_value"] = rule.action_value

        rules_data.append(rule_data)

    return {
        "id": form.pk,
        "slug": form.slug,
        "title": form.get_translated_field("title", language_code) or form.title,
        "description": form.get_translated_field("description", language_code) or form.description,
        "submit_button_text": form.get_translated_field("submit_button_text", language_code)
        or form.submit_button_text,
        "success_message": form.get_translated_field("success_message", language_code)
        or form.success_message,
        "error_message": form.get_translated_field("error_message", language_code)
        or form.error_message,
        "is_multi_step": form.is_multi_step,
        "require_login": form.require_login,
        "spam_protection": form.spam_protection,
        "save_partial_responses": form.save_partial_responses,
        "steps": steps_data,
        "fields": fields_data,
        "rules": rules_data,
    }


@register.simple_tag
def form_data_json(form_data):
    """
    Convert form data to JSON for JavaScript initialization.

    Usage:
        {% form_data_json form_data %}
    """
    if not form_data:
        return "null"
    return mark_safe(json.dumps(form_data))


@register.inclusion_tag("form_builder/render_form.html", takes_context=True)
def render_form(context, form_slug, **options):
    """
    Render a complete form with all styling options.

    Usage:
        {% render_form "contact-form" %}
        {% render_form "survey" show_title=True field_style="outlined" %}
    """
    form_data = get_form_data(context, form_slug)

    return {
        "form_data": form_data,
        "form_slug": form_slug,
        "options": options,
        "request": context.get("request"),
    }


@register.filter
def get_fields_for_step(fields, step_id):
    """
    Filter fields by step ID.

    Usage:
        {{ form_data.fields|get_fields_for_step:step.id }}
    """
    if step_id is None:
        # Return fields without a step (for single-step forms or orphaned fields)
        return [f for f in fields if f.get("step_id") is None]
    return [f for f in fields if f.get("step_id") == step_id]


@register.filter
def fields_without_step(fields):
    """
    Get fields that don't belong to any step.

    Usage:
        {{ form_data.fields|fields_without_step }}
    """
    return [f for f in fields if f.get("step_id") is None]
