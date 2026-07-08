---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
스피그 라이선스 - 주문 #{{ order_number }}

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
          구매 감사합니다!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          주문 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요, {{ customer_name }},
        </mj-text>
        <mj-text>
          {{ product_name }}의 구매가 완료되었습니다. 아래에 라이선스 키와 설정 토큰이 포함되어 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          주문 요약
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          제품: {{ product_name }}{% if includes_pos %} (POS 포함){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          금액: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          주문 번호: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          귀하의 라이선스 키
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          이 키를 저장하세요 - 재설치 시 필요합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          귀하의 설정 토큰
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          설치 중에 이 토큰을 사용하여 가게를 활성화하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          시작하기
        </mj-text>
        <mj-text font-size="14px">
          1. 우리의 설정 가이드를 따라 서버에 Spwig을 설치하세요
        </mj-text>
        <mj-text font-size="14px">
          2. 설치 중에 설정 토큰을 입력하세요
        </mj-text>
        <mj-text font-size="14px">
          3. 가게가 자동으로 활성화됩니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="설치 가이드 보기" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          계정 생성
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          비밀번호를 설정하여 라이선스를 관리하고 다운로드에 액세스하고 업데이트를 받을 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="계정 생성" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          주의:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          이 이메일을 안전하게 보관하세요 - 향후 참조를 위해 라이선스 키와 설정 토큰이 포함되어 있습니다. 이 자격 증명을 다른 사람과 공유하지 마세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
구매 감사합니다!

주문 #{{ order_number }}

안녕하세요, {{ customer_name }},

{{ product_name }}의 구매가 완료되었습니다. 아래에 라이선스 키와 설정 토큰이 포함되어 있습니다.

주문 요약:
- 제품: {{ product_name }}{% if includes_pos %} (POS 포함){% endif %}
- 금액: {{ price }}
- 주문 번호: {{ order_number }}

귀하의 라이선스 키:
{{ license_key }}
이 키를 저장하세요 - 재설치 시 필요합니다.

귀하의 설정 토큰:
{{ setup_token }}
설치 중에 이 토큰을 사용하여 가게를 활성화하세요.

시작하기:
1. 우리의 설정 가이드를 따라 서버에 Spwig을 설치하세요
2. 설치 중에 설정 토큰을 입력하세요
3. 가게가 자동으로 활성화됩니다

설치 가이드 보기: {{ setup_url }}
{% if activation_url %}
계정 생성:
비밀번호를 설정하여 라이선스를 관리하고 다운로드에 액세스하고 업데이트를 받을 수 있습니다.
{{ activation_url }}
{% endif %}
중요:
이 이메일을 안전하게 보관하세요 - 향후 참조를 위해 라이선스 키와 설정 토큰이 포함되어 있습니다. 이 자격 증명을 다른 사람과 공유하지 마세요.

도움이 필요하신가요? {{ support_email }}에 문의하세요