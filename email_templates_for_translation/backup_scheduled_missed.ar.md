---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ لم تتم تنفيذ النسخ الاحتياطي المجدول - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ لم تتم تنفيذ النسخ الاحتياطي المجدول
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          لم تتم تنفيذ نسخة احتياطية مجدولة لـ {{ shop_name }} كما هو متوقع. قد لا يكون بياناتك م受到完全保护。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل جدول النسخ الاحتياطية:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الوقت المخطط له:</strong> {{ scheduled_time }}<br/>
              <strong>نوع النسخ الاحتياطي:</strong> {{ backup_type }}<br/>
              <strong>آخر نسخة احتياطية ناجحة:</strong> {{ last_successful_backup }}<br/>
              <strong>الوقت منذ آخر نسخة احتياطية:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسباب المحتملة:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • كان الخادم خارج الخدمة أو غير قابل للوصول<br/>
          • خدمة المهام المجدولة غير نشطة<br/>
          • أذونات غير كافية<br/>
          • مساحة التخزين ممتلئة<br/>
          • مشاكل في اتصال قاعدة البيانات
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          قم بتشغيل النسخ الاحتياطي يدويًا
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض سجلات النظام
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ لم تتم تنفيذ النسخ الاحتياطي المجدول

مرحباً {{ admin_name }},

لم تتم تنفيذ نسخة احتياطية مجدولة لـ {{ shop_name }} كما هو متوقع. قد لا يكون بياناتك م受到完全保护。

تفاصيل جدول النسخ الاحتياطية:
- الوقت المخطط له: {{ scheduled_time }}
- نوع النسخ الاحتياطي: {{ backup_type }}
- آخر نسخة احتياطية ناجحة: {{ last_successful_backup }}
- الوقت منذ آخر نسخة احتياطية: {{ time_since_last }}

الأسباب المحتملة:
• كان الخادم خارج الخدمة أو غير قابل للوصول
• خدمة المهام المجدولة غير نشطة
• أذونات غير كافية
• مساحة التخزين ممتلئة
• مشاكل في اتصال قاعدة البيانات

تشغيل النسخ الاحتياطي يدويًا: {{ admin_backup_url }}
عرض سجلات النظام: {{ admin_logs_url }}