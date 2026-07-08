---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Cảm ơn bạn đã đặt hàng #{{ order_number }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Cảm ơn bạn đã đặt hàng!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúng tôi rất vui mừng bạn đã hoàn tất đơn hàng! Đơn hàng của bạn đã được xác nhận và chúng tôi đang chuẩn bị để giao hàng.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Thông tin đơn hàng
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số đơn hàng:</strong> {{ order_number }}<br/>
              <strong>Ngày đặt hàng:</strong> {{ order_date }}<br/>
              <strong>Tổng cộng:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Theo dõi đơn hàng
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Điều gì sẽ xảy ra tiếp theo?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Chúng tôi sẽ chuẩn bị đơn hàng của bạn (thường trong vòng 1-2 ngày làm việc)<br/>
          2. Bạn sẽ nhận được thông báo giao hàng kèm theo thông tin theo dõi<br/>
          3. Đơn hàng của bạn sẽ được giao đến: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Bạn có biết?</strong><br/>
              Bạn có thể theo dõi đơn hàng bất kỳ lúc nào trong bảng điều khiển tài khoản của bạn.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Có câu hỏi? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Liên hệ với nhóm hỗ trợ của chúng tôi</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 CẢMƠN BẠN ĐÃ ĐẶT HÀNG!

Chào {{ customer_name }},

Chúng tôi rất vui mừng bạn đã hoàn tất đơn hàng! Đơn hàng của bạn đã được xác nhận và chúng tôi đang chuẩn bị để giao hàng.

THÔNG TIN ĐƠN HÀNG:
- Số đơn hàng: {{ order_number }}
- Ngày đặt hàng: {{ order_date }}
- Tổng cộng: {{ order_total }}

Theo dõi đơn hàng: {{ order_tracking_url }}

ĐIỀU GÌ SẼ XẢY RA TIẾP THEO?
1. Chúng tôi sẽ chuẩn bị đơn hàng của bạn (thường trong vòng 1-2 ngày làm việc)
2. Bạn sẽ nhận được thông báo giao hàng kèm theo thông tin theo dõi
3. Đơn hàng của bạn sẽ được giao đến: {{ shipping_address }}

💡 BẠN CÓ BIẾT KHÔNG?
Bạn có thể theo dõi đơn hàng bất kỳ lúc nào trong bảng điều khiển tài khoản của bạn.

Có câu hỏi? Liên hệ với nhóm hỗ trợ của chúng tôi: {{ support_url }}

---
Đơn hàng #{{ order_number }} tại {{ shop_name }}