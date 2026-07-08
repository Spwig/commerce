---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
환영합니다! {{ shop_name }} 리워드 프로그램에 가입하셨습니다!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 환영합니다! 리워드 프로그램에 가입하셨습니다!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          모든 구매로 포인트를 시작하여 벌 수 있습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요, {{ customer_name }}!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ shop_name }} 리워드 프로그램에 오신 것을 환영합니다! 자동으로 가입되어 있으며, 즉시 포인트를 벌 수 있습니다.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 환영 보너스: {{ bonus_points }} 포인트!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>당신의 등급:</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          포인트를 얻는 방법
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 구매하기 - 모든 주문에 포인트를 얻을 수 있습니다<br/>
          • 리뷰 작성 - 피드백을 공유하세요<br/>
          • 친구 추천 - 소문을 퍼뜨리세요<br/>
          • 생일 리워드 - 생일에 특별한 포인트를 얻을 수 있습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          내 리워드 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있나요? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">지원팀에 문의하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
환영합니다! {{ shop_name }} 리워드 프로그램에 가입하셨습니다!

안녕하세요, {{ customer_name }}!

{{ shop_name }} 리워드 프로그램에 오신 것을 환영합니다! 자동으로 가입되어 있으며, 즉시 포인트를 벌 수 있습니다.

{% if bonus_points %}환영 보너스: {{ bonus_points }} 포인트!{% endif %}

당신의 등급: {{ current_tier }}
{{ tier_benefits }}

포인트를 얻는 방법:
- 구매하기 - 모든 주문에 포인트를 얻을 수 있습니다
- 리뷰 작성 - 피드백을 공유하세요
- 친구 추천 - 소문을 퍼뜨리세요
- 생일 리워드 - 생일에 특별한 포인트를 얻을 수 있습니다

리워드 보기: {{ account_url }}

{{ shop_name }}
궁금한 점이 있나요? {{ support_email }}에 문의하세요