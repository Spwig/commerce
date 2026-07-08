---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
{{ site_name }}에서 계정을 생성하세요

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
          초대받았습니다!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ site_name }}에서 계정을 생성하세요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요, {{ customer_name }}!
        </mj-text>
        <mj-text>
          저희와의 쇼핑 시 게스트로 이용하셨음을 확인했습니다. 주문 추적, 빠른 결제, 전용 혜택 등 다양한 혜택을 받으려면 전체 계정을 생성해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          구매 내역
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          총 주문 수: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          총 지출 금액: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          계정을 생성하는 이유
        </mj-text>
        <mj-text font-size="14px">
          - 주문을 추적하고 주문 내역을 확인하세요
        </mj-text>
        <mj-text font-size="14px">
          - 저장된 정보로 더 빠른 결제
        </mj-text>
        <mj-text font-size="14px">
          - 주소 및 선호도를 관리하세요
        </mj-text>
        <mj-text font-size="14px">
          - 전용 제안 및 프로모션에 접근하세요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          이 링크는 계정에 비밀번호를 설정할 수 있도록 해줍니다. 기존의 주문 내역은 보존됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
계정을 생성하라는 초대입니다!

안녕하세요, {{ customer_name }}!

저희와의 쇼핑 시 게스트로 이용하셨음을 확인했습니다. 주문 추적, 빠른 결제, 전용 혜택 등 다양한 혜택을 받으려면 전체 계정을 생성해 주세요.

구매 내역:
- 총 주문 수: {{ total_orders }}
- 총 지출 금액: {{ total_spent }}

계정을 생성하는 이유:
- 주문을 추적하고 주문 내역을 확인하세요
- 저장된 정보로 더 빠른 결제
- 주소 및 선호도를 관리하세요
- 전용 제안 및 프로모션에 접근하세요

계정 생성: {{ activation_url }}

이 링크는 계정에 비밀번호를 설정할 수 있도록 해줍니다. 기존의 주문 내역은 보존됩니다.

도움이 필요하신가요? {{ support_email }}에 문의해 주세요