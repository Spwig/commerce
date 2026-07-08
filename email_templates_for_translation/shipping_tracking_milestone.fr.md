---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Votre commande n°{{ order_number }} est {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mise à jour de livraison : {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonne nouvelle ! Votre commande a atteint un point important dans son parcours vers vous.
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
              Détails de la commande : 
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numéro de commande : </strong>{{ order_number }}<br/>
              <strong>Numéro de suivi : </strong>{{ tracking_number }}<br/>
              <strong>Transporteur : </strong>{{ carrier_name }}<br/>
              <strong>Emplacement actuel : </strong>{{ current_location }}<br/>
              <strong>Estimation de livraison : </strong>{{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Suivez votre colis
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questions sur votre livraison ? <a href="{{ support_url }.pdf">Contactez le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Mise à jour de livraison : {{ milestone_status }}

Bonjour {{ customer_name }},

Bonne nouvelle ! Votre commande a atteint un point important dans son parcours vers vous.

📦 {{ milestone_status }}
{{ milestone_description }}

DÉTAILS DE LA COMMANDE : 
- Numéro de commande : {{ order_number }}
- Numéro de suivi : {{ tracking_number }}
- Transporteur : {{ carrier_name }}
- Emplacement actuel : {{ current_location }}
- Estimation de livraison : {{ estimated_delivery }}

Suivez votre colis : {{ tracking_url }}

Questions sur votre livraison ? Contactez le support : {{ support_url }}
