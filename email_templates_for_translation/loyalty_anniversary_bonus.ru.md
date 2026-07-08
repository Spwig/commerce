---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} год{{ years_as_member|pluralize }} на {{ shop_name }} - Спасибо!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} год{{ years_as_member|pluralize }} вместе!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Сегодня отмечает {{ years_as_member }} год{{ years_as_member|pluralize }} со дня вашего присоединения к нашей программе лояльности. Спасибо, что являетесь таким ценным членом!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Добро пожаловать в программу лояльности
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Бонусных баллов
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Добавлено, чтобы отметить {{ years_as_member }} год{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваш путь в {{ years_as_member }}-год:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Посмотреть панель управления лояльности
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Спасибо за {{ years_as_member }} потрясающий год{{ years_as_member|pluralize }}!<br/>
          За много больше 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} ГОД{{ years_as_member|pluralize|upper }} ВМЕСТЕ!

Здравствуйте, {{ customer_name }},

Сегодня отмечает {{ years_as_member }} год{{ years_as_member|pluralize }} со дня вашего присоединения к нашей программе лояльности. Спасибо, что являетесь таким ценным членом!

ДОБРО ПОЖАЛОВАТЬ В ПРОГРАММУ ЛОЯЛЬНОСТИ:
{{ bonus_points }} Бонусных баллов
Добавлено, чтобы отметить {{ years_as_member }} год{{ years_as_member|pluralize }}!

ВАШ ПУТЬ В {{ years_as_member }}-ГОД:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

Посмотреть панель управления лояльности: {{ loyalty_dashboard_url }}

Спасибо за {{ years_as_member }} потрясающий год{{ years_as_member|pluralize }}!
За много больше 🥂
