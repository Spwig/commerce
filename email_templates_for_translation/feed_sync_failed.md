---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ {{ feed_name }} sync failed to {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Sync Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sync Error
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Failed to sync {{ feed_name }} to {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Failure Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Common Causes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Invalid API credentials or expired token<br/>
          • Network connectivity issues<br/>
          • Platform API rate limits exceeded<br/>
          • Feed format doesn't meet platform requirements
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Recommended Action
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Retry Sync
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Check Feed Settings
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SYNC FAILED

Sync Error

Failed to sync {{ feed_name }} to {{ platform_name }}.

FAILURE DETAILS:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

ERROR MESSAGE:
{{ error_message }}

COMMON CAUSES:
• Invalid API credentials or expired token
• Network connectivity issues
• Platform API rate limits exceeded
• Feed format doesn't meet platform requirements

{% if recommended_action %}
RECOMMENDED ACTION:
{{ recommended_action }}
{% endif %}

Retry sync: {{ retry_url }}
Check feed settings: {{ admin_feed_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| feed_name | Feed display name | Google Shopping Feed |
| platform_name | External platform name | Google Merchant Center |
| failed_at | Failure timestamp | February 15, 2026 at 3:45 PM |
| error_code | Error code | FEED_SYNC_003 |
| error_message | User-friendly error | API authentication failed: invalid access token |
| recommended_action | What to do | Reconnect your Google Merchant Center account in feed settings |
| retry_url | Retry sync URL | https://shop.com/en/admin/feeds/google/sync |
| admin_feed_url | Feed settings page | https://shop.com/en/admin/feeds/google |

## Notes

- CRITICAL admin notification
- Sent immediately on sync failure to external platform
- Includes error details and troubleshooting
- Suggests common causes
- Provides retry action
- Transactional email
