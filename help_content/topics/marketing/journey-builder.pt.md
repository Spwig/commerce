---
title: Builder de Viagem
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: O seletor de modelos com os oito modelos iniciais visíveis (Série de Boas-vindas,
    Onboarding de primeiro pedido, Pós-venda e avaliação, Oferta VIP vs. padrão, Recuperação de carrinho abandonado, Retomada de clientes inativos, Solicitação de avaliação pós-entrega,
    Alerta de estoque de volta) — substitui a imagem com os quatro modelos antigos no mesmo caminho, que agora está obsoleta.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

O **Builder de Viagem** é a área visual, com arrastar e soltar, onde você projeta o que uma [Viagem](/help/triggered-journeys) realmente faz — quais e-mails são enviados, quanto tempo esperar entre eles e se diferentes assinantes devem seguir caminhos diferentes. Em vez de preencher um formulário, você cria o fluxo como um fluxograma: caixas conectadas em uma tela que você pode reorganizar, ramificar e visualizar de uma olhada.

## Abrindo o construtor

Toda jornada tem seu próprio canvas do construtor. Você pode acessá-lo de duas formas:

- Criando uma nova jornada — preencha seu **Nome**, **Disparador** e público-alvo na página de configurações e clique em **Salvar** — você será direcionado diretamente para o construtor para começar a projetar imediatamente.
- Abrindo a página de configurações de uma jornada existente e clicando em **Designar jornada** no topo.

O construtor é um ambiente de trabalho em tela cheia com três áreas: uma **paleta** de tipos de etapas à esquerda, o **canvas** no meio e um painel de **configurações da etapa** à direita que aparece quando você seleciona algo.

