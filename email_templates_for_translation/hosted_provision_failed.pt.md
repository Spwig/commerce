---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Ação Necessária - Problema na Configuração da Loja {{ store_name }}

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
          Problema na Configuração da Loja
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
          Nós encontramos um problema ao configurar sua loja <strong>{{ store_name }}</strong>. Nossa equipe foi notificada e está investigando.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          O que aconteceu
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
          O que acontece em seguida?
        </mj-text>
        <mj-text font-size="14px">
          Nossa equipe de suporte foi automaticamente notificada sobre esse problema. Você não precisa tomar nenhuma ação - entraremos em contato com você assim que o problema for resolvido.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Se você tiver alguma dúvida no meio tempo, não hesite em nos contatar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Problema na Configuração da Loja - {{ store_name }}

Olá {{ name|default:'there' }},

Nós encontramos um problema ao configurar sua loja {{ store_name }}. Nossa equipe foi notificada e está investigando.

O que aconteceu:
{{ provision_error }}

O que acontece em seguida?
Nossa equipe de suporte foi automaticamente notificada sobre esse problema. Você não precisa tomar nenhuma ação - entraremos em contato com você assim que o problema for resolvido.

Se você tiver alguma dúvida no meio tempo, não hesite em nos contatar.

Precisa de ajuda? Entre em contato com {{ support_email }}