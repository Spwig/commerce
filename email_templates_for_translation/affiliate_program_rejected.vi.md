---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Cập nhật ứng dụng chương trình

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
          Cập nhật ứng dụng
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
          Cảm ơn bạn đã ứng tuyển để quảng bá {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Sau khi xem xét hồ sơ của bạn, chúng tôi quyết định không chấp thuận vào lúc này.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bạn vẫn có thể quảng bá các chương trình khác trong mạng lưới đối tác của chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Xem các chương trình khác
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
Cập nhật ứng dụng chương trình

Chào {{ affiliate_name }},

Cảm ơn bạn đã ứng tuyển để quảng bá {{ program_name }}.

Sau khi xem xét hồ sơ của bạn, chúng tôi quyết định không chấp thuận vào lúc này.

Bạn vẫn có thể quảng bá các chương trình khác trong mạng lưới đối tác của chúng tôi.

Xem các chương trình khác: {{ portal_url }}

{{ shop_name }}
Có thắc mắc? Liên hệ {{ support_email }}

