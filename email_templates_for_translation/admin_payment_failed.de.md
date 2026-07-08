---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Zahlung fehlgeschlagen - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Zahlung fehlgeschlagen
        </mj-text>
        <mj-text>
          Ein Zahlungsversuch ist für die Bestellung #{{ order_number }} fehlgeschlagen.
        </mj-text>
        <mj-text>
          <strong>Kunde:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Betrag:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Fehler:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Im Admin-Panel ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Zahlung fehlgeschlagen

Ein Zahlungsversuch ist für die Bestellung #{{ order_number }} fehlgeschlagen.

Kunde: {{ customer_name }}
Betrag: {{ order_total }}
Fehler: {{ error_message }}

Im Admin-Panel ansehen: {{ admin_order_url }}