---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Verifica il tuo indirizzo email

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Verifica il tuo email
        </mj-text>
        <mj-text>
          Per verificare il tuo indirizzo email, fai clic sul pulsante qui sotto.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Verifica email
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Questo link scadrà tra {{ expiry_hours }} ore.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Verifica il tuo email

Per verificare il tuo indirizzo email, fai clic sul link qui sotto.

{{ verification_url }}

Questo link scadrà tra {{ expiry_hours }} ore.