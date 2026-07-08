---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Refund Processed - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Refund Processed
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          Your return for order <strong>#{{ order_number }}</strong> has been inspected and your refund has been processed.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Refund Details
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Refund Amount:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Restocking Fee:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Note:</strong> It may take 5-10 business days for the refund to appear in your account, depending on your payment provider.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          If you have any questions about your refund, please contact our support team.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Refund Processed - Order #{{ order_number }}

Hi {{ customer_name }},

Your return for order #{{ order_number }} has been inspected and your refund has been processed.

Refund Details:
- Refund Amount: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Restocking Fee: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Note: It may take 5-10 business days for the refund to appear in your account, depending on your payment provider.

If you have any questions about your refund, please contact our support team.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Sarah |
| order_number | Order identifier | ORD-12345 |
| refund_amount | Numeric refund amount | 49.99 |
| refund_currency | Currency code | USD |
| restocking_fee | Restocking fee deducted (optional, may be 0) | 5.00 |
| restocking_fee_currency | Currency code for restocking fee | USD |

## Notes

- Transactional email - sent after refund is created from a return inspection
- Restocking fee is conditionally displayed only when applicable
- Separate from the generic `refund_notification` which is for order-level refunds
