---
title: Disponibilidade por região
---

A disponibilidade por região controla quais de suas Regiões de Vendas um produto pode ser vendido, e como os compradores fora dessas regiões experimentam seu catálogo. Use-o quando um produto estiver licenciado apenas para certos países, quando o estoque estiver reservado para um mercado local ou quando você estiver lançando um novo produto região por região.

Isso se baseia nas **Regiões de Vendas**, que agrupam países em mercados nomeados (consulte o guia de Regiões de Vendas para configurá-las). Assim que suas regiões existirem, você poderá restringir produtos individuais a elas e decidir como os produtos restritos aparecem para os compradores que não podem comprá-los.

## Restringindo um produto a regiões específicas

Todo produto possui uma configuração de **Disponibilidade por região** em sua página de edição. Abra **Produtos > Todos os Produtos**, selecione um produto e localize-o na seção **Status**, ao lado de **Status**, **Destacado** e **Esconder da Loja**.

![A seção de Status do formulário de edição do produto, com a opção Disponibilidade por região definida como "Apenas nas regiões selecionadas" ao lado de Destacado e Esconder da Loja](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Opção | O que significa |
|--------|------------------|
| **Disponível em todas as regiões** | Nenhuma restrição. O produto é vendido em todos os lugares. Este é o padrão para cada produto. |
| **Apenas nas regiões selecionadas** | Uma lista de permissões. O produto é vendido apenas nas regiões que você selecionar abaixo — em todos os outros lugares, ele é tratado como não disponível. |
| **Todas as regiões, exceto as selecionadas** | Uma lista de bloqueio. O produto é vendido em todos os lugares *exceto* as regiões que você selecionar abaixo. |

### Escolhendo as regiões

Logo abaixo da seção Status, uma tabela intitulada **Disponibilidade por região (regiões selecionadas)** lista as regiões às quais o modo acima se aplica.

1. Defina **Disponibilidade por região** como **Apenas nas regiões selecionadas** ou **Todas as regiões, exceto as selecionadas**.
2. Na tabela **Disponibilidade por região (regiões selecionadas)**, clique em **Adicionar outra Região** e escolha uma Região de Vendas.
3. Repita para cada região que quiser adicionar.
4. Clique em **Salvar**.

![A tabela **Disponibilidade por região (regiões selecionadas)** com as linhas Norte-Americano e Europa adicionadas](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Se **Disponibilidade por região** estiver definida como **Disponível em todas as regiões**, tudo que houver nessa tabela será ignorado — limpe primeiro o menu suspenso da regra se quiser remover uma restrição sem excluir as linhas.

Para uma visão geral do catálogo de todos os produtos nas regras de região em uma lista (útil ao auditar muitos produtos de uma vez), acesse **Visibilidade de Região de Produto** em `/admin/catalog/productregionvisibility/`.

## Mostrando aos compradores onde o produto não é entregue

Quando a região do comprador não corresponder às regras de disponibilidade do produto, você controla o que eles veem em **Configurações de Exibição de Estoque**, na seção **Disponibilidade por região**. Esta página ainda não tem um atalho de barra lateral — abra-a diretamente em `/admin/catalog/stockdisplaysettings/`.

![Configurações de Exibição de Estoque, seção Disponibilidade por região — o menu suspenso de exibição de região, definido como "Mostrar, marcado como indisponível"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Opção | O que os compradores veem |
|--------|---------------------------|
| **Mostrar, marcado como indisponível** (padrão) | O produto ainda aparece nas listagens, com um selo "Indisponível" e uma notificação "Não é entregue para [região]" no lugar do botão "Adicionar ao Carrinho". Um banner também aparece no topo das páginas de listagem ("Alguns produtos não são entregues para [destino]") com um link para filtrar apenas os itens que são entregues lá. |
| **Esconder das listagens** | O produto é removido das listagens e resultados de busca para os compradores dessa região. |

![Lista de produtos da loja com envio para a Europa — o banner "Alguns produtos não são entregues para a Europa" acima da grade e um cartão de produto marcado como "Indisponível" com uma notificação "Não é entregue para a Europa"](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

A página de um produto restrito sempre exibe uma notificação "Este produto não é enviado para [região]" quando uma compradora chega a ela diretamente (por exemplo, a partir de um link compartilhado ou resultado de mecanismo de busca) — isso se aplica independentemente da opção de lista que você escolher acima, pois um link direto ignora totalmente a lista.

## Permitindo que os clientes escolham ou descubram sua região

O Spwig pode detectar a região de uma compradora automaticamente e oferecer uma alternância, e você pode adicionar um seletor para que as compradoras possam alterá-lo a qualquer momento.

### Antes de começar

Você precisa configurar duas coisas para que a detecção e a troca de região funcionem corretamente:

1. **Regiões de Vendas** — os países em cada região e a moeda padrão de cada região. Se você não vir **Regiões de Vendas** sob **Estoque** na barra lateral, ative **Habilitar Múltiplos Armazéns** sob **Configurações > Configurações da Loja > Comércio Eletrônico** para revelar o link do menu (você não precisa realmente usar múltiplos armazéns — esse recurso apenas libera o item do menu). Você também pode ir diretamente para `/admin/catalog/salesregion/`.
2. **Países de Envio** — os países para os quais sua loja realmente envia. Eles geralmente já estão em vigor: todo país que você adicionar a uma Zona de Envio é automaticamente adicionado aqui também. Para revisar ou ajustar manualmente a lista, abra diretamente `/admin/shipping/shippingcountry/` (também não possui um link de barra lateral yet).

### A confirmação automática de região

O Spwig detecta a região de uma compradora com base em sua localização e a aplica automaticamente. Quando isso os coloca em uma região *diferente* do mercado primário (padrão) da sua loja — e você tiver duas ou mais Regiões de Vendas ativas — o Spwig exibe uma confirmação na primeira visita para que saibam em qual região estão e possam alterá-la:

> **Definimos sua região como [Região]**
> Escolhemos isso com base na sua localização para que você veja os produtos e preços certos. Não está certo? Escolha seu país.
> Enviar para: [seletor de país]  **[Continuar navegando]**

![O modal de confirmação "Definimos sua região como América do Norte" na loja, com um seletor de país "Enviar para" e um botão "Continuar navegando"](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Escolher um país diferente no seletor os muda imediatamente. Fechar ou clicar em **Continuar navegando** mantém sua região atual, e eles não serão perguntados novamente nesse navegador. Visitantes que já estão na região padrão da sua loja nem mesmo recebem a confirmação.

### Adicionando um seletor de envio ao seu cabeçalho ou rodapé

Se quiser que os clientes alterem a região por conta própria a qualquer momento (em vez de depender apenas do aviso automático), adicione o widget **Seletor de Envio** ao seu cabeçalho ou rodapé.

1. Navegue até **Design > Construtor de Cabeçalho** (ou **Construtor de Rodapé**).
2. Arraste o widget **Seletor de Envio** da Biblioteca de Widgets para uma linha.
3. Clique em **Salvar**.

![A biblioteca de widgets do Construtor de Cabeçalho com o grupo Comprar destacado, mostrando o widget Seletor de Envio juntamente com Carrinho de Compras, Menu de Conta e Seletor de Idioma](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

O widget não precisa de configuração — ele lista automaticamente os Países de Envio ativos, e exibe a seleção atual da compradora (ou o país detectado pelo GeoIP, se ela ainda não tiver escolhido um). Escolher um país diferente atualiza imediatamente sua região e recarrega a disponibilidade e os preços dos produtos da página.

O Seletor de Envio ainda não tem um formulário de configuração dedicado. Se quiser alterar o estilo do botão (outline, sólido ou fantasma) ou ocultar o rótulo "Enviar para", abra as configurações do widget no construtor e edite diretamente o campo **Configuração Personalizada (JSON)**, usando `button_style` e `show_label`.

### Moeda segue região

Se sua loja oferecer mais de uma moeda (definida sob **Configurações > Múltiplas Moedas**), alternar de região — seja pelo aviso ou pelo Seletor de Envio — também altera a moeda exibida para a moeda padrão dessa região.

Se sua loja tiver apenas uma moeda, ou não tiver ativado explicitamente uma segunda, a moeda permanece inalterada quando o cliente muda de região.

## Dicas

- Deixe **Disponibilidade por região** como **Disponível em todas as regiões**, a menos que você tenha um motivo específico para restringir um produto: é a opção mais simples e não exige manutenção conforme você adicionar mais regiões.
- Use **Apenas em regiões selecionadas** para uma lista de permissões pequena (por exemplo, um produto que será lançado em um único país primeiro) e **Todas as regiões, exceto as selecionadas** para uma lista de bloqueio pequena (por exemplo, em todos os lugares, exceto um país onde o item não tem licença) — escolha a que exigir menos linhas para configurar.
- Se os clientes relatam que um produto está faltando, mas deveria estar visível, verifique o recurso **Disponibilidade por região** do produto e se o país deles está coberto por uma **Região de Vendas** ativa e um **País de Envio** ativo.
- **Esconder das listagens** mantém seu catálogo com aparência limpa para os clientes que não podem comprar certos itens, mas também significa que merchandising e busca parecerão mais vazios nesses regiões — **Mostrar, marcado como indisponível** é geralmente melhor, se você quiser que os clientes ainda possam navegar pelo catálogo completo, mesmo onde não puderem finalizar a compra.
- Teste o comportamento das regiões adicionando o Seletor de Endereço de Entrega ao cabeçalho e alternando entre países você mesmo antes de depender da detecção de GeoIP durante um lançamento.
- Defina os valores de prioridade das suas regiões de forma deliberada — a região com maior prioridade ativa é o padrão para os clientes cujo país não puder ser detectado ou não corresponder a nenhuma região.