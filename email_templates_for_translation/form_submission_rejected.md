---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Update on your {{ form_name }} submission

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Update on Your Submission
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thank you for submitting the {{ form_name }} form. After careful review, we're unable to approve your submission at this time.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Submission Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Submitted:</strong> {{ submission_date }}<br/>
              <strong>Reviewed:</strong> {{ rejection_date }}<br/>
              <strong>Reference #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Reason:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if can_resubmit %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              You Can Resubmit
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ resubmit_instructions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if resubmit_url %}
        <mj-button href="{{ resubmit_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Submit Again
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contact Support
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If you have questions about this decision, please don't hesitate to reach out.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
UPDATE ON YOUR SUBMISSION

Hi {{ submitter_name }},

Thank you for submitting the {{ form_name }} form. After careful review, we're unable to approve your submission at this time.

SUBMISSION DETAILS:
- Form: {{ form_name }}
- Submitted: {{ submission_date }}
- Reviewed: {{ rejection_date }}
- Reference #: {{ submission_id }}

{% if rejection_reason %}
REASON:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
YOU CAN RESUBMIT:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}Submit again: {{ resubmit_url }}{% endif %}
{% if support_url %}Contact support: {{ support_url }}{% endif %}

If you have questions about this decision, please don't hesitate to reach out.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| submitter_name | Submitter's name | John Smith |
| form_name | Form title | Vendor Application |
| submission_date | When submitted | February 15, 2026 |
| rejection_date | When rejected | February 16, 2026 |
| submission_id | Reference number | FORM-2026-001234 |
| rejection_reason | Why rejected | Your application doesn't meet our current vendor criteria |
| can_resubmit | Boolean flag | true |
| resubmit_instructions | How to resubmit | Please address the issues mentioned and resubmit your application |
| resubmit_url | Resubmit form URL | https://shop.com/en/forms/vendor-application |
| support_url | Support contact | https://shop.com/en/contact |

## Notes

- Sent when admin rejects submission
- Professional, respectful tone
- Provides clear rejection reason
- Offers path forward if resubmission allowed
- Use case: applications, registrations, requests
- Transactional email
