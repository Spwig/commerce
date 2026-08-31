"""
Form Builder API Views

API endpoints for public form submission.
"""

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from core.api.api_descriptions import (
    AUTH_REQUIRED,
    STAFF_ACCESS_REQUIRED,
)
from core.api.authentication import HeadlessAPIMixin

from .models import Form, FormField, FormResponse


def _login_required_response(form, request):
    """Return a 401 response when the form requires login and the requester is anonymous."""
    if form.require_login and not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    return None


def _coerce_int(value):
    """Return ``value`` as an int, or ``None`` when it cannot be interpreted as one."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class FormListForSelectorView(APIView):
    """
    GET /api/form-builder/forms/list/
    Returns list of active forms for Page Builder form selector.
    Requires staff authentication.
    """

    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Form Builder"],
        summary=_("List active forms for selector"),
        description=_("""Returns a list of all active forms for use in the Page Builder form element selector.

        **Authentication:** Staff/Admin only

        **Response includes:**
        - Form ID, slug, name, and title
        - Whether the form is multi-step
        - Field and step counts
        - URL to create new forms
        """),
        responses={
            200: OpenApiResponse(description=_("List of active forms")),
            401: OpenApiResponse(description=AUTH_REQUIRED),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    )
    def get(self, request):
        forms = (
            Form.objects.filter(is_active=True)
            .annotate(
                num_fields=Count("fields", distinct=True),
                num_steps=Count("steps", distinct=True),
            )
            .order_by("name")
        )

        forms_data = []
        for form in forms:
            forms_data.append(
                {
                    "id": form.pk,
                    "slug": form.slug,
                    "name": form.name,
                    "title": form.title,
                    "is_multi_step": form.is_multi_step,
                    "field_count": form.num_fields,
                    "step_count": form.num_steps if form.is_multi_step else 1,
                }
            )

        return Response(
            {
                "forms": forms_data,
                "create_url": reverse("form_builder:create_form"),
            }
        )


class FormDetailView(HeadlessAPIMixin, APIView):
    """
    GET /api/form-builder/forms/<slug>/
    Retrieve form structure for rendering
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Form Builder"],
        summary=_("Get form structure for rendering"),
        description=_("""Retrieves the complete form structure including fields, steps, and conditional rules
        for rendering on the frontend.

        **Authentication:** Public (AllowAny), unless form requires login

        **Response includes:**
        - Form metadata (title, description, button text, messages)
        - All fields with validation rules and options
        - Steps data for multi-step forms
        - Conditional rules for dynamic field behavior
        """),
        parameters=[
            OpenApiParameter(
                name="slug",
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Form slug identifier"),
            )
        ],
        responses={
            200: OpenApiResponse(description=_("Form structure with fields, steps, and rules")),
            401: OpenApiResponse(description=_("Authentication required (if form requires login)")),
            404: OpenApiResponse(description=_("Form not found or inactive")),
        },
    )
    def get(self, request, slug):
        form = get_object_or_404(Form, slug=slug, is_active=True)

        # Check login requirement
        if (login_required := _login_required_response(form, request)) is not None:
            return login_required

        # Build form structure
        fields_data = []
        for field in form.fields.all().select_related("step").order_by("step__order", "order"):
            field_data = {
                "id": field.pk,
                "field_name": field.field_name,
                "field_type": field.field_type,
                "label": field.translated_label,
                "placeholder": field.translated_placeholder,
                "help_text": field.translated_help_text,
                "is_required": field.is_required,
                "width": field.width,
                "order": field.order,
                "default_value": field.default_value,
            }

            # Add validation rules
            if field.min_length:
                field_data["min_length"] = field.min_length
            if field.max_length:
                field_data["max_length"] = field.max_length
            if field.min_value is not None:
                field_data["min_value"] = float(field.min_value)
            if field.max_value is not None:
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

            # Add step info
            if field.step:
                field_data["step"] = {
                    "id": field.step.pk,
                    "title": field.step.get_translated_field("title") or field.step.title,
                    "order": field.step.order,
                }

            fields_data.append(field_data)

        # Build steps data
        steps_data = []
        if form.is_multi_step:
            for step in form.steps.all().order_by("order"):
                steps_data.append(
                    {
                        "id": step.pk,
                        "title": step.get_translated_field("title") or step.title,
                        "description": step.get_translated_field("description") or step.description,
                        "order": step.order,
                        "is_skippable": step.is_skippable,
                        "next_button_text": step.get_translated_field("next_button_text")
                        or step.next_button_text,
                        "back_button_text": step.get_translated_field("back_button_text")
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

            # Add target based on action type
            if rule.target_field:
                rule_data["target_field_id"] = rule.target_field_id
                rule_data["target_field_name"] = rule.target_field.field_name
            if rule.target_step:
                rule_data["target_step_id"] = rule.target_step_id
                rule_data["target_step_order"] = rule.target_step.order

            # Add action value if present
            if rule.action_value:
                rule_data["action_value"] = rule.action_value

            rules_data.append(rule_data)

        return Response(
            {
                "id": form.pk,
                "slug": form.slug,
                "title": form.translated_title,
                "description": form.translated_description,
                "submit_button_text": form.translated_submit_button_text,
                "success_message": form.translated_success_message,
                "error_message": form.translated_error_message,
                "is_multi_step": form.is_multi_step,
                "require_login": form.require_login,
                "spam_protection": form.spam_protection,
                "save_partial_responses": form.save_partial_responses,
                "steps": steps_data,
                "fields": fields_data,
                "rules": rules_data,
            }
        )


class FormSubmitView(HeadlessAPIMixin, APIView):
    """
    POST /api/form-builder/forms/<slug>/submit/
    Submit form response
    """

    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "public_write"

    @extend_schema(
        tags=["Form Builder"],
        summary=_("Submit form response"),
        description=_("""Submits a completed form response. Validates required fields and creates
        a form response record.

        **Authentication:** Public (AllowAny), unless form requires login

        **Request body:** JSON object with field_name: value pairs matching form fields

        **Side effects:**
        - Creates FormResponse record
        - Records IP address, user agent, and referrer for analytics
        - Future: Triggers form actions (email notifications, webhooks)
        """),
        parameters=[
            OpenApiParameter(
                name="slug",
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Form slug identifier"),
            )
        ],
        responses={
            200: OpenApiResponse(description=_("Form submitted successfully with response ID")),
            400: OpenApiResponse(description=_("Validation errors - required fields missing")),
            401: OpenApiResponse(description=_("Authentication required (if form requires login)")),
            404: OpenApiResponse(description=_("Form not found or inactive")),
        },
    )
    def post(self, request, slug):
        form = get_object_or_404(Form, slug=slug, is_active=True)

        # Check login requirement
        if (login_required := _login_required_response(form, request)) is not None:
            return login_required

        from .validation import check_spam, validate_submission

        # Spam protection (honeypot / reCAPTCHA), enforced server-side. A tripped
        # honeypot returns a benign success without storing so bots can't tune,
        # while a failed reCAPTCHA is an explicit error.
        spam = check_spam(form, request)
        if spam == "spam_detected":
            return Response({"success": True, "message": form.translated_success_message})
        if spam == "recaptcha_failed":
            return Response(
                {"errors": {"__all__": _("Spam verification failed. Please try again.")}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Normalize QueryDict (FormData) to a plain dict of single values, then
        # validate against the form definition: type/length/regex/choice checks,
        # conditional required/hidden/set-value rules, and whitelist to declared
        # fields only (never store arbitrary posted keys).
        from django.http import QueryDict

        raw = request.data
        if isinstance(raw, QueryDict):
            submitted = {}
            for key in raw:
                vals = raw.getlist(key)
                submitted[key] = vals if len(vals) > 1 else raw.get(key)
        elif isinstance(raw, dict):
            submitted = dict(raw)
        else:
            return Response(
                {"errors": {"__all__": _("Invalid request body.")}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        clean_data, errors = validate_submission(form, submitted)
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Create response
        response = FormResponse.objects.create(
            form=form,
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key or "",
            data=clean_data,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            referrer=request.META.get("HTTP_REFERER", "")[:500],
            language=request.LANGUAGE_CODE if hasattr(request, "LANGUAGE_CODE") else "",
            status="completed",
            submitted_at=timezone.now(),
            completed_at=timezone.now(),
        )

        # Execute form actions asynchronously (email, webhook, etc.)
        from .tasks import execute_form_actions

        execute_form_actions.delay(response.pk)

        return Response(
            {
                "success": True,
                "message": form.translated_success_message,
                "response_id": response.pk,
            }
        )

    def get_client_ip(self, request):
        """Get client IP address from request"""
        # Use the proxy-aware helper so a spoofed X-Forwarded-For can't poison
        # the stored IP (it skips private/invalid hops).
        from geoip.utils.ip_utils import get_client_ip as _trusted_client_ip

        return _trusted_client_ip(request)


class SavePartialView(HeadlessAPIMixin, APIView):
    """
    POST /api/form-builder/forms/<slug>/partial/
    Save partial form response (for multi-step forms)
    """

    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        tags=["Form Builder"],
        summary=_("Save partial form response"),
        description=_("""Saves a partial/draft form response for multi-step forms. Allows users to
        save progress and resume later.

        **Authentication:** Public (AllowAny)

        **Request body:**
        - response_id (optional): Existing draft response ID to update
        - current_step: Current step number
        - data: Object with field values to save

        **Behavior:**
        - If response_id provided: Updates existing draft
        - If no response_id: Creates new draft response
        - Only works if form has save_partial_responses enabled
        """),
        parameters=[
            OpenApiParameter(
                name="slug",
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Form slug identifier"),
            )
        ],
        responses={
            200: OpenApiResponse(
                description=_("Partial response saved with response ID and current step")
            ),
            400: OpenApiResponse(description=_("Partial responses not enabled for this form")),
            404: OpenApiResponse(description=_("Form or existing response not found")),
        },
    )
    def post(self, request, slug):
        form = get_object_or_404(Form, slug=slug, is_active=True)

        # Check login requirement
        if (login_required := _login_required_response(form, request)) is not None:
            return login_required

        if not form.save_partial_responses:
            return Response(
                {"error": "Partial responses not enabled for this form"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_id = request.data.get("response_id")

        # Validate current_step: reject non-integers, negatives, and steps that
        # fall outside the form's available steps before it reaches the DB.
        current_step = _coerce_int(request.data.get("current_step", 1))
        max_step = form.steps.count() if form.is_multi_step else 1
        if current_step is None or current_step < 1 or (max_step and current_step > max_step):
            return Response(
                {"errors": {"current_step": "Invalid step"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.get("data", {})
        if not isinstance(data, dict):
            return Response(
                {"errors": {"data": "Invalid data payload"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Keep drafts to declared field names only — never store arbitrary keys.
        known = set(form.fields.values_list("field_name", flat=True))
        data = {k: v for k, v in data.items() if k in known}

        # Ensure a session exists so anonymous drafts can be scoped to their owner.
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key or ""

        if response_id:
            # Coerce to int up front so a non-numeric id yields a handled 404
            # rather than an unhandled ValueError from the pk lookup.
            response_pk = _coerce_int(response_id)
            if response_pk is None or response_pk < 1:
                return Response({"error": "Response not found"}, status=status.HTTP_404_NOT_FOUND)
            # Scope the draft to its owner (authenticated user, else session) so a
            # sequential id can't be used to overwrite another user's draft (IDOR).
            lookup = {"pk": response_pk, "form": form, "status": "draft"}
            if request.user.is_authenticated:
                lookup["user"] = request.user
            else:
                lookup["session_key"] = session_key
            try:
                response = FormResponse.objects.get(**lookup)
            except FormResponse.DoesNotExist:
                return Response({"error": "Response not found"}, status=status.HTTP_404_NOT_FOUND)
            response.data.update(data)
            response.current_step = current_step
            response.save(update_fields=["data", "current_step"])
        else:
            # Create new draft response
            response = FormResponse.objects.create(
                form=form,
                user=request.user if request.user.is_authenticated else None,
                session_key=session_key,
                data=data,
                ip_address=self.get_client_ip(request),
                current_step=current_step,
                status="draft",
            )

        return Response(
            {
                "success": True,
                "response_id": response.pk,
                "current_step": response.current_step,
            }
        )

    def get_client_ip(self, request):
        # Use the proxy-aware helper so a spoofed X-Forwarded-For can't poison
        # the stored IP (it skips private/invalid hops).
        from geoip.utils.ip_utils import get_client_ip as _trusted_client_ip

        return _trusted_client_ip(request)


class FileUploadView(HeadlessAPIMixin, APIView):
    """
    POST /api/form-builder/forms/<slug>/upload/
    Upload file for a file field
    """

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=["Form Builder"],
        summary=_("Upload file for form field"),
        description=_("""Uploads a file for a file-type form field. Validates file size and type
        against field configuration.

        **Authentication:** Public (AllowAny)

        **Request (multipart/form-data):**
        - field_name: Name of the file field
        - file: The file to upload

        **Validation:**
        - Checks file size against field's max_size_mb setting
        - Checks file extension against field's allowed_types list
        - Returns error if validation fails

        **Response:**
        - file_path: Storage path of uploaded file
        - file_name: Original filename
        - file_size: File size in bytes
        """),
        parameters=[
            OpenApiParameter(
                name="slug",
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Form slug identifier"),
            )
        ],
        responses={
            200: OpenApiResponse(
                description=_("File uploaded successfully with path and metadata")
            ),
            400: OpenApiResponse(
                description=_("Validation error - no file, invalid field, size/type exceeded")
            ),
            404: OpenApiResponse(description=_("Form not found or inactive")),
        },
    )
    def post(self, request, slug):
        form = get_object_or_404(Form, slug=slug, is_active=True)

        # Check login requirement
        if (login_required := _login_required_response(form, request)) is not None:
            return login_required

        field_name = request.data.get("field_name")
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Get field configuration
        try:
            field = form.fields.get(field_name=field_name, field_type="file")
        except FormField.DoesNotExist:
            return Response({"error": "Invalid field"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file
        file_config = field.file_config or {}
        max_size_mb = file_config.get("max_size_mb", 5)
        allowed_types = file_config.get("allowed_types", [])

        # Check file size
        if file.size > max_size_mb * 1024 * 1024:
            return Response(
                {"error": f"File size exceeds {max_size_mb}MB limit"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deny-by-default type check + magic-byte content sniff + safe filename.
        from .upload_security import UploadRejected, safe_stored_name, validate_upload

        try:
            ext = validate_upload(file, allowed_types)
        except UploadRejected as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Save file under a sanitised, non-traversable path.
        from django.core.files.storage import default_storage

        filename = safe_stored_name(form.slug, file.name, ext)
        path = default_storage.save(f"form_uploads/{filename}", file)

        return Response(
            {
                "success": True,
                "file_path": path,
                "file_name": file.name,
                "file_size": file.size,
            }
        )
