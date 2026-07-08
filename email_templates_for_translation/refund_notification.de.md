---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Rückzahlung verarbeitet - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Rückzahlung verarbeitet
        </mj-text>
        <mj-text>
          Eine Rückzahlung wurde für die Bestellung #{{ order_number }} verarbeitet.
        </mj-text>
        <mj-text>
          <strong>Rückzahlungsbetrag:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          Die Rückzahlung wird in Ihrem Konto innerhalb von {{ refund_days }} Werktagen angezeigt.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rückzahlung verarbeitet

Eine Rückzahlung wurde für die Bestellung #{{ order_number }} verarbeitet.

Rückzahlungsbetrag: {{ refund_amount }}

Die Rückzahlung wird in Ihrem Konto innerhalb von {{ refund_days }} Werktagen angezeigt.