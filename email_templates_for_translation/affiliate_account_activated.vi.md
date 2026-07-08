---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Chào lại! Tài khoản đã kích hoạt lại

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
          🎉 Tài khoản đã kích hoạt lại!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Chào lại!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Tài khoản đại lý của bạn đã được kích hoạt lại
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
          Tin tốt! Tài khoản đại lý của bạn với {{ shop_name }} đã được kích hoạt lại.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bạn có thể tiếp tục quảng bá sản phẩm của chúng tôi và nhận hoa hồng ngay lập tức.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Truy cập Bảng điều khiển Đại lý
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Có câu hỏi? <a href="mailto:{{ support_email }}" style="color: #007bff;">Liên hệ Hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Chào lại! Tài khoản đã kích hoạt lại

Chào {{ affiliate_name }},

Tin tốt! Tài khoản đại lý của bạn với {{ shop_name }} đã được kích hoạt lại.

Bạn có thể tiếp tục quảng bá sản phẩm của chúng tôi và nhận hoa hồng ngay lập tức.

Truy cập bảng điều khiển của bạn: {{ portal_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}