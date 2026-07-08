---
template_type: loyalty_points_expiring
category: Loyalty Program
---

# Email Template: loyalty_points_expiring

## Subject
お知らせ: {{ expiring_points }} ポイントが間もなく期限切れになります

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
          ⏰ ポイントが間もなく期限切れになります
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
          ポイントが{{ days_until_expiration }}日後に期限切れになります
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center">
          期限切れ日: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          こんにちは {{ customer_name }}、
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          ポイントを無駄にしないでください！{{ expiring_points }}ポイントが間もなく期限切れになります。
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          期限切れになる前に、限定特典を獲得するために今すぐポイントを交換してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Suggested Rewards -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          獲得可能な特典:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          特典カタログを閲覧し、期限切れになる前にポイントを交換してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          今すぐポイントを交換
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
お知らせ: {{ expiring_points }} ポイントが間もなく期限切れになります

こんにちは {{ customer_name }}、

ポイントを無駄にしないでください！{{ expiring_points }}ポイントが{{ days_until_expiration }}日後に期限切れになります。

期限切れ日: {{ expiration_date }}

期限切れになる前に、限定特典を獲得するために今すぐポイントを交換してください。

ポイントを交換: {{ rewards_url }}

{{ shop_name }}