---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
E-postanizi Dogrulayin

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          E-postanizi Dogrulayin
        </mj-text>
        <mj-text>
          Lutfen alttaki butona tiklayarak e-posta adresinizi dogrulayin.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          E-posta Dogrula
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Bu link {{ expiry_hours }} saat sonra sona erecektir.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
E-postanizi Dogrulayin

Lutfen alttaki linke tiklayarak e-posta adresinizi dogrulayin.

{{ verification_url }}

Bu link {{ expiry_hours }} saat sonra sona erecektir.