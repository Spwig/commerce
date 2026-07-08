---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Đơn hàng #{{ order_number }} của bạn đã được gửi!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Đơn hàng đã được gửi!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Trên đường vận chuyển!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tin vui! Đơn hàng của bạn đã được gửi và đang trên đường đến bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết vận chuyển:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Mã đơn hàng:</strong> {{ order_number }}<br/>
              <strong>Mã theo dõi:</strong> {{ tracking_number }}<br/>
              <strong>Đơn vị vận chuyển:</strong> {{ carrier_name }}<br/>
              <strong>Thời gian giao hàng dự kiến:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Theo dõi gói hàng của bạn
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ĐƠN HÀNG ĐÃ ĐƯỢC GỬI!

TRÊN ĐƯỜNG VẬN CHUYỂN!

Chào {{ customer_name }},

Tin vui! Đơn hàng của bạn đã được gửi và đang trên đường đến bạn.

CHI TIẾT VẬN CHUYỂN:
- Mã đơn hàng: {{ order_number }}
- Mã theo dõi: {{ tracking_number }}
- Đơn vị vận chuyển: {{ carrier_name }}
- Thời gian giao hàng dự kiến: {{ estimated_delivery }}

Theo dõi gói hàng của bạn: {{ tracking_url }}