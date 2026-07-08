---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Cập nhật trạng thái hoa hồng - Đơn hàng #{{ order_number }}

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
          Cập nhật trạng thái hoa hồng
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
          Chúng tôi muốn thông báo với bạn rằng hoa hồng cho đơn hàng #{{ order_number }} ({{ commission_amount }}) không được duyệt.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Điều này thường xảy ra khi đơn hàng bị hủy hoặc hoàn tiền trước khi thời gian hoa hồng kết thúc.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Nếu bạn có bất kỳ câu hỏi nào về hoa hồng này, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Xem Bảng Điều Khiển Đại Lý
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
Cập nhật trạng thái hoa hồng - Đơn hàng #{{ order_number }}

Chào {{ affiliate_name }},

Chúng tôi muốn thông báo với bạn rằng hoa hồng cho đơn hàng #{{ order_number }} ({{ commission_amount }}) không được duyệt.

Điều này thường xảy ra khi đơn hàng bị hủy hoặc hoàn tiền trước khi thời gian hoa hồng kết thúc.

Nếu bạn có bất kỳ câu hỏi nào về hoa hồng này, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.

Xem bảng điều khiển của bạn: {{ portal_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}

