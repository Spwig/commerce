---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
ข้อผิดพลาดในการจัดส่ง - คำสั่งซื้อ #{{ order_number }} ต้องการความช่วยเหลือ

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ ข้อผิดพลาดในการจัดส่ง
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เราติดต่อคุณเพื่อแจ้งข้อผิดพลาดเกี่ยวกับการจัดส่งของคุณ เรากำลังดำเนินการแก้ไขปัญานี้โดยเร็วที่สุดเท่าที่จะเป็นไปได้
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              รายละเอียดข้อผิดพลาด:
            </mj-text>
            <mj-text color="#92400e">
              <strong>ประเภทข้อผิดพลาด:</strong> {{ exception_type }}<br/>
              <strong>คำอธิบาย:</strong> {{ exception_description }}<br/>
              <strong>เกิดขึ้นเมื่อ:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ข้อมูลคำสั่งซื้อ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>หมายเลขคำสั่งซื้อ:</strong> {{ order_number }}<br/>
              <strong>หมายเลขติดตาม:</strong> {{ tracking_number }}<br/>
              <strong>ผู้ให้บริการจัดส่ง:</strong> {{ carrier_name }}<br/>
              <strong>สถานที่ปัจจุบัน:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สิ่งที่จะเกิดขึ้นต่อไปคืออะไร?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ การดำเนินการที่จำเป็น:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ติดตามคำสั่งซื้อของคุณ
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ติดต่อฝ่ายสนับสนุน
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ข้อผิดพลาดในการจัดส่ง

สวัสดี {{ customer_name }},

เราติดต่อคุณเพื่อแจ้งข้อผิดพลาดเกี่ยวกับการจัดส่งของคุณ เรากำลังดำเนินการแก้ไขปัญานี้โดยเร็วที่สุดเท่าที่จะเป็นไปได้

รายละเอียดข้อผิดพลาด:
- ประเภทข้อผิดพลาด: {{ exception_type }}
- คำอธิบาย: {{ exception_description }}
- เกิดขึ้นเมื่อ: {{ exception_date }}

ข้อมูลคำสั่งซื้อ:
- หมายเลขคำสั่งซื้อ: {{ order_number }}
- หมายเลขติดตาม: {{ tracking_number }}
- ผู้ให้บริการจัดส่ง: {{ carrier_name }}
- สถานที่ปัจจุบัน: {{ current_location }}

สิ่งที่จะเกิดขึ้นต่อไปคืออะไร?
{{ resolution_steps }}

{% if action_required %}
⚠️ การดำเนินการที่จำเป็น:
{{ action_required_description }}
{% endif %}

ติดตามคำสั่งซื้อของคุณ: {{ tracking_url }}
ติดต่อฝ่ายสนับสนุน: {{ support_url }}