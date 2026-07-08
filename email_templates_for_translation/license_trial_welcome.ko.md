---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
스피그에 오신 것을 환영합니다 - {{ trial_days }}일 무료 체험

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          스피그에 오신 것을 환영합니다!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ trial_days }}일 무료 체험 준비 완료
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
          {{ product_name }}을(를) 시도해 주셔서 감사합니다! 체험은 활성화되었으며, 스피그의 모든 기능을 {{ trial_days }}일 동안 탐색하실 수 있습니다{% if includes_pos %}, 포인트 오브 세일 시스템도 포함{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          설치 토큰
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          설치 중에 이 토큰을 사용하여 체험용 스토어를 활성화하세요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          시작하기
        </mj-text>
        <mj-text font-size="14px">
          1. 스피그를 서버에 설치하기 위해我们的 설치 가이드를 따르세요
        </mj-text>
        <mj-text font-size="14px">
          2. 설치 중에 요청 시 설치 토큰을 입력하세요
        </mj-text>
        <mj-text font-size="14px">
          3. 온라인 스토어를 구축해 보세요!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="설치 가이드 보기" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          체험에 포함된 항목
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ trial_days }}일 동안 모든 핵심 기능에 대한 전체 접근 권한
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          상품 카탈로그, 주문 및 고객 관리
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          테마 커스터마이징 및 페이지 빌더
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          결제 및 배송 제공업체 통합
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          포인트 오브 세일 (POS) 시스템
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ trial_days }}일 후에 체험 기간이 만료됩니다. 준비가 되셨다면, 데이터 손실 없이 스토어를 계속 운영할 수 있도록 전체 라이선스로 업그레이드하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
스피그에 오신 것을 환영합니다!
{{ trial_days }}일 무료 체험 준비 완료.

안녕하세요, {{ customer_name }}!

{{ product_name }}을(를) 시도해 주셔서 감사합니다! 체험은 활성화되었으며, 스피그의 모든 기능을 {{ trial_days }}일 동안 탐색하실 수 있습니다{% if includes_pos %}, 포인트 오브 세일 시스템도 포함{% endif %}.

설치 토큰:
{{ setup_token }}
설치 중에 이 토큰을 사용하여 체험용 스토어를 활성화하세요.

시작하기:
1. 스피그를 서버에 설치하기 위해我们的 설치 가이드를 따르세요
2. 설치 중에 요청 시 설치 토큰을 입력하세요
3. 온라인 스토어를 구축해 보세요!

설치 가이드 보기: {{ setup_url }}

체험에 포함된 항목:
- {{ trial_days }}일 동안 모든 핵심 기능에 대한 전체 접근 권한
- 상품 카탈로그, 주문 및 고객 관리
- 테마 커스터마이징 및 페이지 빌더
- 결제 및 배송 제공업체 통합
{% if includes_pos %}- 포인트 오브 세일 (POS) 시스템{% endif %}

{{ trial_days }}일 후에 체험 기간이 만료됩니다. 준비가 되셨다면, 데이터 손실 없이 스토어를 계속 운영할 수 있도록 전체 라이선스로 업그레이드하세요.

도움이 필요하신가요? {{ support_email }}로 문의해 주세요