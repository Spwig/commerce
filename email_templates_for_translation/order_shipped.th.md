---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
คำสั่งซื้อของคุณ #{{ order_number }} ได้ถูกจัดส่งแล้ว!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 คำสั่งซื้อได้ถูกจัดส่งแล้ว!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          กำลังเดินทางมายังคุณ!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ข่าวดี! คำสั่งซื้อของคุณได้ถูกจัดส่งแล้ว และกำลังเดินทางมายังคุณ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการจัดส่ง:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order #:</strong> {{ order_number }}<br/>
              <strong>Tracking #:</strong> {{ tracking_number }}<br/>
              <strong>Carrier:</strong> {{ carrier_name }}<br/>
              <strong>Est. Delivery:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ติดตามพัสดุของคุณ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 คำสั่งซื้อได้ถูกจัดส่งแล้ว!

กำลังเดินทางมายังคุณ!

Hi {{ customer_name }},

ข่าวดี! คำสั่งซื้อของคุณได้ถูกจัดส่งแล้ว และกำลังเดินทางมายังคุณ

รายละเอียดการจัดส่ง:
- Order #: {{ order_number }}
- Tracking #: {{ tracking_number }}
- Carrier: {{ carrier_name }}
- Est. Delivery: {{ estimated_delivery }}

Track your package: {{ tracking_url }}