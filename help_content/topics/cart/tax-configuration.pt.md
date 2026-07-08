---
title: Configuração de Impostos
---

Configure regras de impostos para sua loja para que os impostos corretos sejam aplicados automaticamente aos pedidos com base na localização do cliente. Você pode carregar configurações regionais com um clique ou criar regras personalizadas para qualquer país, estado, cidade ou código postal.

![Painel de Impostos](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Painel de Impostos

Navegue até **Pedidos > Envios > Taxas de Imposto** para abrir o painel de impostos. A página mostra:

- **Painel de Estatísticas** — quatro cartões exibindo Total de Regras, Regras Ativas, Países Cobertos e Tipos de Imposto em uso
- **Filtros** — pesquisar por nome, país ou estado, e filtrar por país, tipo de imposto (Imposto de Venda, IVA, IGV, Personalizado) ou status (Ativo/Inativo)
- **Cartões de Regra de Imposto** — cada cartão mostra a bandeira do país, nome da regra, localização, percentual da taxa, badge do tipo de imposto, badge de status, prioridade e contagem de isenções

## Carregando Configurações de Impostos

Clique em **Carregar Configurações** para abrir o modal de configurações. As configurações são coleções de taxas de imposto padrão para uma região, prontas para serem carregadas em sua loja com um clique.

![Carregar Configurações](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

As configurações são organizadas por região do mundo:

| Região | Grupos de Configurações |
|--------|------------------------|
| **África** | IVA da África (25 taxas) |
| **Ásia-Pacífico** | IVA/IGV da Ásia-Pacífico (24 taxas), IVA da Ásia Central (6 taxas) |
| **Europa** | Taxas de IVA da UE, IVA do Reino Unido, Outras Taxas de IVA da Europa |
| **América Latina** | IVA da América Latina |
| **Médio Oriente** | IVA do Médio Oriente |
| **América do Norte** | Imposto de Venda dos Estados Unidos por Estado, IGV/HST do Canadá |
| **Oceania** | IGV/IVA da Oceania |

### Como as Configurações Funcionam

1. Clique em **Carregar** no grupo de configurações que deseja
2. O sistema cria regras de imposto para todos os países ou estados desse grupo
3. Regras existentes com o mesmo país, estado e tipo de imposto são automaticamente ignoradas para evitar duplicatas
4. Após o carregamento, cada regra é totalmente editável — ajuste as taxas, adicione isenções ou desative as regras que não precisa

Você pode carregar vários grupos de configurações. Por exemplo, carregue tanto as Taxas de IVA da UE quanto as do Reino Unido se vender para clientes em toda a Europa.

## Criando Regras de Imposto Manualmente

Clique em **Adicionar Taxa de Imposto** para criar uma regra personalizada. O formulário tem quatro seções:

![Formulário de Taxa de Imposto](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Informações Básicas

| Campo | Descrição |
|-------|-----------|
| **Nome** | Nome de exibição para a regra (ex: "Imposto de Venda da Califórnia") |
| **Ativo** | Alternar para habilitar ou desabilitar a regra |
| **Tipo de Imposto** | Imposto de Venda, IVA, IGV ou Imposto Personalizado |
| **Taxa (%)** | A taxa de imposto como porcentagem (ex: digite 8,25 para 8,25%) |
| **Prioridade** | Números mais altos têm precedência quando várias regras correspondem à mesma localização |

### Escopo Geográfico

| Campo | Descrição |
|-------|-----------|
| **País** | Código ISO 3166-1 alpha-2 (ex: US, GB, DE) |
| **Estado** | Estado ou província (deixe em branco para aplicar a todo o país) |
| **Cidade** | Nome da cidade (opcional, para regras de imposto em nível de cidade) |
| **Códigos Postais** | Lista de códigos postais específicos (opcional, para regras de imposto em nível de código postal) |

As regras são correspondidas da mais específica para a menos específica. Uma regra para um código postal específico tem prioridade sobre uma regra para o mesmo estado, que tem prioridade sobre uma regra para o país inteiro.

### Regras de Aplicação

| Campo | Descrição |
|-------|-----------|
| **Aplica-se ao Envio** | Quando marcado, este imposto também se aplica aos custos de envio |
| **Imposto Composto** | Quando marcado, este imposto é calculado sobre outros impostos (o valor base mais impostos já aplicados) |

### Isenções de Produtos

| Campo | Descrição |
|-------|-----------|
| **Tipos de Produtos Isentos** | Tipos de produtos isentos deste imposto (ex: digital, serviço) |
| **Categorias Isentas** | Categorias de produtos específicas isentas deste imposto |

## Tipos de Imposto

| Tipo | Usado Para | Exemplos |
|------|------------|--------|
| **Imposto de Venda** | EUA, Canadá | Impostos estaduais e provinciais de venda |
| **IVA** | Europa, Reino Unido, grande parte da Ásia e África | Imposto sobre o Valor Adicionado |
| **IGV** | Austrália, Nova Zelândia, Índia, Cingapura | Imposto sobre Bens e Serviços |
| **Imposto Personalizado** | Casos especiais | Sobretaxas locais, impostos ambientais, impostos sobre luxo |

## Como o Cálculo de Imposto Funciona

Quando um cliente chega ao checkout, o sistema calcula automaticamente os impostos com base no endereço de envio:

1. **Correspondência Geográfica** — encontra todas as regras ativas que correspondem ao país do cliente, depois estreita por estado, cidade e código postal
2. **Classificação de Especificidade** — regras mais específicas (código postal > cidade > estado > país) são classificadas com prioridade mais alta
3. **Classificação por Prioridade** — dentro do mesmo nível de especificidade, regras com prioridade mais alta têm precedência
4. **Isenções de Produtos** — produtos isentos são excluídos de cada regra aplicável
5. **Impostos Não Compostos** — calculados primeiro no preço base de cada item
6. **Impostos Compostos** — calculados no preço base mais todos os impostos não compostos já aplicados
7. **Imposto de Envio** — se uma regra tiver "Aplica-se ao Envio" habilitado, o custo de envio é incluído no valor tributável

A quebra de impostos é armazenada com o pedido para que você possa ver exatamente quais regras foram aplicadas e quanto cada uma contribuiu.

## Configurações Comuns

### Loja da UE

1. Clique em **Carregar Configurações** e carregue o grupo **Taxas de IVA da UE**
2. Isso cria regras de IVA para todos os países membros da UE com suas taxas padrão atuais
3. Carregue opcionalmente **IVA do Reino Unido** se também vender para o Reino Unido

### Loja dos EUA

1. Clique em **Carregar Configurações** e carregue o grupo **Imposto de Venda por Estado dos EUA**
2. Isso cria regras de imposto de venda para todos os estados dos EUA que coletam imposto de venda
3. Para impostos em nível de cidade, adicione manualmente regras com o campo cidade preenchido e uma prioridade mais alta

### Loja Multirregional

1. Carregue vários grupos de configurações para cada mercado em que vende
2. O sistema aplica o imposto correto com base na localização de cada cliente
3. Ajuste as regras individuais conforme necessário para atender aos requisitos específicos do seu negócio

## Dicas

- **Comece com configurações** — carregue os grupos de configurações para seus mercados-alvo, depois personalize as taxas individuais em vez de criar cada regra do zero.
- **Use a prioridade com sabedoria** — defina valores de prioridade mais altos para regras locais mais específicas para que elas substituam corretamente as regras regionais mais amplas.
- **Verifique cuidadosamente o imposto composto** — o imposto composto é raro. A maioria das jurisdições usa imposto simples (não composto). Apenas habilite o imposto composto quando suas regulamentações locais especificamente exigirem o cálculo de imposto sobre imposto.
- **Mantenha regras ativas/inativas** — em vez de excluir regras de imposto para mudanças sazonais ou temporárias, ative-as como inativas e reative quando necessário.
- **Teste antes de ir ao vivo** — após configurar suas regras de imposto, faça um pedido de teste de diferentes endereços para verificar se os impostos corretos estão sendo aplicados.