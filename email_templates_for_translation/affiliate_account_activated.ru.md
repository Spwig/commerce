---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Добро пожаловать обратно! Счет восстановлен

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 Счет восстановлен!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Добро пожаловать обратно!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Ваш аккаунт аффилиата снова активен
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Здравствуйте {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Хорошие новости! Ваш аккаунт аффилиата с {{ shop_name }} был восстановлен.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Вы можете возобновить продвижение наших продуктов и получение комиссионных сразу же.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Войти в панель аффилиата
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Вопросы? <a href="mailto:{{ support_email }}" style="color: #007bff;">Связаться с поддержкой</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Добро пожаловать обратно! Счет восстановлен

Здравствуйте {{ affiliate_name }},

Хорошие новости! Ваш аккаунт аффилиата с {{ shop_name }} был восстановлен.

Вы можете возобновить продвижение наших продуктов и получение комиссионных сразу же.

Войти в панель аффилиата: {{ portal_url }}

{{ shop_name }}
Вопросы? Связаться с {{ support_email }}

