---
title: 'Configuração de SSO: Google Workspace'
---

Este guia orienta você na conexão do Spwig ao Google Workspace para o login único de administradores. Uma vez configurado, seu pessoal poderá fazer login no painel de administração do Spwig usando sua conta do Google Workspace.

**Nota:** O Google pode atualizar a interface do Console Cloud ao longo do tempo. Estas instruções foram escritas com base na interface como estava no início de 2026. Se alguma etapa for diferente do que você vê, consulte a documentação oficial do Google sobre [configuração do OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Pré-requisitos

- Uma assinatura do Google Workspace (Google Workspace Business, Enterprise ou Education)
- Acesso de administrador ao [Google Cloud Console](https://console.cloud.google.com)
- O URL da sua loja Spwig (ex.: `https://your-store.com`)
- Os membros da equipe devem ter endereços de e-mail no Spwig que correspondam a suas contas do Google Workspace

## Etapa 1: Criar ou Selecionar um Projeto do Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Clique no seletor de projeto na barra superior
3. Clique em **Novo Projeto** (ou selecione um projeto existente se preferir)
4. Insira um nome para o projeto (ex.: `Spwig SSO`)
5. Selecione sua organização
6. Clique em **Criar**

## Etapa 2: Configurar a Tela de Consentimento do OAuth

1. No Console Cloud, navegue até **APIs & Services > OAuth consent screen**
2. Selecione **Internal** como o tipo de usuário — isso restringe o login a usuários dentro de sua organização do Google Workspace
3. Clique em **Create**
4. Preencha os campos necessários:

| Campo | Valor |
|-------|-------|
| **Nome do aplicativo** | `Spwig Admin` (ou o nome da sua loja) |
| **E-mail de suporte do usuário** | Seu endereço de e-mail de administrador |
| **Domínios autorizados** | `your-store.com` (o domínio da sua loja, sem `https://`) |
| **E-mail de contato do desenvolvedor** | Seu endereço de e-mail de administrador |

5. Clique em **Save and Continue**
6. Na página **Scopes**, clique em **Add or Remove Scopes** e adicione:
   - `openid`
   - `email`
   - `profile`
7. Clique em **Save and Continue**
8. Revise o resumo e clique em **Back to Dashboard**

## Etapa 3: Criar Credenciais OAuth

1. Navegue até **APIs & Services > Credentials**
2. Clique em **Create Credentials > OAuth client ID**
3. Configure o cliente:

| Campo | Valor |
|-------|-------|
| **Tipo de aplicativo** | Aplicativo Web |
| **Nome** | `Spwig SSO` |
| **URIs de redirecionamento autorizados** | `https://your-store.com/oidc/callback/` |

4. Clique em **Create**
5. Um diálogo mostra seu **Client ID** e **Client Secret** — copie ambos os valores. Você também pode baixá-los como JSON para armazenamento seguro.

**Importante:** A URI de redirecionamento deve corresponder exatamente a `https://your-store.com/oidc/callback/` — incluindo a barra final e o esquema `https://`. Substitua `your-store.com` pelo domínio real da sua loja.

## Etapa 4: Obter a URL de Descoberta

O Google usa uma única URL de Descoberta padrão para todos os inquilinos do Workspace:

```
https://accounts.google.com/.well-known/openid-configuration
```

Essa URL é a mesma para todas as organizações do Google Workspace — você não precisa personalizá-la com um inquilino ou domínio.

## Etapa 5: Configurar no Spwig

1. No painel de administração do Spwig, navegue até **Enterprise SSO > SSO Provider Configuration**
2. Defina **Provider Name** como `Google Workspace`
3. Insira a URL de Descoberta: `https://accounts.google.com/.well-known/openid-configuration`
4. Clique em **Auto-Discover** — isso preenche automaticamente todos os campos de endpoint
5. Insira o **Client ID** da Etapa 3
6. Insira o **Client Secret** da Etapa 3
7. Clique em **Save**

### Mapeamento de Atributos

O Google usa nomes padrão de reivindicações OIDC, então a configuração padrão do Spwig funciona prontamente:

| Configuração do Spwig | Reivindicação do Google | Valor Padrão |
|----------------------|------------------------|--------------|
| Atributo de E-mail | `email` | `email` |
| Atributo de Nome de Solteiro | `given_name` | `given_name` |
| Atributo de Sobrenome | `family_name` | `family_name` |

Nenhuma alteração no mapeamento de reivindicações é necessária.

## Etapa 6: Habilitar e Testar

1.

Navegue até **Site Settings > Security** tab
2.

Marque **Enable SSO for admin login**
3.

Clique em **Save**
4.

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

Abra a página de login do administrador em uma **janela privada/incógnita**
5.

Você deve ver um botão **Entrar com Google Workspace**
6.

Clique nele — você deve ser redirecionado para a página de login do Google
7.

Faça login com uma conta do Google Workspace cujo e-mail corresponda a um usuário da equipe no Spwig
8.

Você deve ser redirecionado de volta ao painel de administração do Spwig

## Mapeamento de Papel com Base em Grupo

Diferente do Microsoft Entra ID ou Okta, o Google não inclui a associação a grupos nos tokens OIDC padrão por padrão. Implementar reivindicações de grupo com o Google requer a API de Diretório do Google Workspace e configurações adicionais além do OIDC básico.

Para a maioria das implantações do Google Workspace, recomendamos gerenciar o status de membros da equipe e superusuários diretamente no Spwig, em vez de mapear automaticamente os papéis:

1. Crie contas de equipe no Spwig com as permissões apropriadas
2. Use o sistema de papéis de equipe do Spwig para controlar os níveis de acesso
3. Os membros da equipe fazem login via SSO, e o Spwig usa suas permissões existentes

Se você precisar de mapeamento automático de papéis com base em grupo, consulte a [documentação da API de Diretório do Admin SDK do Google Workspace](https://developers.google.com/admin-sdk/directory) para configurar reivindicações personalizadas.

## Problemas Comuns

| Problema | Causa | Solução |
|---------|-------|----------|
| **Erro 400: redirect_uri_mismatch** | O URI de redirecionamento no Google Cloud não corresponde exatamente | Verifique se o URI de redirecionamento é `https://your-store.com/oidc/callback/` com a barra no final. Verifique HTTP vs HTTPS. |
| **Erro 403: access_denied** | O usuário não está na organização do Google Workspace | Com o tipo de usuário "Interno", apenas usuários em sua organização podem fazer login. Verifique se a conta do usuário faz parte do domínio do Workspace. |
| **A tela de consentimento do OAuth mostra "Este app não está verificado"** | Normal para apps internos | Esse aviso é esperado para apps internos e não afeta a funcionalidade. Os usuários em sua organização ainda podem fazer login. |
| **Login bem-sucedido no Google, mas falha no Spwig** | Não há usuário correspondente no Spwig | Certifique-se de que uma conta de equipe existe no Spwig com o mesmo e-mail da conta do Google Workspace. Verifique se "Restringir a equipe" está configurado corretamente. |
| **"Acesso bloqueado: Esta solicitação do app é inválida"** | Escopos não configurados corretamente | Verifique se os escopos `openid`, `email` e `profile` foram adicionados à tela de consentimento do OAuth. |

## Dicas

- **Use o tipo de usuário "Interno"** — isso restringe o login à sua organização do Google Workspace e não requer o processo de verificação do app do Google.
- **Segredos do cliente do Google não expiram** — diferentemente do Microsoft Entra ID, os segredos do cliente do OAuth do Google não têm uma data de expiração. No entanto, você pode rotacioná-los a qualquer momento na página de Credenciais.
- **Um projeto para múltiplos apps** — você pode criar múltiplos IDs de cliente OAuth dentro do mesmo projeto do Google Cloud se tiver múltiplas instalações do Spwig.
- **Teste com uma conta não administradora** — crie uma conta de equipe de teste no Spwig e use um usuário regular do Google Workspace (não um superadministrador) para verificar se o SSO funciona conforme o esperado.