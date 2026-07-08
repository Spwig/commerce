"""
Form Builder Admin Views

Views for form management in the admin interface.
"""
import json
import csv
import logging
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q, Max
from django.db import IntegrityError
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from .models import Form, FormStep, FormField, FormResponse, FormConditionalRule, FormAction

logger = logging.getLogger(__name__)


@staff_member_required
@require_GET
def preview_form(request, pk):
    """Preview a form"""
    form = get_object_or_404(Form, pk=pk)

    # Render form preview template
    html = render_to_string(
        'form_builder/form_render.html',
        {'form': form, 'preview_mode': True},
        request=request,
    )

    return HttpResponse(html)


@staff_member_required
@require_POST
def duplicate_form(request, pk):
    """Duplicate a form with all its fields"""
    original_form = get_object_or_404(Form, pk=pk)

    # Create new form
    new_form = Form.objects.create(
        name=f"{original_form.name} (Copy)",
        slug=f"{original_form.slug}-copy-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        title=original_form.title,
        description=original_form.description,
        submit_button_text=original_form.submit_button_text,
        success_message=original_form.success_message,
        error_message=original_form.error_message,
        is_active=False,  # Start as inactive
        is_multi_step=original_form.is_multi_step,
        require_login=original_form.require_login,
        save_partial_responses=original_form.save_partial_responses,
        spam_protection=original_form.spam_protection,
        translations=original_form.translations,
    )

    # Duplicate steps
    step_mapping = {}
    for step in original_form.steps.all():
        new_step = new_form.steps.create(
            title=step.title,
            description=step.description,
            order=step.order,
            is_skippable=step.is_skippable,
            next_button_text=step.next_button_text,
            back_button_text=step.back_button_text,
            translations=step.translations,
        )
        step_mapping[step.pk] = new_step

    # Duplicate fields
    for field in original_form.fields.all():
        new_step = step_mapping.get(field.step_id) if field.step_id else None
        new_form.fields.create(
            step=new_step,
            field_name=field.field_name,
            field_type=field.field_type,
            label=field.label,
            placeholder=field.placeholder,
            help_text=field.help_text,
            is_required=field.is_required,
            min_length=field.min_length,
            max_length=field.max_length,
            min_value=field.min_value,
            max_value=field.max_value,
            validation_regex=field.validation_regex,
            validation_message=field.validation_message,
            options=field.options,
            rating_config=field.rating_config,
            file_config=field.file_config,
            product_config=field.product_config,
            default_value=field.default_value,
            order=field.order,
            width=field.width,
            css_class=field.css_class,
            translations=field.translations,
        )

    messages.success(
        request,
        _('Form "%(name)s" duplicated successfully.') % {'name': original_form.name}
    )

    return redirect('admin:form_builder_form_change', new_form.pk)


