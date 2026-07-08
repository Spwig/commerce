---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
Construa Seu Catálogo - {{ store_name }}

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
          Começando: Seus Produtos
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Construa um excelente catálogo para {{ store_name }}
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
          Sua loja <strong>{{ store_name }}</strong> está tudo configurada. Agora é hora de construir seu catálogo de produtos. Aqui estão cinco dicas para começar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Importe Produtos do CSV
        </mj-text>
        <mj-text font-size="14px">
          Já tem uma lista de produtos? Vá para <strong>Admin > Catálogo > Importar</strong> para importar em massa seus produtos de um arquivo CSV. Este é o método mais rápido para preencher sua loja.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Organize com Categorias e Filtros
        </mj-text>
        <mj-text font-size="14px">
          Crie categorias e filtros de atributos para que os clientes possam navegar facilmente e encontrar o que procuram. Catálogos bem organizados levam a taxas de conversão mais altas.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Escreva Descrições de Produtos Engajadoras
        </mj-text>
        <mj-text font-size="14px">
          Descrições excelentes vendem produtos. Foque nos benefícios, não apenas nas características. Conte aos clientes por que eles precisam do seu produto e como ele resolve seu problema.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Carregue Imagens de Alta Qualidade dos Produtos
        </mj-text>
        <mj-text font-size="14px">
          Imagens claras e profissionais fazem uma grande diferença. Carregue vários ângulos e use iluminação consistente. O Spwig otimiza automaticamente as imagens para carregamento rápido.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure Variantes de Produtos
        </mj-text>
        <mj-text font-size="14px">
          Se seus produtos vierem em tamanhos, cores ou estilos diferentes, crie variantes para que os clientes possam selecionar exatamente o que querem. Cada variante pode ter seu próprio preço, nível de estoque e imagens.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Gerencie Seus Produtos" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Começando: Seus Produtos - {{ store_name }}

Olá {{ name|default:'there' }},

Sua loja {{ store_name }} está tudo configurada. Agora é hora de construir seu catálogo de produtos. Aqui estão cinco dicas para começar.

1. Importe Produtos do CSV
Já tem uma lista de produtos? Vá para Admin > Catálogo > Importar para importar em massa seus produtos de um arquivo CSV.

2. Organize com Categorias e Filtros
Crie categorias e filtros de atributos para que os clientes possam navegar facilmente e encontrar o que procuram.

3. Escreva Descrições de Produtos Engajadoras
Descrições excelentes vendem produtos. Foque nos benefícios, não apenas nas características. Conte aos clientes por que eles precisam do seu produto.

4. Carregue Imagens de Alta Qualidade dos Produtos
Imagens claras e profissionais fazem uma grande diferença. Carregue vários ângulos e use iluminação consistente.

5. Configure Variantes de Produtos
Se seus produtos vierem em tamanhos, cores ou estilos diferentes, crie variantes para que os clientes possam selecionar exatamente o que querem.

Gerencie Seus Produtos: {{ admin_url }}

Precisa de ajuda? Entre em contato com {{ support_email }}