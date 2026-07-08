---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
Đơn hàng #{{ order_number }} - Cập nhật trạng thái: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cập nhật trạng thái đơn hàng
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
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
          Trạng thái đơn hàng <strong>#{{ order_number }}</strong> đã được cập nhật.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Status:</strong> {{ old_status_display }}<br/>
              <strong>New Status:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

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
Cập nhật trạng thái đơn hàng - Order #{{ order_number }}

Hi {{ customer_name }},

Trạng thái đơn hàng #{{ order_number }} đã được cập nhật.

Previous Status: {{ old_status_display }}
New Status: {{ new_status_display }}

{% if order_url %}View order details: {{ order_url }}{% endif %}