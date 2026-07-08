---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Cập nhật ứng tuyển đại lý

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
          Cập nhật ứng tuyển
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
          Cảm ơn bạn đã quan tâm đến chương trình đại lý của {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Sau khi xem xét đơn ứng tuyển của bạn, chúng tôi quyết định không tiếp tục tại thời điểm này.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Quyết định này dựa trên các yêu cầu hiện tại của chương trình đại lý và có thể không phản ánh năng lực hoặc tiềm năng của bạn.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bạn luôn có thể nộp đơn lại trong tương lai nếu điều kiện của bạn thay đổi.
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
Cập nhật ứng tuyển đại lý

Chào {{ affiliate_name }},

Cảm ơn bạn đã quan tâm đến chương trình đại lý của {{ shop_name }}.

Sau khi xem xét đơn ứng tuyển của bạn, chúng tôi quyết định không tiếp tục tại thời điểm này.

Quyết định này dựa trên các yêu cầu hiện tại của chương trình đại lý và có thể không phản ánh năng lực hoặc tiềm năng của bạn.

Bạn luôn có thể nộp đơn lại trong tương lai nếu điều kiện của bạn thay đổi.

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}