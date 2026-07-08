---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Создайте свой аккаунт на {{ site_name }}

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
          Вас пригласили!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Создайте свой аккаунт на {{ site_name }}
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
          Мы заметили, что вы покупали у нас как гость. Создайте полный аккаунт, чтобы получить преимущества, такие как отслеживание заказов, быстрый checkout и эксклюзивные предложения.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ваша история покупок
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Общее количество заказов: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Общая сумма: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Зачем создавать аккаунт?
        </mj-text>
        <mj-text font-size="14px">
          - Отслеживайте свои заказы и просматривайте историю заказов
        </mj-text>
        <mj-text font-size="14px">
          - Быстрый checkout с сохраненными данными
        </mj-text>
        <mj-text font-size="14px">
          - Управляйте своими адресами и предпочтениями
        </mj-text>
        <mj-text font-size="14px">
          - Получайте доступ к эксклюзивным предложениям и акциям
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Этот ссылка позволит вам установить пароль для вашего аккаунта. Ваша существующая история заказов будет сохранена.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Вас пригласили создать аккаунт!

Здравствуйте, {{ customer_name }},

Мы заметили, что вы покупали у нас как гость. Создайте полный аккаунт, чтобы получить преимущества, такие как отслеживание заказов, быстрый checkout и эксклюзивные предложения.

Ваша история покупок:
- Общее количество заказов: {{ total_orders }}
- Общая сумма: {{ total_spent }}

Зачем создавать аккаунт?
- Отслеживайте свои заказы и просматривайте историю заказов
- Быстрый checkout с сохраненными данными
- Управляйте своими адресами и предпочтениями
- Получайте доступ к эксклюзивным предложениям и акциям

Создайте свой аккаунт: {{ activation_url }}

Этот ссылка позволит вам установить пароль для вашего аккаунта. Ваша существующая история заказов будет сохранена.

Нужна помощь? Свяжитесь с {{ support_email }}