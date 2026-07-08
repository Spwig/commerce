---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 تخزين نسخة احتياطية الحصة الحرجة - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 الحصة الحرجة لتخزين
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>عاجل:</strong> تخزين النسخ الاحتياطية الخاص بك منخفض بشكل خطير. قد تفشل النسخ الاحتياطية المستقبلية إذا لم يتم تحرير مساحة التخزين.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              حالة التخزين:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>المستخدم:</strong> {{ storage_used }} من {{ storage_total }}<br/>
              <strong>معدل الاستخدام:</strong> {{ storage_percentage }}%<br/>
              <strong>التوفر:</strong> {{ storage_available }}<br/>
              <strong>الحالة:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              الإجراءات الفورية المطلوبة:
            </mj-text>
            <mj-text color="#92400e">
              1. حذف النسخ الاحتياطية القديمة التي لم تعد مطلوبة<br/>
              2. أ存档 النسخ الاحتياطية إلى تخزين خارجي<br/>
              3. زيادة الحصة/القدرة على التخزين<br/>
              4. مراجعة سياسة الاحتفاظ بالنسخ الاحتياطية<br/>
              5. مراقبة التخزين يوميًا حتى يتم حل المشكلة
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          إداره التخزين الآن
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 الحصة الحرجة لتخزين

مرحبا {{ admin_name }},

عاجل: تخزين النسخ الاحتياطية الخاص بك منخفض بشكل خطير. قد تفشل النسخ الاحتياطية المستقبلية إذا لم يتم تحرير مساحة التخزين.

حالة التخزين:
- المستخدم: {{ storage_used }} من {{ storage_total }}
- معدل الاستخدام: {{ storage_percentage }}%
- التوفر: {{ storage_available }}
- الحالة: {{ storage_status }}

الإجراءات الفورية المطلوبة:
1. حذف النسخ الاحتياطية القديمة التي لم تعد مطلوبة
2. أ存档 النسخ الاحتياطية إلى تخزين خارجي
3. زيادة الحصة/القدرة على التخزين
4. مراجعة سياسة الاحتفاظ بالنسخ الاحتياطية
5. مراقبة التخزين يوميًا حتى يتم حل المشكلة

إدارة التخزين الآن: {{ admin_backup_url }}