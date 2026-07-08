---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
Seu carrinho está esperando! Complete seu pedido - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Você deixou {{ cart_item_count }} item{{ cart_item_count|pluralize }} no seu carrinho
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nós notamos que você não completou sua compra. Seus itens ainda estão esperando no seu carrinho!
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Complete Your Order
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Need help? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contact our support team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Você deixou {{ cart_item_count }} item{{ cart_item_count|pluralize }} no seu carrinho

Olá {{ customer_name }},

Nós notamos que você não completou sua compra. Seus itens ainda estão esperando no seu carrinho!

SEU CARRINHO:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Complete seu pedido: {{ cart_url }}

Precisa de ajuda? Entre em contato com nossa equipe de suporte: {{ support_url }}

---
Você está recebendo este e-mail porque adicionou itens ao seu carrinho em {{ shop_name }}.
Para parar de receber lembretes de carrinho, visite: {{ preferences_url }}