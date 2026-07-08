---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
Ihre Bestellung #{{ order_number }} wurde storniert

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bestellung storniert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre Bestellung <strong>#{{ order_number }}</strong> wurde storniert.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Reason:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wenn eine Zahlung getätigt wurde, wird ein Erstattungsbetrag gemäß dem ursprünglichen Zahlungsmittel verarbeitet.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bestelldetails ansehen
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bestellung storniert

Hi {{ customer_name }},

Ihre Bestellung #{{ order_number }} wurde storniert.

{% if cancellation_reason %}Reason: {{ cancellation_reason }}{% endif %}

Wenn eine Zahlung getätigt wurde, wird ein Erstattungsbetrag gemäß dem ursprünglichen Zahlungsmittel verarbeitet.

{% if order_url %}Bestelldetails ansehen: {{ order_url }}{% endif %}

Fragen zu dieser Stornierung?
E-Mail: {{ support_email }}
Telefon: {{ support_phone }}