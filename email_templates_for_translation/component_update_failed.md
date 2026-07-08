---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Update Failed: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Update Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Installation Error
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          The update for {{ component_name }} to version {{ target_version }} failed to install.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Failure Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Target Version:</strong> {{ target_version }}<br/>
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

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Full Error Log:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What to Do:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Check system requirements and dependencies<br/>
          2. Review the error log for details<br/>
          3. Try installing again, or contact support<br/>
          4. Your store is still running on {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Retry Installation
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contact Support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ UPDATE FAILED

Installation Error

The update for {{ component_name }} to version {{ target_version }} failed to install.

FAILURE DETAILS:
- Component: {{ component_name }}
- Target Version: {{ target_version }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

ERROR MESSAGE:
{{ error_message }}

{% if error_log %}
FULL ERROR LOG:
{{ error_log|truncatewords:50 }}
{% endif %}

WHAT TO DO:
1. Check system requirements and dependencies
2. Review the error log for details
3. Try installing again, or contact support
4. Your store is still running on {{ current_version }}

Retry installation: {{ retry_url }}
Contact support: {{ support_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| component_name | Component display name | Stripe Payment Gateway |
| target_version | Version that failed to install | 1.3.0 |
| current_version | Still-running version | 1.2.0 |
| failed_at | Failure timestamp | February 15, 2026 at 3:45 PM |
| error_code | Error code | COMP_UPDATE_001 |
| error_message | User-friendly error | Installation failed due to missing dependencies |
| error_log | Full error log | Stack trace and detailed error info |
| retry_url | Retry installation URL | https://shop.com/en/admin/components/updates |
| support_url | Support contact | https://shop.com/en/support |

## Notes

- CRITICAL admin notification
- Sent immediately on installation failure
- Includes full error details for troubleshooting
- Store remains on previous version
- Transactional email
