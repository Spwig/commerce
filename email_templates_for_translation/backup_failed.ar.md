---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
⚠️ طارئ: فشل النسخ الاحتياطي - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ فشل النسخ الاحتياطي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          توقفت عملية النسخ الاحتياطي الحرجة لمستودرك {{ shop_name }}. يتطلب الأمر إجراءً فوريًا لضمان حماية البيانات.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              تفاصيل النسخ الاحتياطي:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>نوع النسخ الاحتياطي:</strong> {{ backup_type }}<br/>
              <strong>بدأ:</strong> {{ backup_started_at }}<br/>
              <strong>فشل:</strong> {{ backup_failed_at }}<br/>
              <strong>المدة:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تفاصيل الخطأ:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات المقترحة:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. تحقق من مساحة القرص المتاحة على خادمك<br/>
          2. تأكد من اتصال قاعدة البيانات<br/>
          3. راجع سجل الأخطاء للحصول على مسار التتبع التفصيلي<br/>
          4. جرّب النسخ الاحتياطي مرة أخرى يدويًا أو انتظر التشغيل التالي المجدول<br/>
          5. تواصل مع الدعم إذا استمرت المشكلة
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض سجلات النسخ الاحتياطي
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          جرّب النسخ الاحتياطي الآن
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>آخر نسخ احتياطي ناجح:</strong> {{ last_successful_backup }}<br/>
          <strong>النسخ الاحتياطي التالي المجدول:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ طارئ: فشل النسخ الاحتياطي

مرحباً {{ admin_name }},

توقفت عملية النسخ الاحتياطي الحرجة لمستودرك {{ shop_name }}. يتطلب الأمر إجراءً فوريًا لضمان حماية البيانات.

تفاصيل النسخ الاحتياطي:
- نوع النسخ الاحتياطي: {{ backup_type }}
- بدأت: {{ backup_started_at }}
- فشل: {{ backup_failed_at }}
- المدة: {{ backup_duration }}

تفاصيل الخطأ:
{{ error_message }}

الإجراءات المقترحة:
1. تحقق من مساحة القرص المتاحة على خادمك
2. تأكد من اتصال قاعدة البيانات
3. راجع سجل الأخطاء للحصول على مسار التتبع التفصيلي
4. جرّب النسخ الاحتياطي مرة أخرى يدويًا أو انتظر التشغيل التالي المجدول
5. تواصل مع الدعم إذا استمرت المشكلة

عرض سجلات النسخ الاحتياطي: {{ admin_backup_url }}
جرّب النسخ الاحتياطي الآن: {{ retry_backup_url }}

آخر نسخ احتياطي ناجح: {{ last_successful_backup }}
النسخ الاحتياطي التالي المجدول: {{ next_scheduled_backup }}

---
هذا تنبيه نظامي حرجة للمديرين {{ shop_name }}.