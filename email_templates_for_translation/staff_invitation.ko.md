---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
{{ store_name }}에 초대받았습니다

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
          스태프 초대
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}에 초대받았습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요, {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }}님이 {{ store_name }}의 스태프로 가입하도록 초대했습니다. 관리자 대시보드에서 매장을 도와 관리할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="초대 수락" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          이 초대는 {{ expires_at|date:"N j, Y" }}에 만료됩니다. 이 초대를 예상하지 못하셨다면 이 이메일을 무시해도 됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
{{ store_name }}에 초대받았습니다

안녕하세요, {{ first_name }},

{{ invited_by }}님이 {{ store_name }}의 스태프로 가입하도록 초대했습니다. 관리자 대시보드에서 매장을 도와 관리할 수 있습니다.

초대 수락: {{ invitation_url }}

이 초대는 {{ expires_at|date:"N j, Y" }}에 만료됩니다. 이 초대를 예상하지 못하셨다면 이 이메일을 무시해도 됩니다.

도움이 필요하신가요? {{ support_email }}에 문의해 주세요.