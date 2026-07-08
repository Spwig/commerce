---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
Giỏ hàng của bạn đang chờ! Hoàn tất đơn hàng - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bạn đã để lại {{ cart_item_count }} mặt hàng trong giỏ hàng của mình
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúng tôi nhận thấy bạn chưa hoàn tất việc mua hàng. Các mặt hàng của bạn vẫn đang chờ trong giỏ hàng!
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
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng cộng: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Hoàn tất đơn hàng
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Cần hỗ trợ? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Liên hệ với nhóm hỗ trợ của chúng tôi</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bạn đã để lại {{ cart_item_count }} mặt hàng trong giỏ hàng của mình

Hi {{ customer_name }},

Chúng tôi nhận thấy bạn chưa hoàn tất việc mua hàng. Các mặt hàng của bạn vẫn đang chờ trong giỏ hàng!

GIỎ HÀNG:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Tổng cộng: {{ cart_total }}

Hoàn tất đơn hàng: {{ cart_url }}

Cần hỗ trợ? Liên hệ với nhóm hỗ trợ của chúng tôi: {{ support_url }}

---
Bạn đang nhận được email này vì bạn đã thêm các mặt hàng vào giỏ hàng tại {{ shop_name }}.
Để dừng nhận các lời nhắc giỏ hàng, vui lòng truy cập: {{ preferences_url }}