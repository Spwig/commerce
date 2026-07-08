---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Запрос на сброс пароля

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Запрос на сброс пароля
        </mj-text>
        <mj-text>
          Мы получили запрос на сброс вашего пароля. Нажмите на кнопку ниже, чтобы сбросить его.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Сбросить пароль
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Если вы не запрашивали это, вы можете безопасно игнорировать это письмо.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Этот ссылка истекает через {{ expiry_hours }} часов.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Запрос на сброс пароля

Мы получили запрос на сброс вашего пароля. Нажмите на ссылку ниже, чтобы сбросить его.

{{ reset_url }}

Если вы не запрашивали это, вы можете безопасно игнорировать это письмо.
Эта ссылка истечет через {{ expiry_hours }} часов.