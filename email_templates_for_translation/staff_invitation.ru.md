---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Вы были приглашены присоединиться к {{ store_name }}

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
          Приглашение сотрудника
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Вас пригласили присоединиться к {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Привет, {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} пригласил вас присоединиться к <strong>{{ store_name }}</strong> в качестве сотрудника. Вы сможете помогать управлять магазином через панель администратора.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Принять приглашение" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Это приглашение истекает {{ expires_at|date:"N j, Y" }}. Если вы не ожидали это приглашение, вы можете безопасно игнорировать это письмо.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Вы были приглашены присоединиться к {{ store_name }}

Привет, {{ first_name }},

{{ invited_by }} пригласил вас присоединиться к {{ store_name }} в качестве сотрудника. Вы сможете помогать управлять магазином через панель администратора.

Принять приглашение: {{ invitation_url }}

Это приглашение истекает {{ expires_at|date:"N j, Y" }}. Если вы не ожидали это приглашение, вы можете безопасно игнорировать это письмо.

Нужна помощь? Свяжитесь с {{ support_email }}