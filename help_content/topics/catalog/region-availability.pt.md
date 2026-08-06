---
title: Disponibilidade por Região
---

A disponibilidade por região controla quais de suas Regiões de Vendas um produto pode ser vendido, e como os compradores fora dessas regiões experimentam seu catálogo. Use-o quando um produto estiver licenciado apenas para certos países, quando o estoque estiver reservado para um mercado local ou quando você estiver lançando um novo produto região por região.

Isso se baseia nas **Regiões de Vendas**, que agrupam países em mercados nomeados (consulte o guia Regiões de Vendas para configurá-las). Assim que suas regiões existirem, você poderá restringir produtos individuais a elas e decidir como os produtos restritos aparecem para os compradores que não podem comprá-los.

## Restringindo um produto a regiões específicas

Todo produto possui uma configuração de **Disponibilidade por Região** em sua página de edição. Abra **Produtos > Todos os Produtos**, selecione um produto e localize-o na seção **Status**, ao lado de **Status**, **Destacado** e **Esconder da Loja**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Página de edição do produto rolando até a seção de Status, com o campo de disponibilidade por região visível e definido como "Apenas nas regiões selecionadas"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Use um produto com pelo menos 2 regiões já selecionadas abaixo, se possível, para que a tabela inline tenha linhas visíveis na segunda imagem.
-->

| Opção | O que significa |
|--------|----------------|
| **Disponível em todas as regiões** | Nenhuma restrição. O produto é vendido em todos os lugares. Este é o padrão para cada produto. |
| **Apenas nas regiões selecionadas** | Uma lista de permissões. O produto é vendido apenas nas regiões que você selecionar abaixo — em todos os outros lugares, ele é tratado como não disponível. |
| **Todas as regiões, exceto as selecionadas** | Uma lista de bloqueio. O produto é vendido em todos os lugares *exceto* as regiões que você selecionar abaixo. |

### Escolhendo as regiões

Logo abaixo da seção Status, uma tabela com o título **Disponibilidade por Região (regiões selecionadas)** lista as regiões às quais o modo acima se aplica.

1. Defina **Disponibilidade por Região** como **Apenas nas regiões selecionadas** ou **Todas as regiões, exceto as selecionadas**.
2. Na tabela **Disponibilidade por Região (regiões selecionadas)**, clique em **Adicionar outra Região** e escolha uma Região de Vendas.
3. Repita para cada região que quiser adicionar.
4. Clique em **Salvar**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: A tabela "Disponibilidade por Região (regiões selecionadas)" com duas ou três linhas de região adicionadas
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Se **Disponibilidade por Região** estiver definida como **Disponível em todas as regiões**, tudo que houver nessa tabela será ignorado — limpe o campo de seleção primeiro se quiser remover uma restrição sem excluir as linhas.

Para uma visão em larga escala de todas as regras de região de cada produto em uma lista (útil ao auditar muitos produtos de uma vez), acesse **Visibilidade de Região do Produto** em `/admin/catalog/productregionvisibility/`.

## Mostrando aos compradores onde um produto não é entregue

