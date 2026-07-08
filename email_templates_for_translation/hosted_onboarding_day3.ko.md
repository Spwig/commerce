---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
상품 카탈로그를 구축하세요 - {{ store_name }}

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
          시작하기: 상품
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}을 위한 카탈로그를 구축하세요
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
          귀하의 가게 <strong>{{ store_name }}</strong>은 모두 설정되었습니다. 이제 상품 카탈로그를 구축할 시간입니다. 시작하는 데 도움이 되는 5가지 팁을 아래에 소개합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          CSV 파일에서 상품 가져오기
        </mj-text>
        <mj-text font-size="14px">
          이미 상품 목록이 있습니까? <strong>관리자 > 카탈로그 > 가져오기</strong>로 이동하여 CSV 파일에서 상품을 일괄 가져올 수 있습니다. 이는 가게를 빠르게 채우는 가장 빠른 방법입니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          카테고리와 필터로 정리하기
        </mj-text>
        <mj-text font-size="14px">
          고객이 쉽게 둘러보고 원하는 것을 찾을 수 있도록 카테고리와 속성 필터를 생성하세요. 잘 정리된 카탈로그는 전환율을 높이는 데 도움이 됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          매력적인 상품 설명 작성하기
        </mj-text>
        <mj-text font-size="14px">
          훌륭한 설명은 상품을 판매합니다. 기능이 아닌 이점을 중심으로 집중하세요. 고객에게 왜 이 상품이 필요하고 문제를 어떻게 해결하는지 말해주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          고화질 상품 이미지 업로드
        </mj-text>
        <mj-text font-size="14px">
          명확하고 전문적인 이미지는 큰 차이를 만듭니다. 다양한 각도를 업로드하고 일관된 조명을 사용하세요. Spwig는 이미지를 자동으로 최적화하여 빠른 로딩을 보장합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          상품 변형 설정하기
        </mj-text>
        <mj-text font-size="14px">
          상품이 다양한 크기, 색상, 스타일로 제공된다면 고객이 정확히 원하는 것을 선택할 수 있도록 변형을 생성하세요. 각 변형은 자체 가격, 재고 수준, 이미지를 가질 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="상품 관리" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
상품 시작하기: {{ store_name }}

안녕하세요 {{ name|default:'there' }},

귀하의 가게 {{ store_name }}은 모두 설정되었습니다. 이제 상품 카탈로그를 구축할 시간입니다. 시작하는 데 도움이 되는 5가지 팁을 아래에 소개합니다.

1. CSV 파일에서 상품 가져오기
이미 상품 목록이 있습니까? 관리자 > 카탈로그 > 가져오기로 이동하여 CSV 파일에서 상품을 일괄 가져올 수 있습니다.

2. 카테고리와 필터로 정리하기
고객이 쉽게 둘러보고 원하는 것을 찾을 수 있도록 카테고리와 속성 필터를 생성하세요.

3. 매력적인 상품 설명 작성하기
훌륭한 설명은 상품을 판매합니다. 기능이 아닌 이점을 중심으로 집중하세요. 고객에게 왜 이 상품이 필요하고 문제를 어떻게 해결하는지 말해주세요.

4. 고화질 상품 이미지 업로드
명확하고 전문적인 이미지는 큰 차이를 만듭니다. 다양한 각도를 업로드하고 일관된 조명을 사용하세요.

5. 상품 변형 설정하기
상품이 다양한 크기, 색상, 스타일로 제공된다면 고객이 정확히 원하는 것을 선택할 수 있도록 변형을 생성하세요.

상품 관리: {{ admin_url }}

도움이 필요하시면 {{ support_email }}로 연락주세요.