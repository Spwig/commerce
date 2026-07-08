---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Quan trọng: Tài khoản bị tạm dừng

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
          Tài khoản bị tạm dừng
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
          Tài khoản đại lý của bạn với {{ shop_name }} đã bị tạm dừng.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Điều này thường là do vi phạm điều khoản và điều kiện chương trình đại lý của chúng tôi.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Nếu bạn cho rằng đây là một lỗi hoặc muốn thảo luận về quyết định này, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Có câu hỏi? <a href="mailto:{{ support_email }}" style="color: #007bff;">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Quan trọng: Tài khoản bị tạm dừng

Chào {{ affiliate_name }},

Tài khoản đại lý của bạn với {{ shop_name }} đã bị tạm dừng.

Điều này thường là do vi phạm điều khoản và điều kiện chương trình đại lý của chúng tôi.

Nếu bạn cho rằng đây là một lỗi hoặc muốn thảo luận về quyết định này, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}