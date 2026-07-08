---
template_type: back_in_stock_waitlist_confirmation
category: Stock Notifications
---

# Email Template: back_in_stock_waitlist_confirmation

## Subject
✓ Bạn đã đăng ký danh sách chờ cho {{ product_name }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Bạn đã đăng ký danh sách chờ!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cảm ơn bạn đã đăng ký! Chúng tôi sẽ thông báo cho bạn ngay khi sản phẩm này có sẵn trở lại.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Biến thể: {{ variant_name }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Điều bạn có thể mong đợi:</strong><br/>
              Chúng tôi sẽ gửi email cho bạn ngay khi sản phẩm này được tái cung cấp. Số lượng hàng tồn kho có giới hạn, vì vậy hãy hành động nhanh khi bạn được thông báo!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Trong khi chờ đợi...
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Hãy xem những sản phẩm tương tự này đang có sẵn hiện tại:
        </mj-text>

        {% for product in similar_products %}
        <mj-spacer height="10px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column width="25%">
            <mj-image src="{{ product.image }}" alt="{{ product.name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product.price }}
            </mj-text>
            <mj-text font-size="13px">
              <a href="{{ product.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Xem sản phẩm →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Thay đổi ý định? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Hủy đăng ký danh sách chờ này</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BẠN ĐÃ ĐĂNG KÝ DANH SÁCH CHỜ!

Chào {{ customer_name }},

Cảm ơn bạn đã đăng ký! Chúng tôi sẽ thông báo cho bạn ngay khi sản phẩm này có sẵn trở lại.

SẢN PHẨM:
{{ product_name }}
{{ product_description }}
Giá: {{ product_price }}
{% if variant_name %}Biến thể: {{ variant_name }}{% endif %}

💡 ĐIỀU BẠN CÓ THỂ MONG ĐỢI:
Chúng tôi sẽ gửi email cho bạn ngay khi sản phẩm này được tái cung cấp. Số lượng hàng tồn kho có giới hạn, vì vậy hãy hành động nhanh khi bạn được thông báo!

TRONG KHI CHỜ ĐỢI...
Hãy xem những sản phẩm tương tự này đang có sẵn hiện tại:
{% for product in similar_products %}
- {{ product.name }} - {{ product.price }}
  {{ product.url }}
{% endfor %}

Thay đổi ý định? Hủy đăng ký danh sách chờ này: {{ unsubscribe_url }}