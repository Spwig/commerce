---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
We've Received Your Return - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Return Received
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Order #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We have received your returned items for order <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>What happens next:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Our team will inspect the returned items within 2-3 business days<br/>
          2. We will verify the items are in their original condition<br/>
          3. Once inspection is complete, we will process your refund<br/>
          4. You will receive a confirmation email once the refund is processed
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          The refund will be credited to your original payment method and may take 5-10 business days to appear in your account.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thank you for your patience!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Return Received - Order #{{ order_number }}

Hi {{ customer_name }},

We have received your returned items for order #{{ order_number }}.

What happens next:
1. Our team will inspect the returned items within 2-3 business days
2. We will verify the items are in their original condition
3. Once inspection is complete, we will process your refund
4. You will receive a confirmation email once the refund is processed

The refund will be credited to your original payment method and may take 5-10 business days to appear in your account.

Thank you for your patience!

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Sarah |
| order_number | Order identifier | ORD-12345 |

## Notes

- Transactional email - sent when staff marks a return as received at warehouse
- Sets expectations for inspection timeline (2-3 business days)
- Informs about refund processing timeline (5-10 business days)
