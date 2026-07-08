---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Passwortzurücksetzung angefordert

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Passwortzurücksetzung angefordert
        </mj-text>
        <mj-text>
          Wir haben einen Antrag zur Zurücksetzung Ihres Passworts erhalten. Klicken Sie auf den untenstehenden Button, um es zurückzusetzen.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Passwort zurücksetzen
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Wenn Sie diese Anfrage nicht gestellt haben, können Sie diese E-Mail sicher ignorieren.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Dieser Link läuft in {{ expiry_hours }} Stunden ab.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Passwortzurücksetzung angefordert

Wir haben einen Antrag zur Zurücksetzung Ihres Passworts erhalten. Klicken Sie auf den untenstehenden Link, um es zurückzusetzen.

{{ reset_url }}

Wenn Sie diese Anfrage nicht gestellt haben, können Sie diese E-Mail sicher ignorieren.
Dieser Link läuft in {{ expiry_hours }} Stunden ab.