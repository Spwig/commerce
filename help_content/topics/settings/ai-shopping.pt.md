---
title: Compras com IA
---

Compras com IA permite que assistentes de compras com IA encontrem seus produtos e, quando você permitir, comprem em nome de um cliente em sua loja. Ele está **desativado por padrão** — ativar é uma escolha intencional, e até que você o faça, sua loja não expõe nada a esses assistentes.

## Ativando

Abra **Configurações → Compras com IA** e ative **Comércio Agente habilitado**. A partir desse momento, assistentes que suportam o Protocolo de Comércio Universal podem descobrir sua loja e ler seu catálogo. Nada sobre sua loja normal muda.

## Painel de preparação

No topo da página de Compras com IA, há uma pergunta respondida em uma única frase: **os assistentes de IA podem realmente comprar em sua loja agora?**

- **"Os assistentes de IA podem comprar em sua loja"** — tudo necessário para uma compra está em vigor.
- **"Os assistentes de IA podem navegar em sua loja, mas ainda não podem comprar"** — sua loja é descobrível, mas algo ainda está faltando para concluir uma compra (normalmente um provedor de pagamento conectado).
- **"Parada de emergência está ligada"** ou **"Comércio Agente está desativado"** — nada está sendo servido aos assistentes.

Abaixo da avaliação, você verá uma lista curta de verificação — provedor de pagamento conectado, envio pode ser cotado, produtos são visíveis aos assistentes — com uma dica ao lado de qualquer coisa que ainda precise de atenção. Os contadores mostram quantos produtos os assistentes podem vender, quantos você escondeu deles, quantos assistentes visitaram e quantos você bloqueou.

A lista de verificação reflete sua **configuração ativa**: conecte um provedor de pagamento ou adicione um método de envio e a avaliação será atualizada na próxima vez que você abrir a página.

## Parada de emergência

A **parada de emergência** é um interruptor separado do principal. Use-a para parar imediatamente todas as atividades dos assistentes — por exemplo, se algo parecer errado — sem desmontar sua configuração. Limpe-a para retomar. Considere o interruptor principal como "esta funcionalidade está configurada" e a parada de emergência como "pare tudo agora".

## O que os assistentes podem fazer

Dois níveis de acesso, controlados separadamente:

- **Leitura** (descoberta e navegação) é de menor risco. Um assistente pode encontrar sua loja e ler detalhes do produto.
- **Checkout** (realmente comprar) é de maior risco e permanece fechado para assistentes não verificados, a menos que você permita.

Uma loja pode ser descobrível sem ser comprável — um método útil para começar.

## Ocultando produtos específicos

Cada produto tem um **Visível para agentes de compras com IA** (ativado por padrão). Desative-o para manter um produto específico oculto dos assistentes enquanto ele permanece em sua loja — útil para itens que você prefere vender apenas por meio do seu próprio site.

## Gerenciando assistentes individuais

Quando um assistente faz sua primeira compra — ou tenta — o Spwig o registra em **Compras com IA → Identidades de Agentes**. Cada entrada mostra o local verificado do assistente (o diretório com o qual ele assina) e quantas solicitações ele fez. O nome e o logotipo apresentados pelo assistente são mostrados apenas como *detalhes reivindicados* — trate-os como um rótulo, não como prova de identidade; o local verificado é a parte que pode ser confiada.

Novos assistentes começam **limitados**: eles podem transacionar, mas dentro de limites. Para bloquear um, selecione-o e escolha **Bloquear assistentes selecionados** — os checkouts abertos terminam e o assistente não pode mais comprar, enquanto qualquer pagamento já realizado permanece inalterado. **Desbloquear assistentes selecionados** retorna a ele ao estado limitado (nunca diretamente para ilimitado — remover limites sempre é um passo separado e intencional).

## Registro de atividade

**Compras com IA → Eventos de Agentes** é um registro evidente de alterações feitas pelos assistentes — cada solicitação verificada, cada tentativa bloqueada, cada alteração que você fez. É somente para visualização e não pode ser editado ou excluído, então ele serve como seu rastro de evidências se uma compra feita por um assistente for alguma vez contestada.

## Uma nota sobre as plataformas de assistentes

As empresas que operam esses assistentes (e as regras para aparecer nelas) são novas e mudam com frequência.

Alguns exigem que você se candidate ou atenda a condições regionais antes que seus produtos possam ser comprados por meio delas.

Spwig torna sua loja pronta; se um determinado assistente lista você ou não depende desse assistente.