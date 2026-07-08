---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Thanh toán thất bại - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Thanh toán thất bại
        </mj-text>
        <mj-text>
          Một lần thanh toán đã thất bại cho đơn hàng #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Khách hàng:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Số tiền:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Lỗi:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Xem trong phần quản trị
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Thanh toán thất bại

Một lần thanh toán đã thất bại cho đơn hàng #{{ order_number }}.

Khách hàng: {{ customer_name }}
Số tiền: {{ order_total }}
Lỗi: {{ error_message }}

Xem trong phần quản trị: {{ admin_order_url }}