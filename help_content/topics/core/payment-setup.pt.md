---
title: Configuração de Pagamento
---

Fornecedores de pagamento conectam sua loja a passarelas de pagamento para que você possa aceitar cartões de crédito, carteiras digitais e outros métodos de pagamento no checkout. O Spwig suporta múltiplos fornecedores simultaneamente, oferecendo a seus clientes opções flexíveis de pagamento.

![Fornecedores de pagamento](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Fornecedores Disponíveis

| Fornecedor | Descrição |
|----------|-------------|
| **Stripe** | Cartões de crédito, Apple Pay, Google Pay e 135+ moedas |
| **PayPal** | Saldo do PayPal, cartões de crédito/débito e opções de pagamento posterior |
| **Airwallex** | Pagamentos em múltiplas moedas otimizados para comércio transfronteiriço |
| **Adyen** | Pagamentos de nível corporativo com 250+ métodos de pagamento em todo o mundo |
| **Square** | Pagamentos presenciais e online com suporte integrado ao POS |
| **Revolut** | Pagamentos rápidos na Europa com taxas de câmbio competitivas |

## Conectar um Fornecedor

Navegue até **Configurações > Fornecedores de Pagamento** e clique em **Conectar Fornecedor** para iniciar o assistente de configuração.

### Etapa 1: Selecione o Fornecedor

Escolha entre os fornecedores de pagamento disponíveis. Cada cartão mostra as funcionalidades e regiões suportadas pelo fornecedor.

### Etapa 2: Instruções de Configuração

Revise o guia de configuração específico do fornecedor. Isso inclui:
- Como criar uma conta com o fornecedor (se você não tiver uma)
- Onde encontrar suas credenciais de API no painel do fornecedor
- Quaisquer pré-requisitos (por exemplo, verificação da empresa)

### Etapa 3: Insira as Credenciais

Insira suas credenciais de API:
- **Chave API / Chave Secreta** — Suas credenciais de autenticação do painel do fornecedor
- **Modo de Checkout** — Escolha como os clientes interagem com o formulário de pagamento:

| Modo | Descrição |
|------|-------------|
| **Hospedado** | Os clientes são redirecionados para a página de pagamento do fornecedor (por exemplo, Stripe Checkout). Configuração mais simples, conformidade com o PCI é tratada pelo fornecedor. |
| **Integrado** | O formulário de pagamento é embutido diretamente em sua página de checkout. Experiência sem interrupções, mas requer o SDK JavaScript do fornecedor. |

- **Modo de Teste / Modo de Produção** — Comece no modo de teste para testes, depois mude para produção quando estiver pronto

### Etapa 4: Testar Conexão

Clique em **Testar Conexão** para verificar se suas credenciais são válidas. O assistente verifica:
- Autenticação da chave API
- Permissões da conta
- Acessibilidade do endpoint de webhook

### Etapa 5: Configurar e Salvar

Finalize as configurações do fornecedor:
- **Ativo** — Ative ou desative o fornecedor
- **Fornecedor Padrão** — Defina como o método de pagamento principal no checkout
- **Nome de Exibição** — O nome exibido aos clientes durante o checkout
- **Ordem de Classificação** — Controla a ordem em que os fornecedores aparecem no checkout (números mais baixos aparecem primeiro)

## Dashboard de Pagamento

Navegue até **Configurações > Dashboard de Pagamento** para obter uma visão geral da atividade de pagamento:

### Ações Necessárias

Cartões de alerta no topo destacam problemas que precisam de atenção:
- **Transações Falhadas** — Pagamentos que não puderam ser processados
- **Capturas Pendentes** — Pagamentos autorizados aguardando captura
- **Erros de Conexão** — Fornecedores com problemas de conectividade

### Análise de Receita

- **Gráfico de Receita** — Quebra-cabeça visual do volume de pagamentos ao longo do tempo, agrupado por dia, semana ou mês
- **Métricas de Desempenho** — Receita total, taxa de sucesso, valor médio de transação e taxa de reembolso
- **Comparação de Fornecedores** — Cartões de desempenho lado a lado para cada fornecedor conectado

### Quebra de Transação

- **Distribuição de Status** — Contagens de transações concluídas, pendentes, falhas e reembolsos
- **Mix de Métodos de Pagamento** — Quais métodos de pagamento os clientes usam com mais frequência (cartões de crédito, PayPal, carteiras digitais)

## Gerenciamento de Métodos de Pagamento

Cada fornecedor suporta diferentes métodos de pagamento. Você pode ativar ou desativar métodos específicos por país:

1. Navegue até a página de configuração do fornecedor
2. Role até a seção **Métodos de Pagamento**
3. Ative ou desative métodos individuais
4. Use controles de nível de país para restringir métodos a mercados específicos

Isso é útil quando um método de pagamento é popular em uma região, mas não em outra (por exemplo, iDEAL na Holanda, Bancontact na Bélgica).

## Webhooks

Webhooks mantêm sua loja sincronizada com o fornecedor de pagamento em tempo real. Eles lidam com eventos como:
- Pagamento concluído ou falhado
- Reembolsos processados
- Disputas e contestações abertas
- Renovações de assinaturas

### Configuração Automática

Quando você conecta um fornecedor, o Spwig registra automaticamente um endpoint de webhook com o fornecedor. O URL do webhook é exibido na página de configuração do fornecedor para referência.

### Monitoramento de Webhook

Cada webhook recebido é registrado com:
- **Tipo de evento** (por exemplo, payment_intent.succeeded)
- **Carimbo de data/hora** e status de processamento
- **Payload** para depuração

Se um webhook falhar no processamento, será registrado como um erro para que você possa investigar.

## Usando Múltiplos Fornecedores

Você pode conectar múltiplos fornecedores de pagamento simultaneamente:

- **Fornecedor Padrão** — O fornecedor selecionado por padrão no checkout. Marque um fornecedor como padrão em sua configuração.
- **Ordem de Classificação** — Controla a ordem de exibição no checkout. Os clientes veem todos os fornecedores ativos e podem escolher o preferido.
- **Fallback** — Se um fornecedor tiver falhas, os clientes ainda podem pagar usando um fornecedor alternativo.

## Dicas

- Comece com **Stripe** ou **PayPal** — eles cobrem a gama mais ampla de métodos de pagamento e regiões.
- Use **modo de teste/teste** para processar transações de teste antes de ir ao ar. Cada fornecedor tem números de cartão de teste em sua documentação.
- Ative **múltiplos fornecedores** para que os clientes tenham uma opção de pagamento de backup se um fornecedor tiver problemas.
- Defina uma **ordem de classificação baixa** para seu fornecedor preferido para que ele apareça primeiro no checkout.
- Monitore o Dashboard de Pagamento semanalmente para detectar transações falhadas e problemas de conexão cedo.
- Mantenha suas credenciais de API seguras — elas são armazenadas criptografadas no banco de dados, mas nunca devem ser compartilhadas.

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.