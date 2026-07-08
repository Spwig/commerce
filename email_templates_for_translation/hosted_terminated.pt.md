---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Loja Removida - {{ store_name }}

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
          Loja Removida
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
          Sua loja <strong>{{ store_name }}</strong> foi removida permanentemente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Backup de Dados
        </mj-text>
        <mj-text font-size="14px">
          Um backup dos seus dados estará disponível por 90 dias mediante solicitação. Entre em contato com <strong>support@spwig.com</strong> se precisar de um exportação de dados.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Obrigado por ser um cliente Spwig. Esperamos vê-lo novamente no futuro.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Loja Removida - {{ store_name }}

Olá {{ name|default:'there' }},

Sua loja {{ store_name }} foi removida permanentemente.

Backup de Dados:
Um backup dos seus dados estará disponível por 90 dias mediante solicitação. Entre em contato com support@spwig.com se precisar de um exportação de dados.

Obrigado por ser um cliente Spwig. Esperamos vê-lo novamente no futuro.

Precisa de ajuda? Entre em contato com {{ support_email }}