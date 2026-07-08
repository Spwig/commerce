---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
Bestellung #{{ order_number }} - Statusaktualisierung: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bestellstatusaktualisierung
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Der Status Ihrer Bestellung <strong>#{{ order_number }}</strong> wurde aktualisiert.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Vorheriger Status:</strong> {{ old_status_display }}<br/>
              <strong>Neuer Status:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

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
Bestellstatusaktualisierung - Bestellung #{{ order_number }}

Hi {{ customer_name }},

Der Status Ihrer Bestellung #{{ order_number }} wurde aktualisiert.

Vorheriger Status: {{ old_status_display }}
Neuer Status: {{ new_status_display }}

{% if order_url %}Bestelldetails ansehen: {{ order_url }}{% endif %}