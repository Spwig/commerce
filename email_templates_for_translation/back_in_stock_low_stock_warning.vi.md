---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} đang trở lại nhưng đang bán nhanh! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Hàng tồn kho có giới hạn - Hành động nhanh!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} đã có hàng tồn kho!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tin vui! Sản phẩm bạn đang chờ đợi đã quay lại trong kho hàng. Nhưng hãy nhanh lên - chúng tôi chỉ còn {{ stock_remaining }} đơn vị hàng tồn kho!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Biến thể: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Chỉ còn {{ stock_remaining }} trong kho!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Mua ngay trước khi hết hàng
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>Chiếc sản phẩm này đã hết hàng {{ times_sold_out }} lần trong tháng vừa qua!</strong><br/>
              Đừng bỏ lỡ lần nữa - đặt hàng ngay khi còn hàng.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Không còn quan tâm nữa? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Hủy đăng ký thông báo này</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ HÀNG TỒN KHO HẠN CHẾ - HÀNH ĐỘNG NHANH!

{{ product_name }} đã có hàng tồn kho!

Hi {{ customer_name }},

Tin vui! Sản phẩm bạn đang chờ đợi đã quay lại trong kho hàng. Nhưng hãy nhanh lên - chúng tôi chỉ còn {{ stock_remaining }} đơn vị hàng tồn kho!

SẢN PHẨM:
{{ product_name }}
{{ product_description }}
Giá: {{ product_price }}
{% if variant_name %}Biến thể: {{ variant_name }}{% endif %}

⚠️ CHỈ CÒN {{ stock_remaining }} TRONG KHO!

Mua ngay trước khi hết hàng: {{ product_url }}

🔥 Chiếc sản phẩm này đã hết hàng {{ times_sold_out }} lần trong tháng vừa qua!
Đừng bỏ lỡ lần nữa - đặt hàng ngay khi còn hàng.

Không còn quan tâm nữa? Hủy đăng ký: {{ unsubscribe_url }}