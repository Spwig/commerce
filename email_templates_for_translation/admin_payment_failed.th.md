---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
การชำระเงินล้มเหลว - ใบสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          การชำระเงินล้มเหลว
        </mj-text>
        <mj-text>
          การพยายามชำระเงินสำหรับใบสั่งซื้อ #{{ order_number }} ล้มเหลว
        </mj-text>
        <mj-text>
          <strong>ลูกค้า:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>จำนวนเงิน:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>ข้อผิดพลาด:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          ดูในระบบผู้ดูแล
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
การชำระเงินล้มเหลว

การพยายามชำระเงินสำหรับใบสั่งซื้อ #{{ order_number }} ล้มเหลว

ลูกค้า: {{ customer_name }}
จำนวนเงิน: {{ order_total }}
ข้อผิดพลาด: {{ error_message }}

ดูในระบบผู้ดูแล: {{ admin_order_url }}