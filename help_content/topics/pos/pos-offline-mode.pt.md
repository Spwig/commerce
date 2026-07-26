---
title: Modo Offline do POS & Instalação do Aplicativo
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA em repouso — visão principal de seleção de login/terminal mostrando a marca Spwig POS
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Add-to-Home-Screen screenshots (iPad Safari, Android Chrome) são específicas do sistema operacional/navegador
         capturas de referência anotadas. A sessão capturando isso deve usar emulação de dispositivo
         ou imagens de referência em vez de tentar disparar o prompt de instalação do navegador.
-->

O Spwig POS é um Progressive Web App (PWA). Ele executa totalmente no navegador e pode ser instalado na tela inicial de um dispositivo como um aplicativo nativo. Como o aplicativo, seu catálogo de produtos e histórico de pedidos recentes são armazenados localmente no dispositivo, seu caixa continua funcionando durante interrupções breves na rede e conexões lentas.

Este tópico explica exatamente o que funciona quando a conexão cai, como as vendas em fila são reconciliadas quando ela retorna, como instalar o POS na tela inicial de um dispositivo e como as atualizações chegam aos dispositivos instalados.

## Como o modo offline funciona

Quando você abre o POS pela primeira vez em um dispositivo, o navegador baixa e armazena em cache todo o aplicativo — sua interface, imagens e todo o código de suporte. Um componente de fundo chamado Service Worker gerencia esse cache. A partir desse momento, o aplicativo carrega do cache local mesmo que o servidor esteja inacessível.

Além do cache do aplicativo, o POS mantém um banco de dados local no dispositivo (usando o armazenamento IndexedDB embutido no navegador). Esse banco de dados contém:

- **Produtos e variantes** — sincronizados do seu catálogo e atualizados a cada cinco minutos enquanto online
- **Categorias** — sincronizadas no início e atualizadas junto com os produtos
- **Níveis de estoque** — sincronizados a cada dois minutos enquanto online (usando uma estratégia de rede-first que recorre aos dados em cache se o servidor não responder dentro de três segundos)
- **Registros de clientes** — até 1.000 clientes recentes
- **Histórico de pedidos** — um número configurável de pedidos recentes do POS (padrão: 500 pedidos em 14 dias; definido por terminal em **POS > POS Terminals**)
- **Imagens de produtos** — armazenadas localmente por até 24 horas

Quando o POS detecta que o dispositivo ficou offline, uma barra aparece no topo da tela: **"Modo Offline - As vendas serão sincronizadas quando a conexão for restaurada."** O caixa continua operando usando os dados armazenados localmente.

## Funcionalidades disponíveis offline

| Funcionalidade | Disponibilidade offline |
|----------------|--------------------------|
| Pesquisa e navegação por produtos | Disponível — usa o catálogo armazenado localmente |
| Leitura de códigos de barras | Disponível — as leituras procuram produtos no cache local |
| Adicionar itens ao carrinho | Disponível |
| Aplicar descontos manuais | Disponível |
| Aplicar códigos de voucher | Não disponível — verificação de saldo requer conexão ativa |
| Pagamentos em dinheiro | Disponível — registrados localmente e colocados em fila para sincronização |
| Pagamentos com cartão (Entrada Manual) | Disponível — o caixa processa em um terminal separado e insere a referência; registrados localmente e colocados em fila para sincronização |
| Pagamentos com cartão (leitor integrado — Stripe Terminal, etc.) | Não disponível — leitores de cartão integrados se comunicam com a rede de pagamento em tempo real |
| Pagamentos com cartões-presente | Não disponível — verificação de saldo requer conexão ativa |
| Pagamentos divididos combinando dinheiro e cartão manual | Disponível |
| Impressão de recibos em uma impressora de rede | Disponível se a impressora estiver na mesma rede local do dispositivo — a impressão não precisa de acesso à internet, apenas conectividade de rede local |
| Recibos digitais (e-mail/SMS/WhatsApp) | Não disponível — o envio requer conexão ativa |
| Navegação pelo histórico de pedidos | Disponível — mostra pedidos armazenados com uma barra indicando que você está visualizando dados offline |
| Devoluções e anulações | Não disponível — essas ações requerem conexão ativa |
| Consulta de pontos de fidelidade do cliente | Não disponível |
| Abrir e fechar turnos | Disponível — o estado do turno é armazenado localmente |

## Vendas em fila e sincronização quando a conexão retorna

As vendas offline não são perdidas.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Quando o registro não consegue acessar o servidor, cada venda concluída é gravada em uma fila local (o armazenamento `pendingTransactions` no banco de dados local do dispositivo).

A venda inclui todos os itens do carrinho, quantidades, preços, método de pagamento e o horário em que foi concluída.

Quando o acesso à internet é restaurado, o POS faz automaticamente:

1. Detecta a reconexão via o evento `online` do navegador
2. Mostra um banner: **"Sincronizando N transação(s) pendente(s)..."**
3. Envia as vendas em fila para o backend na ordem, usando um plano de repetição com back-off exponencial se o primeiro tentativa falhar (até 10 tentativas em uma janela máxima de cinco minutos por tentativa)
4. Marca cada venda como sincronizada uma vez que o backend confirmar

