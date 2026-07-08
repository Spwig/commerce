---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
매장 일시 중지 - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          계정 일시 중지
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          귀하의 매장 <strong>{{ store_name }}</strong>이 미결제 요금으로 인해 일시 중지되었습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          이는 무엇을 의미하는가
        </mj-text>
        <mj-text font-size="14px">
          귀하의 매장은 이제 읽기 전용 모드가 됩니다 — 고객은 둘러보기만 할 수 있지만 주문은 비활성화됩니다. 귀하의 데이터는 안전하며 30일 동안 보존됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          전체 액세스를 복원하려면 결제 수단을 업데이트하고 미결 잔액을 정산해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="매장 재활성화" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
계정 일시 중지 - {{ store_name }}

안녕하세요, {{ name|default:'there' }},

귀하의 매장 {{ store_name }}이 미결제 요금으로 인해 일시 중지되었습니다.

이것은 무엇을 의미하는가:
귀하의 매장은 이제 읽기 전용 모드가 됩니다 — 고객은 둘러보기만 할 수 있지만 주문은 비활성화됩니다. 귀하의 데이터는 안전하며 30일 동안 보존됩니다.

전체 액세스를 복원하려면 결제 수단을 업데이트하고 미결 잔액을 정산해 주세요.

매장 재활성화: https://spwig.com/account

도움이 필요하신가요? {{ support_email }}로 문의해 주세요.