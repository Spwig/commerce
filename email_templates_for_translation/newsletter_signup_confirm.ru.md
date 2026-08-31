---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Подтвердите подписку на {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Подтвердите подписку
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо, что подписались, чтобы получать новости от {{ store_name }}! Пожалуйста, подтвердите адрес электронной почты, чтобы начать получать наши обновления и предложения.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Подтвердите подписку
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Не можете нажать на кнопку? Скопируйте и вставьте эту ссылку в браузер:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Зачем подтверждать?</strong><br/>
          Подтверждение электронной почты помогает нам убедиться, что вы действительно хотите получать наши обновления, и держит ваш ящик свободным от спама.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Не регистрировались? Вы можете спокойно проигнорировать это письмо.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Подтвердите подписку на {{ store_name }}

Спасибо, что подписались, чтобы получать новости от {{ store_name }}! Пожалуйста, подтвердите адрес электронной почты, чтобы начать получать наши обновления и предложения:

{{ confirmation_url }}

Подтверждение электронной почты помогает нам убедиться, что вы действительно хотите получать наши обновления, и держит ваш ящик свободным от спама.

Не регистрировались? Вы можете спокойно проигнорировать это письмо.