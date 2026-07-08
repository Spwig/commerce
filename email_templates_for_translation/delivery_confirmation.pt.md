---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Encomenda Entregue - Encomenda #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Encomenda Entregue
        </mj-text>
        <mj-text>
          Sua encomenda #{{ order_number }} foi entregue!
        </mj-text>
        <mj-text>
          Esperamos que você aproveite sua compra. Se tiver quaisquer perguntas ou preocupações, não hesite em nos contatar.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ver Encomenda
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Encomenda Entregue

Sua encomenda #{{ order_number }} foi entregue!

Esperamos que você aproveite sua compra. Se tiver quaisquer perguntas ou preocupações, não hesite em nos contatar.

Ver encomenda: {{ order_url }}