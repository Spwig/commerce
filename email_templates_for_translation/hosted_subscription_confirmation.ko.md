---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
구독 확인 - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          구독 확인!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwig에 오신 것을 환영합니다
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
          구독을 감사합니다! {{ store_name }}을 위한 <strong>{{ plan_name }}</strong> 플랜이 확인되었습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          플랜 세부 정보
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          플랜: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          청구 주기: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          금액: {{ currency }}{{ amount }}{% if intro_period %} (시범 가격){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          시범 가격은 {{ intro_period }} 동안 적용됩니다. 이후에는 {{ currency }}{{ full_amount }}/{{ billing_interval }}에 따라 플랜이 갱신됩니다.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          귀하의 스토어가 현재 설정되고 있으며, 준비되면 이메일을 다시 받게 됩니다.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          다음 청구일: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
구독 확인!

안녕하세요 {{ name|default:'there' }},

구독을 감사합니다! {{ store_name }}을 위한 {{ plan_name }} 플랜이 확인되었습니다.

플랜 세부 정보:
- 플랜: {{ plan_name }}
- 청구 주기: {{ billing_interval }}
- 금액: {{ currency }}{{ amount }}{% if intro_period %} (시범 가격){% endif %}
{% if intro_period %}
이 시범 가격은 {{ intro_period }} 동안 적용됩니다. 이후에는 {{ currency }}{{ full_amount }}/{{ billing_interval }}에 따라 플랜이 갱신됩니다.
{% endif %}
귀하의 스토어가 현재 설정되고 있으며, 준비되면 이메일을 다시 받게 됩니다.

다음 청구일: {{ next_billing_date }}

도움이 필요하신가요? {{ support_email }}에 문의해 주세요