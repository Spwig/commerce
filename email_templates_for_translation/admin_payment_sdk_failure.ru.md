---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Проблема с провайдером оплаты - SDK {{ provider_name }} не загрузился

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Проблема с провайдером оплаты
        </mj-text>
        <mj-text>
          SDK для оплаты {{ provider_name }} не загрузился для клиента во время оформления заказа. Это может указывать на сбой в работе провайдера.
        </mj-text>
        <mj-text>
          <strong>Провайдер:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Тип ошибки:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Время:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Количество сбоев (за последний час):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Это уведомление ограничено по частоте: одно на провайдера в час. Если проблема сохраняется, проверьте панель управления провайдера или обратитесь в их поддержку.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Просмотр настроек оплаты
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Проблема с провайдером оплаты

SDK для оплаты {{ provider_name }} не загрузился для клиента во время оформления заказа. Это может указывать на сбой в работе провайдера.

Провайдер: {{ provider_name }}
Тип ошибки: {{ error_type }}
Время: {{ timestamp }}
Количество сбоев (за последний час): {{ failure_count }}

Это уведомление ограничено по частоте: одно на провайдера в час. Если проблема сохраняется, проверьте панель управления провайдера или обратитесь в их поддержку.

Просмотр настроек оплаты: {{ admin_url }}