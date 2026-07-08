---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
ยังสนใจอยู่ไหม? ตะกร้าของคุณจะหมดอายุเร็ว ๆ นี้ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your {{ cart_item_count }} item{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} still waiting
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We're holding your cart for you, but these items won't last forever. Complete your purchase before they're gone!
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
              ⚠️ Only {{ item.stock_remaining }} left in stock!
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
          Complete Your Order Now
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Free shipping on orders over {{ free_shipping_threshold }}<br/>
              ✓ 30-day money-back guarantee<br/>
              ✓ Secure checkout
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Your {{ cart_item_count }} item{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} still waiting

Hi {{ customer_name }},

We're holding your cart for you, but these items won't last forever. Complete your purchase before they're gone!

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Only {{ item.stock_remaining }} left!{% endif %}
{% endfor %}

Total: {{ cart_total }}

Complete your order now: {{ cart_url }}

WHY SHOP WITH US:
✓ Free shipping on orders over {{ free_shipping_threshold }}
✓ 30-day money-back guarantee
✓ Secure checkout

---
To stop receiving cart reminders, visit: {{ preferences_url }}