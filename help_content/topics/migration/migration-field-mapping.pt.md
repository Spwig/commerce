---
title: Mapeamento de Campos de Migração
---

Cada plataforma nomeia as coisas um pouco de forma diferente — o `regular_price` do WooCommerce não é o `price` do Shopify, e uma coluna CSV chamada `barcode` pode ser exatamente a mesma coisa que o Spwig espera ver rotulada como `sku`. A etapa 4 do assistente de migração, **Configurar Mapeamento de Campos**, é onde você verifica como os seus dados de origem serão mapeados no Spwig antes que a importação realmente execute. Este tópico aborda cada bloco dessa página e se aplica às migrações de WooCommerce, Shopify, Magento e CSV, com diferenças de plataforma destacadas onde elas importam. Para credenciais e as etapas anteriores do assistente, consulte [Migrando do WooCommerce](migrate-from-woocommerce) ou o guia equivalente para sua plataforma.

## Mapeamentos Automáticos

Este bloco mostra, para cada tipo de dado que você selecionou na etapa 3, uma lista somente leitura de campos de origem e o campo Spwig em que cada um cai — por exemplo, o `name` de um produto mapeado para o título do produto do Spwig, ou o `email` de um cliente mapeado para o e-mail da conta. Apenas os tipos de dados que você está realmente importando aparecem aqui; se você não selecionou Avaliações na etapa 3, não haverá uma seção de Avaliações nesta página.

Como essas linhas são somente leitura, não há nada para configurar — elas existem para que você possa verificar o mapeamento antes de comprometer-se com a importação. Se um mapeamento parecer errado para seus dados, não há como substituí-lo nesta tela; suas opções são corrigir os dados de origem antes da migração ou corrigir os registros afetados no Spwig após a importação ser concluída.

## Mapeamento de Colunas CSV

Este bloco aparece apenas para migrações CSV, com uma tabela por arquivo que você carregou. O Spwig detecta automaticamente correspondências prováveis com base nos cabeçalhos das suas colunas — por exemplo, um mapeamento `sku` também reconhece cabeçalhos como `barcode`, `part_number` ou `item_number` — então, na maioria dos casos, você não precisará tocar nada aqui.

Cada coluna CSV recebe um menu suspenso listando os campos que o Spwig espera para esse tipo de arquivo:

- **produtos** — `id, name, slug, description, price, sku, stock_quantity, category`
- **categorias** — `id, name, slug, description, parent_id`
- **clientes** — `id, email, first_name, last_name, phone`
- **pedidos** — `id, customer_email, order_date, status, total, currency`
- **avaliações** — `id, product_id, customer_email, rating, comment, date`

Cada menu suspenso também inclui **— Pular esta coluna —**, o que exclui totalmente essa coluna da importação. Substitua o mapeamento detectado automaticamente quando seu cabeçalho usar uma convenção de nomenclatura que o Spwig não reconheceu, ou quando uma coluna realmente não corresponder a nada que o Spwig importa (um campo de nota interna, por exemplo) — escolha Pular em vez de forçá-la para o campo disponível mais próximo.

## Campos Personalizados

Este bloco é exclusivo do WooCommerce. O Spwig coleta 10 produtos, clientes e pedidos da sua loja e lista quaisquer campos meta personalizados que encontrar além dos campos padrão do WooCommerce, juntamente com o tipo detectado e um valor de exemplo.

Para cada campo, escolha onde ele deve ser mapeado:

- **Mapear para** — Campo Personalizado 1, 2 ou 3 para produtos (Campo Personalizado 1 ou 2 para clientes e pedidos), ou **Meta Dados (JSON)** como uma opção geral se você tiver mais campos personalizados do que os espaços numerados, ou deixe-o como **— Pular este campo —**.
- **Transformar** — como o valor deve ser convertido ao ser importado: Como Texto, Como Número (Inteiro), Como Decimal, Como Verdadeiro/Falso (Booleano), Como JSON, Como Data, Como URL ou Como E-mail.

> **Nota:** Os metafields do Shopify não são detectados por este recurso de forma alguma — as migrações do Shopify nunca mostram um bloco de Campos Personalizados, independentemente de quanta informação de metafield sua loja tiver. Se você depender de metafields do Shopify para especificações de produtos, atributos de clientes ou semelhantes, planeje-se para reentrar esses dados manualmente no Spwig após a importação.

