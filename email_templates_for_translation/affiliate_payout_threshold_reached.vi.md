---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Bạn đã đạt đến ngưỡng thanh toán tối thiểu!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Ngưỡng thanh toán đã đạt!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tin Tức Tuyệt Vời!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúc mừng! Số dư đại lý của bạn đã đạt đến ngưỡng thanh toán tối thiểu. Bạn có thể yêu cầu thanh toán bây giờ.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Số dư của bạn:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số dư có thể sử dụng:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Ngưỡng thanh toán tối thiểu:</strong> {{ minimum_payout }}<br/>
              <strong>Số dư đang chờ:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bước tiếp theo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Yêu cầu thanh toán từ bảng điều khiển đại lý của bạn<br/>
          • Các khoản thanh toán được xử lý {{ payout_schedule }}<br/>
          • Số tiền sẽ được gửi qua {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Yêu cầu thanh toán
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem bảng điều khiển
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 NGƯỠNG THANH TOÁN ĐÃ ĐẠT!

Tin Tức Tuyệt Vời!

Hi {{ affiliate_name }},

Chúc mừng! Số dư đại lý của bạn đã đạt đến ngưỡng thanh toán tối thiểu. Bạn có thể yêu cầu thanh toán bây giờ.

SỐ DƯ CỦA BẠN:
- Số dư có thể sử dụng: {{ available_balance }}
- Ngưỡng thanh toán tối thiểu: {{ minimum_payout }}
- Số dư đang chờ: {{ pending_balance }}

BƯỚC TIẾP THEO:
• Yêu cầu thanh toán từ bảng điều khiển đại lý của bạn
• Các khoản thanh toán được xử lý {{ payout_schedule }}
• Số tiền sẽ được gửi qua {{ payment_method }}

Yêu cầu thanh toán: {{ request_payout_url }}
Xem bảng điều khiển: {{ portal_url }}