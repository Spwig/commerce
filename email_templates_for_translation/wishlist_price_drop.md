---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Price Drop Alert: {{ product_name }} is now {{ discount_percentage }}% off!

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
🔥 PRICE DROP ALERT!
Save {{ discount_percentage }}% on Your Wishlist Item

Great News, {{ customer_name }}!

A product on your wishlist just dropped in price! Don't miss this opportunity to save.

{{ product_name }}
Was: {{ original_price }}
NOW: {{ new_price }}
SAVE {{ savings_amount }} ({{ discount_percentage }}% OFF)

Buy now & save {{ discount_percentage }}%: {{ product_url }}

⏰ LIMITED TIME: This sale won't last forever. Prices may go back up at any time!

Remove from wishlist: {{ remove_wishlist_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| product_name | Product name | Wireless Headphones |
| original_price | Previous price | $79.99 |
| new_price | Discounted price | $59.99 |
| savings_amount | Dollar savings | $20.00 |
| discount_percentage | Percentage off | 25 |
| product_image | Image URL | https://shop.com/media/headphones.jpg |
| product_url | Product page | https://shop.com/en/products/wireless-headphones |
| remove_wishlist_url | Remove from wishlist | https://shop.com/en/wishlist/remove/123 |

## Notes

- HIGH CONVERSION email (15-20% typical)
- Sent when price drops by configured threshold (e.g., >10%)
- Marketing email - respects preferences
- Creates urgency with limited-time messaging
- Green color scheme for positive savings
- Daily price monitoring recommended
