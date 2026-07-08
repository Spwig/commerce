---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
결제 실패 - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          결제 문제
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}에 대한 조치가 필요합니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요 {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          저희는 <strong>{{ plan_name }}</strong>에 대한 결제를 처리할 수 없습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          결제 정보
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          금액: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          플랜: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. 서비스 중단을 피하기 위해 결제 방법을 업데이트해 주시기 바랍니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="결제 방법 업데이트" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
결제 문제 - {{ store_name }}

안녕하세요 {{ name|default:'there' }},

저희는 {{ plan_name }}에 대한 결제를 처리할 수 없습니다.

결제 정보:
- 금액: {{ currency }}{{ amount }}
- 플랜: {{ plan_name }}

{{ retry_info }}. 서비스 중단을 피하기 위해 결제 방법을 업데이트해 주시기 바랍니다.

결제 방법 업데이트: https://spwig.com/account

도움이 필요하신가요? {{ support_email }}에 문의해 주세요