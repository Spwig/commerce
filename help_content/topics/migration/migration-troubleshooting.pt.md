---
title: Solucionando Problemas de Migração
---

A maioria das migrações completa-se sem incidentes, mas conexões falham, importações expiram e, ocasionalmente, uma execução para metade. Este tópico aborda a diagnose de uma conexão falha, a leitura do log de progresso enquanto uma importação está em execução, e — mais importante — quais são suas opções reais uma vez que algo dê errado, incluindo o que realmente fazem Retry, Cancel e Rollback.

## Falhas de conexão na etapa 2

A opção **Teste a conexão antes de prosseguir** está ativada por padrão e é sua primeira diagnose — ela valida as credenciais contra a plataforma de origem antes que você comite para o restante do assistente. Se falhar, a mensagem de erro normalmente aponta para uma dessas:

- **WooCommerce** — URL da loja faltando `https://` ou com um segmento de caminho no final; uma chave/segredo de consumidor digitada errada ou regenerada; ou uma chave de API REST criada sem permissão **Leitura** em **WooCommerce > Configurações > Avançado > API REST**.
- **Shopify** — Domínio da loja não está no formato `yourstore.myshopify.com`; ID/segredo do cliente de um aplicativo errado; ou, mais comumente, um aplicativo criado no painel de desenvolvedor, mas nunca realmente **instalado** — criar uma versão do aplicativo não é suficiente, você precisa do link de distribuição personalizado e de um clique em **Instalar**. O Spwig também avisa se `read_products`, `read_customers` ou `read_orders` não foram incluídos nas permissões do aplicativo.
- **Magento 2** — URL da loja apontando para a loja virtual em vez da raiz da API, ou um token de integração que foi criado, mas nunca ativado (**Salvar > Ativar > Permitir**).
- **Problemas de SSL** — um certificado expirado, autoassinado ou mal configurado falha na conexão antes que as credenciais sejam verificadas, aparecendo como um erro genérico em vez de um erro de autenticação. Se as credenciais parecem corretas, verifique o certificado em seguida.

Reexecute o teste de conexão após cada correção em vez de alterar várias credenciais de uma só vez — isso isola qual estava errada.

## Lendo o log ao vivo na etapa 5

Enquanto uma importação está em execução, a etapa 5 mostra um log de atividade conforme acontece. Clique em **Mostrar Detalhes** para expandi-lo em entradas individuais — nível e mensagem — em vez de apenas a resumo da etapa atual. Este é o método mais rápido para ver o que está acontecendo se o progresso parecer travado: uma parede de entradas "puladas" para um tipo de dados geralmente significa que "Pular itens existentes" está funcionando conforme o esperado, e não que algo esteja travado.

A visualização do log mostra apenas as **últimas 500 entradas**, então, em uma migração grande, as entradas mais antigas rolarão para fora da visão enquanto a importação ainda está em execução. Se você precisar do log completo após um tipo de dados ter terminado, use **Baixar Logs** na página de resultados em vez disso — ele não tem esse limite.

## O que uma migração falha realmente significa

Este é o ponto mais importante para entender se uma migração falhar.

Quando uma migração falha, a página de conclusão informa claramente o que aconteceu: os itens importados antes do erro ainda estão na sua loja, nada foi removido automaticamente, e corrigir o problema e executar a importação novamente pulará o que já foi importado na primeira vez. Aceite isso como está. Nenhuma etapa da importação é executada dentro de uma transação de banco de dados que poderia ser revertida como unidade — o que foi importado com sucesso antes do ponto de falha, produtos, categorias, clientes, pedidos, o que a tarefa conseguiu, permanece na sua loja exatamente como foi criado. Uma migração falha é uma **migração parcial**, e não uma que foi desfeita.

