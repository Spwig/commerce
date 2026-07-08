---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
Ваша корзина ждет! Завершите заказ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Вы оставили {{ cart_item_count }} товар{{ cart_item_count|pluralize }} в своей корзине
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы заметили, что вы не завершили покупку. Ваши товары все еще ждут вас в корзине!
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
          Итого: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Завершите свой заказ
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Нужна помощь? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Свяжитесь с нашей службой поддержки</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Вы оставили {{ cart_item_count }} товар{{ cart_item_count|pluralize }} в своей корзине

Здравствуйте {{ customer_name }},

Мы заметили, что вы не завершили покупку. Ваши товары все еще ждут вас в корзине!

ВАША КОРЗИНА:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Итого: {{ cart_total }}

Завершите свой заказ: {{ cart_url }}

Нужна помощь? Свяжитесь с нашей службой поддержки: {{ support_url }}

---
Вы получаете это письмо, потому что добавили товары в свою корзину на {{ shop_name }}.
Чтобы прекратить получать напоминания о корзине, перейдите по ссылке: {{ preferences_url }}