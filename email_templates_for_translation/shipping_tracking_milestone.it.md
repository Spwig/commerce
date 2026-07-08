---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Il tuo ordine #{{ order_number }} è {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aggiornamento sulla consegna: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Buone notizie! Il tuo ordine ha raggiunto un importante traguardo nel suo percorso verso di te.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'ordine:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numero dell'ordine:</strong> {{ order_number }}<br/>
              <strong>Numero di tracciamento:</strong> {{ tracking_number }}<br/>
              <strong>Corriere:</strong> {{ carrier_name }}<br/>
              <strong>Posizione corrente:</strong> {{ current_location }}<br/>
              <strong>Data stimata di consegna:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tracciare il tuo pacchetto
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Hai domande sulla tua consegna? <a href="{{ support_url }.pdf">Contatta il supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aggiornamento sulla consegna: {{ milestone_status }}

Ciao {{ customer_name }},

Buone notizie! Il tuo ordine ha raggiunto un importante traguardo nel suo percorso verso di te.

📦 {{ milestone_status }}
{{ milestone_description }}

DETTAGLI DELL'ORDINE:
- Numero dell'ordine: {{ order_number }}
- Numero di tracciamento: {{ tracking_number }}
- Corriere: {{ carrier_name }}
- Posizione corrente: {{ current_location }}
- Data stimata di consegna: {{ estimated_delivery }}

Tracciare il tuo pacchetto: {{ tracking_url }}

Hai domande sulla tua consegna? Contatta il supporto: {{ support_url }}