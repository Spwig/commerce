---
title: Preferências de Comunicação
---

Preferências de comunicação permitem que os clientes controlem quais e-mails e mensagens de SMS recebem da sua loja. Este sistema garante a conformidade com o GDPR e ajuda você a respeitar as preferências de comunicação dos clientes em todos os canais.

Navegue até **Clientes > Preferências de Comunicação** no menu lateral de administração para gerenciar as preferências de comunicação dos clientes.

## Entendendo Preferências de Comunicação

O sistema de preferências de comunicação fornece aos clientes controle granular sobre as mensagens que recebem. Isso inclui:

- **E-mails transacionais** — Confirmações essenciais de pedidos, atualizações de envio, e-mails de segurança da conta (sempre ativo)
- **E-mails de marketing** — Boletins informativos, promoções, recomendações de produtos (requer opt-in)
- **Notificações específicas do app** — Posts do blog, pontos de fidelidade, recompensas de indicação, comissões de afiliados
- **Notificações por SMS** — Notificações por mensagem de texto (requer opt-in explícito per TCPA)

Todas as comunicações de marketing requerem consentimento do cliente e verificação do e-mail para garantir a conformidade com o GDPR.

## Explicação dos Tipos de Preferência

### Comunicações Transacionais (Sempre Ativadas)

As mensagens transacionais são essenciais para a conta e pedidos do cliente. Essas **não podem ser desativadas** pelos clientes:

| Tipo | Descrição | Exemplos |
|------|-------------|----------|
| **Confirmações de Pedido** | Confirmação quando o pedido é feito | O pedido #12345 foi recebido |
| **Atualizações de Envio** | Notificações quando o status do pedido muda | Seu pedido foi enviado |
| **Confirmações de Pagamento** | Pagamento recebido, reembolso processado | Pagamento de $49,99 confirmado |
| **Segurança da Conta** | Redefinição de senha, verificação de e-mail | Redefina sua senha |

### Comunicações de Marketing (Requer Opt-In)

As mensagens de marketing requerem consentimento do cliente e verificação do e-mail:

| Tipo | Descrição | Padrão |
|------|-------------|---------|
| **Boletim Informativo** | Boletins informativos e atualizações gerais | Opt-out |
| **Ofertas Promocionais** | Vendas, descontos, ofertas especiais | Opt-out |
| **Recomendações de Produtos** | Sugestões personalizadas de produtos | Opt-out |
| **De volta ao estoque** | Notificações quando os produtos retornam | Opt-out |

Os clientes devem **verificar seu endereço de e-mail** antes de receber quaisquer e-mails de marketing (requisito de opt-in duplo do GDPR).

### Preferências Específicas do App

Os clientes podem controlar notificações de recursos específicos:

**Notificações do Blog**
- Novo post do blog publicado (imediatamente, digesto semanal ou digesto mensal)
- Assinaturas específicas de categoria
- Preferências de frequência

**Programa de Fidelidade**
- Notificações de pontos conquistados
- Atualizações de níveis
- Recompensas desbloqueadas
- Pontos prestes a expirar
- Bônus de aniversário
- Ofertas de campanha

**Programa de Indicações**
- Recompensa concedida (indicador e indicado)
- Cadastro bem-sucedido de indicação
- Recompensa prestes a expirar
- Convites de indicação

**Programa de Afiliados**
- Comissão conquistada
- Comissão aprovada ou rejeitada
- Pagamento processado, concluído ou falhado
- Relatórios de desempenho mensais

### Notificações por SMS (Requer Opt-In Explícito)

Todas as notificações por SMS requerem **opt-in explícito** conforme as regulamentações TCPA. Os clientes devem ativamente marcar a caixa de opt-in de SMS:

- **SMS transacional** — Pedido enviado, entregue (requer opt-in)
- **SMS de marketing** — Promoções, ofertas especiais (requer opt-in separado)

Até mesmo o SMS transacional requer opt-in porque o envio de mensagens de texto não solicitadas é regulamentado de forma mais rigorosa do que o e-mail.

## Gerenciando Preferências dos Clientes no Admin

### Visualizando Todas as Preferências

Navegue até **Clientes > Preferências de Comunicação** para ver todas as preferências dos clientes:

