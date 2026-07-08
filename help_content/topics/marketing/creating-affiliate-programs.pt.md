---
title: Criando Programas de Afiliados
---

Programas de afiliados definem como seus parceiros ganham comissões quando eles referenciam clientes para sua loja. Cada programa tem sua própria estrutura de comissão, regras de rastreamento e limites de pagamento. Você pode criar múltiplos programas para atender a diferentes segmentos de afiliados — como influenciadores, criadores de conteúdo ou parceiros de referência em massa.

![Lista de Programas](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Componentes do Programa

Todo programa de afiliados consiste em:

- **Nome e Descrição** — Identifique o programa e explique-o aos afiliados
- **Estrutura de Comissão** — Quanto os afiliados ganham por venda (percentual ou valor fixo)
- **Duração do Cookie** — Quanto tempo dura o rastreamento de referência após um clique (1–365 dias)
- **Aprovação Automática** — Se novos afiliados se juntam automaticamente ou requerem revisão manual
- **Limite Mínimo de Pagamento** — Quanto os afiliados devem ganhar antes de solicitar um pagamento
- **Status** — Ativo, pausado ou arquivado

## Tipos de Comissão

Escolha entre dois modelos de comissão ao criar seu programa:

| Tipo | Como Funciona | Quando Usar | Cálculo Exemplo |
|------|-------------|-------------|---------------------|
| **Percentual** | O afiliado ganha um percentual do subtotal do pedido | Recompensas escaláveis que crescem com o valor do pedido | 10% de um pedido de $150 = $15 de comissão |
| **Valor Fixo** | O afiliado ganha um valor fixo por venda | Custos previsíveis; ideal para produtos de alto volume e baixa margem | $25 por venda, independentemente do valor do pedido |

**Comissões percentuais** se escalam naturalmente — os afiliados ganham mais quando referenciam clientes de alto valor. Isso alinha seus incentivos aos seus e é o modelo mais comum (normalmente 5–15%).

**Comissões fixas** funcionam bem para serviços, assinaturas ou programas de referência em massa onde você deseja custos por venda previsíveis. Eles são fáceis de entender e planejar, mas podem subcompensar afiliados que trazem pedidos grandes.

## Criando um Programa

Navegue até **Marketing > Programas de Afiliados** e clique em **+ Adicionar Programa**.

### Configuração Passo a Passo

1. **Nome do Programa**
   Insira um nome descritivo visível aos afiliados (ex.: "Programa de Parceiros" ou "Nível de Influenciador").

2. **Slug**
   Um identificador amigável para URLs, gerado automaticamente a partir do nome. Usado em URLs e referências internas. Você pode personalizá-lo se necessário.

3. **Descrição**
   Texto opcional explicando os benefícios e termos do programa. Os afiliados veem isso ao revisar programas que podem se juntar.

4. **Tipo de Comissão**
   Selecione **Percentual** ou **Valor Fixo**.

5. **Valor da Comissão**
   - Para percentual: Insira um valor entre 0 e 100 (ex.: `10` para 10%)
   - Para valor fixo: Insira o valor em dólares por venda (ex.: `25.00` para $25)

6. **Duração do Cookie em Dias**
   Quantos dias o cookie de rastreamento dura (1–365). Veja a seção abaixo para orientação.

7. **Aprovação Automática de Afiliados**
   - **Marcado** — Novos afiliados se juntam automaticamente
   - **Não marcado** — Você revisa e aprova cada solicitação manualmente

8. **Pagamento Mínimo**
   O saldo mínimo que um afiliado deve acumular antes de solicitar um pagamento (ex.: `50.00` para $50).

9. **Status**
   Defina como **Ativo** para aceitar novos afiliados e rastrear referências.

10. **Salvar** o programa.

## Explicação sobre a Duração do Cookie

A duração do cookie determina por quanto tempo o Spwig lembra que um cliente clicou em um link de referência de um afiliado.

### Como Funciona

1. Um cliente clica em um link de um afiliado
2. O Spwig define um cookie de rastreamento no navegador do cliente
3. Se o cliente completar uma compra **dentro da duração do cookie**, o pedido é creditado ao afiliado
4. Se o cookie expirar antes da compra, o afiliado não ganha comissão

### Escolhendo uma Duração

| Duração | Caso de Uso | Cenário Típico |
|----------|----------|------------------|
| **1–7 dias** | Compras impulsivas, vendas flash | Produtos de consumo rápido, ofertas limitadas |
| **30 dias** | E-commerce padrão | Varejo online geral, recomendação padrão |
| **60–90 dias** | Compras consideradas | Itens de alto valor, B2B, serviços |
| **180+ dias** | Ciclos de venda longos | Software empresarial, assinaturas, produtos de luxo |

**Padrão da indústria é 30 dias.** Isso equilibra a atribuição justa para afiliados com limites práticos de rastreamento. Durações curtas favorecem clientes que convertem rapidamente; durações mais longas dão aos clientes tempo para pesquisar e retornar para completar a compra.

### Nota Técnica

A duração do cookie afeta apenas a **atribuição**. Comissões aprovadas permanecem válidas indefinidamente — a duração do cookie apenas determina se um pedido é creditado ao afiliado no primeiro lugar.

## Configurações de Aprovação Automática

A configuração de aprovação automática controla se novas solicitações de afiliados requerem revisão manual.

### Quando Habilitar Aprovação Automática

- **Programas públicos** — Você deseja crescer rapidamente sua base de afiliados sem gargalos
- **Produtos de baixo risco** — Risco de fraude ou de marca é mínimo
- **Programas de alto volume** — Você espera muitas solicitações e não pode revisar cada uma manualmente

### Quando Requerer Revisão Manual

- **Programas por convite** — Você aceita apenas parceiros pré-avaliados
- **Programas premium** — Taxas de comissão altas ou benefícios exclusivos
- **Produtos sensíveis à marca** — Você precisa garantir que os afiliados estejam alinhados com os valores da sua marca
- **Prevenção de fraude** — Você deseja filtrar contas suspeitas

### Considerações de Segurança

Revisar manualmente os afiliados ajuda a prevenir:
- Esquemas de autoreferência (afiliados criando contas falsas para ganhar comissões)
- Violações de marca (afiliados licitando termos da sua marca em busca paga)
- Desalinhamento de marca (afiliados promovendo seus produtos em contextos inapropriados)

Para a maioria das lojas, começar com **aprovação manual** é mais seguro. Você sempre pode habilitar aprovação automática depois que estabelecer padrões de confiança.

## Limite Mínimo de Pagamento

O limite mínimo de pagamento previne sobrecarga administrativa de processar muitos pagamentos pequenos.

### Por Que Estabelecer um Limite Mínimo

- **Reduz taxas de transação** — Processadores de pagamento cobram por transação, então agrupar pagamentos economiza dinheiro
- **Simplifica a contabilidade** — Menos eventos de pagamento significam menos trabalho de reconciliação
- **Padrão da indústria** — A maioria dos programas de afiliados tem limites ($25–$100)

### Limites Típicos

| Limite | Caso de Uso |
|-----------|----------|
| **$25–$50** | Programas de alto volume onde os afiliados atingem o limite rapidamente |
| **$50–$100** | Limite padrão para a maioria dos programas |
| **$100–$200** | Programas premium ou pagamentos internacionais com altas taxas de processamento |

### Equilibrando a Satisfação dos Afiliados

Definir o limite **muito alto** frustra afiliados que podem esperar meses para receber seu primeiro pagamento. Definir o limite **muito baixo** cria uma sobrecarga administrativa e consome suas margens com taxas.

**Recomendação:** Comece com $50. Isso é baixo o suficiente para que afiliados ativos atinjam o limite em suas primeiras poucas vendas, mas alto o suficiente para agrupar pagamentos de forma eficiente.

### Nenhum Limite Máximo

Não há limite máximo — os afiliados podem acumular ganhos indefinidamente antes de solicitar um pagamento. Alguns afiliados preferem agrupar suas solicitações trimestralmente ou anualmente para planejamento fiscal.

## Gerenciamento do Status do Programa

Os programas podem estar em um dos três status:

| Status | Descrição | Comportamento |
|--------|-------------|----------|
| **Ativo** | O programa está em execução | Aceita novos afiliados, rastreia referências, calcula comissões |
| **Pausado** | Desativado temporariamente | Afiliados existentes permanecem, mas não há novas inscrições; cookies de referência existentes ainda funcionam |
| **Arquivado** | Fechado permanentemente | Nenhum novo afiliado, nenhuma nova referência rastreada; dados históricos preservados para relatórios |

### Quando Pausar um Programa

- Você está revisando taxas de comissão ou termos
- Você está acima do orçamento para pagamentos de afiliados este trimestre
- Você está testando uma nova estrutura de programa e quer impedir que novos afiliados se juntem ao antigo

Programas pausados ainda honram cookies de rastreamento existentes e comissões pendentes — você está apenas impedindo novos afiliados de se juntarem.

### Quando Arquivar um Programa

- Você substituiu o programa por uma nova estrutura
- O programa era limitado a tempo (ex.: campanha sazonal)
- Você está consolidando múltiplos programas em um

Programas arquivados permanecem no banco de dados para relatórios históricos, mas são removidos das visões de gestão ativa.

## Exemplos de Programas

### Exemplo 1: Programa de Influenciadores (Percentual)

| Campo | Valor |
|-------|-------|
| Nome | Programa de Influenciadores |
| Tipo de Comissão | Percentual |
| Valor da Comissão | 10 |
| Duração do Cookie em Dias | 30 |
| Aprovação Automática | Não marcado (revisão manual) |
| Limite Mínimo de Pagamento | 50.00 |
| Status | Ativo |

**Caso de Uso:** Recrute influenciadores de mídia social e criadores de conteúdo. A comissão de 10% se escala com o valor do pedido, recompensando afiliados que atraem clientes de alto gasto. A aprovação manual garante que você avalie cada influenciador público e alinhamento com a marca.

### Exemplo 2: Programa de Referência em Massa (Valor Fixo)

| Campo | Valor |
|-------|-------|
| Nome | Programa de Parceiros de Referência |
| Tipo de Comissão | Valor Fixo |
| Valor da Comissão | 25.00 |
| Duração do Cookie em Dias | 7 |
| Aprovação Automática | Marcado |
| Limite Mínimo de Pagamento | 100.00 |
| Status | Ativo |

**Caso de Uso:** Parceria com sites de ofertas, agregadores de cupons e redes de referência que geram alto volume. A comissão fixa de $25 mantém os custos previsíveis, e a curta duração do cookie (7 dias) visa conversões rápidas. A aprovação automática está habilitada, pois esses parceiros geralmente se servem sozinhos.

### Exemplo 3: Parceiro Premium (Alto Percentual)

| Campo | Valor |
|-------|-------|
| Nome | Nível de Parceiro Premium |
| Tipo de Comissão | Percentual |
| Valor da Comissão | 15 |
| Duração do Cookie em Dias | 90 |
| Aprovação Automática | Não marcado |
| Limite Mínimo de Pagamento | 200.00 |
| Status | Ativo |

**Caso de Uso:** Programa exclusivo para afiliados de alto desempenho ou parceiros estratégicos. Maior comissão (15%) recompensa seu tráfego de qualidade, e a duração do cookie de 90 dias acomoda ciclos de consideração mais longos. Aprovação manual apenas — este é um nível por convite.

## Dicas

- Comece com uma **comissão percentual** (5–15%) para a maioria dos programas — é mais fácil explicar aos afiliados e se escala naturalmente com o valor do pedido.
- Use **duração do cookie de 30 dias** como base — é o padrão da indústria e equilibra a atribuição justa com limites práticos de rastreamento.
- Ative **aprovação manual** inicialmente para avaliar afiliados, depois mude para aprovação automática depois que estabelecer padrões de confiança e controles contra fraude.
- Defina seu **limite mínimo de pagamento** para $50–$100 para equilibrar a satisfação dos afiliados (não muito alto para atingir) com eficiência administrativa (não muitos pagamentos pequenos).
- Crie **programas separados** para diferentes segmentos de afiliados (influenciadores, sites de conteúdo, agregadores de ofertas) para que você possa rastrear o desempenho e ajustar as comissões de forma independente.
- Monitore o **painel de análise** regularmente para identificar afiliados de alto desempenho e ajustar as taxas de comissão para reter os melhores parceiros.

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.