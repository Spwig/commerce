---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Eccezione di Spedizione - L'ordine #{{ order_number }} richiede attenzione

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Eccezione di Spedizione
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We're writing to inform you of an exception with your shipment. We're working to resolve this issue as quickly as possible.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Dettagli dell'Eccezione:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Tipo di Eccezione:</strong> {{ exception_type }}<br/>
              <strong>Descrizione:</strong> {{ exception_description }}<br/>
              <strong>Occorso:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informazioni sull'Ordine:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numero dell'Ordine:</strong> {{ order_number }}<br/>
              <strong>Numero di Tracciamento:</strong> {{ tracking_number }}<br/>
              <strong>Corriere:</strong> {{ carrier_name }}<br/>
              <strong>Posizione Corrente:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa accadrà successivamente?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Azione Richiesta:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tracciare il tuo ordine
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contattare il supporto
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ECCEZIONE DI SPEDIZIONE

Hi {{ customer_name }},

We're writing to inform you of an exception with your shipment. We're working to resolve this issue as quickly as possible.

DETTAGLI DELL'ECCEZIONE:
- Tipo di Eccezione: {{ exception_type }}
- Descrizione: {{ exception_description }}
- Occorso: {{ exception_date }}

INFORMAZIONI SULL'ORDINE:
- Numero dell'Ordine: {{ order_number }}
- Numero di Tracciamento: {{ tracking_number }}
- Corriere: {{ carrier_name }}
- Posizione Corrente: {{ current_location }}

COSA ACCADRÀ SUCCESSIVAMENTE?
{{ resolution_steps }}

{% if action_required %}
⚠️ AZIONE RICHIESTA:
{{ action_required_description }}
{% endif %}

Tracciare il tuo ordine: {{ tracking_url }}
Contattare il supporto: {{ support_url }}

Remember: Preserve ALL Django template syntax ({{ }}, {% %}), all MJML tags (<mj-*>), all HTML attributes, and all emojis.