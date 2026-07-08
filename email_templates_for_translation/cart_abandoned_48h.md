---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
Last chance! Your cart expires in 24 hours - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ Last Chance - Cart Expires in 24 Hours
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Don't miss out, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          This is your final reminder. Your cart will expire in 24 hours and we can't hold these items any longer.
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
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Complete Order Before It's Too Late
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questions? Our team is here to help: <a href="{{ support_url }}">Contact Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ LAST CHANCE - CART EXPIRES IN 24 HOURS

Don't miss out, {{ customer_name }}!

This is your final reminder. Your cart will expire in 24 hours and we can't hold these items any longer.

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Complete your order before it's too late: {{ cart_url }}

Questions? Our team is here to help: {{ support_url }}

---
This is the final reminder for cart #{{ cart_id }}.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | John |
| cart_id | Cart identifier | CART-ABC123 |
| cart_items | Product list | [{name, image, qty, price}] |
| cart_total | Total value | $89.99 |
| cart_url | Checkout URL | https://shop.com/en/cart |
| support_url | Support contact | https://shop.com/en/contact |

## Notes

- Sent 48 hours after abandonment
- Final email in sequence - highest urgency
- Red CTA button for urgency
- Conversion rate: 5-8% typically
- No more reminders sent after this
