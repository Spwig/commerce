---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Ссылка для загрузки истекла - Заказ #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Ссылка для загрузки истекла
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Здравствуйте, {{ customer_name }},
        </mj-text>
        <mj-text>
          Ссылка для загрузки <strong>{{ product_name }}</strong> из заказа #{{ order_number }} истекла.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Ссылки для загрузки истекают через {{ expiration_days }} дней после покупки по соображениям безопасности.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Нужна новая ссылка для загрузки?
        </mj-text>
        <mj-text>
          Вы можете запросить новую ссылку для загрузки, войдя в свой аккаунт или связавшись с нашей службой поддержки.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Перейти в мой аккаунт
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Вопросы? Свяжитесь с {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ссылка для загрузки истекла

Здравствуйте, {{ customer_name }},

Ссылка для загрузки {{ product_name }} из заказа #{{ order_number }} истекла.

Ссылки для загрузки истекают {{ expiration_days }} дней после покупки по соображениям безопасности.

Нужна новая ссылка для загрузки?
Вы можете запросить новую ссылку для загрузки, войдя в свой аккаунт или связавшись с нашей службой поддержки.

Перейти в мой аккаунт: {{ account_url }}

Вопросы? Свяжитесь с {{ support_email }}