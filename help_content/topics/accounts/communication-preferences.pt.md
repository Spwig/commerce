---
title: Preferências de Comunicação
---

As preferências de comunicação permitem que os clientes controlem quais e-mails e mensagens de SMS recebem de sua loja. Este sistema garante conformidade com o RGPD e ajuda você a respeitar as preferências de comunicação dos clientes em todos os canais.

Navegue até **Clientes > Preferências de Comunicação** no menu lateral do administrador para gerenciar as preferências de comunicação dos clientes.

## Entendendo as Preferências de Comunicação

O sistema de preferências de comunicação fornece controle granular aos clientes sobre as mensagens que recebem. Isso inclui:

- **E-mails de transação** — Confirmações de pedido, atualizações de envio, e-mails de segurança da conta (sempre ativados)
- **E-mails de marketing** — Newsletters, promoções, recomendações de produtos (requer opt-in)
- **Notificações específicas do aplicativo** — Postagens de blog, pontos de fidelidade, recompensas de indicação, comissões de afiliados
- **Notificações por SMS** — Notificações por mensagem de texto (requer opt-in explícito conforme regulamentado pelo TCPA)

Todos os comunicados de marketing exigem consentimento do cliente e verificação de e-mail para garantir conformidade com o RGPD.

## Explicação dos Tipos de Preferência

### Comunicações de Transação (Sempre Habilitadas)

As mensagens de transação são essenciais para a conta e pedidos do cliente. Essas **não podem ser desativadas** pelos clientes:

| Tipo | Descrição | Exemplos |
|------|-------------|----------|
| **Confirmações de Pedido** | Confirmação quando o pedido é feito | Pedido #12345 foi recebido |
| **Atualizações de Envio** | Notificações quando o status do pedido muda | Seu pedido foi enviado |
| **Confirmações de Pagamento** | Pagamento recebido, reembolso processado | Confirmação de pagamento de $49,99 |
| **Segurança da Conta** | Redefinição de senha, verificação de e-mail | Redefina sua senha |

### Comunicações de Marketing (Opt-In Necessário)

As mensagens de marketing exigem consentimento do cliente e verificação de e-mail:

| Tipo | Descrição | Padrão |
|------|-------------|---------|
| **Newsletter** | Notícias gerais e atualizações | Opt-out |
| **Ofertas de Marketing** | Vendas, descontos, ofertas especiais | Opt-out |
| **Recomendações de Produtos** | Sugestões de produtos personalizadas | Opt-out |
| **Produto Restaurado** | Notificações quando os produtos voltam | Opt-out |

Os clientes devem **verificar o endereço de e-mail** antes de receber quaisquer e-mails de marketing (exigência de opt-in duplo do RGPD).

### Preferências Específicas do Aplicativo

Os clientes podem controlar notificações de recursos específicos:

**Notificações de Blog**
- Nova postagem de blog publicada (imediata, resumo semanal ou resumo mensal)
- Assinaturas específicas de categoria
- Preferências de frequência

**Programa de Fidelidade**
- Notificações de pontos ganhos
- Aumento de nível
- Recompensas desbloqueadas
- Pontos próximos de expiração
- Bônus de aniversário
- Ofertas de campanha

**Programa de Indicação**
- Recompensa concedida (referidor e indicado)
- Cadastro bem-sucedido de indicação
- Recompensa próxima de expiração
- Convites de indicação

**Programa de Afiliados**
- Comissão ganha
- Comissão aprovada ou rejeitada
- Pagamento processado, concluído ou falho
- Relatórios de desempenho mensal

### Notificações por SMS (Opt-In Explícito Necessário)

Todas as notificações por SMS exigem **opt-in explícito** conforme regulamentado pela TCPA. Os clientes devem marcar ativamente a caixa de opt-in para SMS:

- **SMS de transação** — Pedido enviado, entregue (opt-in necessário)
- **SMS de marketing** — Promoções, ofertas especiais (opt-in separado necessário)

Mesmo os SMS de transação exigem opt-in, pois enviar mensagens de texto não solicitadas é regulamentado de forma mais rigorosa do que e-mail.

## Gerenciando as Preferências dos Clientes no Admin

### Visualizando todas as Preferências

Navegue até **Clientes > Preferências de Comunicação** para ver todas as preferências dos clientes:

