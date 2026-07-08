---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 تقرير المبيعات اليومي - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 تقرير المبيعات اليومي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص المبيعات - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>إجمالي الأرباح:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>الطلبات:</strong> {{ order_count }}<br/>
              <strong>قيمة الطلب المتوسطة:</strong> {{ avg_order_value }}<br/>
              <strong>معدل التحويل:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الزوار:</strong> {{ visitor_count }}<br/>
              <strong>العملاء الجدد:</strong> {{ new_customers }}<br/>
              <strong>العملاء العائدين:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          المنتجات الشائعة:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} مبيعات ({{ product.revenue }})
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
📊 تقرير المبيعات اليومي

ملخص المبيعات - {{ report_date }}

الأداء:
- إجمالي الأرباح: {{ total_revenue }}
- الطلبات: {{ order_count }}
- قيمة الطلب المتوسطة: {{ avg_order_value }}
- معدل التحويل: {{ conversion_rate }}%

الحركة:
- الزوار: {{ visitor_count }}
- العملاء الجدد: {{ new_customers }}
- العملاء العائدين: {{ returning_customers }}

المنتجات الشائعة:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} مبيعات ({{ product.revenue }})
{% endfor %}

عرض التقرير الكامل: {{ full_report_url }}