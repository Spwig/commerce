---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Бонусные баллы за приглашение {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Получен бонус за реферала!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Спасибо за делегирование, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Великолепные новости! {{ referee_name }} только что присоединился к нашей программе лояльности через вашу реферальную ссылку, и вы заработали бонусные баллы!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Вы заработали
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Баллов
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              За приглашение {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваш обновленный баланс:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Баланс баллов:</strong> {{ total_points }} баллов<br/>
          <strong>Бонус за реферала:</strong> +{{ bonus_points }} баллов<br/>
          <strong>Приглашенные друзья:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Продолжайте делиться, продолжайте зарабатывать!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Получите {{ points_per_referral }} баллов за каждого друга, который присоединяется. Нет ограничений!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Поделиться вашей реферальной ссылкой
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Начать покупки
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 БОНУС ЗА РЕФЕРАЛА!

Спасибо за делегирование, {{ customer_name }}!

Великолепные новости! {{ referee_name }} только что присоединился к нашей программе лояльности через вашу реферальную ссылку, и вы заработали бонусные баллы!

ВЫ ЗАРАБОТАЛИ:
+{{ bonus_points }} Баллов
За приглашение {{ referee_name }}

ВАШ ОБНОВЛЕННЫЙ БАЛАНС:
- Баланс баллов: {{ total_points }} баллов
- Бонус за реферала: +{{ bonus_points }} баллов
- Приглашенные друзья: {{ total_referrals }}

ПРОДОЛЖАЙТЕ ДЕЛИТЬСЯ, ПРОДОЛЖАЙТЕ ЗАРАБАТЫВАТЬ!
Зарабатывайте {{ points_per_referral }} баллов за каждого друга, который присоединяется. Нет ограничений!

Поделиться вашей реферальной ссылкой: {{ referral_url }}
Начать покупки: {{ shop_url }}