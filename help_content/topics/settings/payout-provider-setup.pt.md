---
title: Configuração do Fornecedor de Pagamentos
---

A configuração do fornecedor de pagamentos permite que você configure o PayPal e o Airwallex para pagamentos de afiliados automatizados. Este guia mostra como conectar suas contas de provedores de pagamento, configurar webhooks e testar sua integração.

## Fornecedores de Pagamentos Suportados

O Spwig integra-se com dois fornecedores de pagamentos para automatizar pagamentos de afiliados:

| Fornecedor | Método de Pagamento | Processamento | Suporte a Lotes | Melhor Para |
|------------|---------------------|---------------|------------------|-------------|
| **PayPal** | Transferências por conta do PayPal | Baseado em API | Sim (até 15.000) | Maioria dos afiliados, alcance global |
| **Airwallex** | Transferências bancárias internacionais | Baseado em API | Não (individual) | Transferências bancárias, pagamentos internacionais |

### Diferenças Principais

**Pagamentos do PayPal**:
- Requer que o afiliado tenha uma conta PayPal (e-mail de pagamento)
- Processa lotes de até 15.000 pagamentos de uma só vez
- Processamento mais rápido (1-2 dias úteis)
- Menor complexidade de configuração
- Taxas: ~2% ou $0,25-$1,00 por pagamento
- Um único webhook para todo o lote

**Airwallex**:
- Suporta transferências bancárias diretas
- Processa pagamentos individuais um por um
- Processamento mais longo (2-5 dias úteis)
- Suporta múltiplas moedas e países
- Taxas variam conforme o país de destino
- Webhook individual por pagamento

Você pode configurar ambos os provedores e permitir que os afiliados escolham o método de pagamento preferido.

## Por Que Usar Fornecedores de Pagamentos?

Integrar provedores de pagamento oferece benefícios significativos em relação aos pagamentos manuais:

- **Processamento automatizado** — Nenhuma entrada de dados manual ou execução de pagamento
- **Eficiência de lotes** — Processar dezenas ou centenas de pagamentos com um único clique
- **Confirmações de webhook** — Atualizações automáticas de status quando os pagamentos forem concluídos
- **Redução de erros** — O sistema valida os detalhes da conta antes do processamento
- **Rastreamento de auditoria** — Registro completo de transações e respostas do provedor
- **Pagamentos mais rápidos** — Os afiliados recebem os fundos mais rapidamente
- **Escalabilidade** — Gerenciar programas de afiliados em crescimento sem um aumento proporcional no trabalho administrativo

Sem a integração do provedor, você deve processar cada pagamento manualmente por meio do seu banco ou painel do PayPal, depois retornar ao Spwig para marcar os pagamentos como concluídos.

## Configuração do PayPal

Siga estas etapas para configurar os pagamentos do PayPal para pagamentos automatizados de afiliados.

### Pré-requisitos

