---
title: Tokens da API
---

Tokens da API são chaves seguras que permitem que serviços externos e integrações comuniquem-se com sua loja. Quando um serviço de terceiros ou ferramenta precisa acessar os dados da sua loja ou acionar ações, ela envia um token da API com cada solicitação para que sua loja possa verificar se a solicitação está autorizada. Você cria e gerencia todos os tokens, incluindo exatamente quais partes de sua loja eles podem acessar, na seção Tokens da API do seu painel de administração.

## Quando você precisa de um token da API

Você geralmente precisará criar um token da API quando:

- Conectar um serviço externo ou ferramenta de automação que precise ler ou gravar em sua loja
- Configurar um receptor de webhook que precise autenticar chamadas entrantes
- Configurar o Sistema de Ajuda do Spwig para sua instalação
- Construir uma integração personalizada usando a API do Spwig
- Sincronizar dados entre sua loja do Spwig e outro sistema

Cada integração deve ter seu próprio token para que você possa revogar o acesso para um serviço sem afetar os outros.

## Tipos de token

Ao criar um token, você escolhe um tipo que descreve seu propósito. O tipo é para sua referência e ajuda você a manter o controle sobre o que cada token faz.

| Tipo | Propósito |
|------|---------|
| **Sistema de Ajuda** | Usado pelo sistema de documentação de ajuda do Spwig |
| **Integração Externa** | Serviços de terceiros, ferramentas de automação (ex.: Zapier) ou ferramentas de sincronização de dados |
| **Webhook** | Autenticação para receptores de webhook ou endpoints |
| **Personalizado** | Qualquer outro propósito que não se encaixe nas categorias acima |
| **Sincronização de Instância** | Sincronização entre instalações do Spwig ou serviços externos do Spwig |

## Escopos da API: controlando o que um token pode acessar

Cada token também tem uma seção **Escopos da API** que decide exatamente quais partes de sua loja ele é autorizado a chamar. Em vez de um token ter acesso abrangente a tudo, você concede acesso uma área de cada vez — e no nível que a integração realmente precisa.

**Um token sem escopos selecionados não pode acessar nenhuma API**, mesmo que esteja ativo e válido. Isso é o padrão para um novo token, então uma integração não funcionará até que você conceda intencionalmente acesso a ela.

Para cada escopo, você escolhe um dos três níveis de acesso:

| Nível de Acesso | O que ele permite |
|------------------|------------------|
| **Nenhum acesso** | O token não pode chamar nenhum endpoint nessa área |
| **Leitura** | O token pode recuperar dados dessa área, mas não pode alterar nada |
| **Leitura e Escrita** | O token pode recuperar dados e também criá-los, atualizá-los ou excluí-los |

Os escopos são agrupados para corresponder às áreas do seu painel de administração:

| Grupo | Escopo | Leitura e Escrita disponível? | Concede acesso a |
|-------|-------|:---:|-------------------|
| Análise | **Análise de Vendas** | Apenas Leitura | Dashboards de vendas, KPIs, análises de produtos/clientes/categorias, comparações e exportações |
| Análise | **Análise Web** | Apenas Leitura | Análises de visitantes e tráfego: visão geral, tendências, páginas mais visitadas, geografia e referências |
| Catálogo | **Produtos** | Sim | Produtos, variantes, imagens, ajustes de estoque e atribuição de atributos |
| Catálogo | **Categorias** | Sim | Categorias de produtos, incluindo imagens e banners |
| Catálogo | **Marcas** | Sim | Marcas de produtos |
| Catálogo | **Atributos** | Sim | Definições de atributos de produtos |
| Catálogo | **Estoque** | Sim | Dashboards de estoque, velocidade de estoque, movimentos, sugestões de reposição e configurações de estoque |
| Pedidos | **Pedidos** | Sim | Pedidos, notas de pedido, atualizações de status/acompanhamento, cancelamentos, reembolsos e documentos de pedido |
| Clientes | **Mensagens de Cliente** | Sim | Mensagens de clientes de formulários de contato e notas de pedido, incluindo atualizações de status e respostas |
| Loja e Configurações | **Configurações da Loja** | Sim | Configurações da loja, idiomas disponíveis e branding (nome, cores, logotipo) |
| Usuários e Acesso | **Funcionários e Papéis** | Sim | Contas de funcionários, convites, papéis e catálogo de permissões |

Os dois escopos de **Análise** são sempre somente leitura — os dados de relatório não têm um conceito de "escrita", então o seletor oferece apenas **Nenhum acesso** ou **Leitura** para eles.

