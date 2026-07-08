---
template_type: dev_account_suspended
category: Developer Portal
---

# Email Template: dev_account_suspended

## Subject
บัญชีผู้พัฒนา Spwig ของคุณถูกระงับการใช้งาน

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Warning Accent -->
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          บัญชีถูกระงับการใช้งาน
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          การอัปเดตสำคัญเกี่ยวกับบัญชีผู้พัฒนาของคุณ
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
          บัญชีผู้พัฒนา Spwig ของคุณถูกระงับการใช้งาน ช่วงนี้ส่วนประกอบที่คุณเผยแพร่ยังคงสามารถใช้งานได้ แต่คุณไม่สามารถส่งส่วนประกอบใหม่หรืออัปเดตได้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reason Section (if provided) -->
    {% if suspension_reason %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          เหตุผล:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.warning|default:'#f59e0b' }}">
          {{ suspension_reason }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          หากคุณคิดว่าการกระทำนี้เป็นข้อผิดพลาด กรุณาติดต่อเราที่ <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; text-decoration: none;">{{ support_email }}</a>.
        </mj-text>
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

บัญชีผู้พัฒนา Spwig ของคุณถูกระงับการใช้งาน ช่วงนี้ส่วนประกอบที่คุณเผยแพร่ยังคงสามารถใช้งานได้ แต่คุณไม่สามารถส่งส่วนประกอบใหม่หรืออัปเดตได้

{% if suspension_reason %}เหตุผล: {{ suspension_reason }}{% endif %}

หากคุณคิดว่าการกระทำนี้เป็นข้อผิดพลาด กรุณาติดต่อเราที่ {{ support_email }}.

---
Spwig Developer Portal