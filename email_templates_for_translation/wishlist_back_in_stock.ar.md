---
template_type: wishlist_back_in_stock
category: Wishlist
---

# Email Template: wishlist_back_in_stock

## Subject
✓ عاد {{ product_name }} إلى المخزون! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ عاد إلى المخزون!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أخبار سارة، {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          منتج من قائمتك المرغوب فيه عاد إلى المخزون. احصل عليه قبل أن ينفد مرة أخرى!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            <mj-text font-size="14px" color="#059669" font-weight="bold">
              ✓ الآن في المخزون
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          اشترِ الآن
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إزالة من قائمة الرغبات: <a href="{{ remove_wishlist_url }}">اضغط هنا</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ عاد إلى المخزون!

أخبار سارة، {{ customer_name }}!

منتج من قائمتك المرغوب فيه عاد إلى المخزون. احصل عليه قبل أن ينفد مرة أخرى!

{{ product_name }}
سعر: {{ product_price }}
✓ الآن في المخزون

اشترِ الآن: {{ product_url }}

إزالة من قائمة الرغبات: {{ remove_wishlist_url }}