---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Снижение цены: {{ product_name }} теперь на {{ discount_percentage }}% скидки!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 Price Drop Alert!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Save {{ discount_percentage }}% on Your Wishlist Item
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Great News, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          A product on your wishlist just dropped in price! Don't miss this opportunity to save.
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Was: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Now: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              Save {{ savings_amount }} ({{ discount_percentage }}% OFF)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Buy Now & Save {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Limited Time:</strong> This sale won't last forever. Prices may go back up at any time!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Remove from wishlist: <a href="{{ remove_wishlist_url }}">Click here</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 СНИЖЕНИЕ ЦЕНЫ!
Сэкономьте {{ discount_percentage }}% на товаре из вашего списка желаний

Великолепные новости, {{ customer_name }}!

Товар из вашего списка желаний снизил цену! Не упустите возможность сэкономить.

{{ product_name }}
Было: {{ original_price }}
Теперь: {{ new_price }}
Экономия {{ savings_amount }} ({{ discount_percentage }}% СКИДКА)

Купите сейчас и сэкономьте {{ discount_percentage }}%: {{ product_url }}

⏰ ОГРАНИЧЕННОЕ ВРЕМЯ: Эта распродажа не продлится вечно. Цены могут снова вырасти в любое время!

Удалить из списка желаний: {{ remove_wishlist_url }}