---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
อัปเดตการสั่งซื้อของคุณ #{{ order_number }} - การจัดส่งล่าช้า

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          อัปเดตการสั่งซื้อของคุณ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณ {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เราอยากแจ้งให้คุณทราบเกี่ยวกับการล่าช้าของคำสั่งซื้อของคุณ ขออภัยในความไม่สะดวกและขอบคุณที่คุณอดทน
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการสั่งซื้อ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>หมายเลขการสั่งซื้อ:</strong> {{ order_number }}<br/>
              <strong>ETA ต้นฉบับ:</strong> {{ original_delivery_date }}<br/>
              <strong>ETA ใหม่:</strong> {{ new_delivery_date }}<br/>
              <strong>หมายเลขติดตาม:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เหตุผลของการล่าช้า:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ติดตามการสั่งซื้อของคุณ
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          เราทำงานอย่างหนักเพื่อให้ได้รับคำสั่งซื้อของคุณเร็วที่สุดเท่าที่จะทำได้ คุณจะได้รับการอัปเดตอีกครั้งเมื่อพัสดุของคุณเริ่มเดินทาง
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          มีคำถาม? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ติดต่อทีมบริการลูกค้าของเรา</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
อัปเดตการสั่งซื้อของคุณ #{{ order_number }}

คุณ {{ customer_name }},

เราอยากแจ้งให้คุณทราบเกี่ยวกับการล่าช้าของคำสั่งซื้อของคุณ ขออภัยในความไม่สะดวกและขอบคุณที่คุณอดทน

รายละเอียดการสั่งซื้อ:
- หมายเลขการสั่งซื้อ: {{ order_number }}
- ETA ต้นฉบับ: {{ original_delivery_date }}
- ETA ใหม่: {{ new_delivery_date }}
- หมายเลขติดตาม: {{ tracking_number }}

เหตุผลของการล่าช้า:
{{ delay_reason }}

ติดตามการสั่งซื้อของคุณ: {{ tracking_url }}

เราทำงานอย่างหนักเพื่อให้ได้รับคำสั่งซื้อของคุณเร็วที่สุดเท่าที่จะทำได้ คุณจะได้รับการอัปเดตอีกครั้งเมื่อพัสดุของคุณเริ่มเดินทาง

มีคำถาม? ติดต่อทีมบริการลูกค้าของเรา: {{ support_url }}

---
อัปเดตนี้เป็นสำหรับการสั่งซื้อ #{{ order_number }} ที่ {{ shop_name }}.