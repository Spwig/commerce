---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Hành động cần thiết: Giao tiền thất bại

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ Giao tiền thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          Mã giao tiền: {{ payout_id }}
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
          Chúng tôi gặp phải một vấn đề khi xử lý khoản giao tiền {{ payout_amount }} của bạn.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Điều này thường do thông tin thanh toán không chính xác hoặc vấn đề từ nhà cung cấp thanh toán của bạn.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Vui lòng cập nhật thông tin thanh toán của bạn trong bảng điều khiển đại lý và liên hệ với nhóm hỗ trợ của chúng tôi để giải quyết vấn đề này.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Cập nhật thông tin thanh toán
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Cần giúp đỡ? <a href="mailto:{{ support_email }}" style="color: #007bff;">Liên hệ Hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hành động cần thiết: Giao tiền thất bại

Chào {{ affiliate_name }},

Chúng tôi gặp phải một vấn đề khi xử lý khoản giao tiền {{ payout_amount }} (Mã giao tiền: {{ payout_id }}).

Điều này thường do thông tin thanh toán không chính xác hoặc vấn đề từ nhà cung cấp thanh toán của bạn.

Vui lòng cập nhật thông tin thanh toán của bạn trong bảng điều khiển đại lý và liên hệ với nhóm hỗ trợ của chúng tôi để giải quyết vấn đề này.

Cập nhật thông tin thanh toán: {{ portal_url }}

{{ shop_name }}
Cần giúp đỡ? Liên hệ {{ support_email }}