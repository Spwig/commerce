---
title: Configuração de E-mail
---

A configuração de e-mail controla como sua loja envia e-mails transacionais — confirmações de pedido, notificações de envio, redefinições de senha e muito mais. O Spwig inclui um servidor SMTP integrado e suporta provedores externos de e-mail para maior entregabilidade.

![Contas de e-mail](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Provedores Disponíveis

| Provedor | Descrição |
|----------|-------------|
| **SMTP Integrado** | Servidor de e-mail gratuito e auto-hospedado incluído com o Spwig. Assinatura DKIM automática. |
| **Gmail API** | Envie através da sua conta Gmail ou Google Workspace usando autenticação OAuth. |
| **SMTP Genérico** | Conecte qualquer servidor SMTP (SendGrid, Mailgun, Amazon SES ou seu próprio servidor de e-mail). |

## Configuração de E-mail

Navegue até **Configurações > Contas de E-mail** e clique em **Adicionar Conta de E-mail** para iniciar o assistente de configuração.

### Etapa 1: Selecionar Provedor

Escolha seu provedor de e-mail. O servidor SMTP integrado é a opção mais simples para começar — não requer contas externas.

### Etapa 2: Configurar Credenciais

Insira as credenciais para o provedor escolhido:

- **SMTP Integrado** — Nenhuma credencial necessária. O servidor é executado na sua instalação do Spwig.
- **Gmail API** — Autentique via Google OAuth. Você será redirecionado para fazer login com sua conta Google.
- **SMTP Genérico** — Insira o endereço do servidor SMTP, porta, nome de usuário e senha.

### Etapa 3: Configuração do Remetente

Defina a identidade do remetente para os e-mails de saída:

- **E-mail do Remetente** — O endereço de e-mail que aparece no campo "De" (ex.: orders@yourstore.com)
- **Nome do Remetente** — O nome de exibição ao lado do endereço de e-mail (ex.: "Nome da Sua Loja")
- **E-mail de Resposta** — Para onde as respostas dos clientes são direcionadas (pode diferir do endereço do remetente)

### Etapa 4: Validação DNS

Verifique os registros de autenticação de e-mail do seu domínio. O assistente verifica três registros DNS:

| Registro | Propósito |
|--------|---------|
| **SPF** | Autoriza seu servidor a enviar e-mails em nome do seu domínio |
| **DKIM** | Assina digitalmente os e-mails para provar que não foram adulterados |
| **DMARC** | Informa aos servidores receptores o que fazer com e-mails que falham nas verificações SPF/DKIM |

Para cada registro, o assistente mostra:
- **Status atual** — Se o registro está configurado corretamente
- **Valor necessário** — O registro DNS exato a ser adicionado no seu registrador de domínio
- **Status de propagação** — Se as alterações recentes entraram em vigor (as alterações de DNS podem levar até 48 horas)

O servidor SMTP integrado gera automaticamente as chaves DKIM para o seu domínio.

### Etapa 5: Enviar E-mail de Teste

Envie um e-mail de teste para verificar se tudo funciona:
1. Insira um endereço de e-mail do destinatário
2. Clique em **Enviar Teste**
3. Verifique sua caixa de entrada em busca da mensagem de teste
4. Verifique se o e-mail chega sem avisos de spam

### Etapa 6: Salvar e Ativar

Salve a configuração e defina a conta como ativa. Marque-a como **Padrão** se ela deve ser a conta de e-mail principal.

## Modelos de E-mail

O Spwig inclui mais de 30 modelos de e-mail para todos os eventos transacionais. Navegue até **Configurações > Modelos de E-mail** para gerenciá-los.

### Tipos de Modelos

Os modelos cobrem todos os eventos da loja, incluindo:
- **Ciclo de Vida do Pedido** — Confirmação, processamento, enviado, entregue, cancelado
- **Pagamento** — Recibo, confirmação de reembolso, pagamento falho
- **Conta do Cliente** — Boas-vindas, redefinição de senha, verificação de e-mail
- **Cartões Presente** — Entrega, notificação de saldo
- **Envio** — Atualizações de rastreamento, confirmação de entrega
- **Produtos Digitais** — Links de download, chaves de licença
- **Marketing** — Recuperação de carrinho abandonado, solicitações de avaliação

### Personalização de Modelos

1. Navegue até a lista de modelos
2. Clique em um modelo para editar
3. Modifique a linha de assunto, cabeçalho, conteúdo do corpo e rodapé
4. Use variáveis de modelo (ex.: `{{ order.number }}`, `{{ customer.name }}`) para conteúdo dinâmico
5. Visualize o e-mail antes de salvar

### Suporte Multilíngue

Preserve todo o formato markdown, caminhos de imagem, blocos de código e termos técnicos.

Os modelos de e-mail suportam múltiplos idiomas:
- Cada modelo pode ter traduções para todos os idiomas ativos da sua loja
- O sistema envia e-mails no idioma preferido do cliente
- **Cadeia de fallback de idioma** — Se uma tradução não estiver disponível, o sistema recorre ao idioma padrão da loja
- Use o recurso **Tradução por IA** para traduzir automaticamente os modelos para outros idiomas

### Clonagem de Modelos

Para criar uma versão personalizada de um modelo do sistema:
1. Abra o modelo que deseja modificar
2. Clique em **Clonar Modelo**
3. Edite a versão clonada
4. O clone tem prioridade sobre o modelo original do sistema

## Fila de E-mails

Monitore os e-mails de saída em **Configurações > Fila de E-mails**:

- **Na fila** — E-mails aguardando envio
- **Enviando** — Atualmente em transmissão
- **Enviado** — Entregue com sucesso
- **Falhou** — Não pôde ser entregue (com detalhes do erro)
- **Rejeitado** — Rejeitado pelo servidor de e-mail do destinatário

Clique em qualquer e-mail para ver todos os seus detalhes, incluindo destinatário, assunto, horário de envio e status de entrega.

## Rastreamento de Entrega

Acompanhe o engajamento dos e-mails:
- **Aberturas** — Quantos destinatários abriram o e-mail
- **Cliques** — Cliques em links dentro do e-mail
- **Rejeições** — Rastreamento de rejeições duras e suaves
- **Reclamações** — Relatórios de spam dos destinatários

## Múltiplas Contas

Você pode configurar múltiplas contas de e-mail:
- **Conta Padrão** — Usada para todos os e-mails de saída, a menos que seja substituída
- **Fallback** — Se a conta padrão falhar, os e-mails ficam na fila para nova tentativa
- Use contas diferentes para diferentes finalidades (por exemplo, uma para e-mails transacionais, outra para marketing)

## Modo de Entrega de E-mails

Navegue até **Configurações > Configurações da Loja** para controlar como sua loja lida com e-mails de saída. Essas configurações são úteis durante o desenvolvimento e testes.

| Modo | Descrição |
|------|-------------|
| **Ao vivo** | Os e-mails são entregues normalmente aos destinatários reais |
| **Pausado** | Os e-mails ficam retidos na fila e não são enviados até que você volte para o modo Ao vivo |
| **Apenas Log** | Os e-mails são registrados na caixa de saída, mas nunca são entregues |

### Redirecionamento de E-mail de Teste

Defina um endereço de **Redirecionamento de E-mail de Teste** para interceptar todos os e-mails de saída e redirecioná-los para um único endereço. Quando definido, todos os e-mails — independentemente do destinatário real — vão para esse endereço em vez do original. Isso é útil para testar modelos de e-mail sem enviar acidentalmente para clientes reais. Deixe em branco para enviar e-mails aos destinatários reais.

### Lista de Permissões de E-mail em Sandbox

No modo sandbox ou de desenvolvimento, você pode restringir a entrega de e-mails a uma lista de permissões de endereços aprovados. Apenas e-mails para endereços na lista de permissões serão entregues. Todos os outros e-mails são registrados, mas nunca enviados. O e-mail do administrador é sempre incluído automaticamente. Você pode adicionar até 10 endereços.

## Dicas

- Comece com o servidor **SMTP Integrado** para uma configuração rápida, depois mude para um provedor externo se precisar de maiores volumes de envio ou melhor entregabilidade.
- Configure sempre os registros **SPF, DKIM e DMARC** — sem eles, os e-mails têm muito mais probabilidade de cair em pastas de spam.
- Envie um **e-mail de teste** após qualquer alteração de configuração para verificar se a entrega funciona.
- Monitore a fila de e-mails regularmente em busca de e-mails **falhos** ou **rejeitados** — esses indicam problemas de entregabilidade.
- Use um **endereço de remetente profissional** (por exemplo, pedidos@sualoja.com) em vez de um endereço de e-mail gratuito para melhor confiança e entregabilidade.
- Mantenha seus modelos concisos — os e-mails transacionais devem entregar informações rapidamente, e não serem newsletters de marketing.