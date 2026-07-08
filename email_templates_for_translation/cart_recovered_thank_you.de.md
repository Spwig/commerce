---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Vielen Dank für Ihre Bestellung #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Vielen Dank für Ihre Bestellung!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir freuen uns, dass Sie Ihre Bestellung abgeschlossen haben! Ihre Bestellung wurde bestätigt und wird für die Auslieferung vorbereitet.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Bestellübersicht
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bestellnummer:</strong> {{ order_number }}<br/>
              <strong>Bestelldatum:</strong> {{ order_date }}<br/>
              <strong>Gesamt:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bestellung verfolgen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was geschieht als Nächstes?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Wir werden Ihre Bestellung vorbereiten (meist innerhalb von 1-2 Werktagen)<br/>
          2. Sie erhalten eine Versandbestätigung mit Tracking-Informationen<br/>
          3. Ihre Bestellung wird an folgende Adresse geliefert: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Wussten Sie?</strong><br/>
              Sie können Ihre Bestellung jederzeit in Ihrem Konten-Dashboard verfolgen.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Fragen? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Kontaktieren Sie unser Support-Team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 VIEL DANK FÜR IHR BESTELLUNG!

Hi {{ customer_name }},

Wir freuen uns, dass Sie Ihre Bestellung abgeschlossen haben! Ihre Bestellung wurde bestätigt und wird für die Auslieferung vorbereitet.

BESTELLÜBERSICHT:
- Bestellnummer: {{ order_number }}
- Bestelldatum: {{ order_date }}
- Gesamt: {{ order_total }}

Track your order: {{ order_tracking_url }}

WAS GESCHIEHT ALS NÄCHSTES?
1. Wir werden Ihre Bestellung vorbereiten (meist innerhalb von 1-2 Werktagen)
2. Sie erhalten eine Versandbestätigung mit Tracking-Informationen
3. Ihre Bestellung wird an folgende Adresse geliefert: {{ shipping_address }}

💡 WUSSTEN SIE?
Sie können Ihre Bestellung jederzeit in Ihrem Konten-Dashboard verfolgen.

Fragen? Kontaktieren Sie unser Support-Team: {{ support_url }}

---
Bestellung #{{ order_number }} bei {{ shop_name }}