| Coluna | Descrição |
|--------|-------------|
| **Email do Usuário** | Endereço de e-mail do cliente (link para o admin de usuários) |
| **Status do E-mail** | Verde ✓ se os e-mails estiverem habilitados, cinza ○ se estiverem desativados |
| **Status do SMS** | Verde ✓ se o SMS estiver habilitado, cinza ○ se estiver desativado |
| **Status de Marketing** | Faixa de "Optou por" ou "Optou contra" |
| **Status de Verificação** | 📧✓ se o e-mail estiver verificado, 📱✓ se o SMS estiver verificado |
| **Fonte de Consentimento** | Onde o cliente consentiu (registro, checkout, centro de preferências) |
| **Atualizado em** | Última vez que as preferências foram alteradas |

### Filtro de Preferências

Use o painel de filtro para encontrar clientes:

- **E-mail Habilitado** — Sim/Não
- **SMS Habilitado** — Sim/Não
- **Marketing por E-mail** — Sim/Não (optou por marketing)
- **Marketing por SMS** — Sim/Não (optou por marketing por SMS)
- **E-mail Verificado** — Sim/Não (verificou seu endereço de e-mail)
- **SMS Verificado** — Sim/Não (verificou seu número de telefone)
- **Fonte de Consentimento** — Registro, Checkout, Centro de Preferências, API, Migração
- **Código de Idioma** — Idioma preferido para comunicações

### Pesquisa de Preferências

Pesquise por clientes por:
- Email do usuário
- Nome de usuário
- Nome
- Sobrenome
- Token de cancelamento de assinatura

### Ações em Larga

Selecione vários clientes e aplique ações em larga:

**✓ Marcar E-mail como Verificado**
- Verificar manualmente os endereços de e-mail dos clientes
- Útil ao importar clientes de outro sistema
- Invalida o cache de preferências para aplicar as alterações imediatamente

**🚫 Cancelar Assinatura de Todos os Marketing**
- Desativa todas as comunicações de marketing (e-mail, SMS, todos os aplicativos)
- Mantém os e-mails transacionais habilitados
- Use isso para clientes que solicitam o cancelamento completo
- Respeita o direito do GDPR de retirar o consentimento

**📥 Exportar Preferências para CSV**
- Exportar as preferências dos clientes para planilha
- Inclui todos os campos de preferência e configurações específicas do aplicativo
- Útil para auditorias de conformidade e análise
- Formato: CSV com cabeçalhos

## Centro de Preferências de Autogestão do Cliente

Os clientes podem gerenciar suas próprias preferências em `/accounts/preferences/` ao fazer login.

### Recursos do Centro de Preferências

**Ações Rápidas**
- **Assinar Todos os Marketing** — Ativar todas as comunicações de marketing em um clique
- **Cancelar Assinatura de Todos** — Desativar todas as comunicações de marketing (transacionais ainda estão habilitadas)

**Cartões de Preferências**
- **E-mails Transacionais** — Apenas leitura (sempre habilitado, marcado como "Obrigatório")
- **Comunicações de Marketing** — Ativar/desativar com selo de verificação
- **Preferências do Blog** — Ativar/desativar, selecionar frequência (imediata, semanal, mensal)
- **Programa de Fidelidade** — Ativar/desativar tipos individuais de notificação
- **Programa de Indicação** — Ativar/desativar notificações de recompensas
- **Programa de Afiliados** — Ativar/desativar notificações de comissão e pagamento
- **Notificações por SMS** — Optar por entrar/sair do SMS (mostra o status de verificação)

**Atualizações em Tempo Real**
- Alterações salvas imediatamente via AJAX
- Nenhuma recarrega de página necessária
- Feedback visual quando salvo

### Processo de Verificação por E-mail

Quando um cliente ativa os e-mails de marketing:

1. O cliente ativa a opção "Comunicações de Marketing" para ON
2. O sistema envia um e-mail de verificação com um link único
3. O cliente clica no link de verificação
4. O e-mail é marcado como verificado (o selo 📧✓ aparece)
5. Os e-mails de marketing agora serão enviados

**Clientes não verificados NÃO receberão e-mails de marketing**, mesmo que a opção esteja ativada. Isso garante conformidade com o double opt-in do GDPR.

## Cancelamento de Um Clique

Todos os e-mails de marketing incluem um link de cancelamento de assinatura no rodapé. Clicar nesse link:

1. Leva o cliente para `/accounts/unsubscribe/<token>/` (sem necessidade de login)
2. Mostra o que eles estão se cancelando
3. Permite feedback opcional (motivo do cancelamento)
4. Desativa as comunicações de marketing
5. Mantém os e-mails transacionais habilitados
6. Fornece link para o centro completo de preferências

Os clientes podem se ressuscitar a qualquer momento pelo centro de preferências.

## Requisitos de Conformidade e Legais

### Conformidade com o Artigo 7 do GDPR

