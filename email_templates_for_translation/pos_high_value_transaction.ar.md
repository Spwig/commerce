---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 عملية مالية كبيرة: {{ transaction_amount }} في {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 عملية مالية كبيرة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم معالجة عملية مالية كبيرة
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم معالجة عملية بقيمة {{ transaction_amount }} في {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل العملية:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المبلغ:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>النقطة:</strong> {{ terminal_name }}<br/>
              <strong>البائع:</strong> {{ cashier_name }}<br/>
              <strong>الوقت:</strong> {{ transaction_time }}<br/>
              <strong>رقم العملية:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          معلومات الدفع:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص العناصر:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>إجمالي العناصر:</strong> {{ item_count }}<br/>
              <strong>المجموع الفرعي:</strong> {{ subtotal }}<br/>
              <strong>الضرائب:</strong> {{ tax_amount }}<br/>
              <strong>المجموع:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          معلومات العميل:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              يتم إرسال هذا الإشعار لكل عملية تتجاوز {{ threshold_amount }} بهدف منع الاحتيال والرصد.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض العملية
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض الفاتورة
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 عملية مالية كبيرة

تم معالجة عملية مالية كبيرة

تم معالجة عملية بقيمة {{ transaction_amount }} في {{ terminal_name }}.

تفاصيل العملية:
- المبلغ: {{ transaction_amount }}
- النقطة: {{ terminal_name }}
- البائع: {{ cashier_name }}
- الوقت: {{ transaction_time }}
- رقم العملية: {{ transaction_id }}

معلومات الدفع:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

ملخص العناصر:
- إجمالي العناصر: {{ item_count }}
- المجموع الفرعي: {{ subtotal }}
- الضرائب: {{ tax_amount }}
- المجموع: {{ transaction_amount }}

{% if customer_info %}
معلومات العميل:
{{ customer_info }}
{% endif %}

هذا الإشعار يتم إرساله لكل عملية تتجاوز {{ threshold_amount }} بهدف منع الاحتيال والرصد.

عرض العملية: {{ transaction_url }}
عرض الفاتورة: {{ receipt_url }}