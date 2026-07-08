---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Hoàn tất thanh toán: {{ payout_amount }}

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
          🎉 Hoàn tất thanh toán!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Đã thanh toán thành công
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID thanh toán: {{ payout_id }}
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
          Số tiền thanh toán của bạn là {{ payout_amount }} đã được hoàn tất thành công!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Số tiền đã được gửi đến phương thức thanh toán của bạn. Tùy thuộc vào ngân hàng hoặc nhà cung cấp dịch vụ thanh toán của bạn, có thể mất 1-2 ngày làm việc để hiển thị trên tài khoản của bạn.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Cảm ơn bạn đã quảng bá {{ shop_name }}. Hãy tiếp tục làm tốt!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Xem chi tiết thanh toán
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
✓ Hoàn tất thanh toán: {{ payout_amount }}

Chào {{ affiliate_name }},

Số tiền thanh toán của bạn là {{ payout_amount }} đã được hoàn tất thành công!

Chi tiết thanh toán:
- ID thanh toán: {{ payout_id }}
- Số tiền: {{ payout_amount }}
- Phương thức thanh toán: {{ payout_method }}

Số tiền đã được gửi đến phương thức thanh toán của bạn. Tùy thuộc vào ngân hàng hoặc nhà cung cấp dịch vụ thanh toán của bạn, có thể mất 1-2 ngày làm việc để hiển thị trên tài khoản của bạn.

Cảm ơn bạn đã quảng bá {{ shop_name }}. Hãy tiếp tục làm tốt!

Xem chi tiết thanh toán: {{ portal_url }}

{{ shop_name }}
Có thắc mắc? Liên hệ {{ support_email }}