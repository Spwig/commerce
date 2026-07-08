---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Vérifiez votre adresse e-mail

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Vérifiez votre e-mail
        </mj-text>
        <mj-text>
          Veuillez vérifier votre adresse e-mail en cliquant sur le bouton ci-dessous.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Vérifier l'e-mail
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Ce lien expirera dans {{ expiry_hours }} heures.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Vérifiez votre e-mail

Veuillez vérifier votre adresse e-mail en cliquant sur le lien ci-dessous.

{{ verification_url }}

Ce lien expirera dans {{ expiry_hours }} heures.