**Proteção contra duplicação de vendas** — cada venda em fila é atribuída um ID local único antes de sair do dispositivo. O backend verifica esse ID antes de criar um pedido. Se a mesma venda for enviada duas vezes (por exemplo, porque uma tentativa de repetição se sobrepôs com uma primeira tentativa bem-sucedida), o backend ignora a duplicada. Você nunca terminará com vendas contabilizadas duas vezes.

**Detecção de conflito** — em casos raros, o backend pode marcar uma venda em fila como conflito (por exemplo, se um produto foi excluído no servidor enquanto o dispositivo estava offline). Vendas em conflito aparecem em **POS > Configurações > Transações Pendentes** para que você possa revisá-las e resolvê-las manualmente.

**Ajustes de estoque offline** são tratados da mesma forma: alterações de estoque feitas enquanto offline são colocadas em fila e retransmitidas quando a conexão retornar. As figuras de estoque locais no dispositivo são atualizadas imediatamente para que o caixa veja uma contagem precisa (estimada).

## Instalando o POS em uma tela inicial de dispositivo

Instalar o POS em uma tela inicial fornece uma experiência em tela cheia sem a barra de endereço do navegador, um atalho ícone no dispositivo e tempos de inicialização mais rápidos.

### iPad (Safari)

1. Abra o Safari e navegue até o URL do POS do seu loja: `https://yourstore.com/pos/`
2. Faça login e conclua o emparelhamento inicial se for um novo dispositivo.
3. Toque no botão **Compartilhar** (o quadrado com uma seta para cima) na barra de ferramentas do Safari.
4. Role para baixo na folha de compartilhamento e toque em **Adicionar à Tela Inicial**.
5. Edite o nome se desejar (o padrão é "Spwig POS") e toque em **Adicionar**.

O ícone do POS agora aparece na tela inicial do seu iPad. Toque nele para abrir o app em tela cheia sem o chrome do navegador Safari.

> **Nota:** O Safari no iPad é necessário para a opção Adicionar à Tela Inicial. Navegadores de terceiros no iOS (Chrome, Firefox) não suportam a instalação de PWA até meados de 2025.

### Android (Chrome)

1. Abra o Chrome e navegue até o URL do POS do seu loja: `https://yourstore.com/pos/`
2. Faça login e conclua o emparelhamento se necessário.
3. Toque no **menu de três pontos** (canto superior direito) e toque em **Instalar app** (ou **Adicionar à Tela Inicial** em versões mais antigas do Chrome).
4. Confirme tocando em **Instalar**.

O ícone do POS aparece na tela inicial e no drawer de apps. Ao iniciar a partir do ícone, o app abre em modo standalone.

### Desktop (Chrome ou Edge)

1. Navegue até o URL do POS do seu loja no Chrome ou Edge.
2. Procure o **ícone de instalação** na barra de endereço do navegador (um monitor de computador com uma seta para baixo, ou um ícone de "+" dependendo da versão).
3. Alternativamente, abra o **menu de três pontos** e escolha **Instalar Spwig POS** (Chrome) ou **Apps > Instalar este site como um app** (Edge).
4. Confirme a instalação.

O POS abre como uma janela standalone sem guias do navegador ou a barra de endereço. Ele aparece na lista de apps do seu sistema e pode ser fixado na barra de tarefas.

## Como o app é atualizado

O POS gerencia suas próprias atualizações através do Service Worker. Você não precisa visitar uma loja de apps ou baixar algo manualmente.

**Ciclo de atualização:**

1.

Cada vez que você abrir o POS (ou a guia se tornar ativa após estar em segundo plano), o Service Worker verifica o servidor por uma nova versão.
2.

Se uma nova versão estiver disponível, o Service Worker a baixa em segundo plano enquanto você continua trabalhando — sua sessão atual não é interrompida.
3.

A atualização entra em vigor na próxima vez que você abrir o POS.

Se o app já estiver aberto e uma sincronização estiver pendente, o POS aguarda a fila esvaziar antes de sinalizar que uma recarregamento está pronto, para evitar interromper um turno ativo com vendas não sincronizadas.

**O que "recarregar" significa quando há vendas pendentes** — se você vir uma solicitação para recarregar para uma atualização e tiver vendas offline pendentes, encerre o turno atual de forma limpa (ou espere até que o banner de sincronização desapareça) antes de recarregar. Recarregar enquanto as vendas estão na fila não as apaga — elas permanecem no banco de dados local — mas é mais seguro sincronizar primeiro para confirmar que foram recebidas.

**Verificando a versão instalada** — abra o POS, toque no **ícone de menu** (três linhas horizontais) e vá para **Configurações**. A versão atual do build é mostrada na parte inferior do painel de configurações.

## Armazenamento e limpeza da instalação

O POS armazena vários tipos de dados localmente:

