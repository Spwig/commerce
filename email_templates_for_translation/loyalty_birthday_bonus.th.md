---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 วันเกิดสุขสันต์ {{ customer_name }}! นี่คือของขวัญพิเศษจาก {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Happy Birthday!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Happy Birthday, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          To celebrate your special day, we've added {{ bonus_points }} bonus points to your loyalty account!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Your Birthday Gift
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Added to your account!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your Loyalty Account:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Points Balance:</strong> {{ total_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Birthday Bonus:</strong> +{{ bonus_points }} points
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Start Shopping & Use Your Points
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Have an amazing birthday! 🎉<br/>
          - The {{ shop_name }} Team
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 HAPPY BIRTHDAY!

วันเกิดสุขสันต์ {{ customer_name }}!

เพื่อเฉลิมฉลองวันพิเศษของคุณ เราได้เพิ่ม {{ bonus_points }} คะแนนพิเศษเข้าไปในบัญชีความภักดีของคุณ!

ของขวัญวันเกิดของคุณ:
{{ bonus_points }} Points
เพิ่มเข้าไปในบัญชีของคุณ!

บัญชีความภักดีของคุณ:
- คะแนนคงเหลือ: {{ total_points }} points
- ระดับปัจจุบัน: {{ loyalty_tier }}
- ของขวัญวันเกิด: +{{ bonus_points }} points

เริ่มต้นการช้อปปิ้งและใช้คะแนนของคุณ: {{ shop_url }}

ขอให้วันเกิดของคุณมีความสุขที่สุด! 🎉
- ทีม {{ shop_name }}