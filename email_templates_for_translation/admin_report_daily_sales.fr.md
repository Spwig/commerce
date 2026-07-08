---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Rapport de Ventes Journalier - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Rapport de Ventes Journalier
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé des Ventes - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Revenue:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Orders:</strong> {{ order_count }}<br/>
              <strong>Average Order Value:</strong> {{ avg_order_value }}<br/>
              <strong>Conversion Rate:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Visitors:</strong> {{ visitor_count }}<br/>
              <strong>New Customers:</strong> {{ new_customers }}<br/>
              <strong>Returning Customers:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Top Products:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} sales ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Full Report
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RAPPORT DE VENTES JOURNALIER

Résumé des Ventes - {{ report_date }}

PERFORMANCE:
- Total Revenue: {{ total_revenue }}
- Orders: {{ order_count }}
- Average Order Value: {{ avg_order_value }}
- Conversion Rate: {{ conversion_rate }}%

TRAFFIC:
- Visitors: {{ visitor_count }}
- New Customers: {{ new_customers }}
- Returning Customers: {{ returning_customers }}

TOP PRODUCTS:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} sales ({{ product.revenue }})
{% endfor %}

View full report: {{ full_report_url }}