---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
คุณได้รับคำเชิญให้เข้าร่วม {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          การเชิญเข้าร่วมเป็นพนักงาน
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          คุณได้รับคำเชิญให้เข้าร่วม {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          สวัสดี {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} ได้เชิญคุณให้เข้าร่วม {{ store_name }} ด้วยบทบาทเป็นพนักงาน คุณจะสามารถช่วยจัดการร้านค้าผ่านแดชบอร์ดผู้ดูแลระบบได้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accept Invitation" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          การเชิญนี้จะหมดอายุในวันที่ {{ expires_at|date:"N j, Y" }} หากคุณไม่ได้คาดหวังการเชิญนี้ คุณสามารถปลอดภัยได้โดยการเพิกเฉยอีเมลนี้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
คุณได้รับคำเชิญให้เข้าร่วม {{ store_name }}

สวัสดี {{ first_name }},

{{ invited_by }} ได้เชิญคุณให้เข้าร่วม {{ store_name }} ด้วยบทบาทเป็นพนักงาน คุณจะสามารถช่วยจัดการร้านค้าผ่านแดชบอร์ดผู้ดูแลระบบได้

ยอมรับคำเชิญ: {{ invitation_url }}

การเชิญนี้จะหมดอายุในวันที่ {{ expires_at|date:"N j, Y" }} หากคุณไม่ได้คาดหวังการเชิญนี้ คุณสามารถปลอดภัยได้โดยการเพิกเฉยอีเมลนี้

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}