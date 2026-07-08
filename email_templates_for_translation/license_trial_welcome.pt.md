---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Bem-vindo ao Spwig - Seu teste gratuito de {{ trial_days }} dias

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Bem-vindo ao Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Seu teste gratuito de {{ trial_days }} dias está pronto
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
          Obrigado por experimentar <strong>{{ product_name }}</strong>! Seu teste foi ativado e você tem <strong>{{ trial_days }} dias</strong> para explorar tudo o que o Spwig tem a oferecer{% if includes_pos %}, incluindo nosso sistema de Ponto de Venda{% endif %}.
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
          Use este token durante a instalação para ativar sua loja de teste
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
          3. Comece a construir sua loja online!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Ver Guia de Configuração" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          O que está incluído no seu teste
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Acesso completo a todas as funcionalidades principais por {{ trial_days }} dias
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Catálogo de produtos, pedidos e gerenciamento de clientes
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Personalização de tema e construtor de páginas
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Integrações com provedores de pagamento e envio
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sistema de Ponto de Venda (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Seu teste expirará em {{ trial_days }} dias. Quando estiver pronto, atualize para uma licença completa para continuar a operar sua loja sem perda de dados.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bem-vindo ao Spwig!
Seu teste gratuito de {{ trial_days }} dias está pronto.

Olá {{ customer_name }},

Obrigado por experimentar {{ product_name }}! Seu teste foi ativado e você tem {{ trial_days }} dias para explorar tudo o que o Spwig tem a oferecer{% if includes_pos %}, incluindo nosso sistema de Ponto de Venda{% endif %}.

SEU TOKEN DE CONFIGURAÇÃO:
{{ setup_token }}
Use este token durante a instalação para ativar sua loja de teste.

Começando:
1. Siga nosso guia de configuração para instalar o Spwig em seu servidor
2. Insira seu token de configuração quando solicitado durante a instalação
3. Comece a construir sua loja online!

Ver Guia de Configuração: {{ setup_url }}

O que está incluído no seu teste:
- Acesso completo a todas as funcionalidades principais por {{ trial_days }} dias
- Catálogo de produtos, pedidos e gerenciamento de clientes
- Personalização de tema e construtor de páginas
- Integrações com provedores de pagamento e envio
{% if includes_pos %}- Sistema de Ponto de Venda (POS){% endif %}

Seu teste expirará em {{ trial_days }} dias. Quando estiver pronto, atualize para uma licença completa para continuar a operar sua loja sem perda de dados.

Precisa de ajuda? Entre em contato com {{ support_email }}