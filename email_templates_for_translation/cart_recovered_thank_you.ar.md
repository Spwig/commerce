---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
شكرًا لك على طلبك #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 شكرًا لك على طلبك!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          نحن سعداء جدًا لأنك أنهيت شراءك! تم تأكيد طلبك ونحن نقوم بإعداده للشحن.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ملخص الطلب
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم الطلب:</strong> {{ order_number }}<br/>
              <strong>تاريخ الطلب:</strong> {{ order_date }}<br/>
              <strong>المجموع:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تتبع طلبك
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا يحدث بعد ذلك؟
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. سنقوم بإعداد طلبك (عادةً خلال 1-2 أيام عمل)<br/>
          2. ستحصل على رسالة تأكيد الشحن مع معلومات تتبع الطلب<br/>
          3. سيتم تسليم طلبك إلى: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>هل تعلم أن:</strong><br/>
              يمكنك تتبع طلبك في أي وقت من لوحة تحكم حسابك.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          هل لديك أسئلة؟ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بفريق الدعم لدينا</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 شكرًا لك على طلبك!

Hi {{ customer_name }},

نحن سعداء جدًا لأنك أنهيت شراءك! تم تأكيد طلبك ونحن نقوم بإعداده للشحن.

ملخص الطلب:
- رقم الطلب: {{ order_number }}
- تاريخ الطلب: {{ order_date }}
- المجموع: {{ order_total }}

تتبع طلبك: {{ order_tracking_url }}

ماذا يحدث بعد ذلك؟
1. سنقوم بإعداد طلبك (عادةً خلال 1-2 أيام عمل)
2. ستحصل على رسالة تأكيد الشحن مع معلومات تتبع الطلب
3. سيتم تسليم طلبك إلى: {{ shipping_address }}

💡 هل تعلم أن:
يمكنك تتبع طلبك في أي وقت من لوحة تحكم حسابك.

هل لديك أسئلة؟ اتصل بفريق الدعم لدينا: {{ support_url }}

---
طلب #{{ order_number }} في {{ shop_name }}