---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Ваша лицензия Spwig - Заказ #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Спасибо за покупку!
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
          Ваша покупка <strong>{{ product_name }}</strong> завершена. Ниже вы найдете ваш ключ лицензии и токен настройки, чтобы начать работу.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Сводка заказа
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Продукт: {{ product_name }}{% if includes_pos %} (включает POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Сумма: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Номер заказа: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          ВАШ КЛЮЧ ЛИЦЕНЗИИ
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Сохраните этот ключ — вам понадобится он для переустановки
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          ВАШ ТОКЕН НАСТРОЙКИ
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Используйте этот токен во время установки, чтобы активировать ваш магазин
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Начало работы
        </mj-text>
        <mj-text font-size="14px">
          1. Следуйте нашему руководству по настройке, чтобы установить Spwig на ваш сервер
        </mj-text>
        <mj-text font-size="14px">
          2. Введите ваш токен настройки, когда вас об этом попросят во время установки
        </mj-text>
        <mj-text font-size="14px">
          3. Ваш магазин будет автоматически активирован
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Создайте свой аккаунт
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Установите пароль, чтобы управлять своими лицензиями, получать доступ к загрузкам и получать обновления.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Важно:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Сохраните это письмо — оно содержит ваш ключ лицензии и токен настройки для будущего использования. Не делитесь этими учетными данными с другими.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Спасибо за покупку!

Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Ваша покупка {{ product_name }} завершена. Ниже вы найдете ваш ключ лицензии и токен настройки, чтобы начать работу.

Сводка заказа:
- Продукт: {{ product_name }}{% if includes_pos %} (включает POS){% endif %}
- Сумма: {{ price }}
- Номер заказа: {{ order_number }}

ВАШ КЛЮЧ ЛИЦЕНЗИИ:
{{ license_key }}
Сохраните этот ключ — вам понадобится он для переустановки.

ВАШ ТОКЕН НАСТРОЙКИ:
{{ setup_token }}
Используйте этот токен во время установки, чтобы активировать ваш магазин.

Начало работы:
1. Следуйте нашему руководству по настройке, чтобы установить Spwig на ваш сервер
2. Введите ваш токен настройки, когда вас об этом попросят во время установки
3. Ваш магазин будет автоматически активирован

Просмотр руководства по настройке: {{ setup_url }}
{% if activation_url %}
Создайте свой аккаунт:
Установите пароль, чтобы управлять своими лицензиями, получать доступ к загрузкам и получать обновления.
{{ activation_url }}
{% endif %}
ВАЖНО:
Сохраните это письмо — оно содержит ваш ключ лицензии и токен настройки для будущего использования. Не делитесь этими учетными данными с другими.

Нужна помощь? Свяжитесь с {{ support_email }}