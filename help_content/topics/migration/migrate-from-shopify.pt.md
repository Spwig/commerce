---
title: Migrando do Shopify
---

Se sua loja atualmente funciona no Shopify, o assistente de migração do Spwig pode importar seus produtos, clientes, pedidos e conteúdo conectando-se a um pequeno aplicativo personalizado que você cria no painel de parceiros do Shopify. A plataforma do Shopify é mais restritiva do que a maioria, então a maior parte deste guia é sobre criar esse aplicativo corretamente — a conexão em si é um passo de cinco minutos uma vez que o aplicativo existir.

## Antes de Começar

Dois limites específicos do Shopify são importantes o suficiente para serem mencionados aqui, e não apenas mais adiante em uma tabela:

> **Importante:** O Shopify não tem uma API de avaliações, então **as avaliações dos clientes não são migradas de forma alguma**, independentemente das permissões de aplicativo que você conceder. Se você precisar de suas avaliações, exporte-as separadamente do aplicativo de avaliação que estiver usando (Judge.me, Yotpo, Loox, etc.) e importe-as no Spwig por conta própria.

> **Importante:** Por padrão, o Spwig pode ler **apenas pedidos dos últimos 60 dias**. Para transferir sua história completa de pedidos, você deve adicionar o escopo `read_all_orders` ao criar seu aplicativo — veja a lista de escopos abaixo. Isso é fácil de ser perdido, já que o aplicativo ainda se conecta e importa com sucesso sem ele; ele apenas limita silenciosamente o quanto você pode voltar na história de pedidos.

Tudo o resto transfere bem: categorias (como Coleções — veja abaixo), produtos, imagens, variantes, clientes e endereços, descontos e conteúdo do blog. Campos personalizados são outra lacuna notável — veja **Metafields do Shopify** no final deste guia.

Também lembre-se de:

- As opções **Importar configurações de impostos** e **Importar zonas e métodos de envio** do assistente não são aplicadas aos dados importados. Configure as taxas de impostos e envio no Spwig por conta própria depois — veja [Depois da Migração](after-migration-review).
- A opção **Ajuste de preço** na mesma etapa *faz* efeito para importações do Shopify, alterando o preço base de cada produto conforme ele é criado. Deixe-a definida como **Nenhum** a menos que você queira deliberadamente que todos os preços sejam ajustados.
- Você precisará ter acesso a uma conta Shopify Partners para criar o aplicativo. Se você ainda não tem uma, o Shopify permite que você crie uma gratuitamente em partners.shopify.com.

## Criando o Aplicativo do Shopify

O Spwig se conecta ao Shopify por meio de um aplicativo personalizado que você cria e instala em sua própria loja. Isso imita o guia **Shopify API Setup Guide** dentro do produto (aberto via **Open Setup Guide** na etapa 2 do assistente), então os passos abaixo correspondem exatamente ao que você verá lá — você pode seguir qualquer um deles.

### Etapa 1: Criar o aplicativo

