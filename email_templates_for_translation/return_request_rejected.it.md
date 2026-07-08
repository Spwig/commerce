---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Aggiornamento richiesta reso - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Aggiornamento richiesta reso
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          Abbiamo esaminato la tua richiesta di reso per l'ordine <strong>#{{ order_number }}</strong> e al momento non possiamo approvarla.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Ragione:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se hai domande su questa decisione o credi che possa esserci un errore, contatta il nostro team di supporto.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aggiornamento richiesta reso - Ordine #{{ order_number }}

Ciao {{ customer_name }},

Abbiamo esaminato la tua richiesta di reso per l'ordine #{{ order_number }} e al momento non possiamo approvarla.

{% if rejection_reason %}Ragione: {{ rejection_reason }}{% endif %}

Se hai domande su questa decisione o credi che possa esserci un errore, contatta il nostro team di supporto.