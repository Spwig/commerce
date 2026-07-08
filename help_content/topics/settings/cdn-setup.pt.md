---
title: Configuração de CDN
---

A Content Delivery Network (CDN) armazena cópias das imagens, folhas de estilo e scripts da sua loja em servidores ao redor do mundo. Quando um cliente visita sua loja, esses arquivos são fornecidos a partir do servidor mais próximo a ele, em vez do seu servidor de hospedagem principal. Isso reduz o tempo de carregamento da página, especialmente para clientes localizados longe do local onde sua loja está hospedada.

O Spwig já otimiza a entrega de ativos estáticos por padrão com pré-compressão Brotli e gzip, cache de ativos com assinatura e cabeçalhos imutáveis de 1 ano, e negociação de conteúdo adequada. Adicionar uma CDN é opcional, mas pode melhorar ainda mais a velocidade para lojas com uma base de clientes internacional.

## Sua Loja Precisa de uma CDN?

Não todas as lojas se beneficiam igualmente de uma CDN. Use estas diretrizes para decidir:

**Uma CDN é recomendada se**:
- Seus clientes estão espalhados por múltiplos países ou continentes
- Sua loja possui muitas imagens de produtos ou páginas pesadas em termos de mídia
- Você deseja os tempos de carregamento de página mais rápidos possíveis em todo o mundo
- Você vende para regiões longe do seu servidor de hospedagem (ex.: servidor na Europa, clientes na Ásia)

**Uma CDN provavelmente é desnecessária se**:
- Seus clientes são principalmente locais ou dentro do mesmo país do seu servidor
- Sua loja tem um catálogo pequeno com poucas imagens
- Seu provedor de hospedagem já inclui uma CDN integrada

Quando em dúvida, uma CDN não prejudica o desempenho. Serviços como o Cloudflare oferecem planos gratuitos, então não há custo para tentar.

## Como o Spwig Funciona com CDNs

O Spwig está pronto para CDN por padrão. Você não precisa alterar nenhum código ou configuração dentro do painel de administração do Spwig. Aqui está o que o Spwig já faz por você:

- **Arquivos estáticos com assinatura** -- Cada arquivo CSS, JavaScript e imagem inclui um hash de versão única em seu nome de arquivo. Isso significa que as CDNs podem armazenar em cache esses arquivos por um longo tempo sem servir conteúdo desatualizado.
- **Cabeçais de cache de longa duração** -- Ativos estáticos são fornecidos com cabeçais de cache imutáveis de 1 ano, informando às CDNs e navegadores para armazenar em cache agressivamente.
- **Arquivos pré-comprimidos** -- O Spwig pré-comprime ativos usando Brotli e gzip, então sua CDN pode entregar arquivos menores sem processamento adicional.
- **Negociação de conteúdo adequada** -- O Spwig envia os cabeçais de tipo de conteúdo e codificação corretos que as CDNs dependem para armazenamento em cache adequado.

Tudo que você precisa fazer é apontar os DNS do seu domínio para o provedor da CDN, e tudo funciona automaticamente.

## Configurando o Cloudflare

O Cloudflare é a CDN mais popular e oferece um plano gratuito que funciona bem para a maioria das lojas. Siga estas etapas:

**Etapa 1: Criar uma Conta no Cloudflare**
- Visite cloudflare.com e cadastre-se para uma conta gratuita

**Etapa 2: Adicionar seu Domínio**
- Clique em **Adicionar um Site** e insira o nome do domínio da sua loja
- Selecione o plano **Gratuito** (suficiente para a maioria das lojas)

**Etapa 3: Atualizar os Nameservers do DNS**
- O Cloudflare mostrará dois nameservers (ex.: `anna.ns.cloudflare.com`)
- Faça login no seu registrador de domínio (onde você comprou seu domínio)
- Substitua os nameservers atuais pelos nameservers do Cloudflare
- As alterações de DNS podem levar até 24 horas para surtir efeito

**Etapa 4: Configurar SSL/TLS**
- No painel do Cloudflare, vá para **SSL/TLS**
- Defina o modo de criptografia para **Full (strict)**
- Isso garante que todo o tráfego entre o Cloudflare e seu servidor permaneça criptografado

**Etapa 5: Verificar se Está Funcionando**
- Depois que o DNS propagar, visite sua loja e verifique o cabeçalho `cf-cache-status` no seu navegador (veja Verificando sua CDN abaixo)

## Configurando o AWS CloudFront

Se você já usa o Amazon Web Services, o CloudFront se integra naturalmente com sua infraestrutura:

1. Abra o console do **CloudFront** em sua conta AWS
2. Crie uma nova **Distribuição** com o domínio da sua loja como origem
3. Defina a **Política de Protocolo de Origem** para "HTTPS Only"
4. Sob **Comportamento de Cache**, defina a **Política de Cache** para "CachingOptimized" para ativos estáticos
5. Adicione o domínio da sua loja como **Nome de Domínio Alternativo (CNAME)**
6. Anexe um certificado SSL do AWS Certificate Manager
7. Atualize o DNS do seu domínio para apontar para a URL da distribuição do CloudFront

O preçário do CloudFront é baseado no uso.

Para a maioria das lojas, os custos são mínimos, pois os ativos com impressão digital do Spwig são armazenados em cache por períodos longos.

## Configurações Recomendadas para CDN

Para os melhores resultados, configure seu CDN para armazenar em cache o conteúdo certo e pular o resto.