| Coluna | Descrição |
|--------|-------------|
| **E-mail do Usuário** | Endereço de e-mail do cliente (link para administração do usuário) |
| **Status do E-mail** | ✓ verde se os e-mails estiverem ativados, ○ cinza se desativados |
| **Status do SMS** | ✓ verde se o SMS estiver ativado, ○ cinza se desativado |
| **Status do Marketing** | Faixa de "Opted In" ou "Opted Out" |
| **Status de Verificação** | 📧✓ se o e-mail foi verificado, 📱✓ se o SMS foi verificado |
| **Fonte do Consentimento** | Onde o cliente deu o consentimento (registro, checkout, centro de preferências) |
| **Atualizado Em** | Última vez que as preferências foram alteradas |

### Filtrando Preferências

Use o sidebar de filtro para encontrar clientes:

- **E-mail Ativado** — Sim/Não
- **SMS Ativado** — Sim/Não
- **Marketing por E-mail** — Sim/Não (ativado para marketing)
- **Marketing por SMS** — Sim/Não (ativado para marketing por SMS)
- **E-mail Verificado** — Sim/Não (verificou seu endereço de e-mail)
- **SMS Verificado** — Sim/Não (verificou seu número de telefone)
- **Fonte do Consentimento** — Registro, Checkout, Centro de Preferências, API, Migração
- **Código de Idioma** — Idioma preferido para comunicações

### Pesquisando Preferências

Pesquise clientes por:
- E-mail do usuário
- Nome de usuário
- Nome
- Sobrenome
- Token de cancelamento

### Ações em Lote

Selecione múltiplos clientes e aplique ações em lote:

**✓ Marcar E-mail como Verificado**
- Verifique manualmente os endereços de e-mail dos clientes
- Útil ao importar clientes de outro sistema
- Invalida o cache de preferências para aplicar as mudanças imediatamente

**🚫 Cancelar Inscrição de Todos os Marketing**
- Desativa todas as comunicações de marketing (e-mail, SMS, todos os apps)
- Mantém e-mails transacionais ativados
- Use isso para clientes que solicitaram ser totalmente cancelados
- Respeita o direito do GDPR de retirada do consentimento

**📥 Exportar Preferências para CSV**
- Exportar preferências dos clientes para planilha
- Inclui todos os campos de preferência e configurações específicas do app
- Útil para auditorias de conformidade e análise
- Formato: CSV com cabeçalhos

## Centro de Preferências de Autoatendimento do Cliente

Os clientes podem gerenciar suas próprias preferências em `/accounts/preferences/` quando conectados.

### Funcionalidades do Centro de Preferências

**Ações Rápidas**
- **Assinar Todos os Marketing** — Ativar todas as comunicações de marketing com um único clique
- **Cancelar Inscrição de Todos** — Desativar todas as comunicações de marketing (mantém e-mails transacionais ativados)

**Cartões de Preferência**
- **E-mails Transacionais** — Somente leitura (sempre ativados, marcados como "Necessários")
- **Comunicações de Marketing** — Alternar ligado/desligado com badge de verificação
- **Preferências do Blog** — Ativar/desativar, selecionar frequência (imediatamente, semanal, mensal)
- **Programa de Fidelidade** — Ativar/desativar tipos específicos de notificações
- **Programa de Indicações** — Ativar/desativar notificações de recompensas
- **Programa de Afiliados** — Ativar/desativar notificações de comissão e pagamento
- **Notificações por SMS** — Optar por entrar/sair do SMS (mostra o status de verificação)

**Atualizações em Tempo Real**
- As mudanças são salvas imediatamente via AJAX
- Nenhuma recarga da página necessária
- Feedback visual quando salvo

### Processo de Verificação de E-mail

Quando um cliente ativa e-mails de marketing:

1. O cliente ativa "E-mails de Marketing" para ON
2. O sistema envia um e-mail de verificação com um link único
3. O cliente clica no link de verificação
4. O e-mail é marcado como verificado (aparece o badge 📧✓)
5. E-mails de marketing serão enviados agora

**Clientes não verificados NÃO receberão e-mails de marketing** mesmo que o interruptor esteja ON. Isso garante conformidade com o opt-in duplo do GDPR.

## Cancelamento de Inscrição em Um Clique

Todos os e-mails de marketing incluem um link de cancelamento no rodapé. Clicando nesse link:

1. Leva o cliente para `/accounts/unsubscribe/<token>/` (não requer login)
2. Mostra do que eles estão se cancelando
3. Permite feedback opcional (razão do cancelamento)
4. Desativa as comunicações de marketing
5. Mantém os e-mails transacionais ativados
6. Fornece um link para o centro completo de preferências

Os clientes podem se reinscrever a qualquer momento via o centro de preferências.

