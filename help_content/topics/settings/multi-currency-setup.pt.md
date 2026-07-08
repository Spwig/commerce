---
title: Configuração de Moedas Múltiplas
---

A opção de moedas múltiplas permite que seus clientes naveguem pelos produtos e completem o checkout na moeda de sua preferência. Os preços são convertidos automaticamente a partir da sua moeda base usando taxas de câmbio de um provedor conectado ou taxas definidas manualmente.

## Antes de começar

Antes de ativar a opção de moedas múltiplas, você precisa:

1. **De um provedor de taxas de câmbio ativo** - Vá para **Configurações > Guia de Moedas Múltiplas > Painel de Taxas de Câmbio** e conecte pelo menos um provedor (como Open Exchange Rates, Fixer.io ou ExchangeRate-API). O provedor deve estar ativo e sincronizando as taxas.
2. **Pelo menos duas moedas** - Sua moeda base mais uma ou mais moedas adicionais que deseja suportar.

## Ativar moedas múltiplas

Navegue até **Configurações > Moedas Múltiplas** e marque **Ativar Moedas Múltiplas**. Após ativada, configure as seguintes opções:

| Configuração | Descrição |
|---------|-------------|
| **Modo de Seleção de Moeda** | Como os clientes escolhem sua moeda. *Automático* detecta a partir de seu local, *Manual* permite que eles escolham a partir de um seletor, *Ambos* combina as duas abordagens. |
| **Mostrar Seletor de Moeda** | Exibir um seletor de moeda em sua loja virtual para que os clientes possam mudar a moeda manualmente. |
| **Posição do Seletor** | Onde o seletor de moeda aparece (cabeçalho, rodapé ou barra lateral). |
| **Mostrar Informação de Taxa de Câmbio** | Exibir uma notificação aos clientes informando que os preços são conversões aproximadas a partir da sua moeda base. |
| **Ativar Formatação de Localização** | Formatar números e símbolos de moeda de acordo com a localização de cada cliente (ex.: 1.234,56 para formatos europeus). |

## Modo de checkout

Escolha como a opção de moedas múltiplas funciona no checkout:

| Modo | Descrição |
|------|-------------|
| **Multi-Moeda Completo** | Os clientes navegam, adicionam itens ao carrinho e pagam na moeda selecionada. A taxa de câmbio é bloqueada no checkout e registrada com o pedido. Este é o modo padrão. |
| **Apenas Exibição** | Os preços são exibidos na moeda do cliente para conveniência, mas o carrinho e o pagamento são sempre processados em sua moeda base. No checkout, os clientes veem uma notificação mostrando o valor aproximado convertido ao lado do valor real cobrado em sua moeda base. |

**Apenas Exibição** é útil quando seu provedor de pagamento só suporta sua moeda base, ou quando deseja evitar totalmente o risco de taxa de câmbio. Os clientes ainda veem preços localizados enquanto navegam, dando-lhes uma noção de custo em sua própria moeda.

## Intervalo de sincronização de taxas de câmbio

Controle com que frequência sua loja busca taxas de câmbio atualizadas do seu provedor conectado:

| Intervalo | Descrição |
|----------|-------------|
| **Em tempo real** | A cada 15 minutos. Ideal para lojas com vendas internacionais de alto volume. |
| **Horário** | Uma vez por hora. Boa combinação entre frescor e uso da API. |
| **Diário** | Uma vez por dia. Adequado para a maioria das lojas. Este é o padrão. |
| **Semanal** | Uma vez por semana. Para lojas com preços estáveis. |
| **Mensal / Trimestral** | Atualizações menos frequentes para lojas que raramente alteram as taxas. |
| **Apenas Manual** | As taxas nunca são buscadas automaticamente. Você gerencia todas as taxas manualmente. |

O intervalo de sincronização afeta com que frequência a tarefa de fundo busca taxas do seu provedor. Entre as sincronizações, taxas armazenadas em cache são usadas. Se você precisar forçar uma sincronização imediata, use o botão **Sincronizar Agora** no Painel de Taxas de Câmbio ou **Sincronizar do Provedor** na página de Taxas de Câmbio Manual.

## Taxas de câmbio manuais

As taxas de câmbio manuais permitem que você defina taxas de conversão exatas para pares específicos de moedas. Elas têm prioridade sobre as taxas obtidas do provedor, dando a você controle total sobre os preços.

Navegue até **Taxas de Câmbio > Taxas de Câmbio Manuais** para gerenciá-las.

### Definindo taxas manualmente

Clique em **Adicionar Taxa** para criar uma taxa para um par de moedas. Especifique a moeda base, a moeda de destino e a taxa. Por exemplo, definir USD/EUR para 0,92 significa que 1 USD = 0,92 EUR.

### Sincronizando com um provedor

Clique em **Sincronizar do Provedor** para popular automaticamente as taxas manuais com as taxas mais recentes do seu provedor conectado.

Isso cria taxas manuais para todas as moedas suportadas, fornecendo um ponto de partida para ajustes finos.

Taxas bloqueadas são ignoradas durante a sincronização, então quaisquer taxas que você tenha ajustado manualmente não serão substituídas.

### Bloqueio de taxas

