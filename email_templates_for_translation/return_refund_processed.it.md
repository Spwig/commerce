---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Rimborso processato - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Rimborso processato
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          Il tuo reso per l'ordine <strong>#{{ order_number }}</strong> è stato ispezionato e il rimborso è stato processato.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Dettagli del rimborso
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Importo del rimborso:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tassa di rimborso:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Nota:</strong> Potrebbero essere necessari da 5 a 10 giorni lavorativi affinché il rimborso appaia nel tuo account, a seconda del tuo fornitore di pagamento.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se hai domande sul tuo rimborso, contatta il nostro team di supporto.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rimborso processato - Ordine #{{ order_number }}

Ciao {{ customer_name }},

Il tuo reso per l'ordine #{{ order_number }} è stato ispezionato e il rimborso è stato processato.

Dettagli del rimborso:
- Importo del rimborso: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Tassa di rimborso: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Nota: Potrebbero essere necessari da 5 a 10 giorni lavorativi affinché il rimborso appaia nel tuo account, a seconda del tuo fornitore di pagamento.

Se hai domande sul tuo rimborso, contatta il nostro team di supporto.