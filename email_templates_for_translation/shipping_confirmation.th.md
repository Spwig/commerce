---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
สินค้าของคุณได้ถูกจัดส่งแล้ว - หมายเลขคำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          สินค้าของคุณได้ถูกจัดส่งแล้ว!
        </mj-text>
        <mj-text>
          ข่าวดี! คำสั่งซื้อของคุณ #{{ order_number }} ได้ถูกจัดส่งแล้ว
        </mj-text>
        <mj-text>
          <strong>หมายเลขติดตาม:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>ผู้ให้บริการจัดส่ง:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          ติดตามการจัดส่ง
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
สินค้าของคุณได้ถูกจัดส่งแล้ว!

ข่าวดี! คำสั่งซื้อของคุณ #{{ order_number }} ได้ถูกจัดส่งแล้ว

หมายเลขติดตาม: {{ tracking_number }}
ผู้ให้บริการจัดส่ง: {{ carrier }}

ติดตามการจัดส่ง: {{ tracking_url }}