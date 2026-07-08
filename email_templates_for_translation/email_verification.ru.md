---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
Подтвердите свой адрес электронной почты

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Подтвердите свой адрес электронной почты
        </mj-text>
        <mj-text>
          Пожалуйста, подтвердите свой адрес электронной почты, нажав на кнопку ниже.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Подтвердить адрес электронной почты
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Этот ссылка истечет через {{ expiry_hours }} часов.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Подтвердите свой адрес электронной почты

Пожалуйста, подтвердите свой адрес электронной почты, нажав на ссылку ниже.

{{ verification_url }}

Этот ссылка истечет через {{ expiry_hours }} часов.