---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Hoàn tiền đã được xử lý - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Hoàn tiền đã được xử lý
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
          Việc hoàn trả cho đơn hàng <strong>#{{ order_number }}</strong> của bạn đã được kiểm tra và hoàn tiền của bạn đã được xử lý.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Chi tiết hoàn tiền
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số tiền hoàn lại:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Phí hoàn trả:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Lưu ý:</strong> Việc hoàn tiền có thể mất 5-10 ngày làm việc để hiển thị trên tài khoản của bạn, tùy thuộc vào nhà cung cấp thanh toán của bạn.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nếu bạn có bất kỳ câu hỏi nào về hoàn tiền của bạn, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hoàn tiền đã được xử lý - Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Việc hoàn trả cho đơn hàng #{{ order_number }} của bạn đã được kiểm tra và hoàn tiền của bạn đã được xử lý.

Chi tiết hoàn tiền:
- Số tiền hoàn lại: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Phí hoàn trả: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Lưu ý: Việc hoàn tiền có thể mất 5-10 ngày làm việc để hiển thị trên tài khoản của bạn, tùy thuộc vào nhà cung cấp thanh toán của bạn.

Nếu bạn có bất kỳ câu hỏi nào về hoàn tiền của bạn, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.