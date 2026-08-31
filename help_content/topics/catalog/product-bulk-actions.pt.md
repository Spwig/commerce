---
title: Ações em Lote para Produtos
---

A lista de **Produtos** permite que você atue em muitos produtos de uma vez, em vez de abrir cada um individualmente. A partir do menu suspenso **Ações em Lote** na barra de ferramentas acima da grade de produtos, você pode publicar ou não publicar produtos, destacá-los ou removê-los da destaque, exportar dados para CSV, verificar quais produtos estão prontos para envio internacional ou excluí-los — tudo em um único passo.

Navegue até **Produtos > Todos os Produtos** para usar essas ações.

![A barra de ferramentas da lista de produtos com três cartões de produto selecionados e o menu suspenso Ações em Lote mostrando todas as opções, incluindo Exportar Dados de Alfândega (CSV) e Verificar Prontidão para Envio Internacional](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Executando uma Ação em Lote

1. Use o painel de filtros ou a caixa de **Pesquisa** para reduzir os produtos que você deseja, se necessário
2. Marque a caixa no canto superior esquerdo de cada cartão de produto que você deseja incluir — a barra de **Ações em Lote** mostra uma contagem em tempo real de quantos produtos estão selecionados
3. Escolha uma ação do menu suspenso **Ações em Lote**
4. Clique em **Aplicar**

Ações que alteram ou exportam dados são executadas imediatamente; **Excluir Selecionados** pede confirmação primeiro, pois é a única ação aqui que não é facilmente desfeita a partir da própria lista.

## Ações Disponíveis

| Ação | O que ela faz |
|--------|---------------|
| **Marcar como Publicado** | Define o status dos produtos selecionados como Publicado, tornando-os visíveis na loja. |
| **Marcar como Rascunho** | Define o status dos produtos selecionados como Rascunho, ocultando-os da loja enquanto você continua editando. |
| **Marcar como Destaque** | Ativa **É Destaque** nos produtos selecionados. |
| **Remover Destaque** | Desativa **É Destaque** nos produtos selecionados. |
| **Exportar para CSV** | Baixa um CSV dos IDs, nomes, SKU, status, sinalizador de destaque e preço dos produtos selecionados. |
| **Exportar Dados de Alfândega (CSV)** | Baixa um CSV das informações de alfândega para os produtos selecionados. Consulte abaixo. |
| **Verificar Prontidão para Envio Internacional** | Mostra um resumo de quais produtos selecionados possuem os dados de alfândega necessários para envios internacionais. Consulte abaixo. |
| **Excluir Selecionados** | Move os produtos selecionados para o lixo, após uma confirmação. |

## Exportar Dados de Alfândega (CSV)

Use isso quando você precisar de uma folha de declaração de alfândega para entregar a um transportador, correios ou corretor de alfândega — por exemplo, antes de um grande envio internacional, ou ao configurar um novo transportador que pede códigos HS e dados de origem no início.

Selecione os produtos, escolha **Exportar Dados de Alfândega (CSV)** no menu suspenso e clique em **Aplicar**. O Spwig baixa um arquivo chamado `product_customs_data.csv` com uma linha por produto e essas colunas:

| Coluna | Fonte |
|--------|--------|
| **SKU** | O SKU do produto |
| **Nome** | O nome do produto |
| **Código HS** | O código de classificação do Sistema Harmonizado |
| **País de Origem** | Onde o produto é fabricado |
| **Preço Unitário de Alfândega** | O valor declarado por unidade para alfândega |
| **Licença de Exportação** | O número da licença de exportação, se o produto precisar de uma |
| **Data de Validade da Licença** | A data de expiração da licença de exportação, se definida |
| **Pronto para Internacionais** | `Sim` ou `Não` — se o produto possui os dados mínimos necessários para envio internacional (consulte abaixo) |

Esses campos vêm da seção **Envio Internacional / Alfândega** do formulário do produto. Se um produto estiver faltando um deles, sua coluna ficará em branco na exportação — preencha os dados em falta no produto antes de confiar nesse arquivo para um envio real.

## Verificar Prontidão para Envio Internacional

Use isso para audituar um lote de produtos antes de começar a enviá-los internacionalmente, sem abrir cada produto individualmente ou esperar por uma exportação completa em CSV.

Selecione os produtos, escolha **Verificar Prontidão para Envio Internacional** e clique em **Aplicar**. O Spwig verifica cada produto selecionado contra três campos obrigatórios — **Código HS**, **País de Origem** e **Preço Unitário de Alfândega** — e exibe uma notificação resumindo o resultado:

- Se todos os produtos selecionados tiverem os três campos preenchidos, você verá uma confirmação de que todos estão prontos.
- Se alguns estiverem com dados faltando, a notificação relata quantos estão prontos e quantos não estão, e lista cada produto que não está pronto junto com os campos que faltam (por exemplo, "Caneca de Cerâmica Azul (faltando: hs_code, country_of_origin)").

Se mais de 10 produtos estiverem com dados faltando, a notificação lista os primeiros 10 e informa quantos mais existem.

Esta ação apenas lê dados — ela não altera nada nos produtos, portanto, é seguro executá-la quantas vezes você quiser enquanto preenche as informações de alfândega em todo o seu catálogo.

**Export License Number** e **Export License Expiry** não fazem parte da verificação de prontidão. Eles se aplicam apenas a itens controlados ou restritos, portanto, um produto pode estar "pronto" para envio internacional sem eles.

## Dicas

- Execute **Check International Shipping Readiness** em todo o seu catálogo (ou categoria por categoria) antes do seu primeiro pedido internacional — é muito mais rápido do que descobrir um código HS faltando quando a remessa já está na fronteira.
- Mantenha o **Export Customs Data (CSV)** para entregar a corretores e transportadoras, e o **Check International Shipping Readiness** para sua própria lista de verificação interna — o CSV é um registro, a verificação de prontidão é uma lista de tarefas.
- Preencha **HS Code**, **Country of Origin** e **Customs Unit Price** no formulário do produto (em **International Shipping / Customs**) à medida que adiciona novos produtos, para que você não precise fazer isso em massa depois.
- A grade de produtos carrega mais produtos automaticamente conforme você rola a página (rolagem infinita), e suas seleções de caixa de seleção são mantidas à medida que novos produtos são carregados — assim, você pode rolar para construir uma seleção grande antes de aplicar uma ação. No entanto, alterar um filtro ou recarregar a página limpa sua seleção, portanto, aplique a ação antes de ajustar os filtros.
- **Mark as Draft** é uma forma rápida de remover vários produtos da vitrine de uma vez — por exemplo, antes de uma contagem de estoque — sem alterar nada mais sobre eles.