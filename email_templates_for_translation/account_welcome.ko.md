---
template_type: account_welcome
category: Enhanced E-commerce
---

# Email Template: account_welcome

## Subject
환영합니다! {{ shop_name }}!

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
          환영합니다! 👋
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          우리 커뮤니티의 일원이 되어 주셔서 기쁩니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personalized Greeting -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          안녕하세요, {{ customer_name }}",
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          귀하의 계정이 성공적으로 생성되었습니다. 쇼핑을 시작할 준비가 되셨습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          회원 혜택
        </mj-text>

        {% for benefit in shop_benefits %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 0">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px;">✓</span> {{ benefit }}
        </mj-text>
        {% endfor %}
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-button
          href="{{ browse_products_url }}"
          background-color="{{ theme.color.primary|default:'#2563eb' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="16px"
          font-weight="600"
          border-radius="6px"
          padding="14px 32px"
        >
          쇼핑 시작
        </mj-button>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button
          href="{{ account_url }}"
          background-color="{{ theme.color.text_muted|default:'#6b7280' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="14px"
          border-radius="6px"
          padding="12px 24px"
        >
          내 계정 관리
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
환영합니다! 👋

안녕하세요, {{ customer_name }},

귀하의 계정이 성공적으로 생성되었습니다. 쇼핑을 시작할 준비가 되셨습니다!

회원 혜택:
{% for benefit in shop_benefits %}
✓ {{ benefit }}
{% endfor %}

쇼핑 시작: {{ browse_products_url }}
내 계정 관리: {{ account_url }}

도움이 필요하신가요?
이메일: {{ support_email }}
전화: {{ support_phone }}