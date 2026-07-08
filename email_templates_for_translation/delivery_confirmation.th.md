---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
สินค้าจัดส่งแล้ว - ใบสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          สินค้าจัดส่งแล้ว
        </mj-text>
        <mj-text>
          ใบสั่งซื้อของคุณ #{{ order_number }} ได้รับการจัดส่งแล้ว!
        </mj-text>
        <mj-text>
          เราหวังว่าคุณจะได้รับความพึงพอใจจากสินค้าที่ซื้อไป หากคุณมีคำถามหรือข้อกังวลใด ๆ โปรดไม่ลังเลที่จะติดต่อเรา
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          ดูใบสั่งซื้อ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
สินค้าจัดส่งแล้ว

ใบสั่งซื้อของคุณ #{{ order_number }} ได้รับการจัดส่งแล้ว!

เราหวังว่าคุณจะได้รับความพึงพอใจจากสินค้าที่ซื้อไป หากคุณมีคำถามหรือข้อกังวลใด ๆ โปรดไม่ลังเลที่จะติดต่อเรา

ดูใบสั่งซื้อ: {{ order_url }}

Thank you for your order!