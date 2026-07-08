---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 С днём рождения {{ customer_name }}! Вот особенный подарок от {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          С днём рождения!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          С днём рождения, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Чтобы отметить ваш особенный день, мы добавили {{ bonus_points }} бонусных баллов в ваш лояльностный счёт!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Ваш подарок на день рождения
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Баллов
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Добавлено в ваш аккаунт!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваш лояльностный счёт:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Баланс баллов:</strong> {{ total_points }} баллов<br/>
          <strong>Текущий уровень:</strong> {{ loyalty_tier }}<br/>
          <strong>Бонус на день рождения:</strong> +{{ bonus_points }} баллов
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Начать покупки и использовать баллы
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Пусть ваш день рождения будет волшебным! 🎉<br/>
          - Команда {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 С ДНЕМ РОЖДЕНИЯ!

С днём рождения, {{ customer_name }}!

Чтобы отметить ваш особенный день, мы добавили {{ bonus_points }} бонусных баллов в ваш лояльностный счёт!

ВАШ ПОДАРОК НА ДЕНЬ РОЖДЕНИЯ:
{{ bonus_points }} Баллов
Добавлено в ваш аккаунт!

ВАШ ЛОЯЛЬНОСТНЫЙ СЧЁТ:
- Баланс баллов: {{ total_points }} баллов
- Текущий уровень: {{ loyalty_tier }}
- Бонус на день рождения: +{{ bonus_points }} баллов

Начать покупки и использовать баллы: {{ shop_url }}

Пусть ваш день рождения будет волшебным! 🎉
- Команда {{ shop_name }}