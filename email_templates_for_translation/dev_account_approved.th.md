---
template_type: dev_account_approved
category: Developer Portal
---

# Email Template: dev_account_approved

## Subject
ยินดีต้อนรับคุณ {{ developer_name }} ถึงโปรแกรมนักพัฒนา Spwig!

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          ยินดีต้อนรับสู่ Spwig!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          การสมัครนักพัฒนาของคุณได้รับการอนุมัติแล้ว
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
          ยินดีด้วย! การสมัครนักพัฒนาของคุณได้รับการอนุมัติแล้ว คุณสามารถเข้าถึงพอร์ทัลนักพัฒนา Spwig ได้เต็มที่แล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Free License Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 0">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          ใบอนุญาตนักพัฒนาฟรีของคุณกำลังรออยู่
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          เมื่อคุณได้รับการอนุมัติเป็นนักพัฒนา คุณจะได้รับการติดตั้ง Spwig Shop + POS ฟรีพร้อมอัปเดตตลอดชีวิต ขอรับใบอนุญาตของคุณ ติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ และเริ่มสร้างส่วนประกอบได้ทันที
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ license_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          ขอรับใบอนุญาตฟรี
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Get Started Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          เริ่มต้น:
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> ขอรับใบอนุญาตนักพัฒนาฟรีของคุณ
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> ติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>3.</strong> สร้างส่วนประกอบแรกของคุณโดยใช้ SDKs ของเรา
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>4.</strong> ส่งมันจากแดชบอร์ดของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          ไปที่แดชบอร์ด
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

ยินดีด้วย! การสมัครนักพัฒนาของคุณได้รับการอนุมัติแล้ว คุณสามารถเข้าถึงพอร์ทัลนักพัฒนา Spwig ได้เต็มที่แล้ว

ใบอนุญาตนักพัฒนาฟรีของคุณกำลังรออยู่
เมื่อคุณได้รับการอนุมัติเป็นนักพัฒนา คุณจะได้รับการติดตั้ง Spwig Shop + POS ฟรีพร้อมอัปเดตตลอดชีวิต ขอรับใบอนุญาตของคุณ ติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ และเริ่มสร้างส่วนประกอบได้ทันที

ขอรับใบอนุญาตฟรี: {{ license_url }}

เริ่มต้น:
1. ขอรับใบอนุญาตนักพัฒนาฟรีของคุณ: {{ license_url }}
2. ติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ
3. สร้างส่วนประกอบแรกของคุณโดยใช้ SDKs ของเรา
4. ส่งมันจากแดชบอร์ดของคุณ

ไปที่แดชบอร์ด: {{ dashboard_url }}

---
Spwig Developer Portal