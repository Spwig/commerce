---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
{{ store_name }}에서 최대한 활용하는 팁

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
          시작 팁
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwig 스토어를 최대한 활용해 보세요
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
          이제 {{ store_name }}이 정상적으로 작동 중이므로, 스토어를 최대한 활용할 수 있는 팁을 몇 가지 알려드릴게요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          외형을 커스터마이즈하세요
        </mj-text>
        <mj-text font-size="14px">
          <strong>디자인 > 테마 설정</strong>으로 이동하여 테마를 선택하고 로고를 업로드하며 브랜드 색상을 설정하세요. 스토어 프론트는 즉시 업데이트되어 변경 사항을 실시간으로 미리 볼 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          상품을 추가하세요
        </mj-text>
        <mj-text font-size="14px">
          <strong>카탈로그 > 상품</strong>으로 이동하여 상품을 추가하기 시작하세요. 색상, 사이즈 등 상품 변형을 생성하고 가격을 설정하며 재고를 관리하고 고해상도 이미지를 업로드할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          결제를 설정하세요
        </mj-text>
        <mj-text font-size="14px">
          <strong>설정 > 결제 제공업체</strong>로 이동하여 Stripe, PayPal 또는 다른 결제 방식을 연결하세요. 여러 제공업체를 활성화하여 고객이 선호하는 방식으로 결제할 수 있도록 할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          배송을 설정하세요
        </mj-text>
        <mj-text font-size="14px">
          <strong>설정 > 배송</strong> 아래에서 배송 지역과 요금을 설정하세요. 다양한 지역에 대해 고정 요금, 무게 기반, 또는 무료 배송 규칙을 생성할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          SEO를 강화하세요
        </mj-text>
        <mj-text font-size="14px">
          Spwig은 자동으로 사이트맵과 메타 태그를 생성합니다. <strong>설정 > SEO</strong>로 이동하여 페이지 제목, 설명, 소셜 공유 이미지를 커스터마이즈하여 고객이 스토어를 쉽게 찾을 수 있도록 도와주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
시작 팁 - {{ store_name }}

안녕하세요 {{ name|default:'there' }},

이제 {{ store_name }}이 정상적으로 작동 중이므로, 스토어를 최대한 활용할 수 있는 팁을 몇 가지 알려드릴게요.

1. 외형을 커스터마이즈하세요
Design > Theme Settings으로 이동하여 테마를 선택하고 로고를 업로드하며 브랜드 색상을 설정하세요.

2. 상품을 추가하세요
Catalog > Products로 이동하여 상품을 추가하세요. 변형, 가격, 이미지 등을 포함한 상품을 추가할 수 있습니다.

3. 결제를 설정하세요
Settings > Payment Providers로 이동하여 Stripe, PayPal 또는 다른 결제 방식을 연결하세요.

4. 배송을 설정하세요
Settings > Shipping 아래에서 배송 지역과 요금을 설정하세요. 다양한 지역에 대해 고정 요금, 무게 기반, 또는 무료 배송 규칙을 생성할 수 있습니다.

5. SEO를 강화하세요
Settings > SEO로 이동하여 페이지 제목, 설명, 소셜 공유 이미지를 커스터마이즈하여 고객이 스토어를 쉽게 찾을 수 있도록 도와주세요.

Admin Panel로 이동: {{ admin_url }}

도움이 필요하신가요? {{ support_email }}로 문의해 주세요.