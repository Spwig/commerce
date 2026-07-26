---
title: Importando de Arquivos CSV
---

O importe de CSV é a rota de migração de fallback para qualquer loja que o Spwig não conecte diretamente. Se você vem do BigCommerce, PrestaShop, Squarespace, Wix, uma planilha que você mantém manualmente ou um sistema personalizado sem uma API que o Spwig entenda, este é o lugar em que você chega — exporte seus dados para arquivos CSV e carregue-os aqui em vez de se conectar ao vivo.

Este guia abrange quando usar CSV em vez de uma conexão de API, o que ele não pode trazer consigo, os cinco arquivos envolvidos, como prepará-los e como funciona o mapeamento de colunas.

## Quando Usar CSV em vez de uma Conexão de API

O Spwig se conecta diretamente ao WooCommerce, Shopify e Magento 2/Adobe Commerce — veja [Visão Geral da Migração de Dados](migration-overview) para esses. Para qualquer outra plataforma, o CSV é sua única opção; não há integração direta para BigCommerce, PrestaShop, Squarespace ou Wix. Também é a escolha certa se você estiver consolidando dados de uma planilha, encerrando uma loja personalizada ou quiser controlar exatamente o que será importado curando os arquivos por conta própria.

## O que o CSV Não Pode Fazer

Antes de preparar qualquer coisa, saiba o que essa rota deixa para trás — este é o maior motivo de surpresa para comerciantes que usam o importe CSV:

- **Nenhuma imagem de produto.** Os produtos são importados sem imagens anexadas; carregue-as depois.
- **Nenhuma variante.** Cada produto é criado como um produto simples. Reconstrua as estruturas de tamanho, cor e estilo no Spwig após a importação.
- **Nenhum cupom.** Códigos de desconto e promoções não fazem parte do formato CSV.
- **Nenhume conteúdo do blog.** Não há um arquivo CSV para posts ou artigos.

Nenhuma dessas coisas bloqueia a importação — apenas significa que os produtos precisarão de trabalho pós-importação uma vez que estiverem no Spwig. Veja [Após Sua Migração](after-migration-review) para a lista completa de verificação pós-importação.

## Os Cinco Arquivos

A etapa CSV do assistente oferece cinco entradas de arquivo, cada uma com um botão **Baixar Modelo**. Comece com esses modelos em vez de construir os arquivos do zero — eles garantem os nomes de coluna certos e permitem que a detecção automática faça mais do trabalho na etapa 4.

| Arquivo | Necessário? |
|---|---|
| Produtos | **Necessário** |
| Categorias | Opcional |
| Clientes | Opcional |
| Pedidos | Opcional |
| Avaliações | Opcional |

O único arquivo que o Spwig insiste é o de Produtos — os demais podem ser deixados vazios se você ainda não tiver esses dados.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Etapa 2 com CSV selecionado, mostrando as cinco entradas de arquivo e seus botões de Baixar Modelo
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Produtos (Necessário)

| Coluna | Descrição |
|---|---|
| `id` | Identificador único em seus dados de origem; não mostrado aos clientes. |
| `name` | O título do produto. **Essencial.** |
| `slug` | Versão amigável para URL do nome; gerado automaticamente a partir de `name` se estiver em branco. |
| `description` | A descrição mostrada no site de vendas. |
| `price` | O preço regular do produto. **Essencial.** |
| `sku` | Unidade de estoque — usada para correspondência quando **Pular itens existentes** está ativado. |
| `stock_quantity` | Unidades atualmente em estoque. |
| `category` | Nome da categoria a que este produto pertence. Deve corresponder a um `name` em seu arquivo de categorias. |

### Categorias

| Coluna | Descrição |
|---|---|
| `id` | Identificador único em seus dados de origem. |
| `name` | O nome da categoria. **Essencial.** |
| `slug` | Versão amigável para URL do nome; gerado automaticamente se estiver em branco. |
| `description` | Texto da descrição da categoria. |
| `parent_id` | O `id` da categoria pai. Em branco significa nível superior. |

### Clientes

| Coluna | Descrição |
|---|---|
| `id` | Identificador único em seus dados de origem. |
| `email` | Endereço de e-mail do cliente. **Essencial** — vincula pedidos e avaliações ao cliente certo. |
| `first_name` | Primeiro nome do cliente. |
| `last_name` | Último nome do cliente. |
| `phone` | Número de telefone do cliente. |

### Pedidos


| Coluna | Descrição |
|---|---|
| `id` | Identificador único em seus dados de origem. |
| `customer_email` | Email do cliente que realizou o pedido. **Essencial** — vincula o pedido ao registro do cliente. |
| `order_date` | A data em que o pedido foi feito. |
| `status` | O status do pedido (ex. concluído, em processamento). |
| `total` | O total do pedido. **Essencial.** |
| `currency` | Código da moeda para o total do pedido. |

### Avaliações (Opcional)

