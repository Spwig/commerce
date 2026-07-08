---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Vẫn quan tâm chứ? Giỏ hàng của bạn sắp hết hạn - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Giỏ hàng {{ cart_item_count }} mục của bạn vẫn đang chờ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúng tôi đang giữ giỏ hàng cho bạn, nhưng những mặt hàng này sẽ không tồn tại mãi. Hoàn tất đơn hàng trước khi chúng bị bán hết!
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
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ Chỉ còn {{ item.stock_remaining }} sản phẩm trong kho!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Hoàn tất đơn hàng ngay
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Miễn phí vận chuyển cho đơn hàng trên {{ free_shipping_threshold }}<br/>
              ✓ Cam kết hoàn tiền trong 30 ngày<br/>
              ✓ Thanh toán an toàn
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Giỏ hàng {{ cart_item_count }} mục của bạn vẫn đang chờ

Chào {{ customer_name }},

Chúng tôi đang giữ giỏ hàng cho bạn, nhưng những mặt hàng này sẽ không tồn tại mãi. Hoàn tất đơn hàng trước khi chúng bị bán hết!

GIỎ HÀNG:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Chỉ còn {{ item.stock_remaining }} sản phẩm trong kho!{% endif %}
{% endfor %}

Tổng: {{ cart_total }}

Hoàn tất đơn hàng ngay: {{ cart_url }}

TẠI SAO MUA SẮM VỚI CHÚNG TÔI:
✓ Miễn phí vận chuyển cho đơn hàng trên {{ free_shipping_threshold }}
✓ Cam kết hoàn tiền trong 30 ngày
✓ Thanh toán an toàn

---
Để dừng nhận thông báo giỏ hàng, vui lòng truy cập: {{ preferences_url }}