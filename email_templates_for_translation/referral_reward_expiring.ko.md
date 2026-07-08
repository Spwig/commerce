---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
기억하세요: {{ reward_amount }} 보상이 곧 만료됩니다

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ 보상이 곧 만료됩니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Banner -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center" padding-top="10px">
          {{ days_until_expiration }}일 후 만료됩니다
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          만료일: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요, {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ reward_amount }} 추천 보상을 날리지 마세요! {{ days_until_expiration }}일 후 만료됩니다.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          너무 늦기 전에 다음 구매에서 사용하세요!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>보상 유형:</strong> {{ reward_type_display }}<br/>
          <strong>금액:</strong> {{ reward_amount }}<br/>
          <strong>만료일:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          지금 쇼핑하기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있나요? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">고객 지원에 문의하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
기억하세요: {{ reward_amount }} 보상이 곧 만료됩니다

안녕하세요, {{ customer_name }},

{{ reward_amount }} 추천 보상을 날리지 마세요! {{ days_until_expiration }}일 후 만료됩니다.

보상 정보:
- 유형: {{ reward_type_display }}
- 금액: {{ reward_amount }}
- 만료일: {{ expiration_date }}

너무 늦기 전에 다음 구매에서 사용하세요!

지금 쇼핑하기: {{ shop_url }}

{{ shop_name }}
궁금한 점이 있나요? {{ support_email }}에 문의하세요