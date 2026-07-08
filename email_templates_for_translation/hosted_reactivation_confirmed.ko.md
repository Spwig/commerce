---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
환영합니다! {{ store_name }}이 다시 활성화되었습니다

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
          환영합니다!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}이 다시 활성화되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요,
        </mj-text>
        <mj-text>
          기쁜 소식입니다! 귀하의 <strong>{{ store_name }}</strong> 스토어가 다시 활성화되었습니다. 귀하의 <strong>{{ plan_name }}</strong> 구독이 이제 활성화되었으며, 스토어가 다시 온라인으로 돌아옵니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          재활성화 세부 정보
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          플랜: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          처리된 결제: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          다음 결제 날짜: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          귀하의 스토어가 지금 다시 온라인으로 돌아옵니다. 모든 항목이 완전히 복원되기까지 몇 분이 걸릴 수 있습니다. 다시 온라인 상태가 되면, 귀하의 스토어는 {{ store_url }}에서 접근할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
환영합니다! {{ store_name }}이 다시 활성화되었습니다

안녕하세요,

기쁜 소식입니다! 귀하의 {{ store_name }} 스토어가 다시 활성화되었습니다. 귀하의 {{ plan_name }} 구독이 이제 활성화되었으며, 스토어가 다시 온라인으로 돌아옵니다.

재활성화 세부 정보:
- 플랜: {{ plan_name }}
- 처리된 결제: {{ currency }}{{ amount }}
- 다음 결제 날짜: {{ next_billing_date }}

귀하의 스토어가 지금 다시 온라인으로 돌아옵니다. 모든 항목이 완전히 복원되기까지 몇 분이 걸릴 수 있습니다. 다시 온라인 상태가 되면, 귀하의 스토어는 {{ store_url }}에서 접근할 수 있습니다.

스토어로 이동: {{ admin_url }}

도움이 필요하신가요? {{ support_email }}로 문의해 주세요