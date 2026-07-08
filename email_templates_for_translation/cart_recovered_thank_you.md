---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Thank you for your order #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Thank You for Your Order!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We're thrilled you completed your purchase! Your order has been confirmed and we're preparing it for shipment.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Order Summary
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order Number:</strong> {{ order_number }}<br/>
              <strong>Order Date:</strong> {{ order_date }}<br/>
              <strong>Total:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Track Your Order
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What Happens Next?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. We'll prepare your order (usually within 1-2 business days)<br/>
          2. You'll receive a shipping confirmation with tracking info<br/>
          3. Your order will be delivered to: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Did you know?</strong><br/>
              You can track your order anytime in your account dashboard.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questions? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contact our support team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 THANK YOU FOR YOUR ORDER!

Hi {{ customer_name }},

We're thrilled you completed your purchase! Your order has been confirmed and we're preparing it for shipment.

ORDER SUMMARY:
- Order Number: {{ order_number }}
- Order Date: {{ order_date }}
- Total: {{ order_total }}

Track your order: {{ order_tracking_url }}

WHAT HAPPENS NEXT?
1. We'll prepare your order (usually within 1-2 business days)
2. You'll receive a shipping confirmation with tracking info
3. Your order will be delivered to: {{ shipping_address }}

💡 DID YOU KNOW?
You can track your order anytime in your account dashboard.

Questions? Contact our support team: {{ support_url }}

---
Order #{{ order_number }} at {{ shop_name }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | John |
| order_number | Order number | ORD-2024-001234 |
| order_date | Order placement date | February 15, 2026 |
| order_total | Total amount | $89.99 |
| order_tracking_url | Order tracking page | https://shop.com/en/orders/ORD-2024-001234 |
| shipping_address | Delivery address (shortened) | 123 Main St, New York, NY 10001 |
| support_url | Support contact | https://shop.com/en/contact |
| shop_name | Store name | Amazing Shop |

## Notes

- Sent immediately after cart recovery order is placed
- Separate from standard order_confirmation (this celebrates the recovery)
- Positive, enthusiastic tone
- Reassures customer about next steps
- Opportunity to upsell/cross-sell in future iterations
- Tracks cart recovery success metric
