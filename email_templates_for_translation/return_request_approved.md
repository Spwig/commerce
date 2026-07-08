---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Your Return Has Been Approved - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Return Approved
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
          Your return request for order <strong>#{{ order_number }}</strong> has been approved.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Next steps:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Download and print the return label below<br/>
          2. Pack the items securely in their original packaging if possible<br/>
          3. Attach the return label to the outside of the package<br/>
          4. Drop off at your nearest shipping location
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Download Return Label
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Return Tracking Number:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Important:</strong> Please ship the return within 7 days to ensure prompt processing of your refund.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Once we receive and inspect your return, we will process your refund to the original payment method.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Return Approved - Order #{{ order_number }}

Hi {{ customer_name }},

Your return request for order #{{ order_number }} has been approved.

Next steps:
1. Download and print the return label
2. Pack the items securely in their original packaging if possible
3. Attach the return label to the outside of the package
4. Drop off at your nearest shipping location

{% if return_label_url %}Download your return label: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Return Tracking Number: {{ return_tracking_number }}{% endif %}

Important: Please ship the return within 7 days to ensure prompt processing of your refund.

Once we receive and inspect your return, we will process your refund to the original payment method.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Sarah |
| order_number | Order identifier | ORD-12345 |
| return_label_url | URL to download return label PDF (optional) | https://shop.com/returns/label/abc123/ |
| return_tracking_number | Return shipment tracking number (optional) | 1Z999AA10123456784 |

## Notes

- Transactional email - sent when staff approves a return request
- Return label URL and tracking number are conditionally displayed
- Includes 7-day shipping deadline reminder
