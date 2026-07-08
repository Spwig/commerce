---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Update on your order #{{ order_number }} - Delivery Delay

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Update on Your Order
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We wanted to let you know about a delay with your order. We apologize for the inconvenience and appreciate your patience.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Order Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order Number:</strong> {{ order_number }}<br/>
              <strong>Original ETA:</strong> {{ original_delivery_date }}<br/>
              <strong>New ETA:</strong> {{ new_delivery_date }}<br/>
              <strong>Tracking Number:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Reason for Delay:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Track Your Order
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          We're working hard to get your order to you as quickly as possible. You'll receive another update when your package is on its way.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questions? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contact our customer service team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Update on Your Order #{{ order_number }}

Hi {{ customer_name }},

We wanted to let you know about a delay with your order. We apologize for the inconvenience and appreciate your patience.

ORDER DETAILS:
- Order Number: {{ order_number }}
- Original ETA: {{ original_delivery_date }}
- New ETA: {{ new_delivery_date }}
- Tracking Number: {{ tracking_number }}

REASON FOR DELAY:
{{ delay_reason }}

Track your order: {{ tracking_url }}

We're working hard to get your order to you as quickly as possible. You'll receive another update when your package is on its way.

Questions? Contact our customer service team: {{ support_url }}

---
This update is for order #{{ order_number }} at {{ shop_name }}.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| order_number | Order number | ORD-2024-001234 |
| original_delivery_date | Initially promised delivery date | February 18, 2026 |
| new_delivery_date | Updated estimated delivery | February 22, 2026 |
| tracking_number | Carrier tracking number | 1Z999AA10123456784 |
| tracking_url | Link to tracking page | https://shop.com/en/track/1Z999AA10123456784 |
| delay_reason | Explanation for delay | Weather conditions have affected shipping in your area |
| support_url | Customer support URL | https://shop.com/en/contact |
| shop_name | Store name | Amazing Shop |
| theme.color.primary | Primary brand color | #2563eb |
| theme.color.text | Main text color | #1f2937 |
| theme.color.text_secondary | Secondary text color | #6b7280 |
| theme.color.surface | Surface background color | #f9fafb |

## Notes

- Transactional email - always sent regardless of preferences
- Triggered by shipping provider webhook or manual admin update
- Should be sent as soon as delay is detected
- Proactive communication improves customer satisfaction
- Include honest, specific delay reason when possible
- Tone should be apologetic but reassuring
- Follow up with shipping_confirmation when package ships
- Consider offering discount code for significant delays (optional)
- Common delay reasons: weather, customs, carrier issues, high volume
- Mobile-optimized layout for on-the-go customers
