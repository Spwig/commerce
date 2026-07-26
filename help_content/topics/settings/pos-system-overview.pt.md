---
title: Visão Geral do Sistema POS
---

O sistema POS do Spwig transforma sua loja em uma solução de varejo completa com terminais de ponto de venda modernos. Ele está incluído em todas as edições — Comunidade, Profissional e Empresarial — com terminais ilimitados em locais ilimitados, sem custo adicional. Cada terminal é uma Progressive Web App (PWA) que funciona offline, sincroniza automaticamente e integra-se de forma perfeita com seu estoque, dados de clientes e processamento de pagamentos. Gerencie tudo a partir do painel de administração — configuração do terminal, reconciliação de turnos, personalização de recibos e integração de hardware.

Use o sistema POS quando tiver lojas físicas, lojas pop-up, feiras de negócios ou qualquer ambiente em que os clientes realizem compras presencialmente, em vez de online.

![Painel do POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## O que é o Spwig POS?

O Spwig POS é um sistema de ponto de venda totalmente integrado, projetado para comerciantes que vendem online e em locais físicos. Ao contrário de sistemas de POS de terceiros que exigem integrações complexas, o Spwig POS é construído diretamente em sua plataforma, garantindo uma sincronização perfeita de dados em todos os canais de venda.

**Características Principais**:
- **Terminais Ilimitados** - Implante tantos terminais quantos forem necessários, sem custo adicional
- **Arquitetura Offline-First** - Continua processando vendas mesmo quando a conectividade de internet for perdida
- **Progressive Web App** - Nenhuma instalação em lojas de apps; acesso via navegador em qualquer dispositivo (tablets, computadores, terminais dedicados)
- **Sincronização de Estoque Real** - Reserva de estoque (TTL de 15 minutos) evita a super venda em canais
- **Suporte a Pagamento Dividido** - Aceite múltiplos métodos de pagamento por transação (dinheiro + cartão + cartão-presente)
- **Integração de Hardware** - Impressoras térmicas ESC/POS, leitores de código de barras, caixas registradoras, telas de cliente
- **Gerenciamento de Turnos** - Conciliação de caixa com contagens de abertura/fechamento e rastreamento de discrepâncias
- **Pronto para Multi-Local** - Grupos de lojas com herança de configurações para gerenciamento de franquias e regionais

## Edições

O POS está incluído em todas as edições do Spwig — Comunidade, Profissional e Empresarial — desde a versão 1.5.8 do Spwig. Não há licença de POS separada, nenhum passo de ativação e nenhuma taxa por terminal.

**O que está incluído em todas as edições**:
- Registros ilimitados de terminais
- Atribuições ilimitadas de funcionários
- Todas as funcionalidades do POS (turnos, gerenciamento de caixa, personalização de recibos, telas de cliente)
- Integrações com provedores de pagamento (Stripe Terminal e outros provedores suportados)
- Suporte à integração de hardware

Comerciantes que operam lojas hospedadas no Spwig ou pagam por uma licença Profissional/Empresarial obtêm limites mais altos nos serviços hospedados no Spwig (GeoIP, geocodificador, notificações por push) e suporte prioritário, mas o conjunto de funcionalidades do POS em si é idêntico em todas as edições.

## Arquitetura do Sistema

**Frontend** - Progressive Web App com React 18:
- Primeiro offline com cache de Service Worker (funciona sem internet)
- Sistema de build Vite para carregamento rápido
- CSS Modules + tokens de design (consistente com o tema da sua loja)
- IndexedDB para persistência de dados locais
- 10 idiomas suportados (Inglês, Chinês Simplificado/Tradicional, Francês, Alemão, Espanhol, Português, Japonês, Russo, Árabe)

**Backend** - Integração do Backend:
- 13 modelos de POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- Mais de 43 endpoints REST para operações de terminal
- Sistema de reserva de estoque com gerenciamento de TTL
- Tarefas do Celery para sincronização em segundo plano
- Armazenamento criptografado de credenciais para provedores de pagamento

**Segurança**:
- Emparelhamento de terminal via códigos de 8 caracteres (gerados no lado do servidor, expiram após o uso)
- Controle de atribuição de funcionários que usuários podem acessar quais terminais
- Capacidade de bloqueio/desbloqueio remoto para emergências de administração
- Credenciais criptografadas de provedores de pagamento
- Autenticação baseada em sessão com suporte a desbloqueio biométrico (dependente do navegador)

## Fluxo de Trabalho para Iniciar

Siga estas 4 etapas para implantar seu primeiro terminal POS.

Para obter um checklist passo a passo completo, incluindo configuração de equipe, provedores de pagamento e execução da primeira venda, veja [Getting Started with POS](getting-started-with-pos).

**Etapa 1: Criar Armazém**
- Navegue até **Catalog > Warehouses**
- Crie um armazém que represente sua localização de varejo
- Configure o endereço e as informações de contato
- Esse armazém rastreará o estoque físico para vendas no POS

**Etapa 2: Registrar Terminal**
- Navegue até **POS > Terminals**
- Clique em **+ Adicionar Terminal**
- Defina o nome do terminal (ex.: "Caixa Principal", "Checkout 1")
- Atribua o armazém da Etapa 2
- Configure as configurações de hardware (impressoras, scanners, caixa registradora)
- Salve para gerar um código de emparelhamento de 8 caracteres

**Etapa 3: Atribuir Equipe**
- Na configuração do terminal, role até **Assigned Users**
- Selecione os membros da equipe autorizados a usar esse terminal
- Apenas usuários atribuídos podem fazer login no terminal
- Os usuários devem ter permissões adequadas de POS em seu papel de equipe

**Etapa 4: Emparelhar Dispositivo**
- No seu dispositivo de terminal (tablete/computador), navegue até o URL `/pos/`
- Insira o código de emparelhamento de 8 caracteres da Etapa 3
- O terminal baixa a configuração e sincroniza os dados iniciais
- Faça login com as credenciais da equipe atribuída
- O terminal está pronto para vendas

Após o emparelhamento, os terminais sincronizam automaticamente a cada 5 minutos (configurável). O modo offline permite a operação contínua quando a internet não estiver disponível — as vendas sincronizam automaticamente quando a conectividade retornar.

## Funcionalidades Principais do POS

**Processamento de Vendas**:
- Pesquisa de produtos por nome, SKU ou código de barras
- Divisão de pagamento (múltiplos métodos de pagamento por pedido)
- Cestas de compras pendentes (salve transações incompletas)
- Devoluções e anulações com rastreamento de motivo
- Aplicação de descontos (cupons, cartões-presente, promoções)
- Pesquisa de clientes e resgate de pontos de fidelidade

**Gestão de Caixa**:
- Abertura de turno com contagem inicial de dinheiro
- Fechamento de turno com reconciliação entre esperado e real
- Movimentos de dinheiro (adicionais de flutuação, saques de dinheiro de pequeno valor com razões)
- Cálculo automático de dinheiro esperado com base em vendas em dinheiro
- Rastreamento e relatórios de discrepâncias

**Integração de Hardware**:
- Impressoras de recibos térmicas ESC/POS (rede ou serial)
- Scanners de código de barras USB
- Acionamento de caixa registradora via pulso da impressora
- Displays para clientes (carrossel promocional durante o tempo ocioso)
- Leitores de cartões Stripe Terminal (S700, WisePOS E, P400)

**Funcionalidades Offline**:
- O Service Worker armazena todos os ativos do terminal em cache
- O IndexedDB armazena pedidos recentes (configurável: 7-30 dias, 200-1000 pedidos)
- Reserva de estoque com TTL de 15 minutos previne a super venda
- Fila de vendas para sincronização quando a conectividade retornar
- Detecção automática de reconexão

## Páginas de Administração do POS

Acesse estas páginas de administração para gerenciar todos os aspectos de sua implantação do POS:

**Painel do POS** (`/admin/pos/`)
- Visão geral do sistema e estatísticas rápidas
- Atividade recente de terminais
- Resumo de turnos ativos
- Tijolos de uso de serviços hospedados (GeoIP, geocoder, push — veja [Spwig Hosted Services](hosted-services))

**Gerenciamento de Terminais** (`/admin/pos_app/posterminal/`)
- Registre e configure terminais
- Atribua equipes e armazéns
- Monitore o status online/offline (rastreamento de batimento cardíaco)
- Desbloqueie terminais remotamente
- [Saiba mais: Gerenciando Terminais POS](managing-pos-terminals)

**Gerenciamento de Turnos** (`/admin/pos_app/posshift/`)
- Visualize todos os turnos (abertos, fechados, históricos)
- Revise relatórios de reconciliação de dinheiro
- Rastreie movimentos de dinheiro e discrepâncias
- Auditoria da atividade do turno
- [Saiba mais: Turnos POS e Gestão de Caixa](pos-shifts-cash-management)

**Grupos de Lojas** (`/admin/pos_app/storegroup/`)
- Organize terminais por localização/região
- Configure configurações de nível de grupo (moeda, idioma, fuso horário)
- Implemente hierarquia de herança de configurações
- [Saiba mais: Grupos de Lojas POS](pos-store-groups)

**Modelos de Recibo** (`/admin/pos_app/receipttemplate/`)
- Personalize recibos impressos (largura do papel, logotipo, cabeçalho/rodapé)
- Configure campos de conformidade (ID fiscal, registro comercial)
- Adicione códigos QR para promoções
- Defina escopo de modelos para lojas ou grupos específicos
- [Saiba mais: Personalização de Modelos de Recibo](receipt-template-customization)

**Slides de Promoção** (`/admin/pos_app/promoslide/`)
- Crie conteúdo de carrossel para exibição ao cliente
- Direcione slides para lojas ou grupos específicos
- Agende promoções sazonais
- [Saiba mais: Slides de Promoção para Exibição ao Cliente](customer-display-promo-slides)

**Fornecedores de Pagamento** (`/admin/pos_app/posterminalprovider/`)
- Configure a integração do Stripe Terminal
- Gerencie credenciais de fornecedores de pagamento
- Monitore o status da conexão
- [Saiba mais: Fornecedores de Terminal de Pagamento](payment-terminal-providers)

**Leitores de Cartão** (`/admin/pos_app/posterminalreader/`)
- Registre leitores de cartão físicos
- Atribua leitores a terminais
- Personalize telas de splash (marcação de exibição para clientes)
- Monitore o status do leitor (online/offline/ocupado)
- [Saiba mais: Gerenciamento de Leitores de Cartão](card-reader-management)

## Implantação Multilocação

Para comerciantes com múltiplas localizações de varejo, o Spwig POS oferece suporte à hierarquia de configurações:

**Hierarquia de Configurações** (prioridade mais alta para mais baixa):
1. Configurações específicas do terminal (sobrepõem todas)
2. Configurações específicas da loja (sobrepõem grupo e site)
3. Configurações do grupo (sobrepõem padrões do site)
4. Padrões do site (fallback para todos)

Configure configurações compartilhadas no nível do grupo (ex: moeda regional, idioma) e sobrepõem conforme necessário para lojas ou terminais específicos. Veja [Grupos de Lojas POS](pos-store-groups) para orientação detalhada de configuração.

## Dicas

- **Comece com um único terminal** - Teste a configuração e o fluxo de trabalho do POS com um único terminal antes de implantar em toda a frota
- **Atribua o armazém antes de emparelhar** - Terminais não podem processar vendas sem uma atribuição de armazém
- **Configure modelos de recibo cedo** - Campos de conformidade (IDs fiscais) variam por região; configure antes de entrar em produção
- **Teste o modo offline** - Desconecte a internet e verifique se as vendas continuam; confirme a sincronização ao se reconectar
- **Use grupos de lojas para multilocação** - Simplifica o gerenciamento de configurações para implantações de franquias ou regionais
- **Monitore o status do heartbeat** - Terminais pingam o servidor a cada 5 minutos; terminais offline aparecem no painel de administração
- **Configure limites de sincronização para desempenho** - Terminais com conexões lentas se beneficiam de configurações de sync_days/sync_limit mais baixas
- **Faça backup da configuração do hardware** - Documente IPs de impressoras, configurações de leitores de código de barras, configuração de caixa registradora para recuperação em caso de desastre