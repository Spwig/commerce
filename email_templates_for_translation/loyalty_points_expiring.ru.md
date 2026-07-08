---
template_type: loyalty_points_expiring
category: Loyalty Program
---

# Email Template: loyalty_points_expiring

## Subject
Напоминание: {{ expiring_points }} баллов скоро истекут

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
          ⏰ Баллы скоро истекут
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
          баллов истекут через {{ days_until_expiration }} дней
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center">
          Дата истечения: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Не позволяйте своим баллам пропасть! У вас есть {{ expiring_points }} баллов, которые скоро истекут.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Обменяйте их сейчас, чтобы получить эксклюзивные награды до того, как они исчезнут.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Suggested Rewards -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Награды, которые вы можете получить:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ознакомьтесь с нашим каталогом наград и обменяйте свои баллы до их истечения.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          Обменять баллы сейчас
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
Напоминание: {{ expiring_points }} баллов скоро истекут

Здравствуйте, {{ customer_name }},

Не позволяйте своим баллам пропасть! У вас есть {{ expiring_points }} баллов, которые скоро истекут в течение {{ days_until_expiration }} дней.

Дата истечения: {{ expiration_date }}

Обменяйте их сейчас, чтобы получить эксклюзивные награды до того, как они исчезнут.

Обменять баллы: {{ rewards_url }}

{{ shop_name }}