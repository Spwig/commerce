---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
Tiền hoa hồng đã được phê duyệt: {{ commission_amount }}

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
          ✓ Tiền hoa hồng đã được phê duyệt!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Đã được phê duyệt để thanh toán
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
          Tiền hoa hồng {{ commission_amount }} từ đơn hàng #{{ order_number }} của bạn đã được phê duyệt và sẽ được bao gồm trong khoản thanh toán tiếp theo của bạn.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Các khoản thanh toán được xử lý theo lịch trình thanh toán của bạn. Bạn sẽ nhận được email khác khi khoản thanh toán được xử lý.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Xem Tiền Hoa Hồng
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
Tiền hoa hồng đã được phê duyệt: {{ commission_amount }}

Chào {{ affiliate_name }},

Tiền hoa hồng {{ commission_amount }} từ đơn hàng #{{ order_number }} của bạn đã được phê duyệt và sẽ được bao gồm trong khoản thanh toán tiếp theo của bạn.

Các khoản thanh toán được xử lý theo lịch trình thanh toán của bạn. Bạn sẽ nhận được email khác khi khoản thanh toán được xử lý.

Xem tiền hoa hồng: {{ portal_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}