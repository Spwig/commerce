---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Neue Bestellung empfangen - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Neue Bestellung empfangen
        </mj-text>
        <mj-text>
          Eine neue Bestellung wurde in Ihrem Geschäft platziert.
        </mj-text>
        <mj-text>
          <strong>Bestellnummer:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Kunde:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Gesamt:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          In der Verwaltung ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Neue Bestellung empfangen

Eine neue Bestellung wurde in Ihrem Geschäft platziert.

Bestellnummer: {{ order_number }}
Kunde: {{ customer_name }}
Gesamt: {{ order_total }}

In der Verwaltung ansehen: {{ admin_order_url }}