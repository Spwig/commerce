---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Ihre Bestellung #{{ order_number }} ist {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lieferstatus: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gute Nachrichten! Ihre Bestellung hat einen wichtigen Meilenstein auf ihrem Weg zu Ihnen erreicht.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Bestellinformationen:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bestellnummer:</strong> {{ order_number }}<br/>
              <strong>Sendungsnummer:</strong> {{ tracking_number }}<br/>
              <strong>Spediteur:</strong> {{ carrier_name }}<br/>
              <strong>Aktueller Standort:</strong> {{ current_location }}<br/>
              <strong>geschätzte Lieferzeit:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Paket verfolgen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Fragen zu Ihrer Lieferung? <a href="{{ support_url }">Kontaktieren Sie den Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Lieferstatus: {{ milestone_status }}

Hi {{ customer_name }},

Gute Nachrichten! Ihre Bestellung hat einen wichtigen Meilenstein auf ihrem Weg zu Ihnen erreicht.

📦 {{ milestone_status }}
{{ milestone_description }}

BESTELLDATEN:
- Bestellnummer: {{ order_number }}
- Sendungsnummer: {{ tracking_number }}
- Spediteur: {{ carrier_name }}
- Aktueller Standort: {{ current_location }}
- Geschätzte Lieferzeit: {{ estimated_delivery }}

Paket verfolgen: {{ tracking_url }}

Fragen zu Ihrer Lieferung? Kontaktieren Sie den Support: {{ support_url }}
