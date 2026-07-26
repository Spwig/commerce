---
title: Visão Geral da Migração de Dados
---

Se seus produtos, clientes e pedidos estão atualmente no WooCommerce, Shopify ou Magento — ou apenas em alguns arquivos CSV — a ferramenta de migração traz esses dados para sua nova loja Spwig, para que você não precise inseri-los manualmente. Ela lida com categorias, produtos, clientes, pedidos, avaliações e cupons, e, no caso do WooCommerce, também pode transferir conteúdo do blog e, com um plugin de ponte, seu programa de afiliados.

Encontre-a no menu lateral do administrador, sob **Painel do Sistema > Importação/Exportação de Dados** (visível para superusuários em instalações auto-hospedadas; se você não a vir, pergunte a quem gerencia sua instalação). A página, intitulada **Importação e Exportação de Dados**, lista todas as migrações que você iniciou com cartões de estatísticas para Total de Migrações, Concluídas, Em Andamento e Falhas, além dos botões **Iniciar Nova Migração**, **Ver Logs** e **Mapeamento de Campos**. Migrações só podem ser criadas pelo assistente.

## Plataformas suportadas

Spwig se conecta diretamente a três plataformas, além de arquivos CSV simples:

- **WooCommerce** — o caminho mais completo; dados de extensões (assinaturas, pacotes, cartões-presente, reservas) e seu programa de afiliados também podem ser transferidos.
- **Shopify** — conecta-se por meio de um aplicativo personalizado que você cria no painel de desenvolvedor do Shopify.
- **Magento 2** — conecta-se por meio de um token de integração do seu painel de administração do Magento.
- **Arquivos CSV** — cinco arquivos separados (produtos, categorias, clientes, pedidos, avaliações), para outras plataformas ou dados preparados manualmente.

> **Nota:** BigCommerce, PrestaShop, Squarespace e Wix não são suportados como conexões diretas. Se você estiver migrando de uma dessas plataformas, exporte seu catálogo e dados de clientes para CSV e use a rota CSV em vez disso — veja [Importação a partir de Arquivos CSV](csv-import).

## O que é transferido, por plataforma

A cobertura varia por plataforma — verifique esta tabela contra sua própria loja antes de comprometer uma data de lançamento.

| Dados | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Categorias | Sim, com hierarquia | Sim, como Coleções (planas) | Sim | Sim |
| Produtos | Sim | Sim | Sim | Sim (arquivo obrigatório) |
| Imagens de produtos | Sim | Sim | Sim | Não |
| Variantes | Sim | Sim | Sim | Não |
| Clientes + endereços | Sim | Sim | Sim | Sim |
| Pedidos | Sim | Sim, apenas os últimos 60 dias, a menos que o escopo `read_all_orders` seja adicionado | Sim | Sim |
| Avaliações | Sim | Não suportado de forma alguma | Normalmente indisponível — o Magento Community não tem um ponto de extremidade REST para avaliações | Sim |
| Cupons / descontos | Sim | Sim | Sim | Não |
| Blog / conteúdo do CMS | Sim (posts, categorias, tags, imagens) | Sim (artigos) | Sim (páginas do CMS) | Não |
| Afiliados, comissões, pagamentos | Sim, requer o plugin Spwig Migration Bridge | Não | Não | Não |
| Detecção de campos personalizados | Sim | Não — os metafields do Shopify não são lidos | Não | n/a |

Mercadores do Shopify devem planejar reentrar manualmente quaisquer dados de metafield (especificações personalizadas de produtos, campos adicionais de clientes) após a importação, pois eles não são detectados ou transferidos. Para tudo o mais, veja [Mapeamento de Campos de Migração](migration-field-mapping) para ver como os campos de origem se mapeiam para os campos do Spwig.

## Planejamento da sua migração

- **Migre antes de ir ao ar**, contra uma instalação do Spwig que ainda não está lidando com tráfego real, antes de apontar o DNS do seu domínio para ela — dessa forma, você pode revisar e corrigir coisas sem que os clientes vejam um catálogo incompleto.
- **Mantenha sua loja antiga em execução, somente leitura**, até que você tenha verificado que a cópia do Spwig está correta.
- **Planeje tempo para a configuração de impostos e envio depois** — as configurações do assistente para isso parecem importar suas taxas e zonas, mas elas não são aplicadas (veja [Mapeamento de Campos de Migração](migration-field-mapping)). Configure **Configurações > Impostos e Moeda** e **Configurações > Envio** manualmente.
- **Faça verificações pontuais em vez de apenas dar uma olhada rápida** — os dados de extensão são importados com o melhor esforço possível; um produto cujos dados de extensão não puderam ser lidos ainda será criado, apenas sem eles. Veja [Após sua migração](after-migration-review) antes de anunciar algo aos clientes.

- **Acesso de administrador à sua plataforma de origem** para criar credenciais de API — uma chave de API REST no WooCommerce, um aplicativo personalizado no Shopify ou um token de integração no Magento.

