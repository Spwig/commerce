---
title: 'Configuração de SSO: Microsoft Entra ID'
---

Este guia orienta você na conexão do Spwig com o Microsoft Entra ID (anteriormente Azure Active Directory) para o single sign-on dos administradores. Uma vez configurado, seu pessoal poderá fazer login no painel de administração do Spwig usando sua conta de trabalho Microsoft.

**Nota:** A Microsoft pode atualizar a interface do centro de administração do Entra ao longo do tempo. Estas instruções foram escritas com base na interface como estava no início de 2026. Se alguma etapa for diferente do que você vê, consulte a documentação oficial da Microsoft sobre [registro de uma aplicação com a plataforma de identidade Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Pré-requisitos

- Uma assinatura Azure com acesso ao Microsoft Entra ID
- Perfil de **Administrador de Aplicativos** ou **Administrador Global** em seu inquilino do Entra ID
- Seu URL do armazém Spwig (ex.: `https://your-store.com`)
- Os membros da equipe devem ter endereços de e-mail no Spwig que correspondam a suas contas Microsoft

## Etapa 1: Registrar uma Aplicação

1. Faça login no [centro de administração do Microsoft Entra](https://entra.microsoft.com)
2. Navegue até **Identidade > Aplicações > Registros de aplicação**
3. Clique em **Novo registro**
4. Configure o registro:

| Campo | Valor |
|-------|-------|
| **Nome** | `Spwig Admin SSO` (ou qualquer nome que você preferir) |
| **Tipos de conta suportados** | **Contas nesse diretório organizacional apenas** (Single tenant) |
| **URI de redirecionamento** | Plataforma: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Clique em **Registrar**

**Importante:** O URI de redirecionamento deve corresponder exatamente a `https://your-store.com/oidc/callback/` — incluindo a barra no final. Substitua `your-store.com` pelo domínio real do seu armazém.

## Etapa 2: Anote os IDs da Aplicação

Após o registro, você verá a página **Visão Geral** da aplicação. Anote esses dois valores — você precisará deles mais tarde:

| Valor | Onde Encontrar | Para O quê É Usado |
|-------|-----------------|---------------|
| **Application (client) ID** | Página de visão geral, seção superior | Insira como **Client ID** no Spwig |
| **Directory (tenant) ID** | Página de visão geral, seção superior | Usado para construir o URL de Descoberta |

## Etapa 3: Criar um Segredo do Cliente

1. No registro da aplicação, navegue até **Certificados & segredos**
2. Clique em **Novo segredo do cliente**
3. Insira uma descrição (ex.: `Spwig SSO`) e escolha um período de expiração
4. Clique em **Adicionar**
5. **Copie o Valor imediatamente** — ele é exibido apenas uma vez. Este é o segredo do cliente que você inserirá no Spwig.

**Não copie o ID do Segredo** — você precisa da **coluna Valor**, não da coluna ID.

**Defina um lembrete** para rotacionar o segredo antes de expirar. Quando um segredo expirar, o SSO deixará de funcionar até que você crie um novo e atualize-o no Spwig.

## Etapa 4: Configurar Permissões da API

1. Navegue até **Permissões da API**
2. Verifique se **Microsoft Graph > User.Read** (delegado) está listado. Isso é adicionado por padrão.
3. Se as permissões `openid`, `email` e `profile` não estiverem listadas, clique em **Adicionar uma permissão > Microsoft Graph > Permissões delegadas** e adicione-as.
4. Clique em **Conceder consentimento de administrador para [sua organização]** se solicitado.

## Etapa 5: Construir o URL de Descoberta

O URL de Descoberta OIDC segue este formato:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Substitua `{tenant-id}` pelo **Directory (tenant) ID** da Etapa 2.

Exemplo: se seu ID do inquilino for `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, o URL de Descoberta será:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Etapa 6: Configurar Atributos de Grupo (Opcional)

Se você quiser que o Spwig atribua automaticamente o status de funcionário ou superusuário com base na associação a grupos do Entra ID:

1. No registro da aplicação, navegue até **Configuração de token**
2. Clique em **Adicionar reivindicação de grupo**
3. Selecione os tipos de grupo a incluir (normalmente **Grupos de segurança**)
4. Em **Personalizar propriedades do token por tipo**, para o token **ID**, selecione **ID do grupo**
5. Clique em **Adicionar**

**Importante:** O Entra ID envia **Object IDs** (UUIDs como `a1b2c3d4-...`), e não os nomes exibidos dos grupos.

Ao configurar o mapeamento de papéis no Spwig, você deve usar esses Object IDs.

Para encontrar o Object ID de um grupo:
1. No centro de administração do Entra, vá para **Identity > Groups > All groups**
2. Clique no grupo
3. Copie o **Object ID** da página de visão geral do grupo

### Limite de Grupo

O Microsoft Entra ID inclui no máximo **200 grupos** no token. Se um usuário pertencer a mais de 200 grupos, a reivindicação de grupo será substituída por um link para a API Microsoft Graph. Para organizações com muitos grupos, considere criar um grupo de segurança dedicado para o acesso ao Spwig e usar [filtragem de grupo](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) para limitar quais grupos são incluídos.

## Etapa 7: Configure no Spwig

1. No admin do Spwig, navegue até **Enterprise SSO > SSO Provider Configuration**
2. Defina **Provider Name** como `Microsoft Entra ID`
3. Cole a URL de Descoberta do Discovery da Etapa 5 em **OIDC Discovery URL**
4. Clique em **Auto-Discover** — isso preenche automaticamente todos os campos de endpoint
5. Insira o **Client ID** da Etapa 2
6. Insira o **Client Secret** (o Valor) da Etapa 3
7. Se você configurou reivindicações de grupo na Etapa 6:
   - Defina **Groups Claim** como `groups`
   - Em **Staff Groups**, insira os Object IDs dos grupos cujos membros devem ser funcionários (separados por vírgula)
   - Em **Superuser Groups**, insira os Object IDs dos grupos cujos membros devem ser superusuários (separados por vírgula)
8. Clique em **Save**

## Etapa 8: Ativar e Testar

1. Navegue até **Site Settings > Security** tab
2. Marque **Enable SSO for admin login**
3. Clique em **Save**
4. Abra a página de login do admin em uma **janela privada/incógnita**
5. Você deve ver um botão **Sign in with Microsoft Entra ID**
6. Clique nele — você deve ser redirecionado para a página de login do Microsoft
7. Faça login com uma conta Microsoft cujo e-mail corresponda a um usuário de staff no Spwig
8. Você deve ser redirecionado de volta ao painel de administração do Spwig

## Problemas Comuns

| Problema | Causa | Solução |
|---------|-------|----------|
| **AADSTS50011: O URI de redirecionamento não corresponde** | O URI de redirecionamento no Entra não corresponde exatamente | Verifique se o URI de redirecionamento é `https://your-store.com/oidc/callback/` com a barra no final. Verifique se há uma discrepancia entre HTTP e HTTPS. |
| **AADSTS700016: Aplicativo não encontrado** | Client ID incorreto ou inquilino | Verifique novamente o Client ID e certifique-se de que a URL de Descoberta use o ID do inquilino correto |
| **Login bem-sucedido no Microsoft, mas falha no Spwig** | Não há usuário correspondente no Spwig | Certifique-se de que uma conta de staff existe no Spwig com o mesmo endereço de e-mail da conta Microsoft. Verifique se o usuário tem status de staff se a opção "Restrict to Staff" estiver ativada. |
| **A reivindicação de grupo está vazia** | As reivindicações de grupo não estão configuradas | Siga a Etapa 6 para adicionar uma reivindicação de grupo na configuração do token |
| **A reivindicação de grupo retorna uma URL em vez de IDs** | O usuário está em mais de 200 grupos | Use a filtragem de grupo para limitar os grupos no token, ou atribua grupos específicos |
| **O SSO para de funcionar após alguns meses** | O segredo do cliente expirou | Crie um novo segredo do cliente no Entra e atualize-o na configuração do provedor de SSO do Spwig |

## Dicas

- **Use grupos de segurança** para mapeamento de papéis, e não grupos Microsoft 365 ou listas de distribuição.

Os grupos de segurança são projetados para controle de acesso e funcionam com mais confiabilidade com reivindicações OIDC.
- **Um único inquilino é recomendado** — selecionar "Accounts in this organizational directory only" restringe o SSO aos usuários da sua organização.

Configurações multilocais exigem validação adicional.
- **Defina uma expiração longa para o segredo** — escolha 24 meses ao criar o segredo do cliente e defina um lembrete no calendário em 22 meses para rotacioná-lo.
- **Acesso condicional** — você pode criar políticas de acesso condicional no Entra ID que se aplicam especificamente ao registro da aplicação Spwig.

Por exemplo, exige MFA, bloqueie o login de localizações não confiáveis ou exija dispositivos compatíveis.
- **Teste com uma conta não administradora** — crie uma conta de staff de teste no Spwig para verificar se o SSO funciona antes de implantá-lo para toda a sua equipe.