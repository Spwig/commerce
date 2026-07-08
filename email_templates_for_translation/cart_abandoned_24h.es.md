---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
¿Todavía estás interesado? Tu carrito se agota pronto - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tu {{ cart_item_count }} artículo{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} aún está esperando
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Estamos guardando tu carrito para ti, pero estos artículos no durarán para siempre. Completa tu compra antes de que se agoten!
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
              ⚠️ Solo quedan {{ item.stock_remaining }} en stock!
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
          Completa tu pedido ahora
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Envío gratis en pedidos superiores a {{ free_shipping_threshold }}<br/>
              ✓ Garantía de devolución de dinero de 30 días<br/>
              ✓ Pago seguro
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tu {{ cart_item_count }} artículo{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} aún está esperando

Hola {{ customer_name }},

Estamos guardando tu carrito para ti, pero estos artículos no durarán para siempre. Completa tu compra antes de que se agoten!

TU CARRO:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Solo quedan {{ item.stock_remaining }} en stock!{% endif %}
{% endfor %}

Total: {{ cart_total }}

Completa tu pedido ahora: {{ cart_url }}

¿POR QUÉ COMPRAR CON NOSOTROS?:
✓ Envío gratis en pedidos superiores a {{ free_shipping_threshold }}
✓ Garantía de devolución de dinero de 30 días
✓ Pago seguro

---
Para dejar de recibir recordatorios de carrito, visite: {{ preferences_url }}