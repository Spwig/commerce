---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
Ordine #{{ order_number }} - Aggiornamento dello stato: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aggiornamento dello stato dell'ordine
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          Ordine #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Lo stato del tuo ordine <strong>#{{ order_number }}</strong> è stato aggiornato.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Stato precedente:</strong> {{ old_status_display }}<br/>
              <strong>Stato nuovo:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza i dettagli dell'ordine
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aggiornamento dello stato dell'ordine - Ordine #{{ order_number }}

Ciao {{ customer_name }},

Lo stato del tuo ordine #{{ order_number }} è stato aggiornato.

Stato precedente: {{ old_status_display }}
Stato nuovo: {{ new_status_display }}

{% if order_url %}Visualizza i dettagli dell'ordine: {{ order_url }}{% endif %}