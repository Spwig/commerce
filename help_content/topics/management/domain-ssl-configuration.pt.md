---
title: Configuração de Domínio & SSL
---

Este guia explica como conectar um domínio personalizado ao seu loja Spwig e configurar certificados SSL para acesso seguro via HTTPS. Você pode configurar um domínio durante a instalação ou adicionar um depois.

## Adicionar um domínio após a instalação

Se você instalou o Spwig sem um domínio (usando o endereço IP do servidor), você pode adicionar um a qualquer momento.

### Etapa 1: Configurar DNS

Com seu registrador de domínio ou provedor de DNS:

1. Crie um **registro A** apontando seu domínio (ou subdomínio) para o endereço IP do seu servidor
2. Se estiver usando um subdomínio como `shop.example.com`, crie o registro A para `shop`
3. Aguarde a propagação do DNS — isso geralmente leva 5–60 minutos

Verifique se o registro DNS está funcionando:

```bash
 dig +short shop.example.com
```

Isso deve retornar o endereço IP do seu servidor.

### Etapa 2: Execute o script de configuração do domínio

SSH no seu servidor e navegue até o diretório de instalação do Spwig:

```bash
 ./configure-domain.sh
```

O script fará:

1. Pedir o nome do seu domínio
2. Verificar se o DNS está apontando para seu servidor
3. Atualizar a configuração da loja
4. Obter um certificado SSL gratuito do Let's Encrypt
5. Configurar o servidor web para usar HTTPS
6. Reiniciar os serviços relevantes

Sua loja agora está acessível em `https://yourdomain.com`.

### Etapa 3: Atualizar as configurações da loja

Após adicionar um domínio, faça login no seu painel de administração e vá para **Configurações da Loja**. Verifique se o **URL da Loja** corresponde ao seu novo domínio. Isso garante que e-mails, notas fiscais e links usem o endereço correto.

## Certificados SSL

### SSL automático (Let's Encrypt)

Em **modo standalone**, o instalador obtém automaticamente um certificado SSL gratuito do Let's Encrypt. Esses certificados:

- São confiados por todos os principais navegadores
- Válidos por 90 dias
- Renovam automaticamente — uma verificação de renovação é executada diariamente, e os certificados são renovados quando têm menos de 30 dias restantes
- Cobrem seu domínio exato (ex. `shop.example.com`)

Você não precisa gerenciar a renovação manualmente.

### Certificados autoassinados

Em algumas situações, o Spwig usa um certificado autoassinado em vez disso:

- **Modo local** (instalação para desenvolvimento/teste)
- Quando o Let's Encrypt não pode acessar seu servidor (porta 80 bloqueada por firewall, DNS ainda não propagado)
- Quando nenhum domínio está configurado (acesso apenas por IP)

Certificados autoassinados criptografam o tráfego, mas não são confiados pelos navegadores — os visitantes verão um aviso de segurança. Isso é aceitável para testes, mas não deve ser usado em produção.

### SSL no modo Sidecar

No **modo sidecar**, seu servidor web existente (Apache, Nginx, Caddy, etc.) lida com o término do SSL. O Spwig roda em uma porta HTTP atrás do seu proxy. Configure o SSL no seu servidor web principal como normalmente faria.

O instalador gera um bloco de configuração de proxy que você pode adicionar ao seu servidor web. Para Nginx, ele parece algo assim:

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Alterar seu domínio

Para mudar para um domínio diferente:

1. Configure o DNS para o novo domínio (registro A apontando para seu servidor)
2. Execute `./configure-domain.sh` novamente com o novo domínio
3. O script atualiza todas as configurações, obtém um novo certificado e reinicia os serviços
4. Atualize **Configurações da Loja** no painel de administração com o novo URL

Seu antigo domínio deixará de funcionar uma vez que a configuração for atualizada.

## Solução de problemas

### "Validação de DNS falhou"

O script configure-domain verifica se seu domínio aponta para seu servidor antes de solicitar um certificado. Se essa verificação falhar:

- Verifique se o registro A está correto com `dig +short yourdomain.com`
- Aguarde alguns minutos a mais para a propagação do DNS
- Verifique se você está configurando o domínio ou subdomínio exato (não um wildcard)

### "Limite de taxa do Let's Encrypt atingido"

O Let's Encrypt limita as solicitações de certificados a 5 por domínio por semana. Se você atingir esse limite:



- Espere 7 dias antes de tentar novamente
- Use um subdomínio diferente no meio tempo
- A loja permanece acessível via HTTP ou com um certificado autoassinado enquanto você espera

### "Porta 80 não está acessível"

O Let's Encrypt precisa se conectar ao seu servidor na porta 80 para verificar a propriedade do domínio. Certifique-se de:

- Seu firewall permite entrada de TCP na porta 80
- Nenhuma outra aplicação está bloqueando a porta 80
- O grupo de segurança ou firewall de rede do seu provedor de nuvem permite a porta 80

### Falhas no renovação do certificado

Se a renovação automática falhar, o certificado expirará após 90 dias. Para renovar manualmente:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Verifique o log de renovação para detalhes, se isso falhar. A causa mais comum é a porta 80 estar bloqueada por uma mudança no firewall após a instalação inicial.