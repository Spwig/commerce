---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Требуется действие - проблема с настройкой магазина {{ store_name }}

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Проблема с настройкой магазина
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
          Здравствуйте, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Мы столкнулись с проблемой при настройке вашего магазина <strong>{{ store_name }}</strong>. Наша команда уже уведомлена и работает над этим.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          Что произошло
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что будет дальше?
        </mj-text>
        <mj-text font-size="14px">
          Наша служба поддержки автоматически уведомлена о данной проблеме. Вам не нужно предпринимать никаких действий — мы свяжемся с вами, как только проблема будет решена.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Если у вас есть какие-либо вопросы в ближайшее время, пожалуйста, не стесняйтесь обращаться к нам.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Проблема с настройкой магазина - {{ store_name }}

Здравствуйте, {{ name|default:'there' }},

Мы столкнулись с проблемой при настройке вашего магазина {{ store_name }}. Наша команда уже уведомлена и работает над этим.

Что произошло:
{{ provision_error }}

Что будет дальше?
Наша служба поддержки автоматически уведомлена о данной проблеме. Вам не нужно предпринимать никаких действий — мы свяжемся с вами, как только проблема будет решена.

Если у вас есть какие-либо вопросы в ближайшее время, пожалуйста, не стесняйтесь обращаться к нам.

Нужна помощь? Свяжитесь с {{ support_email }}