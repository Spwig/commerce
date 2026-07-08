---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Ação Necessária - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Aviso de Suspensão
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Ação necessária para {{ store_name }}
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
          Seu pagamento para <strong>{{ plan_name }}</strong> está atrasado. Se não for resolvido até <strong>{{ grace_end_date }}</strong>, sua loja será colocada em modo somente leitura.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          O Que a Suspensão Significa
        </mj-text>
        <mj-text font-size="14px">
          Se sua loja for suspensa, ela permanecerá visível para os visitantes, mas você não poderá fazer alterações. Novos pedidos serão pausados até que o saldo pendente seja quitado.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Por favor, atualize seu método de pagamento para evitar qualquer interrupção em sua loja.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Atualizar Método de Pagamento" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Aviso de Suspensão - {{ store_name }}

Olá {{ name|default:'there' }},

Seu pagamento para {{ plan_name }} está atrasado. Se não for resolvido até {{ grace_end_date }}, sua loja será colocada em modo somente leitura.

O Que a Suspensão Significa:
Se sua loja for suspensa, ela permanecerá visível para os visitantes, mas você não poderá fazer alterações. Novos pedidos serão pausados até que o saldo pendente seja quitado.

Por favor, atualize seu método de pagamento para evitar qualquer interrupção em sua loja.

Atualizar Método de Pagamento: https://spwig.com/account

Precisa de ajuda? Entre em contato com {{ support_email }}