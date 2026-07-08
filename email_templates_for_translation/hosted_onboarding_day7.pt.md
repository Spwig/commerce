---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
Aumente suas Vendas - {{ store_name }}

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
          Começando: Marketing & Crescimento
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Direcione tráfego e vendas para {{ store_name }}
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
          Agora que <strong>{{ store_name }}</strong> está tomando forma, é hora de se concentrar em direcionar tráfego e crescer suas vendas. Aqui estão cinco dicas de marketing para começar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Crie seu Primeiro Código de Desconto
        </mj-text>
        <mj-text font-size="14px">
          Ofereça um desconto de lançamento para atrair seus primeiros clientes. Vá para <strong>Marketing > Códigos de Desconto</strong> para criar descontos percentuais ou fixos com limites de uso e datas de expiração opcionais.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure a Recuperação de Carrinho Abandonado
        </mj-text>
        <mj-text font-size="14px">
          Recupere vendas perdidas automaticamente. Ative e-mails de recuperação de carrinho abandonado em <strong>Marketing > Carrinhos Abandonados</strong> para lembrar aos clientes dos itens que deixaram para trás.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Conecte suas Contas de Mídia Social
        </mj-text>
        <mj-text font-size="14px">
          Conecte seus perfis de mídia social à sua loja para que os clientes possam encontrá-lo e segui-lo. Adicione links de mídia social em <strong>Configurações > Mídia Social</strong> para exibi-los no rodapé da sua loja.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure o Rastreamento do Google Analytics
        </mj-text>
        <mj-text font-size="14px">
          Entenda de onde seus visitantes vêm e como eles interagem com sua loja. Adicione seu ID de rastreamento do Google Analytics em <strong>Configurações > Analytics</strong> para começar a coletar dados.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Crie um Formulário de Inscrição para Newsletter
        </mj-text>
        <mj-text font-size="14px">
          Construa sua lista de e-mails desde o primeiro dia. Adicione um formulário de inscrição para newsletter em sua loja para capturar e-mails de visitantes. Use esses contatos para promoções, lançamentos de produtos e engajamento com clientes.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Começando: Marketing & Crescimento - {{ store_name }}

Olá {{ name|default:'there' }},

Agora que {{ store_name }} está tomando forma, é hora de se concentrar em direcionar tráfego e crescer suas vendas. Aqui estão cinco dicas de marketing para começar.

1. Crie seu Primeiro Código de Desconto
Ofereça um desconto de lançamento para atrair seus primeiros clientes. Vá para Marketing > Códigos de Desconto para criar descontos com limites de uso e datas de expiração opcionais.

2. Configure a Recuperação de Carrinho Abandonado
Recupere vendas perdidas automaticamente. Ative e-mails de recuperação de carrinho abandonado em Marketing > Carrinhos Abandonados.

3. Conecte suas Contas de Mídia Social
Conecte seus perfis de mídia social à sua loja. Adicione links de mídia social em Configurações > Mídia Social.

4. Configure o Rastreamento do Google Analytics
Entenda de onde seus visitantes vêm. Adicione seu ID de rastreamento do Google Analytics em Configurações > Analytics.

5. Crie um Formulário de Inscrição para Newsletter
Construa sua lista de e-mails desde o primeiro dia. Adicione um formulário de inscrição para newsletter para capturar e-mails de visitantes para promoções e engajamento.

Vá para Marketing: {{ admin_url }}

Precisa de ajuda? Entre em contato com {{ support_email }}