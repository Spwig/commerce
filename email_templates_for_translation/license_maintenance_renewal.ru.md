---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Обновление технической поддержки - Заказ #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Обновление технической поддержки!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Заказ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Здравствуйте, {{ customer_name }},
        </mj-text>
        <mj-text>
          Ваша подписка на техническую поддержку Spwig успешно обновлена. Вы продолжите получать обновления платформы, исправления безопасности и новые функции.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Сводка обновления
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ключ лицензии: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Срок действия технической поддержки: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Номер заказа: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что входит в пакет
        </mj-text>
        <mj-text font-size="14px">
          Ваша активная техническая поддержка предоставляет вам доступ к:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Обновлениям функций и улучшениям платформы
        </mj-text>
        <mj-text font-size="14px">
          - Исправлениям безопасности и устранению ошибок
        </mj-text>
        <mj-text font-size="14px">
          - Новым выпускам компонентов через сервер обновлений
        </mj-text>
        <mj-text font-size="14px">
          - Технической поддержке
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Нет действий, необходимых с вашей стороны. Обновления будут продолжать поступать через систему обновления компонентов в вашем административном панели.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Обновление технической поддержки!

Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Ваша подписка на техническую поддержку Spwig успешно обновлена. Вы продолжите получать обновления платформы, исправления безопасности и новые функции.

Сводка обновления:
- Ключ лицензии: {{ license_key }}
- Срок действия технической поддержки: {{ renewal_expires_at }}
- Номер заказа: {{ order_number }}

Что входит в пакет:
- Обновления функций и улучшения платформы
- Исправления безопасности и устранение ошибок
- Новые выпуски компонентов через сервер обновлений
- Техническая поддержка

Нет действий, необходимых с вашей стороны. Обновления будут продолжать поступать через систему обновления компонентов в вашем административном панели.

Нужна помощь? Свяжитесь с {{ support_email }}