---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Payment Provider Issue - {{ provider_name }} SDK Failed to Load

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Payment Provider Issue
        </mj-text>
        <mj-text>
          The {{ provider_name }} payment SDK failed to load for a customer during checkout. This may indicate a service disruption with the provider.
        </mj-text>
        <mj-text>
          <strong>Provider:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Error Type:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Time:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Failure Count (last hour):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          This notification is rate-limited to one per provider per hour. If the issue persists, check the provider dashboard or contact their support.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          View Payment Settings
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Payment Provider Issue

The {{ provider_name }} payment SDK failed to load for a customer during checkout. This may indicate a service disruption with the provider.

Provider: {{ provider_name }}
Error Type: {{ error_type }}
Time: {{ timestamp }}
Failure Count (last hour): {{ failure_count }}

This notification is rate-limited to one per provider per hour. If the issue persists, check the provider dashboard or contact their support.

View payment settings: {{ admin_url }}