Antes de começar, você precisa:
- De uma conta PayPal Business (contas pessoais não podem usar a API de Pagamentos)
- Acesso ao [Painel do Desenvolvedor do PayPal](https://developer.paypal.com/dashboard/)
- Aprovação para uso da API de Pagamentos (após testes no ambiente de sandbox)

### Etapa 1: Criar uma Aplicação do PayPal

1. **Navegue** até [Painel do Desenvolvedor do PayPal](https://developer.paypal.com/dashboard/)
2. **Faça login** com sua conta PayPal Business
3. **Clique** em **Minhas Aplicações e Credenciais** no menu lateral esquerdo
4. **Selecione** a guia **Live** (ou Sandbox para testes)
5. **Clique** em **Criar Aplicação**
6. **Digite o nome da aplicação** (ex: "Pagamentos de Afiliados do Spwig")
7. **Selecione o tipo de aplicação**: Merchante
8. **Clique** em **Criar Aplicação**

O PayPal gera suas credenciais.

### Etapa 2: Obter Credenciais da API

Depois de criar a aplicação:

1. **Copie o ID do Cliente** — Uma longa string alfanumérica
2. **Clique** em **Mostrar** sob Segredo
3. **Copie o Segredo do Cliente** — Mantenha-o confidencial
4. **Anote o modo** — Sandbox ou Live

### Etapa 3: Habilitar o Recurso de Pagamentos

As aplicações do PayPal requerem permissão explícita para usar pagamentos:

1. **Role** até a seção **Recursos** em sua aplicação
2. **Localize** o recurso **Pagamentos**
3. **Clique** em **Adicionar** se ainda não estiver habilitado
4. **Submeta para aprovação** se estiver usando o modo Live (a aprovação leva 1-2 dias úteis)

### Etapa 4: Adicionar o Fornecedor no Spwig

Agora adicione a conta do PayPal ao Spwig:

1. **Navegue** até **Configurações > Fornecedores de Pagamentos**
2. **Clique** em **+ Adicionar Conta do PayPal**
3. **Preencha o formulário**:
   - **Nome da Conta**: Rótulo descritivo (ex: "Conta Principal do PayPal")
   - **ID do Cliente**: Cole do Painel do Desenvolvedor do PayPal
   - **Segredo do Cliente**: Cole do Painel do Desenvolvedor do PayPal
   - **Modo**: Selecione Sandbox (testes) ou Produção (ativo)
   - **Ativo**: Marque para habilitar
4. **Clique em Salvar**

O Spwig valida as credenciais solicitando um token de acesso. Se a validação falhar, verifique novamente o ID do Cliente e o Segredo.

### Etapa 5: Testar a Conexão

Verifique sua integração do PayPal:

1. Crie um pagamento de teste em **Programa de Afiliados > Pagamentos**
2. Use seu próprio e-mail do PayPal como destinatário
3. Defina o valor como $0,01 (se estiver em modo Produção) ou qualquer valor (se for Sandbox)
4. Processar com o provedor
5. Verifique a conta do PayPal para ver o pagamento recebido
6. Verifique se o webhook atualiza o status do pagamento no Spwig

Se estiver usando o modo Sandbox, crie uma conta de teste do PayPal no [Sandbox do PayPal](https://developer.paypal.com/dashboard/accounts) para receber pagamentos de teste.

## Configuração do Airwallex

O Airwallex suporta transferências bancárias internacionais para afiliados que preferem depósitos diretos.

### Pré-requisitos

Antes de começar, você precisa:
- De uma conta do Airwallex (crie em [airwallex.com](https://www.airwallex.com))
- Status de conta empresarial verificada
- Acesso à API habilitado (entre em contato com o suporte do Airwallex se necessário)
- Saldo suficiente em sua conta do Airwallex

### Etapa 1: Gerar Credenciais da API

1. **Faça login** no [Painel do Airwallex](https://www.airwallex.com/app/)
2. **Navegue** até **Configurações > Chaves da API**
3. **Clique** em **Criar Chave da API**
4. **Digite a descrição**: "Pagamentos de Afiliados do Spwig"
5. **Selecione as permissões**: Ative **Pagamentos** (leitura e escrita)
6. **Clique** em **Gerar**
7. **Copie a Chave da API** — Mostrada apenas uma vez
8. **Copie o ID do Cliente** — Exibido com a chave

### Etapa 2: Anotar seu Ambiente

O Airwallex fornece dois ambientes:

- **Demo**: Para testes com transações fictícias
- **Produção**: Para transferências reais de dinheiro

Certifique-se de saber a qual ambiente sua chave da API pertence.

### Etapa 3: Adicionar o Fornecedor no Spwig

Adicione a conta do Airwallex ao Spwig:

1. **Navegue** até **Configurações > Fornecedores de Pagamentos**
2. **Clique** em **+ Adicionar Conta do Airwallex**
3. **Preencha o formulário**:
   - **Nome da Conta**: Rótulo descritivo (ex: "Conta do Airwallex em EUR")
   - **Chave da API**: Cole do painel do Airwallex
   - **ID do Cliente**: Cole do painel do Airwallex
   - **Ambiente**: Selecione Demo ou Produção
   - **Ativo**: Marque para habilitar
4. **Clique em Salvar**

O Spwig valida as credenciais consultando o saldo da sua conta.

### Etapa 4: Verificar Países Suportados

O Airwallex suporta transferências para muitos países, mas não todos. Verifique a página de [cobertura do Airwallex](https://www.airwallex.com/global-business-account/global-transfers) para confirmar se os países dos seus afiliados são suportados.

Países comuns suportados incluem:
- Estados Unidos
- Reino Unido
- Países da União Europeia
- Austrália
- Canadá
- Singapura
- Hong Kong

### Etapa 5: Testar Transferência Bancária

Teste sua integração do Airwallex:

1. Crie um pagamento de teste para um afiliado com detalhes bancários
2. Use um valor pequeno ($1-$5) se estiver no modo Produção
3. Processar com o provedor
4. Verifique o painel do Airwallex para a transação
5. Aguarde a confirmação do webhook
6. Verifique se o pagamento foi concluído no Spwig

O modo Demo processa instantaneamente. O modo Produção leva 2-5 dias úteis.

## Lógica de Seleção do Fornecedor

Ao processar um pagamento, o Spwig seleciona automaticamente o fornecedor apropriado com base no método de pagamento do afiliado.

### Fluxo de Seleção

1. **Verifique o método de pagamento do afiliado**:
   - Se `payment_email` estiver definido → O afiliado prefere o PayPal
   - Se os detalhes bancários estiverem definidos → O afiliado prefere transferência bancária
2. **Correlacione ao fornecedor**:
   - E-mail do PayPal → Use a conta ativa do PayPal
   - Detalhes bancários → Use a conta ativa do Airwallex
3. **Caso o fornecedor preferido não esteja configurado, use o primeiro disponível**
4. **Exiba um erro** se nenhum fornecedor compatível existir

### Múltiplas Contas de Fornecedor

Você pode configurar múltiplas contas para o mesmo fornecedor (ex: duas contas do PayPal para diferentes regiões). O Spwig seleciona a primeira conta ativa que corresponda ao método de pagamento. Para controlar qual conta é usada, reordene-as na lista do administrador ou defina apenas uma como ativa.

## Teste da Integração de Pagamentos

Sempre teste sua integração do provedor antes de processar pagamentos reais para afiliados.

### Teste no Modo Sandbox/Demo

1. **Defina o provedor para o modo sandbox** (PayPal Sandbox ou Airwallex Demo)
2. **Crie um afiliado de teste** com detalhes de pagamento de teste
3. **Crie comissões de teste** e aprovê-las
4. **Crie um pagamento de teste** incluindo essas comissões
5. **Processar com o provedor** usando o menu de ações
6. **Monitore os logs do Celery** para solicitações da API
7. **Verifique o painel do provedor** para a transação
8. **Aguarde o webhook** para atualizar o status do pagamento
9. **Verifique se as comissões foram marcadas como pagas**

### Teste em Produção

Antes de ir ao ar:

1. **Mude para o modo de produção** nas configurações do provedor
2. **Crie um pequeno pagamento de teste** para si mesmo ($0,01-$1,00)
3. **Processar** e aguarde a conclusão
4. **Verifique se os fundos foram recebidos** em sua própria conta
5. **Verifique se o webhook foi acionado** e atualizou o status
6. **Revise as taxas de transação do provedor**

### Problemas Comuns em Testes

| Problema | Causa | Solução |
|---------|-------|---------|
| "Credenciais inválidas" | Chave de API incorreta ou modo não correspondente | Reverifique as credenciais, verifique se o modo sandbox vs produção está correto |
| Webhook nunca é acionado | URL não configurada no provedor | Adicione a URL do webhook no painel do provedor |
| Pagamento fica em Processamento | Assinatura do webhook falhou | Verifique se o segredo do webhook corresponde |
| Nenhum provedor disponível | Nenhuma conta de provedor ativa para o método de pagamento | Ative pelo menos uma conta de provedor |

## Processamento em Lotes (PayPal)

O PayPal suporta processamento em lotes para eficiência e economia de custos.

### Como Funciona o Processamento em Lotes

Quando você seleciona múltiplos pagamentos e clica em **Processar com o Provedor**:

1. O Spwig agrupa todos os pagamentos do PayPal em um único lote
2. O sistema envia uma única solicitação de API com todos os detalhes dos pagamentos (até 15.000)
3. O PayPal processa todo o lote como uma única transação
4. O webhook retorna com os resultados do lote
5. O Spwig atualiza todos os pagamentos com base na resposta do lote

### Vantagens do Processamento em Lotes

- **Redução de chamadas da API** — Uma solicitação para centenas de pagamentos
- **Menores taxas** — Algumas estruturas de taxas do PayPal favorecem o processamento em lotes
- **Processamento mais rápido** — Execução paralela para todo o lote
- **Um único webhook** — Facilita o monitoramento e o registro

### Limites de Lotes

O PayPal impõe os seguintes limites:
- Máximo de 15.000 destinatários por lote
- Máximo de $100.000 total por lote
- Processamento geralmente concluído em minutos

Se você ultrapassar 15.000 pagamentos, o Spwig divide automaticamente em lotes múltiplos.

## Processamento Individual (Airwallex)

O Airwallex processa pagamentos um por um, o que oferece diferentes tradeoffs.

### Como Funciona o Processamento Individual

Ao processar pagamentos do Airwallex:

1. O sistema envia uma solicitação de API separada para cada pagamento
2. O Airwallex filas as transferências individualmente
3. Cada transferência é concluída independentemente (2-5 dias)
4. Um webhook individual é acionado quando cada transferência é concluída
5. O Spwig atualiza os pagamentos conforme os webhooks chegam

### Vantagens do Processamento Individual

- **Melhor isolamento de erros** — Uma falha não bloqueia as outras
- **Rastreamento por pagamento** — IDs de transação individuais
- **Mais detalhes do pagamento** — Informações específicas do banco por transferência
- **Tempo flexível** — Transferências concluem em taxas diferentes

### Tempo de Processamento

Diferente do processamento em lote instantâneo do PayPal, as transferências do Airwallex levam mais tempo:
- Transferências domésticas: 1-2 dias úteis
- Transferências internacionais: 3-5 dias úteis
- Alguns países: Até 7 dias úteis

Defina as expectativas dos afiliados de acordo com os termos do seu programa.

## Configuração de Webhook

Webhooks permitem atualizações automáticas do status do pagamento quando os provedores concluem transações.

### Formato da URL do Webhook

Configure esta URL no painel do provedor:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Substitua `{provider}` com:
- `paypal` para webhooks do PayPal
- `airwallex` para webhooks do Airwallex

Exemplos:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### Configuração de Webhook do PayPal

1. **Navegue** até [Painel do Desenvolvedor do PayPal](https://developer.paypal.com/dashboard/)
2. **Clique** no nome da sua aplicação
3. **Role** até a seção **Webhooks**
4. **Clique** em **Adicionar Webhook**
5. **Digite a URL do webhook** (formato acima)
6. **Selecione eventos**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Clique em Salvar**

O PayPal fornece uma chave de assinatura do webhook. O Spwig usa isso para verificar a autenticidade do webhook.

### Configuração de Webhook do Airwallex

1. **Navegue** até [Painel do Airwallex](https://www.airwallex.com/app/)
2. **Vá para** **Configurações > Webhooks**
3. **Clique** em **Criar Webhook**
4. **Digite a URL do webhook** (formato acima)
5. **Selecione eventos**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Clique em Criar**

O Airwallex assina os webhooks com o seu segredo da API.

### Segurança dos Webhooks

Os webhooks são validados usando os seguintes mecanismos:

- **Verificação de assinatura** — O provedor assina a carga útil do webhook com a chave secreta
- **Verificação de carimbo de tempo** — Rejeita webhooks antigos (impede ataques de repetição)
- **Listas de IPs permitidos** (opcional) — Restringe a faixas de IPs do provedor
- **HTTPS obrigatório** — Webhooks só funcionam com SSL

Nunca desative a verificação de assinatura em produção.

### Teste de Webhooks

A maioria dos provedores oferece ferramentas de teste de webhooks:

**PayPal**: Use o "Simulador" no Painel do Desenvolvedor para disparar webhooks de teste

**Airwallex**: Crie uma transferência de teste no modo Demo e observe o webhook

Você também pode verificar os logs de webhooks no Spwig em **Configurações > Logs do Sistema** (se o registro estiver habilitado).

## Solução de Problemas

### Erro de Credenciais Inválidas

**Sintoma**: "Falha na autenticação" ao salvar a conta do provedor

**Causas**:
- ID do Cliente ou Segredo incorretos
- Credenciais do sandbox usadas no modo de produção (ou vice-versa)
- Chave de API expirada ou revogada
- Conta não verificada

**Soluções**:
- Re-copie as credenciais do painel do provedor
- Verifique se o modo corresponde (sandbox vs produção)
- Regenere as chaves da API
- Entre em contato com o suporte do provedor para verificar o status da conta

### Webhook Não Recebido

**Sintoma**: O pagamento fica em estado "Processando" indefinidamente

**Causas**:
- URL do webhook não configurada no painel do provedor
- Certificado SSL inválido
- Firewall bloqueando IPs do provedor
- Verificação de assinatura do webhook falhando

**Soluções**:
- Verifique novamente a URL do webhook nas configurações do provedor
- Verifique se o certificado SSL é válido
- Whitelist as faixas de IPs do provedor no firewall
- Verifique os logs do Celery para erros de assinatura
- Teste o webhook com a ferramenta de simulação do provedor

### Pagamento Falhou

**Sintoma**: O status do pagamento muda para "Falhou" com uma mensagem de erro

**Causas**:
- Detalhes de pagamento do afiliado inválidos (e-mail ou conta bancária incorreta)
- Saldo insuficiente na conta do provedor
- Conta do destinatário não pode receber pagamentos
- País não suportado (Airwallex)
- Pagamento excede os limites do provedor

**Soluções**:
- Revise o erro no campo **Resposta do Provedor**
- Verifique se os detalhes de pagamento do afiliado estão corretos
- Adicione fundos à conta do provedor
- Peça ao afiliado para verificar o status de sua conta
- Verifique o suporte de país e moeda do provedor
- Divida pagamentos grandes se ultrapassarem os limites

### Mismatch de Modo

**Sintoma**: Pagamentos de teste funcionam, mas os pagamentos em produção falham

**Causas**:
- O provedor está no modo Sandbox, mas usando contas de afiliados em produção
- Credenciais da API de um ambiente errado

**Soluções**:
- Mude o modo do provedor para Produção
- Regenere as credenciais da API de produção
- Verifique se a URL do webhook aponta para o domínio de produção

## Boas Práticas de Segurança

Proteja sua integração de pagamentos com estas medidas de segurança:

### Armazenamento de Credenciais

- **Nunca comite credenciais em controle de versão** — Use variáveis de ambiente ou armazenamento seguro
- **Rotacione chaves da API trimestralmente** — Gere novas chaves a cada 3 meses
- **Use chaves separadas para sandbox e produção** — Nunca misture ambientes
- **Limite as permissões da API** — Apenas conceda acesso a pagamentos, não controle total da conta

O Spwig armazena as credenciais do provedor criptografadas no banco de dados. Mantenha os backups do banco de dados seguros.

### Segurança dos Webhooks

- **Sempre verifique as assinaturas** — Nunca pule a validação da assinatura
- **Use HTTPS exclusivamente** — Webhooks não são suportados por HTTP
- **Implemente listas de IPs permitidos** — Restrinja webhooks às faixas de IPs do provedor
- **Registre todos os webhooks** — Monitore atividade suspeita
- **Limite a taxa de webhooks** — Previna abusos

### Controle de Acesso

- **Limite o acesso do pessoal** — Apenas pessoal confiável deve processar pagamentos
- **Use autenticação de dois fatores** — Requer 2FA para contas do pessoal
- **Audição de ações de pagamento** — Revise quem processou quais pagamentos
- **Separe funções** — Pessoal diferente para aprovação vs processamento

### Monitoramento

- **Verifique pagamentos falhados diariamente** — Resolva problemas com rapidez
- **Monitore os saldos da conta do provedor** — Garanta fundos suficientes
- **Revise os logs de transações semanalmente** — Detecte anomalias cedo
- **Configure alertas** — Notificações por e-mail para pagamentos grandes ou falhados

## Dicas

- Teste sua integração de forma abrangente no modo sandbox antes de migrar para produção — identifique problemas com dinheiro falso.
- Configure tanto o PayPal quanto o Airwallex para dar aos afiliados a escolha de método de pagamento — afiliados diferentes preferem métodos diferentes.
- Defina URLs de webhook durante a configuração inicial e verifique se elas são acionadas corretamente — webhooks são críticos para automação.
- Mantenha os saldos das contas do provedor sempre atualizados para evitar falhas em pagamentos durante o processamento em lotes.
- Use nomes descritivos para contas se configurar múltiplos provedores (ex: "Conta do PayPal em USD", "Conta do PayPal em EUR").
- Rotacione as credenciais da API a cada trimestre como uma boa prática de segurança.
- Documente suas URLs de webhook e credenciais em um gerenciador de senhas seguro compartilhado com sua equipe.
- Monitore pagamentos falhados imediatamente — atrasos frustram os afiliados e prejudicam a reputação do programa.
- Sempre use HTTPS para sua instalação do Spwig — os webhooks exigem certificados SSL.
- Entre em contato com o suporte do provedor se encontrar erros persistentes — eles podem verificar o status da sua conta e permissões.