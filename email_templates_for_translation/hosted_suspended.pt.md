---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Loja Suspensa - {{ store_name }}

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
          Conta Suspensa
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
          Sua loja <strong>{{ store_name }}</strong> foi suspensa devido a uma fatura pendente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          O Que Isso Significa
        </mj-text>
        <mj-text font-size="14px">
          Sua loja agora está em modo somente leitura — os clientes podem navegar, mas os pedidos estão desativados. Seus dados estão seguros e serão preservados por 30 dias.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Para restaurar o acesso completo, atualize seu método de pagamento e pague o saldo pendente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivar Sua Loja" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Conta Suspensa - {{ store_name }}

Olá {{ name|default:'there' }},

Sua loja {{ store_name }} foi suspensa devido a uma fatura pendente.

O Que Isso Significa:
Sua loja agora está em modo somente leitura — os clientes podem navegar, mas os pedidos estão desativados. Seus dados estão seguros e serão preservados por 30 dias.

Para restaurar o acesso completo, atualize seu método de pagamento e pague o saldo pendente.

Reactivar Sua Loja: https://spwig.com/account

Precisa de ajuda? Entre em contato com {{ support_email }}