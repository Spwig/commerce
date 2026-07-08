---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Магазин удалён - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Магазин удалён
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
          Ваш магазин <strong>{{ store_name }}</strong> был永久но удалён.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Резервная копия данных
        </mj-text>
        <mj-text font-size="14px">
          Резервная копия ваших данных будет доступна в течение 90 дней по запросу. Обратитесь по адресу <strong>support@spwig.com</strong>, если вам нужна экспорт данных.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Спасибо, что являетесь клиентом Spwig. Надеемся увидеть вас снова в будущем.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Магазин удалён - {{ store_name }}

Привет, {{ name|default:'there' }},

Ваш магазин {{ store_name }} был永久но удалён.

Резервная копия данных:
Резервная копия ваших данных будет доступна в течение 90 дней по запросу. Обратитесь по адресу support@spwig.com, если вам нужна экспорт данных.

Спасибо, что являетесь клиентом Spwig. Надеемся увидеть вас снова в будущем.

Нужна помощь? Обратитесь по адресу {{ support_email }}