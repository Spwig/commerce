---
title: 'Configuração de SSO: Okta'
---

Este guia orienta você na conexão do Spwig com o Okta para o single sign-on (SSO) de administradores. Uma vez configurado, seu pessoal poderá fazer login no painel de administração do Spwig usando sua conta Okta.

**Nota:** O Okta pode atualizar sua interface do console de administrador ao longo do tempo. Estas instruções foram escritas com base no console de administrador do Okta até o início de 2026. Se alguma etapa for diferente do que você vê, consulte a documentação oficial do Okta sobre [criar uma integração de aplicativo OIDC](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Pré-requisitos

- Uma organização Okta (qualquer nível — contas gratuitas para desenvolvedores funcionam para testes)
- Papel de **Super Administrador** ou **Administrador de Aplicativo** no Okta
- Seu URL do armazém Spwig (ex.: `https://your-store.com`)
- Os membros da equipe devem ter endereços de e-mail no Spwig que correspondam a suas contas Okta

## Etapa 1: Criar um Aplicativo

1. Faça login no [Console de Administração do Okta](https://your-org-admin.okta.com)
2. Navegue até **Aplicativos > Aplicativos**
3. Clique em **Criar Integração de Aplicativo**
4. Selecione:

| Campo | Valor |
|-------|-------|
| **Método de login** | OIDC - OpenID Connect |
| **Tipo de aplicativo** | Aplicativo Web |

5. Clique em **Próximo**

## Etapa 2: Configurar o Aplicativo

Preencha as configurações do aplicativo:

| Campo | Valor |
|-------|-------|
| **Nome da integração do aplicativo** | `Spwig Admin SSO` (ou qualquer nome que você preferir) |
| **Tipo de concessão** | Código de Autorização (deve estar selecionado por padrão) |
| **URIs de redirecionamento de login** | `https://your-store.com/oidc/callback/` |
| **URIs de redirecionamento de logout** | `https://your-store.com/en/admin/login/` |
| **Acesso controlado** | Escolha com base em suas necessidades (veja abaixo) |

Para **Acesso controlado**, escolha uma das opções:

- **Permitir que todos na sua organização acessem** — todos os usuários Okta podem fazer login (você ainda pode controlar o acesso ao Spwig com a configuração Restringir a Pessoal)
- **Limitar o acesso a grupos selecionados** — apenas usuários em grupos específicos do Okta podem fazer login
- **Pular a atribuição de grupo por enquanto** — você atribuirá usuários ou grupos manualmente mais tarde

Clique em **Salvar**.

**Importante:** O URI de redirecionamento de login deve corresponder exatamente a `https://your-store.com/oidc/callback/` — incluindo a barra no final.

## Etapa 3: Obter as Credenciais do Cliente

Após salvar, a guia **Geral** do aplicativo mostra suas credenciais:

| Valor | Onde Encontrar |
|-------|-----------------|
| **ID do Cliente** | Guia Geral, seção Credenciais do Cliente |
| **Segredo do Cliente** | Guia Geral, seção Credenciais do Cliente (clique no ícone de olho para revelar) |

Copie ambos os valores — você precisará deles para o Spwig.

## Etapa 4: Construir a URL de Descoberta

A URL de Descoberta depende de sua organização Okta e servidor de autorização:

**Servidor de autorização padrão (mais comum):**

Clique em **Adicionar Atribuição**
5.

Configure a atribuição:

| Campo | Valor |
|-------|-------|
| **Nome** | `groups` |
| **Incluir no tipo de token** | ID Token, Always |
| **Tipo de valor** | Groups |
| **Filtro** | Correspondência com regex: `.*` (para incluir todas as grupos) |
| **Incluir em** | Qualquer escopo (ou `openid` se quiser limitar) |

6. Clique em **Criar**

**Dica:** Ao contrário do Microsoft Entra ID, que envia Object IDs, o Okta envia **nomes de grupo** por padrão. Isso torna o mapeamento de roles mais intuitivo — você pode usar diretamente os nomes exibidos dos grupos do Okta nos campos Grupos de Funcionários e Grupos de Superusuários do Spwig.

### Filtro de Grupos

Se seus usuários pertencem a muitos grupos do Okta e você deseja incluir apenas alguns específicos no token:

- Altere o filtro de `.*` para uma regex mais específica, por exemplo, `^Spwig.*` para incluir apenas grupos que começam com "Spwig"
- Ou use os filtros **Começa com**, **Igual a** ou **Contém** em vez de regex

## Etapa 7: Configurar no Spwig

1. No administrador do Spwig, navegue até **Enterprise SSO > Configuração do Provedor de SSO**
2. Defina **Nome do Provedor** como `Okta`
3. Insira a URL de Descoberta do passo 4
4. Clique em **Descobrir Automaticamente** — isso preenche automaticamente todos os campos de endpoint
5. Insira o **ID do Cliente** do passo 3
6. Insira o **Segredo do Cliente** do passo 3
7. Se configurou atribuições de grupo no passo 6:
   - Defina **Atribuição de Grupo** como `groups`
   - Em **Grupos de Funcionários**, insira os nomes dos grupos do Okta cujos membros devem ser funcionários (separados por vírgula)
   - Em **Grupos de Superusuários**, insira os nomes dos grupos do Okta cujos membros devem ser superusuários (separados por vírgula)
8. Clique em **Salvar**

## Etapa 8: Habilitar e Testar

1. Navegue até **Configurações do Site > Guia de Segurança**
2. Marque **Habilitar SSO para login de administrador**
3. Clique em **Salvar**
4. Abra a página de login do administrador em uma **janela privada/incógnita**
5. Você deve ver um botão **Entrar com Okta**
6. Clique nele — você deve ser redirecionado para a página de login do Okta
7. Faça login com uma conta do Okta que esteja atribuída ao aplicativo e cujo e-mail corresponda a um usuário de funcionário no Spwig
8. Você deve ser redirecionado de volta ao painel de administração do Spwig

## Problemas Comuns

| Problema | Causa | Solução |
|---------|-------|----------|
| **A URI de redirecionamento não é permitida** | A URI de redirecionamento não corresponde à configuração do aplicativo | Verifique se a URI de redirecionamento de login está exatamente `https://your-store.com/oidc/callback/` com a barra no final |
| **O usuário não está atribuído ao cliente do aplicativo** | O usuário não está atribuído ao aplicativo do Okta | Atribua o usuário ou seu grupo ao aplicativo na guia Atribuições |
| **Login bem-sucedido no Okta, mas falha no Spwig** | Não há usuário correspondente no Spwig | Certifique-se de que uma conta de funcionário existe no Spwig com o mesmo e-mail. Verifique a configuração Restringir a Funcionários. |
| **Atribuição de grupo está vazia** | A atribuição de grupo não está configurada no servidor de autorização | Siga o passo 6 para adicionar uma atribuição de grupo. Certifique-se de que está adicionando-a ao servidor de autorização correto. |
| **Servidor de autorização incorreto** | A URL de descoberta usa um servidor de autorização diferente do onde a atribuição de grupo foi configurada | Verifique se a URL de descoberta corresponde ao servidor de autorização onde você configurou a atribuição de grupo |
| **"O client_id fornecido é inválido"** | O ID do cliente não corresponde ou o aplicativo está inativo | Verifique se o ID do cliente está correto e se o status do aplicativo é Ativo no Okta |

## Dicas

- **O Okta envia nomes de grupo, não IDs** — isso torna o mapeamento de roles direto.

Insira o nome exato do grupo exibido (por exemplo, `Spwig Admins`) nos campos Grupos de Funcionários ou Grupos de Superusuários do Spwig.
- **Use atribuição de grupo para controle de acesso** — atribua grupos específicos do Okta ao aplicativo do Spwig em vez de permitir que todos os usuários acessem.

# Configurações de Autenticação

Dessa forma, apenas o pessoal pretendido pode fazer login.
- **Os segredos do cliente Okta não expiram por padrão** — mas você pode rotacioná-los a qualquer momento na guia Geral do aplicativo para seguir as melhores práticas de segurança.
- **Teste com uma conta não administradora** — use um usuário comum do Okta (não um superadministrador) atribuído ao aplicativo para verificar se o SSO funciona conforme o esperado.
- **MFA no Okta** — configure a política de sessão global do Okta ou as políticas de autenticação para exigir MFA.

Isso se aplicará a todos os logins SSO no Spwig, sem a necessidade de configurar MFA separadamente no Spwig.