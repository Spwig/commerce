---
title: Serviços Hospedados Spwig
---

Spwig inclui três serviços em nuvem opcionais que sua loja pode usar sem que você precise configurar ou hospedar nada por conta própria: **GeoIP** detecta onde seus visitantes estão localizados, **Geocoder** converte endereços de clientes em coordenadas de mapa e **Push** envia notificações instantâneas para seu aplicativo de administração móvel Spwig. Na edição Comunitária (gratuita), cada serviço vem com uma cota mensal generosa. Quando qualquer serviço se aproximar de seu limite, o Spwig avisa você no painel de administração para que você possa decidir se deseja atualizar antes que seus clientes notem alguma coisa.

## Os três serviços hospedados

### GeoIP — detecção do país do visitante

O GeoIP identifica o país de cada visitante com base em seu endereço IP. Sua loja usa essa informação para exibir automaticamente a moeda correta quando um cliente chega e para preencher automaticamente o campo do país durante o checkout. Por exemplo, um visitante da Alemanha verá os preços em euros e um visitante do Japão verá os preços em ienes — sem precisar escolher manualmente.

Cada carregamento de página em que o GeoIP realiza uma consulta conta contra sua cota mensal. Visitas repetidas do mesmo navegador de sessão não consomem uma consulta cada uma; o resultado é armazenado em cache para a sessão. Consultas de GeoIP ocorrem apenas no site da loja, não no painel de administração.

### Geocoder — endereço para coordenadas

O Geocoder traduz endereços digitados pelos clientes em coordenadas geográficas (latitude e longitude). Sua loja usa essas coordenadas para dois propósitos: calcular custos de envio com base na distância quando você tiver pontos de coleta ou regras de envio com base em raio, e alimentar as sugestões de autocompletar de endereço na página de checkout para que os clientes possam encontrar seu endereço rapidamente.

Uma consulta ao geocoder é acionada quando um cliente seleciona ou confirma um endereço durante o checkout. Assim como o GeoIP, os resultados são armazenados em cache para que o mesmo endereço seja consultado apenas uma vez por sessão.

### Push — notificações no aplicativo de administração

O Push envia notificações em tempo real para seu aplicativo móvel de comerciante Spwig. Quando uma nova encomenda chega, quando o estoque cai abaixo de um limite ou quando um cliente envia uma mensagem, o Push envia uma notificação instantânea para seu dispositivo para que você possa responder sem precisar manter o painel de administração aberto.

Cada notificação enviada para seu dispositivo conta como uma solicitação de push contra sua cota mensal.

## A camada gratuita da Comunidade

Na edição Comunitária do Spwig, cada serviço está incluído sem custo até o limite de solicitações mensais. Os limites exatos são definidos pelo Spwig e podem variar; seu painel de administração sempre mostra as figuras atuais para sua instalação. Planos pagos (Iniciante, Crescimento, Profissional, Profissional Plus) e instalações auto-hospedadas com licença paga têm limites mais altos para cada serviço.

Quando um serviço atinge 100% da cota da Comunidade, as solicitações para esse serviço param até que o contador seja redefinido no próximo mês calendário. O impacto em sua loja depende de qual serviço está afetado:

| Serviço | O que acontece em 100% |
|---------|----------------------|
| GeoIP | A detecção automática de moeda volta para a moeda padrão da sua loja. Os clientes ainda podem mudar a moeda manualmente. |
| Geocoder | O autocompletar de endereço para de oferecer sugestões. Os clientes ainda podem digitar seu endereço manualmente. O cálculo da taxa de envio continua usando as coordenadas conhecidas anteriormente. |
| Push | Novas notificações do aplicativo de administração são enfileiradas, mas não entregues até o próximo mês ou uma atualização. |

Sua loja continua a operar normalmente em todos os casos — nenhuma encomenda é perdida e os clientes ainda podem finalizar o checkout. Os efeitos são limitados a recursos de conveniência.

## Lendo o tile do painel

O tile **Uso dos serviços Spwig** aparece na página inicial do seu painel de administração. Ele mostra uma barra de progresso para cada um dos três serviços.

Cada linha no tile segue o mesmo layout:

- **Nome do serviço** (esquerda) — GeoIP, Busca de endereço (Geocoder) ou Notificações de push.
- **Barra de progresso** (centro) — preenche da esquerda para a direita conforme o uso aumenta.

A cor da barra muda conforme os limites se aproximam:
  - **Verde** — o uso está abaixo de 80%.

Tudo está funcionando normalmente.
  - **Amber** — o uso está entre 80% e 99%.

O serviço ainda está em execução, mas está se aproximando do limite.
  - **Red** — o uso atingiu 100%.

O serviço agora está limitado para este mês.
- **Contagem de uso** (direita) — o número exato de solicitações usadas do total permitido, por exemplo `3.241 / 10.000`.

O rótulo entre parênteses mostra a janela de tempo, normalmente `(este mês)`.

Se o tile não conseguir se conectar ao servidor de atualização do Spwig para obter seu uso atual (por exemplo, se seu servidor não tiver acesso à internet), a coluna de contagem mostrará um traço (`—`) para esse serviço. Isso não significa que o serviço esteja quebrado; significa que a exibição de uso está temporariamente indisponível.

