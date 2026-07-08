---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Password Reset Request

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Password Reset Request
        </mj-text>
        <mj-text>
          We received a request to reset your password. Click the button below to reset it.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Reset Password
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          If you didn't request this, you can safely ignore this email.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          This link will expire in {{ expiry_hours }} hours.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Password Reset Request

We received a request to reset your password. Click the link below to reset it.

{{ reset_url }}

If you didn't request this, you can safely ignore this email.
This link will expire in {{ expiry_hours }} hours.
