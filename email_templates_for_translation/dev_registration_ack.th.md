---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
เราได้รับคำขอเข้าร่วมจากคุณแล้ว {{ developer_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ได้รับคำขอแล้ว!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          เราอยู่ในขั้นตอนการตรวจสอบคำขอเข้าร่วมของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          สวัสดี {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          ขอบคุณที่สมัครเข้าร่วมโปรแกรมนักพัฒนา Spwig เราได้รับคำขอของคุณแล้ว และทีมงานของเราจะตรวจสอบคำขอของคุณเร็ว ๆ นี้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          ขั้นตอนต่อไปคืออะไร?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> ทีมงานของเราจะตรวจสอบคำขอของคุณ (โดยทั่วไปใช้เวลา 2-3 วันทำการ)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> คุณจะได้รับอีเมลที่แจ้งผลการพิจารณา
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> เมื่อได้รับการอนุมัติ คุณจะสามารถเข้าถึงแดชบอร์ดสำหรับนักพัฒนาได้ทั้งหมด
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          ดูแดชบอร์ดนักพัฒนา
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig Developer Portal</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          มีคำถาม? ติดต่อฝ่ายสนับสนุนนักพัฒนา
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
สวัสดี {{ developer_name }},

ขอบคุณที่สมัครเข้าร่วมโปรแกรมนักพัฒนา Spwig เราได้รับคำขอของคุณแล้ว และทีมงานของเราจะตรวจสอบคำขอของคุณเร็ว ๆ นี้

ขั้นตอนต่อไปคืออะไร?
1. ทีมงานของเราจะตรวจสอบคำขอของคุณ (โดยทั่วไปใช้เวลา 2-3 วันทำการ)
2. คุณจะได้รับอีเมลที่แจ้งผลการพิจารณา
3. เมื่อได้รับการอนุมัติ คุณจะสามารถเข้าถึงแดชบอร์ดสำหรับนักพัฒนาได้ทั้งหมด

ดูแดชบอร์ดนักพัฒนา: {{ portal_url }}

---
Spwig Developer Portal