## Conformidade e Requisitos Legais

### Conformidade com o Artigo 7 do GDPR

O sistema garante conformidade total com o Artigo 7 do GDPR:

**✅ Prova de Consentimento**
- Marca de tempo quando o consentimento foi dado
- Fonte do consentimento (registro, checkout, centro de preferências)
- Endereço IP do consentimento
- User agent (informações do navegador)

**✅ Consentimento Separado**
- E-mails de marketing e transacionais são interruptores separados
- Cada app (blog, fidelidade, etc.) requer consentimento individual

**✅ Retirada Fácil**
- Cancelamento em um clique em todos os e-mails de marketing
- Centro de preferências disponível para todos os clientes conectados
- O cancelamento entra em vigor imediatamente

**✅ Consentimento Dado Livremente**
- O padrão é opt-out para marketing (melhor prática do GDPR)
- Nenhuma caixa pré-selecionada (os clientes devem ativamente optar por entrar)

**✅ Consentimento Específico e Informado**
- Descrições claras de o que cada preferência controla
- Preferências granulares por nível de app (não tudo ou nada)

**✅ Consentimento Verificável**
- Opt-in duplo para e-mails de marketing
- Rastreamento de status via EmailOutbox para auditoria

### Conformidade com TCPA (Regulamentações de SMS dos EUA)

Todas as notificações por SMS requerem **opt-in explícito**:

- Os clientes devem ativamente marcar a caixa de opt-in de SMS
- Não são permitidas caixas pré-selecionadas
- Descrição clara do que eles estão optando por entrar
- Cancelamento fácil via centro de preferências
- Todos os envios de SMS são registrados para auditoria de conformidade

### Conformidade com CAN-SPAM (Regulamentações de E-mail dos EUA)

O sistema garante conformidade com CAN-SPAM:

- Link de cancelamento em cada e-mail de marketing
- Processamento imediato do cancelamento (10 dias úteis exigidos, fazemos imediatamente)
- Nome "De" claro (nome da sua loja)
- Endereço físico no rodapé do e-mail
- Nenhuma linha de assunto enganosa

## Entendendo o Status do E-mail no EmailOutbox

Ao visualizar **Sistema de E-mail > Saída de E-mail**, você verá como as preferências afetam a entrega de e-mails:

| Status | Significado | Motivo |
|--------|---------|--------|
| **Pendente** | E-mail em fila para envio | As preferências permitem este e-mail |
| **Na fila** | Na fila de envio | As preferências permitem este e-mail |
| **Pulado** | E-mail não enviado | Preferência do cliente desativada |
| **Enviado** | Entregue com sucesso | E-mail enviado normalmente |

Quando um e-mail é **pulado**, o campo `skip_reason` mostra o motivo:

- **user_preference_disabled** — O cliente desativou este tipo de e-mail nas preferências
- **email_not_verified** — O cliente não verificou seu endereço de e-mail
- **email_disabled** — O cliente desativou todos os e-mails (interruptor mestre)

Este rastro de auditoria é importante para a conformidade com o GDPR — você pode provar que honrou as preferências do cliente.

## Configurações do Site para Preferências

Navegue até **Configurações > Configurações do Site** para configurar os padrões globais de preferência:

**Habilitar Opt-In Duplo para E-mails de Marketing** (Padrão: Sim)
- Requer verificação do e-mail antes de enviar e-mails de marketing
- Melhor prática do GDPR
- Recomendado: Mantenha habilitado

**Estado Padrão de Opt-In de Marketing** (Padrão: Não - Opt-Out)
- Estado padrão quando novos clientes se registram
- O GDPR exige opt-out padrão
- Recomendado: Mantenha como opt-out (Falso)

**Centro de Preferências Habilitado** (Padrão: Sim)
- Permite que os clientes gerenciem suas próprias preferências
- Requerido para o direito do GDPR de retirada do consentimento
- Recomendado: Mantenha habilitado

**Requer Verificação de SMS** (Padrão: Não)
- Requer verificação do número de telefone para notificações por SMS
- Opcional, mas recomendado para remetentes de SMS de alto volume
- Pode ser habilitado se quiser opt-in duplo para SMS

**Mostrar Motivos de Cancelamento** (Padrão: Sim)
- Coleta feedback opcional quando os clientes se cancelam
- Ajuda a entender por que os clientes estão optando por sair
- Recomendado: Mantenha habilitado para insights

## Boas Práticas

