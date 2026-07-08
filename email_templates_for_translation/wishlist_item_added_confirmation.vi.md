---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} đã được thêm vào danh sách yêu thích của bạn - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Đã thêm vào danh sách yêu thích của bạn!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bạn đã thành công thêm {{ product_name }} vào danh sách yêu thích. Chúng tôi sẽ theo dõi nó cho bạn!
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
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if product_in_stock %}
            <mj-text font-size="13px" color="#059669">
              ✓ Tồn kho
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ Hết hàng - Chúng tôi sẽ thông báo khi có hàng!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Chúng tôi sẽ thông báo cho bạn về:</strong><br/>
              • Giảm giá<br/>
              • Thông báo hàng trở lại<br/>
              • Khuyến mãi thời gian giới hạn
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem danh sách yêu thích của tôi
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Mua ngay
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ ĐÃ THÊM VÀO DANH SÁCH YÊU THÍCH!

Hi {{ customer_name }},

Bạn đã thành công thêm {{ product_name }} vào danh sách yêu thích. Chúng tôi sẽ theo dõi nó cho bạn!

{{ product_name }}
Giá: {{ product_price }}
{% if product_in_stock %}✓ Tồn kho{% else %}⚠️ Hết hàng - Chúng tôi sẽ thông báo khi có hàng!{% endif %}

💡 CHÚNG TÔI SẼ THÔNG BÁO CHO BẠN VỀ:
• Giảm giá
• Thông báo hàng trở lại
• Khuyến mãi thời gian giới hạn

Xem danh sách yêu thích của tôi: {{ wishlist_url }}
{% if product_in_stock %}Mua ngay: {{ product_url }}{% endif %}