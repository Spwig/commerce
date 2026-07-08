---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 High Value Transaction: {{ transaction_amount }} at {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 High Value Transaction
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Large Transaction Processed
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A transaction of {{ transaction_amount }} was processed at {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Transaction Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Amount:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cashier:</strong> {{ cashier_name }}<br/>
              <strong>Timestamp:</strong> {{ transaction_time }}<br/>
              <strong>Transaction ID:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Payment Information:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Items Summary:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Items:</strong> {{ item_count }}<br/>
              <strong>Subtotal:</strong> {{ subtotal }}<br/>
              <strong>Tax:</strong> {{ tax_amount }}<br/>
              <strong>Total:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Customer Information:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              This notification is sent for all transactions exceeding {{ threshold_amount }} for fraud prevention and monitoring purposes.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Transaction
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Receipt
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 HIGH VALUE TRANSACTION

Large Transaction Processed

A transaction of {{ transaction_amount }} was processed at {{ terminal_name }}.

TRANSACTION DETAILS:
- Amount: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Cashier: {{ cashier_name }}
- Timestamp: {{ transaction_time }}
- Transaction ID: {{ transaction_id }}

PAYMENT INFORMATION:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

ITEMS SUMMARY:
- Total Items: {{ item_count }}
- Subtotal: {{ subtotal }}
- Tax: {{ tax_amount }}
- Total: {{ transaction_amount }}

{% if customer_info %}
CUSTOMER INFORMATION:
{{ customer_info }}
{% endif %}

This notification is sent for all transactions exceeding {{ threshold_amount }} for fraud prevention and monitoring purposes.

View transaction: {{ transaction_url }}
View receipt: {{ receipt_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| transaction_amount | Total transaction amount | $5,247.50 |
| terminal_name | Terminal display name | Checkout 1 |
| cashier_name | Cashier's name | John Smith |
| transaction_time | Transaction timestamp | February 15, 2026 at 3:45 PM |
| transaction_id | Unique transaction ID | TXN-2026-001234 |
| payment_methods | Payment breakdown array | [{method: 'Credit Card', amount: '$5,247.50'}] |
| item_count | Number of items | 12 |
| subtotal | Subtotal before tax | $4,850.00 |
| tax_amount | Tax amount | $397.50 |
| customer_info | Optional customer details | John Doe - john@example.com |
| threshold_amount | Alert threshold | $1,000 |
| transaction_url | Transaction details page | https://shop.com/en/admin/pos/transactions/12345 |
| receipt_url | Receipt view | https://shop.com/en/admin/pos/receipts/12345 |

## Notes

- Manager/admin notification
- Sent when transaction exceeds configurable threshold (e.g., $1,000)
- Fraud prevention and monitoring purpose
- Includes payment and customer details
- Links to transaction details and receipt
- Transactional email
