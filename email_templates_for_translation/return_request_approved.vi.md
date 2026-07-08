---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Yêu cầu hoàn trả của bạn đã được chấp thuận - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Yêu cầu hoàn trả đã được chấp thuận
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Đơn hàng #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Yêu cầu hoàn trả cho đơn hàng <strong>#{{ order_number }}</strong> của bạn đã được chấp thuận.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Bước tiếp theo:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Tải xuống và in nhãn hoàn trả bên dưới<br/>
          2. Đóng gói các mặt hàng một cách an toàn trong bao bì gốc nếu có thể<br/>
          3. Dán nhãn hoàn trả lên mặt ngoài của gói hàng<br/>
          4. Giao tại điểm giao hàng gần nhất của bạn
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tải xuống nhãn hoàn trả
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Số theo dõi hoàn trả:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Quan trọng:</strong> Vui lòng gửi hoàn trả trong vòng 7 ngày để đảm bảo xử lý hoàn tiền của bạn được thực hiện nhanh chóng.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Khi chúng tôi nhận được và kiểm tra đơn hoàn trả của bạn, chúng tôi sẽ xử lý hoàn tiền về phương thức thanh toán ban đầu.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Yêu cầu hoàn trả đã được chấp thuận - Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Yêu cầu hoàn trả cho đơn hàng #{{ order_number }} của bạn đã được chấp thuận.

Bước tiếp theo:
1. Tải xuống và in nhãn hoàn trả
2. Đóng gói các mặt hàng một cách an toàn trong bao bì gốc nếu có thể
3. Dán nhãn hoàn trả lên mặt ngoài của gói hàng
4. Giao tại điểm giao hàng gần nhất của bạn

{% if return_label_url %}Tải xuống nhãn hoàn trả: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Số theo dõi hoàn trả: {{ return_tracking_number }}{% endif %}

Quan trọng: Vui lòng gửi hoàn trả trong vòng 7 ngày để đảm bảo xử lý hoàn tiền của bạn được thực hiện nhanh chóng.

Khi chúng tôi nhận được và kiểm tra đơn hoàn trả của bạn, chúng tôi sẽ xử lý hoàn tiền về phương thức thanh toán ban đầu.