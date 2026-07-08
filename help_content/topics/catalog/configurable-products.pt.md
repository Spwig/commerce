---
title: "Produtos Configuráveis"
---

Produtos configuráveis permitem que os clientes montem seu próprio produto escolhendo opções de diferentes slots de configuração. Isso é ideal para itens feitos sob encomenda, como PCs personalizados, caixas de presentes personalizadas ou móveis sob medida, onde cada componente é um produto real no seu catálogo.

![Product configurator admin](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Como Funciona

Um produto configurável é composto por **slots** (categorias de escolhas) e **opções** (os produtos reais que os clientes podem escolher). Por exemplo, um PC personalizado pode ter slots para Processador, Placa de Vídeo, RAM e Armazenamento — cada slot contendo várias opções de produtos para escolher.

## Estratégias de Preço

Escolha como o preço final é calculado:

| Estratégia | Descrição |
|------------|-----------|
| **Soma dos Componentes** | Preço final = total de todos os preços das opções selecionadas. Não é necessário preço base. |
| **Preço Base + Ajustes** | Começa com o preço base do produto, depois adiciona/subtrai ajustes de preço por opção. |
| **Preço Fixo** | Um preço único independentemente das opções que o cliente selecionar. |

## Configurando um Produto Configurável

### Passo 1: Criar o Produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina o **Tipo de Produto** como **Produto Configurável**
3. Escolha sua **Estratégia de Preço** (Soma dos Componentes é a mais comum)
4. Preencha o nome do produto, descrição e outros detalhes básicos
5. Salve o produto

### Passo 2: Adicionar Slots de Configuração

Após salvar, mude para a aba **Configuração** para configurar seus slots.

1. Clique em **+ Adicionar Slot** para criar uma nova categoria de configuração
2. Para cada slot, configure:
   - **Nome** — O que o cliente vê (ex.: "Processador", "Cor")
   - **Ícone** — Classe de ícone Font Awesome para identificação visual
   - **Obrigatório** — Se o cliente deve fazer uma seleção
   - **Seleções Mín/Máx** — Quantas opções o cliente pode escolher (padrão: exatamente 1)
   - **Ordem de Classificação** — Controla a ordem em que os slots aparecem no assistente de configuração

### Passo 3: Adicionar Opções a Cada Slot

Cada slot precisa de opções de produtos para os clientes escolherem:

1. Clique em **Gerenciar Opções** em um slot
2. Pesquise e adicione produtos existentes do seu catálogo
3. Para cada opção, configure:
   - **Ajuste de Preço** — Valor a adicionar ou subtrair (usado com preço Base + Ajustes)
   - **Padrão** — Pré-selecionar esta opção quando o configurador carregar
   - **Popular** — Mostrar um selo "Popular" para ajudar os clientes a decidir
   - **Quantidade** — Quantas unidades deste componente estão incluídas
   - **Tags de Compatibilidade** — Tags usadas para geração em lote de regras de compatibilidade

**Dica:** Produtos componentes podem ser ocultados da vitrine marcando **Ocultar da Vitrine** na aba Informações Básicas do produto componente. Isso os mantém disponíveis como opções do configurador sem poluir seu catálogo de produtos.

### Passo 4: Definir Regras de Compatibilidade

Regras de compatibilidade impedem que os clientes selecionem combinações incompatíveis:

| Tipo de Regra | Descrição |
|---------------|-----------|
| **Requer** | Quando a opção A é selecionada, apenas as opções listadas ficam disponíveis no slot de destino |
| **Exclui** | Quando a opção A é selecionada, as opções listadas são ocultadas do slot de destino |

Para adicionar regras:

1. Role até a seção **Regras de Compatibilidade** na aba Configuração
2. Clique em **+ Adicionar Regra**
3. Selecione a **opção de origem** (o gatilho)
4. Escolha o **tipo de regra** (Requer ou Exclui)
5. Selecione o **slot de destino** e as **opções afetadas**

Você também pode gerar regras automaticamente a partir de tags de compatibilidade atribuídas às opções, o que é mais rápido ao gerenciar muitas combinações.

### Passo 5: Criar Predefinições (Opcional)

Predefinições são configurações pré-montadas que dão aos clientes um ponto de partida rápido:

1. Role até a seção **Predefinições de Configuração**
2. Clique em **+ Adicionar Predefinição**
3. Dê à predefinição um nome e descrição (ex.: "Build Gamer", "Iniciante Econômico")
4. Selecione as opções para cada slot
5. Opcionalmente, envie uma imagem de pré-visualização e marque como **Destaque**

Os clientes podem começar a partir de uma predefinição e depois personalizar slots individuais conforme sua preferência.

## Experiência do Cliente

Quando um cliente visualiza um produto configurável na sua vitrine:

1. **Interface de Assistente** — Os slots são apresentados como etapas, guiando o cliente por cada escolha
2. **Filtragem** — Opções incompatíveis são automaticamente ocultadas com base nas regras de compatibilidade
3. **Selos de Popular** — Opções marcadas como populares exibem um selo para ajudar na decisão
4. **Predefinições** — Predefinições em destaque aparecem como opções de início rápido
5. **Atualizações de Preço** — O preço total é atualizado em tempo real conforme as opções são selecionadas
6. **Resumo** — Uma etapa de revisão mostra todas as opções selecionadas antes de adicionar ao carrinho

## Dicas

- Comece com a estratégia de preço "Soma dos Componentes" — é a mais intuitiva para os clientes e a mais fácil de manter.
- Use regras de compatibilidade para prevenir configurações inválidas em vez de depender do conhecimento do cliente.
- Crie 2-3 predefinições para suas configurações mais populares para reduzir a fadiga de decisão.
- Oculte produtos componentes da vitrine se eles devem estar disponíveis apenas através do configurador.
- Teste o fluxo completo de configuração no frontend após a configuração para garantir que todas as regras funcionem como esperado.