| O que | Tamanho típico |
|------|-------------|
| Shell do app (HTML, CSS, JS, ícones) | ~3–5 MB |
| Catálogo de produtos (texto e metadados) | 1–10 MB dependendo do tamanho do catálogo |
| Imagens de produtos (cachê) | 5–50 MB dependendo do tamanho do catálogo |
| Histórico de pedidos | 1–5 MB (500 pedidos) |
| Registros de clientes | 1–3 MB (1.000 clientes) |
| Fila de transações pendentes | Mínimo; limpa durante a sincronização |

**Se o dispositivo estiver com pouca armazenamento** — os navegadores aplicam pressão ao armazenamento em cache quando o dispositivo estiver cheio. O POS define seus caches como persistentes onde o navegador permite, mas em dispositivos muito cheios o navegador pode excluir as imagens de produtos primeiro. Se as imagens pararem de carregar, o POS as recarregará na próxima sincronização. As vendas sincronizadas e a shell do app não são afetadas.

**Reiniciando a instalação** — se o POS estiver se comportando de forma inesperada (preso em uma versão antiga, catálogo não atualizando, sincronização permanentemente presa), você pode executar um reinício limpo:

1. **Desinstale o app** — no mobile, pressione e segure o ícone do POS e escolha **Remover** ou **Desinstalar**. No desktop, clique com o botão direito na barra de título da janela do app e escolha **Desinstalar**.
2. Abra diretamente o URL do POS no navegador e faça o login novamente.
3. O dispositivo será solicitado novamente pelo código de emparelhamento de 8 caracteres do terminal. Você pode encontrar ou regenerar esse código no admin em **POS > Terminais POS** — abra o terminal e clique em **Regenerar código de emparelhamento**.
4. Um emparelhamento fresco força uma re-sincronização completa de todos os dados em cache.

> **Após o reinício**: quaisquer vendas offline que estavam na fila, mas não foram sincronizadas antes do reinício, serão perdidas, pois o banco de dados local é limpo. Sempre garanta que a conexão esteja restaurada e o banner de sincronização desapareça antes de reiniciar uma instalação.

## Solução de problemas

### O POS está preso em uma versão antiga

O Service Worker pode não ter ativado a nova versão ainda. Tente fechar todas as guias do navegador que têm o POS aberto, depois reabrir o POS. Se o problema persistir, reinicie a instalação conforme descrito acima.

### O banner "Sem conexão" não desaparece

Verifique se o dispositivo tem acesso à internet fora do POS (tente carregar outro site). Se o dispositivo estiver online, mas o banner persistir:

- O servidor do POS pode estar temporariamente inacessível — espere um minuto e o POS tentará novamente automaticamente.
- Se você estiver em uma rede que requer uma página de login (portal cativo), abra uma nova guia do navegador, conclua o login e depois retorne ao POS.

### Um produto está faltando no POS, mas existe no admin

O POS sincroniza produtos a cada cinco minutos enquanto está online. Se você adicionou um produto no admin há muito pouco tempo, toque no **ícone de menu** e vá para **Configurações > Sincronizar Agora** para disparar uma sincronização imediata. Se o produto ainda não aparecer, confirme se ele está marcado como **Ativo** e não está excluído da disponibilidade no POS nas configurações do produto.

### Transações pendentes estão presas no status "Conflito"

Vá para **POS > Configurações** (no próprio app do POS) e verifique o painel de **Transações Pendentes**.

Transações em conflito geralmente são causadas por um produto ou preço que mudou entre o momento em que a venda foi feita offline e quando foi sincronizada.


Você pode visualizar os detalhes da venda e, se a venda foi recebida corretamente, marcá-la como revisada.

## Dicas

- Execute o POS em um dispositivo dedicado que permaneça conectado ao seu Wi-Fi local. Quedas breves de Wi-Fi são tratadas automaticamente, mas um dispositivo que passa longos períodos offline precisará de mais tempo para re-sincronizar quando se reconectar.
- Os intervalos de sincronização são por dispositivo. Se você tiver múltiplos terminais, cada um sincroniza independentemente. Uma venda em um terminal aparece imediatamente no administrador ao sincronizar, mas o cache de pedidos local do outro terminal só atualiza em seu próprio ciclo de sincronização.
- Antes de uma interrupção planejada da internet (por exemplo, ao se mover para um evento sem Wi-Fi), abra o POS enquanto ainda estiver conectado para que o catálogo e os dados de estoque estejam totalmente atualizados. Vendas em dinheiro serão enfileiradas de forma confiável; apenas evite pagamentos integrados por cartão até que você volte online.
- Se você precisar apenas de vendas em dinheiro em um evento, o método de pagamento por cartão manual (o caixa processa em um terminal autônomo e insere uma referência) também funciona offline para transações por cartão.
- Mantenha o dispositivo conectado durante um turno longo — o banco de dados local e o processo de sincronização não afetam significativamente a bateria em comparação com a tela, mas um dispositivo carregado sempre é mais seguro para negociação.