[![O seletor de escopo da API, com uma nota de acesso acima dos grupos de escopo Analytics e Catalog](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

Abaixo do seletor de escopo, uma visão geral de **"Este token pode acessar:"** somente leitura lista cada escopo que você concedeu e seu nível, para que você possa verificar rapidamente o acesso do token sem decodificar o seletor.

[![A visão geral de "Este token pode acessar" listando cada escopo concedido e seu nível de Leitura ou Leitura & Escrita](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)]

### Quais permissões um token realmente usa

Os escopos de um token descrevem o *teto* do que ele pode fazer — mas o token também herda as permissões reais do membro da equipe que o criou:

- O token nunca pode agir com poderes de **superusuário**, mesmo que o membro da equipe que o criou seja um superusuário.
- **Leitura & Escrita** em um escopo só funciona se o papel do membro da equipe que o criou também permitir acesso de escrita a essa área. Se seu papel for apenas visualização, por exemplo, para Produtos, um token que ele criar com "Produtos: Leitura & Escrita" ainda só poderá ler — o papel atua como uma segunda porta acima do escopo.
- Se o membro da equipe que criou um token for excluído ou sua conta for desativada, o token perde imediatamente o acesso à API, independentemente de seus escopos — não há mais um usuário permitido para ele agir.

Isso significa que a maneira mais segura de limitar os escopos de um token é criá-lo enquanto estiver logado como um membro da equipe cujo próprio papel já corresponda ao acesso que você deseja que o token tenha.

## Criando um token de API

1. Navegue até **Configurações > Tokens de API**
2. Clique em **+ Adicionar Token de API**
3. Insira um **Nome** que descreva claramente para o que o token é usado (ex: `Zapier Sincronização de Produtos` ou `API do Sistema de Ajuda`)
4. Selecione o tipo de **Token apropriado**
5. Adicione opcionalmente uma **Descrição** com mais detalhes sobre a integração
6. Em **Escopos de API**, escolha **Nenhum acesso**, **Leitura** ou **Leitura & Escrita** para cada área que a integração necessita — deixe todos os outros escopos em **Nenhum acesso**
7. Configure o status **Ativo**, a **Data de Expiração** e os **IPs Permitidos** conforme necessário (veja abaixo)
8. Clique em **Salvar**

Após salvar, o valor completo do token é exibido na página de detalhes. **Copie-o imediatamente** — o token é mascarado na visão de lista por segurança e não pode ser recuperado novamente após você sair dessa página.

[![Detalhes do Token de API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)]

## Segurança do valor do token

O Spwig exibe o valor completo do token apenas uma vez: imediatamente após você salvar um novo token. Após isso, a visão de lista mostra apenas uma versão mascarada (ex: `spw_••••••••••••••••••••3f8a`).

Se você perder o valor de um token, não será possível recupera-lo. Você precisará excluir o token antigo e criar um novo, depois atualizar a integração que estava usando-o.

**Nunca compartilhe valores de token por e-mail, mensagens de chat ou código-fonte.** Trate-os como senhas.

## Definindo uma data de expiração

O campo **Expira em** define uma data e hora após as quais o token deixará de funcionar automaticamente. Deixe-o em branco para tokens que não devem expirar.

Datas de expiração são úteis para:

- Integrações temporárias com data de término fixa
- Tokens fornecidos a terceiros onde você deseja a remoção automática do acesso
- Adicionar uma camada extra de segurança a integrações de alto privilégio

Quando um token expira, as solicitações que o usarem serão rejeitadas. Você pode estender o acesso atualizando a data **Expira em** ou criando um token de substituição.

## Restringindo a endereços IP específicos

O campo **IPs Permitidos** aceita uma lista de endereços IP. Quando a lista não estiver vazia, o token só funcionará quando a solicitação vier de um desses endereços.

Por exemplo, se sua ferramenta de análise rodar em um servidor em `203.0.113.42`, adicionar esse IP significa que o token não pode ser mal utilizado de qualquer outro local, mesmo que ele seja vazado.

Deixe **IPs Permitidos** vazio para permitir solicitações de qualquer endereço IP.

**A expiração e as restrições de IP são verificadas independentemente das permissões.** Um token expirado ou fora da lista de IPs permitidos é rejeitado antes que suas permissões sequer sejam consideradas, e um token com permissões generosas ainda é rejeitado no momento em que expira ou é chamado de um IP não listado.

## Chamando a API com um token

Integrações autenticam-se na API de administração do Spwig enviando o token em um cabeçalho `Authorization`:

```
Authorization: Bearer <seu-valor-de-token>
```

Todos os endpoints da API de administração estão localizados em `/api/admin/...`. O desenvolvedor que está construindo sua integração decide quais endpoints chamar — sua tarefa como comerciante é garantir que o token tenha **Permissões da API** que cubram esses endpoints. Se uma solicitação for rejeitada com um erro de permissão, a primeira coisa a verificar é se o token foi concedido a permissão correta no nível de acesso correto.

### Exemplo: lendo análise de tráfego da web

O Spwig expõe um endpoint `GET /api/admin/analytics/traffic/` que retorna análise de visitantes e tráfego para sua loja — uma visão geral de visitas e visitantes únicos, tendências ao longo do tempo, páginas mais acessadas, geografia dos visitantes e fontes de referência. Para permitir que uma ferramenta de relatórios ou painel de controle leia esses dados:

1. Crie um token (ou edite um existente) para essa integração
2. Em **Permissões da API**, defina **Análise de Web** para **Leitura**
3. Salve o token e forneça-o à integração

Como **Análise de Web** é uma permissão somente leitura, não há opção de "Leitura e Escrita" para escolher — a integração pode apenas recuperar dados de análise, nunca alterar a configuração da sua loja.

## Monitorando o uso do token

A lista de tokens mostra:

- **Contagem de Uso** — número total de vezes que o token foi usado
- **Último Uso** — quando o token foi usado pela última vez para fazer uma solicitação

Esses campos ajudam você a identificar tokens não utilizados (candidatos para revogação) e detectar atividade inesperada. Um aumento súbito na contagem de uso pode indicar que o token está sendo usado por alguém diferente da integração pretendida.

## Revogando um token

Para parar imediatamente um token de funcionar sem excluí-lo:

1. Clique no nome do token
2. Desmarque **Ativo**
3. Salve

O token permanece em sua lista para referência, mas é rejeitado em qualquer solicitação subsequente. Isso é útil quando você precisa suspender temporariamente uma integração enquanto investiga um problema.

Para remover permanentemente um token:

1. Selecione sua caixa de seleção na lista
2. Escolha **Excluir os tokens de API selecionados** no menu de ações
3. Confirme a exclusão

Uma vez excluído, um token não pode ser recuperado. Se a integração ainda precisar de acesso, crie um novo token e atualize a configuração da integração.

## Exemplo: configurando uma integração Zapier

**Cenário:** Você deseja conectar sua loja ao Zapier para automatizar notificações de pedidos.

| Campo | Valor |
|-------|-------|
| Nome | `Zapier Order Automation` |
| Tipo de Token | Integração Externa |
| Descrição | Usado pelo Zapier para ler novos pedidos e disparar notificações |
| Permissões da API | **Pedidos**: Leitura e Escrita |
| Ativo | Sim |
| Expira em | *(deixe em branco)* |
| IPs Permitidos | *(deixe em branco — o Zapier usa IPs dinâmicos)* |

Apenas a permissão **Pedidos** é concedida, então mesmo que esse token fosse exposto, ele não poderia acessar produtos, mensagens de clientes, contas de funcionários ou qualquer outra parte da sua loja. Após salvar, copie o valor completo do token e cole nas configurações da integração do Spwig no Zapier.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- Dê a cada token um nome claro e específico — `Shopify Sync v2` é muito mais útil do que `Token 3` quando você estiver solucionando problemas meses depois
- Crie um token por integração — se uma integração for comprometida, você pode revogar apenas esse token sem atrapalhar as outras
- **Conceda apenas os escopos que a integração realmente precisa** — uma ferramenta de relatórios precisa apenas de acesso de Leitura a Analytics de Vendas ou Web Analytics, e não de Leitura e Escrita em Produtos ou Funcionários & Papéis
- Verifique a **"Este token pode acessar:"** no formulário de alteração antes de entregar um token a uma terceira parte — é a forma mais rápida de confirmar que você não concedeu mais do que o planejado
- Lembre-se de que o acesso de escrita também depende do próprio papel do membro da equipe que criou o token — se um escopo mostra Leitura & Escrita, mas as escritas ainda estão falhando, verifique também as permissões do papel desse usuário
- Defina uma data de expiração para tokens usados em projetos únicos ou integrações temporárias — isso reduz o risco de tokens esquecidos permanecerem ativos indefinidamente
- Revise sua lista de tokens a cada alguns meses e desative qualquer token com uma data **Último Uso** que seja inesperadamente antiga, pois esses podem pertencer a integrações que não estão mais em execução
- Se você suspeitar que um token foi exposto, desative-o imediatamente, crie um substituto e atualize a integração afetada antes de reativar o acesso