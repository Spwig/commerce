---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Hoàn tiền hoa hồng - Đơn hàng #{{ order_number }}

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
          Hoàn tiền hoa hồng
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
          Hoa hồng cho đơn hàng #{{ order_number }} ({{ commission_amount }}) đã bị hoàn tiền do khách hàng hoàn tiền.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Khi khách hàng yêu cầu hoàn tiền, bất kỳ hoa hồng nào liên quan đều được hoàn tự động để đảm bảo kế toán chính xác.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Đây là một phần bình thường của quy trình liên kết. Tiếp tục quảng bá {{ shop_name }} để kiếm hoa hồng mới!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Xem Bảng điều khiển Liên kết
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
Hoàn tiền hoa hồng - Đơn hàng #{{ order_number }}

Chào {{ affiliate_name }},

Hoa hồng cho đơn hàng #{{ order_number }} ({{ commission_amount }}) đã bị hoàn tiền do khách hàng hoàn tiền.

Khi khách hàng yêu cầu hoàn tiền, bất kỳ hoa hồng nào liên quan đều được hoàn tự động để đảm bảo kế toán chính xác.

Đây là một phần bình thường của quy trình liên kết. Tiếp tục quảng bá {{ shop_name }} để kiếm hoa hồng mới!

Xem bảng điều khiển của bạn: {{ portal_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}