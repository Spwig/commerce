---
title: Audiências
---

Um **Segmento** é uma audiência salva na qual você pode direcionar uma campanha, uma jornada ou um teste A/B — a própria lista de Segmentos do Campaign Studio os chama de "Audiências direcionadas", e este guia usa ambas as palavras para a mesma coisa. Cada segmento é **dinâmico**, definido por regras que o Spwig reavalia cada vez que é usado, ou **estático**, uma lista explícita de assinantes que você escolhe manualmente.

Este guia aborda a construção das regras de um segmento dinâmico — incluindo campos mais recentes que direcionam os próprios buckets de valor do cliente da sua loja, o programa de fidelidade e os afiliados — e o botão **Adicionar audiências iniciais** que cria um conjunto de segmentos prontos a partir dos dados que sua loja já possui.

## Segmentos dinâmicos vs. estáticos

| Tipo | Como funciona | Melhor para |
|---|---|---|
| **Dinâmico (regras)** | Você define condições — por exemplo, "Total gasto é de pelo menos $500." O Spwig recalcula quem corresponde cada vez que o segmento é usado, então a membresia muda automaticamente conforme seus assinantes mudam. | Audiências contínuas que devem sempre estar atualizadas, como "clientes VIP" ou "não fez pedido em 90 dias". |
| **Estático (lista fixa)** | Uma lista explícita de assinantes que você adiciona ou remove manualmente. A membresia nunca muda, a menos que você a altere. | Uma lista única — todos de um evento específico, ou um grupo escolhido manualmente para um envio único. |

Escolha o tipo com o campo **Tipo** ao criar um segmento. O restante deste guia é sobre segmentos dinâmicos — os estáticos são apenas uma lista de membros sem regras para configurar.

## Construindo um segmento dinâmico

Abra **Campaign Studio > Segmentos**, depois clique em **+ Novo Segmento** (ou abra um segmento dinâmico existente) para acessar o construtor de **Regras de audiência**. Clique em **+ Adicionar condição** para adicionar uma regra, escolha o que verificar e como, e defina se um assinante deve corresponder a **todas** ou a **qualquer** uma das suas condições. Uma contagem ao vivo no canto superior direito — por exemplo, "8 assinantes correspondentes" — é atualizada um momento após cada alteração, para que você possa ver exatamente quem se qualifica antes de salvar.

