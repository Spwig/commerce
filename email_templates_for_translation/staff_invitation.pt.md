---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Você foi convidado para se juntar a {{ store_name }}

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
          Convite para Equipe
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Você foi convidado para se juntar a {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} convidou você para se juntar a <strong>{{ store_name }}</strong> como membro da equipe. Você poderá ajudar a gerenciar a loja a partir do painel de administração.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Aceitar Convite" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Este convite expira em {{ expires_at|date:"N j, Y" }}. Se você não esperava esse convite, pode ignorar este e-mail com segurança.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Você foi convidado para se juntar a {{ store_name }}

Olá {{ first_name }},

{{ invited_by }} convidou você para se juntar a {{ store_name }} como membro da equipe. Você poderá ajudar a gerenciar a loja a partir do painel de administração.

Aceite seu convite: {{ invitation_url }}

Este convite expira em {{ expires_at|date:"N j, Y" }}. Se você não esperava esse convite, pode ignorar este e-mail com segurança.

Precisa de ajuda? Entre em contato com {{ support_email }}