---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 تنبيه خصم: منتج {{ product_name }} الآن {{ discount_percentage }}% خصم!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 تنبيه خصم!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          احصِد {{ discount_percentage }}% على عنصر القائمة المرغوبة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أخبار جيدة، {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          منتج في قائمة المرغوبات الخاصة بك انخفض سعره! لا تفوت فرصة لتوفير المال.
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              كان: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              الآن: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              ادخار {{ savings_amount }} ({{ discount_percentage }}% خصم)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          اشترِ الآن واحفظ {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>فترة محدودة:</strong> هذه البيع لن تدوم للأبد. قد تعود الأسعار إلى الارتفاع في أي وقت!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إزالة من قائمة المرغوبات: <a href="{{ remove_wishlist_url }}">اضغط هنا</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 تنبيه خصم!
احصِد {{ discount_percentage }}% على عنصر القائمة المرغوبة

أخبار جيدة، {{ customer_name }}!

منتج في قائمة المرغوبات الخاصة بك انخفض سعره! لا تفوت فرصة لتوفير المال.

{{ product_name }}
كان: {{ original_price }}
الآن: {{ new_price }}
ادخار {{ savings_amount }} ({{ discount_percentage }}% خصم)

اشترِ الآن واحفظ {{ discount_percentage }}%: {{ product_url }}

⏰ فترة محدودة: هذه البيع لن تدوم للأبد. قد تعود الأسعار إلى الارتفاع في أي وقت!

إزالة من قائمة المرغوبات: {{ remove_wishlist_url }}