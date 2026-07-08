---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
Atualização de Faturamento - {{ store_name }}

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
          Atualização de Faturamento
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
          Olá,
        </mj-text>
        <mj-text>
          O intervalo de faturamento do seu plano <strong>{{ plan_name }}</strong> na <strong>{{ store_name }}</strong> foi atualizado.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalhes de Faturamento
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plano: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Intervalo de Faturamento Anterior: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Novo Intervalo de Faturamento: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Próxima Data de Faturamento: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Sua assinatura permanece ativa. Você pode gerenciar suas preferências de faturamento a qualquer momento a partir da sua conta.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Gerenciar Assinatura" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Atualização de Faturamento - {{ store_name }}

Olá,

O intervalo de faturamento do seu plano {{ plan_name }} na {{ store_name }} foi atualizado.

Detalhes de Faturamento:
- Plano: {{ plan_name }}
- Intervalo de Faturamento Anterior: {{ old_interval }}
- Novo Intervalo de Faturamento: {{ new_interval }}
- Próxima Data de Faturamento: {{ next_billing_date }}

Sua assinatura permanece ativa. Você pode gerenciar suas preferências de faturamento a qualquer momento a partir da sua conta.

Gerenciar Assinatura: https://spwig.com/account

Precisa de ajuda? Entre em contato com {{ support_email }}