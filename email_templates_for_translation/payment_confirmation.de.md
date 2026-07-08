---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Zahlung bestätigt - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Zahlung bestätigt
        </mj-text>
        <mj-text>
          Ihre Zahlung für Bestellung #{{ order_number }} wurde erfolgreich verarbeitet.
        </mj-text>
        <mj-text>
          <strong>Zahlungsbetrag:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Zahlungsmethode:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Zahlung bestätigt

Ihre Zahlung für Bestellung #{{ order_number }} wurde erfolgreich verarbeitet.

Zahlungsbetrag: {{ amount_paid }}
Zahlungsmethode: {{ payment_method }}

