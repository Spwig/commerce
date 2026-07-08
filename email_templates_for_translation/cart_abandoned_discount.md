---
template_type: cart_abandoned_discount
category: Cart Recovery
---

# Email Template: cart_abandoned_discount

## Subject
Exclusive {{ discount_percentage }}% off your cart! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎉 Special Offer Just For You!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          {{ discount_percentage }}% OFF Your Cart
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          We want to make this easy, {{ customer_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Complete your purchase now and save {{ discount_percentage }}% with code <strong>{{ discount_code }}</strong>
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px" border="2px dashed #059669">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              YOUR EXCLUSIVE CODE
            </mj-text>
            <mj-text font-size="28px" font-weight="bold" color="#047857" align="center" font-family="'Courier New', monospace">
              {{ discount_code }}
            </mj-text>
            <mj-text font-size="13px" color="#065f46" align="center">
              Expires: {{ discount_expiry }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

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
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text align="right">
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">Subtotal:</span> <span style="text-decoration: line-through; color: #9ca3af;">{{ cart_total }}</span>
            </mj-text>
            <mj-text align="right">
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">Discount ({{ discount_percentage }}%):</span> <span style="color: #059669; font-weight: bold;">-{{ discount_amount }}</span>
            </mj-text>
            <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
              New Total: {{ discounted_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Claim Your {{ discount_percentage }}% Discount
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-style="italic">
          Offer expires {{ discount_expiry }} - Don't miss out!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 SPECIAL OFFER JUST FOR YOU!
{{ discount_percentage }}% OFF YOUR CART

We want to make this easy, {{ customer_name }}

Complete your purchase now and save {{ discount_percentage }}% with code {{ discount_code }}

═══════════════════════════
YOUR EXCLUSIVE CODE
{{ discount_code }}
Expires: {{ discount_expiry }}
═══════════════════════════

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Subtotal: {{ cart_total }}
Discount ({{ discount_percentage }}%): -{{ discount_amount }}
NEW TOTAL: {{ discounted_total }}

Claim your {{ discount_percentage }}% discount: {{ cart_url }}

Offer expires {{ discount_expiry }} - Don't miss out!

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| discount_code | Unique discount code | CART10-ABC123 |
| discount_percentage | Percentage off | 10 |
| discount_amount | Dollar amount saved | $8.99 |
| discount_expiry | Expiration date/time | February 20, 2026 at 11:59 PM |
| cart_items | Product list | [{name, image, qty, price}] |
| cart_total | Original total | $89.99 |
| discounted_total | New total after discount | $81.00 |
| cart_url | Auto-applied discount URL | https://shop.com/en/cart?code=CART10-ABC123 |

## Notes

- Optional incentive template (use strategically)
- Typically 5-15% discount
- Time-limited offer (24-48 hours)
- Code auto-applied via URL parameter
- Use sparingly to avoid training customers to wait for discounts
- Best for high-value carts or first-time customers
- Conversion rate: 20-30% (higher than non-discount)
