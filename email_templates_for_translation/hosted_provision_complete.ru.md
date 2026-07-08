---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Ваш магазин готов - {{ store_name }}

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
          Ваш магазин уже работает!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} готов к использованию
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Привет, {{ name|default:'there' }}!
        </mj-text>
        <mj-text>
          Великолепные новости! Ваш магазин Spwig <strong>{{ store_name }}</strong> создан и теперь работает. Вы можете сразу приступить к настройке товаров, брендинга и методов оплаты.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Детали вашего магазина
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL магазина: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Панель администратора: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Регион: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Быстрый старт
        </mj-text>
        <mj-text font-size="14px">
          1. Войдите в панель администратора, используя email и пароль, которые вы указали при оформлении заказа
        </mj-text>
        <mj-text font-size="14px">
          2. Добавьте логотип и брендинг магазина в разделе Дизайн > Настройки темы
        </mj-text>
        <mj-text font-size="14px">
          3. Добавьте первые товары в разделе Каталог > Товары
        </mj-text>
        <mj-text font-size="14px">
          4. Настройте провайдера оплаты в разделе Настройки > Провайдеры оплаты
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Перейти в панель администратора" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Ваш магазин уже работает!

{{ store_name }} готов к использованию.

Привет, {{ name|default:'there' }}!

Великолепные новости! Ваш магазин Spwig {{ store_name }} создан и теперь работает. Вы можете сразу приступить к настройке товаров, брендинга и методов оплаты.

Детали вашего магазина:
- URL магазина: {{ store_url }}
- Панель администратора: {{ admin_url }}
- Регион: {{ region }}

Быстрый старт:
1. Войдите в панель администратора, используя email и пароль, которые вы указали при оформлении заказа
2. Добавьте логотип и брендинг магазина в разделе Дизайн > Настройки темы
3. Добавьте первые товары в разделе Каталог > Товары
4. Настройте провайдера оплаты в разделе Настройки > Провайдеры оплаты

Перейти в панель администратора: {{ admin_url }}

Нужна помощь? Свяжитесь с {{ support_email }}