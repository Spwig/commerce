---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Bestätigen Sie Ihre E-Mail-Adresse

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Bestätigen Sie Ihre E-Mail
        </mj-text>
        <mj-text>
          Bitte bestätigen Sie Ihre E-Mail-Adresse, indem Sie auf den untenstehenden Button klicken.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          E-Mail bestätigen
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Dieser Link wird in {{ expiry_hours }} Stunden ablaufen.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bestätigen Sie Ihre E-Mail

Bitte bestätigen Sie Ihre E-Mail-Adresse, indem Sie auf den untenstehenden Link klicken.

{{ verification_url }}

Dieser Link wird in {{ expiry_hours }} Stunden ablaufen.