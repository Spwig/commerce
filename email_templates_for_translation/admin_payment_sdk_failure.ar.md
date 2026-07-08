---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
مشكلة مزود الدفع - فشل تحميل SDK {{ provider_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          مشكلة مزود الدفع
        </mj-text>
        <mj-text>
          فشل تحميل SDK لدفع {{ provider_name }} لعميل أثناء عملية الشراء. قد يشير هذا إلى انقطاع في خدمة المزود.
        </mj-text>
        <mj-text>
          <strong>المزود:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>نوع الخطأ:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>الوقت:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>عدد الفشل (الساعة الماضية):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          هذه الإشعار محدودة بالسرعة لمرة واحدة لكل مزود في الساعة. إذا استمرت المشكلة، يرجى التحقق من لوحة تحكم المزود أو التواصل مع دعمهم.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          عرض إعدادات الدفع
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
مشكلة مزود الدفع

فشل تحميل SDK لدفع {{ provider_name }} لعميل أثناء عملية الشراء. قد يشير هذا إلى انقطاع في خدمة المزود.

المزود: {{ provider_name }}
نوع الخطأ: {{ error_type }}
الوقت: {{ timestamp }}
عدد الفشل (الساعة الماضية): {{ failure_count }}

هذه الإشعار محدودة بالسرعة لمرة واحدة لكل مزود في الساعة. إذا استمرت المشكلة، يرجى التحقق من لوحة تحكم المزود أو التواصل مع دعمهم.

عرض إعدادات الدفع: {{ admin_url }}