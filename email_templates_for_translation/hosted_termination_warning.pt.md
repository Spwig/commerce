---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Importante: Exclusão de Dados em 7 Dias - {{ store_name }}

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
          Aviso de Exclusão de Dados
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
          Olá {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Sua loja <strong>{{ store_name }}</strong> e todos os dados associados serão excluídos permanentemente em <strong>{{ termination_date }}</strong>. Esta ação não pode ser desfeita.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          O Que Você Pode Fazer
        </mj-text>
        <mj-text font-size="14px">
          Se quiser manter seus dados, por favor, exporte-os antes dessa data ou reative sua assinatura para evitar a exclusão.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Aviso de Exclusão de Dados - {{ store_name }}

Olá {{ name|default:'there' }},

Sua loja {{ store_name }} e todos os dados associados serão excluídos permanentemente em {{ termination_date }}. Esta ação não pode ser desfeita.

O Que Você Pode Fazer:
Se quiser manter seus dados, por favor, exporte-os antes dessa data ou reative sua assinatura para evitar a exclusão.

Reactivate Subscription: https://spwig.com/account

Precisa de ajuda? Entre em contato com {{ support_email }}