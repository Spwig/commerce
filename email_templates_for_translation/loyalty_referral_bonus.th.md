---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 ได้คะแนนพิเศษจากการแนะนำ {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 ได้คะแนนพิเศษจากการแนะนำ!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ขอบคุณสำหรับการแบ่งปัน, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ข่าวดี! {{ referee_name }} ได้เข้าร่วมโปรแกรมความภักดีของเราผ่านการแนะนำของคุณ และคุณได้รับคะแนนพิเศษ!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              คุณได้รับ
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} คะแนน
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              สำหรับการแนะนำ {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ยอดคงเหลือที่อัปเดตของคุณ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>คะแนนคงเหลือ:</strong> {{ total_points }} คะแนน<br/>
          <strong>โบนัสการแนะนำ:</strong> +{{ bonus_points }} คะแนน<br/>
          <strong>เพื่อนที่แนะนำ:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ยิ่งแบ่งปัน ยิ่งได้คะแนนมากขึ้น!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ได้รับ {{ points_per_referral }} คะแนนสำหรับเพื่อนแต่ละคนที่เข้าร่วม ไม่มีข้อจำกัด!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              แบ่งปันลิงก์การแนะนำของคุณ
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          เริ่มช้อปปิ้ง
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 ได้รับโบนัสการแนะนำ!

ขอบคุณสำหรับการแบ่งปัน, {{ customer_name }}!

ข่าวดี! {{ referee_name }} ได้เข้าร่วมโปรแกรมความภักดีของเราผ่านการแนะนำของคุณ และคุณได้รับคะแนนพิเศษ!

คุณได้รับ:
+{{ bonus_points }} คะแนน
สำหรับการแนะนำ {{ referee_name }}

ยอดคงเหลือที่อัปเดตของคุณ:
- คะแนนคงเหลือ: {{ total_points }} คะแนน
- โบนัสการแนะนำ: +{{ bonus_points }} คะแนน
- เพื่อนที่แนะนำ: {{ total_referrals }}

ยิ่งแบ่งปัน ยิ่งได้คะแนนมากขึ้น!
ได้รับ {{ points_per_referral }} คะแนนสำหรับเพื่อนแต่ละคนที่เข้าร่วม ไม่มีข้อจำกัด!

แบ่งปันลิงก์การแนะนำของคุณ: {{ referral_url }}
เริ่มช้อปปิ้ง: {{ shop_url }}