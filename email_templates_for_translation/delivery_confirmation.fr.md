---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Commande livrée - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Commande livrée
        </mj-text>
        <mj-text>
          Votre commande n°{{ order_number }} a été livrée !
        </mj-text>
        <mj-text>
          Nous espérons que vous apprécierez votre achat. Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Voir la commande
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Commande livrée

Votre commande n°{{ order_number }} a été livrée !

Nous espérons que vous apprécierez votre achat. Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter.

Voir la commande : {{ order_url }}

