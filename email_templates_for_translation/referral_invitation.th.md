---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} ส่งของขวัญมาให้คุณ!

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 คุณถูกเชิญชวนแล้ว!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} ต้องการแบ่งปัน {{ shop_name }} ให้คุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          รับของขวัญต้อนรับของคุณ
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          เมื่อคุณทำการซื้อครั้งแรก
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    {% if personal_message %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" font-style="italic" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ personal_message }}"
          <br/><br/>
          - {{ referrer_name }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          สวัสดีค่ะ,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} คิดว่าคุณจะชอบการช้อปปิ้งที่ {{ shop_name }} ในการต้อนรับคุณ เราเสนอส่วนลด {{ reward_amount }} สำหรับการซื้อครั้งแรกของคุณ!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          เพียงแค่คลิกปุ่มด้านล่างเพื่อเริ่มต้น และของขวัญของคุณจะถูกนำไปใช้โดยอัตโนมัติในคำสั่งซื้อแรกของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          วิธีการใช้งาน
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. คลิกปุ่มเพื่อเข้าสู่ {{ shop_name }}<br/>
          2. เลือกสินค้าและเพิ่มลงในตะกร้า<br/>
          3. ดำเนินการชำระเงิน<br/>
          4. ส่วนลด {{ reward_amount }} ของคุณจะถูกนำไปใช้โดยอัตโนมัติ!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          รับของขวัญ {{ reward_amount }} ของฉัน
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          คำเชิญนี้ถูกส่งโดย {{ referrer_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} ส่งของขวัญมาให้คุณ!

สวัสดีค่ะ,

{{ referrer_name }} คิดว่าคุณจะชอบการช้อปปิ้งที่ {{ shop_name }} ในการต้อนรับคุณ เราเสนอส่วนลด {{ reward_amount }} สำหรับการซื้อครั้งแรกของคุณ!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

วิธีการใช้งาน:
1. เข้าสู่ {{ shop_name }}
2. เลือกสินค้าและเพิ่มลงในตะกร้า
3. ดำเนินการชำระเงิน
4. ส่วนลด {{ reward_amount }} ของคุณจะถูกนำไปใช้โดยอัตโนมัติ!

รับของขวัญ: {{ referral_link }}

{{ shop_name }}
คำเชิญนี้ถูกส่งโดย {{ referrer_name }}
คำถาม? ติดต่อ {{ support_email }}