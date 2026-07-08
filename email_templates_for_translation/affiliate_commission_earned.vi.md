---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Bạn đã kiếm được {{ commission_amount }} hoa hồng!

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
          💰 Hoa Hồng Đã Kiếm!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Tin Tốt Từ {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Hoa Hồng Của Bạn
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Từ Đơn Hàng #{{ order_number }}
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
          Chúc mừng! Bạn đã kiếm được {{ commission_amount }} hoa hồng từ đơn hàng #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Hãy tiếp tục quảng bá {{ shop_name }} để kiếm thêm nhiều hoa hồng hơn. Càng nhiều doanh số bạn tạo ra, bạn càng kiếm được nhiều hơn!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Số Đơn Hàng:</strong> #{{ order_number }}<br/>
          <strong>Số Tiền Hoa Hồng:</strong> {{ commission_amount }}<br/>
          <strong>Tỷ Lệ Hoa Hồng:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Xem Bảng Điều Khiển Liên Kết
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Có câu hỏi? <a href="mailto:{{ support_email }}" style="color: #007bff;">Liên Hệ Hỗ Trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bạn đã kiếm được {{ commission_amount }} hoa hồng!

Chào {{ affiliate_name }},

Chúc mừng! Bạn đã kiếm được {{ commission_amount }} hoa hồng từ đơn hàng #{{ order_number }}.

Chi Tiết Hoa Hồng:
- Số Đơn Hàng: #{{ order_number }}
- Số Tiền Hoa Hồng: {{ commission_amount }}
- Tỷ Lệ Hoa Hồng: {{ commission_rate }}%

Hãy tiếp tục quảng bá {{ shop_name }} để kiếm thêm nhiều hoa hồng hơn.

Xem bảng điều khiển của bạn: {{ portal_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}