---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
New {{ form_name }} Submission from {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 New Form Submission
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          New Submission Received
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A new {{ form_name }} submission has been received.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Submission Info:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Submitted By:</strong> {{ submitter_name }}<br/>
              <strong>Email:</strong> {{ submitter_email }}<br/>
              <strong>Submitted:</strong> {{ submission_date }}<br/>
              <strong>Reference #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Submitted Data:
        </mj-text>

        {% for field in submission_data %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-size="13px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ field.label }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ field.value }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_submission_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View in Admin
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Reply to Submitter
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 NEW FORM SUBMISSION

New Submission Received

A new {{ form_name }} submission has been received.

SUBMISSION INFO:
- Form: {{ form_name }}
- Submitted By: {{ submitter_name }}
- Email: {{ submitter_email }}
- Submitted: {{ submission_date }}
- Reference #: {{ submission_id }}

SUBMITTED DATA:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

View in admin: {{ admin_submission_url }}
{% if reply_to_email %}Reply to submitter: mailto:{{ reply_to_email }}{% endif %}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| form_name | Form title | Contact Form |
| submitter_name | Submitter's name | John Smith |
| submitter_email | Submitter's email | john@example.com |
| submission_date | When submitted | February 15, 2026 at 3:45 PM |
| submission_id | Reference number | FORM-2026-001234 |
| submission_data | Form field data | [{label: 'Message', value: 'I have a question about...'}] |
| admin_submission_url | Admin view link | https://shop.com/en/admin/forms/submissions/1234 |
| reply_to_email | Submitter's email | john@example.com |

## Notes

- Admin notification - sent to form recipients
- Transactional email - always sent
- Includes all submission data
- Quick access to admin panel
- Reply button for convenience
