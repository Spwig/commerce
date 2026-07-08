---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Translation job failed: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Translation Job Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Translation Error
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Your bulk translation job encountered an error and could not be completed.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Job Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error Message:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Partial Completion
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} of {{ total_items }} items were successfully translated before the error occurred.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Common Causes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Translation service API connection issues<br/>
          • Insufficient translation credits<br/>
          • Invalid or corrupted source content<br/>
          • Unsupported language pair
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Check your translation service settings<br/>
          2. Verify translation credits are available<br/>
          3. Review error message for specific issues<br/>
          4. Retry the translation job
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Retry Translation
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Check Settings
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If the problem persists, contact support with error code {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ TRANSLATION JOB FAILED

Translation Error

Your bulk translation job encountered an error and could not be completed.

JOB DETAILS:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Target Languages: {{ target_languages }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

ERROR MESSAGE:
{{ error_message }}

{% if partial_completion %}
PARTIAL COMPLETION:
{{ items_completed }} of {{ total_items }} items were successfully translated before the error occurred.
{% endif %}

COMMON CAUSES:
• Translation service API connection issues
• Insufficient translation credits
• Invalid or corrupted source content
• Unsupported language pair

RECOMMENDED ACTIONS:
1. Check your translation service settings
2. Verify translation credits are available
3. Review error message for specific issues
4. Retry the translation job

Retry translation: {{ retry_url }}
Check settings: {{ settings_url }}

If the problem persists, contact support with error code {{ error_code }}.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| job_id | Unique job identifier | TJ-2026-001234 |
| content_type | What was being translated | Product Descriptions |
| target_languages | Languages being translated to | French, German, Spanish |
| failed_at | Failure timestamp | February 15, 2026 at 4:15 PM |
| error_code | Error code | TRANS_API_500 |
| error_message | User-friendly error | Translation service API returned error 500: Internal Server Error |
| partial_completion | Boolean flag | true |
| items_completed | Items successfully translated | 157 |
| total_items | Total items in job | 247 |
| retry_url | Retry job URL | https://shop.com/en/admin/translations/retry/12345 |
| settings_url | Translation settings page | https://shop.com/en/admin/translations/settings |

## Notes

- CRITICAL admin notification
- Sent when bulk translation job fails
- Includes error details for troubleshooting
- Shows partial completion if applicable
- Provides retry action
- Links to settings for configuration check
- Transactional email
