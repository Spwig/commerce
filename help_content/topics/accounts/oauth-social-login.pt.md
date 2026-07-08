---
title: Configuração de Autenticação OAuth e Social
---

OAuth e login social permitem que os clientes façam login na sua loja usando suas contas existentes do Google, Apple ou Microsoft — não é necessário criar e lembrar outro senha.

![Configurações de OAuth](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## O que é OAuth / Login Social?

OAuth é um padrão de autenticação seguro que permite que os clientes façam login usando credenciais de provedores confiáveis, como Google, Apple ou Microsoft.

### Benefícios

- **Checkout Mais Rápido** — Os clientes poupam o formulário de registro e fazem login com um clique
- **Redução de Fricção** — Nenhuma criação de senha, e-mails de verificação ou fluxos de senhas esquecidas
- **Melhor Conversão** — Estudos mostram que o login social pode aumentar as taxas de conversão em 20-40%
- **Segurança Aumentada** — As credenciais nunca passam pela sua loja; a autenticação é feita pelo provedor
- **Confiança do Cliente** — Os clientes confiam em provedores estabelecidos com suas credenciais de login

### Como Funciona

1. O cliente clica em "Faça login com o Google" (ou Apple/Microsoft) na página de login da sua loja
2. Eles são redirecionados para a página de login segura do provedor
3. O cliente autentica com suas credenciais do provedor
4. O provedor envia de volta informações de identidade verificadas para sua loja
5. O cliente é autenticado automaticamente

Na primeira login, uma nova conta do cliente é criada automaticamente usando seu e-mail e informações do perfil do provedor.

## Provedores Suportados

O Spwig suporta três principais provedores OAuth:

| Provedor | Caso de Uso | Requisitos de Credenciais |
|----------|----------|------------------------|
| **Google** | Mais popular, mais fácil de configurar | ID do Cliente, Segredo do Cliente |
| **Apple** | Necessário para apps iOS, foco em privacidade | ID do Cliente, ID da Equipe, ID da Chave, Chave Privada |
| **Microsoft** | Clientes corporativos, usuários do Office 365 | ID do Cliente, Segredo do Cliente, ID do Inquilino |

Você pode habilitar um, dois ou todos os três provedores. Cada um opera de forma independente.

## Configuração do OAuth do Google

O OAuth do Google é a opção mais popular e a mais fácil de configurar.

### Pré-requisitos

- Uma conta do Google
- Acesso ao Google Cloud Console

### Configuração Passo a Passo

1. **Navegue até as Configurações de OAuth**
   - Vá para **Configurações > Configurações da Loja** no seu painel de administração
   - Role até a seção **Provedores OAuth**
   - Clique em **Configurar Google**

2. **Crie um Projeto do Google Cloud**
   - Visite [Google Cloud Console](https://console.cloud.google.com/)
   - Clique em **Criar Projeto**
   - Insira um nome do projeto (ex: "Meu Store OAuth")
   - Clique em **Criar**

3. **Ative a API do Google+**
   - Na barra lateral esquerda, vá para **APIs & Services > Biblioteca**
   - Procure "API do Google+"
   - Clique em **Ativar**

4. **Crie Credenciais OAuth**
   - Vá para **APIs & Services > Credenciais**
   - Clique em **Criar Credenciais > ID do Cliente OAuth**
   - Selecione o tipo de aplicativo: **Aplicativo Web**
   - Insira um nome (ex: "Login da Loja")

5. **Configure a URI de Redirecionamento**
   - Sob **URIs de Redirecionamento Autorizados**, adicione:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Substitua `yourdomain.com` pelo seu domínio real
   - Clique em **Criar**

6. **Copie as Credenciais**
   - Copie o **ID do Cliente** e **Segredo do Cliente** da janela pop-up

7. **Insira as Credenciais no Spwig**
   - Volte para as configurações de OAuth do Spwig
   - Cole o ID do Cliente e o Segredo do Cliente
   - Clique em **Salvar**
   - Ative o **OAuth do Google** clicando no interruptor

### Teste

- Visite a página de login da sua loja
- Procure o botão "Faça login com o Google"
- Clique nele e autentique com sua conta do Google
- Você deve estar logado e redirecionado para o painel do cliente

## Configuração do OAuth da Apple

O OAuth da Apple é mais complexo que o Google devido ao seu sistema de autenticação baseado em chaves.

### Pré-requisitos

- Uma conta do desenvolvedor Apple (membro pago necessário)
- Acesso ao portal do desenvolvedor Apple

### Configuração Passo a Passo

1. **Navegue até as Configurações de OAuth**
   - Vá para **Configurações > Configurações da Loja > Provedores OAuth**
   - Clique em **Configurar Apple**

2. **Crie um ID de Serviço**
   - Faça login em [Apple Developer](https://developer.apple.com/account/)
   - Vá para **Certificados, Identificadores & Perfis**
   - Clique em **Identificadores** e depois no botão **+**
   - Selecione **IDs de Serviço** e clique em **Continuar**
   - Insira uma descrição (ex: "Login da Loja")
   - Insira um identificador (ex: `com.yourstore.login`)
   - Clique em **Continuar** e depois em **Registrar**

3. **Configure o ID de Serviço**
   - Clique no seu novo ID de Serviço criado
   - Marque **Faça login com a Apple**
   - Clique em **Configurar**
   - Adicione seu domínio e URL de retorno:
     - **Domínios**: `yourdomain.com`
     - **URLs de Retorno**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Clique em **Salvar** e depois em **Continuar** e **Salvar** novamente

4. **Crie uma Chave**
   - Na barra lateral esquerda, clique em **Chaves** e depois no botão **+**
   - Insira um nome da chave (ex: "Chave de OAuth da Loja")
   - Marque **Faça login com a Apple**
   - Clique em **Configurar** e selecione seu ID de Aplicativo Principal
   - Clique em **Salvar**, depois em **Continuar** e **Registrar**
   - **Baixe o arquivo da chave** (.p8) — você não poderá baixá-lo novamente

5. **Reúna as Informações Necessárias**
   Você precisa:
   - **ID do Cliente** (ID de Serviço): O identificador que você criou (ex: `com.yourstore.login`)
   - **ID da Equipe**: Localizado no canto superior direito do portal do desenvolvedor Apple
   - **ID da Chave**: Mostrado quando você criou a chave
   - **Chave Privada**: O conteúdo do arquivo .p8 que você baixou

6. **Insira as Credenciais no Spwig**
   - Volte para as configurações de OAuth do Spwig
   - Cole o ID do Cliente, ID da Equipe e ID da Chave
   - Abra o arquivo .p8 em um editor de texto e copie seu conteúdo
   - Cole a chave inteira (incluindo cabeçalhos) no campo de Chave Privada
   - Clique em **Salvar**
   - Ative o **OAuth da Apple** clicando no interruptor

### Teste

- Visite a página de login da sua loja em um dispositivo com um ID da Apple
- Clique em "Faça login com a Apple"
- Autentique com seu ID da Apple
- Você deve estar logado com sucesso

## Configuração do OAuth do Microsoft

O OAuth do Microsoft é ideal para lojas que atendem a clientes corporativos que usam o Office 365 ou Azure AD.

### Pré-requisitos

- Uma conta do Microsoft
- Acesso ao Azure Portal

### Configuração Passo a Passo

1. **Navegue até as Configurações de OAuth**
   - Vá para **Configurações > Configurações da Loja > Provedores OAuth**
   - Clique em **Configurar Microsoft**

2. **Registre um Aplicativo no Azure**
   - Visite [Azure Portal](https://portal.azure.com/)
   - Vá para **Azure Active Directory > Registros de Aplicativo**
   - Clique em **Nova inscrição**
   - Insira um nome (ex: "OAuth da Loja")
   - Selecione **Contas em qualquer diretório organizacional e contas pessoais Microsoft**
   - Sob **URI de Redirecionamento**, selecione **Web** e insira:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Clique em **Registrar**

3. **Copie o ID do Aplicativo**
   - Na página de visão geral do aplicativo, copie o **ID do Aplicativo (cliente)**

4. **Crie um Segredo do Cliente**
   - Na barra lateral esquerda, clique em **Certificados & segredos**
   - Clique em **Novo segredo do cliente**
   - Insira uma descrição (ex: "Segredo OAuth")
   - Selecione um período de expiração (recomendado: 24 meses)
   - Clique em **Adicionar**
   - **Copie o valor do segredo imediatamente** — ele não será mostrado novamente

5. **Insira as Credenciais no Spwig**
   - Volte para as configurações de OAuth do Spwig
   - Cole o ID do Aplicativo (cliente) como ID do Cliente
   - Cole o valor do segredo como Segredo do Cliente
   - Opcionalmente insira um ID do Inquilino (para aplicativos de único inquilino; deixe em branco para multi-inquilino)
   - Clique em **Salvar**
   - Ative o **OAuth do Microsoft** clicando no interruptor

### Teste

- Visite a página de login da sua loja
- Clique em "Faça login com o Microsoft"
- Autentique com sua conta do Microsoft
- Você deve estar logado com sucesso

## Gerenciamento de Conexões OAuth

### Visão do Cliente

Os clientes podem visualizar e gerenciar seus provedores OAuth conectados a partir do painel de controle da conta:

- Navegue até **Minha Conta > Contas Conectadas**
- Veja quais provedores estão vinculados (Google, Apple, Microsoft)
- Desconecte um provedor clicando em **Desconectar**
- Reconecte clicando novamente no login com esse provedor

### Múltiplos Provedores

Uma única conta do cliente pode estar vinculada a múltiplos provedores OAuth. Por exemplo, um cliente pode conectar tanto o Google quanto o Apple à mesma conta.

Se um cliente tentar fazer login com um provedor OAuth diferente usando o mesmo endereço de e-mail, o Spwig vinculará automaticamente à sua conta existente.

### Gerenciamento pelo Admin

Como administrador, você pode visualizar as conexões OAuth dos clientes:

- Vá para **Clientes > Clientes**
- Abra o registro do cliente
- Role até a seção **Contas Conectadas**
- Veja quais provedores estão vinculados e quando foram conectados

Você não pode desconectar provedores em nome dos clientes — eles devem fazê-lo por motivos de segurança.

## Solução de Problemas

### Mismatch de URI de Redirecionamento

**Erro**: "Mismatch de URI de redirecionamento" ou "URI de redirecionamento inválido"

**Solução**:
- Certifique-se de que a URI de redirecionamento nas configurações do provedor corresponda exatamente àquela no Spwig
- Verifique se há barras inclinadas no final — elas devem corresponder
- Verifique se você está usando `https://` (não `http://`)
- Limpe o cache do navegador e tente novamente

### Credenciais Inválidas

**Erro**: "ID do cliente inválido" ou "Autenticação falhou"

**Solução**:
- Verifique novamente se você copiou corretamente o ID do Cliente e o Segredo do Cliente
- Certifique-se de que não haja espaços extras ou quebras de linha
- Verifique se as credenciais são do projeto/aplicativo correto
- Para Apple, certifique-se de que a Chave Privada inclua o conteúdo completo do arquivo .p8

### API do Provedor Não Ativada

**Erro**: "API não ativada" ou "Acesso não configurado"

**Solução**:
- Para Google: Certifique-se de que você ativou a API do Google+ no seu projeto do Google Cloud
- Para Microsoft: Verifique se sua inscrição do aplicativo foi aprovada e está ativa
- Para Apple: Verifique se "Faça login com a Apple" está ativado para o seu ID de Serviço

### SSL Necessário

**Erro**: "OAuth requer HTTPS" ou "URI de redirecionamento insegura"

**Solução**:
- Os provedores OAuth exigem SSL/TLS (HTTPS) para segurança
- Certifique-se de que sua loja tenha um certificado SSL válido instalado
- Atualize suas URIs de redirecionamento para usar `https://` em vez de `http://`
- Se estiver testando localmente, use um serviço como ngrok para criar um túnel HTTPS

### Botão Não Aparece

**Problema**: O botão "Faça login com Google/Apple/Microsoft" não aparece na página de login

**Solução**:
- Verifique se o provedor está habilitado nas configurações de OAuth
- Limpe o cache do navegador e atualize a página
- Verifique se seu tema inclui o modelo de login social
- Revise o console do navegador para erros de JavaScript

## Dicas e Boas Práticas

### Segurança

- **Rotacione segredos regularmente** — Atualize os Segredos do Cliente a cada 12-24 meses
- **Monitore tentativas de login falhadas** — Observe padrões de autenticação incomuns
- **Use credenciais separadas por ambiente** — Credenciais diferentes para staging e produção
- **Restrinja URIs de redirecionamento** — Adicione apenas as URIs exatas que você precisa

### Experiência do Usuário

- **Habilite todos os três provedores** — Dê aos clientes escolha; diferentes demografias preferem diferentes provedores
- **Posicione os botões de forma proeminente** — Os botões de login social devem estar acima do formulário de e-mail/senha
- **Use branding reconhecível** — Mantenha os estilos padrão dos botões do Google/Apple/Microsoft
- **Teste em dispositivos móveis** — Os fluxos OAuth funcionam de forma diferente em navegadores móveis

### Conformidade

- **Política de Privacidade** — Divulgue que você usa provedores OAuth e quais dados você recebe
- **Termos de Serviço** — Cumpra os termos do provedor (Google, Apple, Microsoft cada um tem requisitos)
- **Minimização de Dados** — Solicite apenas as informações do perfil que você realmente precisa

### Checklist de Teste

Antes de ir ao ar, teste:

- [ ] Login com cada provedor no desktop
- [ ] Login com cada provedor em dispositivos móveis
- [ ] Primeiro login (criação de conta)
- [ ] Logins subsequentes (vinculação de conta)
- [ ] Login com o mesmo e-mail em diferentes provedores
- [ ] Desconectar e reconectar um provedor
- [ ] Fluxo de redefinição de senha ainda funciona para usuários não OAuth

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.