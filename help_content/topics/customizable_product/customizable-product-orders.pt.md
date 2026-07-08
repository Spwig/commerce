---
title: Atendendo Pedidos de Produtos Personalizáveis
---

Quando um cliente cria um produto e coloca um pedido, seu design é congelado e armazenado junto com o pedido. Este guia explica como os designs personalizados fluem ao longo do ciclo de vida do pedido e como acessar os arquivos prontos para impressão que você precisa para o atendimento.

## Ciclo de vida do design

O design do cliente passa por várias etapas desde a criação até o atendimento:

### 1. Criação do design

O cliente usa o editor visual no site para criar seu design. Enquanto trabalham, seu progresso é salvo automaticamente no navegador. Clientes registrados também podem salvar designs em sua conta para edição posterior.

### 2. Rascunho do design

Quando o cliente clica em **Adicionar ao Carrinho**, o estado atual do design é salvo como um **rascunho de design**. O rascunho inclui:

- O estado completo do canvas para cada superfície (posições dos elementos, conteúdo de texto, imagens carregadas, clipart, estilização)
- Uma quebra de custos mostrando todas as taxas de design aplicáveis
- Pré-visualizações em miniatura de cada superfície

O rascunho é vinculado ao item do carrinho por meio de um token único. Isso garante que o design exato criado pelo cliente seja preservado, mesmo que ele continue comprando antes de finalizar o pedido.

**Expiração do rascunho:** Os rascunhos de design expiram automaticamente após 7 dias, se o cliente não completar o pedido. Isso evita o acúmulo de designs abandonados.

### 3. Captura do design

Quando o cliente finaliza o checkout e o pedido é colocado, o rascunho de design é convertido em uma **captura de design imutável**. Esta é o registro permanente do design:

- A captura não pode ser modificada pelo cliente após a compra
- Ela contém os mesmos dados de design que o rascunho
- Ela está permanentemente vinculada ao item específico do pedido

Essa imutabilidade é importante — garante que o que o cliente pediu seja exatamente o que você produz e envia, sem possibilidade de alterações após o pagamento.

### 4. Renderização dos arquivos de atendimento

Após o pedido ser colocado, o sistema gera automaticamente **arquivos de atendimento em alta resolução** para cada superfície do design. Esses são imagens compostas que combinam todos os elementos do design (texto, imagens, clipart) em um único arquivo pronto para impressão, na DPI configurada para cada superfície.

A renderização acontece assincronamente em segundo plano. Para a maioria dos designs, a renderização é concluída em alguns segundos. O status **Renderizado** da captura indica se os arquivos de atendimento estão prontos.

## Acessando dados de design nos pedidos

### Página de detalhes do pedido

Quando você visualiza um pedido que contém produtos personalizáveis no painel de administração:

1. Navegue até **Pedidos > Todos os Pedidos**
2. Abra o pedido que contém o produto personalizado
3. O item do pedido para o produto personalizado mostra as informações do design, incluindo pré-visualizações das superfícies e um link para a captura do design

### Lista de capturas de design

Você também pode navegar por todas as capturas de design diretamente:

1. Navegue até **Produtos Personalizáveis > Capturas de Design**
2. A lista mostra todas as capturas vinculadas a itens de pedido
3. Clique em uma captura para visualizar os dados de design completos, imagens renderizadas e arquivos de atendimento

Cada captura mostra:

| Campo | Descrição |
|-------|-------------|
| **Item do Pedido** | Link para o item do pedido associado |
| **Dados do Design** | O estado completo do canvas (JSON) |
| **Imagens Renderizadas** | Miniaturas de pré-visualização por superfície |
| **Arquivos de Atendimento** | Arquivos compostos em alta resolução para impressão |
| **Renderizado** | Se a renderização está concluída |
| **Renderizado em** | Carimbo de tempo de quando os arquivos foram gerados |

## Baixando arquivos de atendimento

Os arquivos de atendimento são os que você envia ao seu provedor de impressão ou usa em seu processo de produção.

**Para um pedido de camiseta personalizada:**
- Baixe o arquivo da superfície **Frente** (ex.: PNG composto de 300 DPI)
- Baixe o arquivo da superfície **Costas**
- Baixe o arquivo da superfície **Mangas** (se projetado)
- Envie todos os arquivos ao seu impressor de tela ou impressora DTG (direct-to-garment)

**Para um pedido personalizado de pôster:**
- Baixe o arquivo de superfície **Front** única em resolução de impressão
- O arquivo inclui área de sangria se a sangria foi configurada para a superfície
- Envie para sua impressora de pôster/cartão

