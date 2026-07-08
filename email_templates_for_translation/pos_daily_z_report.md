---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Daily Z Report - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Daily Z Report
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          End of Day Settlement Report
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Daily summary for {{ location_name }} on {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sales Summary:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Sales:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>Transactions:</strong> {{ transaction_count }}<br/>
              <strong>Items Sold:</strong> {{ items_sold }}<br/>
              <strong>Average Sale:</strong> {{ average_sale }}<br/>
              <strong>Tax Collected:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Payment Methods:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} transactions)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Shifts Summary:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Shifts:</strong> {{ shift_count }}<br/>
              <strong>Terminals Used:</strong> {{ terminal_count }}<br/>
              <strong>Active Cashiers:</strong> {{ cashier_count }}
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
              Sales: {{ terminal.sales }} | Transactions: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Adjustments & Discounts:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Discounts Given:</strong> {{ discounts_total }}<br/>
              <strong>Refunds Issued:</strong> {{ refunds_total }}<br/>
              <strong>Voids:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Total Cash Variance: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Top Selling Products:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} sold ({{ product.revenue }})
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
📊 DAILY Z REPORT

End of Day Settlement Report

Daily summary for {{ location_name }} on {{ report_date }}.

SALES SUMMARY:
- Total Sales: {{ total_sales }}
- Transactions: {{ transaction_count }}
- Items Sold: {{ items_sold }}
- Average Sale: {{ average_sale }}
- Tax Collected: {{ tax_collected }}

PAYMENT METHODS:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transactions)
{% endfor %}

SHIFTS SUMMARY:
- Total Shifts: {{ shift_count }}
- Terminals Used: {{ terminal_count }}
- Active Cashiers: {{ cashier_count }}

TERMINAL BREAKDOWN:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} transactions
{% endfor %}

ADJUSTMENTS & DISCOUNTS:
- Discounts Given: {{ discounts_total }}
- Refunds Issued: {{ refunds_total }}
- Voids: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ TOTAL CASH VARIANCE: {{ cash_variance }}
{{ variance_note }}
{% endif %}

TOP SELLING PRODUCTS:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} sold ({{ product.revenue }})
{% endfor %}

View full report: {{ full_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| report_date | Report date | February 15, 2026 |
| location_name | Store/location name | Main Store |
| total_sales | Total daily sales | $12,547.35 |
| transaction_count | Total transactions | 287 |
| items_sold | Total items | 756 |
| average_sale | Average transaction | $43.70 |
| tax_collected | Total tax | $1,003.79 |
| payment_methods | Payment breakdown | [{method: 'Cash', amount: '$3,250.00', count: 87}] |
| shift_count | Number of shifts | 3 |
| terminal_count | Terminals used | 2 |
| cashier_count | Active cashiers | 5 |
| terminal_stats | Per-terminal stats | [{name: 'Checkout 1', sales: '$7,200', transactions: 165}] |
| discounts_total | Total discounts | $247.50 |
| refunds_total | Total refunds | $125.00 |
| voids_total | Total voids | $89.99 |
| cash_variance | Cash discrepancy | $15.00 short |
| variance_note | Variance explanation | Minor variances across 3 shifts |
| top_products | Top sellers | [{rank: 1, name: 'iPhone Case', quantity: 23, revenue: '$459.00'}] |
| full_report_url | Full report page | https://shop.com/en/admin/pos/reports/z/2026-02-15 |

## Notes

- Manager/admin report
- Sent daily at end of business day
- Complete financial summary
- Per-terminal breakdown
- Top products analysis
- Flags cash variances
- Can be scheduled (e.g., 11 PM daily)
