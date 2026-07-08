---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
⚠️ خطير: فشل استعادة النسخة الاحتياطية - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ خطير: فشل استعادة النسخة الاحتياطية
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          يا {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          فشلت عملية استعادة النسخة الاحتياطية الخطيرة. قد تكون متجرك في حالة غير متسقة ويحتاج إلى انتباه فوري.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              تفاصيل الاستعادة:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>ملف النسخة الاحتياطية:</strong> {{ backup_filename }}<br/>
              <strong>بدأ:</strong> {{ restore_started_at }}<br/>
              <strong>فشل:</strong> {{ restore_failed_at }}<br/>
              <strong>المدة:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              ⚠️ إجراء فوري مطلوب:
            </mj-text>
            <mj-text color="#92400e">
              1. لا <strong>تُجري</strong> أي تغييرات على المتجر<br/>
              2. تحقق من اتصال قاعدة البيانات وسلامتها<br/>
              3. اراجع سجلات الأخطاء للحصول على مسار الأكواد التفصيلي<br/>
              4. تواصل فورًا مع الدعم الفني<br/>
              5. فكّر في العودة إلى الحالة الجيدة الأخيرة
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض سجلات الاستعادة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          التواصل مع الدعم الطارئ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ خطير: فشل استعادة النسخة الاحتياطية

يا {{ admin_name }},

فشل عملية استعادة النسخة الاحتياطية الخطيرة. قد تكون متجرك في حالة غير متسقة ويحتاج إلى انتباه فوري.

تفاصيل الاستعادة:
- ملف النسخة الاحتياطية: {{ backup_filename }}
- بدأت: {{ restore_started_at }}
- فشلت: {{ restore_failed_at }}
- المدة: {{ restore_duration }}

تفاصيل الخطأ:
{{ error_message }}

⚠️ إجراء فوري مطلوب:
1. لا تُجري أي تغييرات على المتجر
2. تحقق من اتصال قاعدة البيانات وسلامتها
3. اراجع سجلات الأخطاء للحصول على مسار الأكواد التفصيلي
4. تواصل فورًا مع الدعم الفني
5. فكّر في العودة إلى الحالة الجيدة الأخيرة

عرض سجلات الاستعادة: {{ admin_backup_url }}
التواصل مع الدعم الطارئ: {{ support_url }}