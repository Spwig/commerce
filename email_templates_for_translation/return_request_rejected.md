---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Return Request Update - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Return Request Update
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          We have reviewed your return request for order <strong>#{{ order_number }}</strong> and are unable to approve it at this time.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Reason:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          If you have questions about this decision or believe there has been an error, please contact our support team.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Return Request Update - Order #{{ order_number }}

Hi {{ customer_name }},

We have reviewed your return request for order #{{ order_number }} and are unable to approve it at this time.

{% if rejection_reason %}Reason: {{ rejection_reason }}{% endif %}

If you have questions about this decision or believe there has been an error, please contact our support team.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Sarah |
| order_number | Order identifier | ORD-12345 |
| rejection_reason | Explanation for rejection (optional) | Item was used and shows signs of wear |

## Notes

- Transactional email - sent when staff rejects a return request
- Uses neutral "update" language in subject rather than negative "rejected"
- Rejection reason is conditionally displayed
- Encourages customer to contact support if they disagree
