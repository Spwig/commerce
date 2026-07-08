---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
تحديث حول طلبك #{{ order_number }} - تأخير التسليم

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحديث حول طلبك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          نود إعلامك بتأخير في طلبك. نعتذر عن الإزعاج ونقدر صبرك.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1b2635' }}">
              تفاصيل الطلب:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم الطلب:</strong> {{ order_number }}<br/>
              <strong>وقت التسليم الأصلي:</strong> {{ original_delivery_date }}<br/>
              <strong>وقت التسليم الجديد:</strong> {{ new_delivery_date }}<br/>
              <strong>رقم المتابعة:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          سبب التأخير:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تتبع طلبك
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          نحن نبذل قصارى جهودنا لتوصيل طلبك إليك بأسرع ما يمكن. سيتم إرسال تحديث إضافي إليك عندما يبدأ طردك في السفر.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          لديك أسئلة؟ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بفريق خدمة العملاء لدينا</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تحديث حول طلبك #{{ order_number }}

مرحبًا {{ customer_name }},

نود إعلامك بتأخير في طلبك. نعتذر عن الإزعاج ونقدر صبرك.

تفاصيل الطلب:
- رقم الطلب: {{ order_number }}
- وقت التسليم الأصلي: {{ original_delivery_date }}
- وقت التسليم الجديد: {{ new_delivery_date }}
- رقم المتابعة: {{ tracking_number }}

سبب التأخير:
{{ delay_reason }}

تتبع طلبك: {{ tracking_url }}

نحن نبذل قصارى جهودنا لتوصيل طلبك إليك بأسرع ما يمكن. سيتم إرسال تحديث إضافي إليك عندما يبدأ طردك في السفر.

هل لديك أسئلة؟ اتصل بفريق خدمة العملاء لدينا: {{ support_url }}

---

هذا التحديث هو لطلبك #{{ order_number }} في {{ shop_name }}.