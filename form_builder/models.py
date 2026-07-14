"""
Form Builder Models

A powerful form creation system for merchants with:
- Multiple field types (text, email, select, checkbox, radio, file, ratings, etc.)
- Multi-step forms with progress indicators
- Conditional logic and dependency paths
- Translatable field labels
- Form actions (email, webhook, database, newsletter)
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteModel


class Form(SoftDeleteModel):
    """Main form definition"""

    SPAM_PROTECTION_CHOICES = [
        ("none", _("None")),
        ("honeypot", _("Honeypot Field")),
        ("recaptcha", _("Google reCAPTCHA")),
    ]

    # Identity
    name = models.CharField(
        _("Internal Name"),
        max_length=255,
        help_text=_("Internal name for identification (not displayed to users)"),
    )
    slug = models.SlugField(
        _("Slug"), unique=True, help_text=_("URL-friendly identifier for the form")
    )

    # Display content (translatable via JSONField)
    title = models.CharField(
        _("Form Title"), max_length=255, help_text=_("Title displayed to users")
    )
    description = models.TextField(
        _("Description"), blank=True, help_text=_("Optional description shown above the form")
    )
    submit_button_text = models.CharField(_("Submit Button Text"), max_length=100, default="Submit")

    # Messages (translatable via JSONField)
    success_message = models.TextField(
        _("Success Message"),
        default="Thank you for your submission!",
        help_text=_("Message shown after successful submission"),
    )
    error_message = models.TextField(
        _("Error Message"),
        default="Something went wrong. Please try again.",
        help_text=_("Message shown when submission fails"),
    )

    # Settings
    is_active = models.BooleanField(
        _("Active"), default=True, help_text=_("Only active forms can receive submissions")
    )
    is_multi_step = models.BooleanField(
        _("Multi-step Form"), default=False, help_text=_("Enable multi-step form with sections")
    )
    require_login = models.BooleanField(
        _("Require Login"), default=False, help_text=_("Users must be logged in to submit")
    )
    save_partial_responses = models.BooleanField(
        _("Save Partial Responses"),
        default=False,
        help_text=_("Allow users to save progress and continue later"),
    )

    # Spam protection
    spam_protection = models.CharField(
        _("Spam Protection"), max_length=20, choices=SPAM_PROTECTION_CHOICES, default="honeypot"
    )
    recaptcha_site_key = models.CharField(
        _("reCAPTCHA Site Key"),
        max_length=255,
        blank=True,
        help_text=_("Required when using reCAPTCHA protection"),
    )
    recaptcha_secret_key = models.CharField(
        _("reCAPTCHA Secret Key"),
        max_length=255,
        blank=True,
        help_text=_("Required when using reCAPTCHA protection"),
    )

    # Translations storage
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Translations for form content in different languages"),
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    def get_translated_field(self, field_name, language_code=None):
        """
        Get translated value for a field with fallback logic.

        Args:
            field_name: Name of the field (title, description, etc.)
            language_code: Target language. If None, uses current language.

        Returns:
            Translated value or original field value as fallback.
        """
        from django.utils import translation

        if not language_code:
            language_code = translation.get_language()

        # Normalize language code (e.g., 'en-us' -> 'en')
        if language_code and "-" in language_code:
            base_code = language_code.split("-")[0]
        else:
            base_code = language_code

        # Check translations JSONField
        if self.translations:
            # Try exact match
            if language_code in self.translations:
                value = self.translations[language_code].get(field_name)
                if value:
                    return value
            # Try base language
            if base_code in self.translations:
                value = self.translations[base_code].get(field_name)
                if value:
                    return value

        # Fallback to original field
        return getattr(self, field_name, "")

    @property
    def translated_title(self):
        return self.get_translated_field("title") or self.title

    @property
    def translated_description(self):
        return self.get_translated_field("description") or self.description

    @property
    def translated_submit_button_text(self):
        return self.get_translated_field("submit_button_text") or self.submit_button_text

    @property
    def translated_success_message(self):
        return self.get_translated_field("success_message") or self.success_message

    @property
    def translated_error_message(self):
        return self.get_translated_field("error_message") or self.error_message

    @property
    def field_count(self):
        """Return the number of fields in this form"""
        return self.fields.count()

    @property
    def step_count(self):
        """Return the number of steps in this form"""
        return self.steps.count() if self.is_multi_step else 1

    @property
    def response_count(self):
        """Return the number of responses to this form"""
        return self.responses.filter(status="completed").count()


class FormStep(models.Model):
    """A step/section in a multi-step form"""

    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="steps", verbose_name=_("Form")
    )

    # Display
    title = models.CharField(_("Step Title"), max_length=255)
    description = models.TextField(_("Step Description"), blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    # Navigation
    is_skippable = models.BooleanField(
        _("Skippable"), default=False, help_text=_("Allow users to skip this step")
    )
    next_button_text = models.CharField(_("Next Button Text"), max_length=50, default="Next")
    back_button_text = models.CharField(_("Back Button Text"), max_length=50, default="Back")

    # Translations
    translations = models.JSONField(
        default=dict, blank=True, help_text=_("Translations for step content")
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Form Step")
        verbose_name_plural = _("Form Steps")
        ordering = ["order"]
        unique_together = [["form", "order"]]

    def __str__(self):
        return f"{self.form.name} - Step {self.order + 1}: {self.title}"

    def get_translated_field(self, field_name, language_code=None):
        """Get translated value for a field with fallback logic."""
        from django.utils import translation

        if not language_code:
            language_code = translation.get_language()

        if language_code and "-" in language_code:
            base_code = language_code.split("-")[0]
        else:
            base_code = language_code

        if self.translations:
            if language_code in self.translations:
                value = self.translations[language_code].get(field_name)
                if value:
                    return value
            if base_code in self.translations:
                value = self.translations[base_code].get(field_name)
                if value:
                    return value

        return getattr(self, field_name, "")

    @property
    def translated_title(self):
        return self.get_translated_field("title") or self.title

    @property
    def translated_description(self):
        return self.get_translated_field("description") or self.description

    @property
    def translated_next_button_text(self):
        return self.get_translated_field("next_button_text") or self.next_button_text

    @property
    def translated_back_button_text(self):
        return self.get_translated_field("back_button_text") or self.back_button_text


class FormField(models.Model):
    """Individual field in a form"""

    FIELD_TYPES = [
        # Basic inputs
        ("text", _("Single Line Text")),
        ("textarea", _("Multi-line Text")),
        ("email", _("Email Address")),
        ("phone", _("Phone Number")),
        ("number", _("Number")),
        ("url", _("URL")),
        ("date", _("Date")),
        ("time", _("Time")),
        ("datetime", _("Date & Time")),
        # Selection fields
        ("select", _("Dropdown Select")),
        ("checkbox", _("Checkbox")),
        ("checkbox_group", _("Checkbox Group")),
        ("radio", _("Radio Buttons")),
        # Advanced fields
        ("file", _("File Upload")),
        ("product_select", _("Product Selector")),
        ("rating_stars", _("Star Rating")),
        ("rating_likert", _("Likert Scale")),
        ("rating_nps", _("Net Promoter Score")),
        # Layout/Display
        ("heading", _("Section Heading")),
        ("paragraph", _("Descriptive Text")),
        ("divider", _("Divider Line")),
        ("hidden", _("Hidden Field")),
    ]

    WIDTH_CHOICES = [
        ("full", _("Full Width")),
        ("half", _("Half Width")),
        ("third", _("One Third")),
    ]

    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="fields", verbose_name=_("Form")
    )
    step = models.ForeignKey(
        FormStep,
        on_delete=models.SET_NULL,
        related_name="fields",
        null=True,
        blank=True,
        verbose_name=_("Step"),
        help_text=_("For multi-step forms, which step this field belongs to"),
    )

    # Field identity
    field_name = models.CharField(
        _("Field Name"),
        max_length=100,
        help_text=_("Machine name (no spaces, used in data storage)"),
    )
    field_type = models.CharField(_("Field Type"), max_length=30, choices=FIELD_TYPES)

    # Display (translatable)
    label = models.CharField(_("Label"), max_length=255)
    placeholder = models.CharField(_("Placeholder"), max_length=255, blank=True)
    help_text = models.CharField(_("Help Text"), max_length=500, blank=True)

    # Validation
    is_required = models.BooleanField(_("Required"), default=False)
    min_length = models.PositiveIntegerField(_("Minimum Length"), null=True, blank=True)
    max_length = models.PositiveIntegerField(_("Maximum Length"), null=True, blank=True)
    min_value = models.DecimalField(
        _("Minimum Value"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_value = models.DecimalField(
        _("Maximum Value"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    validation_regex = models.CharField(
        _("Validation Pattern"),
        max_length=500,
        blank=True,
        help_text=_("Regular expression for custom validation"),
    )
    validation_message = models.CharField(_("Validation Error Message"), max_length=255, blank=True)

    # Options (for select, radio, checkbox_group, likert)
    options = models.JSONField(
        _("Options"),
        default=list,
        blank=True,
        help_text=_("Options for select, radio, or checkbox group fields"),
    )

    # Rating field config
    rating_config = models.JSONField(
        _("Rating Configuration"),
        default=dict,
        blank=True,
        help_text=_("Configuration for star rating, Likert, or NPS fields"),
    )

    # File upload config
    file_config = models.JSONField(
        _("File Upload Configuration"),
        default=dict,
        blank=True,
        help_text=_("Allowed file types, max size, max files"),
    )

    # Product select config
    product_config = models.JSONField(
        _("Product Selector Configuration"),
        default=dict,
        blank=True,
        help_text=_("Category filters, max selections, display options"),
    )

    # Default value
    default_value = models.TextField(
        _("Default Value"), blank=True, help_text=_("Default value for the field")
    )

    # Layout
    order = models.PositiveIntegerField(_("Order"), default=0)
    width = models.CharField(_("Width"), max_length=20, choices=WIDTH_CHOICES, default="full")
    css_class = models.CharField(
        _("CSS Class"),
        max_length=100,
        blank=True,
        help_text=_("Additional CSS classes for styling"),
    )

    # Translations
    translations = models.JSONField(
        default=dict, blank=True, help_text=_("Translations for field labels and help text")
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Form Field")
        verbose_name_plural = _("Form Fields")
        ordering = ["step__order", "order"]

    def __str__(self):
        return f"{self.form.name} - {self.label}"

    def get_translated_field(self, field_name, language_code=None):
        """Get translated value for a field with fallback logic."""
        from django.utils import translation

        if not language_code:
            language_code = translation.get_language()

        if language_code and "-" in language_code:
            base_code = language_code.split("-")[0]
        else:
            base_code = language_code

        if self.translations:
            if language_code in self.translations:
                value = self.translations[language_code].get(field_name)
                if value:
                    return value
            if base_code in self.translations:
                value = self.translations[base_code].get(field_name)
                if value:
                    return value

        return getattr(self, field_name, "")

    @property
    def translated_label(self):
        return self.get_translated_field("label") or self.label

    @property
    def translated_placeholder(self):
        return self.get_translated_field("placeholder") or self.placeholder

    @property
    def translated_help_text(self):
        return self.get_translated_field("help_text") or self.help_text


class FormResponse(models.Model):
    """A submitted form response"""

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("submitted", _("Submitted")),
        ("processing", _("Processing")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
    ]

    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="responses", verbose_name=_("Form")
    )

    # Submitter info
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="form_responses",
        verbose_name=_("User"),
    )
    session_key = models.CharField(
        _("Session Key"), max_length=40, blank=True, help_text=_("For anonymous submissions")
    )

    # Response data
    data = models.JSONField(
        _("Response Data"), default=dict, help_text=_("Field values submitted by the user")
    )

    # Metadata
    ip_address = models.GenericIPAddressField(_("IP Address"), null=True, blank=True)
    user_agent = models.TextField(_("User Agent"), blank=True)
    referrer = models.URLField(_("Referrer"), blank=True, max_length=500)
    language = models.CharField(_("Language"), max_length=10, blank=True)

    # Progress (for multi-step)
    current_step = models.PositiveIntegerField(_("Current Step"), default=1)
    completed_steps = models.JSONField(_("Completed Steps"), default=list, blank=True)

    # Status tracking
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="submitted"
    )
    action_results = models.JSONField(
        _("Action Results"),
        default=dict,
        blank=True,
        help_text=_("Results of form actions (email sent, webhook triggered, etc.)"),
    )

    # Timestamps
    started_at = models.DateTimeField(_("Started"), auto_now_add=True)
    submitted_at = models.DateTimeField(_("Submitted"), null=True, blank=True)
    completed_at = models.DateTimeField(_("Completed"), null=True, blank=True)

    # Analytics
    time_to_complete = models.PositiveIntegerField(
        _("Time to Complete (seconds)"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Form Response")
        verbose_name_plural = _("Form Responses")
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["form", "-submitted_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        if self.user:
            return f"{self.form.name} - {self.user.email}"
        return f"{self.form.name} - Anonymous ({self.pk})"

    def get_field_value(self, field_name):
        """Get the value for a specific field"""
        return self.data.get(field_name)

    def get_display_data(self):
        """Get response data with field labels for display"""
        display_data = []
        for field in self.form.fields.all():
            value = self.data.get(field.field_name)
            if value is not None:
                display_data.append(
                    {
                        "label": field.translated_label,
                        "value": value,
                        "field_type": field.field_type,
                    }
                )
        return display_data


class FormConditionalRule(models.Model):
    """
    Conditional logic for showing/hiding fields or steps based on user input.

    Allows merchants to create dynamic forms where certain fields or steps
    appear/hide based on answers to previous questions. Supports branching
    logic for surveys and multi-path forms.

    Examples:
    - IF "contact_method" EQUALS "phone" THEN show "phone_number" field
    - IF "order_type" EQUALS "wholesale" THEN skip to "wholesale_details" step
    - IF "rating" LESS_THAN "3" THEN require "feedback" field
    """

    OPERATOR_CHOICES = [
        ("equals", _("Equals")),
        ("not_equals", _("Does Not Equal")),
        ("contains", _("Contains")),
        ("not_contains", _("Does Not Contain")),
        ("greater_than", _("Greater Than")),
        ("less_than", _("Less Than")),
        ("greater_than_or_equal", _("Greater Than or Equal")),
        ("less_than_or_equal", _("Less Than or Equal")),
        ("is_empty", _("Is Empty")),
        ("is_not_empty", _("Is Not Empty")),
        ("in_list", _("Is One Of")),
        ("not_in_list", _("Is Not One Of")),
        ("starts_with", _("Starts With")),
        ("ends_with", _("Ends With")),
    ]

    ACTION_CHOICES = [
        ("show_field", _("Show Field")),
        ("hide_field", _("Hide Field")),
        ("require_field", _("Make Field Required")),
        ("unrequire_field", _("Make Field Optional")),
        ("skip_to_step", _("Skip to Step")),
        ("show_step", _("Show Step")),
        ("hide_step", _("Hide Step")),
        ("set_value", _("Set Field Value")),
    ]

    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="rules", verbose_name=_("Form")
    )

    # Rule metadata
    name = models.CharField(
        _("Rule Name"),
        max_length=255,
        blank=True,
        help_text=_("Optional description of what this rule does"),
    )
    is_active = models.BooleanField(
        _("Active"), default=True, help_text=_("Inactive rules are not evaluated")
    )

    # Condition (source)
    source_field = models.ForeignKey(
        FormField,
        on_delete=models.CASCADE,
        related_name="source_rules",
        verbose_name=_("Source Field"),
        help_text=_("The field whose value triggers this rule"),
    )
    operator = models.CharField(
        _("Operator"), max_length=25, choices=OPERATOR_CHOICES, default="equals"
    )
    value = models.JSONField(
        _("Comparison Value"),
        default=dict,
        blank=True,
        help_text=_(
            'Value to compare against. Can be single value or list for "in_list" operators.'
        ),
    )

    # Action (target)
    action = models.CharField(
        _("Action"), max_length=25, choices=ACTION_CHOICES, default="show_field"
    )
    target_field = models.ForeignKey(
        FormField,
        on_delete=models.CASCADE,
        related_name="target_rules",
        null=True,
        blank=True,
        verbose_name=_("Target Field"),
        help_text=_("Field affected by this rule (for field-related actions)"),
    )
    target_step = models.ForeignKey(
        FormStep,
        on_delete=models.CASCADE,
        related_name="target_rules",
        null=True,
        blank=True,
        verbose_name=_("Target Step"),
        help_text=_("Step affected by this rule (for step-related actions)"),
    )
    action_value = models.JSONField(
        _("Action Value"),
        default=dict,
        blank=True,
        help_text=_("Additional data for the action (e.g., value to set)"),
    )

    # Priority for complex rule chains
    priority = models.PositiveIntegerField(
        _("Priority"), default=0, help_text=_("Rules with higher priority are evaluated first")
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Conditional Rule")
        verbose_name_plural = _("Conditional Rules")
        ordering = ["-priority", "id"]
        indexes = [
            models.Index(fields=["form", "is_active"]),
            models.Index(fields=["source_field"]),
        ]

    def __str__(self):
        if self.name:
            return f"{self.form.name} - {self.name}"
        return f"{self.form.name} - Rule #{self.pk}"

    def clean(self):
        """Validate that target_field or target_step is set based on action type"""
        from django.core.exceptions import ValidationError

        field_actions = [
            "show_field",
            "hide_field",
            "require_field",
            "unrequire_field",
            "set_value",
        ]
        step_actions = ["skip_to_step", "show_step", "hide_step"]

        if self.action in field_actions and not self.target_field:
            raise ValidationError({"target_field": _("Target field is required for this action.")})

        if self.action in step_actions and not self.target_step:
            raise ValidationError({"target_step": _("Target step is required for this action.")})

    def evaluate(self, field_value):
        """
        Evaluate if this rule's condition is met.

        Args:
            field_value: The current value of the source field

        Returns:
            bool: True if the condition is met, False otherwise
        """
        comparison_value = self.value.get("value") if isinstance(self.value, dict) else self.value

        # Handle empty checks first
        if self.operator == "is_empty":
            return field_value is None or field_value == "" or field_value == []
        if self.operator == "is_not_empty":
            return field_value is not None and field_value != "" and field_value != []

        # Convert to string for string comparisons
        str_field_value = str(field_value) if field_value is not None else ""
        str_comparison_value = str(comparison_value) if comparison_value is not None else ""

        if self.operator == "equals":
            return str_field_value.lower() == str_comparison_value.lower()
        elif self.operator == "not_equals":
            return str_field_value.lower() != str_comparison_value.lower()
        elif self.operator == "contains":
            return str_comparison_value.lower() in str_field_value.lower()
        elif self.operator == "not_contains":
            return str_comparison_value.lower() not in str_field_value.lower()
        elif self.operator == "starts_with":
            return str_field_value.lower().startswith(str_comparison_value.lower())
        elif self.operator == "ends_with":
            return str_field_value.lower().endswith(str_comparison_value.lower())

        # Numeric comparisons
        try:
            num_field = float(field_value) if field_value else 0
            num_comparison = float(comparison_value) if comparison_value else 0

            if self.operator == "greater_than":
                return num_field > num_comparison
            elif self.operator == "less_than":
                return num_field < num_comparison
            elif self.operator == "greater_than_or_equal":
                return num_field >= num_comparison
            elif self.operator == "less_than_or_equal":
                return num_field <= num_comparison
        except (ValueError, TypeError):
            # Fall back to string comparison for non-numeric values
            if self.operator in [
                "greater_than",
                "less_than",
                "greater_than_or_equal",
                "less_than_or_equal",
            ]:
                return False

        # List comparisons
        if self.operator in ["in_list", "not_in_list"]:
            comparison_list = self.value.get("list", []) if isinstance(self.value, dict) else []
            # Normalize to lowercase strings
            normalized_list = [str(v).lower() for v in comparison_list]
            if self.operator == "in_list":
                return str_field_value.lower() in normalized_list
            else:
                return str_field_value.lower() not in normalized_list

        return False

    def get_action_display_text(self):
        """Get human-readable description of this rule"""
        source = self.source_field.label if self.source_field else "?"
        operator_display = dict(self.OPERATOR_CHOICES).get(self.operator, self.operator)
        action_display = dict(self.ACTION_CHOICES).get(self.action, self.action)

        # Format the value for display
        if isinstance(self.value, dict):
            value_display = self.value.get("value", self.value.get("list", ""))
        else:
            value_display = self.value

        # Format the target
        if self.target_field:
            target_display = self.target_field.label
        elif self.target_step:
            target_display = self.target_step.title
        else:
            target_display = "?"

        return f"IF {source} {operator_display} '{value_display}' THEN {action_display} '{target_display}'"


class FormAction(models.Model):
    """
    Actions triggered after form submission.

    Supports email notifications, auto-reply emails, and webhook POST requests.
    Actions are executed asynchronously via Celery after a form response is created.
    """

    ACTION_TYPES = [
        ("email_notification", _("Email Notification")),
        ("auto_reply", _("Auto-Reply Email")),
        ("webhook", _("Webhook")),
    ]

    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="actions", verbose_name=_("Form")
    )
    action_type = models.CharField(_("Action Type"), max_length=30, choices=ACTION_TYPES)
    name = models.CharField(
        _("Action Name"), max_length=255, help_text=_("Descriptive name for this action")
    )
    is_active = models.BooleanField(_("Active"), default=True)

    # Type-specific configuration stored as JSON
    # email_notification: {to_emails: [], subject_template: "", body_template: "", include_data: true}
    # auto_reply: {email_field: "email", subject: "", body_template: ""}
    # webhook: {url: "", method: "POST", headers: {}, include_fields: [], secret: ""}
    config = models.JSONField(
        _("Configuration"), default=dict, help_text=_("Action-specific configuration")
    )

    order = models.PositiveIntegerField(_("Order"), default=0)

    # Timestamps
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Form Action")
        verbose_name_plural = _("Form Actions")
        ordering = ["order"]
        indexes = [
            models.Index(fields=["form", "is_active"]),
        ]

    def __str__(self):
        return f"{self.form.name} - {self.name}"
