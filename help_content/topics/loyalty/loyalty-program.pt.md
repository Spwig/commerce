---
title: Programa de Fidelidade
---

O Programa de Fidelidade permite que você recompense os clientes por compras e engajamento com um sistema baseado em pontos. Os clientes ganham pontos, avançam por níveis e resgatam recompensas. Navegue até **Marketing > Programa de Fidelidade** no menu lateral do administrador.

![Painel de fidelidade](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Painel de Fidelidade

O painel fornece uma visão abrangente do seu programa de fidelidade:

### Métricas Principais

- **Total de Membros** — Total de clientes inscritos
- **Membros Ativos (30d)** — Membros que ganharam ou resgataram pontos nos últimos 30 dias
- **Pontos Pendentes** — Total de pontos não resgatados de todos os membros
- **Taxa de Resgate** — Percentual de pontos ganhos que foram resgatados
- **Pontos Ganhos (30d)** — Pontos ganhos nos últimos 30 dias
- **Pontos Resgatados (30d)** — Pontos resgatados nos últimos 30 dias
- **Média de Pontos/Membro** — Saldo médio de pontos por membro
- **Regras Ativas** — Número de regras de ganho de pontos ativas atualmente

### Ações Rápidas

O painel tem cartões de atalho para gerenciar todos os aspectos do programa:
- **Membros** — Visualizar e gerenciar membros da fidelidade
- **Níveis** — Configurar níveis de associação
- **Recompensas** — Configurar o catálogo de recompensas
- **Resgates** — Visualizar histórico de resgates
- **Regras** — Configurar como os pontos são ganhos
- **Badges** — Gerenciar badges de conquistas
- **Campanhas** — Executar campanhas de fidelidade especiais
- **Segmentos** — Criar segmentos de membros para direcionamento

### Gráficos e Análises

- **Tendência de Inscrição de Membros** — Novas inscrições de membros ao longo do tempo
- **Pontos Ganhos vs. Resgatados** — Rastrear o equilíbrio do fluxo de pontos
- **Distribuição de Níveis** — Veja como os membros estão distribuídos pelos níveis

## Configurando o Programa

### Etapa 1: Criar Níveis

Os níveis definem os níveis de associação com benefícios crescentes:

1. Navegue até **Fidelidade > Níveis**
2. Crie níveis como Bronze, Prata, Ouro, Platina
3. Para cada nível, defina:
   - **Nome** — Nome de exibição do nível
   - **Rank** — Ordem de classificação (rank mais baixo = nível mais baixo, por exemplo, Bronze = 1, Prata = 2)
   - **Cor** — Cor de destaque visual exibida nos badges dos membros
   - **Pontos Mínimos Ganhos** — Pontos acumulados ao longo da vida para se qualificar para este nível
   - **Gasto Mínimo** — Valor total de gasto para se qualificar para este nível
   - **Número Mínimo de Pedidos** — Número de pedidos para se qualificar para este nível
   - **Multiplicador de Pontos** — Taxa de ganho de bônus para membros deste nível (por exemplo, 2.0 = 2x pontos)

Um membro se qualifica para um nível se **qualquer** um dos três limites for atingido. Você pode usar apenas um limite ou combinar todos os três.

### Etapa 2: Configurar Regras de Ganho

Regras definem como os clientes ganham pontos:

1. Navegue até **Fidelidade > Regras**
2. Crie regras usando um dos quatro tipos de regra:

| Tipo de Regra | Descrição | Exemplo |
|---------------|-----------|---------|
| **Gasto** | Pontos por valor gasto | 1 ponto por $1 |
| **Item** | Pontos por item comprado | 50 pontos por produto em uma categoria específica |
| **Ação** | Pontos por uma ação específica | 200 pontos por inscrição |
| **Evento** | Pontos por um evento no calendário | Pontos de aniversário |

3. Configure configurações adicionais de regra:
   - **Escopo / Filtros de Escopo** — Limite a regra a produtos, categorias ou níveis de associação específicos
   - **Valor Mínimo do Pedido** — Valor mínimo do carrinho para que a regra seja aplicada
   - **Níveis Permitidos** — Restrinja a regra a níveis de associação específicos
   - **É Exclusiva** — Quando ativado, esta regra não pode ser combinada com outras regras
   - **Dias de Pontos Pendentes** — Número de dias antes que os pontos ganhos fiquem disponíveis (útil para considerar janelas de devolução)
   - **Dias de Expiração dos Pontos** — Número de dias após o ganho antes que os pontos expirem (deixe em branco para não expirar)
   - **Início / Fim** — Restrinja a regra a um intervalo de datas

### Etapa 3: Configurar Recompensas

Recompensas são o que os clientes podem resgatar com seus pontos:

1. Navegue até **Fidelidade > Recompensas**
2. Crie recompensas como:
   - **Cupom de $5 de Desconto** — 500 pontos
   - **Frete Grátis** — 300 pontos
   - **10% de Desconto** — 1000 pontos

> **Os códigos de desconto não podem ser resgatados no momento.** Uma recompensa com **Tipo de Recompensa** definido como **Código de Desconto** — como o cupom de $5 de desconto ou o exemplo de 10% de desconto acima — atualmente falha ao resgatar.

O membro vê um erro claro e seus pontos são automaticamente devolvidos ao seu saldo, então nada é perdido, mas a recompensa ainda não está disponível para uso.

Este é um conserto intencional: o resgate costumava relatar sucesso enquanto silenciosamente deduzia pontos e emitia nada.

Se os membros mencionarem um resgate "não funcionando", este é o problema — não um novo problema.

As recompensas de desconto voltarão a funcionar novamente em uma liberação futura.

Isso não afeta as recompensas de Envio Grátis, Produto Grátis ou Experiência/Benefício.

### Passo 4: Criar Badges (Opcional)

Os badges reconhecem conquistas dos clientes:

1. Navegue até **Loyalty > Badges**
2. Crie badges para marcos:
   - **Primeira Compra** — Concedido após a primeira compra
   - **Grande Gasto** — Concedido após gastar $500+
   - **Cliente Fiel** — Concedido após 10 pedidos

Os badges podem incluir recompensas de pontos extras ao serem conquistados.

## Gerenciamento de Membros

### Lista de Membros

Veja todos os membros de fidelidade com:
- Nível e status atual
- Saldo de pontos
- Data de inscrição
- Atividade recente

### Principais Ganhadores de Pontos

O painel destaca seus membros mais ativos com uma classificação que mostra o ranking, nome, nível e pontos ganhos no período.

### Transações Recentes

Um log de transações mostra todas as atividades recentes de pontos. Os tipos de transação incluem:

| Tipo | Significado |
|------|---------|
| **Ganhar** | Pontos creditados de uma compra qualificada ou regra |
| **Resgatar** | Pontos gastos em uma recompensa |
| **Bônus** | Pontos extras de um badge, campanha ou concessão manual |
| **Ajuste** | Correção manual de pontos feita por um membro da equipe |
| **Revogar** | Pontos removidos (por exemplo, após o cancelamento de um pedido) |
| **Expirar** | Pontos que ultrapassaram sua data de validade |

### Ajustes Manuais de Pontos

Você pode adicionar ou deduzir pontos manualmente para qualquer membro:

1. Abra a página de detalhes do membro
2. Clique em **Ajustar Pontos**
3. Insira a quantidade de pontos (positivo para adicionar, negativo para deduzir)
4. Insira uma razão para o ajuste
5. Clique em **Salvar**

O ajuste é registrado como uma transação e é visível no histórico de transações do membro.

## Campanhas

Campanhas de fidelidade permitem que você execute promoções especiais:
- **Finais de semana com pontos duplos** — Aumente temporariamente as taxas de ganho de pontos
- **Eventos de pontos extras** — Conceda pontos extras por ações específicas
- **Promoções de avanço de nível** — Reduza o limite para avanço de nível

## Dicas

- Comece com regras simples de ganho de pontos (1 ponto por $1 gasto) e expanda ao longo do tempo.
- Defina metas de recompensa atingíveis para manter os membros engajados — se as recompensas parecerem inalcançáveis, os membros perderão o interesse.
- Use badges para gamificar a experiência e incentivar comportamentos específicos.
- Monitore a Taxa de Resgate — um programa saudável tem uma taxa de resgate de 10-30%.
- Execute campanhas durante períodos de baixa atividade para aumentar o engajamento.
- Use o gráfico de Pontos Ganhos vs. Pontos Resgatados para garantir que seu programa seja sustentável.