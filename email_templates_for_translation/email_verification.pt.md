---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Verifique Seu Endereço de Email

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Verifique Seu Email
        </mj-text>
        <mj-text>
          Por favor, verifique seu endereço de email clicando no botão abaixo.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Verifique Email
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Este link expirará em {{ expiry_hours }} horas.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Verifique Seu Email

Por favor, verifique seu endereço de email clicando no link abaixo.

{{ verification_url }}

Este link expirará em {{ expiry_hours }} horas.