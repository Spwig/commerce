---
template_type: subscription_canceled
category: Subscriptions
---

# Email Template: subscription_canceled

## Subject
❌ Ваша подписка на {{ plan_name }} отменена - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Мы сожалеем, что вы уходите
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Ваша подписка была отменена
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Cancellation Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px" border="2px solid {{ theme.color.text_muted|default:'#6b7280' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
                Сводка по отмене
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>План:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Отменено:</strong> {{ cancellation_date|date:"F d, Y" }}
              </mj-text>

              {% if access_until %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Доступ до:</strong> {{ access_until|date:"F d, Y" }}
              </mj-text>
              <mj-text font-size="14px" color="{{ theme.color.success|default:'#10b981' }}" padding="10px 0 5px 0">
                ✓ У вас все еще есть доступ к вашим преимуществам до {{ access_until|date:"F d, Y" }}
              </mj-text>
              {% else %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Статус:</strong> Отменено сразу
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What This Means Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Что это значит
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Вас больше не будут взимать с вас плату
        </mj-text>

        {% if access_until %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Вы можете продолжать пользоваться своими преимуществами до {{ access_until|date:"F d, Y" }}
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Ваш доступ завершился сразу
        </mj-text>
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Вы можете восстановить подписку в любое время
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Feedback Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          Мы хотели бы узнать ваше мнение, чтобы помочь нам улучшиться.
        </mj-text>
        <mj-button href="{{ feedback_url }}" background-color="{{ theme.color.text_muted|default:'#6b7280' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="14px" font-weight="600" border-radius="6px" padding="12px 28px">
          Поделиться отзывом
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Reactivate CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          Изменили мнение? Вы можете восстановить подписку в любое время.
        </mj-text>
        <mj-button href="{{ reactivate_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Восстановить подписку
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Нужна помощь? Свяжитесь с нами по адресу {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Мы сожалеем, что вы уходите

Ваша подписка была отменена

СВОДКА ПО ОТМЕНЕ:
План: {{ plan_name }}
Отменено: {{ cancellation_date|date:"F d, Y" }}
{% if access_until %}Доступ до: {{ access_until|date:"F d, Y" }}

✓ У вас все еще есть доступ к вашим преимуществам до {{ access_until|date:"F d, Y" }}
{% else %}Статус: Отменено сразу
{% endif %}

Что это значит:
• Вас больше не будут взимать с вас плату
{% if access_until %}• Вы можете продолжать пользоваться своими преимуществами до {{ access_until|date:"F d, Y" }}
{% else %}• Ваш доступ завершился сразу
{% endif %}• Вы можете восстановить подписку в любое время

Мы хотели бы узнать ваше мнение, чтобы помочь нам улучшиться.
Поделиться отзывом: {{ feedback_url }}

Изменили мнение? Вы можете восстановить подписку в любое время.
Восстановить подписку: {{ reactivate_url }}

Нужна помощь? Свяжитесь с нами по адресу {{ support_email }}

---
Powered by Spwig - https://spwig.com