Clique no ícone de bloqueio em qualquer taxa para impedir que ela seja substituída durante a sincronização do provedor. Isso é útil quando você negocia uma taxa específica ou deseja manter uma taxa fixa, independentemente das flutuações do mercado.

- **Taxas bloqueadas** mostram um distintivo de bloqueio e são excluídas da sincronização automática.
- **Taxas desbloqueadas** podem ser atualizadas quando você clicar em Sincronizar do Provedor.

### Comparação de provedores

Cada taxa manual exibe a taxa atual do provedor ao lado dela, com uma diferença percentual. Isso ajuda você a ver, de um olhar, como suas taxas manuais se comparam às taxas do mercado:

- Uma **porcentagem verde** significa que sua taxa é maior que a taxa do provedor.
- Uma **porcentagem vermelha** significa que sua taxa é menor que a taxa do provedor.

## Markup de taxa de câmbio

Você pode adicionar um markup percentual às taxas de câmbio para cobrir taxas de conversão de moeda e proteger contra flutuações de taxa entre o momento em que um cliente faz um pedido e quando você recebe o pagamento.

Por exemplo, um markup de 2% em uma taxa de câmbio USD/EUR de 1,18 ajustaria isso para aproximadamente 1,20 USD/EUR. Esse pequeno buffer ajuda a garantir que você não perca dinheiro em conversões de moeda.

## Estratégia de seleção de taxas

Quando você tem vários provedores de taxas de câmbio conectados, você pode escolher como as taxas são selecionadas:

- **Provedor principal** - Sempre usa as taxas do seu provedor principal designado. Isso garante preços consistentes em toda a sua loja. Se o provedor principal não tiver dados para um par de moedas, ele recorrerá à taxa mais recente disponível de qualquer provedor.
- **Mais recente disponível** - Usa a taxa mais recentemente sincronizada de qualquer provedor ativo. Isso fornece os dados mais recentes, mas as taxas podem variar ligeiramente entre os provedores.

Para a maioria das lojas, o **Provedor principal** é a escolha recomendada, pois fornece os preços mais previsíveis.

## Moedas suportadas

Use o gerenciador de moedas de arrastar e soltar para escolher quais moedas sua loja suporta:

1. **Moedas disponíveis** (coluna da esquerda) mostra todas as moedas que você pode habilitar.
2. **Moedas ativas** (coluna da direita) mostra as moedas atualmente habilitadas em sua loja.
3. Arraste moedas entre as colunas para habilitar ou desabilitar.
4. Arraste dentro da coluna Ativa para reordenar como as moedas aparecem no seletor.
5. Clique em **Salvar Configuração de Moeda** para aplicar suas alterações.

Sua moeda base está sempre ativa e não pode ser removida.

## Como as taxas de câmbio são resolvidas

Quando um preço precisa ser convertido, o sistema verifica as taxas nesta ordem:

1. **Taxa de câmbio manual** - Se uma taxa manual ativa existir para o par de moedas, ela sempre será usada primeiro.
2. **Taxa do provedor** - Se nenhuma taxa manual existir, a taxa mais recente do seu provedor conectado será usada.

Isso significa que você pode usar provedores para a maioria das moedas e substituir pares específicos com taxas manuais onde você precisa de controle preciso.

## Importante: Esta configuração é permanente

Uma vez que o multi-câmbio estiver habilitado e os clientes fizerem pedidos em moedas estrangeiras, esta configuração **não pode ser desativada**. Isso é porque:

- Pedidos armazenam permanentemente a moeda escolhida pelo cliente e a taxa de câmbio usada no momento da compra.
- Relatórios financeiros e cálculos de reembolso dependem desses dados históricos de moeda.
- Desativar o multi-câmbio deixaria pedidos existentes em um estado inconsistente.

Se nenhum pedido foi feito em moedas estrangeiras, você ainda pode desativar o multi-câmbio.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- **Teste com um pedido pequeno primeiro** - Faça um pedido de teste em uma moeda estrangeira para verificar o fluxo de checkout e garantir que as taxas de câmbio sejam aplicadas corretamente.
- **Monitore as taxas de câmbio regularmente** - Verifique o Painel de Taxas de Câmbio periodicamente para garantir que seu provedor esteja sincronizando as taxas e que elas pareçam razoáveis.
- **Considere uma margem para moedas voláteis** - Se você suportar moedas com alta volatilidade, uma margem ligeiramente maior (2-3%) pode proteger seus margens.
- **Comece com moedas principais** - Comece com moedas amplamente utilizadas (EUR, GBP, JPY, CAD, AUD) e expanda com base na demanda dos clientes.
- **Revise a compatibilidade com provedores de pagamento** - Nem todos os provedores de pagamento suportam todas as moedas.

Verifique a documentação do seu provedor de pagamento para confirmar quais moedas eles processam.
- **Use o modo de exibição apenas se estiver em dúvida** - Se você não tiver certeza se seu provedor de pagamento lida com checkout multimoeda, comece com o modo de exibição apenas.

Você pode mudar para o modo Multimoeda Completo depois.
- **Bloqueie as taxas antes de períodos promocionais** - Se você estiver realizando uma promoção, bloqueie suas taxas de câmbio com antecedência para garantir preços consistentes durante a promoção.