---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Все ещё интересуетесь? Ваша корзина скоро истечёт - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваше {{ cart_item_count }} товар{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} всё ещё ждут
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы держим вашу корзину для вас, но эти товары не продержатся вечно. Завершите покупку до того, как они исчезнут!
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
              ⚠️ Только {{ item.stock_remaining }} осталось на складе!
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
          Завершите свой заказ сейчас
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Бесплатная доставка при заказах свыше {{ free_shipping_threshold }}<br/>
              ✓ Гарантия возврата денег в течение 30 дней<br/>
              ✓ Безопасная оплата
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ваше {{ cart_item_count }} товар{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} всё ещё ждут

Здравствуйте, {{ customer_name }},

Мы держим вашу корзину для вас, но эти товары не продержатся вечно. Завершите покупку до того, как они исчезнут!

ВАША КОРЗИНА:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Только {{ item.stock_remaining }} осталось!{% endif %}
{% endfor %}

Total: {{ cart_total }}

Завершите свой заказ сейчас: {{ cart_url }}

ПОЧЕМУ СТОИТ ПОКУПАТЬ У НАС:
✓ Бесплатная доставка при заказах свыше {{ free_shipping_threshold }}
✓ Гарантия возврата денег в течение 30 дней
✓ Безопасная оплата

---
Чтобы прекратить получать напоминания о корзине, перейдите по ссылке: {{ preferences_url }}