### 1. Padrão para Opt-Out em Marketing

Sempre defina as comunicações de marketing para **opt-out** (desmarcado):
- Conforma com o GDPR
- Constrói confiança com os clientes
- Reduz reclamações de spam
- Envie apenas para clientes engajados

### 2. Requer Verificação de E-mail

Mantenha **Opt-In Duplo** habilitado:
- Garante que os endereços de e-mail sejam válidos
- Confirma que o cliente realmente deseja receber e-mails de marketing
- Reduz a taxa de rejeição
- Requerido para conformidade com o GDPR

### 3. Respeite as Preferências Imediatamente

Quando um cliente altera as preferências:
- As mudanças entram em vigor imediatamente
- O cache de preferência é invalidado
- O próximo envio de e-mail verificará as preferências atualizadas
- Nenhuma demora em atender solicitações de cancelamento

### 4. Monitore E-mails Pulsados

Verifique regularmente a **Saída de E-mail** para e-mails pulsados:
- Taxa de pulso alta indica que os clientes estão se cancelando
- Pode sinalizar que o conteúdo do e-mail precisa ser melhorado
- Ajuda a identificar problemas de preferência

### 5. Auditorias de Conformidade Periódicas

Exportar preferências periodicamente para conformidade:
1. Navegue até **Preferências de Comunicação**
2. Selecione todos os clientes
3. Escolha **Exportar Preferências para CSV**
4. Salve para rastro de auditoria do GDPR

Armazene as exportações por **pelo menos 3 anos** para cumprir os requisitos de retenção de dados do GDPR.

### 6. Comunicação Clara

Ao coletar consentimento:
- Use linguagem clara, não jargões legais
- Explique o que os clientes receberão
- Mostre a frequência (diária, semanal, mensal)
- Faça os campos de opt-in visíveis, mas não pré-selecionados

### 7. Segmentar por Preferência

Ao enviar campanhas de marketing:
- Envie apenas para clientes verificados e opt-in
- Respeite as preferências específicas do app (não envie e-mails do blog para clientes que desativaram o blog)
- Use preferências de frequência (não envie e-mails imediatos para assinantes de digesto semanal)

## Dicas

**💡 Verifique as Preferências Antes de Enviar**

O sistema verifica automaticamente as preferências quando você envia e-mails usando `EmailSendingService.send_template_email()`. Certifique-se de que todos os envios de e-mail usem este serviço, não chamadas diretas SMTP.

**💡 O Status de Pulsado é Normal**

Não se preocione com e-mails pulsados na saída — isso significa que o sistema está funcionando corretamente e respeitando as preferências do cliente. É melhor pular e-mails indesejados do que correr o risco de multas do GDPR ou reclamações de spam.

**💡 O Cache de Preferência é de 5 Minutos**

Verificações de preferência são cacheadas por 5 minutos para desempenho. Quando os clientes alteram preferências via o centro de preferências ou ações do admin, o cache é invalidado imediatamente para que as mudanças entrem em vigor imediatamente.

**💡 Clientes Anônimos Pularão as Verificações**

Clientes que fizeram checkout anônimo (sem conta) receberão todos os e-mails normalmente porque não têm registro de preferência. Isso é intencional — eles optaram por entrar fornecendo seu e-mail no checkout.

**💡 E-mails Transacionais Sempre Enviados**

Confirmações de pedido, atualizações de envio e e-mails de segurança da conta **sempre são enviados** independentemente das preferências. Isso garante que os clientes recebam informações críticas sobre seus pedidos e contas.

**💡 Use Ações em Lote com Cuidado**

A ação em lote "Cancelar Inscrição de Todos os Marketing" afeta **todos os apps** (blog, fidelidade, indicações, afiliados). Use isso apenas para clientes que solicitaram explicitamente ser totalmente cancelados. Para preferências específicas, edite os registros de clientes individuais.

**💡 Rastro de Auditoria para Conformidade**

O sistema rastreia:
- Marca de tempo e fonte do consentimento
- Endereço IP e user agent
- Marca de tempo da verificação do e-mail
- Cada mudança de preferência via status de pulso do EmailOutbox

Este rastro de auditoria prova a conformidade com o GDPR se as autoridades solicitarem evidências de consentimento.

## Tópicos Relacionados

- [Gerenciamento de Contas de Clientes](/help/managing-customer-accounts) — Gerenciamento do perfil do cliente
- [Configuração de E-mail](/help/email-configuration) — Configuração SMTP e modelos de e-mail

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.