Se o Spwig não detectar nenhum campo personalizado em sua amostra, você verá uma mensagem de confirmação em vez deste bloco, e não haverá mais nada para configurar.

Quando algumas de suas categorias de origem não têm uma correspondência óbvia no Spwig, este bloco oferece três opções: **Criar novas categorias**, **Atribuir à categoria padrão** (uma categoria "Não categorizado" de uso geral) ou **Pular itens com categorias não mapeadas**.

> **Nota:** Independentemente da opção que você escolher aqui, o Spwig cria automaticamente uma categoria correspondente para qualquer produto que tenha dados de categoria de origem, e só recorre para "Não categorizado" para produtos que não têm nenhuma informação de categoria. Você não precisa se preocupar muito com essa escolha — se, no final, você tiver categorias que não deseja, é mais rápido mesclá-las ou excluí-las em **Catálogo > Categorias** após a importação do que depender desse ajuste.

## Configurações de impostos, envio e preço

O último bloco, **Configurações de Imposto e Envio**, possui três controles: **Importar configurações de imposto**, **Importar zonas e métodos de envio** e um tipo e valor de **Ajuste de Preço**.

Os dois checkboxes não afetam a importação no momento — nenhuma taxa de imposto ou zona de envio vem do seu antigo plataforma, independentemente de como elas estão configuradas. Configure-as diretamente no Spwig após a importação: taxas de imposto em **Configurações > Imposto e Moeda**, zonas e métodos de envio em **Configurações > Envio**.

**Ajuste de Preço** se comporta de forma diferente dependendo da sua plataforma de origem:

- **Migrações de WooCommerce, CSV e Shopify** — este controle funciona conforme descrito. Escolha **Percentual** ou **Valor Fixo**, insira um valor (por exemplo, `10` para um aumento de 10%, ou `-5` para uma redução de $5), e o preço base de cada produto é ajustado por esse valor durante a importação. Ele se aplica apenas ao preço base — preços de promoção/preço de comparação vêm sem ajustes.
- **Migrações de Magento** — o mesmo controle aparece na página, mas não tem efeito; os preços do Magento são importados sem alteração, independentemente do que você insira. Se você precisar de uma alteração geral de preço em uma migração de Magento, aplique-a depois usando as ferramentas de ajuste de preço em lote do catálogo do Spwig, em vez desse campo.

> **Aviso:** Se você estiver migrando do WooCommerce, CSV ou Shopify e não quiser que os preços sejam alterados, deixe **Ajuste de Preço** definido como **Nenhum**. É o único controle nesta página que realmente altera seus dados, e é fácil assumir — incorretamente — que ele se comporta da mesma forma que os checkboxes de imposto e envio logo acima.

## Mapeamentos são salvos para a próxima vez

O que você configurar nesta página é salvo com o trabalho de migração, e o Spwig o reutiliza como seu ponto de partida para futuras migrações da mesma plataforma — útil se você estiver executando uma migração em fases (categorias e produtos primeiro, pedidos depois) ou precisar reimportar após corrigir um problema de dados. Você também pode revisitar e ajustar os mapeamentos salvos após a conclusão de uma migração, usando o botão **Mapeamento de Campos** no painel de migração, sem precisar executar novamente todo o assistente.

## Dicas

- **Verifique o bloco de Mapeamentos Automáticos mesmo que você não possa editá-lo** — capturar um mapeamento errado antes de clicar em Iniciar Importação é muito mais barato do que corrigir centenas de registros importados depois.
- **Renomeie cabeçalhos ambíguos do CSV antes de carregar** se a detecção automática não os reconheceu, em vez de tentar forçar um campo mal correspondido através do menu suspenso.
- **Use Metadados (JSON) como seu overflow de campos personalizados** — é o único alvo de mapeamento que não atinge um limite após dois ou três campos.
- **Não dependa desta página para impostos, envio ou (no Magento) preços** — trate esses como uma tarefa de configuração manual imediatamente após a importação, e não algo que o assistente lida por você.
- **Deixe o Ajuste de Preço como Nenhum na sua primeira execução de uma nova migração**, depois use um lote de teste pequeno para confirmar a matemática antes de aplicá-lo ao seu catálogo completo.