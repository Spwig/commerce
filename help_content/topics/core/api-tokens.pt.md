---
title: Tokens da API
---

Tokens da API são chaves seguras que permitem que serviços externos e integrações comuniquem com sua loja. Quando um serviço de terceiros ou ferramenta precisa acessar os dados da sua loja ou acionar ações, ela envia um token da API com cada solicitação para que sua loja possa verificar se a solicitação está autorizada. Você cria e gerencia todos os tokens na seção Tokens da API do seu painel administrativo.

## Quando você precisa de um token da API

Você normalmente precisará criar um token da API quando:

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
| **Integração Externa** | Serviços de terceiros, ferramentas de automação (ex: Zapier) ou ferramentas de sincronização de dados |
| **Webhook** | Autenticação para receptores de webhook ou endpoints |
| **Personalizado** | Qualquer outro propósito que não se encaixe nas categorias acima |
| **Sincronização de Instância** | Sincronização entre instalações do Spwig ou serviços externos do Spwig |

## Criando um token da API

1. Navegue até **Configurações > Tokens da API**
2. Clique em **+ Adicionar Token da API**
3. Insira um **Nome** que descreva claramente para o que o token serve (ex: `Sincronização de Produtos do Zapier` ou `API do Sistema de Ajuda`)
4. Selecione o tipo de token apropriado
5. Adicione opcionalmente uma **Descrição** com mais detalhes sobre a integração
6. Configure o status **Ativo**, a **Data de Expiração** e os **IPs Permitidos** conforme necessário (veja abaixo)
7. Clique em **Salvar**

Após salvar, o valor completo do token é exibido na página de detalhes. **Copie-o imediatamente** — o token é mascarado na visualização da lista por segurança e não pode ser recuperado novamente após você sair dessa página.

![Detalhes do Token da API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Segurança do valor do token

O Spwig exibe o valor completo do token apenas uma vez: imediatamente após você salvar um novo token. Após isso, a visualização da lista mostra apenas uma versão mascarada (ex: `spw_••••••••••••••••••••3f8a`).

Se você perder o valor de um token, não será possível recupera-lo. Você precisará excluir o token antigo e criar um novo, depois atualizar a integração que estava usando-o.

**Nunca compartilhe valores de token por e-mail, mensagens de chat ou código-fonte.** Trate-os como senhas.

## Definindo uma data de expiração

O campo **Expira em** define uma data e hora após as quais o token deixará de funcionar automaticamente. Deixe-o em branco para tokens que não devem expirar.

Datas de expiração são úteis para:

- Integrações temporárias com data de término fixa
- Tokens fornecidos a terceiros onde você deseja a remoção automática do acesso
- Adicionar uma camada extra de segurança a integrações com privilégios elevados

Quando um token expira, as solicitações que o usam são rejeitadas. Você pode estender o acesso atualizando a data **Expira em** ou criando um token de substituição.

## Restringindo a endereços IP específicos

O campo **IPs Permitidos** aceita uma lista de endereços IP. Quando a lista não estiver vazia, o token só funcionará quando a solicitação vier de um desses endereços.

Por exemplo, se sua ferramenta de análise rodar em um servidor no endereço `203.0.113.42`, adicionar esse IP significa que o token não poderá ser mal utilizado de nenhum outro local, mesmo que ele seja vazado.

Deixe **IPs Permitidos** vazio para permitir solicitações de qualquer endereço IP.

## Monitorando o uso do token

A lista de tokens mostra:

- **Contagem de Uso** — número total de vezes que o token foi usado
- **Último Uso** — quando o token foi usado pela última vez para fazer uma solicitação

Esses campos ajudam você a identificar tokens não utilizados (candidatos à revogação) e detectar atividades inesperadas.

Um aumento súbito na contagem de uso pode indicar que um token está sendo usado por alguém diferente da integração pretendida.

## Revogando um token

Para parar imediatamente um token de funcionar sem excluí-lo:

1. Clique no nome do token
2. Desmarque **Ativo**
3. Salve

O token permanece em sua lista para referência, mas é rejeitado em qualquer solicitação subsequente. Isso é útil quando você precisa suspender temporariamente uma integração enquanto investiga um problema.

Para remover permanentemente um token:

1. Selecione seu checkbox na lista
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
| Ativo | Sim |
| Expira em | *(deixe em branco)* |
| IPs Permitidos | *(deixe em branco — o Zapier usa IPs dinâmicos)* |

Após salvar, copie o valor completo do token e cole nas configurações da integração Spwig do Zapier.

## Dicas

- Dê a cada token um nome claro e específico — `Shopify Sync v2` é muito mais útil do que `Token 3` quando você estiver investigando um problema meses depois
- Crie um token por integração — se uma integração for comprometida, você pode revogar apenas esse token sem afetar os outros
- Defina uma data de expiração para tokens usados em projetos únicos ou integrações temporárias — isso reduz o risco de tokens esquecidos permanecerem ativos indefinidamente
- Revise sua lista de tokens a cada alguns meses e desative quaisquer tokens com uma data de **Último Uso** que seja inesperadamente antiga, pois esses podem pertencer a integrações que não estão mais em execução
- Se você suspeitar que um token foi exposto, desative-o imediatamente, crie um substituto e atualize a integração afetada antes de reativar o acesso