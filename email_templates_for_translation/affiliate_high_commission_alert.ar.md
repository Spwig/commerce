---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ تم اكتشاف نشاط عمولة غير معتاد - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ تنبيه عمولة مرتفعة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم اكتشاف نشاط غير معتاد
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم تحقيق عمولة غير معتادة مرتفعة من قِبل الوكيل {{ affiliate_name }}. هذا يتطلب مراجعة للوقاية من الاحتيال.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التنبيه:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الوكيل:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>مبلغ العمولة:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>قيمة الطلب:</strong> {{ order_value }}<br/>
              <strong>رقم الطلب:</strong> {{ order_number }}<br/>
              <strong>تم الكشف عنه:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          السبب في تحذير هذا:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات المقترحة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • قم بمراجعة تفاصيل الطلب للتحقق من صحتها<br/>
          • تحقق من سجل الإحالات للوكيل<br/>
          • تأكد من أن العميل ليس مرتبطًا بالإحال،
          • قم بالموافقة أو رفض العمولة من خلال لوحة التحكم الإدارية
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          مراجعة العمولة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض تفاصيل الوكيل
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          هذه العمولة قيد المراجعة ولن تتم دفعها حتى تتم الموافقة عليها.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ تنبيه عمولة مرتفعة

نشاط غير معتاد تم اكتشافه

تم تحقيق عمولة غير معتادة مرتفعة من قِبل الوكيل {{ affiliate_name }}. هذا يتطلب مراجعة للوقاية من الاحتيال.

تفاصيل التنبيه:
- الوكيل: {{ affiliate_name }} ({{ affiliate_id }})
- مبلغ العمولة: {{ commission_amount }}
- قيمة الطلب: {{ order_value }}
- رقم الطلب: {{ order_number }}
- تم الكشف عنه: {{ detected_at }}

السبب في تحذير هذا:
{{ flag_reason }}

الإجراءات المقترحة:
• قم بمراجعة تفاصيل الطلب للتحقق من صحتها
• تحقق من سجل الإحالات للوكيل
• تأكد من أن العميل ليس مرتبطًا بالإحال
• قم بالموافقة أو رفض العمولة من خلال لوحة التحكم الإدارية

مراجعة العمولة: {{ review_commission_url }}
عرض تفاصيل الوكيل: {{ affiliate_details_url }}

هذه العمولة قيد المراجعة ولن تتم دفعها حتى تتم الموافقة عليها.