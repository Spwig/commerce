---
template_type: back_in_stock_waitlist_confirmation
category: Stock Notifications
---

# Email Template: back_in_stock_waitlist_confirmation

## Subject
✓ Вы находитесь в списке ожидания для {{ product_name }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Вы находитесь в списке ожидания!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо за регистрацию! Мы уведомим вас, как только этот продукт снова появится в наличии.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Вариант: {{ variant_name }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Что ожидать:</strong><br/>
              Мы сообщим вам по электронной почте, как только этот товар снова поступит в продажу. Товар ограничен, поэтому действуйте быстро, когда получите уведомление!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Пока ждете...
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Посмотрите эти похожие продукты, которые сейчас в наличии:
        </mj-text>

        {% for product in similar_products %}
        <mj-spacer height="10px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column width="25%">
            <mj-image src="{{ product.image }}" alt="{{ product.name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product.price }}
            </mj-text>
            <mj-text font-size="13px">
              <a href="{{ product.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Просмотреть продукт →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Изменили мнение? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Отписаться от этого списка ожидания</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ВЫ НАХОДИТЕСЬ В СПИСКЕ ОЖИДАНИЯ!

Здравствуйте, {{ customer_name }},

Спасибо за регистрацию! Мы уведомим вас, как только этот продукт снова появится в наличии.

ПРОДУКТ:
{{ product_name }}
{{ product_description }}
Цена: {{ product_price }}
{% if variant_name %}Вариант: {{ variant_name }}{% endif %}

💡 ЧТО ОЖИДАТЬ:
Мы сообщим вам по электронной почте, как только этот товар снова поступит в продажу. Товар ограничен, поэтому действуйте быстро, когда получите уведомление!

ПОКА ВЫ ЖДЁТЕ...
Посмотрите эти похожие продукты, которые сейчас в наличии:
{% for product in similar_products %}
- {{ product.name }} - {{ product.price }}
  {{ product.url }}
{% endfor %}

Изменили мнение? Отписаться от этого списка ожидания: {{ unsubscribe_url }}