Não necessário para CSV.
- **Escopos de leitura somente** onde a plataforma de origem os oferecer — o Spwig lê apenas da sua loja antiga, nunca escreve de volta nela.
- **Um orçamento de tempo** — cada execução tem um limite rígido de 4 horas.

Para uma loja grande, planeje uma abordagem em fases (categorias e produtos primeiro, pedidos depois) em vez de uma única passada.

> **Importante:** O Spwig não criptografa as credenciais de API que você insere no assistente. Uma vez verificada a conclusão da migração, revogue ou exclua a credencial na plataforma de origem.

## O assistente de migração, passo a passo

O assistente tem seis etapas, com o progresso salvo entre elas:

1. **Plataforma** — escolha WooCommerce, Shopify, Magento ou Importação CSV.
2. **Conexão** — insira as credenciais, com a opção (ativada por padrão) de testar a conexão primeiro. Os guias específicos da plataforma cobrem exatamente o que gerar.
3. **Pré-visualização** — contagens em tempo real da sua loja de origem, uma amostra dos primeiros 5 produtos, e caixas de seleção para quais tipos de dados incluir, além de opções como tamanho do lote.
4. **Mapeamento** — como os campos da origem mapeiam para os campos do Spwig, quaisquer campos personalizados do WooCommerce e categorias sem um correspondente óbvio. Detalhes completos em [Migration Field Mapping](migration-field-mapping).
5. **Importação** — executa em segundo plano; você pode fechar a guia e ela continua, com um log em tempo real.
6. **Concluído** — um resumo dos resultados, uma ferramenta de reescrita de links para conteúdo que referencia seu antigo domínio, e downloads de relatórios em PDF/CSV.

## Após sua migração

Uma importação bem-sucedida não é a linha de chegada — veja [After Your Migration](after-migration-review) para uma lista completa de verificação que abrange a verificação de dados, a correção de links internos que ainda apontam para seu antigo domínio e a configuração de impostos e envio que o assistente não lida por você.

## O rollback não é uma rede de segurança

Entenda isso antes de começar, e não depois que algo sair errado. O rollback existe, mas não é o botão de desfazer que parece ser:

- Não há rollback automático se uma importação falhar parcialmente. O que foi importado antes da falha permanece na sua loja, e uma importação falhada não pode ser revertida pelo administrador — você precisará revisar e limpar os dados parciais manualmente.
- Uma migração concluída pode ser revertida, e o rollback remove apenas o que a importação em si criou — nunca mais do que isso. Um cliente migrado que fez um pedido real após a importação mantém sua conta, endereços, histórico de fidelidade e crédito da loja, e esse pedido real permanece inalterado; apenas os pedidos criados pela importação são removidos. Um produto migrado ainda referenciado por qualquer pedido, pacote, cartão-presente ou slot de configurador também é mantido, e pedidos pertencentes a outros clientes nunca são modificados.
- Afiliados, comissões e pagamentos criados pela importação são removidos, assim como qualquer conta de afiliado que a importação criou — um afiliado vinculado a um cliente que já existia mantém sua conta, e apenas o registro do afiliado é removido. Planos de assinatura, níveis de preço e recursos de reserva criados por extensões da loja ainda não são removidos — limpe-os manualmente.
- Antes de confirmar, o Spwig mostra uma pré-visualização exata do que será removido e do que será mantido, por nome e contagem, com o motivo — calculada com base nos seus dados em tempo real. Leia-a antes de confirmar. Depois disso, o rollback é executado em segundo plano, então é seguro fechar a guia; verifique o resumo da migração para o relatório assim que ele terminar.
- O rollback ainda é uma ação permanente e destrutiva sobre as linhas que remove, então use-o com intenção — e limpe manualmente qualquer coisa que o Spwig mantenha e que você não queira. Mas como ele não vai mais além do que a importação criou, não é mais uma ferramenta de uso exclusivo do mesmo dia como costumava ser.
- O botão Rollback permanece disponível no resumo de uma migração concluída enquanto o registro da tarefa existir, e é oferecido novamente se uma tentativa de rollback falhar parcialmente, para que você possa tentar novamente. Os registros não são removidos em nenhum cronograma, então isso não expira por conta própria.

Se você encontrar uma migração com falha ou travada, [Migration Troubleshooting](migration-troubleshooting) aborda a nova tentativa, o cancelamento e a leitura dos logs.

## Dicas

- **Comece com uma execução de teste pequena** — categorias mais um punhado de produtos confirma que o mapeamento de campos parece certo antes do catálogo completo.
- **Leia primeiro o guia específico da plataforma** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify) e [Migrating from Magento](migrate-from-magento) cobrem exatamente quais credenciais e escopos você precisa.
- **Não pule a matriz de capacidades acima** — saber sobre revisões do Shopify ou variantes CSV não virão à tona salva uma surpresa depois que você tiver mudado o DNS.
- **Mantenha o painel de administração da sua plataforma de origem aberto em outra guia** para gerar ou copiar credenciais conforme você avança.
- **Trate os checkboxes do assistente literalmente** — se um ajuste não for descrito como funcionando aqui, configure-o diretamente no Spwig em vez de confiar no assistente.