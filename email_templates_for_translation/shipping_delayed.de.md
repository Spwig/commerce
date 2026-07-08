---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Aktualisierung zu Ihrer Bestellung #{{ order_number }} - Lieferverzögerung

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aktualisierung zu Ihrer Bestellung
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir möchten Sie über eine Verzögerung bei Ihrer Bestellung informieren. Wir entschuldigen uns für die Unannehmlichkeiten und schätzen Ihre Geduld.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Bestelldetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bestellnummer:</strong> {{ order_number }}<br/>
              <strong>Ursprünglicher Liefertermin:</strong> {{ original_delivery_date }}<br/>
              <strong>Neuer Liefertermin:</strong> {{ new_delivery_date }}<br/>
              <strong>Tracking-Nummer:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grund für die Verzögerung:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bestellung verfolgen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Wir arbeiten daran, Ihre Bestellung so schnell wie möglich zu Ihnen zu schicken. Sie erhalten eine weitere Aktualisierung, sobald Ihr Paket unterwegs ist.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Fragen? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Kontaktieren Sie unser Kundenservice-Team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aktualisierung zu Ihrer Bestellung #{{ order_number }}

Hi {{ customer_name }},

Wir möchten Sie über eine Verzögerung bei Ihrer Bestellung informieren. Wir entschuldigen uns für die Unannehmlichkeiten und schätzen Ihre Geduld.

BESTELLDATEN:
- Bestellnummer: {{ order_number }}
- Ursprünglicher Liefertermin: {{ original_delivery_date }}
- Neuer Liefertermin: {{ new_delivery_date }}
- Tracking-Nummer: {{ tracking_number }}

GRUND FÜR DIE VERZÖGERUNG:
{{ delay_reason }}

Bestellung verfolgen: {{ tracking_url }}

Wir arbeiten daran, Ihre Bestellung so schnell wie möglich zu Ihnen zu schicken. Sie erhalten eine weitere Aktualisierung, sobald Ihr Paket unterwegs ist.

Fragen? Kontaktieren Sie unser Kundenservice-Team: {{ support_url }}

---
Diese Aktualisierung betrifft die Bestellung #{{ order_number }} bei {{ shop_name }}.