A falha também marca a tarefa como não reversível, então o botão **Rollback** não estará disponível em uma **importação** falha — ele só aparece uma vez que uma migração foi concluída, ou se um rollback de uma migração concluída falhou parcialmente, nesse caso, o Spwig oferece o botão novamente para que você possa tentar novamente. A única situação em que você mais desejaria um desfazer automático — uma importação falha — é exatamente a situação em que o botão não é oferecido.

Então, quando uma migração falha:


1. **Revise o que realmente foi importado**, usando as contagens de Importado/Ignorado/Falhado e os logs baixados para construir uma visão do que está no seu armazém versus o que não conseguiu ser importado.

2. **Decida como limpar.** Para uma quantidade pequena de dados parciais, revise-os manualmente e exclua o que não quiser através das visões de lista normal do administrador.

Para uma importação parcial maior ou mais desorganizada, é frequentemente mais rápido limpar os dados importados você mesmo antes de começar de novo do que reconciliá-los item por item.

3. **Reexecute com Skip existing items habilitado**, independentemente do caminho de limpeza que escolher — é o que impede os dados que sobreviveram de serem duplicados na próxima tentativa.

## Tente novamente

**Tente novamente** reinicia a importação completamente do início. Ele limpa os contadores e logs anteriores da tarefa e reimporta tudo do zero — ele **não** continua a partir do ponto em que a tentativa falhou. Mantenha **Skip existing items** habilitado para que os itens que já foram importados na primeira vez não sejam duplicados na segunda passagem.

Se uma migração parar porque atingiu o **limite de 4 horas**, a mensagem que você verá é precisa: executar a importação novamente começa do início e pula os itens que já foram importados, não um resumo de onde ela parou. Para uma loja grande o suficiente para atingir o limite de tempo, repetir a tarefa inteira raramente termina; em vez disso, reduza o escopo de cada execução selecionando menos tipos de dados na etapa 3 (produtos em uma execução, pedidos em outra) e faça várias passagens menores.

## Cancelar

**Cancelar** está disponível em uma migração em andamento, e marca a tarefa como falhada no painel imediatamente. Ele **não** para a tarefa de importação em segundo plano, que continua rodando e escrevendo dados até atingir um ponto de parada natural. Espere as contagens importadas continuarem subindo por um tempo após cancelar — deixe-as se estabilizarem antes de decidir o que limpar, em vez de agir com base nas contagens capturadas no momento em que clicou em Cancelar.

## Não há pausa ou retomada

O Spwig não suporta pausar uma migração em andamento e retomá-la posteriormente. O botão **Retomar** no painel é para um caso diferente: uma migração configurada pelo assistente, mas nunca iniciada. Ele reabre o assistente onde você parou de configurá-lo — não está relacionado a uma execução já em andamento.

## Rollback

> **Aviso:** O rollback é uma ação permanente e destrutiva. Leia esta seção completamente antes de usá-la.

O rollback é oferecido em uma migração **concluída**, e novamente em uma cujo próprio rollback falhou parcialmente (status **Rollback Falhou**), então um rollback travado pode ser reexecutado. Ele remove apenas o que a importação mesma criou, e mantém qualquer coisa em que sua loja agora depende:

- Um cliente migrado que fez um pedido real desde a importação é **mantido** — sua conta, endereços, histórico de fidelidade e crédito da loja permanecem com ele, e esse pedido real permanece inalterado. Apenas os pedidos criados pela importação são removidos.

- Um produto migrado que ainda é referenciado por qualquer pedido, conjunto, cartão-presente ou slot de configurador é **mantido**. Pedidos pertencentes a outros clientes nunca são modificados — o rollback não pode mais remover itens de linha de um pedido não relacionado ou deixá-lo com o total errado.

- O que for mantido é relatado de volta a você por nome e contagem, com a razão — por exemplo, "1 Produto mantido, ainda referenciado por um item de pedido" — para que você saiba exatamente o que ainda está lá e por quê.

