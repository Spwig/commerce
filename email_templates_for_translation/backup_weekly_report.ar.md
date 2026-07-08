---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
ملخص النسخ الاحتياطية الأسبوعية - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص النسخ الاحتياطية الأسبوعية
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              إحصائيات النسخ الاحتياطية:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>إجمالي النسخ الاحتياطية:</strong> {{ total_backups }}<br/>
              <strong> الناجحة:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>الم thấtلة:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>الحجم المتوسط:</strong> {{ average_size }}<br/>
              <strong>التخزين المستخدم الكلي:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ تم اكتشاف مشاكل:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} نسخ احتياطية (مُتعددة) فشلت هذا الأسبوع. يرجى مراجعة واتخاذ الإجراء التصحيحية.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أحدث النسخ الاحتياطية:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              الحجم: {{ backup.size }} | المدة: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ النجاح</span>
              {% else %}
              <span style="color: #dc2626;">✗ الفشل</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          عرض جميع النسخ الاحتياطية
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ملخص النسخ الاحتياطية الأسبوعية
{{ week_start }} - {{ week_end }}

إحصائيات النسخ الاحتياطية:
- إجمالي النسخ الاحتياطية: {{ total_backups }}
- الناجحة: {{ successful_backups }}
- الم thấtلة: {{ failed_backups }}
- الحجم المتوسط: {{ average_size }}
- التخزين المستخدم الكلي: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ تم اكتشاف مشاكل:
{{ failed_backups }} نسخ احتياطية (مُتعددة) فشلت هذا الأسبوع. يرجى مراجعة واتخاذ الإجراء التصحيحية.
{% endif %}

أحدث النسخ الاحتياطية:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  الحجم: {{ backup.size }} | المدة: {{ backup.duration }} | الحالة: {{ backup.status }}
{% endfor %}

عرض جميع النسخ الاحتياطية: {{ admin_backup_url }}