O sistema garante conformidade plena com o Artigo 7 do GDPR:

Preserve todos os formatos de markdown, caminhos de imagens, blocos de código e termos técnicos.

**✅ Prova de Consentimento**
- Carimbo de data e hora quando o consentimento foi dado
- Origem do consentimento (registro, checkout, centro de preferências)
- Endereço IP do consentimento
- User agent (informações do navegador)

**✅ Consentimento Separado**
- E-mails de marketing e transacionais são alternadores separados
- Cada aplicativo (blog, fidelidade, etc.) requer consentimento individual

**✅ Retirada Fácil**
- Cancelamento de inscrição com um clique em todos os e-mails de marketing
- Centro de preferências disponível para todos os clientes conectados
- O cancelamento de inscrição tem efeito imediato

**✅ Consentimento Livremente Dado**
- O padrão é opt-out para marketing (melhor prática do GDPR)
- Nenhuma caixa pré-marcada (os clientes devem ativar ativamente o opt-in)

**✅ Consentimento Específico e Informado**
- Descrições claras do que cada preferência controla
- Preferências granulares por aplicativo (não tudo ou nada)

**✅ Consentimento Verificável**
- Double opt-in para e-mails de marketing
- Rastreio de auditoria via acompanhamento de status do EmailOutbox

### Conformidade TCPA (Regulamentos de SMS dos EUA)

Todas as notificações por SMS requerem **opt-in explícito**:

- Os clientes devem marcar ativamente a caixa de opt-in de SMS
- Caixas pré-marcadas não são permitidas
- Descrição clara do que estão optando
- Cancelamento fácil via centro de preferências
- Todos os envios de SMS são registrados para auditoria de conformidade

### Conformidade CAN-SPAM (Regulamentos de E-mail dos EUA)

O sistema garante a conformidade com o CAN-SPAM:

- Link de cancelamento de inscrição em cada e-mail de marketing
- Cancelamento de inscrição processado imediatamente (exigido em 10 dias úteis, nós fazemos instantaneamente)
- Nome "De" claro (o nome da sua loja)
- Endereço físico no rodapé do e-mail
- Nenhuma linha de assunto enganosa

## Compreendendo o Status de E-mail no EmailOutbox

Ao visualizar **Sistema de E-mail > Caixa de Saída de E-mails**, você verá como as preferências afetam a entrega de e-mails:

| Status | Significado | Motivo |
|--------|---------|--------|
| **Pendente** | E-mail enfileirado para envio | Preferências permitem este e-mail |
| **Enfileirado** | Na fila de envio | Preferências permitem este e-mail |
| **Pulado** | E-mail não enviado | Preferência do cliente desativada |
| **Enviado** | Entregue com sucesso | E-mail enviado normalmente |

Quando um e-mail é **pulado**, o campo `skip_reason` mostra o motivo:

- **user_preference_disabled** — O cliente desativou este tipo de e-mail nas preferências
- **email_not_verified** — O cliente não verificou seu endereço de e-mail
- **email_disabled** — O cliente desativou todos os e-mails (alternador principal)

Este rastro de auditoria é importante para a conformidade com o GDPR — você pode provar que honrou as preferências dos clientes.

## Configurações do Site para Preferências

Navegue para **Configurações > Configurações do Site** para configurar os padrões globais de preferências:

**Ativar Double Opt-In para E-mails de Marketing** (Padrão: Sim)
- Requer verificação de e-mail antes de enviar e-mails de marketing
- Melhor prática do GDPR
- Recomendado: Manter ativado

**Estado Padrão de Opt-In de Marketing** (Padrão: Não - Opt-Out)
- Estado padrão quando novos clientes se registram
- O GDPR requer opt-out por padrão
- Recomendado: Manter como opt-out (False)

**Centro de Preferências Ativado** (Padrão: Sim)
- Permite que os clientes gerenciem suas próprias preferências
- Obrigatório para o direito de retirada de consentimento do GDPR
- Recomendado: Manter ativado

**Exigir Verificação de SMS** (Padrão: Não)
- Exigir verificação de número de telefone para notificações por SMS
- Opcional, mas recomendado para remetentes de SMS de alto volume
- Pode ser ativado se você quiser double opt-in para SMS

**Mostrar Motivos de Cancelamento de Inscrição** (Padrão: Sim)
- Coletar feedback opcional quando os clientes cancelam a inscrição
- Ajuda a entender por que os clientes estão optando
- Recomendado: Manter ativado para insights

## Melhores Práticas

### 1. Padrão para Opt-Out de Marketing

