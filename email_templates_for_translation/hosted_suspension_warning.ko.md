---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
조치가 필요한 경우 - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          정지 경고
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
          안녕하세요, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          {{ plan_name }}의 결제가 지연되었습니다. {{ grace_end_date }}까지 해결하지 않으면, 귀하의 스토어는 읽기 전용 모드로 전환됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          정지의 의미
        </mj-text>
        <mj-text font-size="14px">
          스토어가 정지되면 방문자에게는 여전히 보이지만, 변경 사항을 적용할 수 없습니다. 미결 잔액이 정산될 때까지 새로운 주문은 일시 중단됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          스토어의 중단을 피하려면 결제 수단을 업데이트해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="결제 수단 업데이트" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
정지 경고 - {{ store_name }}

안녕하세요, {{ name|default:'there' }},

{{ plan_name }}의 결제가 지연되었습니다. {{ grace_end_date }}까지 해결하지 않으면, 귀하의 스토어는 읽기 전용 모드로 전환됩니다.

정지의 의미:
스토어가 정지되면 방문자에게는 여전히 보이지만, 변경 사항을 적용할 수 없습니다. 미결 잔액이 정산될 때까지 새로운 주문은 일시 중단됩니다.

스토어의 중단을 피하려면 결제 수단을 업데이트해 주세요.

결제 수단 업데이트: https://spwig.com/account

도움이 필요하신가요? {{ support_email }}에 문의해 주세요.