![O construtor de regras de audiência com condições de Segmento de cliente, Nível de fidelidade, Valor vitalício e Afiliado definidas, e uma contagem ao vivo de assinantes correspondentes](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Uma condição com uma verificação fixa no estilo **é verdadeiro** — **Fez pedido**, **Optou por marketing**, **Membro de fidelidade**, **Afiliado** — não requer nada além de escolher o próprio campo; não há operador ou valor a definir.

## O que você pode direcionar

| Campo | O que verifica |
|---|---|
| **Total gasto** | Total vitalício de pedidos. |
| **Número de pedidos** | Contagem de pedidos concluídos. |
| **Valor vitalício** | O valor vitalício calculado do cliente. |
| **Valor médio do pedido** | Valor médio por pedido concluído. |
| **Dias desde o último pedido** | Quanto tempo desde o pedido mais recente do cliente — direcione 90+ dias para uma audiência de recuperação. |
| **Fez pedido** | Se o cliente tem pelo menos um pedido concluído. |
| **Optou por marketing** | Se o assinante consentiu com e-mails de marketing. |
| **Idioma** | O idioma armazenado do assinante. |
| **Origem** | Como o assinante se juntou — Inscrição na loja, Importação, Pedido, Adicionado manualmente ou API. |
| **Juntou-se após** | Assinantes que se juntaram em ou após uma data escolhida. |
| **Tem tag** | Se o assinante possui uma [tag](/help/subscriber-tags) que você criou. |
| **Segmento de cliente** | Se o cliente se enquadra em um dos seus próprios [segmentos de clientes](/help/customer-segments) nomeados — Cliente Convidado, Novo Cliente, Cliente Regular, Comprador Frequente, Alto Valor, Cliente VIP, Caçador de Ofertas, Em Risco ou Inativo. |
| **Membro de fidelidade** | Se o cliente é um membro ativo do seu programa de fidelidade. |
| **Pontos de fidelidade** | O saldo atual de pontos disponíveis do membro. |
| **Nível de fidelidade** | Qual nível de fidelidade o membro atualmente possui. |
| **Afiliado** | Se o cliente é um dos seus parceiros afiliados ativos. |

**Segmento de cliente**, os dois campos de valor **Fidelidade**, **Nível de fidelidade** e **Afiliado** são adições mais recentes, e cada um só aparece no seletor de condições quando sua loja realmente possui esse tipo de dados: os campos de fidelidade aparecem quando seu programa de fidelidade tem membros e pelo menos um nível ativo, **Afiliado** aparece quando você tem pelo menos um afiliado, e **Segmento de cliente** aparece quando você tem pelo menos um segmento de cliente ativo configurado.

Você não verá uma opção em uma loja nova que não poderia corresponder a ninguém.

Uma limitação atual que vale a pena saber: para qualquer condição com uma lista suspensa de opções — **Idioma**, **Origem**, **Tem tag**, **Segmento de cliente**, **Nível de fidelidade** — o operador **é qualquer um de** ainda permite escolher apenas um valor por vez. Se você deseja corresponder a vários (por exemplo, clientes em qualquer um dos segmentos VIP ou Alto Valor), adicione uma condição por valor e defina **Correspondência** como **qualquer**.

## Adicionar públicos iniciais

Criar uma regra do zero para cada público óbvio — seus VIPs, seus membros de fidelidade, todos que ficaram em silêncio — é tedioso quando o Spwig já pode ver quem se qualifica. Na lista de Segmentos, clique em **Adicionar públicos iniciais** e o Spwig cria um conjunto de segmentos dinâmicos prontos e editáveis com base nos dados de clientes, fidelidade e afiliados que sua loja já possui.

![A lista de Segmentos com os botões Novo Segmento e Adicionar públicos iniciais](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Inicial | Alvo | Requisitos |
|---|---|---|
| **Clientes VIP** | Seu segmento de clientes VIP | Um segmento de clientes VIP ativo |
| **Clientes de alto valor** | Seus segmentos de clientes VIP e Alto Valor | Um segmento de clientes VIP ou Alto Valor ativo |
| **Compradores recorrentes** | Seus segmentos de Comprador Frequente e Regular | Um segmento de Comprador Frequente ou Regular ativo |
| **Novos clientes** | Seu segmento de Novos clientes | Um segmento de Novos clientes ativo |
| **Clientes em risco de perda** | Clientes que já fizeram pedidos, mas não nos últimos 90 dias | Qualquer histórico de pedidos de clientes |
| **Membros de fidelidade** | Todos os ativos no seu programa de fidelidade | Um programa de fidelidade ativo com membros |
| **Melhor nível de fidelidade** | Membros no seu nível de fidelidade mais alto | Pelo menos um nível de fidelidade ativo |
| **Afiliados** | Seus parceiros afiliados ativos | Pelo menos um afiliado |

O Spwig só cria os iniciais para os quais realmente possui dados — uma loja que ainda não tem um programa de fidelidade simplesmente não receberá um inicial de **Membros de fidelidade**, em vez de um vazio que nunca corresponderia a ninguém. O Spwig confirma exatamente o que foi adicionado, por exemplo: "Adicionado 7 público(s) inicial(is): Clientes de alto valor, Compradores recorrentes, Novos clientes, Clientes em risco de perda, Membros de fidelidade, Melhor nível de fidelidade, Afiliados."

![Mensagem de sucesso confirmando quais públicos iniciais foram adicionados](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

É seguro clicar em **Adicionar públicos iniciais** mais de uma vez. O Spwig nunca cria um duplicado de um inicial que já existe, então clicar novamente após configurar (por exemplo) seu programa de fidelidade pela primeira vez apenas adiciona o que está disponível agora — se tudo já estiver configurado, ele simplesmente informa isso.

![Mensagem de informação exibida quando todos os públicos iniciais já existem](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Se você excluir um inicial que não deseja, clicar em **Adicionar públicos iniciais** novamente não o trará de volta — o Spwig o trata como um segmento que você removeu intencionalmente, e não como um a ser recriado.

Uma vez criado, um inicial é um segmento dinâmico comum: abra-o a partir da lista para revisar ou ajustar suas regras, renomeá-lo ou excluí-lo, exatamente como faria com qualquer segmento que você mesmo criou.

## A quem esses públicos realmente alcançam


As condições de cliente, fidelidade e afiliado acima só correspondem a assinantes cujo e-mail esteja vinculado a uma conta de cliente — um cadastro de newsletter anônimo não corresponderá a uma condição de **membro de fidelidade** ou **VIP**, mesmo que corretamente, já que o Spwig não tem histórico de pedidos ou fidelidade para verificá-los.

Se muitos dos seus clientes tiverem contas, mas ainda não se inscreveram, peça a quem gerencia sua instalação do Spwig para executar uma sincronização de assinantes — ela cria um registro de assinante para cada conta de cliente existente em um único passo, para que esses públicos tenham pessoas reais para corresponderem.

Independentemente do número de assinantes de um segmento, esse número descreve quem *pode* receber uma campanha, e não quem irá. Cada envio ainda verifica primeiro o consentimento de marketing de cada assinante, então um segmento nunca é uma forma de contornar isso.

## Dicas

- Comece com um público inicial e o ajuste, em vez de construir a mesma regra manualmente — uma vez criado, um público inicial é idêntico a qualquer segmento que você tenha criado sozinho.
- Condições booleanas como **membro de fidelidade**, **afiliado** e **fez uma compra** não precisam de operador ou valor — basta adicionar a condição e estará pronto.
- Combine os novos campos com os originais para uma segmentação mais precisa, por exemplo, **membro de fidelidade** mais **optou por marketing**, em vez de depender apenas de uma condição.
- Se as regras de um segmento referenciarem algo que foi removido desde então — um segmento de cliente excluído, uma etiqueta esvaziada, e assim por diante — o Spwig o trata como correspondendo a ninguém, em vez de recorrer à sua lista completa de assinantes. O alvo quebrado envia menos; ele nunca envia para todos acidentalmente.
- Se o número de membros de um segmento parecer desatualizado, abra-o e salve novamente, ou use a ação em lote **Reconstruir números de membros** da lista de Segmentos, para recalculá-lo imediatamente.
- Observe o contador de "assinantes que correspondem" em tempo real enquanto você constrói uma regra — é a maneira mais rápida de detectar uma condição que esteja mais restrita (ou mais ampla) do que você pretendia antes de salvá-la.