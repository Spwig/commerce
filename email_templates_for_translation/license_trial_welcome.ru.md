---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Добро пожаловать в Spwig - Ваш бесплатный пробный период на {{ trial_days }} дней

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Добро пожаловать в Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Ваш бесплатный пробный период на {{ trial_days }} дней готов
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
          Спасибо, что попробовали <strong>{{ product_name }}</strong>! Ваш пробный период активирован, и у вас есть <strong>{{ trial_days }} дней</strong>, чтобы изучить всё, что предлагает Spwig{% if includes_pos %}, включая нашу систему Point of Sale{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          ВАШ ТОКЕН УСТАНОВКИ
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Используйте этот токен во время установки, чтобы активировать ваш пробный магазин
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
          3. Начните создание своего онлайн-магазина!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что входит в ваш пробный период
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Полный доступ ко всем основным функциям на {{ trial_days }} дней
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Каталог товаров, заказы и управление клиентами
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Настройка темы и конструктор страниц
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Интеграции с платежными и транспортными провайдерами
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Система Point of Sale (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ваш пробный период истечет через {{ trial_days }} дней. Когда вы будете готовы, обновитесь до полной лицензии, чтобы продолжить работу вашего магазина без потери данных.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Добро пожаловать в Spwig!
Ваш бесплатный пробный период на {{ trial_days }} дней готов.

Здравствуйте, {{ customer_name }},

Спасибо, что попробовали {{ product_name }}! Ваш пробный период активирован, и у вас есть {{ trial_days }} дней, чтобы изучить всё, что предлагает Spwig{% if includes_pos %}, включая нашу систему Point of Sale{% endif %}.

ВАШ ТОКЕН УСТАНОВКИ:
{{ setup_token }}
Используйте этот токен во время установки, чтобы активировать ваш пробный магазин.

Начало работы:
1. Следуйте нашему руководству по настройке, чтобы установить Spwig на ваш сервер
2. Введите ваш токен настройки, когда вас об этом попросят во время установки
3. Начните создание своего онлайн-магазина!

Просмотр руководства по настройке: {{ setup_url }}

Что входит в ваш пробный период:
- Полный доступ ко всем основным функциям на {{ trial_days }} дней
- Каталог товаров, заказы и управление клиентами
- Настройка темы и конструктор страниц
- Интеграции с платежными и транспортными провайдерами
{% if includes_pos %}- Система Point of Sale (POS){% endif %}

Ваш пробный период истечет через {{ trial_days }} дней. Когда вы будете готовы, обновитесь до полной лицензии, чтобы продолжить работу вашего магазина без потери данных.

Нужна помощь? Свяжитесь с {{ support_email }}