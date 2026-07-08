---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Báo cáo Ca làm việc: {{ terminal_name }} - {{ shift_date }}

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
📊 CA LÀM VIỆC ĐÃ KẾT THÚC

Báo cáo Tổng quan Ca làm việc

Ca làm việc đã kết thúc trên {{ terminal_name }} bởi {{ cashier_name }}.

CHI TIẾT CA LÀM VIỆC:
- Thiết bị: {{ terminal_name }}
- Nhân viên thu ngân: {{ cashier_name }}
- Bắt đầu: {{ shift_started }}
- Kết thúc: {{ shift_ended }}
- Thời gian: {{ shift_duration }}

TỔNG HÓA ĐƠN BÁN HÀNG:
- Tổng doanh thu: {{ total_sales }}
- Số giao dịch: {{ transaction_count }}
- Số mặt hàng bán được: {{ items_sold }}
- Trung bình mỗi giao dịch: {{ average_sale }}
- Thuế thu được: {{ tax_collected }}

THỐNG KÊ PHƯƠNG THỨC THANH TOÁN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} giao dịch)
{% endfor %}

ĐỐI CHIỀU TIỀN MẶT:
- Tiền mặt ban đầu: {{ opening_cash }}
- Doanh thu tiền mặt: {{ cash_sales }}
- Số tiền mặt dự kiến: {{ expected_cash }}
- Số tiền mặt đã đếm: {{ counted_cash }}
- Chênh lệch: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ CHÊNH LỆCH TIỀN MẶT: {{ discrepancy_amount }}
{% if discrepancy_note %}Ghi chú: {{ discrepancy_note }}{% endif %}
{% endif %}

Xem báo cáo đầy đủ: {{ shift_report_url }}