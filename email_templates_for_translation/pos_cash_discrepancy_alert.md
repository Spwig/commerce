---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Cash Discrepancy Alert: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Cash Discrepancy Detected
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cash Variance Alert
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A cash discrepancy of {{ discrepancy_amount }} was detected when closing shift on {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Discrepancy Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cashier:</strong> {{ cashier_name }}<br/>
              <strong>Shift Date:</strong> {{ shift_date }}<br/>
              <strong>Shift Duration:</strong> {{ shift_duration }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cash Count:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Expected Cash:</strong> {{ expected_cash }}<br/>
              <strong>Counted Cash:</strong> {{ counted_cash }}<br/>
              <strong>Discrepancy:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Opening Cash:</strong> {{ opening_cash }}<br/>
              <strong>Cash Sales:</strong> {{ cash_sales }}<br/>
              <strong>Cash Refunds:</strong> {{ cash_refunds }}<br/>
              <strong>Cash Paid Out:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cashier's Note:
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
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Review transaction history for errors<br/>
          2. Check for unrecorded cash payments<br/>
          3. Verify cash count was accurate<br/>
          4. Document discrepancy in shift notes<br/>
          5. Follow up with cashier if needed
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Shift Report
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Review Transactions
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ CASH DISCREPANCY DETECTED

Cash Variance Alert

A cash discrepancy of {{ discrepancy_amount }} was detected when closing shift on {{ terminal_name }}.

DISCREPANCY DETAILS:
- Terminal: {{ terminal_name }}
- Cashier: {{ cashier_name }}
- Shift Date: {{ shift_date }}
- Shift Duration: {{ shift_duration }}
- Detected: {{ detected_at }}

CASH COUNT:
- Expected Cash: {{ expected_cash }}
- Counted Cash: {{ counted_cash }}
- Discrepancy: {{ discrepancy_amount }}

BREAKDOWN:
- Opening Cash: {{ opening_cash }}
- Cash Sales: {{ cash_sales }}
- Cash Refunds: {{ cash_refunds }}
- Cash Paid Out: {{ cash_paid_out }}

{% if cashier_note %}
CASHIER'S NOTE:
"{{ cashier_note }}"
{% endif %}

RECOMMENDED ACTIONS:
1. Review transaction history for errors
2. Check for unrecorded cash payments
3. Verify cash count was accurate
4. Document discrepancy in shift notes
5. Follow up with cashier if needed

View shift report: {{ shift_report_url }}
Review transactions: {{ transaction_history_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| terminal_name | Terminal display name | Checkout 1 |
| cashier_name | Cashier's name | John Smith |
| shift_date | Shift date | February 15, 2026 |
| shift_duration | Total shift time | 8 hours |
| detected_at | When detected | February 15, 2026 at 5:15 PM |
| expected_cash | Expected cash total | $1,050.00 |
| counted_cash | Actual counted cash | $1,045.00 |
| discrepancy_amount | Discrepancy amount | $5.00 short |
| opening_cash | Starting cash drawer | $200.00 |
| cash_sales | Cash transactions | $850.00 |
| cash_refunds | Cash refunds given | $0.00 |
| cash_paid_out | Paid outs during shift | $0.00 |
| cashier_note | Optional cashier note | Customer disputed $5 change |
| shift_report_url | Full shift report | https://shop.com/en/admin/pos/shifts/12345 |
| transaction_history_url | Transaction list | https://shop.com/en/admin/pos/transactions?shift=12345 |

## Notes

- IMPORTANT manager/admin notification
- Sent when cash discrepancy exceeds threshold (e.g., $5)
- Immediate alert for potential loss prevention
- Includes cashier notes if provided
- Links to shift report and transactions for review
- Transactional email
