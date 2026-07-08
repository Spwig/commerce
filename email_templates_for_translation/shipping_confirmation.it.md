---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
La Tua Ordine è Stato Spedito - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          La Tua Ordine è Stato Spedito!
        </mj-text>
        <mj-text>
          Grande notizia! La tua ordine #{{ order_number }} è stato spedito.
        </mj-text>
        <mj-text>
          <strong>Numero di Tracciamento:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Corriere:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Tracciare la spedizione
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
La Tua Ordine è Stato Spedito!

Grande notizia! La tua ordine #{{ order_number }} è stato spedito.

Numero di Tracciamento: {{ tracking_number }}
Corriere: {{ carrier }}

Tracciare la spedizione: {{ tracking_url }}

