---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 工作班次報告：{{ terminal_name }} - {{ shift_date }}

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
📊 班次已結束

班次摘要報告

班次在 {{ terminal_name }} 上由 {{ cashier_name }} 結束。

班次詳情：
- 終端機：{{ terminal_name }}
- 收銀員：{{ cashier_name }}
- 開始時間：{{ shift_started }}
- 結束時間：{{ shift_ended }}
- 持續時間：{{ shift_duration }}

銷售摘要：
- 總銷售額：{{ total_sales }}
- 交易數量：{{ transaction_count }}
- 賣出商品數量：{{ items_sold }}
- 平均銷售額：{{ average_sale }}
- 收取稅款：{{ tax_collected }}

付款方式明細：
{% for payment in payment_methods %}
{{ payment.method }}：{{ payment.amount }} （{{ payment.count }} 交易）
{% endfor %}

現金對賬：
- 開始現金：{{ opening_cash }}
- 現金銷售：{{ cash_sales }}
- 預期現金：{{ expected_cash }}
- 實點現金：{{ counted_cash }}
- 差異：{{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ 現金差額：{{ discrepancy_amount }}
{% if discrepancy_note %}備註：{{ discrepancy_note }}{% endif %}
{% endif %}

查看完整報告：{{ shift_report_url }}