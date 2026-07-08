---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Đơn hàng của bạn #{{ order_number }} đang ở trạng thái {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cập nhật giao hàng: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tin tốt! Đơn hàng của bạn đã đạt được một mốc quan trọng trong hành trình đến với bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết đơn hàng:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số đơn hàng:</strong> {{ order_number }}<br/>
              <strong>Số theo dõi:</strong> {{ tracking_number }}<br/>
              <strong>Đơn vị vận chuyển:</strong> {{ carrier_name }}<br/>
              <strong>Vị trí hiện tại:</strong> {{ current_location }}<br/>
              <strong>Thời gian giao hàng dự kiến:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Theo dõi gói hàng của bạn
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Có câu hỏi về đơn hàng của bạn? <a href="{{ support_url }.ogg">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Cập nhật giao hàng: {{ milestone_status }}

Chào {{ customer_name }},

Tin tốt! Đơn hàng của bạn đã đạt được một mốc quan trọng trong hành trình đến với bạn.

📦 {{ milestone_status }}
{{ milestone_description }}

CHI TIẾT ĐƠN HÀNG:
- Số đơn hàng: {{ order_number }}
- Số theo dõi: {{ tracking_number }}
- Đơn vị vận chuyển: {{ carrier_name }}
- Vị trí hiện tại: {{ current_location }}
- Thời gian giao hàng dự kiến: {{ estimated_delivery }}

Theo dõi gói hàng của bạn: {{ tracking_url }}

Có câu hỏi về đơn hàng của bạn? Liên hệ hỗ trợ: {{ support_url }}