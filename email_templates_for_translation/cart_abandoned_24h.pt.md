---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Ainda interessado(a)? Seu carrinho vai expirar em breve - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Seu {{ cart_item_count }} item{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} ainda aguardando
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Estamos mantendo seu carrinho para você, mas esses itens não vão durar para sempre. Conclua seu pedido antes que eles sejam removidos!
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
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ Apenas {{ item.stock_remaining }} restantes em estoque!
            </mj-text>
            {% endif %}
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
          Conclua seu pedido agora
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Frete grátis para pedidos acima de {{ free_shipping_threshold }}<br/>
              ✓ Garantia de devolução em 30 dias<br/>
              ✓ Checkout seguro
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Seu {{ cart_item_count }} item{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} ainda aguardando

Olá {{ customer_name }},

Estamos mantendo seu carrinho para você, mas esses itens não vão durar para sempre. Conclua seu pedido antes que eles sejam removidos!

SEU CARRINHO:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Apenas {{ item.stock_remaining }} restantes!{% endif %}
{% endfor %}

Total: {{ cart_total }}

Conclua seu pedido agora: {{ cart_url }}

POR QUE COMPRAR CONOSCO:
✓ Frete grátis para pedidos acima de {{ free_shipping_threshold }}
✓ Garantia de devolução em 30 dias
✓ Checkout seguro

---
Para parar de receber lembretes de carrinho, visite: {{ preferences_url }}