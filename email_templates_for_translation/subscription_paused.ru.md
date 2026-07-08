---
template_type: subscription_paused
category: Subscriptions
---

# Email Template: subscription_paused

## Subject
⏸️ Ваша подписка на {{ plan_name }} приостановлена - {{ shop_name }}

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
          ⏸️ Подписка приостановлена
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Ваша подписка на {{ plan_name }} теперь приостановлена
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Pause Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#9a3412" align="center" padding-bottom="15px">
                Информация о приостановке
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>План:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Приостановлено:</strong> {{ pause_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Статус:</strong> Приостановлено
              </mj-text>
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
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">•</span>
          Оплата подписки приостановлена — вы не будете платить
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">•</span>
          Доступ к преимуществам подписки может быть ограничен
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">•</span>
          Вы можете возобновить подписку в любое время
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ resume_subscription_url }}" background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Возобновить подписку
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ manage_subscription_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            Управление подпиской
          </a>
        </mj-text>
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
⏸️ Подписка приостановлена

Ваша подписка на {{ plan_name }} теперь приостановлена

Информация о приостановке:
План: {{ plan_name }}
Приостановлено: {{ pause_date|date:"F d, Y" }}
Статус: Приостановлено

Что это значит:
• Оплата подписки приостановлена — вы не будете платить
• Доступ к преимуществам подписки может быть ограничен
• Вы можете возобновить подписку в любое время

Возобновить подписку: {{ resume_subscription_url }}
Управление подпиской: {{ manage_subscription_url }}

Нужна помощь? Свяжитесь с нами по адресу {{ support_email }}

---
Powered by Spwig - https://spwig.com