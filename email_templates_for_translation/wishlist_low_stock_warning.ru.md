---
template_type: wishlist_low_stock_warning
category: Wishlist
---

# Email Template: wishlist_low_stock_warning

## Subject
⚠️ Спешите! {{ product_name }} быстро раскупают - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Предупреждение о низком запасе!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Действуйте быстро, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Товар на вашем списке желаний почти распродан. Осталось только {{ stock_remaining }} единица{{ stock_remaining|pluralize }} - оформьте заказ сейчас, пока не закончилось!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Осталось только {{ stock_remaining }} единиц на складе!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Купить до того, как закончилось
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ПРЕДУПРЕЖДЕНИЕ О НИЗКОМ ЗАПАСЕ!

Действуйте быстро, {{ customer_name }}!

Товар на вашем списке желаний почти распродан. Осталось только {{ stock_remaining }} единица{{ stock_remaining|pluralize }} - оформьте заказ сейчас, пока не закончилось!

{{ product_name }}
Цена: {{ product_price }}
⚠️ Осталось только {{ stock_remaining }} единиц на складе!

Купите до того, как закончилось: {{ product_url }}