@staff_member_required
@require_POST
def reorder_fields(request, pk):
    """AJAX endpoint for reordering form fields"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    import json
    try:
        data = json.loads(request.body)
        field_order = data.get('field_order', [])

        for index, field_id in enumerate(field_order):
            FormField.objects.filter(
                pk=field_id,
                form=form
            ).update(order=index)

        return JsonResponse({'success': True})
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid data'}, status=400)


@staff_member_required
@require_GET
def export_responses(request, form_pk):
    """Export form responses to CSV"""
    form = get_object_or_404(Form, pk=form_pk)
    responses = form.responses.filter(status='completed').order_by('-submitted_at')

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{form.slug}_responses_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)

    # Get all field names
    fields = form.fields.all().order_by('step__order', 'order')
    field_names = [f.field_name for f in fields]
    field_labels = [f.label for f in fields]

    # Write header
    header = ['Submitted At', 'User', 'IP Address', 'Status'] + field_labels
    writer.writerow(header)

    # Write data rows
    for resp in responses:
        row = [
            resp.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if resp.submitted_at else '',
            resp.user.email if resp.user else 'Anonymous',
            resp.ip_address or '',
            resp.status,
        ]

        # Add field values
        for field_name in field_names:
            value = resp.data.get(field_name, '')
            # Handle list values (checkboxes, multi-select)
            if isinstance(value, list):
                value = ', '.join(str(v) for v in value)
            row.append(value)

        writer.writerow(row)

    return response


@staff_member_required
@require_GET
def create_form(request):
    """Create a new blank form and redirect to the visual builder"""
    from django.utils.text import slugify
    import uuid

    # Generate unique name and slug
    unique_id = str(uuid.uuid4())[:8]
    name = f"New Form {unique_id}"
    slug = slugify(name)

    # Create the form (use str() to avoid lazy translation proxy)
    form = Form.objects.create(
        name=name,
        slug=slug,
        title=str(_('Untitled Form')),
        description='',
        is_active=False,  # Start as inactive until configured
    )

    # Redirect to visual builder
    return redirect('form_builder:visual_builder', pk=form.pk)


@staff_member_required
@require_GET
def visual_builder(request, pk):
    """Visual drag-and-drop form builder interface"""
    form = get_object_or_404(Form, pk=pk)
    logger.info(f"[VISUAL_BUILDER] Loading form pk={pk}, name={form.name}")
    logger.info(f"[VISUAL_BUILDER] Form has {form.fields.count()} fields, {form.steps.count()} steps")

    # Serialize form data for JavaScript
    form_data = {
        'id': form.pk,
        'name': form.name,
        'slug': form.slug,
        'title': form.title,
        'description': form.description,
        'submit_button_text': form.submit_button_text,
        'success_message': form.success_message,
        'error_message': form.error_message,
        'is_active': form.is_active,
        'is_multi_step': form.is_multi_step,
        'require_login': form.require_login,
        'save_partial_responses': form.save_partial_responses,
        'spam_protection': form.spam_protection,
        'translations': form.translations or {},
    }

    # Serialize steps
    steps_data = []
    for step in form.steps.all().order_by('order'):
        steps_data.append({
            'id': step.pk,
            'title': step.title,
            'description': step.description,
            'order': step.order,
            'is_skippable': step.is_skippable,
            'next_button_text': step.next_button_text,
            'back_button_text': step.back_button_text,
            'translations': step.translations or {},
        })

    # Serialize fields
    fields_data = []
    all_fields = list(form.fields.all().select_related('step').order_by('step__order', 'order'))
    logger.info(f"[VISUAL_BUILDER] Queried {len(all_fields)} fields from database")
    for field in all_fields:
        logger.info(f"[VISUAL_BUILDER] Field: id={field.pk}, name={field.field_name}, type={field.field_type}")
        fields_data.append({
            'id': field.pk,
            'step_id': field.step_id,
            'field_name': field.field_name,
            'field_type': field.field_type,
            'label': field.label,
            'placeholder': field.placeholder,
            'help_text': field.help_text,
            'is_required': field.is_required,
            'min_length': field.min_length,
            'max_length': field.max_length,
            'min_value': str(field.min_value) if field.min_value is not None else None,
            'max_value': str(field.max_value) if field.max_value is not None else None,
            'validation_regex': field.validation_regex,
            'validation_message': field.validation_message,
            'options': field.options or [],
            'rating_config': field.rating_config or {},
            'file_config': field.file_config or {},
            'product_config': field.product_config or {},
            'default_value': field.default_value,
            'order': field.order,
            'width': field.width,
            'css_class': field.css_class,
            'translations': field.translations or {},
        })
    logger.info(f"[VISUAL_BUILDER] Serialized {len(fields_data)} fields for JavaScript")

    # Serialize conditional rules
    rules_data = []
    for rule in form.rules.select_related('source_field', 'target_field', 'target_step').order_by('-priority', 'id'):
        rules_data.append({
            'id': rule.pk,
            'name': rule.name,
            'is_active': rule.is_active,
            'source_field_id': rule.source_field_id,
            'source_field_label': rule.source_field.label if rule.source_field else None,
            'operator': rule.operator,
            'operator_display': rule.get_operator_display(),
            'value': rule.value,
            'action': rule.action,
            'action_display': rule.get_action_display(),
            'target_field_id': rule.target_field_id,
            'target_field_label': rule.target_field.label if rule.target_field else None,
            'target_step_id': rule.target_step_id,
            'target_step_title': rule.target_step.title if rule.target_step else None,
            'action_value': rule.action_value,
            'priority': rule.priority,
            'description': rule.get_action_display_text(),
        })
    logger.info(f"[VISUAL_BUILDER] Serialized {len(rules_data)} rules for JavaScript")

    # Get available languages for translations (same approach as Product admin)
    try:
        from page_builder.translation_utils import get_available_languages, get_primary_language
        all_languages = get_available_languages()
        primary_language = get_primary_language()

        # Format for JavaScript, excluding primary language from translation targets
        languages = [
            {
                'code': code,
                'name': str(name),
                'is_primary': code == primary_language
            }
            for code, name in all_languages
            if code != primary_language
        ]

        # Include primary language info for display
        primary_lang_name = dict(all_languages).get(primary_language, primary_language.upper())
    except (ImportError, Exception):
        # Fallback to settings.LANGUAGES if translation service unavailable
        languages = [
            {'code': code, 'name': str(name), 'is_primary': False}
            for code, name in settings.LANGUAGES[1:]  # Exclude first (primary)
        ]
        primary_language = settings.LANGUAGE_CODE.split('-')[0] if '-' in settings.LANGUAGE_CODE else settings.LANGUAGE_CODE
        primary_lang_name = str(dict(settings.LANGUAGES).get(settings.LANGUAGE_CODE, 'English'))

    context = {
        'form': form,
        'form_data_json': json.dumps(form_data),
        'steps_data_json': json.dumps(steps_data),
        'fields_data_json': json.dumps(fields_data),
        'rules_data_json': json.dumps(rules_data),
        'languages': languages,
        'languages_json': json.dumps(languages),
        'primary_language': primary_language,
        'primary_language_name': primary_lang_name,
        'title': str(_('Edit Form Design: %(name)s') % {'name': form.name}),
        'site_header': str(_('Spwig Administration')),
        'has_permission': True,
    }

    return render(request, 'admin/form_builder/form/visual_builder.html', context)


@staff_member_required
@require_POST
def save_form_builder(request, pk):
    """AJAX endpoint to save form from visual builder"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        data = json.loads(request.body)
        logger.info(f"[SAVE_FORM_BUILDER] Form pk={pk}, keys in request: {list(data.keys())}")
        logger.info(f"[SAVE_FORM_BUILDER] 'steps' in data: {'steps' in data}, 'fields' in data: {'fields' in data}")

        # Update form settings
        form_data = data.get('form', {})
        form.name = form_data.get('name', form.name)
        form.title = form_data.get('title', form.title)
        form.description = form_data.get('description', form.description)
        form.submit_button_text = form_data.get('submit_button_text', form.submit_button_text)
        form.success_message = form_data.get('success_message', form.success_message)
        form.error_message = form_data.get('error_message', form.error_message)
        form.is_active = form_data.get('is_active', form.is_active)
        form.is_multi_step = form_data.get('is_multi_step', form.is_multi_step)
        form.require_login = form_data.get('require_login', form.require_login)
        form.save_partial_responses = form_data.get('save_partial_responses', form.save_partial_responses)
        form.spam_protection = form_data.get('spam_protection', form.spam_protection)
        form.translations = form_data.get('translations', form.translations)
        form.save()

        # Update steps - only process if 'steps' key is explicitly provided in request
        # This prevents accidental deletion when only saving form settings
        if 'steps' in data:
            steps_data = data.get('steps', [])
            existing_step_ids = set(form.steps.values_list('id', flat=True))
            updated_step_ids = set()

            for step_data in steps_data:
                step_id = step_data.get('id')
                if step_id and step_id in existing_step_ids:
                    # Update existing step
                    step = form.steps.get(pk=step_id)
                    updated_step_ids.add(step_id)
                else:
                    # Create new step
                    step = FormStep(form=form)

                step.title = step_data.get('title', 'Step')
                step.description = step_data.get('description', '')
                step.order = step_data.get('order', 0)
                step.is_skippable = step_data.get('is_skippable', False)
                step.next_button_text = step_data.get('next_button_text', 'Next')
                step.back_button_text = step_data.get('back_button_text', 'Back')
                step.translations = step_data.get('translations', step.translations)
                step.save()

                if not step_id:
                    # Update the step_data with new ID for field references
                    step_data['id'] = step.pk

            # Delete removed steps
            steps_to_delete = existing_step_ids - updated_step_ids
            form.steps.filter(pk__in=steps_to_delete).delete()

        # Update fields - only process if 'fields' key is explicitly provided in request
        # This prevents accidental deletion when only saving form settings
        if 'fields' in data:
            fields_data = data.get('fields', [])
            existing_field_ids = set(form.fields.values_list('id', flat=True))
            updated_field_ids = set()

            for field_data in fields_data:
                field_id = field_data.get('id')
                if field_id and field_id in existing_field_ids:
                    # Update existing field
                    field = form.fields.get(pk=field_id)
                    updated_field_ids.add(field_id)
                else:
                    # Create new field
                    field = FormField(form=form)

                # Get step reference
                step_id = field_data.get('step_id')
                if step_id:
                    try:
                        field.step = form.steps.get(pk=step_id)
                    except FormStep.DoesNotExist:
                        field.step = None
                else:
                    field.step = None

                field.field_name = field_data.get('field_name', 'field')
                field.field_type = field_data.get('field_type', 'text')
                field.label = field_data.get('label', 'Field')
                field.placeholder = field_data.get('placeholder', '')
                field.help_text = field_data.get('help_text', '')
                field.is_required = field_data.get('is_required', False)
                field.min_length = field_data.get('min_length')
                field.max_length = field_data.get('max_length')

                # Handle decimal values
                min_val = field_data.get('min_value')
                max_val = field_data.get('max_value')
                field.min_value = float(min_val) if min_val else None
                field.max_value = float(max_val) if max_val else None

                field.validation_regex = field_data.get('validation_regex', '')
                field.validation_message = field_data.get('validation_message', '')
                field.options = field_data.get('options', [])
                field.rating_config = field_data.get('rating_config', {})
                field.file_config = field_data.get('file_config', {})
                field.product_config = field_data.get('product_config', {})
                field.default_value = field_data.get('default_value', '')
                field.order = field_data.get('order', 0)
                field.width = field_data.get('width', 'full')
                field.css_class = field_data.get('css_class', '')
                field.translations = field_data.get('translations', field.translations)
                field.save()

            # Delete removed fields
            fields_to_delete = existing_field_ids - updated_field_ids
            form.fields.filter(pk__in=fields_to_delete).delete()

        return JsonResponse({
            'success': True,
            'message': str(_('Form saved successfully.')),
            'form_id': form.pk
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def add_field(request, pk):
    """AJAX endpoint to add a new field"""
    logger.info(f"[ADD_FIELD] Request received for form pk={pk}")

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        logger.warning(f"[ADD_FIELD] Invalid request - missing XMLHttpRequest header")
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)
    logger.info(f"[ADD_FIELD] Form found: {form.name} (id={form.id})")

    try:
        data = json.loads(request.body)
        field_type = data.get('field_type', 'text')
        step_id = data.get('step_id')
        logger.info(f"[ADD_FIELD] Creating field type={field_type}, step_id={step_id}")
        position = data.get('position', 0)

        # Get step if specified
        step = None
        if step_id:
            try:
                step = form.steps.get(pk=step_id)
            except FormStep.DoesNotExist:
                pass

        # Generate unique field name
        base_name = f'{field_type}_field'
        count = form.fields.filter(field_name__startswith=base_name).count()
        field_name = f'{base_name}_{count + 1}'

        # Default labels based on field type (use str() to avoid lazy translation proxy)
        default_labels = {
            'text': str(_('Text Field')),
            'textarea': str(_('Text Area')),
            'email': str(_('Email')),
            'phone': str(_('Phone')),
            'number': str(_('Number')),
            'url': str(_('URL')),
            'date': str(_('Date')),
            'time': str(_('Time')),
            'datetime': str(_('Date & Time')),
            'select': str(_('Dropdown')),
            'radio': str(_('Radio Buttons')),
            'checkbox': str(_('Checkbox')),
            'checkbox_group': str(_('Checkbox Group')),
            'rating_stars': str(_('Rating')),
            'rating_likert': str(_('Likert Scale')),
            'rating_nps': str(_('NPS Score')),
            'file': str(_('File Upload')),
            'product_select': str(_('Product Selection')),
            'hidden': str(_('Hidden Field')),
            'heading': str(_('Section Heading')),
            'paragraph': str(_('Paragraph')),
            'divider': str(_('Divider')),
        }

        # Default options for selection fields
        default_options = []
        if field_type in ['select', 'radio', 'checkbox_group']:
            default_options = [
                {'value': 'option1', 'label': str(_('Option 1'))},
                {'value': 'option2', 'label': str(_('Option 2'))},
            ]

        # Default rating config
        default_rating_config = {}
        if field_type == 'rating_stars':
            default_rating_config = {
                'max_stars': 5,
                'icon': 'fa-star',
                'allow_half': False,
                'color': '#fbbf24'
            }
        elif field_type == 'rating_likert':
            default_rating_config = {
                'scale_type': '5_point',
                'labels': {
                    '1': str(_('Strongly Disagree')),
                    '2': str(_('Disagree')),
                    '3': str(_('Neutral')),
                    '4': str(_('Agree')),
                    '5': str(_('Strongly Agree'))
                }
            }
        elif field_type == 'rating_nps':
            default_rating_config = {
                'low_label': str(_('Not at all likely')),
                'high_label': str(_('Extremely likely'))
            }

        # Create the field
        logger.info(f"[ADD_FIELD] About to create field with field_name={field_name}")
        field = FormField.objects.create(
            form=form,
            step=step,
            field_name=field_name,
            field_type=field_type,
            label=default_labels.get(field_type, str(_('Field'))),
            is_required=False,
            options=default_options,
            rating_config=default_rating_config,
            order=position,
            width='full',
        )
        logger.info(f"[ADD_FIELD] Field created successfully: id={field.pk}, field_name={field.field_name}")
        logger.info(f"[ADD_FIELD] Total fields for form {form.pk}: {form.fields.count()}")

        return JsonResponse({
            'success': True,
            'field': {
                'id': field.pk,
                'step_id': field.step_id,
                'field_name': field.field_name,
                'field_type': field.field_type,
                'label': field.label,
                'placeholder': field.placeholder,
                'help_text': field.help_text,
                'is_required': field.is_required,
                'options': field.options,
                'rating_config': field.rating_config,
                'order': field.order,
                'width': field.width,
                'translations': field.translations or {},
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def delete_field(request, pk, field_id):
    """AJAX endpoint to delete a field"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        field = form.fields.get(pk=field_id)
        field.delete()
        return JsonResponse({'success': True})
    except FormField.DoesNotExist:
        return JsonResponse({'error': 'Field not found'}, status=404)


@staff_member_required
@require_POST
def update_field(request, pk, field_id):
    """AJAX endpoint to update a single field"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        field = form.fields.get(pk=field_id)
        data = json.loads(request.body)

        # Update field properties
        if 'label' in data:
            field.label = data['label']
        if 'placeholder' in data:
            field.placeholder = data['placeholder']
        if 'help_text' in data:
            field.help_text = data['help_text']
        if 'is_required' in data:
            field.is_required = data['is_required']
        if 'min_length' in data:
            field.min_length = data['min_length']
        if 'max_length' in data:
            field.max_length = data['max_length']
        if 'min_value' in data:
            field.min_value = float(data['min_value']) if data['min_value'] else None
        if 'max_value' in data:
            field.max_value = float(data['max_value']) if data['max_value'] else None
        if 'validation_regex' in data:
            field.validation_regex = data['validation_regex']
        if 'validation_message' in data:
            field.validation_message = data['validation_message']
        if 'options' in data:
            field.options = data['options']
        if 'rating_config' in data:
            field.rating_config = data['rating_config']
        if 'file_config' in data:
            field.file_config = data['file_config']
        if 'default_value' in data:
            field.default_value = data['default_value']
        if 'width' in data:
            field.width = data['width']
        if 'css_class' in data:
            field.css_class = data['css_class']
        if 'translations' in data:
            field.translations = data['translations']
        if 'order' in data:
            field.order = data['order']
        if 'step_id' in data:
            if data['step_id']:
                try:
                    field.step = form.steps.get(pk=data['step_id'])
                except FormStep.DoesNotExist:
                    field.step = None
            else:
                field.step = None

        field.save()

        return JsonResponse({
            'success': True,
            'field': {
                'id': field.pk,
                'step_id': field.step_id,
                'field_name': field.field_name,
                'field_type': field.field_type,
                'label': field.label,
                'placeholder': field.placeholder,
                'help_text': field.help_text,
                'is_required': field.is_required,
                'options': field.options,
                'rating_config': field.rating_config,
                'order': field.order,
                'width': field.width,
                'translations': field.translations or {},
            }
        })

    except FormField.DoesNotExist:
        return JsonResponse({'error': 'Field not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# =============================================================================
# Step CRUD Views
# =============================================================================

@staff_member_required
@require_POST
def add_step(request, pk):
    """AJAX endpoint to add a new step to a form"""
    logger.info(f"[ADD_STEP] Request received for form pk={pk}")

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        logger.warning(f"[ADD_STEP] Invalid request - missing XMLHttpRequest header")
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)
    logger.info(f"[ADD_STEP] Form found: {form.name} (id={form.id})")

    try:
        data = json.loads(request.body)

        # Get the next order number
        # Note: We use "is None" instead of "or" because 0 is a valid order value
        # but 0 is falsy in Python, so "0 or -1" would incorrectly return -1
        max_order = form.steps.aggregate(Max('order'))['order__max']
        if max_order is None:
            max_order = -1
        order = max_order + 1
        logger.info(f"[ADD_STEP] Calculated order={order} (max_order={max_order})")

        # Create the step
        step = FormStep.objects.create(
            form=form,
            title=data.get('title', str(_('Step %(num)d') % {'num': order + 1})),
            description=data.get('description', ''),
            order=order,
            is_skippable=data.get('is_skippable', False),
            next_button_text=data.get('next_button_text', str(_('Next'))),
            back_button_text=data.get('back_button_text', str(_('Back'))),
            translations=data.get('translations', {}),
        )
        logger.info(f"[ADD_STEP] Step created successfully: id={step.pk}, title={step.title}, order={step.order}")
        logger.info(f"[ADD_STEP] Total steps for form {form.pk}: {form.steps.count()}")

        return JsonResponse({
            'success': True,
            'step': {
                'id': step.pk,
                'title': step.title,
                'description': step.description,
                'order': step.order,
                'is_skippable': step.is_skippable,
                'next_button_text': step.next_button_text,
                'back_button_text': step.back_button_text,
                'translations': step.translations or {},
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except IntegrityError as e:
        # This could happen if there's a race condition with the order number
        return JsonResponse({
            'error': 'Could not create step. Please try again.',
            'details': str(e)
        }, status=409)  # 409 Conflict
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def update_step(request, pk, step_id):
    """AJAX endpoint to update a step"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        step = form.steps.get(pk=step_id)
        data = json.loads(request.body)

        # Update step properties
        if 'title' in data:
            step.title = data['title']
        if 'description' in data:
            step.description = data['description']
        if 'order' in data:
            step.order = data['order']
        if 'is_skippable' in data:
            step.is_skippable = data['is_skippable']
        if 'next_button_text' in data:
            step.next_button_text = data['next_button_text']
        if 'back_button_text' in data:
            step.back_button_text = data['back_button_text']
        if 'translations' in data:
            step.translations = data['translations']

        step.save()

        return JsonResponse({
            'success': True,
            'step': {
                'id': step.pk,
                'title': step.title,
                'description': step.description,
                'order': step.order,
                'is_skippable': step.is_skippable,
                'next_button_text': step.next_button_text,
                'back_button_text': step.back_button_text,
                'translations': step.translations or {},
            }
        })

    except FormStep.DoesNotExist:
        return JsonResponse({'error': 'Step not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def delete_step(request, pk, step_id):
    """AJAX endpoint to delete a step"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        step = form.steps.get(pk=step_id)

        # Unassign all fields from this step (move them to no step)
        step.fields.update(step=None)

        # Delete the step
        step.delete()

        # Reorder remaining steps
        for idx, remaining_step in enumerate(form.steps.order_by('order')):
            if remaining_step.order != idx:
                remaining_step.order = idx
                remaining_step.save(update_fields=['order'])

        return JsonResponse({'success': True})

    except FormStep.DoesNotExist:
        return JsonResponse({'error': 'Step not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# =============================================================================
# Conditional Rule CRUD Views
# =============================================================================

@staff_member_required
@require_GET
def list_rules(request, pk):
    """AJAX endpoint to list all conditional rules for a form"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    rules = []
    for rule in form.rules.select_related('source_field', 'target_field', 'target_step').order_by('-priority', 'id'):
        rules.append({
            'id': rule.pk,
            'name': rule.name,
            'is_active': rule.is_active,
            'source_field_id': rule.source_field_id,
            'source_field_label': rule.source_field.label if rule.source_field else None,
            'operator': rule.operator,
            'operator_display': rule.get_operator_display(),
            'value': rule.value,
            'action': rule.action,
            'action_display': rule.get_action_display(),
            'target_field_id': rule.target_field_id,
            'target_field_label': rule.target_field.label if rule.target_field else None,
            'target_step_id': rule.target_step_id,
            'target_step_title': rule.target_step.title if rule.target_step else None,
            'action_value': rule.action_value,
            'priority': rule.priority,
            'description': rule.get_action_display_text(),
        })

    return JsonResponse({
        'success': True,
        'rules': rules
    })


@staff_member_required
@require_POST
def add_rule(request, pk):
    """AJAX endpoint to add a new conditional rule"""
    logger.info(f"[ADD_RULE] Request received for form pk={pk}")

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        data = json.loads(request.body)

        # Validate required fields
        source_field_id = data.get('source_field_id')
        if not source_field_id:
            return JsonResponse({'error': 'Source field is required'}, status=400)

        try:
            source_field = form.fields.get(pk=source_field_id)
        except FormField.DoesNotExist:
            return JsonResponse({'error': 'Source field not found'}, status=404)

        # Get target field if specified
        target_field = None
        target_field_id = data.get('target_field_id')
        if target_field_id:
            try:
                target_field = form.fields.get(pk=target_field_id)
            except FormField.DoesNotExist:
                return JsonResponse({'error': 'Target field not found'}, status=404)

        # Get target step if specified
        target_step = None
        target_step_id = data.get('target_step_id')
        if target_step_id:
            try:
                target_step = form.steps.get(pk=target_step_id)
            except FormStep.DoesNotExist:
                return JsonResponse({'error': 'Target step not found'}, status=404)

        # Create the rule
        rule = FormConditionalRule.objects.create(
            form=form,
            name=data.get('name', ''),
            is_active=data.get('is_active', True),
            source_field=source_field,
            operator=data.get('operator', 'equals'),
            value=data.get('value', {}),
            action=data.get('action', 'show_field'),
            target_field=target_field,
            target_step=target_step,
            action_value=data.get('action_value', {}),
            priority=data.get('priority', 0),
        )

        logger.info(f"[ADD_RULE] Rule created: id={rule.pk}")

        return JsonResponse({
            'success': True,
            'rule': {
                'id': rule.pk,
                'name': rule.name,
                'is_active': rule.is_active,
                'source_field_id': rule.source_field_id,
                'source_field_label': rule.source_field.label,
                'operator': rule.operator,
                'operator_display': rule.get_operator_display(),
                'value': rule.value,
                'action': rule.action,
                'action_display': rule.get_action_display(),
                'target_field_id': rule.target_field_id,
                'target_field_label': rule.target_field.label if rule.target_field else None,
                'target_step_id': rule.target_step_id,
                'target_step_title': rule.target_step.title if rule.target_step else None,
                'action_value': rule.action_value,
                'priority': rule.priority,
                'description': rule.get_action_display_text(),
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception(f"[ADD_RULE] Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def update_rule(request, pk, rule_id):
    """AJAX endpoint to update a conditional rule"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        rule = form.rules.get(pk=rule_id)
        data = json.loads(request.body)

        # Update basic properties
        if 'name' in data:
            rule.name = data['name']
        if 'is_active' in data:
            rule.is_active = data['is_active']
        if 'operator' in data:
            rule.operator = data['operator']
        if 'value' in data:
            rule.value = data['value']
        if 'action' in data:
            rule.action = data['action']
        if 'action_value' in data:
            rule.action_value = data['action_value']
        if 'priority' in data:
            rule.priority = data['priority']

        # Update source field
        if 'source_field_id' in data:
            source_field_id = data['source_field_id']
            if source_field_id:
                try:
                    rule.source_field = form.fields.get(pk=source_field_id)
                except FormField.DoesNotExist:
                    return JsonResponse({'error': 'Source field not found'}, status=404)

        # Update target field
        if 'target_field_id' in data:
            target_field_id = data['target_field_id']
            if target_field_id:
                try:
                    rule.target_field = form.fields.get(pk=target_field_id)
                except FormField.DoesNotExist:
                    return JsonResponse({'error': 'Target field not found'}, status=404)
            else:
                rule.target_field = None

        # Update target step
        if 'target_step_id' in data:
            target_step_id = data['target_step_id']
            if target_step_id:
                try:
                    rule.target_step = form.steps.get(pk=target_step_id)
                except FormStep.DoesNotExist:
                    return JsonResponse({'error': 'Target step not found'}, status=404)
            else:
                rule.target_step = None

        rule.save()

        return JsonResponse({
            'success': True,
            'rule': {
                'id': rule.pk,
                'name': rule.name,
                'is_active': rule.is_active,
                'source_field_id': rule.source_field_id,
                'source_field_label': rule.source_field.label,
                'operator': rule.operator,
                'operator_display': rule.get_operator_display(),
                'value': rule.value,
                'action': rule.action,
                'action_display': rule.get_action_display(),
                'target_field_id': rule.target_field_id,
                'target_field_label': rule.target_field.label if rule.target_field else None,
                'target_step_id': rule.target_step_id,
                'target_step_title': rule.target_step.title if rule.target_step else None,
                'action_value': rule.action_value,
                'priority': rule.priority,
                'description': rule.get_action_display_text(),
            }
        })

    except FormConditionalRule.DoesNotExist:
        return JsonResponse({'error': 'Rule not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception(f"[UPDATE_RULE] Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def delete_rule(request, pk, rule_id):
    """AJAX endpoint to delete a conditional rule"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        rule = form.rules.get(pk=rule_id)
        rule.delete()
        return JsonResponse({'success': True})
    except FormConditionalRule.DoesNotExist:
        return JsonResponse({'error': 'Rule not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# =============================================================================
# Form Action CRUD Views
# =============================================================================

def _serialize_action(action):
    """Serialize a FormAction to a dict."""
    return {
        'id': action.pk,
        'action_type': action.action_type,
        'action_type_display': action.get_action_type_display(),
        'name': action.name,
        'is_active': action.is_active,
        'config': action.config,
        'order': action.order,
    }


@staff_member_required
@require_GET
def list_actions(request, pk):
    """AJAX endpoint to list all actions for a form."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)
    actions = [_serialize_action(a) for a in form.actions.order_by('order')]

    return JsonResponse({
        'success': True,
        'actions': actions,
    })


@staff_member_required
@require_POST
def add_action(request, pk):
    """AJAX endpoint to add a new form action."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        data = json.loads(request.body)

        action_type = data.get('action_type')
        if action_type not in dict(FormAction.ACTION_TYPES):
            return JsonResponse({'error': 'Invalid action type'}, status=400)

        max_order = form.actions.aggregate(Max('order'))['order__max']
        order = (max_order or 0) + 1

        action = FormAction.objects.create(
            form=form,
            action_type=action_type,
            name=data.get('name', ''),
            is_active=data.get('is_active', True),
            config=data.get('config', {}),
            order=order,
        )

        return JsonResponse({
            'success': True,
            'action': _serialize_action(action),
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception("add_action error: %s", e)
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def update_action(request, pk, action_id):
    """AJAX endpoint to update a form action."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        action = form.actions.get(pk=action_id)
        data = json.loads(request.body)

        if 'name' in data:
            action.name = data['name']
        if 'is_active' in data:
            action.is_active = data['is_active']
        if 'config' in data:
            action.config = data['config']
        if 'order' in data:
            action.order = data['order']
        if 'action_type' in data and data['action_type'] in dict(FormAction.ACTION_TYPES):
            action.action_type = data['action_type']

        action.save()

        return JsonResponse({
            'success': True,
            'action': _serialize_action(action),
        })

    except FormAction.DoesNotExist:
        return JsonResponse({'error': 'Action not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception("update_action error: %s", e)
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_POST
def delete_action(request, pk, action_id):
    """AJAX endpoint to delete a form action."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    form = get_object_or_404(Form, pk=pk)

    try:
        action = form.actions.get(pk=action_id)
        action.delete()
        return JsonResponse({'success': True})
    except FormAction.DoesNotExist:
        return JsonResponse({'error': 'Action not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
