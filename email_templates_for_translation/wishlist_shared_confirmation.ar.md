---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ تم مشاركة قوائم رغباتك - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ تم مشاركة قائمة الرغبات بنجاح!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم مشاركة قائمة رغباتك بنجاح، والتي تحتوي على {{ wishlist_item_count }} عنصر{{ wishlist_item_count|pluralize }}. يمكن الآن للآخرين الاطلاع على قائمة رغباتك باستخدام الرابط أدناه.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              رابط المشاركة:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              نسخ الرابط
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما الذي تم مشاركته:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • اسم قائمة الرغبات (إذا تم تحديده)
          <br/>
          • {{ wishlist_item_count }} منتج{{ wishlist_item_count|pluralize }}
          <br/>
          • أسماء المنتجات، الصور، والأسعار
          <br/>
          • روابط الشراء لكل عنصر
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 مثالي لمشاركة القوائم مع الأصدقاء والعائلة للفترات الخاصة والمناسبات!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          إدارة قائمة رغباتي
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          هل ترغب في إيقاف المشاركة؟ يمكنك تعطيل رابط المشاركة في أي وقت من خلال <a href="{{ wishlist_settings_url }}">إعدادات قائمة رغباتك</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ قائمة الرغبات تم مشاركتها بنجاح!

مرحبًا {{ customer_name }},

تم مشاركة قائمة رغباتك بنجاح، والتي تحتوي على {{ wishlist_item_count }} عنصر{{ wishlist_item_count|pluralize }}. يمكن الآن للآخرين الاطلاع على قائمة رغباتك باستخدام الرابط أدناه.

رابط المشاركة:
{{ share_url }}

ما الذي تم مشاركته:
• اسم قائمة الرغبات (إذا تم تحديده)
• {{ wishlist_item_count }} منتج{{ wishlist_item_count|pluralize }}
• أسماء المنتجات، الصور، والأسعار
• روابط الشراء لكل عنصر

💡 مثالي لمشاركة القوائم مع الأصدقاء والعائلة للفترات الخاصة والمناسبات!

إدارة قائمة رغباتي: {{ wishlist_url }}

هل ترغب في إيقاف المشاركة؟ يمكنك تعطيل رابط المشاركة في أي وقت من خلال إعدادات قائمة رغباتك: {{ wishlist_settings_url }}