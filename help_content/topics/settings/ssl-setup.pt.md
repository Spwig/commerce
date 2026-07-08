---
title: Configuração SSL
---

SSL (Secure Sockets Layer) criptografa a conexão entre os navegadores dos seus clientes e sua loja. Quando o SSL está ativo, o URL da sua loja começa com `https://` e os navegadores exibem um ícone de cadeado. O SSL é essencial para aceitar pagamentos, proteger os dados dos clientes e obter um bom ranqueamento nos motores de busca.

O Spwig oferece suporte a vários modos de SSL para se adequar a diferentes configurações de hospedagem. Este guia explica cada modo e ajuda você a escolher o correto.

## Escolhendo um Modo SSL

| Modo | Melhor para | Custo do certificado | Renovação |
|------|----------|-----------------|---------|
| **Let's Encrypt** | A maioria das lojas | Grátis | Automática |
| **Cloudflare Origin CA** | Lojas usando o proxy da Cloudflare | Grátis | Manual (até 15 anos) |
| **Certificado Personalizado** | Lojas com certificados comprados | Varia | Manual |
| **Gerenciado Externamente** | Balanceadores de carga, Cloudflare Flexible | N/A | N/A |
| **Autoassinado** | Desenvolvimento e testes | Grátis | Manual |
| **Nenhum (HTTP)** | Apenas desenvolvimento local | N/A | N/A |

Se você não tiver certeza de qual modo usar, **Let's Encrypt** é a melhor escolha para a maioria das lojas. É gratuito, automático e confiável por todos os navegadores.

## Let's Encrypt

O Let's Encrypt fornece certificados SSL gratuitos e confiáveis que se renovam automaticamente a cada 60-90 dias. Esta é a opção recomendada para a maioria dos comerciantes.

**Requisitos:**
- Seu domínio deve apontar para seu servidor (registro A no DNS)
- A porta 80 deve estar acessível na internet (para verificação do certificado)
- Um endereço de e-mail para notificações de expiração do certificado

**Passos de configuração:**
1. Vá para **Configurações > Configurações do Site** e abra a guia **Domínio & SSL**
2. Insira o nome do seu domínio
3. Selecione **Let's Encrypt**
4. Insira o endereço de e-mail do administrador
5. Clique em **Aplicar Configuração**

O Spwig lida com tudo automaticamente: verificando seu domínio, obtendo o certificado, configurando o NGINX e configurando a renovação automática.

## Cloudflare Origin CA

Os certificados Cloudflare Origin CA criptografam a conexão entre os servidores de borda da Cloudflare e sua loja. Esses certificados são gratuitos e podem durar até 15 anos, mas são **confiáveis apenas pela Cloudflare** — navegadores conectando-se diretamente ao seu servidor verão um aviso de certificado.

Este modo é ideal se você usar a Cloudflare como proxy (nuvem laranja ativada) para seu domínio. A Cloudflare apresenta seu próprio certificado confiável aos visitantes, e o certificado Origin CA protege a conexão entre a Cloudflare e seu servidor.

**Requisitos:**
- Uma conta Cloudflare com seu domínio adicionado
- Um certificado Origin CA e uma chave privada gerados a partir do painel da Cloudflare
- O modo SSL/TLS da Cloudflare definido como **Full (Strict)**

**Gerando o certificado Origin CA:**
1. Faça login no painel da Cloudflare
2. Selecione seu domínio
3. Vá para **SSL/TLS > Origin Server**
4. Clique em **Criar Certificado**
5. Escolha RSA ou ECC (RSA é mais compatível)
6. Adicione seu domínio (ex: `example.com` e `*.example.com`)
7. Escolha um período de validade (15 anos é recomendado)
8. Clique em **Criar** e copie tanto o certificado quanto a chave privada

**Configurando no Spwig:**
1. Vá para **Configurações > Configurações do Site** e abra a guia **Domínio & SSL**
2. Insira o nome do seu domínio
3. Selecione **Cloudflare Origin CA**
4. Cole o certificado no campo **Certificado (PEM)**
5. Cole a chave privada no campo **Chave Privada (PEM)**
6. Clique em **Aplicar Configuração**

