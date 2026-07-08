---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Feed generation failed: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Feed Generation Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Generation Error
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          The {{ feed_name }} product feed failed to generate due to an error.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Error Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
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
          <strong>Error Log:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Common Causes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Missing required product data (title, price, image)<br/>
          • Invalid product data format<br/>
          • Database connection issues<br/>
          • Insufficient disk space or memory
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Retry Generation
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Feed Settings
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If the problem persists, contact support with the error code {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ FEED GENERATION FAILED

Generation Error

The {{ feed_name }} product feed failed to generate due to an error.

ERROR DETAILS:
- Feed: {{ feed_name }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

ERROR MESSAGE:
{{ error_message }}

{% if error_log %}
ERROR LOG:
{{ error_log|truncatewords:30 }}
{% endif %}

COMMON CAUSES:
• Missing required product data (title, price, image)
• Invalid product data format
• Database connection issues
• Insufficient disk space or memory

Retry generation: {{ retry_url }}
View feed settings: {{ admin_feed_url }}

If the problem persists, contact support with error code {{ error_code }}.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| feed_name | Feed display name | Google Shopping Feed |
| failed_at | Failure timestamp | February 15, 2026 at 3:45 PM |
| error_code | Error code | FEED_GEN_001 |
| error_message | User-friendly error | Missing required field 'price' for 23 products |
| error_log | Full error log | Detailed stack trace and error context |
| retry_url | Retry generation URL | https://shop.com/en/admin/feeds/google/generate |
| admin_feed_url | Feed settings page | https://shop.com/en/admin/feeds/google |

## Notes

- CRITICAL admin notification
- Sent immediately on feed generation failure
- Includes error details for troubleshooting
- Suggests common causes and solutions
- Provides retry action
- Transactional email
