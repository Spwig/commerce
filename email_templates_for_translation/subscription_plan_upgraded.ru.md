---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ Ваш план подписки был обновлен!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ План обновлен!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Добро пожаловать в {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваш план подписки был успешно обновлен. Теперь у вас есть доступ ко всем преимуществам {{ new_plan_name }}!
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
              <strong>Обновлено:</strong> {{ upgrade_date }}<br/>
              <strong>Вступает в силу немедленно</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что нового:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Информация о платежах:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Новая цена:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Дата следующего платежа:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Предварительный платеж сегодня:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Сегодня вы были списаны {{ prorated_charge }} за оставшуюся часть вашего текущего периода оплаты.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть мою подписку
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вопросы? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Свяжитесь с поддержкой</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ПЛАН ОБНОВЛЕН!

Добро пожаловать в {{ new_plan_name }}

Здравствуйте, {{ customer_name }},

Ваш план подписки был успешно обновлен. Теперь у вас есть доступ ко всем преимуществам {{ new_plan_name }}!

ДЕТАЛИ ИЗМЕНЕНИЯ ПЛАНА:
- Предыдущий план: {{ old_plan_name }}
- Новый план: {{ new_plan_name }}
- Обновлено: {{ upgrade_date }}
- Вступает в силу немедленно

ЧТО НОВОГО:
{{ new_features }}

ИНФОРМАЦИЯ О ПЛАТЕЖАХ:
- Новая цена: {{ new_price }} / {{ billing_period }}
- Дата следующего платежа: {{ next_billing_date }}
{% if prorated_charge %}- Предварительный платеж сегодня: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Сегодня вы были списаны {{ prorated_charge }} за оставшуюся часть вашего текущего периода оплаты.
{% endif %}

Просмотреть мою подписку: {{ account_url }}
Вопросы? Свяжитесь с поддержкой: {{ support_url }}