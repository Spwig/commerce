---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
Cơ hội cuối cùng! Giỏ hàng của bạn sẽ hết hạn sau 24 giờ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ Cơ hội cuối cùng - Giỏ hàng sẽ hết hạn sau 24 giờ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Đừng bỏ lỡ, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Đây là lời nhắc cuối cùng của bạn. Giỏ hàng của bạn sẽ hết hạn sau 24 giờ và chúng tôi không thể giữ các mặt hàng này thêm nữa.
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng cộng: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Hoàn tất đơn hàng trước khi quá muộn
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Có câu hỏi? Đội ngũ của chúng tôi sẵn sàng hỗ trợ: <a href="{{ support_url }.pdf}">
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ CƠ HỘI CUỐI CÙNG - GIỎ HÀNG SẼ HẾT HẠN SAU 24 GIỜ

Đừng bỏ lỡ, {{ customer_name }}!

Đây là lời nhắc cuối cùng của bạn. Giỏ hàng của bạn sẽ hết hạn sau 24 giờ và chúng tôi không thể giữ các mặt hàng này thêm nữa.

GIỎ HÀNG CỦA BẠN:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Tổng cộng: {{ cart_total }}

Hoàn tất đơn hàng trước khi quá muộn: {{ cart_url }}

Có câu hỏi? Đội ngũ của chúng tôi sẵn sàng hỗ trợ: {{ support_url }}

---
Đây là lời nhắc cuối cùng cho giỏ hàng #{{ cart_id }}.