**O que armazenar em cache** (ativos estáticos):
- `/static/` -- Todos os estilos, scripts, fontes e ativos do tema
- `/media/` -- Imagens de produtos e arquivos de mídia carregados
- Arquivos de imagem (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Arquivos de fonte (`.woff`, `.woff2`)

**O que NÃO armazenar em cache** (páginas dinâmicas):
- `/admin/` -- O painel de administração deve sempre servir conteúdo atual
- `/cart/` -- Páginas do carrinho de compras contêm dados específicos da sessão
- `/checkout/` -- Páginas de checkout nunca devem ser armazenadas em cache por segurança
- `/accounts/` -- Páginas de conta do cliente contêm dados privados
- Qualquer página que exija login ou exiba conteúdo personalizado

**Regras gerais de armazenamento em cache**:
- **Respeite os cabeçalhos de cache do origin** -- O Spwig envia os cabeçalhos de controle de cache corretos para cada tipo de conteúdo. Configure seu CDN para respeitar esses cabeçalhos em vez de substituí-los.
- **Ative a compressão Brotli** -- Tanto o Cloudflare quanto o CloudFront suportam Brotli. Ative-o para aproveitar os ativos pré-comprimidos do Spwig.
- **Defina o TTL de cache do navegador para "Respeitar os Cabeçalhos Existentes"** -- Isso permite que a política de cache embutida do Spwig determine o comportamento.

## Verificando Seu CDN

Após a configuração, confirme que o CDN está servindo corretamente seu conteúdo:

**Etapa 1: Abra as Ferramentas de Desenvolvedor do Navegador**
- No Chrome ou Firefox, pressione **F12** para abrir as ferramentas de desenvolvedor
- Clique na guia **Rede**

**Etapa 2: Carregue Sua Loja**
- Visite a página inicial de sua loja com as ferramentas de desenvolvedor abertas
- Clique em qualquer solicitação de arquivo estático (ex: um arquivo `.css` ou `.js`)

**Etapa 3: Verifique os Cabeçalhos de Resposta**
- **Cloudflare**: Procure o cabeçalho `cf-cache-status`. Um valor de `HIT` significa que o arquivo foi servido a partir do cache do CDN. `MISS` significa que foi buscado no seu servidor (apenas na primeira solicitação).
- **CloudFront**: Procure o cabeçalho `x-cache`. Um valor de `Hit from cloudfront` confirma a entrega pelo CDN.

**Etapa 4: Teste de Outra Localização**
- Use uma ferramenta gratuita como gtmetrix.com ou webpagetest.org para testar sua loja de diferentes localizações geográficas
- Compare os tempos de carregamento antes e depois da configuração do CDN

## Problemas Comuns

### Conteúdo Obsoleto Após Alterações no Tema

**Problema**: Após atualizar seu tema ou fazer alterações de design, os clientes ainda veem a versão antiga.

**Solução**: Limpe o cache do seu CDN. No Cloudflare, vá para **Caching > Configuração > Limpar Tudo**. No CloudFront, crie uma **Invalidação** para `/*`. Observe que os ativos com impressão digital do Spwig normalmente evitam esse problema, pois os arquivos atualizados recebem automaticamente novos nomes de arquivo. Esse problema afeta mais comumente ativos sem impressão digital, como uploads personalizados.

---

### Avisos de Conteúdo Misturado

**Problema**: Seu navegador mostra um aviso de segurança sobre "conteúdo misturado" após habilitar o CDN.

**Solução**: Certifique-se de que o modo SSL do seu CDN está definido como **Completo (estrito)**, e não "Flexível". O modo Flexível pode causar seu servidor a receber solicitações HTTP em vez de HTTPS, resultando em avisos de conteúdo misturado. No Cloudflare, verifique **SSL/TLS > Visão Geral** e confirme o modo.

---

### Painel de Administração Executando Lentamente

**Problema**: O painel de administração parece mais lento após adicionar um CDN.

**Solução**: CDNs não devem armazenar em cache páginas de administração. Crie uma **Regra de Página** (Cloudflare) ou **Comportamento de Cache** (CloudFront) que defina o armazenamento em cache como "Bypass" para qualquer URL que corresponda a `/admin/*`. Isso garante que as solicitações do painel de administração vão diretamente para seu servidor, sem sobrecarga do CDN.

---

### Imagens Não Carregando

**Problema**: Imagens de produtos ou arquivos de mídia retornam erros após a configuração do CDN.

**Solução**: Verifique se a origem do seu CDN está configurada com o protocolo correto (HTTPS) e a porta. Além disso, verifique se o firewall do seu servidor permite conexões a partir dos intervalos de IP do CDN.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- **Comece com a camada gratuita da Cloudflare** -- Ela atende às necessidades da maioria das lojas e leva apenas minutos para ser configurada
- **Sempre use o modo SSL completo (estrito)** -- O modo flexível cria vulnerabilidades de segurança e pode quebrar fluxos de checkout
- **Limpe o cache do seu CDN após atualizações importantes do tema** -- Embora os arquivos com assinatura de Spwig lidem com a maioria dos casos, uma limpeza completa do cache garante que nenhum conteúdo antigo fique pendurado
- **Não cache as páginas de checkout ou carrinho** -- O cache dessas páginas pode expor os dados de um cliente a outro
- **Teste a partir das localizações dos seus clientes** -- Use ferramentas gratuitas como webpagetest.org para medir o desempenho real-world das regiões onde seus clientes compram
- **Monitore as análises do seu CDN** -- Tanto a Cloudflare quanto a CloudFront oferecem dashboards mostrando taxas de acerto do cache, largura de banda economizada e tráfego por país
- **Mantenha o TTL do DNS baixo durante a configuração** -- Defina o TTL do DNS para 300 segundos (5 minutos) enquanto estiver se alternando para um CDN, depois aumente-o uma vez que tudo estiver confirmado funcionando
- **Um CDN não substitui um bom hospedagem** -- Seu servidor de origem ainda importa para páginas dinâmicas como checkout, carrinho e admin.

Escolha um hospedagem de qualidade junto com um CDN