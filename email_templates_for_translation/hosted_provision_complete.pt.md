---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Sua Loja Está Pronta - {{ store_name }}

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
          Sua Loja Está Ativa!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} está pronta para você
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
          Boas notícias! Sua loja Spwig <strong>{{ store_name }}</strong> foi provisionada e agora está ativa. Você pode começar a configurar seus produtos, branding e métodos de pagamento imediatamente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalhes da Sua Loja
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL da Loja: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Painel de Administração: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Região: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Início Rápido
        </mj-text>
        <mj-text font-size="14px">
          1. Faça login no seu painel de administração usando o e-mail e senha que você configurou durante o checkout
        </mj-text>
        <mj-text font-size="14px">
          2. Adicione o logotipo e branding da sua loja em Design > Configurações do Tema
        </mj-text>
        <mj-text font-size="14px">
          3. Adicione seus primeiros produtos em Catálogo > Produtos
        </mj-text>
        <mj-text font-size="14px">
          4. Configure um provedor de pagamento em Configurações > Provedores de Pagamento
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Sua Loja Está Ativa!

{{ store_name }} está pronta para você.

Olá {{ name|default:'there' }},

Boas notícias! Sua loja Spwig {{ store_name }} foi provisionada e agora está ativa. Você pode começar a configurar seus produtos, branding e métodos de pagamento imediatamente.

Detalhes da Sua Loja:
- URL da Loja: {{ store_url }}
- Painel de Administração: {{ admin_url }}
- Região: {{ region }}

Início Rápido:
1. Faça login no seu painel de administração usando o e-mail e senha que você configurou durante o checkout
2. Adicione o logotipo e branding da sua loja em Design > Configurações do Tema
3. Adicione seus primeiros produtos em Catálogo > Produtos
4. Configure um provedor de pagamento em Configurações > Provedores de Pagamento

Vá para o Painel de Administração: {{ admin_url }}

Precisa de ajuda? Entre em contato com {{ support_email }}