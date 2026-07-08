---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
Il tuo ordine #{{ order_number }} è stato annullato

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ordine Annullato
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Il tuo ordine <strong>#{{ order_number }}</strong> è stato annullato.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Ragione:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se è stata effettuata un pagamento, un rimborso verrà processato in base al metodo di pagamento originale.
        </mj-text>

        <mj-spacer height="30px" />

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
Ordine Annullato

Ciao {{ customer_name }},

Il tuo ordine #{{ order_number }} è stato annullato.

{% if cancellation_reason %}Ragione: {{ cancellation_reason }}{% endif %}

Se è stata effettuata un pagamento, un rimborso verrà processato in base al metodo di pagamento originale.

{% if order_url %}Visualizza i dettagli dell'ordine: {{ order_url }}{% endif %}

Domande su questo annullamento?
Email: {{ support_email }}
Telefono: {{ support_phone }}