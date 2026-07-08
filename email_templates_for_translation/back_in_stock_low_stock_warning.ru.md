---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} вернулся, но распродается быстро! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Ограниченный ассортимент - действуйте быстро!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} вернулся в наличии!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Отличные новости! Товар, который вы ждали, снова в наличии. Но торопитесь - у нас осталось только {{ stock_remaining }} единица{{ stock_remaining|pluralize }}!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Вариант: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Только {{ stock_remaining }} осталось в наличии!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Купите сейчас, пока не закончилось
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>Этот товар распродавался {{ times_sold_out }} раз{{ times_sold_out|pluralize }} в течение последнего месяца!</strong><br/>
              Не упустите снова - заказывайте сейчас, пока есть запасы.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Больше не хотите получать уведомления? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Отписаться от этого уведомления</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ОГРАНИЧЕННЫЙ АССОРТИМЕНТ - ДЕЙСТВУЙТЕ БЫСТРО!

{{ product_name }} вернулся в наличии!

Здравствуйте, {{ customer_name }},

Отличные новости! Товар, который вы ждали, снова в наличии. Но торопитесь - у нас осталось только {{ stock_remaining }} единица{{ stock_remaining|pluralize }}!

ПРОДУКТ:
{{ product_name }}
{{ product_description }}
Цена: {{ product_price }}
{% if variant_name %}Вариант: {{ variant_name }}{% endif %}

⚠️ ТОЛЬКО {{ stock_remaining }} ОСТАЛОСЬ В НАЛИЧИИ!

Купите сейчас, пока не закончилось: {{ product_url }}

🔥 Этот товар распродавался {{ times_sold_out }} раз{{ times_sold_out|pluralize }} в течение последнего месяца!
Не упустите снова - заказывайте сейчас, пока есть запасы.

Больше не хотите получать уведомления? Отписаться: {{ unsubscribe_url }}