1. Vá para seu [painel de desenvolvimento do Shopify Partners](https://dev.shopify.com/dashboard) e abra **Apps**
2. Clique em **Criar aplicativo**
3. Escolha **Começar a partir do Painel de Desenvolvimento**
4. Insira o nome do aplicativo: `Spwig Migration`
5. Clique em **Criar**

![Criando o aplicativo Spwig Migration no painel de desenvolvimento do Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Etapa 2: Definir a URL do Aplicativo e escopos

Na página de configuração do novo aplicativo, sob **Versões**, defina:

- **URL do Aplicativo**: `https://shopify.dev/apps/default-app-home`
- **Escopos**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Definindo a URL do Aplicativo e escopos necessários](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Escopo | Dá ao Spwig acesso a |
|---|---|
| `read_products` | Produtos, variantes, imagens, coleções |
| `read_customers` | Nomes de clientes, e-mails, endereços |
| `read_orders` | Pedidos dos últimos 60 dias |
| `read_content` | Posts de blog e páginas |
| `read_discounts` | Códigos de desconto e regras |
| `read_files` | Arquivos de mídia carregados |

> **Nota:** Quer sua história completa de pedidos em vez de apenas os últimos 60 dias? Adicione `read_all_orders` à lista de escopos acima.

### Etapa 3: Copiar seu ID do Cliente e Segredo

Vá para **Configurações > Credenciais** e copie o **ID do Cliente** e **Segredo** mostrados lá — você colará esses no assistente do Spwig em breve.

![Copiando o ID do Cliente e Segredo da página de configurações do aplicativo](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Etapa 4: Gerar um link de distribuição personalizado

1.

Vá para **Distribuição** e selecione **Distribuição personalizada**
2.

Digite o domínio da sua loja (por exemplo, `yourstore.myshopify.com`)
3.

Clique em **Gerar link**, depois **Copie** o link de instalação que ele produz

![Copiando o link de instalação de distribuição personalizada gerado](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Etapa 5: Instale o app em sua loja

Abra o link de instalação que você acabou de copiar no seu navegador (certifique-se de que você está conectado ao administrador da sua loja Shopify), revise as permissões que ele solicita e clique em **Instalar**.

![Instalando o app na loja Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Importante:** Esta última etapa é fácil de ser ignorada. Gerar o link de instalação não instala o app — você precisa realmente abrir o link e clicar em Instalar, ou o Spwig não será capaz de se conectar. Se o teste de conexão falhar na próxima seção, este é o primeiro item a verificar.

## Copiando suas credenciais para o Spwig

No administrador do Spwig, vá para **Importação e Exportação de Dados > Iniciar Nova Migração**, escolha **Shopify** na etapa 1 e, na etapa 2, insira:

- **Domínio da loja** — `yourstore.myshopify.com`
- **ID do cliente** — de Configurações > Credenciais
- **Segredo do cliente** — de Configurações > Credenciais

Se você preferir seguir o tutorial dentro do produto em vez desse guia, clique em **Abrir Guia de Configuração** nesta etapa — ele cobre os mesmos cinco passos acima com as mesmas capturas de tela e leva cerca de 10 minutos do início ao fim.

Mantenha **Testar a conexão antes de prosseguir** marcado. Se `read_products`, `read_customers` ou `read_orders` estiver faltando nas permissões do seu app, o Spwig avisa você antes de continuar — volte para a página de Versões do app no painel do Shopify, adicione a permissão faltando, salve uma nova versão e tente novamente.

## Revisando e Selecionando Dados

A etapa 3 puxa contagens em tempo real da sua loja e mostra uma amostra dos primeiros cinco produtos. Algumas coisas parecem diferentes de outras plataformas:

- **Coleções, não categorias** — O Shopify organiza produtos em Coleções em vez de categorias, e Coleções não suportam aninhamento, então a hierarquia importa como plana. Se sua loja Shopify usou coleções para representar uma árvore de categorias, planeje-se para reconstruir essa estrutura no gerenciador de categorias do Spwig após a importação.
- **Descontos, não cupons** — Os códigos de desconto e regras do Shopify importam como descontos do Spwig.
- **Nenhuma linha de avaliações** — como o Shopify não tem API de avaliações, esse tipo de dado não aparece nessa etapa de forma alguma, ao contrário do WooCommerce ou importações CSV.

As **Opções de Importação** funcionam da mesma forma que em outras plataformas: **Ignorar itens existentes** (ligado) corresponde a SKU e e-mail para evitar duplicatas; **Importar imagens de produtos** (ligado) é mais lento, mas recomendado; **Manter os IDs originais quando possível** (desligado) deve permanecer desligado, a menos que você tenha um motivo específico para mudar; **Tamanho do lote** padrão é 25.

## Metafields do Shopify

Se você usar metafields do Shopify para armazenar dados extras em produtos, clientes ou pedidos, saiba que o Spwig não detecta ou lê eles — ao contrário do WooCommerce, não há etapa de mapeamento de campos personalizados para importações do Shopify. Qualquer dado que você armazenou em metafields precisará ser reentrado manualmente no Spwig usando [campos personalizados](migration-field-mapping) após a migração, então é útil exportar uma lista de seus metafields e seus valores do Shopify antes de começar.

## Executando a Importação

Uma vez que você revisou a etapa 3, inicie a importação. Ela roda em segundo plano — você pode fechar a janela do navegador e ela continua. A etapa 5 mostra o progresso em tempo real com uma linha por tipo de dado e um log de atividade expansível.

A etapa 6 mostra seus resultados: o que foi importado, ignorado ou falhou, mais uma ferramenta de **Reescrita de Links** se links internos para seu antigo domínio `myshopify.com` foram encontrados no conteúdo importado.

Revise com cuidado o resumo, em seguida, siga o checklist em [Após sua migração](after-migration-review) — ele abrange a verificação dos seus dados, a reconstrução de qualquer hierarquia de coleções, a configuração de taxas de impostos e envio (que o assistente não configura para você) e a reentrada de qualquer coisa que tenha sido armazenada em metafields.

## Exclua o App do Shopify

Depois de confirmar que a migração foi concluída com sucesso, volte para a página **Apps** do administrador do Shopify, ou no painel de Parceiros, e exclua o app de migração do Spwig (ou, no mínimo, desinstale-o do seu loja). Não há razão para manter o acesso de leitura aos dados da sua loja ativo após a migração estar concluída.

## Dicas

- **O histórico de pedidos está limitado por padrão** — se você precisar de mais do que os últimos 60 dias de pedidos, adicione `read_all_orders` à lista de escopo antes de gerar seu link de instalação, e não depois.
- **Avaliações precisam de uma exportação separada** — planeje-se para isso antes de migrar, já que não há como trazer as avaliações por meio do assistente de nenhuma forma.
- **Gerar o link não é o mesmo que instalar o app** — sempre conclua a Etapa 5 e clique em Instalar, ou o teste de conexão no Spwig falhará.
- **Coleções vêm em formato plano** — se a estrutura de categoria importava para navegação ou SEO, reserve tempo para reconstruir a hierarquia no Spwig após a importação.
- **Exporte seus metafields primeiro** — o Spwig não pode lê-los, então capture esses dados do Shopify antes de começar, se você precisar deles mais tarde.
- **Exclua o app uma vez que você estiver verificado** — não deixe uma integração ativa apontando para sua loja antiga depois que você tiver se movido para frente.