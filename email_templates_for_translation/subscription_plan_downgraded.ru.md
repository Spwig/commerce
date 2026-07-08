---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
Ваш план подписки был изменен на {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          План изменен
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обновление плана подписки
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваш план подписки был изменен на {{ new_plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали изменения плана:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Предыдущий план:</strong> {{ old_plan_name }}<br/>
              <strong>Новый план:</strong> {{ new_plan_name }}<br/>
              <strong>Изменен:</strong> {{ downgrade_date }}<br/>
              <strong>Действует с:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что изменилось:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Функции, которые больше недоступны:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Информация о платежах:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Новая стоимость:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Дата вступления в силу:</strong> {{ effective_date }}<br/>
              <strong>Дата следующего платежа:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Кредит в размере {{ credit_amount }} был зачислен на ваш аккаунт за неиспользованную часть вашего предыдущего плана.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Поменяли мнение?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          Вы можете обновиться обратно до {{ old_plan_name }} в любое время.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Обновить план
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть мою подписку
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ПЛАН ИЗМЕНЕН

Обновление плана подписки

Здравствуйте {{ customer_name }},

Ваш план подписки был изменен на {{ new_plan_name }}.

ДЕТАЛИ ИЗМЕНЕНИЯ ПЛАНА:
- Предыдущий план: {{ old_plan_name }}
- Новый план: {{ new_plan_name }}
- Изменен: {{ downgrade_date }}
- Действует с: {{ effective_date }}

ЧТО ИЗМЕНИЛОСЬ:
{{ plan_changes }}

{% if features_lost %}
ФУНКЦИИ, КОТОРЫЕ БОЛЬШЕ НЕ ДОСТУПНЫ:
{{ features_lost }}
{% endif %}

ИНФОРМАЦИЯ О ПЛАТЕЖАХ:
- Новая стоимость: {{ new_price }} / {{ billing_period }}
- Дата вступления в силу: {{ effective_date }}
- Дата следующего платежа: {{ next_billing_date }}

{% if credit_applied %}
💰 Кредит в размере {{ credit_amount }} был зачислен на ваш аккаунт за неиспользованную часть вашего предыдущего плана.
{% endif %}

ПОМЕНИЛИ МНЕНИЕ?
Вы можете обновиться обратно до {{ old_plan_name }} в любое время.

Обновить план: {{ upgrade_url }}
Просмотреть мою подписку: {{ account_url }}