![O canvas do Builder de Viagem mostrando uma série de boas-vindas com uma ramificação Sim/Não](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

No topo do canvas, um cabeçalho repete o **Disparador** e o **público-alvo** da jornada (ou "Todos os assinantes" se nenhum segmento estiver definido), para que você sempre saiba com quem está projetando sem sair do construtor. Use o botão **Voltar** para retornar à página de configurações da jornada.

## Os tipos de etapas

Arraste uma etapa da paleta da esquerda para o canvas, ou clique em um item da paleta para soltá-lo automaticamente. Quatro tipos de etapas estão disponíveis:

| Etapa | O que ela faz |
|------|----------------|
| **Enviar e-mail** | Envia uma das suas campanhas para o assinante. |
| **Esperar** | Pausa por um número definido de horas ou dias antes de continuar. |
| **Ramificação** | Divide o caminho em duas partes — **Sim** ou **Não** — com base em se o assinante pertence a um segmento que você escolher. |
| **Sair** | Encerra a jornada para o assinante. |

Toda jornada começa com uma única etapa de **Entrada**, criada automaticamente a primeira vez que você abrir o construtor. Ela mostra o disparador da jornada e não pode ser excluída — é simplesmente o ponto onde os assinantes entram no fluxo.

## Conectando etapas

Cada etapa tem um pequeno **ponto de conexão**: um na parte superior (entrada) e um ou mais na parte inferior (saída). Para conectar duas etapas, arraste do ponto de saída da etapa para o ponto de entrada da outra etapa — uma linha curva aparece vinculando-as.

Uma etapa de **Ramificação** tem dois pontos de saída em vez de um: um verde **Sim** e um vermelho **Não**. Conecte cada um para onde esse caminho deve levar — eles podem se juntar novamente mais tarde na mesma etapa (como no exemplo acima, onde ambos os caminhos levam de volta ao mesmo **Sair**) ou seguir caminhos totalmente diferentes.

Para reorganizar o layout, arraste uma etapa pelo seu corpo para re posicioná-la — linhas conectadas seguem automaticamente. Arraste uma parte vazia da área de fundo do canvas para rolar em torno dele, e use a roda do mouse para ampliar ou reduzir. Se você perder o controle do fluxo, clique em **Ajustar** na barra de ferramentas para realinhar e ampliar para que tudo fique visível na tela.

## Configurando uma etapa

Clique em qualquer etapa para abrir suas configurações no painel da direita:

{
  "Step": "Configuração",
  "------": "---------",
  "**Enviar e-mail**": "Selecione o **E-mail a enviar** em uma lista suspensa das suas campanhas.",
  "**Aguardar**": "Defina **Aguardar por** — um número mais **horas** ou **dias**.",
  "**Ramificação**": "Escolha **Se o assinante estiver no segmento** — o segmento que decide Sim vs. Não.",
  "**Sair**": "Nenhuma configuração — é apenas um ponto final."
}

![O painel da direita configurando uma etapa de Ramificação, com a tela de fundo embaçada](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

As alterações são salvas automaticamente assim que você selecionar um valor — não há um botão **Salvar** separado no painel. Cada etapa, exceto **Entrada**, tem um botão **Excluir etapa** no final de seu painel de configuração.

Os e-mails que você selecionar para as etapas de **Enviar e-mail** são campanhas comuns que você cria no construtor visual regular do Campaign Studio — linha de assunto, blocos de conteúdo, tudo. Deixe-os como **Rascunho** e apenas os selecione na lista suspensa aqui; o percurso envia-os por você, você nunca clica em Enviar neles pessoalmente.

## Começando a partir de um modelo

Não é sempre necessário construir um fluxo a partir de uma tela em branco — clique em **Modelos** na barra de ferramentas (ou **Procurar modelos** em uma tela em branco) para abrir um seletor com oito iniciadores prontos:

| Modelo | O que ele cria |
|----------|-----------------|
| **Série de boas-vindas** | Cumprimente novos assinantes, compartilhe o que você está fazendo, e depois uma dica de primeiro pedido. |
| **Onboarding de primeiro pedido** | Transforme um comprador pela primeira vez em um cliente recorrente com uma sequência de onboarding suave. |
| **Pós-venda e avaliação** | Agradeça após qualquer pedido, depois peça uma avaliação assim que ele chegar. |
| **Oferta VIP vs. padrão** | Após um pedido, ramificações no seu segmento VIP para enviar a oferta de follow-up certa para cada grupo. |
| **Recuperação de carrinho abandonado** | Lembre um comprador que deixou itens para trás, e depois uma notificação de follow-up um dia depois. |
| **Reenganche de clientes esquecidos** | Reengaje um cliente que não comprou há algum tempo com um motivo para voltar. |
| **Solicitação de avaliação pós-entrega** | Peça uma avaliação alguns dias após um pedido ser marcado como Entregue. |
| **Alerta de estoque de volta** | Informe ao cliente que está esperando o momento em que um produto que ele quer está disponível novamente. |

Cada modelo é pré-conectado ao gatilho correspondente — por exemplo, aplicar **Reenganche de clientes esquecidos** a um novo percurso também espera que o **Gatilho** desse percurso seja **Cliente esquecido (reenganche)**. Veja [Percurso disparado](/help/triggered-journeys) para o que dispara cada um desses eventos de gatilho e como os que focam em recuperação se comportam (janelas de inatividade, checkout de convidado, solicitações de avaliação por pedido, e como um percurso de estoque de volta substitui o alerta simples).

![O seletor de modelos mostrando os percurso iniciadores prontos](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Aplicar um modelo **substitui o fluxo atual** no painel, então use-o no início da criação de um percurso em vez de no meio. O Spwig reconecta cada etapa a um e-mail ou segmento real onde os nomes combinam com algo que você já tem; em qualquer lugar em que ele não consiga encontrar uma correspondência, o cabeçalho relata quantas etapas ainda precisam de um e-mail ou segmento escolhido para que você saiba exatamente o que terminar antes de ir para a vida real.

## Compartilhando percursos

Dois botões da barra de ferramentas permitem mover o design de um percurso entre etapas ou entre lojas:

- **Exportar** baixa o percurso como um arquivo `.journey.json` — uma descrição portátil da forma do fluxo (suas etapas, tempos de espera, ramos e caminhos Sim/Não) mais os *nomes* dos e-mails e segmentos usados em cada etapa. Ele não inclui os próprios designs dos e-mails ou quaisquer dados de assinantes.
- **Importar** carrega um arquivo `.journey.json` no percurso atual, substituindo o que está no painel.

Isso é útil para fazer backup de um fluxo do qual você se orgulha, entregar uma série de boas-vindas comprovada a outra loja Spwig, ou reconstruir um percurso após clonar sua loja para uma instalação nova.

Preserve todos os formatações de markdown, caminhos de imagens, blocos de código e termos técnicos.

Assim como nos modelos, o Spwig re-vincula e-mails e segmentos por nome quando uma correspondência existe na loja de destino, e sinaliza tudo que não pôde ser correspondido para que você possa concluir a configuração.

## Ativando sua jornada

Quando o fluxo estiver pronto, use o controle de status no canto superior direito do construtor. Um selo mostra o status atual da jornada — **Rascunho**, **Ativa** ou **Pausada** — ao lado de um botão **Ativar**.

Ao clicar em **Ativar**, o sistema **verifica o fluxo primeiro**. Se algo impedir o funcionamento, a ativação é bloqueada e um banner lista os problemas — por exemplo, uma etapa de **Enviar e-mail** sem nenhum e-mail selecionado, um **Ramal** sem segmento ou sem caminho Sim/Não, um e-mail ou segmento que foi excluído posteriormente, ou um loop que rodaria para sempre. Cada problema é clicável: ao selecioná-lo, o sistema salta para a etapa problemática, que é destacada em vermelho até que você a corrija. Avisos (como uma etapa inacessível ou uma **Espera** sem atraso definido) também são listados, mas não bloqueiam a ativação.

![Ativação bloqueada, com o problema listado em um banner e a etapa problemática destacada em vermelho](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Quando o fluxo passa na verificação, o selo muda para **Ativa** e a jornada começa a inscrever assinantes sempre que seu gatilho for acionado. O botão se torna **Pausar**, que interrompe novas inscrições — assinantes que já estão em andamento continuam recebendo suas etapas restantes. Veja [Jornadas acionadas](/help/triggered-journeys) para entender como inscrição, tempos de espera e status interagem.

## Vendo quem está na jornada

Quando uma jornada está ativa, cada etapa mostra um pequeno **selo de contagem** em seu canto: o número de assinantes que estão nessa etapa neste momento. É uma forma rápida de ver para onde as pessoas estão fluindo e onde estão se acumulando — um número grande em uma etapa de **Espera** é esperado, enquanto um acúmulo logo antes de um e-mail específico pode merecer atenção. As contagens são atualizadas sempre que você retorna para a aba do construtor.

![O canvas com selos de contagem ao vivo nas etapas e o botão Ativar na barra de ferramentas](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Dicas

- Projete o fluxo enquanto ele ainda está em **Rascunho** — ninguém é inscrito até que você o **Ative**. Ativar a partir do construtor executa uma verificação rápida primeiro e não permite que um fluxo quebrado fique ativo, então não há risco de uma jornada parcialmente construída inscrever assinantes.
- Comece a partir de um **Modelo**, mesmo que você planeje personalizá-lo pesadamente — é mais rápido editar um fluxo existente do que construir um nó por nó, e ele demonstra o padrão de ramificação se você nunca o usou antes.
- Após aplicar um modelo ou importar um arquivo, verifique o cabeçalho por uma nota de etapas não correspondidas e preencha qualquer etapa de **Enviar e-mail** ou **Ramal** que não pôde ser correspondida antes de ativar.
- Clique em **Ajustar** sempre que um fluxo ficar largo (especialmente ramificações) — é a forma mais rápida de ver a forma inteira novamente após dar zoom ou mover a tela.
- Mantenha os nomes das etapas fáceis de ler, mantendo cada etapa de **Espera** imediatamente antes do e-mail que ela atrasa, em vez de agrupar várias esperas juntas.
- **Exporte** uma jornada funcional antes de fazer alterações significativas nela — é uma forma rápida de manter uma cópia de segurança que você pode reimportar se não gostar do resultado.