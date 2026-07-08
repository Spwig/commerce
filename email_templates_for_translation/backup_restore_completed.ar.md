---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ اكتمال استعادة النسخة الاحتياطية - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ اكتمال استعادة النسخة الاحتياطية
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تمت استعادة نسخة احتياطية ناجحة. تم استعادة بيانات متجرك.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الاستعادة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ملف النسخة الاحتياطية:</strong> {{ backup_filename }}<br/>
              <strong>تاريخ النسخة الاحتياطية:</strong> {{ backup_date }}<br/>
              <strong>بدأ:</strong> {{ restore_started_at }}<br/>
              <strong>اكتمال:</strong> {{ restore_completed_at }}<br/>
              <strong>المدة:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ الخطوات المهمة التالية:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. تأكد من أن متجرك يعمل بشكل صحيح<br/>
              2. تحقق من البيانات الرئيسية (المنتجات، الطلبات، العملاء)<br/>
              3. احذف التخزين المؤقت إذا لزم الأمر<br/>
              4. اخضع لاختبار العمليات الحاسمة (الدفع، الوصول إلى لوحة التحكم)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          الانتقال إلى لوحة التحكم الإدارية
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ اكتمال استعادة النسخة الاحتياطية

مرحباً {{ admin_name }},

تمت استعادة نسخة احتياطية ناجحة. تم استعادة بيانات متجرك.

تفاصيل الاستعادة:
- ملف النسخة الاحتياطية: {{ backup_filename }}
- تاريخ النسخة الاحتياطية: {{ backup_date }}
- بدأت: {{ restore_started_at }}
- اكتمال: {{ restore_completed_at }}
- المدة: {{ restore_duration }}

⚠️ الخطوات المهمة التالية:
1. تأكد من أن متجرك يعمل بشكل صحيح
2. تحقق من البيانات الرئيسية (المنتجات، الطلبات، العملاء)
3. احذف التخزين المؤقت إذا لزم الأمر
4. اخضع لاختبار العمليات الحاسمة (الدفع، الوصول إلى لوحة التحكم)

الانتقال إلى لوحة التحكم الإدارية: {{ admin_dashboard_url }}