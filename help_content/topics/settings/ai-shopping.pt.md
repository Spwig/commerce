---
title: Compras com IA
---

Compras com IA permitem que assistentes de compras com IA encontrem seus produtos e, quando você permitir, comprem em seu nome em sua loja. Ele está **desativado por padrão** — ativá-lo é uma escolha deliberada, e até que você o faça, sua loja não expõe nada a esses assistentes.

## Como ativá-lo

Abra **Configurações → Compras com IA** e ative **comércio agente habilitado**. A partir desse momento, assistentes que suportam o Protocolo Universal de Comércio podem descobrir sua loja e ler seu catálogo. Nada sobre sua loja normal muda.

## Painel de preparação

O topo da página de Compras com IA responde a uma pergunta em uma frase: **os assistentes de IA podem comprar em sua loja agora?**

- **"Os assistentes de IA podem comprar em sua loja"** — tudo necessário para uma compra está em vigor.
- **"Os assistentes de IA podem navegar em sua loja, mas ainda não podem comprar"** — sua loja é descoberta, mas algo está faltando antes que uma compra possa ser concluída (geralmente um provedor de pagamento conectado).
- **"Pausa de emergência está ativada"** ou **"Comércio agente está desativado"** — nada está sendo oferecido aos assistentes.

Abaixo do veredicto, você verá uma lista curta — provedor de pagamento conectado, frete pode ser orçado, produtos visíveis para os assistentes — com dicas ao lado de qualquer coisa que ainda precise de atenção. Os contadores mostram quantos produtos os assistentes podem vender, quantos você escondeu deles, quantos assistentes visitaram e quantos você bloqueou.

A lista de verificação reflete sua configuração **ativa**: conecte um provedor de pagamento ou adicione um método de frete e o veredicto será atualizado na próxima vez que você abrir a página.

## A pausa de emergência

A **Pausa de emergência** é um interruptor separado do principal. Use-a para interromper imediatamente toda a atividade do assistente — por exemplo, se algo parecer errado — sem desfazer sua configuração. Limpe-a para retomar. Pense no interruptor principal como "esse recurso está configurado" e a pausa de emergência como "pare tudo agora".

## O que os assistentes podem fazer

Dois níveis de acesso, controlados separadamente:

- **Leitura** (descoberta e navegação) é de menor risco. Um assistente pode encontrar sua loja e ler os detalhes dos produtos.
- **Checkout** (comprar realmente) é de maior risco e permanece fechado para assistentes não verificados, a menos que você o permita.

Uma loja pode ser descoberta sem ser comprável — uma forma útil de começar.

## Ocultando produtos específicos

Todo produto tem uma configuração de **Visível para agentes de compras com IA** (ativada por padrão). Desative-a para manter um produto específico fora dos assistentes enquanto ele permanece em sua loja — útil para itens que você prefere vender apenas por meio do próprio site.

## Gerenciando assistentes individuais

Quando um assistente compra pela primeira vez — ou tenta —, o Spwig o registra em **Compras com IA → Identidades de Agentes**. Cada entrada mostra o endereço verificado do assistente (o diretório com o qual ele se autentica), seu nível de confiança e quantos pedidos ele fez. O nome e o logotipo que o assistente apresenta são mostrados apenas como detalhes *reivindicados* — trate-os como rótulos, não como comprovação de identidade; a parte que pode ser confiável é o endereço verificado.

Todo assistente está em um dos três níveis de confiança:

| Nível de confiança | O que significa |
|---|---|
| **Limitado (verificado, limitado)** | O padrão para um novo assistente. O Spwig registrou sua identidade, e ele carrega o limite de valor do pedido, o limite de gasto diário e as restrições de pagamento definidas em sua política (veja abaixo). |
| **Verificado (limites removidos)** | Uma decisão deliberada sua de confiar totalmente nesse assistente. Seus limites de valor do pedido e gasto diário são removidos. |
| **Bloqueado** | O assistente já não pode comprar em sua loja. Checkouts abertos são encerrados, embora qualquer pagamento já realizado permaneça inalterado. |

Para parar um assistente, selecione-o na lista e escolha **Bloquear os assistentes selecionados**. **Desbloquear os assistentes selecionados** sempre o devolve para **Limitado** — nunca diretamente para **Verificado** — porque levantar os limites é uma etapa separada, deliberada.

Para levantar totalmente os limites de um assistente, selecione-o e escolha **Promover para verificado (remover limites)**.

Isso limpa seu valor máximo de pedido e o teto de gasto diário e move o assistente para o estado Verificado.

Um assistente bloqueado é ignorado - desbloqueie-o primeiro, depois promova-o.

Trate disso como uma decisão real de confiança: promova apenas um assistente no qual você tenha certeza, pois a verificação remove os limites de segurança com os quais um novo assistente começa.

## Definindo os limites de um assistente

Abra a página de detalhes de um assistente e use a seção **Política (limites e ofertas permitidas)** para definir o que ele pode fazer:

| Campo | O que ele controla |
|---|---|
| **Valor máximo do pedido** | O maior pedido único que esse assistente pode fazer. Deixe em branco para sem limite. |
| **Teto de gasto diário** | O máximo que esse assistente pode gastar em todos os pedidos em um dia. Deixe em branco para sem limite. |
| **Permitir códigos de desconto** | Se o assistente pode aplicar códigos de desconto na finalização. |
| **Permitir cartões-presente** | Se o assistente pode resgatar cartões-presente. |
| **Permitir bens digitais** | Se o assistente pode comprar produtos digitais. |
| **Limite de taxa (por minuto)** | Quantas solicitações o assistente pode fazer ao seu estoque por minuto. |

Um novo assistente começa com limites de valor de pedido e gastos definidos, e com descontos, cartões-presente e bens digitais desativados - o padrão deliberadamente conservador. Altere qualquer um desses campos e salve; cada alteração é registrada em **Eventos do Agente** com os valores antes e depois, então você sempre terá um registro de quem mudou o que e quando. Promover um assistente para Verificado limpa seu valor máximo de pedido e teto de gasto diário para você - você não precisa apagá-los manualmente primeiro.

## O registro de atividade

**Compras de IA → Eventos do Agente** é um registro imune a adulterações do que os assistentes fizeram - cada solicitação verificada, cada tentativa bloqueada, cada mudança que você fez. É um registro somente leitura e não pode ser editado ou excluído, então ele serve como sua trilha de evidências se alguma compra feita por um assistente for contestada.

## Uma observação sobre as plataformas de assistentes

As empresas que executam esses assistentes (e as regras para aparecer neles) são novas e mudam com frequência. Algumas exigem que você se candidate ou atenda a condições regionais antes que seus produtos possam ser comprados por meio delas. O Spwig prepara seu estoque; se um determinado assistente o listar é assunto do próprio assistente.

Preserve todos os formatos de markdown, caminhos de imagens, blocos de código e termos técnicos.