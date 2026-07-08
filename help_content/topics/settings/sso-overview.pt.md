---
title: Admin Single Sign-On (SSO)
---

Single Sign-On (SSO) permite que sua equipe faça login no painel de administração usando seu provedor de identidade organizacional em vez de um nome de usuário e senha separados. O Spwig suporta qualquer provedor de identidade que use o protocolo OpenID Connect (OIDC), incluindo Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak e outros.

## O que é SSO Empresarial?

O SSO Empresarial é diferente do login social (fazer login com uma conta pessoal do Google ou Facebook). Com o SSO Empresarial:

- A equipe autentica-se por meio do **provedor de identidade da sua organização** — o mesmo sistema que usam para e-mail, ferramentas internas e outros aplicativos empresariais
- Sua equipe de TI controla o acesso centralmente — quando alguém deixa a organização, desativar sua conta no provedor de identidade revoga imediatamente seu acesso ao Spwig
- A autenticação multifator (MFA) é imposta pelo provedor de identidade, fornecendo uma política de segurança consistente em todos os aplicativos
- A equipe não precisa lembrar uma senha separada para o Spwig

## Como Funciona

Quando o SSO está habilitado, a página de login do administrador mostra um botão **Entrar com [Fornecedor]**. O fluxo de autenticação funciona assim:

1. O membro da equipe clica no botão SSO na página de login do Spwig
2. Eles são redirecionados para a página de login do seu provedor de identidade (ex: login do Microsoft)
3. Eles autenticam-se com o provedor de identidade (incluindo qualquer MFA exigido pelo provedor)
4. O provedor de identidade os redireciona de volta ao Spwig com um código de autorização seguro
5. O Spwig troca o código pelas informações do usuário e cria uma sessão
6. O membro da equipe chega ao painel de administração, totalmente autenticado

Isso usa o protocolo **OpenID Connect (OIDC)** padrão da indústria, que é suportado por praticamente todos os provedores de identidade empresarial.

## Habilitando SSO

O SSO é configurado em dois lugares:

1. **Configurações do Site > aba Segurança** — habilite ou desabilite o SSO e controle a visibilidade do login por senha
2. **Configuração do Provedor SSO** — insira os detalhes OIDC do seu provedor de identidade

### Etapa 1: Configure seu provedor de identidade

Antes de habilitar o SSO no Spwig, você precisa registrar o Spwig como um aplicativo em seu provedor de identidade. Veja os guias específicos do provedor:

- **Microsoft Entra ID** — veja o guia de configuração do Microsoft Entra ID
- **Google Workspace** — veja o guia de configuração do Google Workspace
- **Okta** — veja o guia de configuração do Okta
- **Outros provedores** — qualquer provedor compatível com OIDC funciona. Registre um aplicativo web com URI de redirecionamento `https://your-store.com/oidc/callback/` e consulte a documentação do seu provedor para a URL de descoberta OIDC, ID do cliente e segredo do cliente.

### Etapa 2: Configure o Provedor SSO no Spwig

Navegue até a página **Configuração do Provedor SSO** (ligada da aba Segurança ou acessível em **SSO Empresarial > Configuração do Provedor SSO** no menu lateral do administrador). Insira:

1. **Nome do Provedor** — exibido no botão de login (ex: "Microsoft Entra ID")
2. **URL de Descoberta OIDC** — a URL `.well-known/openid-configuration` do seu provedor. Clique em **Descobrir Automaticamente** para preencher automaticamente os campos de endpoint.
3. **ID do Cliente** e **Segredo do Cliente** — do registro do aplicativo do seu provedor de identidade

O segredo do cliente é armazenado criptografado e nunca é exibido após o salvamento.

### Etapa 3: Habilite o SSO nas Configurações do Site

Navegue até **Configurações do Site > aba Segurança** e marque **Habilitar SSO para login de administrador**. O botão SSO aparecerá imediatamente na página de login do administrador.

## Configurações de SSO

| Configuração | Descrição |
|---------|-------------|
| **Habilitar SSO para login de administrador** | Exibe o botão SSO na página de login do administrador. Não afeta o login por senha a menos que você também o desative. |
| **Permitir login por senha na página de administrador** | Quando desmarcado, o formulário de senha é oculto por trás de um botão de alternância. A equipe vê apenas o botão SSO por padrão. O formulário de senha ainda pode ser acessado clicando em "Entrar com conta local" ou adicionando `?password=1` ao URL de login. |

### Comportamento da Página de Login

| SSO Habilitado | Login por Senha | Resultado |
|-------------|---------------|--------|
| Off | On | Página de login padrão com formulário de nome de usuário/senha apenas |
| On | On | Botão SSO no topo, divisor "ou", depois formulário de senha abaixo |
| On | Off | Botão SSO apenas. O formulário de senha está atrás de um interruptor "Entrar com conta local" |
| Off | Off | Não é possível — o login por senha é automaticamente reativado se o SSO estiver desativado ou não configurado |

## Correspondência de Usuários

Quando um membro da equipe entra via SSO, o Spwig o associa a uma conta de usuário existente por **endereço de e-mail** (insensível a maiúsculas e minúsculas). O e-mail das reivindicações do provedor de identidade deve corresponder ao e-mail da conta do membro da equipe no Spwig.

Se nenhuma conta de usuário correspondente for encontrada:

- **Criar usuários automaticamente desativado** (padrão) — o login é negado. Você deve criar a conta do membro da equipe no Spwig primeiro com um endereço de e-mail correspondente.
- **Criar usuários automaticamente ativado** — uma nova conta de usuário é criada automaticamente com o nome e e-mail das reivindicações do provedor de identidade.

