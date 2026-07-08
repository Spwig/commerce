---
template_type: subscription_addon_added
category: Subscriptions
---

# Email Template: subscription_addon_added

## Subject
✓ {{ addon_name }} был добавлен в вашу подписку

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Дополнение активировано
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Дополнение успешно добавлено
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ addon_name }} был добавлен в вашу подписку {{ plan_name }} и теперь активирован!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали дополнения:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Дополнение:</strong> {{ addon_name }}<br/>
              <strong>Подписка:</strong> {{ plan_name }}<br/>
              <strong>Добавлено:</strong> {{ added_date }}<br/>
              <strong>Статус:</strong> Активно
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что вы получаете:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ addon_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Информация о платежах:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Цена дополнения:</strong> {{ addon_price }} / {{ billing_period }}<br/>
              <strong>Ваш план:</strong> {{ plan_price }} / {{ billing_period }}<br/>
              <strong>Новый итог:</strong> {{ new_total }} / {{ billing_period }}<br/>
              {% if prorated_charge %}<strong>Пропорциональная плата сегодня:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Сегодня вы были charged {{ prorated_charge }} за оставшуюся часть вашего текущего периода оплаты.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть мою подписку
        </mj-button>

        {% if addon_setup_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ addon_setup_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Настроить {{ addon_name }}
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ДОПОЛНЕНИЕ АКТИВИРОВАНО

Дополнение успешно добавлено

Здравствуйте, {{ customer_name }},

{{ addon_name }} был добавлен в вашу подписку {{ plan_name }} и теперь активирован!

ДЕТАЛИ ДОПОЛНЕНИЯ:
- Дополнение: {{ addon_name }}
- Подписка: {{ plan_name }}
- Добавлено: {{ added_date }}
- Статус: Активно

ЧТО ВЫ ПОЛУЧАЕТЕ:
{{ addon_description }}

ИНФОРМАЦИЯ О ПЛАТЕЖАХ:
- Цена дополнения: {{ addon_price }} / {{ billing_period }}
- Ваш план: {{ plan_price }} / {{ billing_period }}
- Новый итог: {{ new_total }} / {{ billing_period }}
{% if prorated_charge %}- Пропорциональная плата сегодня: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Сегодня вы были charged {{ prorated_charge }} за оставшуюся часть вашего текущего периода оплаты.
{% endif %}

Просмотреть мою подписку: {{ account_url }}
{% if addon_setup_url %}Настроить {{ addon_name }}: {{ addon_setup_url }}{% endif %}