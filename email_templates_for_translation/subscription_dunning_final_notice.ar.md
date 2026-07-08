---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ إشعار نهائي: سيتم إلغاء الاشتراك الخاص بك في {{ days_until_cancellation }} أيام

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ إشعار نهائي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          قرب إلغاء الاشتراك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحبًا {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          هذا هو إشعارك النهائي. لم نتمكن من معالجة الدفع لاشتراكك في {{ plan_name }}. إذا لم نستلم الدفع خلال {{ days_until_cancellation }} أيام، سيتم إلغاء اشتراكك.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ فشل الدفع - الإجراء المطلوب
            </mj-text>
            <mj-text color="#991b1b">
              <strong>الاشتراك:</strong> {{ plan_name }}<br/>
              <strong>المبلغ المستحق:</strong> {{ amount_due }}<br/>
              <strong>المحاولات الفاشلة:</strong> {{ retry_count }}<br/>
              <strong>المحاولة الأخيرة:</strong> {{ last_retry_date }}<br/>
              <strong>تاريخ الإلغاء:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          خطأ في الدفع:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا سيحدث:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          إذا لم يتم استلام الدفع بحلول {{ cancellation_date }}:<br/>
          • سيتم إلغاء اشتراكك<br/>
          • ستفقد الوصول إلى جميع مزايا الاشتراك<br/>
          • قد يتم حذف بياناتك (راجع سياسة الاحتفاظ بالبيانات)<br/>
          • ستحتاج إلى الاشتراك مرة أخرى للحصول على الوصول
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          قم بتحديث وسيلة الدفع الآن
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          قم بتحديث وسيلة الدفع
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          المشاكل الشائعة والحلول:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>بطاقة منتهية الصلاحية:</strong> قم بتحديثها ببطاقة ائتمانية سارية<br/>
          • <strong>رصيد غير كافٍ:</strong> تأكد من وجود رصيد كافٍ<br/>
          • <strong>البطاقة رفضت:</strong> تواصل مع بنكك أو استخدم بطاقة مختلفة<br/>
          • <strong>عدم توافق العنوان:</strong> تحقق من توافق عنوان الفاتورة مع البطاقة
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              هل تحتاج إلى مساعدة؟
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              إذا كنت تعاني من مشاكل في الدفع أو تحتاج إلى مساعدة، يرجى التواصل فورًا مع فريق دعمنا.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          تواصل مع الدعم
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إذا كنت ترغب في إلغاء اشتراكك، يمكنك القيام بذلك في إعدادات حسابك.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ إشعار نهائي

قرب إلغاء الاشتراك

مرحبًا {{ customer_name }},

هذا هو إشعارك النهائي. لم نتمكن من معالجة الدفع لاشتراكك في {{ plan_name }}. إذا لم نستلم الدفع خلال {{ days_until_cancellation }} أيام، سيتم إلغاء اشتراكك.

⚠️ فشل الدفع - الإجراء المطلوب:
- الاشتراك: {{ plan_name }}
- المبلغ المستحق: {{ amount_due }}
- المحاولات الفاشلة: {{ retry_count }}
- المحاولة الأخيرة: {{ last_retry_date }}
- تاريخ الإلغاء: {{ cancellation_date }}

خطأ في الدفع:
{{ payment_error_message }}

ماذا سيحدث:
إذا لم يتم استلام الدفع بحلول {{ cancellation_date }}:
• سيتم إلغاء اشتراكك
• ستفقد الوصول إلى جميع مزايا الاشتراك
• قد يتم حذف بياناتك (راجع سياسة الاحتفاظ بالبيانات)
• ستحتاج إلى الاشتراك مرة أخرى للحصول على الوصول

قم بتحديث وسيلة الدفع الآن

المشاكل الشائعة والحلول:
• بطاقة منتهية الصلاحية: قم بتحديثها ببطاقة ائتمانية سارية
• رصيد غير كافٍ: تأكد من وجود رصيد كافٍ
• البطاقة رفضت: تواصل مع بنكك أو استخدم بطاقة مختلفة
• عدم توافق العنوان: تحقق من توافق عنوان الفاتورة مع البطاقة

هل تحتاج إلى مساعدة؟
إذا كنت تعاني من مشاكل في الدفع أو تحتاج إلى مساعدة، يرجى التواصل فورًا مع فريق دعمنا.

تحديث وسيلة الدفع: {{ update_payment_url }}
تواصل مع الدعم: {{ support_url }}

إذا كنت ترغب في إلغاء اشتراكك، يمكنك القيام بذلك في إعدادات حسابك.