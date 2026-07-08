---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
ยืนยันอีเมลของคุณ

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Verify Your Email
        </mj-text>
        <mj-text>
          Please verify your email address by clicking the button below.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Verify Email
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          This link will expire in {{ expiry_hours }} hours.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Verify Your Email

Please verify your email address by clicking the link below.

{{ verification_url }}

This link will expire in {{ expiry_hours }} hours.