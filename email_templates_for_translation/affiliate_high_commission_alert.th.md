---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ ตรวจพบกิจกรรมค่าคอมมิชชั่นผิดปกติ - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ แจ้งเตือนค่าคอมมิชชั่นสูง
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ตรวจพบกิจกรรมผิดปกติ
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          ได้รับค่าคอมมิชชั่นที่สูงผิดปกติจากแอดด์วิช {{ affiliate_name }} ซึ่งจำเป็นต้องตรวจสอบเพื่อป้องกันการฉ้อโกง
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการแจ้งเตือน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>แอดด์วิช:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>จำนวนค่าคอมมิชชั่น:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>มูลค่าคำสั่งซื้อ:</strong> {{ order_value }}<br/>
              <strong>หมายเลขคำสั่งซื้อ:</strong> {{ order_number }}<br/>
              <strong>ตรวจพบเมื่อ:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เหตุผลที่ถูกทำเครื่องหมาย:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การกระทำที่แนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • ตรวจสอบรายละเอียดคำสั่งซื้อเพื่อความถูกต้อง<br/>
          • ตรวจสอบประวัติการแนะนำของแอดด์วิช<br/>
          • ตรวจสอบว่าลูกค้าไม่ได้เกี่ยวข้องกับผู้แนะนำ<br/>
          • อนุมัติหรือปฏิเสธค่าคอมมิชชั่นในแดชบอร์ดผู้ดูแลระบบ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ตรวจสอบค่าคอมมิชชั่น
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ดูรายละเอียดแอดด์วิช
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ค่าคอมมิชชั่นนี้ยังอยู่ในระหว่างการตรวจสอบและจะไม่ได้รับการชำระเงินจนกว่าจะได้รับการอนุมัติ
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ แจ้งเตือนค่าคอมมิชชั่นสูง

ตรวจพบกิจกรรมผิดปกติ

ได้รับค่าคอมมิชชั่นที่สูงผิดปกติจากแอดด์วิช {{ affiliate_name }} ซึ่งจำเป็นต้องตรวจสอบเพื่อป้องกันการฉ้อโกง

รายละเอียดการแจ้งเตือน:
- แอดด์วิช: {{ affiliate_name }} ({{ affiliate_id }})
- จำนวนค่าคอมมิชชั่น: {{ commission_amount }}
- มูลค่าคำสั่งซื้อ: {{ order_value }}
- หมายเลขคำสั่งซื้อ: {{ order_number }}
- ตรวจพบเมื่อ: {{ detected_at }}

เหตุผลที่ถูกทำเครื่องหมาย:
{{ flag_reason }}

การกระทำที่แนะนำ:
• ตรวจสอบรายละเอียดคำสั่งซื้อเพื่อความถูกต้อง
• ตรวจสอบประวัติการแนะนำของแอดด์วิช
• ตรวจสอบว่าลูกค้าไม่ได้เกี่ยวข้องกับผู้แนะนำ
• อนุมัติหรือปฏิเสธค่าคอมมิชชั่นในแดชบอร์ดผู้ดูแลระบบ

ตรวจสอบค่าคอมมิชชั่น: {{ review_commission_url }}
ดูรายละเอียดแอดด์วิช: {{ affiliate_details_url }}

ค่าคอมมิชชั่นนี้ยังอยู่ในระหว่างการตรวจสอบและจะไม่ได้รับการชำระเงินจนกว่าจะได้รับการอนุมัติ