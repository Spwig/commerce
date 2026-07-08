---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Shipping Exception - Order #{{ order_number }} Requires Attention

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Shipping Exception
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We're writing to inform you of an exception with your shipment. We're working to resolve this issue as quickly as possible.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Exception Details:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Exception Type:</strong> {{ exception_type }}<br/>
              <strong>Description:</strong> {{ exception_description }}<br/>
              <strong>Occurred:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Order Information:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order Number:</strong> {{ order_number }}<br/>
              <strong>Tracking Number:</strong> {{ tracking_number }}<br/>
              <strong>Carrier:</strong> {{ carrier_name }}<br/>
              <strong>Current Location:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What Happens Next?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Action Required:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Track Your Order
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contact Support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SHIPPING EXCEPTION

Hi {{ customer_name }},

We're writing to inform you of an exception with your shipment. We're working to resolve this issue as quickly as possible.

EXCEPTION DETAILS:
- Exception Type: {{ exception_type }}
- Description: {{ exception_description }}
- Occurred: {{ exception_date }}

ORDER INFORMATION:
- Order Number: {{ order_number }}
- Tracking Number: {{ tracking_number }}
- Carrier: {{ carrier_name }}
- Current Location: {{ current_location }}

WHAT HAPPENS NEXT?
{{ resolution_steps }}

{% if action_required %}
⚠️ ACTION REQUIRED:
{{ action_required_description }}
{% endif %}

Track your order: {{ tracking_url }}
Contact support: {{ support_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | John |
| order_number | Order number | ORD-2024-001234 |
| exception_type | Exception category | Delivery Attempted - No Access |
| exception_description | Detailed description | Recipient not available, delivery will be reattempted |
| exception_date | When it occurred | February 15, 2026 at 3:45 PM |
| tracking_number | Carrier tracking | 1Z999AA10123456784 |
| carrier_name | Shipping carrier | UPS |
| current_location | Package location | Local Post Office, Brooklyn, NY |
| resolution_steps | Next steps | The carrier will attempt delivery again tomorrow between 9 AM - 5 PM |
| action_required | Boolean flag | true |
| action_required_description | Customer action needed | Please ensure someone is available to receive the package, or contact the carrier to arrange alternate delivery |
| tracking_url | Tracking page | https://shop.com/en/track/1Z999AA10123456784 |
| support_url | Support contact | https://shop.com/en/contact |

## Notes

- Transactional email for shipping problems
- Common exceptions: Delivery Failed, Package Damaged, Address Issue, Customs Hold, Return to Sender
- Triggered by carrier webhooks
- May require customer action (update address, schedule redelivery)
- Provide clear resolution steps
- Offer support contact for assistance
