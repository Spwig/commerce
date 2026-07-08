---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
더 나아가기 - {{ store_name }}

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
          시작하기: 고급 기능
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}의 전체 잠재력을 해방하세요
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
          이제 {{ store_name }}을 운영한 지 몇 주가 지났습니다. 가게를 한 단계 더 끌어올릴 수 있는 고급 기능을 소개합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          자동 이메일 워크플로 설정
        </mj-text>
        <mj-text font-size="14px">
          이메일 워크플로를 통해 고객과의 소통을 자동화하세요. 환영 시퀀스, 구매 후 후속 조치, 재참여 캠페인을 <strong>마케팅 > 이메일 워크플로</strong>에서 설정할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          지역별 세금 규칙 설정
        </mj-text>
        <mj-text font-size="14px">
          올바른 세금 비율을 청구하고 있는지 확인하세요. <strong>설정 > 세금</strong>으로 각 판매 지역의 세금 규칙을 설정할 수 있습니다. 세금 포함 또는 세금 제외 가격 설정도 가능합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          통합을 위한 API 탐색
        </mj-text>
        <mj-text font-size="14px">
          계획에 API 액세스가 포함되어 있다면 외부 도구 및 서비스와 가게를 통합할 수 있습니다. <strong>설정 > API</strong>로 이동하여 API 키를 생성하고 문서를 확인하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          분석 대시보드 확인
        </mj-text>
        <mj-text font-size="14px">
          가게의 성과를 주시하세요. <strong>대시보드</strong>는 수익, 주문, 인기 상품, 고객 인사이트 등 주요 지표를 표시하여 데이터 기반 의사결정을 도와줍니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          오프라인 판매를 위한 POS 추가 고려
        </mj-text>
        <mj-text font-size="14px">
          오프라인 판매도 하시나요? Spwig의 포인트 오브 세일 기능은 온라인 재고 및 주문 관리와 동기화된 오프라인 거래를 처리할 수 있습니다. <strong>설정 > 포인트 오브 세일</strong>을 확인해 보세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="대시보드 탐색" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
시작하기: 고급 기능 - {{ store_name }}

안녕하세요 {{ name|default:'there' }},

이제 {{ store_name }}을 운영한 지 몇 주가 지났습니다. 가게를 한 단계 더 끌어올릴 수 있는 고급 기능을 소개합니다.

1. 자동 이메일 워크플로 설정
환영 시퀀스, 구매 후 후속 조치, 재참여 캠페인을 통해 고객과의 소통을 자동화하세요.

2. 지역별 세금 규칙 설정
올바른 세금 비율을 청구하고 있는지 확인하세요. 설정 > 세금으로 각 지역의 규칙을 설정하세요.

3. 통합을 위한 API 탐색
계획에 API 액세스가 포함되어 있다면 외부 도구와 통합하세요. 설정 > API로 시작하세요.

4. 분석 대시보드 확인
대시보드는 수익, 주문, 인기 상품, 고객 인사이트 등 주요 지표를 표시합니다.

5. 오프라인 판매를 위한 POS 추가 고려
오프라인 판매도 하시나요? Spwig의 포인트 오브 세일 기능은 온라인 재고와 동기화된 오프라인 거래를 처리합니다.

대시보드 탐색: {{ admin_url }}

도움이 필요하신가요? {{ support_email }}로 문의하세요