---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Đơn hàng mới đã nhận - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Đơn hàng mới đã nhận
        </mj-text>
        <mj-text>
          Một đơn hàng mới đã được đặt trên cửa hàng của bạn.
        </mj-text>
        <mj-text>
          <strong>Số đơn hàng:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Khách hàng:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Tổng cộng:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Xem trong phần quản trị
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Đơn hàng mới đã nhận

Một đơn hàng mới đã được đặt trên cửa hàng của bạn.

Số đơn hàng: {{ order_number }}
Khách hàng: {{ customer_name }}
Tổng cộng: {{ order_total }}

Xem trong phần quản trị: {{ admin_order_url }}

