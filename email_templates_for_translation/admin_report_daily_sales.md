---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Daily Sales Report - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Daily Sales Report
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sales Summary - {{ report_date }}
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
📊 DAILY SALES REPORT

Sales Summary - {{ report_date }}

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

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| report_date | Report date | February 15, 2026 |
| total_revenue | Total daily revenue | $12,547.35 |
| order_count | Number of orders | 87 |
| avg_order_value | Average order value | $144.23 |
| conversion_rate | Conversion percentage | 3.2 |
| visitor_count | Total visitors | 2,718 |
| new_customers | New customer count | 23 |
| returning_customers | Returning customer count | 64 |
| top_products | Top sellers array | [{rank: 1, name: 'iPhone Case', sales: 23, revenue: '$459.00'}] |
| full_report_url | Full report page | https://shop.com/en/admin/reports/sales/2026-02-15 |

## Notes

- Admin/merchant report
- Sent daily at end of business day
- Key business metrics summary
- Top products analysis
- Can be opted out via communication preferences
