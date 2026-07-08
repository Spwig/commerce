---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Пожалуйста, подтвердите вашу подписку на {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Подтвердите подписку
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо, что подписались на {{ blog_name }}! Чтобы завершить подписку и начать получать обновления, пожалуйста, подтвердите свой адрес электронной почты.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Подтвердить подписку
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Не можете нажать кнопку? Скопируйте и вставьте эту ссылку в браузер:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Почему нужно подтверждать?</strong><br/>
          Проверка электронной почты помогает нам убедиться, что вы хотите получать обновления и предотвращает спам. Ваша приватность и почта важны для нас.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Не подписывались? Вы можете безопасно игнорировать это письмо.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ПОДТВЕРДИТЕ СВОЮ ПОДПИСКУ

Здравствуйте, {{ subscriber_name }},

Спасибо, что подписались на {{ blog_name }}! Чтобы завершить подписку и начать получать обновления, пожалуйста, подтвердите свой адрес электронной почты.

Подтвердите подписку: {{ confirmation_url }}

ПОЧЕМУ НЕОБХОДИМО ПОДТВЕРЖДЕНИЕ?
Проверка электронной почты помогает нам убедиться, что вы хотите получать обновления и предотвращает спам. Ваша приватность и почта важны для нас.

Не подписывались? Вы можете безопасно игнорировать это письмо.