---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Shift Report: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Shift Closed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Shift Summary Report
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Shift closed on {{ terminal_name }} by {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Shift Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cashier:</strong> {{ cashier_name }}<br/>
              <strong>Started:</strong> {{ shift_started }}<br/>
              <strong>Ended:</strong> {{ shift_ended }}<br/>
              <strong>Duration:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sales Summary:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Sales:</strong> {{ total_sales }}<br/>
              <strong>Transactions:</strong> {{ transaction_count }}<br/>
              <strong>Items Sold:</strong> {{ items_sold }}<br/>
              <strong>Average Sale:</strong> {{ average_sale }}<br/>
              <strong>Tax Collected:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Payment Breakdown:
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
          Cash Reconciliation:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Opening Cash:</strong> {{ opening_cash }}<br/>
              <strong>Cash Sales:</strong> {{ cash_sales }}<br/>
              <strong>Expected Cash:</strong> {{ expected_cash }}<br/>
              <strong>Counted Cash:</strong> {{ counted_cash }}<br/>
              <strong>Difference:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Cash Discrepancy: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Note: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Full Report
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 SHIFT CLOSED

Shift Summary Report

Shift closed on {{ terminal_name }} by {{ cashier_name }}.

SHIFT DETAILS:
- Terminal: {{ terminal_name }}
- Cashier: {{ cashier_name }}
- Started: {{ shift_started }}
- Ended: {{ shift_ended }}
- Duration: {{ shift_duration }}

SALES SUMMARY:
- Total Sales: {{ total_sales }}
- Transactions: {{ transaction_count }}
- Items Sold: {{ items_sold }}
- Average Sale: {{ average_sale }}
- Tax Collected: {{ tax_collected }}

PAYMENT BREAKDOWN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transactions)
{% endfor %}

CASH RECONCILIATION:
- Opening Cash: {{ opening_cash }}
- Cash Sales: {{ cash_sales }}
- Expected Cash: {{ expected_cash }}
- Counted Cash: {{ counted_cash }}
- Difference: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ CASH DISCREPANCY: {{ discrepancy_amount }}
{% if discrepancy_note %}Note: {{ discrepancy_note }}{% endif %}
{% endif %}

View full report: {{ shift_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| terminal_name | Terminal display name | Checkout 1 |
| cashier_name | Cashier's name | John Smith |
| shift_date | Shift date | February 15, 2026 |
| shift_started | Shift start time | 9:00 AM |
| shift_ended | Shift end time | 5:00 PM |
| shift_duration | Total shift time | 8 hours |
| total_sales | Total sales amount | $2,547.35 |
| transaction_count | Number of transactions | 87 |
| items_sold | Total items sold | 234 |
| average_sale | Average transaction value | $29.28 |
| tax_collected | Total tax | $203.79 |
| payment_methods | Payment breakdown array | [{method: 'Cash', amount: '$850.00', count: 23}] |
| opening_cash | Starting cash drawer | $200.00 |
| cash_sales | Cash transactions | $850.00 |
| expected_cash | Expected total | $1,050.00 |
| counted_cash | Actual counted | $1,045.00 |
| cash_difference | Difference | -$5.00 |
| cash_difference_color | CSS color for difference | #dc2626 (red for short) or #059669 (green for over) |
| discrepancy_amount | Absolute discrepancy | $5.00 short |
| discrepancy_note | Cashier's note | Customer disputed $5 change |
| shift_report_url | Full report page | https://shop.com/en/admin/pos/shifts/12345 |

## Notes

- Manager/admin notification
- Sent when cashier closes shift
- Complete shift financial summary
- Payment method breakdown
- Cash reconciliation with discrepancy tracking
- Flags cash variances for review
- Transactional email
