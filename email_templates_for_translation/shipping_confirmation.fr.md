---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Votre commande a été expédiée - Commande #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Votre commande a été expédiée !
        </mj-text>
        <mj-text>
          Grande nouvelle ! Votre commande #{{ order_number }} a été expédiée.
        </mj-text>
        <mj-text>
          <strong>Numéro de suivi:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Transporteur:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Suivre le colis
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Votre commande a été expédiée !

Grande nouvelle ! Votre commande #{{ order_number }} a été expédiée.

Numéro de suivi: {{ tracking_number }}
Transporteur: {{ carrier }}

Suivre votre colis: {{ tracking_url }}