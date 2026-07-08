---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Votre commande n°{{ order_number }} a été expédiée !

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Commande expédiée !
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En route !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande nouvelle ! Votre commande a été expédiée et est en route vers vous.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails d'expédition : 
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numéro de commande : </strong>{{ order_number }}<br/>
              <strong>Numéro de suivi : </strong>{{ tracking_number }}<br/>
              <strong>Transporteur : </strong>{{ carrier_name }}<br/>
              <strong>Est. livraison : </strong>{{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Suivre votre colis
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 COMMANDE EXPÉDIÉE !

En route !

Hi {{ customer_name }},

Grande nouvelle ! Votre commande a été expédiée et est en route vers vous.

DÉTAILS D'EXPÉDITION:
- Numéro de commande : {{ order_number }}
- Numéro de suivi : {{ tracking_number }}
- Transporteur : {{ carrier_name }}
- Est. livraison : {{ estimated_delivery }}

Suivre votre colis : {{ tracking_url }}