---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
คำสั่งซื้อของคุณ #{{ order_number }} อยู่ในสถานะ {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การอัปเดตการจัดส่ง: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ข่าวดี! คำสั่งซื้อของคุณได้ถึงจุดสำคัญในการเดินทางไปยังคุณแล้ว
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดคำสั่งซื้อ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order Number:</strong> {{ order_number }}<br/>
              <strong>Tracking Number:</strong> {{ tracking_number }}<br/>
              <strong>Carrier:</strong> {{ carrier_name }}<br/>
              <strong>Current Location:</strong> {{ current_location }}<br/>
              <strong>Estimated Delivery:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Track Your Package
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          มีคำถามเกี่ยวกับการจัดส่งของคุณ? <a href="{{ support_url }}">Contact Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
การอัปเดตการจัดส่ง: {{ milestone_status }}

สวัสดี {{ customer_name }},

ข่าวดี! คำสั่งซื้อของคุณได้ถึงจุดสำคัญในการเดินทางไปยังคุณแล้ว

📦 {{ milestone_status }}
{{ milestone_description }}

รายละเอียดคำสั่งซื้อ:
- หมายเลขคำสั่งซื้อ: {{ order_number }}
- หมายเลขติดตาม: {{ tracking_number }}
- ผู้ให้บริการ: {{ carrier_name }}
- สถานที่ปัจจุบัน: {{ current_location }}
- การจัดส่งที่คาดการณ์: {{ estimated_delivery }}

ติดตามแพคเกจของคุณ: {{ tracking_url }}

มีคำถามเกี่ยวกับการจัดส่งของคุณ? ติดต่อฝ่ายสนับสนุน: {{ support_url }}