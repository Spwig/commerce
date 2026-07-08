---
title: Guia de Instalação
---

Este guia orienta você na instalação do Spwig em seu próprio servidor. Todo o processo é automatizado — um único comando lida com a configuração do Docker, criação do banco de dados, configuração dos serviços e certificados SSL.

## Antes de começar

Você precisa:

- De um servidor executando **Ubuntu 22.04 ou 24.04** (Debian 12 também é suportado)
- **Acesso root ou sudo** ao servidor
- Pelo menos **4 GB de RAM** e **20 GB de espaço em disco** (8 GB de RAM recomendado)
- Um **token de licença** do seu purchase do Spwig (verifique seu comprovante de e-mail)
- Opcionalmente, um **nome de domínio** apontado para o IP do seu servidor

> **Dica:** Você pode instalar sem um domínio e adicionar um depois usando a ferramenta de configuração de domínio. Sua loja estará acessível via IP do servidor no meio tempo.

## Executando o instalador

Conecte-se ao seu servidor via SSH e execute o comando de instalação do e-mail de confirmação do seu purchase. Ele parece com isso:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Substitua `YOUR_LICENSE_TOKEN` pelo token do seu e-mail.

O instalador passa por oito fases automaticamente:

1. **Verificações pré-voo** — verifica se seu servidor atende aos requisitos (sistema operacional, disco, RAM, portas)
2. **Validação do token** — confirma sua licença e extrai a configuração da sua loja
3. **Detecção do modo** — determina o melhor modo de instalação para seu servidor (veja abaixo)
4. **Configuração** — gera senhas seguras, credenciais do banco de dados e configuração dos serviços
5. **Download de imagem** — puxa as imagens do aplicativo Spwig do repositório
6. **Início do serviço** — inicia o banco de dados, cache, aplicação e trabalhadores de fundo em ordem
7. **Configuração SSL** — obtém um certificado SSL se você tiver um domínio configurado
8. **Finalização** — cria sua conta de administrador e gera scripts de conveniência

O processo leva 5–15 minutos, dependendo da velocidade de internet do seu servidor.

## Modos de instalação

O instalador detecta automaticamente o ambiente do seu servidor e seleciona o modo mais adequado. Você também pode especificar um manualmente com a bandeira `--mode`.

### Modo standalone

**Melhor para:** Servidores dedicados e instâncias VPS onde o Spwig é a única aplicação web.

- Usa diretamente as portas 80 e 443
- Gerencia certificados SSL automaticamente via Let's Encrypt
- Este é o modo mais comum e recomendado

### Modo sidecar

**Melhor para:** Servidores que já executam outra aplicação web (WordPress, um site corporativo, etc.) nas portas 80/443.

- O Spwig roda em uma porta alternativa (detectada automaticamente, geralmente 8080 ou 8443)
- O instalador gera um bloco de configuração do nginx para você adicionar ao seu servidor web existente
- Seu servidor web existente lida com SSL e proxya o tráfego para o Spwig

### Modo local

**Melhor para:** Desenvolvimento e testes no seu próprio computador.

- Acessível apenas em `localhost` ou `127.0.0.1`
- Usa um certificado SSL autoassinado (seu navegador mostrará um aviso de segurança — isso é normal)
- Funcionalidades de depuração estão habilitadas
- Nenhuma validação de licença é necessária

## O que acontece durante a instalação

### Docker

Se o Docker não estiver instalado, o instalador oferece a opção de instalá-lo para você. O Spwig roda totalmente dentro de contêineres Docker — nada é instalado diretamente no sistema operacional do seu servidor fora do Docker.

### Serviços criados

O instalador cria esses serviços:

| Serviço | Propósito |
|---------|---------|
| **Banco de dados** (PostgreSQL 16) | Armazena todos os dados do seu loja — produtos, pedidos, clientes, configurações |
| **Cache** (Redis) | Acelera o carregamento de páginas e gerencia filas de tarefas em segundo plano |
| **Conector de conexões** (PgBouncer) | Gerencia conexões de banco de dados de forma eficiente |
| **Armazenamento de objetos** (MinIO) | Armazena imagens, arquivos e mídia carregados |
| **Aplicação** (Spwig) | A loja em si — painel de administração e loja virtual |
| **Servidor web** (Nginx) | Fornece sua loja aos visitantes com compressão e cache |
| **Trabalhador de fundo** (Celery) | Processa e-mails, traduções, análises e outras tarefas em segundo plano |
| **Agendador de tarefas** (Celery Beat) | Executa tarefas agendadas, como backups automatizados e campanhas de e-mail |
| **Tradutor** | Serviço de tradução com IA para lojas multilíngues |
| **Atualizador** | Gerencia atualizações de componentes do mercado Spwig |

### Conta de administrador

No final da instalação, você é solicitado a criar uma conta de administrador. Esta é a conta que você usará para fazer login no painel de administração da sua loja.

### Modo de manutenção

Sua loja começa no **modo de manutenção** — os visitantes veem uma página "Em breve". Isso lhe dá tempo para configurar sua loja (adicionar produtos, configurar métodos de pagamento, personalizar seu tema) antes de ir ao ar.

Quando estiver pronto, execute o script de conveniência criado pelo instalador:

```bash
./go-live.sh
```

Ou desative o modo de manutenção em **Admin > Configurações da Loja > Manutenção**.

## Após a instalação

Depois que o instalador terminar, você verá um resumo com:

- O URL da sua loja
- O URL do painel de administração (normalmente `https://yourdomain.com/en/admin/`)
- O local dos seus arquivos de configuração
- Scripts de conveniência disponíveis

### Scripts de conveniência

O instalador cria esses scripts no diretório de instalação:

- **`./go-live.sh`** — retira sua loja do modo de manutenção
- **`./configure-domain.sh`** — adiciona ou altera seu domínio e obtém um certificado SSL

### Próximos passos

1. Faça login no seu painel de administração
2. Conclua o **Assistente de Configuração** — ele o guiará pelo nome da loja, moeda, fuso horário e configurações básicas
3. Adicione seus produtos
4. Configure um método de pagamento
5. Escolha e personalize um tema
6. Execute `./go-live.sh` quando estiver pronto

## Instalando em marketplaces de nuvem

O Spwig está disponível como uma aplicação de um clique em vários provedores de nuvem:

- **DigitalOcean** — implante a partir do DigitalOcean Marketplace
- **Akamai (Linode)** — implante a partir do Linode Marketplace
- **Vultr** — implante a partir do Vultr Marketplace

Essas imagens de marketplace vêm com o instalador pré-carregado. Após criar o servidor, faça SSH e siga as instruções na tela para concluir a configuração com seu token de licença.

## Obtenha ajuda

Se a instalação falhar ou você encontrar um erro:

1. Execute a **ferramenta de diagnóstico**: `./doctor.sh` (criada durante a instalação)
2. O doctor verifica todos os serviços, conectividade, SSL e problemas comuns
3. Use `./doctor.sh --fix` para tentar reparos automáticos
4. Entre em contato com o suporte do Spwig com a saída do doctor se o problema persistir