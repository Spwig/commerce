"""
Base action executor for form builder actions.
"""

import logging
import re

logger = logging.getLogger(__name__)

# Matches a single ``{{key}}`` placeholder in a template string.
_PLACEHOLDER_RE = re.compile(r"\{\{([^{}]+)\}\}")


class BaseAction:
    """Base class for form action executors."""

    def __init__(self, action, form_response):
        self.action = action
        self.form_response = form_response
        self.config = action.config or {}

    def execute(self):
        """Execute the action. Must be implemented by subclasses."""
        raise NotImplementedError

    def get_form_data_context(self):
        """Build a context dict from the form response data."""
        context = {
            "form_name": self.form_response.form.name,
            "form_title": self.form_response.form.translated_title,
            "response_id": self.form_response.pk,
            "submitted_at": str(self.form_response.submitted_at or ""),
            "submitter_email": "",
            "submitter_name": "",
        }

        # Add all field values
        for field in self.form_response.form.fields.all():
            value = self.form_response.data.get(field.field_name, "")
            context[field.field_name] = value

            # Try to identify email and name fields
            if field.field_type == "email" and value:
                context["submitter_email"] = value
            if field.field_name in ("name", "full_name", "first_name") and value:
                context["submitter_name"] = value

        # Add user info if authenticated
        if self.form_response.user:
            context["submitter_email"] = context["submitter_email"] or self.form_response.user.email
            context["submitter_name"] = context["submitter_name"] or str(self.form_response.user)

        return context

    def render_template_string(self, template_str, context):
        """Render a template string with context variables using simple substitution."""
        if not template_str:
            return ""

        # Single pass over the original template so a submitted value that itself
        # contains ``{{other_field}}`` is inserted literally, not re-substituted.
        def _resolve(match):
            key = match.group(1)
            if key in context:
                return str(context[key])
            return match.group(0)

        return _PLACEHOLDER_RE.sub(_resolve, template_str)
