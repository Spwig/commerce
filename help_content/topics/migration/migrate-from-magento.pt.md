---
title: Migrando do Magento
---

Spwig pode importar seu catálogo, clientes, pedidos, cupons e páginas do CMS diretamente de uma loja Magento 2 ou Adobe Commerce em execução usando a API REST do Magento. Este guia passa por gerar as credenciais de integração que o Magento exige, executar o assistente de migração e a única lacuna significativa que comerciantes vindo do Magento precisam planejar: avaliações de produtos.

Apenas **Magento 2 e Adobe Commerce** são suportados. O Magento 1 chegou ao fim de sua vida útil há anos e não expõe a API REST em que esta migração depende — se você ainda estiver no Magento 1, use [Importando de Arquivos CSV](csv-import) em vez disso.

## Antes de Começar

Revise [Visão Geral da Migração de Dados](migration-overview) para orientação geral de planejamento. Para o Magento especificamente:

- **Categorias** — importadas com sua hierarquia intacta.
- **Produtos** — importados, incluindo imagens.
- **Clientes e endereços** — importados.
- **Pedidos** — importados.
- **Cupons** — importados como vouchers do Spwig, provenientes das regras de vendas do Magento.
- **Páginas do CMS** — importadas como páginas do Spwig.
- **Avaliações** — normalmente **não** importadas. Veja a próxima seção antes de depender disso.
- Variantes são suportadas para produtos configuráveis.

> **Nota:** Migrações do Magento não carregam programas de afiliados, comissões ou pagamentos — a integração do Spwig com a ponte de afiliados só está disponível para lojas WooCommerce.

### A Limitação das Avaliações

A edição comunitária do Magento não expõe um endpoint REST para avaliações de produtos — a rota `/reviews` simplesmente não existe em uma instalação comunitária padrão. O Spwig verifica se ela está disponível antes da importação e, se não estiver, registra uma mensagem e continua com o restante da sua migração em vez de falhar toda a tarefa. Suas categorias, produtos, clientes, pedidos, cupons e páginas ainda serão transferidas; apenas as avaliações são ignoradas.

Avaliações **serão** importadas se sua loja estiver rodando **Adobe Commerce** (que expõe esse endpoint) ou se sua instalação do Magento tiver um módulo personalizado adicionando uma rota de avaliações compatível.

Se você estiver no Magento Community e precisar que suas avaliações sejam importadas para o Spwig, exporte-as separadamente (a maioria das extensões de avaliação oferece uma exportação CSV) e importe-as depois usando o arquivo de avaliações em [Importando de Arquivos CSV](csv-import), vinculado aos seus produtos por `product_id`.

## Etapa 1: Escolher o Magento

A partir do painel de migração em **Importação e Exportação de Dados**, clique em **Iniciar Nova Migração** e selecione **Magento** como sua plataforma.

## Etapa 2: Conectar-se à Sua Loja

Você precisará da URL da sua loja Magento e de um token de acesso de integração. O admin do Magento não fornece um simples token de API da forma que algumas plataformas fazem — você cria uma **Integração**, que é uma credencial com escopo que o Magento trata como um aplicativo conectado.

### Criando um Token de Acesso de Integração

1. No admin do Magento, vá para **Sistema > Integrações**.
2. Clique em **Adicionar Nova Integração**.
3. Defina o nome como `Spwig Migration` para que seja fácil de identificar depois.
4. Abra a guia **API** e defina **Acesso a Recursos** para **Tudo**.
5. Clique em **Salvar**, depois em **Ativar**.
6. Confirme clicando em **Permitir** na janela pop-up que lista as permissões sendo concedidas.
7. Copie o token de acesso mostrado após a ativação — o Magento exibe-o apenas uma vez.

> **Nota:** O Acesso a Recursos é definido como **Tudo** porque a árvore de recursos do Magento é muito granular — centenas de permissões individuais cobrindo catálogo, vendas, clientes e CMS — sem um único interruptor "ler tudo" além de selecionar todos eles. A migração apenas lê da sua loja; ela nunca escreve de volta, e você pode revogar a integração uma vez que sua migração for verificada (coberta no final deste guia).

