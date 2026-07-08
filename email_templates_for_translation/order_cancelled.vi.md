---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
Đơn hàng #{{ order_number }} Của Bạn Đã Bị Hủy

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Order Cancelled
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Your order <strong>#{{ order_number }}</strong> has been cancelled.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Reason:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          If a payment was made, a refund will be processed according to the original payment method.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Order Details
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Order Cancelled

Hi {{ customer_name }},

Your order #{{ order_number }} has been cancelled.

{% if cancellation_reason %}Reason: {{ cancellation_reason }}{% endif %}

If a payment was made, a refund will be processed according to the original payment method.

{% if order_url %}View order details: {{ order_url }}{% endif %}

Questions about this cancellation?
Email: {{ support_email }}
Phone: {{ support_phone }}