### O botão **Upgrade**

Quando qualquer serviço atingir 80% ou mais, um botão **Upgrade** aparecerá no canto superior direito do tile. Clicar nele abre a página de upgrade do Spwig, onde você pode comparar planos e aumentar os limites do seu serviço. O botão desaparece quando o uso cai abaixo de 80% no início do próximo mês.

## A faixa de aviso de cota

Além do tile do painel, uma faixa aparece no topo de todas as páginas de administração sempre que qualquer serviço ultrapassar o limite de 80%. A faixa só aparece em instalações da Comunidade.

**Faixa amarela — se aproximando do limite (80–99%)**

> **Atingindo o limite de serviços hospedados:** Um dos seus serviços do Spwig está acima de 80% da cota da camada Comunidade. Atualize para aumentar o limite antes que ele seja atingido.

Essa faixa é um aviso antecipado. Seus serviços ainda estão em execução, e você tem tempo para decidir se deseja atualizar antes do final do mês.

**Faixa vermelha — limite atingido (100%)**

> **Limite dos serviços do Spwig atingido:** Um dos seus serviços hospedados atingiu sua cota da camada Comunidade. Atualize para mantê-los em execução sem interrupções.

Essa faixa aparece quando pelo menos um serviço atinge 100% e está agora limitado. Clicar em **Upgrade** em qualquer uma das faixas abre a mesma página de upgrade do tile.

A faixa desaparece automaticamente no início do próximo mês calendário quando os contadores são redefinidos, ou imediatamente após você atualizar para um plano pago.

## Alerta por e-mail em 90%

Quando qualquer serviço ultrapassar 90% de sua cota, o Spwig também enviará um e-mail de aviso único para o endereço configurado nas configurações da loja (**Configurações > Configurações da Loja > Contato > E-mail do Administrador**). O e-mail é enviado no máximo uma vez por serviço por mês calendário, então você não será inundado com mensagens. Não é enviado um e-mail em 100%, pois nesse momento a faixa no painel já deixa a situação clara.

Se você não receber o e-mail, verifique se o endereço de e-mail do administrador está configurado corretamente em **Configurações > Configurações da Loja**.

## Atualizando seu plano

Ao atualizar da camada Comunidade para qualquer plano pago, os limites mais altos entram em vigor imediatamente — não é necessário reiniciar a loja ou alterar a configuração. O tile do painel mostrará o novo limite mais alto na próxima vez que for atualizado (dentro de cinco minutos).

Para atualizar, clique no botão **Upgrade** no tile do painel ou na faixa de cota, ou acesse diretamente a página de upgrade do Spwig. Planos pagos incluem os mesmos três serviços hospedados (GeoIP, Geocoder, Push) com limites mensais elevados, mais acesso à entrega de e-mails hospedada pelo Spwig e suporte prioritário.

## Self-hosting e licenças Pro

Se você executar uma instalação self-hosted do Spwig com uma licença paga, sua camada de licença determina seus limites de serviço, da mesma forma que o plano hospedado equivalente. Sua loja ainda precisa ter acesso à internet para saída para `updates.spwig.com` para que a plataforma possa buscar e verificar sua configuração de camada. As contagens de uso exibidas no tile do painel são obtidas dos pontos de extremidade dos serviços hospedados em `geoip.spwig.com`, `geocoder.spwig.com` e `push.spwig.com`.

Não há, no momento, a opção de substituir GeoIP, Geocoder ou Push por alternativas self-hosted — esses serviços são fornecidos exclusivamente pela infraestrutura do Spwig e estão incluídos em todas as edições.

## Dicas

Preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos.

- **Verifique a tile regularmente no final de meses ocupados** — um evento de vendas ou promoção pode aumentar significativamente as consultas de GeoIP e Geocoder.

A tile lhe dá aviso antecipado antes que os clientes sejam afetados.
- **A fallback de moeda é invisível para a maioria dos clientes** — se o GeoIP atingir seu limite, os clientes verão a moeda padrão do seu loja.

Isso raramente é um problema sério para lojas que atendem principalmente um mercado; é mais relevante para lojas verdadeiramente internacionais.
- **A autocompletação de endereço é uma conveniência, não um obstáculo** — quando o Geocoder é limitado, os clientes ainda podem digitar e enviar seu endereço normalmente.

Se você realiza promoções frequentes que geram tráfego de checkout alto, considere atualizar antes de períodos ocupados.
- **O throttling de push não perde notificações permanentemente** — as notificações em fila do período de throttling não são entregues retroativamente quando o mês se reinicia ou após uma atualização.

Se você depende fortemente do push para alertas de pedidos sensíveis ao tempo, atualizar antes que o limite seja atingido garante que você não perca nada.
- **O cache de 5 minutos significa que a tile não é perfeitamente em tempo real** — as figuras de uso são atualizadas aproximadamente a cada cinco minutos em segundo plano.

Durante períodos de tráfego inesperadamente alto, o uso real pode estar ligeiramente à frente do que a tile mostra.
- **Defina seu endereço de e-mail de administração** — o e-mail de aviso de 90% só funciona se **Configurações > Configurações da Loja > E-mail de Administração** estiver preenchido.

É útil confirmar que isso esteja configurado corretamente para que você receba o aviso antes que problemas ocorram.