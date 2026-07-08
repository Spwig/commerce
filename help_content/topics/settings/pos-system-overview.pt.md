---
title: Visão Geral do Sistema POS
---

O sistema POS da Spwig transforma sua loja em uma solução de varejo completa com terminais de ponto de venda modernos. Implante terminais ilimitados em localizações ilimitadas por uma taxa de licença plana de €499/ano. Cada terminal é uma aplicação da Web Progressiva (PWA) que funciona offline, sincroniza automaticamente e integra-se perfeitamente com seu estoque, dados de clientes e processamento de pagamentos. Gerencie tudo a partir do painel de administração—configuração do terminal, reconciliação de turnos, personalização de recibos e integração de hardware.

Use o sistema POS quando tiver localizações de varejo físicas, lojas pop-up, feiras de negócios ou qualquer ambiente em que os clientes compram presencialmente em vez de online.

![Dashboard POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## O que é o Spwig POS?

O Spwig POS é um sistema de ponto de venda totalmente integrado, projetado para comerciantes que vendem online e em localizações físicas. Ao contrário de sistemas de ponto de venda de terceiros que exigem integrações complexas, o Spwig POS é construído diretamente em sua plataforma, garantindo uma sincronização perfeita de dados em todos os canais de venda.

**Características Principais**:
- **Terminais Ilimitados** - Implante tantos terminais quantos forem necessários sem custo adicional
- **Arquitetura com Foco em Offline** - Continua processando vendas mesmo quando a conexão de internet for perdida
- **Aplicação da Web Progressiva** - Nenhuma instalação em lojas de aplicativos; acesso via navegador em qualquer dispositivo (tablets, computadores, terminais dedicados)
- **Sincronização de Estoque Real** - Reserva de estoque (TTL de 15 minutos) impede a super-venda em canais
- **Suporte a Pagamento Dividido** - Aceite múltiplos métodos de pagamento por transação (dinheiro + cartão + cartão-presente)
- **Integração de Hardware** - Impressoras de recibos térmicas ESC/POS, leitores de código de barras, caixas registradoras, telas para clientes
- **Gerenciamento de Turnos** - Reconciliação de caixa com contagens de abertura/fechamento e rastreamento de discrepâncias
- **Pronto para Multi-localização** - Grupos de lojas com herança de configurações para gerenciamento de franquias e regional

## Licença e Ativação

**Preço com Taxa Fixa**: €499 por ano cobre terminais ilimitados em localizações ilimitadas. Nenhuma taxa por terminal, nenhuma taxa por transação, nenhuma custo oculto.

**Formato da Licença**: `POS-XXXX-XXXX-XXXX-XXXX` (fornecido após a compra)

**Ativação**: Insira sua chave de licença em **Configurações > Licença POS**. O sistema valida com o servidor de licenças da Spwig e ativa imediatamente todas as funcionalidades POS. As licenças incluem um período de graça de 14 dias após a expiração para permitir atrasos no processamento de pagamentos.

**O que Você Obtém**:
- Registros ilimitados de terminais
- Atribuições ilimitadas de pessoal
- Todas as funcionalidades POS (turnos, gerenciamento de caixa, personalização de recibos, telas para clientes)
- Integrações com provedores de pagamento (Stripe Terminal e sistema extensível de provedores)
- Suporte à integração de hardware
- Atualizações e correções de bugs durante o período da licença

Nenhuma funcionalidade POS está disponível sem uma licença válida—o interface de emparelhamento de terminais, gerenciamento de turnos e páginas de administração POS todas exigem ativação.

## Arquitetura do Sistema

**Frontend** - Aplicação da Web Progressiva React 18:
- Primeiro offline com cache de Service Worker (funciona sem internet)
- Sistema de build Vite para carregamento rápido
- Módulos CSS + tokens de design (consistente com o tema da sua loja)
- IndexedDB para persistência de dados locais
- 10 idiomas suportados (Inglês, Chinês Simplificado/Tradicional, Francês, Alemão, Espanhol, Português, Japonês, Russo, Árabe)

**Backend** - Integração de Backend:
- 13 modelos POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- 43+ endpoints de API REST para operações de terminal
- Sistema de reserva de estoque com gerenciamento de TTL
- Tarefas do Celery para sincronização em segundo plano
- Armazenamento criptografado de credenciais para provedores de pagamento

**Segurança**:
- Emparelhamento de terminal via códigos de 8 caracteres (gerados no lado do servidor, expiram após o uso)
- Controle de atribuição de pessoal que usuários podem acessar quais terminais
- Capacidade de bloqueio/desbloqueio remoto para emergências de administração
- Credenciais criptografadas de provedores de pagamento
- Autenticação baseada em sessão com suporte a desbloqueio biométrico (dependente do navegador)

## Fluxo de Trabalho para Iniciar

Siga estas 5 etapas para implantar seu primeiro terminal POS:

**Etapa 1: Ativar Licença POS**
- Navegue até **Configurações > Licença POS**
- Insira sua chave de licença (`POS-XXXX-XXXX-XXXX-XXXX`)
- Valide a licença (requer conexão com a internet)
- Confirme a ativação

**Etapa 2: Criar Armazém**
- Navegue até **Catálogo > Armazéns**
- Crie um armazém representando sua localização de varejo
- Configure endereço e informações de contato
- Esse armazém rastreará o estoque físico para vendas POS

**Etapa 3: Registrar Terminal**
- Navegue até **POS > Terminais**
- Clique em **+ Adicionar Terminal**
- Defina o nome do terminal (ex: "Caixa Principal", "Checkout 1")
- Atribua o armazém da Etapa 2
- Configure as configurações de hardware (impressora, leitor de código de barras, caixa registradora)
- Salve para gerar o código de emparelhamento de 8 caracteres

**Etapa 4: Atribuir Pessoal**
- Na configuração do terminal, role até **Usuários Atribuídos**
- Selecione os membros da equipe autorizados a usar este terminal
- Apenas usuários atribuídos podem fazer login no terminal
- Os usuários devem ter permissões POS apropriadas em seu papel de equipe

**Etapa 5: Emparelhar Dispositivo**
- Em seu dispositivo de terminal (tablet/computador), navegue até o URL `/pos/`
- Insira o código de emparelhamento de 8 caracteres da Etapa 3
- O terminal baixa a configuração e sincroniza os dados iniciais
- Faça login com as credenciais de pessoal atribuídas
- O terminal está pronto para vendas

Após o emparelhamento, os terminais sincronizam automaticamente a cada 5 minutos (configurável). O modo offline permite operação contínua quando a internet não está disponível—vendas sincronizam automaticamente quando a conectividade retorna.

## Funcionalidades Principais do POS

**Processamento de Vendas**:
- Pesquisa de produto por nome, SKU ou código de barras
- Pagamento dividido (múltiplos métodos de pagamento por pedido)
- Cestas de compras paradas (salve transações incompletas)
- Devoluções e anulações com rastreamento de razão
- Aplicação de descontos (cupons, cartões-presente, promoções)
- Pesquisa de clientes e resgate de pontos de fidelidade

**Gerenciamento de Caixa**:
- Abertura de turno com contagem inicial de dinheiro
- Fechamento de turno com reconciliação entre esperado e real
- Movimentos de dinheiro (adicionais de fundos, saques de dinheiro com razões)
- Cálculo automático de dinheiro esperado com base em vendas em dinheiro
- Rastreamento e relatórios de discrepâncias

**Integração de Hardware**:
- Impressoras de recibos térmicas ESC/POS (rede ou serial)
- Leitores de código de barras USB
- Acionamento de caixa registradora via pulso da impressora
- Displays para clientes (carrossel promocional durante o tempo ocioso)
- Leitores de cartões Stripe Terminal (S700, WisePOS E, P400)

**Capacidades Offline**:
- Service Worker armazena todos os ativos do terminal
- IndexedDB armazena pedidos recentes (configurável: 7-30 dias, 200-1000 pedidos)
- Reservas de estoque com TTL de 15 minutos impedem super-venda
- Fila de vendas para sincronização quando a conectividade retorna
- Detecção automática de reconexão

## Páginas de Administração POS

Acesse estas páginas de administração para gerenciar todos os aspectos de sua implantação POS:

**Dashboard POS** (`/admin/pos/`)
- Visão geral do sistema e estatísticas rápidas
- Atividade recente de terminais
- Resumo de turnos ativos
- Status da licença e data de expiração

**Gerenciamento de Terminais** (`/admin/pos_app/posterminal/`)
- Registre e configure terminais
- Atribua pessoal e armazéns
- Monitore o status online/offline (rastreamento de batimento cardíaco)
- Desbloqueie terminais remotamente
- [Saiba mais: Gerenciamento de Terminais POS](managing-pos-terminals)

**Gerenciamento de Turnos** (`/admin/pos_app/posshift/`)
- Visualize todos os turnos (abertos, fechados, históricos)
- Revise relatórios de reconciliação de caixa
- Rastreie movimentos de caixa e discrepâncias
- Auditoria da atividade do turno
- [Saiba mais: Turnos POS e Gerenciamento de Caixa](pos-shifts-cash-management)

**Grupos de Lojas** (`/admin/pos_app/storegroup/`)
- Organize terminais por localização/regionais
- Configure configurações de nível de grupo (moeda, idioma, fuso horário)
- Implemente hierarquia de herança de configurações
- [Saiba mais: Grupos de Lojas POS](pos-store-groups)

**Modelos de Recibos** (`/admin/pos_app/receipttemplate/`)
- Personalize recibos impressos (largura do papel, logotipo, cabeçalho/rodapé)
- Configure campos de conformidade (ID de imposto, registro comercial)
- Adicione códigos QR para promoções
- Escopo de modelos para lojas ou grupos específicos
- [Saiba mais: Personalização de Modelos de Recibo](receipt-template-customization)

**Slides Promocionais** (`/admin/pos_app/promoslide/`)
- Crie conteúdo de carrossel de exibição para clientes
- Destine slides a lojas ou grupos específicos
- Agende promoções sazonais
- [Saiba mais: Slides Promocionais para Exibição de Clientes](customer-display-promo-slides)

**Provedores de Pagamento** (`/admin/pos_app/posterminalprovider/`)
- Configure integração com Stripe Terminal
- Gerencie credenciais de provedores de pagamento
- Monitore status de conexão
- [Saiba mais: Provedores de Terminais de Pagamento](payment-terminal-providers)

**Leitores de Cartões** (`/admin/pos_app/posterminalreader/`)
- Registre leitores de cartões físicos
- Atribua leitores a terminais
- Personalize telas de splash (marcação de exibição para clientes)
- Monitore status do leitor (online/offline/ocupado)
- [Saiba mais: Gerenciamento de Leitores de Cartões](card-reader-management)

## Implantação em Múltiplas Localizações

Para comerciantes com múltiplas localizações de varejo, o Spwig POS oferece suporte à herança hierárquica de configurações:

**Hierarquia de Configurações** (maior prioridade para menor):
1. Configurações específicas do terminal (sobrepõem todas)
2. Configurações específicas da loja (sobrepõem grupo e site)
3. Configurações do grupo (sobrepõem padrões do site)
4. Padrões do site (fallback para todos)

Configure configurações compartilhadas no nível do grupo (ex: moeda regional, idioma) e sobrepõem conforme necessário para lojas ou terminais específicos. Veja [Grupos de Lojas POS](pos-store-groups) para orientação detalhada de configuração.

## Dicas

- **Comece com um terminal** - Teste a configuração e o fluxo de trabalho do POS com um único terminal antes de implantar em toda a frota
- **Atribua armazém antes de emparelhar** - Terminais não podem processar vendas sem uma atribuição de armazém
- **Configure modelos de recibo cedo** - Campos de conformidade (IDs de imposto) variam por região; configure antes de ir ao ar
- **Teste o modo offline** - Desconecte a internet e verifique se as vendas continuam; confirme a sincronização ao se reconectar
- **Use grupos de lojas para multi-localização** - Simplifica o gerenciamento de configuração para implantações de franquia ou regionais
- **Monitore o status do batimento cardíaco** - Terminais pingam o servidor a cada 5 minutos; terminais offline aparecem no painel de administração
- **Configure limites de sincronização para desempenho** - Terminais com conexões lentas beneficiam-se de configurações de sync_days/sync_limit mais baixas
- **Faça backup da configuração de hardware** - Documente IPs de impressoras, configurações de leitores de código de barras, configuração de caixa registradora para recuperação de desastres

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.