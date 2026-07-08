---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 تقرير Z اليومي - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 تقرير Z اليومي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تقرير إغلاق اليوم
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          ملخص يومي لـ {{ location_name }} في {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص المبيعات:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>إجمالي المبيعات:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>المعاملات:</strong> {{ transaction_count }}<br/>
              <strong>العناصر المباعة:</strong> {{ items_sold }}<br/>
              <strong>المبيعات المتوسطة:</strong> {{ average_sale }}<br/>
              <strong>الضرائب المجمعة:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          طرق الدفع:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }} ({{ payment.count }} معاملات)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص التحويلات:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>إجمالي التحويلات:</strong> {{ shift_count }}<br/>
              <strong>أجهزة الطرفية المستخدمة:</strong> {{ terminal_count }}<br/>
              <strong>المحصلين النشطين:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              المبيعات: {{ terminal.sales }} | المعاملات: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التعديلات والخصومات:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الخصومات الممنوحة:</strong> {{ discounts_total }}<br/>
              <strong>الاستبدالات المقدمة:</strong> {{ refunds_total }}<br/>
              <strong>الملغاة:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ إجمالي تباين النقد: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          المنتجات الأكثر مبيعًا:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} تم بيعها ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض التقرير الكامل
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 تقرير Z اليومي

تقرير إغلاق اليوم

ملخص يومي لـ {{ location_name }} في {{ report_date }}.

ملخص المبيعات:
- إجمالي المبيعات: {{ total_sales }}
- المعاملات: {{ transaction_count }}
- العناصر المباعة: {{ items_sold }}
- المبيعات المتوسطة: {{ average_sale }}
- الضرائب المجمعة: {{ tax_collected }}

طرق الدفع:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} معاملات)
{% endfor %}

ملخص التحويلات:
- إجمالي التحويلات: {{ shift_count }}
- أجهزة الطرفية المستخدمة: {{ terminal_count }}
- المحصلين النشطين: {{ cashier_count }}

تحليل أجهزة الطرفية:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} معاملات
{% endfor %}

التعديلات والخصومات:
- الخصومات الممنوحة: {{ discounts_total }}
- الاستبدالات المقدمة: {{ refunds_total }}
- الملغاة: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ إجمالي تباين النقد: {{ cash_variance }}
{{ variance_note }}
{% endif %}

المنتجات الأكثر مبيعًا:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} تم بيعها ({{ product.revenue }})
{% endfor %}

عرض التقرير الكامل: {{ full_report_url }}