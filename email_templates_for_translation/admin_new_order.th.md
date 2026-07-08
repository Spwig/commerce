---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
ได้รับคำสั่งซื้อใหม่ - หมายเลขคำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          ได้รับคำสั่งซื้อใหม่
        </mj-text>
        <mj-text>
          มีคำสั่งซื้อใหม่ที่ถูกวางไว้บนร้านของคุณ
        </mj-text>
        <mj-text>
          <strong>หมายเลขคำสั่งซื้อ:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>ลูกค้า:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>รวมทั้งหมด:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          ดูในแดชบอร์ดผู้ดูแลระบบ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ได้รับคำสั่งซื้อใหม่

มีคำสั่งซื้อใหม่ที่ถูกวางไว้บนร้านของคุณ

หมายเลขคำสั่งซื้อ: {{ order_number }}
ลูกค้า: {{ customer_name }}
รวมทั้งหมด: {{ order_total }}

ดูในแดชบอร์ดผู้ดูแลระบบ: {{ admin_order_url }}