- Afiliados, comissões e pagamentos criados pela importação **são** removidos, juntamente com qualquer conta de afiliado criada pela importação. Um afiliado anexado a um cliente que já existia mantém sua conta; apenas o registro do afiliado é removido.

- O histórico de fidelidade e o crédito da loja seguem o cliente: removidos se o cliente for removido, mantidos se o cliente for mantido.

Ele ainda **não** remove planos de assinatura, níveis de preços ou recursos de agendamento criados por extensões da loja — esses sobrevivem a um rollback e precisam ser limpos manualmente se você não quiser que fiquem.

Antes de confirmar, a página de confirmação mostra uma pré-visualização do que será removido e do que será mantido, calculado com base nos seus dados em tempo real — leia-a antes de clicar **Sim, Reverter Migração**.

O rollback é executado em segundo plano, em vez do seu navegador, então é seguro fechar a guia; verifique o status da migração para obter o relatório do que foi realmente removido e mantido após sua conclusão.

Como o rollback não vai além do que a importação criou, ele não é mais uma ferramenta de uso limitado a um dia — as encomendas reais de um cliente migrado e as vendas reais de um produto migrado estão protegidas independentemente do tempo decorrido desde a migração. Ele ainda é uma ação permanente e destrutiva nas linhas que realmente remove, então use-o com cuidado em vez de casualmente, e limpe manualmente qualquer coisa que o Spwig mantém que você realmente não quer.

Sobre a disponibilidade: o botão Reverter permanece em um resumo de migração concluída enquanto o registro da tarefa existir — para a maioria das plataformas, não há prazo fixo. O Magento é a exceção e perde a disponibilidade de reverter após uma janela definida, então decida rapidamente se estiver usando o Magento. Os registros de tarefas não são removidos em nenhum horário, então uma migração permanece reversível indefinidamente, a menos que você exclua seu registro manualmente.

## Estratégia para lojas grandes e importações lentas

Para uma loja grande o suficiente que uma única execução corra o risco do limite de 4 horas:

- **Aumente o tamanho do lote** na etapa 3 (até 100) — lotes maiores geralmente significam menos viagens de ida e volta e maior throughput.
- **Divida a migração em várias execuções por tipo de dados** — categorias e produtos em uma execução, clientes e pedidos em uma execução subsequente, em vez de tudo de uma só vez.
- **Mantenha Skip existing items ligado** para cada execução após a primeira, para que execuções repetidas não dupliquem o que já foi bem-sucedido.
- **Desative Importar imagens de produtos.** Baixar e processar cada imagem geralmente é o fator mais significativo em uma execução lenta. Você pode adicionar imagens aos produtos individualmente, ou por meio de uma importação CSV separada, uma vez que o restante dos dados estiver em vigor.

## Dicas

- **Teste a conexão após cada alteração de credencial**, e não apenas uma vez no final — isso isola qual valor está errado.
- **Nunca suponha que um trabalho falhado tenha limpo após si mesmo** — verifique o que realmente está em sua loja antes de decidir sobre a limpeza ou uma nova tentativa.
- **Skip existing items deve permanecer ligado para cada nova tentativa** — é a única coisa que impede duplicatas em uma segunda passagem.
- **Não lute contra o limite de 4 horas com mais tentativas** — divida por tipo de dados em vez disso.
- **Leia a pré-visualização de rollback antes de confirmar** — ela nomeia exatamente o que será removido e o que será mantido, calculado com base nos seus dados em tempo real, então não haverá surpresas.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step2/
  filename: step2-connection-test-failed.webp
  description: Formulário de conexão da etapa 2 mostrando um resultado de Teste de Conexão falhado e a mensagem de erro
  save-to: core/static/core/admin/img/help/migration-troubleshooting/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-rollback-panel.webp
  description: Painel de Reverter na página de conclusão com o texto de aviso e o botão Reverter Migração em um trabalho concluído
  save-to: core/static/core/admin/img/help/migration-troubleshooting/
  viewport: 1440x900
-->