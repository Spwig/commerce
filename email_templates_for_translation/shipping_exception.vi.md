---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Ngoại lệ vận chuyển - Đơn hàng #{{ order_number }} cần được xử lý

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Ngoại lệ vận chuyển
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúng tôi viết email này để thông báo về ngoại lệ trong đơn hàng của bạn. Chúng tôi đang cố gắng giải quyết vấn đề này càng sớm càng có thể.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Chi tiết ngoại lệ:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Loại ngoại lệ:</strong> {{ exception_type }}<br/>
              <strong>Mô tả:</strong> {{ exception_description }}<br/>
              <strong>Xảy ra:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Thông tin đơn hàng:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số đơn hàng:</strong> {{ order_number }}<br/>
              <strong>Số theo dõi:</strong> {{ tracking_number }}<br/>
              <strong>Người vận chuyển:</strong> {{ carrier_name }}<br/>
              <strong>Vị trí hiện tại:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Điều gì sẽ xảy ra tiếp theo?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Hành động cần thực hiện:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Theo dõi đơn hàng của bạn
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Liên hệ hỗ trợ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ NGOẠI LỆ VẬN CHUYỂN

Chào {{ customer_name }},

Chúng tôi viết email này để thông báo về ngoại lệ trong đơn hàng của bạn. Chúng tôi đang cố gắng giải quyết vấn đề này càng sớm càng có thể.

CHI TIẾT NGOẠI LỆ:
- Loại ngoại lệ: {{ exception_type }}
- Mô tả: {{ exception_description }}
- Xảy ra: {{ exception_date }}

THÔNG TIN ĐƠN HÀNG:
- Số đơn hàng: {{ order_number }}
- Số theo dõi: {{ tracking_number }}
- Người vận chuyển: {{ carrier_name }}
- Vị trí hiện tại: {{ current_location }}

ĐIỀU GÌ SẼ XẢY RA TIẾP THEO?
{{ resolution_steps }}

{% if action_required %}
⚠️ HÀNH ĐỘNG CẦN THỰC HIỆN:
{{ action_required_description }}
{% endif %}

Theo dõi đơn hàng của bạn: {{ tracking_url }}
Liên hệ hỗ trợ: {{ support_url }}