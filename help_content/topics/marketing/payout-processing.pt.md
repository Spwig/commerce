---
title: Processamento de Pagamentos
---

Processamento de pagamentos permite que você pague afiliados por suas comissões aprovadas. Este guia mostra como criar, gerenciar e processar pagamentos por meio do PayPal ou provedores de transferência bancária.

![Lista de Pagamentos](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Visão Geral do Pagamento

Um pagamento é um lote de pagamento que agrupa várias comissões aprovadas para um único afiliado. Pense nisso como um cheque para todas as receitas pendentes.

Características principais:
- **Inclui várias comissões** — Um pagamento pode cobrir dezenas de comissões aprovadas
- **Requer limiar mínimo** — A maioria dos programas tem montantes mínimos de pagamento ($50-$100 típicos)
- **Processado por meio de provedores** — PayPal ou Airwallex lidam com a transferência real de dinheiro
- **Tem ciclo de vida** — Pendente → Processando → Concluído (ou Falhado)

## Fluxo de Pagamento

O processo completo de pagamento segue seis etapas:

1. **Afiliado ganha comissões** — Vendas atribuídas a links de rastreamento de afiliados
2. **Mercador aprova comissões** — Revisar e aprovar comissões pendentes
3. **Saldo atinge o mínimo** — O saldo aprovado do afiliado atinge o limiar do programa
4. **Afiliado solicita pagamento** — Afiliado envia solicitação de pagamento no seu painel
5. **Mercador processa pagamento** — Você cria e processa o pagamento
6. **Pagamento concluído** — O provedor envia os fundos, comissões marcadas como pagas

## Visualizando Pagamentos

Navegue até **Programa de Afiliados > Pagamentos** para acessar o painel de gerenciamento de pagamentos.

O painel de estatísticas mostra:
- **Pendente** — Pagamentos criados, mas ainda não processados
- **Processando** — Atualmente sendo enviados ao provedor de pagamento
- **Concluído** — Pagamento bem-sucedido
- **Falhado** — Pagamento falhou (requer atenção)

A visão de lista exibe:
- Nome e código do afiliado
- Montante do pagamento
- Método de pagamento (PayPal ou Transferência Bancária)
- Badge de status
- Data de criação e conclusão
- Botões de ação

Use filtros para estreitar por:
- Afiliado
- Método de pagamento
- Status
- Intervalo de data

## Criando um Pagamento

Siga estas etapas para criar um novo pagamento:

1. **Navegue** até **Programa de Afiliados > Pagamentos**
2. **Clique** no botão **+ Adicionar Pagamento**
3. **Selecione afiliado** a partir do menu suspenso
4. **Revise comissões aprovadas** — O sistema exibe todas as comissões não pagas e aprovadas para este afiliado
5. **Selecione comissões para incluir** — Marque as caixas para comissões a pagar (geralmente todas)
6. **Verifique o montante total** — O sistema calcula a soma automaticamente
7. **Escolha o método de pagamento** — PayPal ou Transferência Bancária (com base na preferência do afiliado)
8. **Selecione a conta do provedor** — Escolha qual conta do PayPal/Airwallex usar
9. **Adicione notas** (opcional) — Notas internas para registro
10. **Clique em Salvar** — Pagamento criado com status "Pendente"

O pagamento agora está pronto para processar.

## Processando Pagamentos

Você tem duas opções para processar pagamentos: manual ou baseada em provedor.

### Processamento Manual

Use o processamento manual quando você gerenciar pagamentos fora do sistema (cheques, transferências bancárias, etc.):

1. Selecione o pagamento na lista
2. Clique na ação **Marcar como Processando**
3. Conclua o pagamento por meio do seu método externo
4. Volte ao pagamento
5. Clique na ação **Marcar como Concluído**
6. As comissões são automaticamente atualizadas para o status "Paga"

O processamento manual oferece flexibilidade, mas requer mais trabalho administrativo.

### Processamento por Provedor (Recomendado)

O processamento por provedor automatiza os pagamentos por meio do PayPal ou Airwallex:

1. **Selecione pagamento(s)** na lista (você pode processar vários)
2. **Clique** na ação **Processar com Provedor**
3. **Confirme** no diálogo
4. **O sistema filtra a tarefa** — O trabalhador Celery lida com a chamada da API
5. **O provedor processa o pagamento**:
   - **PayPal**: Agrupa até 15.000 pagamentos por solicitação
   - **Airwallex**: Transferências bancárias individuais
6. **Webhook atualiza o status** — O provedor confirma a conclusão
7. **Comissões marcadas como pagas** — O sistema atualiza todas as comissões incluídas

O processamento por provedor é mais rápido, confiável e cria um rastro de auditoria automático.

## Métodos de Pagamento

Spwig suporta dois métodos de pagamento com requisitos diferentes:

| Método | Provedor | Requisitos | Tempo de Processamento | Taxas | Melhor Para |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Payouts | O afiliado deve ter um `payment_email` válido | 1-2 dias úteis | ~2% ou $0,25-$1,00 por pagamento | A maioria dos afiliados, alcance global |
| **Transferência Bancária** | Airwallex | Detalhes da conta bancária (número da conta, roteamento, SWIFT) | 2-5 dias úteis | Varia por país | Afiliados internacionais, grandes montantes |

Os afiliados configuram seu método de pagamento e detalhes em seu painel. O sistema seleciona automaticamente o provedor apropriado com base em sua preferência.

### Lógica de Seleção do Método de Pagamento

Ao processar um pagamento, o Spwig seleciona o provedor da seguinte forma:

1. Verifique o método de pagamento preferido do afiliado (PayPal ou Transferência Bancária)
2. Corresponda à conta do provedor configurada (PayPal → PayPal, Banco → Airwallex)
3. Recuar para o primeiro provedor disponível se a preferência não estiver disponível
4. Exiba um erro se nenhum provedor estiver configurado

## Fluxo de Status do Pagamento

Entender os status dos pagamentos ajuda você a acompanhar o progresso do pagamento:

| Status | Significado | Próxima Ação |
|--------|---------|-------------|
| **Pendente** | Criado, mas ainda não enviado ao provedor | Processar com o provedor ou marcar como processando |
| **Processando** | Enviado ao provedor de pagamento, aguardando confirmação | Aguarde o webhook ou verifique o painel do provedor |
| **Concluído** | Pagamento bem-sucedido, fundos enviados | Nenhuma — comissões marcadas como pagas |
| **Falhado** | Pagamento falhou (veja detalhes do erro) | Revise o erro, corrija o problema, tente novamente ou cancele |
| **Cancelado** | Cancelado manualmente antes da conclusão | Nenhuma — comissões permanecem não pagas |

### Caminho de Sucesso

Pendente → Processando → Concluído

Este é o caminho feliz. Os webhooks do provedor atualizam automaticamente o status conforme o pagamento avança.

### Caminho de Falha

Pendente → Processando → Falhado

Quando um pagamento falha, o status do pagamento muda para Falhado e você deve investigar.

## Lidando com Pagamentos Falhados

Pagamentos falhados exigem intervenção manual. Causas comuns de falha:

| Causa | Erro do Provedor | Solução |
|-------|----------------|----------|
| Conta inválida | "Conta do destinatário não encontrada" | Verifique o e-mail de pagamento ou detalhes bancários do afiliado |
| Saldo insuficiente | "Fundos insuficientes" | Adicione fundos à sua conta do provedor |
| Erro nos detalhes bancários | "Número de roteamento inválido" | Peça ao afiliado para atualizar as informações bancárias |
| Restrição de conta | "O destinatário não pode receber pagamentos" | Entre em contato com o afiliado para resolver o status da conta |
| Problema do provedor | "Serviço temporariamente indisponível" | Espere e tente novamente após algumas horas |

### Como Reativar um Pagamento Falhado

1. **Veja o pagamento falhado** — Clique nele na lista
2. **Leia a mensagem de erro** — Verifique o campo **Resposta do Provedor** para detalhes
3. **Corrija o problema subjacente** — Atualize os detalhes do afiliado, adicione fundos ao provedor, etc.
4. **Reinicie o status** — Mude o status de volta para Pendente (formulário de edição)
5. **Processar novamente** — Use a ação **Processar com Provedor**

### Como Cancelar e Recriar

Se reativar não funcionar:

1. **Abra o pagamento falhado**
2. **Mude o status para Cancelado**
3. **Salve o pagamento**
4. **Crie um novo pagamento** — Siga as etapas de criação novamente
5. **Processar o novo pagamento**

Pagamentos cancelados não marcam as comissões como pagas, portanto, permanecem elegíveis para novos pagamentos.

## Integração com Provedores de Pagamento

O processamento de pagamentos requer uma conta de provedor de pagamento configurada. O Spwig se integra com:

- **API de Pagamentos PayPal** — Para pagamentos PayPal
- **Airwallex** — Para transferências bancárias internacionais

### Requisitos de Configuração

Antes de processar pagamentos:
1. Configure pelo menos um provedor em **Configurações > Provedores de Pagamento**
2. Adicione credenciais da API (ID do cliente, Segredo, Chave da API)
3. Defina para modo de produção (sandbox para testes)
4. Configure a URL do webhook no painel do provedor
5. Verifique a conectividade com um pagamento de teste

Veja o guia [Configuração do Provedor de Pagamento](#) para instruções detalhadas de configuração.

### Seleção de Provedor por Afiliado

Os afiliados escolhem seu método de pagamento preferido em seu painel:
- PayPal: Insira `payment_email`
- Transferência Bancária: Insira detalhes da conta bancária

O sistema rota automaticamente os pagamentos para o provedor correspondente.

## Melhores Práticas para Agendamento de Pagamentos

Estabeleça um agendamento regular de pagamentos para construir confiança com os afiliados:

| Agendamento | Frequência | Carga de Trabalho | Satisfação do Afiliado | Recomendado Para |
|----------|-----------|----------|------------------------|-----------------|
| Semanal | Toda quinta-feira | Alta | Excelente | Novos programas, alto volume |
| Mensal | Primeiro do mês | Baixa | Aceitável | Programas estabelecidos |
| Trimestral | A cada 3 meses | Muito baixa | Ruim | Não recomendado |

Considere o tamanho do seu programa e a capacidade administrativa ao escolher um agendamento.

## Melhores Práticas para Processamento

Siga estas diretrizes para operações de pagamento suaves:

- **Agrupe pagamentos por agendamento** — Processar todos os pagamentos elegíveis no mesmo dia a cada semana/mês
- **Verifique os detalhes antes de processar** — Confirme duas vezes as informações de pagamento do afiliado, especialmente para grandes montantes
- **Monitore o saldo do provedor** — Garanta fundos suficientes em sua conta do PayPal/Airwallex
- **Defina limites mínimos claros** — Comunique os mínimos de pagamento nos termos do programa ($50-$100 típicos)
- **Documente seu agendamento** — Adicione o agendamento de pagamento aos termos do afiliado e às configurações do portal
- **Use o processamento do provedor** — Evite o processamento manual, a menos que seja absolutamente necessário
- **Revise pagamentos falhados imediatamente** — Trate falhas dentro de 24 horas
- **Mantenha os webhooks do provedor configurados** — Webhooks permitem atualizações de status automáticas
- **Exporte relatórios de pagamentos regularmente** — Faça o download de relatórios mensais para contabilidade

## Registros de Pagamento e Relatórios

Cada pagamento cria um registro imutável com:
- Informações do afiliado
- IDs de comissões incluídas
- Montante total
- Método de pagamento e provedor
- Carimpos de criação e conclusão
- ID de transação do provedor (depois do processamento)
- Dados de resposta do provedor (para depuração)
- Notas internas

Acesse esses dados clicando em qualquer pagamento na lista. Use o recurso de exportação da interface de administração para baixar relatórios de pagamentos para fins de contabilidade ou tributários.

## Dicas

- Processar pagamentos em um horário fixo (por exemplo, toda quinta-feira às 14h) para que os afiliados saibam quando esperar o pagamento.
- Sempre use o processamento do provedor em vez do processamento manual — é mais rápido, confiável e cria melhores rastreamentos de auditoria.
- Defina limites mínimos de pagamento em seus programas para reduzir a carga administrativa — $50 ou $100 é padrão.
- Monitore o saldo da conta do provedor antes de processar lotes grandes para evitar falhas.
- Teste sua integração de pagamento no modo sandbox antes de ir ao vivo com pagamentos reais.
- Adicione uma nota a cada pagamento explicando o período que ele cobre (por exemplo, "Comissões de janeiro de 2026").
- Verifique pagamentos falhados imediatamente — atrasos frustram os afiliados e prejudicam a confiança.
- Comunique atrasos proativamente — se você não puder processar no horário acordado, avise os afiliados afetados com antecedência.

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.