Cada arquivo é uma imagem composta única contendo todos os elementos de design mesclados, renderizados na DPI que você configurou para essa superfície.

## Designs salvos

Clientes registrados podem salvar seus designs em sua conta para edição posterior. Como comerciante, você pode visualizar esses designs salvos em uma lista somente leitura:

1. Navegue até **Produtos Personalizáveis > Designs Salvos**
2. A lista mostra todos os designs salvos pelos clientes com o nome do cliente, produto, nome do design e data

Os designs salvos são:
- **Proprietários do cliente** — Pertencem à conta do cliente
- **Somente leitura para comerciantes** — Você pode visualizar, mas não modificar
- **Separados dos pedidos** — Um design salvo só se torna um pedido quando o cliente adiciona-o ao carrinho e finaliza a compra
- **Reutilizáveis** — Os clientes podem carregar um design salvo, modificá-lo e pedir várias vezes

## Fluxo de atendimento

### Fluxo padrão

1. **Receber pedido** — O pedido aparece em sua lista de pedidos com os itens personalizados
2. **Verificar renderização** — Verifique se a captura do design mostra **Renderizado: Sim**. Se a renderização ainda não estiver concluída, espere alguns minutos e atualize
3. **Baixar arquivos** — Baixe o arquivo de atendimento para cada superfície projetada
4. **Revisar qualidade** — Abra os arquivos e verifique se o design atende aos seus padrões de qualidade de impressão (verifique a DPI, a posição dos elementos e a legibilidade do texto)
5. **Enviar para produção** — Encaminhe os arquivos para seu provedor de impressão ou equipe de produção
6. **Enviar e concluir** — Após a produção, envie o produto e marque o pedido como concluído

### Exemplo de atendimento de camiseta

1. Pedido recebido: "Camiseta de Equipe Personalizada" com designs na frente e na costas
2. Abrir pedido → visualizar captura do design
3. Baixar `front.png` (300 DPI, 300x400mm) e `back.png` (300 DPI, 300x400mm)
4. Envie ambos os arquivos para sua impressora DTG com a cor da peça e tamanho selecionados no variantes do pedido
5. Após a impressão e verificação de qualidade, envie para o cliente

### Exemplo de atendimento de pôster

1. Pedido recebido: "Pôster A4 Personalizado" com uma única superfície projetada
2. Abrir pedido → visualizar captura do design
3. Baixar `front.png` (300 DPI, 210x297mm com 3mm de sangria)
4. Envie para seu serviço de impressão de pôster
5. Após a impressão e corte, envie para o cliente

## Solução de problemas

**Problema:** A captura do design mostra "Renderizado: Não" e a renderização ainda não foi concluída

- **Causa:** A tarefa de renderização em segundo plano pode ter falhado ou ainda está em processamento
- **Solução:** Espere alguns minutos. Se a renderização não for concluída, verifique os logs da tarefa em segundo plano. Você também pode visualizar os dados do design diretamente na captura para confirmar que o design do cliente foi preservado

**Problema:** O arquivo de atendimento parece de menor qualidade do que o esperado

- **Causa:** O cliente pode ter carregado imagens de baixa resolução
- **Solução:** Verifique as configurações de DPI da superfície. Se foram configuradas alertas de DPI mínima, o cliente teria sido alertado durante o processo de design. Para futuros produtos, considere aumentar o requisito de DPI mínimo

**Problema:** O cliente solicita uma alteração em seu design após o pedido

- **Solução:** As capturas de design são imutáveis por design. Se o cliente precisar de alterações, ele deve fazer um novo pedido com o design atualizado. Se você concordar em fazer uma exceção, o cliente pode usar seu design salvo (se ele salvou um) como ponto de partida para um novo pedido

## Dicas

- Sempre verifique se a renderização está concluída antes de iniciar a produção.

Verifique o campo **Renderizado** na captura do design.
- Mantenha as configurações de DPI apropriadas para seu método de impressão.

DPI mais alto produz melhor qualidade, mas arquivos maiores. 300 DPI é padrão para a maioria dos produtos de impressão profissional.
- Incentive os clientes a salvarem seus designs antes de fazerem o pedido.

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.


Se houver um problema na produção e o pedido precisar ser remanufaturado, o design salvo torna o reordenamento direto.
- Crie um buffer no cronograma de produção para produtos personalizados.

Diferente dos produtos padrão, cada item requer tratamento de arquivo individual.
- Se você processar volumes altos de pedidos personalizados, considere automatizar o passo de download de arquivos integrando-se com a API do seu provedor de impressão.