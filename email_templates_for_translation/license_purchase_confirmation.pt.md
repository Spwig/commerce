---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Sua Licença Spwig - Pedido #{{ order_number }}

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
          Obrigado por sua compra!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text>
          Sua compra de <strong>{{ product_name }}</strong> foi concluída. Abaixo você encontrará sua chave de licença e token de configuração para começar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Resumo do Pedido
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Produto: {{ product_name }}{% if includes_pos %} (inclui POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Valor: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Número do Pedido: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          SUA CHAVE DE LICENÇA
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Salve esta chave - você precisará dela para reinstalação
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          SEU TOKEN DE CONFIGURAÇÃO
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Use este token durante a instalação para ativar sua loja
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Começando
        </mj-text>
        <mj-text font-size="14px">
          1. Siga nosso guia de configuração para instalar o Spwig em seu servidor
        </mj-text>
        <mj-text font-size="14px">
          2. Insira seu token de configuração quando solicitado durante a instalação
        </mj-text>
        <mj-text font-size="14px">
          3. Sua loja será ativada automaticamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Ver Guia de Configuração" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Crie sua Conta
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Defina uma senha para gerenciar suas licenças, acessar downloads e receber atualizações.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Crie sua Conta" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Importante:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Mantenha este e-mail seguro - ele contém sua chave de licença e token de configuração para referência futura. Não compartilhe essas credenciais com ninguém.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Obrigado por sua compra!

Pedido #{{ order_number }}

Olá {{ customer_name }},

Sua compra de {{ product_name }} foi concluída. Abaixo você encontrará sua chave de licença e token de configuração para começar.

Resumo do Pedido:
- Produto: {{ product_name }}{% if includes_pos %} (inclui POS){% endif %}
- Valor: {{ price }}
- Número do Pedido: {{ order_number }}

SUAS CHAVE DE LICENÇA:
{{ license_key }}
Salve esta chave - você precisará dela para reinstalação.

SEU TOKEN DE CONFIGURAÇÃO:
{{ setup_token }}
Use este token durante a instalação para ativar sua loja.

Começando:
1. Siga nosso guia de configuração para instalar o Spwig em seu servidor
2. Insira seu token de configuração quando solicitado durante a instalação
3. Sua loja será ativada automaticamente

Ver Guia de Configuração: {{ setup_url }}
{% if activation_url %}
Crie sua Conta:
Defina uma senha para gerenciar suas licenças, acessar downloads e receber atualizações.
{{ activation_url }}
{% endif %}
IMPORTANTE:
Mantenha este e-mail seguro - ele contém sua chave de licença e token de configuração para referência futura. Não compartilhe essas credenciais com ninguém.

Precisa de ajuda? Entre em contato com {{ support_email }}