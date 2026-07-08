---
title: Gerenciamento de Comissões
---

O gerenciamento de comissões é o processo de revisão e aprovação de ganhos de afiliados para garantir que apenas vendas legítimas sejam creditadas. Este guia mostra como revisar comissões pendentes, aprovar as válidas, rejeitar pedidos fraudulentos ou devolvidos e gerenciar comissões de forma eficiente usando ações em lote.

## Painel de Comissões

Navegue até **Marketing > Comissões** para acessar o painel de gerenciamento de comissões.

O painel fornece uma visão geral da atividade de comissões em todos os programas de afiliados:

| Estatística | Descrição |
|-------------|---------|
| **Comissões Pendentes** | Número de comissões aguardando sua revisão |
| **Comissões Aprovadas** | Comissões confirmadas e prontas para pagamento |
| **Comissões Pagas** | Comissões que foram pagas aos afiliados |
| **Comissões Rejeitadas** | Comissões recusadas devido a fraudes, devoluções ou violações de políticas |
| **Valor Pendente de Pagamento** | Valor total das comissões aprovadas, mas não pagas |

Essas estatísticas ajudam você a acompanhar sua carga de trabalho de revisão e monitorar o impacto financeiro do seu programa de afiliados.

![Painel de Comissões](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Visualizando Comissões

A lista de comissões exibe todos os registros de comissões em ordem cronológica.

### Colunas da Lista

| Coluna | Descrição |
|--------|---------|
| **Afiliado** | Nome e código único do afiliado |
| **Programa** | O programa de afiliados que gerou essa comissão |
| **Pedido** | Número do pedido (clique para ver os detalhes completos do pedido) |
| **Valor** | Valor da comissão em sua moeda de loja |
| **Status** | Pendente, Aprovada, Rejeitada ou Paga |
| **Criado** | Quando a comissão foi gerada |

### Filtros de Comissões

Use a barra lateral de filtro para estreitar as comissões:

- **Por Status** — Mostrar apenas comissões pendentes, aprovadas, rejeitadas ou pagas
- **Por Afiliado** — Ver comissões para um parceiro específico
- **Por Programa** — Ver comissões de um programa de afiliados específico
- **Por Faixa de Data** — Filtrar por data de criação

### Buscando Comissões

Use a barra de pesquisa para encontrar comissões específicas:

- Insira um **número de pedido** para encontrar uma comissão para uma venda específica
- Insira um **código de afiliado** para ver todas as comissões de um parceiro

## Detalhes da Comissão

Clique em qualquer comissão na lista para ver seus detalhes completos.

### Campos de Detalhes

A visualização de detalhes mostra:

- **Informações do Pedido** — Clique no número do pedido para ver o pedido completo em uma nova guia, incluindo itens, endereço de envio, status de pagamento e detalhes do cliente
- **Informações do Afiliado** — Nome, código, e-mail de pagamento e status de associação ao programa do afiliado
- **Detalhes do Programa** — Nome do programa, tipo de comissão (percentual ou fixa) e taxa de comissão
- **Marcadores de Tempo** — Data de criação, data de aprovação/rejeição e data de pagamento
- **Seção de Notas** — Notas internas visíveis apenas aos vendedores (explicado abaixo)

Essas informações ajudam você a verificar a legitimidade da comissão antes de aprova-la.

## Aprovação de Comissões

A aprovação de uma comissão confirma que ela é válida e adiciona-a ao saldo disponível do afiliado, tornando-a elegível para pagamento.

### Quando Aprovar

Aprove comissões quando:

- **Pedido foi entregue com sucesso** — Produto foi enviado ou conteúdo digital entregue
- **Nenhuma devolução ou reembolso** — O cliente não solicitou uma devolução (considere aguardar 14-30 dias após a entrega)
- **Padrões de qualidade atendidos** — A venda atende aos termos do seu programa (ex: não é uma autoreferência, cliente usou método de pagamento legítimo)
- **Nenhuma fraude detectada** — O pedido passa pela análise de fraude (verifique IP, descompasso entre endereço de cobrança/envio, padrões incomuns de pedidos)

### Como Aprovar

**Aprovação de uma Única Comissão:"

1. Navegue até **Marketing > Comissões**
2. Clique na comissão que deseja aprovar
3. Clique no botão **Aprovar** no topo da página de detalhes
4. Adicione opcionalmente uma nota (ex: "Aprovada após entrega bem-sucedida")
5. O status muda para **Aprovada** e a comissão é adicionada ao saldo do afiliado

**Aprovação em Lote:"

1. Navegue até **Marketing > Comissões**
2. Marque as caixas ao lado das comissões que deseja aprovar
3. Selecione **Aprovar Selecionadas** no menu suspenso **Ações**
4. Clique em **Ir**
5. Todas as comissões selecionadas mudam para o status **Aprovada**

Comissões aprovadas aparecem no painel do afiliado como saldo disponível e podem ser incluídas no próximo lote de pagamento.

## Rejeição de Comissões

A rejeição de uma comissão a remove do saldo do afiliado e marca-a como inelegível para pagamento.

### Quando Rejeitar

Rejeite comissões quando:

- **Pedido fraudulento** — O pedido mostra sinais de fraude (método de pagamento roubado, descompasso de IP, afiliado usando seu próprio link)
- **Cliente devolveu o produto** — O cliente devolveu itens para um reembolso total
- **Problemas de qualidade** — A venda não atende aos termos do programa (ex: afiliado violou diretrizes de publicidade)
- **Violação de termos** — O afiliado usou métodos proibidos de promoção (spaming, licitação de marcas, preenchimento de cookies)
- **Pedido cancelado** — O cliente cancelou antes da entrega

### Como Rejeitar

**Rejeição de uma Única Comissão:"

1. Navegue até **Marketing > Commissões**
2. Clique na comissão que deseja rejeitar
3. Clique no botão **Rejeitar** no topo da página de detalhes
4. **Adicione uma nota** explicando o motivo (altamente recomendado para resolução de disputas)
5. O status muda para **Rejeitada**

**Rejeição em Lote:"

1. Navegue até **Marketing > Comissões**
2. Marque as caixas ao lado das comissões que deseja rejeitar
3. Selecione **Rejeitar Selecionadas** no menu suspenso **Ações**
4. Clique em **Ir**
5. Todas as comissões selecionadas mudam para o status **Rejeitada**

Comissões rejeitadas são removidas do saldo do afiliado e não podem ser pagas. Elas permanecem visíveis no histórico de comissões para fins de registro.

## Ações em Lote

As ações em lote permitem que você aprovem ou rejeite várias comissões de uma vez, economizando tempo ao processar lotes grandes.

### Usando Ações em Lote

1. Navegue até **Marketing > Comissões**
2. Filtre a lista para mostrar apenas as comissões que deseja processar (ex: filtre por status **Pendente**)
3. Marque a caixa ao lado de cada comissão, ou clique na caixa do cabeçalho para selecionar todas na página atual
4. Escolha uma ação no menu suspenso **Ações**:
   - **Aprovar Selecionadas** — Marque todas as comissões selecionadas como aprovadas
   - **Rejeitar Selecionadas** — Marque todas as comissões selecionadas como rejeitadas
5. Clique em **Ir**
6. Revise a mensagem de confirmação mostrando quantas comissões foram atualizadas

### Processamento em Lote Eficiente

- **Filtrar por programa** — Aprove todas as comissões de um afiliado de alto desempenho confiável de uma vez
- **Filtrar por faixa de data** — Processar comissões com mais de 14 dias (fora do seu período de devolução)
- **Revisar comissões de alto valor separadamente** — Use ações em lote para comissões pequenas, revise manualmente comissões grandes

## Notas de Comissão

O campo de notas permite que você documente suas decisões e comunique-se com sua equipe.

### Adicionando Notas

Notas podem ser adicionadas:

- **Durante a aprovação** — Clique na comissão, adicione uma nota no campo de notas, depois clique em **Aprovar**
- **Durante a rejeição** — Adicione uma nota explicando o motivo da rejeição
- **A qualquer momento** — Clique na comissão, adicione ou edite a nota no campo de notas e salve

### Quando Usar Notas

- **Comissões rejeitadas** — Documente sempre o motivo ("Cliente devolveu o pedido #12345 em 2/10/26")
- **Comissões de alto valor** — Anote os passos de verificação tomados ("Verificado a entrega via rastreamento #ABC123")
- **Comissões contestadas** — Documente a comunicação com o afiliado
- **Padrões de fraude** — Anote atividades suspeitas para referência futura

As notas são **apenas internas** — os afiliados não podem vê-las. Elas servem como sua ferramenta de registro.

## Fluxo de Comissão

Aqui está o fluxo completo de gerenciamento de comissões:

```
Pedido Feito → Comissão Criada (Pendente)
                      ↓
              Merchant Reviews
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Aprovada     Rejeitada
                ↓           ↓
        Pronta para Pagamento  Não Pagável
                ↓
        Incluída no Pagamento
                ↓
              Paga
```

**Exemplo de Cronograma:"

- **Dia 1:** Cliente faz um pedido de $100 via link de afiliado → comissão de $10 criada (Pendente)
- **Dia 15:** Pedido entregue e período de devolução expirado → vendedor aprova a comissão
- **Dia 20:** Vendedor processa o lote de pagamento mensal → status da comissão muda para Paga
- **Dia 21:** Afiliado recebe o pagamento via PayPal

## Boas Práticas

### Janela de Revisão

Estabeleça um horário consistente para revisão:

- **Revisões diárias** — Processar comissões pendentes todas as manhãs (recomendado para programas de alto volume)
- **Revisões semanais** — Reserve um tempo toda segunda-feira para aprovar as comissões da semana anterior
- **Revisões quinzenais** — Alinhe com seu cronograma de pagamento (aprovar comissões no meio do mês, processar pagamentos no final do mês)

### Verificação de Qualidade

Antes de aprovar comissões, verifique:

1. **Pedido foi entregue** — Verifique o status do pedido no painel de administração
2. **Pagamento foi confirmado** — Verifique se o método de pagamento foi processado com sucesso
3. **Período de devolução expirado** — Aguarde 14-30 dias após a entrega para considerar devoluções
4. **Nenhuma bandeira de fraude** — Revise o pedido para padrões suspeitos (endereços desalinhados, países de alto risco, múltiplos pedidos do mesmo IP)
5. **Afiliado em bom estado** — Verifique o histórico do afiliado para fraudes ou violações anteriores

### Prevenção de Fraude

Fique atento a esses sinais vermelhos:

- **Autoreferências** — Afiliado fazendo pedidos usando seu próprio link de rastreamento
- **Preenchimento de cookies** — Proporção anormalmente alta de cliques para conversões com valores de pedido baixos
- **Pedidos duplicados** — Múltiplos pedidos do mesmo cliente/IP via o mesmo link de afiliado
- **Mismatches de geolocalização** — Afiliado no país A gerando vendas exclusivamente no país B
- **Chargebacks** — Taxa alta de chargebacks em pedidos referidos por afiliados

Se detectar fraude, **rejeite as comissões** e considere encerrar a associação do afiliado ao programa.

### Comunicação com Afiliados

- **Estabeleça expectativas** — Documente claramente sua política de aprovação de comissões nos termos do programa
- **Seja transparente** — Se rejeitar comissões, considere enviar um e-mail ao afiliado explicando o motivo (use as notas como referência)
- **Responda a contestações** — Se um afiliado questionar uma rejeição, revise as notas e detalhes do pedido
- **Publique diretrizes** — Crie uma página "Política de Aprovação de Comissões" no portal do afiliado para evitar confusões

## Dicas

- Aprova comissões **após o fechamento do período de devolução** (normalmente 14-30 dias) para evitar aprovar pedidos que os clientes devolvam posteriormente
- Use **ações em lote com filtros** para processar eficientemente comissões de afiliados confiáveis, enquanto revisa manualmente novos ou afiliados de alto risco
- Documente os motivos de rejeição no **campo de notas** — isso protege você se um afiliado contestar a decisão e ajuda a identificar padrões
- Fique atento a **autoreferências** — é uma violação comum onde afiliados usam seus próprios links para ganhar comissões em compras pessoais
- Estabeleça um **limite mínimo de aprovação** — por exemplo, aprovar automaticamente comissões abaixo de $10, mas revisar manualmente qualquer coisa acima de $50 para equilibrar eficiência com risco
- Crie uma **lista de verificação de fraude** — padronize seu processo de revisão com uma lista de sinais vermelhos (mismatch de IP, padrões suspeitos de pedidos, métodos de pagamento de alto risco)
- Monitore **taxas de rejeição por afiliado** — se um afiliado tiver muitas rejeições, pode indicar fraude ou a necessidade de mais treinamento sobre os termos do programa

Lembre-se: Mantenha todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.