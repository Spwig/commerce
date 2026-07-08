---
template_type: dev_component_published
category: Developer Portal
---

# Email Template: dev_component_published

## Subject
{{ component_name }} v{{ version }} ได้เปิดตัวอย่างเป็นทางการใน Spwig Marketplace แล้ว!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="50px 20px">
      <mj-column>
        <mj-text font-size="36px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          ปัจจุบันเปิดตัวแล้ว!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="15px">
          คอมโพเนนต์ของคุณอยู่ใน Spwig Marketplace แล้ว
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
          คอมโพเนนต์ของคุณได้เปิดตัวและพร้อมใช้งานสำหรับผู้ขาย Spwig ทุกคนในตลาดแล้ว!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>คอมโพเนนต์:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>ประเภท:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>เวอร์ชัน:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Analytics Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          ติดตามประสิทธิภาพของคอมโพเนนต์ของคุณผ่านแดชบอร์ดการวิเคราะห์ — การดาวน์โหลด คะแนน และรีวิวจะปรากฏขึ้นเมื่อผู้ขายเริ่มใช้งาน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          ดูการวิเคราะห์
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
          มีคำถาม? ติดต่อฝ่ายสนับสนุนผู้พัฒนา
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
สวัสดี {{ developer_name }},

คอมโพเนนต์ของคุณได้เปิดตัวและพร้อมใช้งานสำหรับผู้ขาย Spwig ทุกคนในตลาดแล้ว!

คอมโพเนนต์: {{ component_name }}
ประเภท: {{ component_type }}
เวอร์ชัน: v{{ version }}

ติดตามประสิทธิภาพของคอมโพเนนต์ของคุณผ่านแดชบอร์ดการวิเคราะห์ — การดาวน์โหลด คะแนน และรีวิวจะปรากฏขึ้นเมื่อผู้ขายเริ่มใช้งาน

ดูการวิเคราะห์: {{ dashboard_url }}

---
Spwig Developer Portal