**Após a configuração:**
- Na Cloudflare, defina o modo SSL/TLS como **Full (Strict)**
- Ative o proxy da Cloudflare (nuvem laranja) para o registro DNS do seu domínio
- Sua loja será acessível via HTTPS com o certificado confiável da Cloudflare

## Certificado Personalizado

Use este modo se você comprou um certificado SSL de uma autoridade de certificação (CA) como DigiCert, Sectigo ou GoDaddy, ou se seu provedor de hospedagem emitiu um para você.

**Passos de configuração:**
1.

Vá para **Configurações > Configurações do Site** e abra a guia **Domínio & SSL**
2.

Insira o nome do seu domínio
3.

Selecione **Certificado Personalizado**
4.

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

Cole a cadeia de certificados (incluindo certificados intermediários) no campo **Certificate (PEM)**
5.

Cole sua chave privada no campo **Private Key (PEM)**
6.

Clique em **Apply Configuration**

Seu certificado deve incluir a cadeia completa: seu certificado do domínio seguido por quaisquer certificados intermediários. A chave privada deve estar no formato PEM (começando com `-----BEGIN PRIVATE KEY-----` ou `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Escolha este modo quando o SSL for terminado por um serviço externo antes que o tráfego chegue ao seu servidor. Nesta configuração, seu servidor recebe apenas tráfego HTTP puro — nenhum certificado é instalado no próprio servidor.

**Cenários comuns:**
- **Cloudflare Flexible SSL** -- O Cloudflare criptografa o tráfego do navegador para o Cloudflare, mas envia HTTP para seu servidor
- **Balanceadores de carga na nuvem** -- O AWS ALB, Google Cloud Load Balancer ou DigitalOcean Load Balancer termina o SSL e encaminha HTTP
- **Proxy reverso** -- Outro servidor à frente do Spwig lida com o SSL

**Passos de configuração:**
1. Vá para **Settings > Site Settings** e abra a guia **Domain & SSL**
2. Insira o nome do seu domínio
3. Selecione **Managed Externally**
4. Clique em **Apply Configuration**

O Spwig configurará o NGINX para servir apenas HTTP e confiará no cabeçalho `X-Forwarded-Proto` do seu proxy para detectar corretamente os visitantes HTTPS.

## Self-Signed Certificate

Certificados autoassinados criptografam a conexão, mas não são confiados pelos navegadores. Os visitantes verão um aviso de segurança que devem ignorar manualmente. Este modo é adequado apenas para servidores de desenvolvimento e testes internos.

**Passos de configuração:**
1. Vá para **Settings > Site Settings** e abra a guia **Domain & SSL**
2. Insira o nome do seu domínio
3. Selecione **Self-Signed**
4. Clique em **Apply Configuration**

O Spwig gera automaticamente um certificado autoassinado. Não use este modo para uma loja de produção.

## Troubleshooting

**Certificado não funcionando após a configuração:**
- Verifique se o registro A do seu domínio aponta para o IP do seu servidor
- Certifique-se de que as portas 80 e 443 estão abertas no seu firewall
- Aguarde alguns minutos para que as alterações no DNS se propaguem

**Let's Encrypt falha ao emitir um certificado:**
- Verifique se o seu domínio resolve para o IP deste servidor
- Certifique-se de que a porta 80 não está bloqueada por um firewall
- Se você estiver atrás do Cloudflare, temporariamente defina o DNS para "DNS only" (nuvem cinza) durante a emissão do certificado

**Cloudflare mostra "Error 526" (Certificado SSL Inválido):**
- Certifique-se de que você selecionou o modo **Cloudflare Origin CA** (não Managed Externally)
- Verifique se o modo SSL/TLS do Cloudflare está definido como **Full (Strict)**
- Verifique se o certificado Origin CA não expirou

**O navegador mostra "Not Secure" apesar de ter SSL:**
- Algumas páginas podem carregar imagens ou scripts via HTTP (conteúdo misto). Verifique o console do desenvolvedor do seu navegador para avisos de conteúdo misto.
- Certifique-se de que a URL do seu site nas Configurações use `https://`