---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Cảnh báo chênh lệch tiền mặt: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Chênh lệch tiền mặt được phát hiện
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cảnh báo biến động tiền mặt
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Một chênh lệch tiền mặt là {{ discrepancy_amount }} đã được phát hiện khi đóng ca tại {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết chênh lệch:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Máy POS:</strong> {{ terminal_name }}<br/>
              <strong>Người thu ngân:</strong> {{ cashier_name }}<br/>
              <strong>Ngày ca:</strong> {{ shift_date }}<br/>
              <strong>Thời gian ca:</strong> {{ shift_duration }}<br/>
              <strong>Phát hiện lúc:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Số tiền mặt:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Tiền mặt dự kiến:</strong> {{ expected_cash }}<br/>
              <strong>Tiền mặt đã đếm:</strong> {{ counted_cash }}<br/>
              <strong>Chênh lệch:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tiền mặt ban đầu:</strong> {{ opening_cash }}<br/>
              <strong>Bán hàng tiền mặt:</strong> {{ cash_sales }}<br/>
              <strong>Hoàn tiền tiền mặt:</strong> {{ cash_refunds }}<br/>
              <strong>Tiền mặt đã chi:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ghi chú của người thu ngân:
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
          Các hành động được đề xuất:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Kiểm tra lịch sử giao dịch để phát hiện lỗi<br/>
          2. Kiểm tra các khoản thanh toán tiền mặt chưa được ghi nhận<br/>
          3. Xác minh việc đếm tiền mặt là chính xác<br/>
          4. Ghi chú chênh lệch trong ghi chú ca<br/>
          5. Liên hệ với người thu ngân nếu cần thiết
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem báo cáo ca
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Kiểm tra giao dịch
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ CHÊNH LỆCH TIỀN MẶT ĐƯỢC PHÁT HIỆN

Cảnh báo biến động tiền mặt

Một chênh lệch tiền mặt là {{ discrepancy_amount }} đã được phát hiện khi đóng ca tại {{ terminal_name }}.

CHI TIẾT CHÊNH LỆCH:
- Máy POS: {{ terminal_name }}
- Người thu ngân: {{ cashier_name }}
- Ngày ca: {{ shift_date }}
- Thời gian ca: {{ shift_duration }}
- Phát hiện lúc: {{ detected_at }}

SỐ TIỀN MẶT:
- Tiền mặt dự kiến: {{ expected_cash }}
- Tiền mặt đã đếm: {{ counted_cash }}
- Chênh lệch: {{ discrepancy_amount }}

BREAKDOWN:
- Tiền mặt ban đầu: {{ opening_cash }}
- Bán hàng tiền mặt: {{ cash_sales }}
- Hoàn tiền tiền mặt: {{ cash_refunds }}
- Tiền mặt đã chi: {{ cash_paid_out }}

{% if cashier_note %}
CHÊNH LỆCH CỦA NGƯỜI THU NGÂN:
"{{ cashier_note }}"
{% endif %}

CÁC HÀNH ĐỘNG ĐƯỢC ĐỀ XUẤT:
1. Kiểm tra lịch sử giao dịch để phát hiện lỗi
2. Kiểm tra các khoản thanh toán tiền mặt chưa được ghi nhận
3. Xác minh việc đếm tiền mặt là chính xác
4. Ghi chú chênh lệch trong ghi chú ca
5. Liên hệ với người thu ngân nếu cần thiết

Xem báo cáo ca: {{ shift_report_url }}
Kiểm tra giao dịch: {{ transaction_history_url }}