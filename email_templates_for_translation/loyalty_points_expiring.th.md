---
template_type: loyalty_points_expiring
category: Loyalty Program
---

# Email Template: loyalty_points_expiring

## Subject
ข้อความเตือน: คะแนน {{ expiring_points }} กำลังจะหมดอายุเร็ว ๆ นี้

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ คะแนนกำลังจะหมดอายุเร็ว ๆ นี้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Points Display -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center">
          {{ expiring_points }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center">
          คะแนนจะหมดอายุใน {{ days_until_expiration }} วัน
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center">
          วันหมดอายุ: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          สวัสดี {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          อย่าปล่อยให้คะแนนของคุณสูญเสียไป! คุณมีคะแนน {{ expiring_points }} คะแนนที่กำลังจะหมดอายุเร็ว ๆ นี้
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          แลกคะแนนตอนนี้เพื่อรับรางวัลพิเศษก่อนที่จะหมดไป
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Suggested Rewards -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          รางวัลที่คุณสามารถได้รับ:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          ดูแคตตาล็อกรางวัลของเราและแลกคะแนนของคุณก่อนที่จะหมดอายุ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          แลกคะแนนตอนนี้
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ข้อความเตือน: {{ expiring_points }} คะแนนกำลังจะหมดอายุเร็ว ๆ นี้

Hi {{ customer_name }},

อย่าปล่อยให้คะแนนของคุณสูญเสียไป! คุณมี {{ expiring_points }} คะแนนที่กำลังจะหมดอายุใน {{ days_until_expiration }} วัน

วันหมดอายุ: {{ expiration_date }}

แลกคะแนนตอนนี้เพื่อรับรางวัลพิเศษก่อนที่จะหมดไป

แลกคะแนน: {{ rewards_url }}

{{ shop_name }}