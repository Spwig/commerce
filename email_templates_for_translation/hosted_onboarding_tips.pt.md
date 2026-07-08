---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Dicas para Obter o Máximo de {{ store_name }}

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
          Dicas para Começar
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Obtenha o máximo da sua loja Spwig
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
          Agora que <strong>{{ store_name }}</strong> está em funcionamento, aqui estão algumas dicas para ajudá-lo a obter o máximo da sua loja.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Personalize o Seu Visual
        </mj-text>
        <mj-text font-size="14px">
          Visite <strong>Design > Configurações do Tema</strong> para escolher um tema, carregar seu logotipo e definir as cores da sua marca. A sua loja atualiza instantaneamente, então você pode visualizar as alterações em tempo real.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Adicione Seus Produtos
        </mj-text>
        <mj-text font-size="14px">
          Vá para <strong>Catálogo > Produtos</strong> para começar a adicionar seus itens. Você pode criar variantes de produto (tamanho, cor), definir preços, gerenciar estoque e carregar imagens de alta qualidade.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Pagamentos
        </mj-text>
        <mj-text font-size="14px">
          Vá para <strong>Configurações > Provedores de Pagamento</strong> para conectar o Stripe, PayPal ou outro método de pagamento. Você pode habilitar múltiplos provedores para que seus clientes paguem da maneira que preferirem.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Envios
        </mj-text>
        <mj-text font-size="14px">
          Em <strong>Configurações > Envios</strong>, configure suas zonas e taxas de envio. Você pode criar regras de envio fixo, baseadas no peso ou gratuitas para diferentes regiões.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Melhore Seu SEO
        </mj-text>
        <mj-text font-size="14px">
          O Spwig gera automaticamente mapas do site e metatags. Visite <strong>Configurações > SEO</strong> para personalizar os títulos das páginas, descrições e imagens para compartilhamento em redes sociais, ajudando os clientes a encontrarem sua loja.
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
Dicas para Começar - {{ store_name }}

Olá {{ name|default:'there' }},

Agora que {{ store_name }} está em funcionamento, aqui estão algumas dicas para ajudá-lo a obter o máximo da sua loja.

1. Personalize o Seu Visual
Visite Design > Configurações do Tema para escolher um tema, carregar seu logotipo e definir as cores da sua marca.

2. Adicione Seus Produtos
Vá para Catálogo > Produtos para começar a adicionar seus itens com variantes, preços e imagens.

3. Configure Pagamentos
Vá para Configurações > Provedores de Pagamento para conectar o Stripe, PayPal ou outro método de pagamento.

4. Configure Envios
Em Configurações > Envios, configure suas zonas e taxas de envio para diferentes regiões.

5. Melhore Seu SEO
Visite Configurações > SEO para personalizar os títulos das páginas, descrições e imagens para compartilhamento em redes sociais.

Acesse o Painel de Administração: {{ admin_url }}

Precisa de ajuda? Entre em contato com {{ support_email }}