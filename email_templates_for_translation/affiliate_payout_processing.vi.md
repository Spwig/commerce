---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Tiền chi trả {{ payout_amount }} của bạn đang được xử lý

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          💸 Xử lý chi trả
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Đang xử lý chi trả của bạn
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Mã chi trả: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Chào {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Tin vui! Số tiền chi trả {{ payout_amount }} của bạn hiện đang được xử lý.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Số tiền sẽ đến tài khoản của bạn trong vòng 3-5 ngày làm việc. Bạn sẽ nhận được email khác khi chi trả hoàn tất.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Mã chi trả:</strong> {{ payout_id }}<br/>
          <strong>Số tiền:</strong> {{ payout_amount }}<br/>
          <strong>Phương thức thanh toán:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Xem lịch sử chi trả
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Có thắc mắc? <a href="mailto:{{ support_email }}" style="color: #007bff;">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tiền chi trả {{ payout_amount }} của bạn đang được xử lý

Chào {{ affiliate_name }},

Tin vui! Số tiền chi trả {{ payout_amount }} của bạn hiện đang được xử lý.

Chi tiết chi trả:
- Mã chi trả: {{ payout_id }}
- Số tiền: {{ payout_amount }}
- Phương thức thanh toán: {{ payout_method }}

Số tiền sẽ đến tài khoản của bạn trong vòng 3-5 ngày làm việc. Bạn sẽ nhận được email khác khi chi trả hoàn tất.

Xem lịch sử chi trả: {{ portal_url }}

{{ shop_name }}
Có thắc mắc? Liên hệ {{ support_email }}