Sempre defina as comunicações de marketing como **opt-out** (desmarcado):
- Em conformidade com o GDPR
- Constrói confiança com os clientes
- Reduz reclamações de spam
- Envie apenas para clientes engajados

### 2. Exigir Verificação de E-mail

Mantenha o **Double Opt-In** ativado:
- Garante que os endereços de e-mail sejam válidos
- Confirma que o cliente realmente deseja e-mails de marketing
- Reduz a taxa de rejeição
- Obrigatório para conformidade com o GDPR

### 3. Respeitar Preferências Imediatamente

Preserve todo o formato markdown, caminhos de imagem, blocos de código e termos técnicos. /no_think

Quando um cliente altera as preferências:
- As alterações têm efeito imediato
- O cache de preferências é invalidado
- O próximo envio de e-mail verificará as preferências atualizadas
- Não há atraso no atendimento de solicitações de cancelamento de inscrição

### 4. Monitorar E-mails Ignorados

Verifique regularmente a **Caixa de Saída de E-mails** em busca de e-mails ignorados:
- Uma taxa alta de ignorados indica que os clientes estão cancelando a inscrição
- Pode sinalizar a necessidade de melhorar o conteúdo dos e-mails
- Ajuda a identificar problemas de preferências

### 5. Auditorias de Conformidade Regulares

Exporte as preferências periodicamente para fins de conformidade:
1. Navegue até **Preferências de Comunicação**
2. Selecione todos os clientes
3. Escolha **Exportar Preferências para CSV**
4. Salve para o rastro de auditoria do GDPR

Guarde as exportações por **pelo menos 3 anos** para cumprir os requisitos de retenção de dados do GDPR.

### 6. Comunicação Clara

Ao coletar o consentimento:
- Use linguagem simples, não jargão legal
- Explique o que os clientes receberão
- Mostre a frequência (diária, semanal, mensal)
- Faça as caixas de inscrição em destaque, mas não pré-marcadas

### 7. Segmentar por Preferência

Ao enviar campanhas de marketing:
- Envie apenas para clientes verificados e inscritos
- Respeite as preferências específicas do aplicativo (não envie e-mails do blog para clientes que desativaram o blog)
- Use as preferências de frequência (não envie e-mails imediatos para assinantes do resumo semanal)

## Dicas

**💡 Verifique a Preferência Antes de Enviar**

O sistema verifica automaticamente as preferências quando você envia e-mails usando `EmailSendingService.send_template_email()`. Certifique-se de que todos os envios de e-mail usem este serviço, e não chamadas diretas de SMTP.

**💡 O Status Ignorado é Normal**

Não se preocupe com e-mails ignorados na caixa de saída — isso significa que o sistema está funcionando corretamente e respeitando as preferências dos clientes. É melhor ignorar e-mails indesejados do que arriscar multas do GDPR ou reclamações de spam.

**💡 O Cache de Preferências é de 5 Minutos**

As verificações de preferências são armazenadas em cache por 5 minutos para desempenho. Quando os clientes alteram as preferências via o centro de preferências ou ações administrativas, o cache é invalidado imediatamente para que as alterações tenham efeito imediato.

**💡 Clientes Convidados Bypassam as Verificações**

Clientes de checkout como convidados (sem conta) receberão todos os e-mails normalmente, pois não possuem registro de preferências. Isso é intencional — eles deram seu consentimento ao fornecer seu e-mail no checkout.

**💡 E-mails Transacionais Sempre São Enviados**

Confirmações de pedido, atualizações de envio e e-mails de segurança da conta **sempre são enviados**, independentemente das preferências. Isso garante que os clientes recebam informações críticas sobre seus pedidos e contas.

**💡 Use Ações em Lote com Cuidado**

A ação em lote "Cancelar Inscrição de Todo o Marketing" afeta **todos os aplicativos** (blog, fidelidade, indicações, afiliados). Use apenas para clientes que solicitaram explicitamente o cancelamento total. Para preferências específicas, edite os registros individuais dos clientes.

**💡 Rastro de Auditoria para Conformidade**

O sistema rastreia:
- Carimbo de data e hora do consentimento e origem
- Endereço IP e user agent
- Carimbo de data e hora da verificação de e-mail
- Cada alteração de preferência via status ignorado da Caixa de Saída de E-mails

Este rastro de auditoria prova a conformidade com o GDPR caso as autoridades solicitem evidências do consentimento.

## Tópicos Relacionados

- [Gerenciamento de Contas de Clientes](/help/managing-customer-accounts) — Gerenciamento de perfil do cliente
- [Configuração de E-mail](/help/email-configuration) — Configuração de SMTP e modelos de e-mail