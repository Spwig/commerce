---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Важно: Удаление данных через 7 дней - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Предупреждение об удалении данных
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Привет, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Ваш магазин <strong>{{ store_name }}</strong> и все связанные с ним данные будут навсегда удалены {{ termination_date }}. Это действие нельзя отменить.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что вы можете сделать
        </mj-text>
        <mj-text font-size="14px">
          Если вы хотите сохранить свои данные, экспортируйте их до этой даты или восстановите подписку, чтобы избежать удаления.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Восстановить подписку" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Предупреждение об удалении данных - {{ store_name }}

Привет, {{ name|default:'there' }},

Ваш магазин {{ store_name }} и все связанные с ним данные будут навсегда удалены {{ termination_date }}. Это действие нельзя отменить.

Что вы можете сделать:
Если вы хотите сохранить свои данные, экспортируйте их до этой даты или восстановите подписку, чтобы избежать удаления.

Восстановить подписку: https://spwig.com/account

Нужна помощь? Свяжитесь с {{ support_email }}