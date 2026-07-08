---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
판매 증가 - {{ store_name }}

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
          시작하기: 마케팅 및 성장
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}으로 트래픽과 판매를 유도하세요
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
          이제 {{ store_name }}이 형성되고 있으니, 트래픽을 유도하고 판매를 성장시키는 데 집중할 때입니다. 시작하는 데 도움이 되는 5가지 마케팅 팁을 아래에 소개합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          첫 번째 할인 코드 생성
        </mj-text>
        <mj-text font-size="14px">
          첫 고객을 유치하기 위해 출시 할인을 제공하세요. Marketing > Discount Codes로 이동하여 사용 횟수 제한 및 만료 날짜를 선택할 수 있는 비율 또는 고정 금액 할인을 생성하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          장바구니 포기 회복 설정
        </mj-text>
        <mj-text font-size="14px">
          손실된 판매를 자동으로 회복하세요. Marketing > Abandoned Carts에서 장바구니 포기 회복 이메일을 활성화하여 고객이 남겨둔 상품을 상기시킬 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          소셜 미디어 계정 연결
        </mj-text>
        <mj-text font-size="14px">
          고객이 당신을 찾고 팔로우할 수 있도록 소셜 미디어 프로필을 가게에 연결하세요. Settings > Social Media에서 소셜 링크를 추가하여 가게 하단에 표시할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Google Analytics 추적 설정
        </mj-text>
        <mj-text font-size="14px">
          방문자의 출처와 가게와의 상호작용을 이해하세요. Settings > Analytics에서 Google Analytics 추적 ID를 추가하여 데이터 수집을 시작하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          뉴스레터 등록 양식 생성
        </mj-text>
        <mj-text font-size="14px">
          첫날부터 이메일 목록을 구축하세요. 가게에 뉴스레터 등록 양식을 추가하여 방문자의 이메일을 수집하세요. 이 연락처는 프로모션, 신제품 출시 및 고객 참여에 활용할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
시작하기: 마케팅 및 성장 - {{ store_name }}

안녕하세요 {{ name|default:'there' }},

이제 {{ store_name }}이 형성되고 있으니, 트래픽을 유도하고 판매를 성장시키는 데 집중할 때입니다. 시작하는 데 도움이 되는 5가지 마케팅 팁을 아래에 소개합니다.

1. 첫 번째 할인 코드 생성
  첫 고객을 유치하기 위해 출시 할인을 제공하세요. Marketing > Discount Codes로 이동하여 사용 횟수 제한 및 만료 날짜를 선택할 수 있는 비율 또는 고정 금액 할인을 생성하세요.

2. 장바구니 포기 회복 설정
  손실된 판매를 자동으로 회복하세요. Marketing > Abandoned Carts에서 장바구니 포기 회복 이메일을 활성화하여 고객이 남겨둔 상품을 상기시킬 수 있습니다.

3. 소셜 미디어 계정 연결
  고객이 당신을 찾고 팔로우할 수 있도록 소셜 미디어 프로필을 가게에 연결하세요. Settings > Social Media에서 소셜 링크를 추가하여 가게 하단에 표시할 수 있습니다.

4. Google Analytics 추적 설정
  방문자의 출처와 가게와의 상호작용을 이해하세요. Settings > Analytics에서 Google Analytics 추적 ID를 추가하여 데이터 수집을 시작하세요.

5. 뉴스레터 등록 양식 생성
  첫날부터 이메일 목록을 구축하세요. 가게에 뉴스레터 등록 양식을 추가하여 방문자의 이메일을 수집하세요. 이 연락처는 프로모션, 신제품 출시 및 고객 참여에 활용할 수 있습니다.

마케팅으로 이동: {{ admin_url }}

도움이 필요하신가요? {{ support_email }}로 문의해 주세요.