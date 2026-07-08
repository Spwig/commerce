---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Return Request Received - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Return Request Received
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
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
          We have received your return request for order <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Return Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Reason:</strong> {{ return_reason }}<br/>
              <strong>Items:</strong> {{ items_count }} item(s)<br/>
              <strong>Status:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What happens next?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Our team will review your return request within 24-48 hours<br/>
          2. Once approved, we will send you a return shipping label via email<br/>
          3. Pack the items securely and attach the return label<br/>
          4. Drop off the package at your nearest shipping location<br/>
          5. Your refund will be processed once we receive and inspect the items
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          If you have any questions, please don't hesitate to contact us.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RETURN REQUEST RECEIVED
Order #{{ order_number }}

Hi {{ customer_name }},

We have received your return request for order #{{ order_number }}.

RETURN DETAILS:
- Reason: {{ return_reason }}
- Items: {{ items_count }} item(s)
- Status: {{ return_status }}

WHAT HAPPENS NEXT?
1. Our team will review your return request within 24-48 hours
2. Once approved, we will send you a return shipping label via email
3. Pack the items securely and attach the return label
4. Drop off the package at your nearest shipping location
5. Your refund will be processed once we receive and inspect the items

If you have any questions, please don't hesitate to contact us.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Jane Smith |
| order_number | Order number | ORD-2026-001234 |
| return_reason | Return reason | Item damaged |
| items_count | Number of return items | 2 |
| return_status | Current status | Pending Review |

## Notes

- Sent when customer creates a return request
- Transactional email - always sent
- Sets expectations for the return process
