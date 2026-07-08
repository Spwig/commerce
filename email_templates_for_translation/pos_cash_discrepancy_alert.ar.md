---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ تنبيه عدم تطابق النقود: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ تم اكتشاف عدم تطابق في النقود
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تنبيه تباين النقود
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم اكتشاف عدم تطابق في المبلغ {{ discrepancy_amount }} عند إغلاق الوردية في {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل عدم التطابق:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>النقطة:</strong> {{ terminal_name }}<br/>
              <strong>البائع:</strong> {{ cashier_name }}<br/>
              <strong>تاريخ الوردية:</strong> {{ shift_date }}<br/>
              <strong>مدة الوردية:</strong> {{ shift_duration }}<br/>
              <strong>تم اكتشافه:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          عد النقود:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>المبلغ المتوقع:</strong> {{ expected_cash }}<br/>
              <strong>المبلغ المعد:</strong> {{ counted_cash }}<br/>
              <strong>عدم التطابق:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>النقود المفتوحة:</strong> {{ opening_cash }}<br/>
              <strong>مبيعات النقد:</strong> {{ cash_sales }}<br/>
              <strong>استبدالات النقد:</strong> {{ cash_refunds }}<br/>
              <strong>النقود المدفوعة:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملاحظة البائع:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات المقترحة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. مراجعة سجل المعاملات للتحقق من الأخطاء<br/>
          2. تحقق من المدفوعات النقدية غير المسجلة<br/>
          3. تأكيد دقة عد النقود<br/>
          4. تسجيل عدم التطابق في ملاحظات الوردية<br/>
          5. التواصل مع البائع إذا لزم الأمر
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض تقرير الوردية
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          مراجعة المعاملات
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ تم اكتشاف عدم تطابق في النقود

تنبيه تباين النقود

تم اكتشاف عدم تطابق في المبلغ {{ discrepancy_amount }} عند إغلاق الوردية في {{ terminal_name }}.

تفاصيل عدم التطابق:
- النقطة: {{ terminal_name }}
- البائع: {{ cashier_name }}
- تاريخ الوردية: {{ shift_date }}
- مدة الوردية: {{ shift_duration }}
- تم اكتشافه: {{ detected_at }}

عد النقود:
- المبلغ المتوقع: {{ expected_cash }}
- المبلغ المعد: {{ counted_cash }}
- عدم التطابق: {{ discrepancy_amount }}

التفصيل:
- النقود المفتوحة: {{ opening_cash }}
- مبيعات النقد: {{ cash_sales }}
- استبدالات النقد: {{ cash_refunds }}
- النقود المدفوعة: {{ cash_paid_out }}

{% if cashier_note %}
ملاحظة البائع:
"{{ cashier_note }}"
{% endif %}

الإجراءات المقترحة:
1. مراجعة سجل المعاملات للتحقق من الأخطاء
2. تحقق من المدفوعات النقدية غير المسجلة
3. تأكيد دقة عد النقود
4. تسجيل عدم التطابق في ملاحظات الوردية
5. التواصل مع البائع إذا لزم الأمر

عرض تقرير الوردية: {{ shift_report_url }}
مراجعة المعاملات: {{ transaction_history_url }}