Quando a região do comprador não corresponder às regras de disponibilidade do produto, você controla o que eles veem em **Configurações de Exibição do Estoque**, na seção **Disponibilidade por Região**. Esta página ainda não tem um atalho de barra lateral — abra-a diretamente em `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Formulário de alteração de Configurações de Exibição do Estoque rolando até o campo de **Disponibilidade por Região**, mostrando o campo de exibição por região
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Opção | O que os compradores veem |
|--------|-------------------|
| **Mostrar, marcado como indisponível** (padrão) | O produto ainda aparece nas listagens, com um selo "Indisponível" e uma notificação "Não envia para [região]" no lugar do botão "Adicionar ao Carrinho". Um banner também aparece no topo das páginas de listagem ("Alguns produtos não enviam para [destino]") com um link para filtrar apenas os itens que enviam para lá. |
| **Esconder das listagens** | O produto é removido das listagens e resultados de busca totalmente para compradores nessa região. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Lista de produtos da loja com o banner de região no topo e pelo menos um cartão de produto mostrando o selo "Indisponível" e a notificação "Não envia para [região]"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Exige uma seleção de envio para a região (ou detecção de GeoIP) que resolva para uma região em que um produto de demonstração esteja restrito.
-->

Um produto restrito sempre mostra uma notificação "Este produto não envia para [região]" quando um comprador chega diretamente nele (por exemplo, de um link compartilhado ou resultado de pesquisa) — isso se aplica independentemente de qual opção de listagem você escolher acima, pois um link direto ignora totalmente a listagem.

## Permitindo que os compradores escolham ou descubram sua região

O Spwig pode detectar a região de um comprador automaticamente e oferecer uma alternância, e você pode adicionar um seletor para que os compradores possam alterá-la a qualquer momento.

### Antes de começar

Você precisa de duas coisas configuradas para a detecção e troca de região funcionarem corretamente:

1. **Regiões de Vendas** — os países em cada região e a moeda padrão de cada região. Se você não vir **Regiões de Vendas** sob **Estoque** na barra lateral, ative **Habilitar Múltiplos Armazéns** sob **Configurações > Configurações da Loja > Comércio Eletrônico** para revelar o link do menu (você não precisa usar realmente múltiplos armazéns — esse recurso apenas libera o item do menu). Você também pode ir diretamente para `/admin/catalog/salesregion/`.
2. **Países de Envio** — os países para os quais sua loja realmente envia. Eles geralmente já estão em vigor: todo país que você adicionar a uma Zona de Envio é automaticamente adicionado aqui também. Para revisar ou ajustar manualmente a lista, abra diretamente `/admin/shipping/shippingcountry/` (também não possui um link na barra lateral yet).

### A confirmação automática da região

O Spwig detecta a região de um comprador a partir de sua localização e a aplica automaticamente. Quando isso os coloca em uma região *diferente* da sua loja padrão (mercado primário) — e você tiver duas ou mais Regiões de Vendas ativas — o Spwig exibe uma confirmação na primeira visita deles para que saibam em qual região estão e possam alterá-la:

> **Definimos sua região como [Região]**
> Selecionamos isso com base na sua localização para que você veja os produtos e preços certos. Não está certo? Escolha seu país.
> Enviar para: [seletor de país]  **[Continuar navegando]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: O modal "Definimos sua região como [Região]" na página inicial da loja, com o seletor de país e o botão Continuar navegando
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Exige GeoIP resolvendo para uma região não-padrão e pelo menos 2 Regiões de Vendas ativas para disparar. Localmente, defina o cookie "geo_country" para um país não-padrão para simular.
-->

Escolher um país diferente no seletor os muda imediatamente. Descartar o modal ou clicar em **[Continuar navegando]** mantém sua região atual, e eles não serão perguntados novamente nesse navegador. Visitantes que já estejam na região padrão da sua loja nem mesmo recebem a confirmação.

### Adicionando um Seletor de Enviar Para no seu cabeçalho ou rodapé

Se você quiser que os compradores alterem a região por conta própria a qualquer momento (em vez de depender apenas do aviso automático), adicione o widget **Seletor de Enviar Para** ao seu cabeçalho ou rodapé.

1.

Navegue até **Design > Construtor de Cabeçalho** (ou **Construtor de Rodapé**).
2.

Arraste o widget **Seletor de Endereço de Entrega** da Biblioteca de Widgets para uma linha.
3.

Clique em **Salvar**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Construtor de Cabeçalho com a barra lateral da Biblioteca de Widgets aberta e o widget Seletor de Endereço de Entrega visível/chamado
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

O widget não requer configuração — ele lista automaticamente os países de envio ativos e mostra a seleção atual do cliente (ou o país detectado pelo GeoIP, se o cliente ainda não tiver escolhido um). Selecionar um país diferente atualiza imediatamente a região e recarrega a disponibilidade e os preços dos produtos da página.

O Seletor de Endereço de Entrega ainda não possui um formulário de configuração dedicado. Se quiser alterar o estilo do botão (outline, sólido ou fantasma) ou ocultar o rótulo "Entregar para", abra as configurações do widget no construtor e edite diretamente o campo **Configuração Personalizada (JSON)**, usando `button_style` e `show_label`.

### Moeda segue a região

Se sua loja oferecer mais de uma moeda (definida em **Configurações > Múltiplas Moedas**), trocar de região — seja pelo prompt ou pelo Seletor de Endereço de Entrega — também muda a moeda exibida para a moeda padrão dessa região. Se sua loja tiver apenas uma moeda ou não tiver habilitado explicitamente uma segunda, a moeda permanecerá a mesma quando o cliente mudar de região.

## Dicas

- Deixe **Disponibilidade por região** como **Disponível em todas as regiões**, a menos que você tenha um motivo específico para restringir um produto — é a opção mais simples e não requer manutenção conforme você adicionar regiões no futuro.
- Use **Apenas nas regiões selecionadas** para uma lista de permissões pequena (por exemplo, um produto que será lançado em um país primeiro) e **Todas as regiões, exceto as selecionadas** para uma lista de bloqueio pequena (por exemplo, em todos os lugares, exceto em um país onde o item não tenha licença) — escolha a que exigir menos linhas para configurar.
- Se os clientes relatarem que um produto está faltando, mas deveria estar visível, verifique as configurações de **Disponibilidade por região** do produto e se o país deles está coberto por uma **Região de Vendas** ativa e um **País de Envio** ativo.
- **Esconder das listagens** mantém o catálogo com aparência limpa para os clientes que não conseguem comprar certos itens, mas também significa que merchandising e pesquisa parecerão mais vazios nesses regiões — **Mostrar, marcado como indisponível** é geralmente melhor, se você quiser que os clientes ainda possam navegar pelo catálogo completo, mesmo onde não puderem finalizar a compra.
- Teste o comportamento da região adicionando o Seletor de Endereço de Entrega ao cabeçalho e alternando entre países você mesmo antes de depender da detecção do GeoIP durante um lançamento.
- Defina os valores de prioridade das regiões de forma deliberada — a região ativa com maior prioridade é o fallback para os clientes cujo país não puder ser detectado ou não corresponder a nenhuma região.