---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Verifikasi Alamat Email Anda

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Verifikasi Email Anda
        </mj-text>
        <mj-text>
          Silakan verifikasi alamat email Anda dengan mengklik tombol di bawah ini.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Verifikasi Email
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Tautan ini akan kedaluwarsa dalam {{ expiry_hours }} jam.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Verifikasi Email Anda

Silakan verifikasi alamat email Anda dengan mengklik tautan di bawah ini.

{{ verification_url }}

Tautan ini akan kedaluwarsa dalam {{ expiry_hours }} jam.