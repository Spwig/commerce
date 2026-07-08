---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
Your cart is waiting! Complete your order - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          You left {{ cart_item_count }} item{{ cart_item_count|pluralize }} in your cart
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We noticed you didn't complete your purchase. Your items are still waiting in your cart!
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
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Complete Your Order
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Need help? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contact our support team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
You left {{ cart_item_count }} item{{ cart_item_count|pluralize }} in your cart

Hi {{ customer_name }},

We noticed you didn't complete your purchase. Your items are still waiting in your cart!

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Complete your order: {{ cart_url }}

Need help? Contact our support team: {{ support_url }}

---
You're receiving this email because you added items to your cart at {{ shop_name }}.
To stop receiving cart reminders, visit: {{ preferences_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | John |
| shop_name | Store name | Amazing Shop |
| cart_item_count | Number of items in cart | 3 |
| cart_items | List of cart items | [{product_name, product_image, quantity, price}] |
| cart_total | Total cart value formatted | $89.99 |
| cart_url | Direct link to cart checkout | https://shop.com/en/cart |
| support_url | Customer support URL | https://shop.com/en/contact |
| preferences_url | Communication preferences URL | https://shop.com/en/account/preferences |
| theme.color.primary | Primary brand color | #2563eb |
| theme.color.text | Main text color | #1f2937 |
| theme.color.text_secondary | Secondary text color | #6b7280 |
| theme.color.surface | Surface background color | #f9fafb |

## Notes

- Sent 1 hour after cart abandonment
- Part of 3-email abandoned cart sequence (1h, 24h, 48h)
- Respects user communication preferences (cart_reminders category)
- Industry data: Averages 15-20% conversion rate
- Should include unsubscribe option as per best practices
- First reminder focuses on simple reminder without discounts
- Mobile-optimized MJML layout
