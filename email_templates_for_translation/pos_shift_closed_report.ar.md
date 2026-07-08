---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 تقرير التحويل: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 تم إغلاق التحويل
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تقرير ملخص التحويل
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم إغلاق التحويل على {{ terminal_name }} بواسطة {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التحويل:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الجهاز:</strong> {{ terminal_name }}<br/>
              <strong>النصاب:</strong> {{ cashier_name }}<br/>
              <strong>بدأ:</strong> {{ shift_started }}<br/>
              <strong>انتهى:</strong> {{ shift_ended }}<br/>
              <strong>المدة:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص المبيعات:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المبيعات الإجمالية:</strong> {{ total_sales }}<br/>
              <strong>المعاملات:</strong> {{ transaction_count }}<br/>
              <strong>العناصر المباعة:</strong> {{ items_sold }}<br/>
              <strong>المبيعات المتوسطة:</strong> {{ average_sale }}<br/>
              <strong>الضرائب المجمعة:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تفكيك الدفع:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} معاملات)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          مطابقة النقد:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>النقد المفتوح:</strong> {{ opening_cash }}<br/>
              <strong>مبيعات النقد:</strong> {{ cash_sales }}<br/>
              <strong>النقد المتوقع:</strong> {{ expected_cash }}<br/>
              <strong>النقد المؤقت:</strong> {{ counted_cash }}<br/>
              <strong>الفرق:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ فرق في النقد: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              ملاحظة: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض التقرير الكامل
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 تم إغلاق التحويل

تقرير ملخص التحويل

تم إغلاق التحويل على {{ terminal_name }} بواسطة {{ cashier_name }}.

تفاصيل التحويل:
- الجهاز: {{ terminal_name }}
- النصاب: {{ cashier_name }}
- بدأ: {{ shift_started }}
- انتهى: {{ shift_ended }}
- المدة: {{ shift_duration }}

ملخص المبيعات:
- المبيعات الإجمالية: {{ total_sales }}
- المعاملات: {{ transaction_count }}
- العناصر المباعة: {{ items_sold }}
- المبيعات المتوسطة: {{ average_sale }}
- الضرائب المجمعة: {{ tax_collected }}

تفكيك الدفع:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} معاملات)
{% endfor %}

مطابقة النقد:
- النقد المفتوح: {{ opening_cash }}
- مبيعات النقد: {{ cash_sales }}
- النقد المتوقع: {{ expected_cash }}
- النقد المؤقت: {{ counted_cash }}
- الفرق: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ فرق في النقد: {{ discrepancy_amount }}
{% if discrepancy_note %}ملاحظة: {{ discrepancy_note }}{% endif %}
{% endif %}

عرض التقرير الكامل: {{ shift_report_url }}