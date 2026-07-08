---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Il tuo reso è stato approvato - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Reso Approvato
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
          La tua richiesta di reso per l'ordine <strong>#{{ order_number }}</strong> è stata approvata.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Passaggi successivi:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Scarica e stampa l'etichetta di reso qui sotto<br/>
          2. Confeziona gli articoli in modo sicuro utilizzando l'imballaggio originale, se possibile<br/>
          3. Attacca l'etichetta di reso all'esterno del pacco<br/>
          4. Porta il pacco alla location di spedizione più vicina
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Scarica l'etichetta di reso
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Numero di tracciamento del reso:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Importante:</strong> Per favore spedisci il reso entro 7 giorni per garantire un rimborso rapido.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Una volta che riceveremo e controlleremo il tuo reso, procederemo al rimborso sul metodo di pagamento originale.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Reso Approvato - Ordine #{{ order_number }}

Ciao {{ customer_name }},

La tua richiesta di reso per l'ordine #{{ order_number }} è stata approvata.

Passaggi successivi:
1. Scarica e stampa l'etichetta di reso
2. Confeziona gli articoli in modo sicuro utilizzando l'imballaggio originale, se possibile
3. Attacca l'etichetta di reso all'esterno del pacco
4. Porta il pacco alla location di spedizione più vicina

{% if return_label_url %}Scarica l'etichetta di reso: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Numero di tracciamento del reso: {{ return_tracking_number }}{% endif %}

Importante: Per favore spedisci il reso entro 7 giorni per garantire un rimborso rapido.

Una volta che riceveremo e controlleremo il tuo reso, procederemo al rimborso sul metodo di pagamento originale.