De volta ao assistente do Spwig, insira sua **URL da Loja** e o **Token de Acesso** que copiou. Deixe **Testar a conexão antes de prosseguir** marcado (ativado por padrão) para que o Spwig verifique se pode acessar e autenticar com sua loja antes de você prosseguir. Se o teste falhar, verifique novamente a URL e se a integração ainda está Ativa no Magento. Clique em **Próximo**.

screenshots-needed

heading

## Passo 3: Revisar o que será importado

paragraph

O Spwig consulta sua loja Magento e mostra contagens em tempo real para cada tipo de dado que encontrou: categorias, produtos, clientes, pedidos, cupons (originados de regras de venda) e páginas CMS. Cada tipo tem uma caixa de seleção, automaticamente marcada quando o Spwig encontrar itens para importar e desativada quando a contagem for zero.

paragraph

Você também verá uma amostra dos primeiros cinco produtos para que possa verificar se os títulos, preços e imagens parecem corretos antes de comprometer-se com a importação completa.

paragraph

Abaixo das contagens, **Opções de Importação** permitem que você controle como a importação se comporta:

list

paragraph

Se você precisar alterar como campos específicos são mapeados — atributos personalizados, correspondência de categorias, tratamento de impostos ou envio — isso acontece no passo 4, abordado em [Mapeamento de Campos de Migração](migration-field-mapping). Clique em **Próximo** para prosseguir com o mapeamento, depois em **Iniciar Migração** uma vez que você tenha revisado.

heading

## Executando a Importação

paragraph

A importação é executada em segundo plano — você pode fechar a janela e ela continuará. A página de progresso mostra o status em tempo real para cada tipo de dado (categorias, produtos, clientes, pedidos, avaliações, cupons) com um log que você pode expandir para detalhes.

paragraph

Uma vez concluída, você será direcionado para a página de resumo dos resultados. Percorra [Após sua Migração](after-migration-review) para verificar o que foi transferido, lidar com qualquer reescrita de links para conteúdo que referenciava suas antigas URLs do Magento e cuidar da configuração de impostos e envio que o assistente coleta, mas não aplica automaticamente.

screenshots-needed

heading

## Prazo para Reversão

paragraph

Magento é a única plataforma onde a reversão tem um limite de tempo. Uma vez que sua migração seja concluída, o botão **Reversão** aparecerá na página de resumo do trabalho — mas, especificamente para o Magento, esse botão pode parar de ser oferecido após um período após a conclusão. Outros tipos de migração (WooCommerce, Shopify, CSV) não têm esse prazo, mas o Magento tem, então não adie a verificação para depois.

blockquote

paragraph

Verifique seus dados importados com urgência, enquanto a reversão ainda estiver disponível, caso precise dela.

heading

## Revogar a Integração

paragraph

Uma vez que você tenha verificado seus dados no Spwig — produtos, preços, imagens, clientes, pedidos, cupons e páginas parecem corretos — volte para **Sistema > Integrações** no Magento, localize `Spwig Migration` e desative ou exclua-a.

O token não será mais necessário, a menos que você planeje executar a migração novamente, e removê-lo encerra uma credencial de leitura aberta que você não precisa mais ter ativa.

## Dicas

- **As avaliações são a maior surpresa para comerciantes Magento** — planeje uma exportação/importação separada se estiver usando a edição Community e as avaliações forem importantes para sua loja.
- **Copie o token de acesso imediatamente** — o Magento exibe-o apenas uma vez, quando você ativa a integração; se você perder o token, será necessário desativar e recriar a integração.
- **Não adie a verificação** — o botão de Rollback está disponível por um período limitado no Magento especificamente, ao contrário de outras plataformas.
- **Use a pré-visualização de exemplo no passo 3** para identificar problemas óbvios de mapeamento (preços incorretos, imagens faltando) antes de executar a importação completa.
- **Os cupons vêm das regras de vendas** — se um cupom do Magento depender de condições complexas, verifique-o no Spwig depois, já que nem todo tipo de regra tem um equivalente direto.
- **Configure as taxas de imposto e as zonas de envio no Spwig após a importação** — as opções de imposto e envio do assistente são salvas, mas não são aplicadas automaticamente à sua loja.