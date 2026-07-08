---
template_type: loyalty_points_expiring
category: Loyalty Program
---

# Email Template: loyalty_points_expiring

## Subject
기한이 임박한 포인트: {{ expiring_points }}

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
          ⏰ 곧 만료되는 포인트
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Points Display -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center">
          {{ expiring_points }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center">
          {{ days_until_expiration }}일 후 만료
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center">
          만료일: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요, {{ customer_name }}님,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          포인트가 낭비되지 않도록 주의하세요! {{ days_until_expiration }}일 후 만료되는 {{ expiring_points }} 포인트가 있습니다.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          만료되기 전에 독점 보상으로 교환하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Suggested Rewards -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          교환 가능한 보상:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          보상 카탈로그를 확인하고 만료되기 전에 포인트를 교환하세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          지금 포인트 교환하기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
기한이 임박한 포인트: {{ expiring_points }}

안녕하세요, {{ customer_name }}님,

포인트가 낭비되지 않도록 주의하세요! {{ days_until_expiration }}일 후 만료되는 {{ expiring_points }} 포인트가 있습니다.

만료일: {{ expiration_date }}

만료되기 전에 독점 보상으로 교환하세요.

포인트 교환: {{ rewards_url }}

{{ shop_name }}