---
title: Gerenciamento de Contas de Clientes
---

Contas de clientes permitem que comerciantes acompanhem informações de clientes, histórico de pedidos e preferências. Navegue até **Clientes > Todos os Clientes** no menu lateral do administrador para gerenciar contas de clientes.

![Adicionar Cliente](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Entendendo Contas de Clientes vs Perfis de Clientes

**Contas de Clientes** são as credenciais de login (e-mail/senha) armazenadas no modelo de usuário. **Perfis de Clientes** armazenam informações adicionais sobre clientes, como número de telefone, data de nascimento, preferências e análises. Cada conta de cliente tem um perfil correspondente que armazena esses dados estendidos.

Quando você gerencia clientes no administrador, está trabalhando com Perfis de Clientes que estão vinculados a contas de usuários no fundo.

## Visualizando Todos os Clientes

A lista de clientes mostra todos os clientes registrados com métricas-chave:

| Coluna | Descrição |
|--------|-------------|
| **Usuário** | Nome e endereço de e-mail do cliente |
| **Status de Afiliado** | Se o cliente também é um parceiro afiliado |
| **Valor do Cliente** | Valor total gasto pelo cliente (codificado em cores) |
| **Segmento do Cliente** | Segmento RFM (Campeão, Fidelizado, Em Risco, etc.) |
| **Total de Pedidos** | Número de pedidos concluídos |
| **Dias desde o Último Pedido** | Recência do último pedido |
| **Cliente VIP** | Badge se o cliente for marcado como VIP |

### Filtrando Clientes

Use o sidebar de filtro para reduzir a lista:

- **Status de Afiliado** — É Afiliado, Não é Afiliado, Afiliado Pendente, Ativo, Suspensão, Rejeitado
- **Layout do Dashboard** — Layout do dashboard preferido pelo cliente
- **Inscrito em Newsletter** — Se o cliente optou por receber newsletters
- **E-mails de Marketing** — Se o cliente optou por receber e-mails de marketing
- **Criado em** — Filtre por data de registro

### Buscando Clientes

Use a barra de busca para encontrar clientes por:
- Nome de usuário
- Endereço de e-mail
- Nome
- Sobrenome
- Número de telefone

## Visualizando Detalhes do Cliente

Clique no nome do cliente para ver seu perfil completo. A página de detalhes do cliente mostra:

![Detalhes do Cliente](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Seção de Informações do Cliente

Detalhes de contato básicos e status da conta:
- **Usuário** — Link para a conta de usuário subjacente
- **Telefone** — Número de telefone do cliente
- **Data de Nascimento** — Para verificação de idade e campanhas de aniversário

### Preferências do Dashboard

Como o cliente personalizou seu dashboard de conta:
- **Layout do Dashboard** — Visual em grade, lista ou compacto
- **Mostrar Histórico de Pedidos** — Se o histórico de pedidos aparece no dashboard
- **Mostrar Lista de Desejos** — Se a lista de desejos aparece no dashboard
- **Mostrar Produtos Recentes** — Se produtos recentemente visualizados aparecem
- **Mostrar Recomendações** — Se recomendações de produtos aparecem

### Preferências de Comunicação

Status de inscrição do cliente para várias comunicações:
- **Inscrito em Newsletter** — Optou por receber newsletters gerais
- **E-mails de Marketing** — Optou por receber e-mails promocionais
- **Notificações de Pedido** — Optou por receber atualizações de status do pedido

### Análises do Cliente

Resumos somente leitura do comportamento e valor do cliente:
- **Resumo de Análises do Cliente** — Pontuação RFM, segmento, valor de vida
- **Resumo do Comportamento de Compra** — Frequência de pedidos, valor médio por pedido, categorias preferidas
- **Resumo de Engajamento** — Último login, taxas de abertura de e-mails, atividade no site

Esses campos de análise são calculados automaticamente e não podem ser editados manualmente. Veja [Entendendo Análises de Cliente](customer-analytics.md) para detalhes.

## Criando uma Conta de Cliente

Comerciantes podem criar manualmente contas de clientes para pedidos por telefone, pickups no estabelecimento ou para registrar previamente clientes atacadistas.

1. Clique em **+ Adicionar Perfil de Cliente** no canto superior direito
2. Preencha os campos obrigatórios e opcionais:

| Campo | Obrigatório | Descrição |
|-------|-------------|-------------|
| **Usuário** | Sim | Selecione uma conta de usuário existente ou crie uma nova |
| **Telefone** | Não | Número de telefone do cliente |
| **Data de Nascimento** | Não | Para verificação de idade e campanhas de aniversário |
| **Inscrito em Newsletter** | Não | Opte pelo cliente para newsletters |
| **E-mails de Marketing** | Não | Opte pelo cliente para e-mails de marketing |

### Criando um Novo Usuário ao Adicionar um Perfil

Se o cliente ainda não tem uma conta de usuário:
1. Clique no ícone **+** ao lado do campo Usuário
2. Insira o **endereço de e-mail** do cliente (este se torna seu nome de usuário)
3. Opicionalmente insira **nome** e **sobrenome**
4. Opicionalmente defina uma **senha**
5. Marque **Enviar e-mail de redefinição de senha** se não definir uma senha
6. Salve a conta de usuário
7. Complete os campos do perfil do cliente
8. Clique em **Salvar**

### E-mails de Boas-vindas

Após criar uma conta de cliente:
- Se você definir uma senha, o cliente pode fazer login imediatamente com essa senha
- Se não definir uma senha, o sistema enviará um e-mail de redefinição de senha para que o cliente defina sua própria senha
- Você pode disparar manualmente um e-mail de boas-vindas pelo sistema de e-mails em **Marketing > Campanhas de E-mail**

## Editando Informações do Cliente

Para atualizar detalhes do cliente:
1. Navegue até **Clientes > Todos os Clientes**
2. Clique no nome do cliente
3. Modifique os campos que deseja atualizar
4. Clique em **Salvar**

### O Que Você Pode Editar

**Detalhes de Contato:**
- Nome (via a conta de usuário)
- Endereço de e-mail (via a conta de usuário)
- Número de telefone
- Data de nascimento

**Preferências:**
- Status de inscrição em newsletters
- Opt-in para e-mails de marketing
- Preferências de notificações de pedidos
- Layout do dashboard e configurações de visibilidade

### O Que Você Não Pode Editar

Esses campos são calculados automaticamente com base no comportamento do cliente:
- Total gasto / Valor do cliente
- Contagem de pedidos
- Segmento do cliente (Campeão, Fidelizado, Em Risco, etc.)
- Pontuações RFM
- Previsões de valor de vida
- Data do último pedido
- Resumos de análise

Se esses campos parecerem incorretos, verifique os dados de pedidos subjacentes ou dispare um recálculo manual em **Clientes > Análises** → **Recalcular Métricas**.

## Notas de Cliente

Adicione notas internas sobre clientes para acompanhar problemas de suporte, solicitações de serviço VIP ou tarefas de acompanhamento.

### Adicionando uma Nota

1. Abra o perfil do cliente
2. Role até a seção **Notas do Cliente** (pode ser uma guia separada)
3. Clique em **+ Adicionar Nota**
4. Preencha os detalhes da nota:

| Campo | Descrição |
|-------|-------------|
| **Tipo de Nota** | Geral, Problema de Suporte, Reclamação, Complimento, Serviço VIP, Necessário Acompanhamento, Problema de Pagamento, Problema de Envio |
| **Título** | Resumo breve da nota |
| **Conteúdo** | Conteúdo detalhado da nota |
| **Necessário Acompanhamento** | Marque se esta nota necessita de ação |
| **Data de Acompanhamento** | Data para acompanhar |
| **Concluído** | Marque quando o acompanhamento estiver concluído |

### Tipos de Nota

| Tipo | Caso de Uso |
|------|----------|
| **Nota Geral** | Qualquer observação geral sobre o cliente |
| **Problema de Suporte** | Registro de um ticket de suporte ou problema |
| **Reclamação** | Reclamação do cliente para rastreamento e resolução |
| **Complimento** | Feedback positivo sobre o cliente ou seu feedback sobre você |
| **Serviço VIP** | Solicitações de tratamento especial para clientes VIP |
| **Necessário Acompanhamento** | Tarefas que precisam de ação até uma data específica |
| **Problema de Pagamento** | Notas sobre problemas ou disputas de pagamento |
| **Problema de Envio** | Notas sobre problemas de envio ou solicitações de entrega especial |

### Visualizando Histórico de Notas

Todas as notas aparecem em ordem cronológica no perfil do cliente. Cada nota mostra:
- Data e hora de criação
- Criado por (nome do membro da equipe)
- Badge do tipo de nota
- Título e conteúdo
- Status de acompanhamento, se aplicável

### Notas Internas vs Notas Visíveis ao Cliente

Todas as notas de cliente são **internas apenas** por padrão — os clientes nunca veem essas notas. Elas são para comunicação entre a equipe do comerciante apenas.

Se você precisar se comunicar com o cliente, use o sistema de e-mail em **Marketing > Campanhas de E-mail** ou adicione um comentário à ordem específica.

## Convertendo Visitantes em Clientes Registrados

Clientes visitantes são criados automaticamente quando alguém completa a checkout sem criar uma conta. Seu nome de usuário segue o padrão `visitante_10374` onde o número é um ID único.

Para converter um visitante em um cliente registrado:

1. Navegue até **Clientes > Todos os Clientes**
2. Procure o visitante pelo endereço de e-mail do pedido
3. Clique no perfil do cliente visitante
4. Clique no link **Usuário** para editar a conta de usuário subjacente
5. Mude o **nome de usuário** de `visitante_10374` para o endereço de e-mail real do cliente
6. Mude o **e-mail** para corresponder
7. Opicionalmente adicione **nome** e **sobrenome**
8. Marque **Enviar e-mail de redefinição de senha** para que o cliente defina uma senha
9. Clique em **Salvar**

Agora o cliente pode fazer login com seu endereço de e-mail e verá seus pedidos anteriores como visitante em seu histórico de pedidos.

### Por Que Converter Clientes Visitantes?

- Pedidos de visitantes não contam para análises ou segmentos de clientes
- Visitantes não podem acompanhar pedidos ou acessar histórico de pedidos
- Converter visitantes aumenta a contagem de clientes registrados e melhora a precisão das análises
- Clientes registrados são mais propensos a fazer compras repetidas

## Desativando vs Excluindo Contas

### Desativando uma Conta de Cliente

A desativação impede o login enquanto preserva todos os dados:

1. Abra o perfil do cliente
2. Clique no link **Usuário** para editar a conta de usuário
3. **Desmarque 'Ativo'**
4. Clique em **Salvar**

**O que acontece:**
- O cliente não pode fazer login
- O histórico de pedidos é preservado
- O cliente pode ser reativado posteriormente marcando 'Ativo' novamente
- As análises e métricas permanecem intactas

**Use a desativação para:**
- Suspender temporariamente contas devido a disputas de pagamento
- Bloquear clientes abusivos
- Clientes que solicitaram parar de receber acesso, mas não excluíram os dados

### Excluindo uma Conta de Cliente

A exclusão remove a conta e pode orfanar o histórico de pedidos:

1. Abra o perfil do cliente
2. Role até o final e clique em **Excluir**
3. Confirme a exclusão

**O que acontece:**
- A conta do cliente é removida permanentemente
- O perfil do cliente é excluído
- O histórico de pedidos pode ser orfanado (pedidos existem, mas não estão vinculados a um cliente)
- Não pode ser desfeito

**Use a exclusão para:**
- Pedidos de exclusão de dados sob GDPR/CCPA (exporte os dados primeiro)
- Contas de teste que nunca deveriam existir
- Contas duplicadas criadas por engano

### Conformidade com o GDPR

Antes de excluir uma conta de cliente em resposta a um pedido sob GDPR:

1. Navegue até **Clientes > Todos os Clientes**
2. Selecione o cliente
3. Use a ação **Exportar Dados** para gerar uma exportação completa de dados
4. Envie a exportação ao cliente se ele solicitou
5. Em seguida, prossiga com a exclusão

A exportação inclui: perfil do cliente, histórico de pedidos, endereços, notas e dados de análise.

## Dicas

- **Use filtros para identificar clientes de alto valor** — Filtre por Valor do Cliente para encontrar seus Campeões e VIPs
- **Revise notas de cliente regularmente** — Verifique tarefas de acompanhamento abertas pelo menos semanalmente
- **Não edite análises manualmente** — Deixe o sistema calcular pontuações RFM e segmentos automaticamente
- **Converta visitantes proativamente** — Após um visitante fazer uma segunda compra, entre em contato e ofereça criar uma conta adequada
- **Use desativação em vez de exclusão** — A desativação preserva os dados e pode ser revertida se necessário
- **Adicione notas durante chamadas de suporte** — Documente interações de suporte para que outros membros da equipe tenham contexto
- **Defina datas de acompanhamento** — Use o sistema de tarefas de acompanhamento nas notas para garantir que nada caia no esquecimento
- **Respeite preferências de comunicação** — Nunca envie e-mails de marketing para clientes que optaram por sair

Lembre-se: Retorne APENAS o objeto JSON com os campos "title" e "content". Mantenha todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado acima.