---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
Vá Mais Longe - {{ store_name }}

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
          Começando: Funcionalidades Avançadas
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Descubra o potencial completo de {{ store_name }}
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
          Você está operando <strong>{{ store_name }}</strong> há algumas semanas agora. Aqui estão algumas funcionalidades avançadas para ajudá-lo a levar sua loja ao próximo nível.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Fluxos de E-mail Automatizados
        </mj-text>
        <mj-text font-size="14px">
          Automatize sua comunicação com clientes usando fluxos de e-mail. Configure sequências de boas-vindas, follow-ups pós-compra e campanhas de reengajamento em <strong>Marketing > Fluxos de E-mail</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Regras de Imposto para Suas Regiões
        </mj-text>
        <mj-text font-size="14px">
          Certifique-se de que está cobrando as taxas corretas. Vá para <strong>Configurações > Imposto</strong> para configurar regras de imposto para cada região em que vende. Você pode configurar preços com imposto incluso ou excluído.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Explore a API para Integrações
        </mj-text>
        <mj-text font-size="14px">
          Se seu plano incluir acesso à API, você pode integrar sua loja com ferramentas e serviços externos. Visite <strong>Configurações > API</strong> para gerar chaves de API e explorar a documentação.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Revise Seu Painel de Análises
        </mj-text>
        <mj-text font-size="14px">
          Mantenha um olho no desempenho da sua loja. Seu <strong>Painel</strong> mostra métricas-chave, incluindo receita, pedidos, produtos mais vendidos e insights de clientes para ajudá-lo a tomar decisões com base em dados.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Considere Adicionar POS para Vendas Presenciais
        </mj-text>
        <mj-text font-size="14px">
          Vender presencialmente também? A funcionalidade de ponto de venda do Spwig permite que você processe transações presenciais que sincronizam com seu estoque online e gestão de pedidos. Verifique <strong>Configurações > Ponto de Venda</strong> para saber mais.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Explore Seu Painel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Começando: Funcionalidades Avançadas - {{ store_name }}

Olá {{ name|default:'there' }},

Você está operando {{ store_name }} há algumas semanas agora. Aqui estão algumas funcionalidades avançadas para ajudá-lo a levar sua loja ao próximo nível.

1. Configure Fluxos de E-mail Automatizados
Automatize sua comunicação com clientes usando sequências de boas-vindas, follow-ups pós-compra e campanhas de reengajamento.

2. Configure Regras de Imposto para Suas Regiões
Certifique-se de que está cobrando as taxas corretas. Vá para Configurações > Imposto para configurar regras para cada região.

3. Explore a API para Integrações
Se seu plano incluir acesso à API, integre sua loja com ferramentas externas. Visite Configurações > API para começar.

4. Revise Seu Painel de Análises
Seu Painel mostra métricas-chave, incluindo receita, pedidos, produtos mais vendidos e insights de clientes.

5. Considere Adicionar POS para Vendas Presenciais
Vender presencialmente também? A funcionalidade de ponto de venda do Spwig sincroniza transações presenciais com seu estoque online.

Explore Seu Painel: {{ admin_url }}

Precisa de ajuda? Entre em contato com {{ support_email }}