A configuração **Restringir a Membros da Equipe** (ativada por padrão) adiciona uma verificação adicional: mesmo que uma conta de usuário exista, o login é negado a menos que o usuário tenha status de membro da equipe. Isso impede que contas não de membros da equipe acessem o painel de administração via SSO.

## Mapeamento de Papéis

Se seu provedor de identidade enviar informações de membros de grupo nas reivindicações OIDC, o Spwig pode definir automaticamente o status de membro da equipe e superusuário com base no grupo de membros.

Para configurar o mapeamento de papéis:

1. Na Configuração do Provedor de SSO, defina o campo **Reivindicação de Grupos** para o nome da reivindicação que seu provedor usa (padrão: `groups`)
2. Em **Grupos de Membros da Equipe**, insira nomes ou IDs de grupo separados por vírgula. Usuários em qualquer um desses grupos são concedidos status de membro da equipe.
3. Em **Grupos de Superusuários**, insira nomes ou IDs de grupo separados por vírgula. Usuários em qualquer um desses grupos são concedidos status de superusuário.

O mapeamento de papéis é avaliado sempre que um usuário entra via SSO. Se um usuário for removido de um grupo no provedor de identidade, seu status de membro da equipe ou superusuário será atualizado em seu próximo login via SSO.

**Importante:** O Microsoft Entra ID envia **IDs de Objeto de Grupo** (UUIDs) por padrão, não nomes de grupo. Copie o ID de Objeto do portal do Azure ao configurar o mapeamento de papéis. Outros provedores, como o Okta, geralmente enviam nomes de grupo.

## Mapeamento de Reivindicações

O Spwig lê informações do usuário de reivindicações OIDC padrão. Os valores padrão funcionam com a maioria dos provedores, mas você pode personalizar os nomes dos campos de reivindicação na Configuração do Provedor de SSO:

| Configuração | Padrão | Descrição |
|---------|---------|-------------|
| **Reivindicação de E-mail** | `email` | A reivindicação contendo o endereço de e-mail do usuário |
| **Reivindicação de Nome de Solteiro** | `given_name` | A reivindicação contendo o nome de solteiro do usuário |
| **Reivindicação de Sobrenome** | `family_name` | A reivindicação contendo o sobrenome do usuário |
| **Reivindicação de Grupos** | `groups` | A reivindicação contendo membros de grupo (deixe em branco para desativar o mapeamento de papéis) |

## Comportamento de Autenticação de Dois Fatores (MFA)

Quando um membro da equipe entra via SSO, a exigência de autenticação de dois fatores (2FA) integrada do Spwig é automaticamente ignorada. Isso ocorre porque o provedor de identidade é responsável por impor MFA como parte do fluxo de login SSO.

Se sua organização exigir MFA, configure-a nas políticas de acesso condicional do seu provedor de identidade, em vez nas configurações de 2FA do Spwig. Isso lhe dá uma gestão centralizada de MFA em todas as suas aplicações.

## Acesso de Recuperação

Se seu provedor de identidade enfrentar uma interrupção ou configuração incorreta, você ainda poderá acessar o formulário de login do administrador:

- **Clique no interruptor** — Se o login por senha estiver desativado, clique em "Entrar com conta local" na página de login para revelar o formulário de senha
- **Parâmetro URL** — Anexe `?password=1` à URL de login do administrador (ex: `https://your-store.com/en/admin/login/?password=1`) para mostrar diretamente o formulário de senha
- **Login por senha sempre disponível** — Mesmo quando oculto na interface, o backend de autenticação por senha permanece ativo. Apenas a visibilidade do formulário é afetada.

O Spwig também impede que você desative o login com senha a menos que o SSO esteja habilitado e configurado corretamente — você não pode se trancar acidentalmente fora do sistema.

## Fornecedores Suportados

O Spwig funciona com qualquer provedor de identidade que suporte o protocolo OpenID Connect (OIDC). Guias de configuração detalhados estão disponíveis para:

- **Microsoft Entra ID** (anteriormente Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Para outros provedores compatíveis com OIDC (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, etc.), as etapas de configuração do Spwig são as mesmas — você precisa da URL de Descoberta OIDC do provedor, do ID do cliente e do Segredo do Cliente. Consulte a documentação do seu provedor para saber como registrar uma aplicação web e obter essas credenciais. O URI de redirecionamento a ser usado é sempre `https://your-store.com/oidc/callback/`.

## Dicas

- **Comece com o login com senha habilitado** — Ative o SSO junto com o login com senha primeiro. Depois que você confirmar que o SSO funciona para sua equipe, poderá desativar opcionalmente o login com senha.
- **Teste em uma janela anônima** — Use uma janela do navegador privada/anônima para testar o SSO sem ser afetado por sua sessão atual de administrador.
- **Crie contas de funcionários primeiro** — A menos que você ative a opção Auto-Criar Usuários, os funcionários precisam de uma conta existente no Spwig com um endereço de e-mail correspondente antes de poderem fazer login via SSO.
- **Use o botão Auto-Descobrir** — Insira a URL de Descoberta OIDC do seu provedor e clique em Auto-Descobrir para preencher automaticamente todos os campos de endpoint. Isso é mais rápido e menos propenso a erros do que inserir os endpoints manualmente.
- **Mantenha uma conta de administrador local** — Sempre mantenha pelo menos uma conta de administrador local com senha como opção de recuperação em caso de problemas com o provedor de identidade.
- **Monitore a expiração do segredo do cliente** — Alguns provedores (notavelmente o Microsoft Entra ID) emitem segredos de cliente com datas de expiração. Configure um lembrete no calendário para rotacionar o segredo antes que expire.