| Coluna | Descrição |
|---|---|
| `id` | Identificador único em seus dados de origem. |
| `product_id` | O `id` do produto que está sendo avaliado, correspondendo ao seu arquivo de produtos. **Essencial** — vincula a avaliação ao produto correto. |
| `customer_email` | Endereço de email do avaliador. |
| `rating` | A classificação em estrelas dada. |
| `comment` | O texto da avaliação. |
| `date` | A data em que a avaliação foi postada. |

## Preparando Seus Arquivos

- **Salve como UTF-8** para evitar caracteres acentuados corrompidos, especialmente de uma codificação de origem diferente.
- **Cite campos que contêm vírgulas** — envolva uma descrição ou nome que contenha uma vírgula em aspas duplas para que não seja mal interpretado como uma quebra de coluna.
- **Inclua uma linha de cabeçalho.** A primeira linha deve conter seus nomes de coluna — um arquivo sem linha de cabeçalho é rejeitado.
- **Construa a hierarquia de categorias com `parent_id`.** Dê a cada categoria um `id` único, depois defina o `parent_id` de uma subcategoria como o `id` de sua categoria pai. Em branco significa nível superior.
- **Vincule pedidos a clientes com `customer_email`**, correspondendo à coluna `email` em seu arquivo de clientes (ou um registro de cliente convidado será criado), em vez de depender de números de ID internos, que raramente coincidem entre plataformas.
- **Vincule avaliações a produtos com `product_id`**, correspondendo a um valor na coluna `id` de seu arquivo de produtos, ou essa avaliação será ignorada.

## Mapeando Colunas no Passo 4

O passo 4 mostra um painel de Mapeamento de Coluna CSV. O Spwig escaneia seus cabeçalhos e detecta automaticamente correspondências prováveis contra uma lista de aliases comuns — por exemplo, um campo `sku` também corresponde a `barcode`, `part_number` ou `item_number`. Cabeçalhos exportados diretamente de outra plataforma geralmente mapeiam corretamente sem nenhum trabalho manual.

Para cada coluna, você pode aceitar a suposição detectada automaticamente, substituí-la escolhendo um campo de destino diferente ou escolher "— Ignorar esta coluna —" para excluí-la. Os mapeamentos são salvos e reutilizados em futuras migrações CSV. Veja [Mapeamento de Campo de Migração](migration-field-mapping) para uma visão completa do passo 4, incluindo mapeamentos de campos automáticos, mapeamento de categorias e as opções de impostos/envio.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Painel de Mapeamento de Coluna CSV do passo 4 mostrando mapeamentos detectados automaticamente com menus suspensos para substituição
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Erros Comuns e O Que Eles Significam

| Erro | Significado |
|---|---|
| `Products CSV is required.` | Você tentou prosseguir sem carregar um arquivo de produtos. É o único arquivo que o Spwig exige — carregue um para continuar. |
| `{Type} CSV has no headers.` | A primeira linha do arquivo nomeado está vazia ou ausente. Adicione uma linha de cabeçalho com os nomes das colunas e reenvie-o. |
| `{Type} CSV could not be read: ...` | O Spwig não conseguiu analisar o arquivo nomeado — geralmente um arquivo corrompido, codificação incorreta ou um arquivo que não é realmente CSV apesar de sua extensão. Reexporte-o e confirme que ele abre limpo antes de carregá-lo novamente. |

## Executando a Importação

Uma vez confirmado o mapeamento, inicie a migração a partir do passo 5. Ele é executado em segundo plano, então você pode fechar a janela — o progresso e um log em tempo real estão disponíveis se você verificar de volta antes que ele termine. Veja [Depois de Sua Migração](after-migration-review) para verificar os resultados.

Lembre-se de que a importação CSV especificamente deixa **imagens de produto** e **variações** para você finalizar manualmente — nenhuma delas vem automaticamente, independentemente de quão completos seus arquivos foram.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- **Comece com o botão Baixar Modelo para cada arquivo** — isso evita que você perca tempo corrigindo erros de digitação em nomes de colunas que, de outra forma, passariam despercebidos até a etapa de mapeamento manual.
- **Corrija as discrepâncias de `product_id` antes de carregar as avaliações** — uma avaliação cujo `product_id` não corresponde a nenhum `id` de produto não tem para onde se anexar e será ignorada.
- **Não renomeie os cabeçalhos de uma exportação de outra plataforma** — a detecção automática muitas vezes reconhece-os como estão, por meio de aliases, então o mapeamento pode não exigir nenhuma intervenção manual.
- **Reserve tempo para imagens e variantes logo após a importação** — essas são as duas coisas que o CSV nunca traz consigo, e é fácil esquecê-las até que um cliente perceba uma página de produto sem imagem.
- **Use `parent_id` para modelar categorias em níveis múltiplos** — aponte o `parent_id` de uma subcategoria para o `id` de sua categoria pai para aninhá-la; deixe-o em branco para categorias de nível superior.
- **Re-exportar e re-verificar em caso de erro "could not be read"** — quase sempre é um problema de codificação ou corrupção no arquivo de origem, e não algo que precise ser corrigido no Spwig.