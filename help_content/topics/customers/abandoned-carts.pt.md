---
title: Carrinhos Abandonados
---

Um carrinho abandonado é criado quando um cliente autenticado adiciona itens ao seu carrinho, mas não completa o checkout dentro de 24 horas. O Spwig rastreia automaticamente esses carrinhos para que você possa entender a receita perdida, identificar padrões de por que os clientes saem e tomar ações para recuperar vendas.

Navegue até **Clientes > Carrinhos Abandonados** para visualizar todas as abandonamentos registrados.

## O que você pode ver na lista de carrinhos abandonados

A visão de lista mostra cada carrinho abandonado com as seguintes informações em visão geral:

| Coluna | Descrição |
|---|---|
| **Cliente** | O nome e o e-mail do cliente |
| **Abandonado em** | Data e hora em que o carrinho foi marcado como abandonado |
| **Valor Total** | O valor monetário dos itens no carrinho no momento do abandono |
| **Total de Itens** | Número de itens no carrinho |
| **Motivo Estimado** | A melhor estimativa do Spwig sobre o motivo do abandono |
| **Status de Recuperação** | Se esse carrinho foi recuperado (transformado em um pedido concluído) |
| **Dias desde o Abandono** | Quanto tempo atrás o carrinho foi abandonado |

### Filtros de carrinhos abandonados

Use os filtros do lado direito para estreitar a lista:

- **Motivo Estimado** — filtre pelo motivo do abandono (ex: mostrar apenas carrinhos onde o motivo estimado foi custo de envio alto)
- **Recuperado** — filtre para mostrar apenas carrinhos recuperados ou não recuperados
- **Abandonado em** — filtre por intervalo de data para focar em abandonamentos recentes ou em um período específico de campanha

## Entendendo os motivos de abandono

O Spwig registra um motivo estimado para cada abandono. Esses motivos são baseados em sinais capturados durante o processo de checkout e não são garantidos para serem exatos, mas eles fornecem um ponto de partida útil para diagnosticar padrões de desistência.

| Motivo | O que pode indicar |
|---|---|
| **Desconhecido** | Nenhum sinal específico foi capturado — o motivo mais comum |
| **Custo de Envio Alto** | O cliente pode ter sido desencorajado pelo custo de envio mostrado no checkout |
| **Total Muito Alto** | O total geral do pedido pode ter sido mais alto do que o esperado |
| **Problemas no Checkout** | O cliente encontrou um problema durante o processo de checkout |
| **Pagamento Falhou** | Uma tentativa de pagamento foi feita, mas falhou |
| **Comparação de Preços** | O cliente provavelmente visitou para comparar preços |
| **Salvo para Mais Tarde** | O cliente salvou intencionalmente itens para uma visita futura |

Se você notar uma proporção grande de carrinhos com o mesmo motivo — por exemplo, um agrupamento significativo de abandonamentos com motivo "Custo de Envio Alto" — esse é um sinal que vale a pena investigar nas configurações de envio ou na apresentação do checkout.

## Visualizando um carrinho abandonado individual

Clique em qualquer linha da lista para abrir a visão detalhada. Você verá:

- **Detalhes do Abandono** — o cliente, a referência do carrinho, quando foi abandonado e o motivo estimado
- **Resumo do Carrinho** — o número de itens e o valor total no momento do abandono
- **Rastreamento de Recuperação** — se o carrinho foi recuperado, quando foi recuperado e qual pedido ele se converteu

O campo **Carrinho** vincula-se diretamente ao registro do carrinho subjacente, então você pode ver exatamente quais produtos estavam no carrinho.

## Fluxo de trabalho de recuperação

O Spwig rastreia se cada carrinho abandonado eventualmente se converte em um pedido concluído. Quando um cliente retorna e completa uma compra a partir de um carrinho abandonado, o registro é automaticamente marcado como **Recuperado** e o pedido resultante é vinculado.

O contador **E-mails de Recuperação Enviados** mostra quantos e-mails de recuperação automatizados foram enviados ao cliente para esse carrinho. Isso ajuda você a entender se suas campanhas de e-mail estão incentivando os clientes a retornarem.

### Ações de recuperação manual

A visão de carrinhos abandonados é somente leitura — é um registro do que aconteceu, não uma ferramenta para editar o conteúdo do carrinho. Para agir sobre carrinhos abandonados:

1.

Anote o endereço de e-mail do cliente a partir do registro do carrinho abandonado
2.

Use seu sistema de e-mail ou ferramentas de marketing para enviar uma mensagem personalizada
3.

Considere anexar um código de cupom para dar ao cliente um incentivo para concluir a compra
4.

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

Monitore o status **Recuperado** nos dias seguintes para ver se a abordagem teve efeito

## Analisando tendências de abandono de carrinho

Analise a lista de carrinhos abandonados regularmente como um check-up de saúde do seu processo de checkout:

- Um aumento súbito no abandono pode indicar um problema técnico com o checkout ou pagamento
- Valores de carrinho consistentemente altos em carrinhos não recuperados representam seu segmento de recuperação com maior oportunidade
- Compare a proporção de carrinhos recuperados em relação aos não recuperados ao longo do tempo para medir a eficácia dos seus e-mails de recuperação

A seção **Análise do Cliente** de cada perfil de cliente também mostra a taxa pessoal de abandono de carrinho, então você pode identificar clientes que frequentemente adicionam itens ao carrinho, mas raramente concluem uma compra.

## Dicas

- Ordene por **Valor Total** (do maior para o menor) para identificar os carrinhos de maior valor que merecem prioridade para abordagem pessoal
- Use o filtro **Abandonado em** para revisar abandons de uma campanha ou período promocional específico — um pico durante uma venda flash pode significar que sua promoção atraiu navegadores em vez de compradores
- Combine os dados de carrinhos abandonados com campanhas de cupons: envie um código de desconto com prazo limitado para clientes com carrinhos de alto valor que ainda não foram recuperados para criar urgência
- Um carrinho abandonado há mais de 7 dias é improvável que se recupere sozinho — se os e-mails de recuperação estiverem ativados, esses são os carrinhos que precisam de mais atenção
- Clientes anônimos não aparecem na lista de carrinhos abandonados — esse rastreamento se aplica apenas a clientes com contas registradas