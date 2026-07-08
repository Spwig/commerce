---
title: Rastreamento de Afiliados & Links
---

O rastreamento de afiliados impulsiona todo o sistema de comissões conectando compras de clientes aos afiliados que os referenciaram. Este guia explica como funcionam os links de rastreamento, quais dados o Spwig registra quando os clientes clicam nesses links e como o sistema de atribuição baseado em cookies determina qual afiliado ganha cada comissão.

Entender os mecanismos de rastreamento ajuda você a resolver problemas de atribuição, analisar o desempenho dos links e educar seus afiliados sobre como maximizar suas conversões.

## O que é um Link de Rastreamento?

Um link de rastreamento é um URL único que redireciona clientes para sua loja enquanto registra a identidade do afiliado em um cookie. Cada afiliado pode criar vários links de rastreamento apontando para diferentes destinos — a página inicial, produtos específicos, páginas de coleções ou páginas de destino.

Formato de link de rastreamento:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Este link redireciona para o destino enquanto define um cookie de rastreamento que associa futuras compras ao afiliado que possui o código de link `a2b7f8c4d1e9`.

Os afiliados geram esses links a partir do painel de controle do seu portal. Eles copiam a URL completa e a compartilham em posts de blog, mídia social, e-mails ou qualquer canal onde eles atingem potenciais clientes.

## Componentes do Link de Rastreamento

Todo link de rastreamento contém esses elementos:

| Componente | Exemplo | Descrição |
|-----------|---------|-------------|
| **URL Base** | `https://yourstore.com` | O domínio da sua loja |
| **Caminho de Rastreamento** | `/affiliate/track/` | Ponto de extremidade de rastreamento do Spwig |
| **Código do Link** | `a2b7f8c4d1e9` | Identificador único de 12 caracteres gerado automaticamente |
| **Destino** | Definido quando o link é criado | Onde o cliente chega após o redirecionamento (página inicial, produto, etc.) |

Quando um afiliado cria um link, o Spwig gera automaticamente o código único de 12 caracteres. O afiliado nunca precisa criar ou editar esse código manualmente — ele simplesmente escolhe o destino e o Spwig cuida do resto.

### Rótulos de Link (Opcional)

Os afiliados podem adicionar um rótulo a cada link para sua própria organização:
- "Link do Perfil do Instagram"
- "Descrição do YouTube"
- "Campanha de E-mail do Black Friday"

Os rótulos ajudam os afiliados a rastrear quais canais promocionais têm o melhor desempenho. Eles são visíveis apenas para o afiliado e você — os clientes nunca veem o rótulo.

## Como Funciona o Rastreamento

O processo de rastreamento e atribuição segue cinco etapas do clique à comissão:

### 1. Cliente Clica no Link

Um cliente potencial clica no link de rastreamento do afiliado de qualquer canal promocional (post de mídia social, artigo de blog, newsletter de e-mail).

### 2. Clique Registrado

O ponto de extremidade de rastreamento do Spwig registra detalhes do clique:
- Endereço IP
- User agent (navegador e dispositivo)
- HTTP referrer (de onde veio o clique)
- Timestamp
- Identificador de sessão

Esses dados aparecem no **Clicles** do painel de administração em **Afiliado > Clicles** para análise e detecção de fraudes.

### 3. Cookie Definido

O sistema de rastreamento define um cookie no navegador do cliente antes de redirecioná-lo. O cookie contém:
- ID do afiliado (quem deve receber a comissão)
- ID do programa (qual estrutura de comissão se aplica)
- Código do link (qual link específico foi clicado)

### 4. Cliente Faz uma Compra

O cliente navega em sua loja e completa uma compra. Isso pode acontecer imediatamente ou dias/semanas depois, desde que a compra seja feita dentro do período de validade do cookie.

### 5. Comissão Criada

Na finalização da compra, o Spwig verifica se há um cookie de afiliado. Se encontrado e ainda válido (dentro do período de validade do cookie), o sistema cria um registro de comissão com status **Pendente** vinculado ao afiliado, programa e pedido.

## Atribuição Baseada em Cookie

O cookie de rastreamento é o mecanismo central que vincula compras a afiliados. Entender como os cookies funcionam ajuda você a definir janelas de atribuição ideais e resolver problemas de rastreamento.

### Estrutura do Cookie

| Propriedade | Valor |
|----------|-------|
| **Nome** | `aff_{program_id}` (exemplo: `aff_7` para ID de programa 7) |
| **Valor** | JSON contendo ID do afiliado, código do link, timestamp |
| **Domínio** | Domínio da sua loja |
| **Caminho** | `/` (acesso em todo o site) |
| **Duração** | Período de vida do cookie do programa (1–365 dias) |
| **HttpOnly** | `true` (impede acesso via JavaScript para segurança) |
| **SameSite** | `Lax` (permite rastreamento de referenciadores externos) |
| **Secure** | `true` em sites HTTPS (recomendado) |

### Janela de Vida do Cookie

O período de vida do cookie determina por quanto tempo os clientes têm para fazer uma compra após clicar em um link de afiliado. Esta janela é definida por programa em **Marketing > Programas de Afiliados** quando você cria ou edita um programa.

Períodos de vida do cookie padrão da indústria:
- **7 dias**: Produtos de decisão rápida (produtos de supermercado, ingressos para eventos)
- **30 dias**: E-commerce padrão (a configuração mais comum)
- **60–90 dias**: Compras consideradas (móveis, eletrônicos, produtos B2B)
- **365 dias**: Ciclos de venda longos (produtos de luxo, serviços de alto valor)

Se um cliente clicar em um link de afiliado em 1 de janeiro e o período de vida do cookie for 30 dias, qualquer compra que ele fizer até 30 de janeiro creditará esse afiliado. Compras em 31 de janeiro ou depois não geram comissão porque o cookie expirou.

### Modelo de Atribuição por Último Clique

O Spwig usa **atribuição por último clique**: o último afiliado a clicar ganha. Veja como isso funciona:

**Cenário**: Um cliente clica no link do afiliado A na segunda-feira, depois no link do afiliado B na quarta-feira e depois faz uma compra na sexta-feira.

**Resultado**: O afiliado B ganha a comissão porque seu link foi o último clique.

O cookie do último clique sobrescreve cookies de afiliados anteriores. Este modelo é simples de entender e evita comissões duplas, embora isso signifique que apenas um afiliado recebe crédito por pedido (o último antes da compra).

## Registro de Clicles

O Spwig registra cada clique em cada link de afiliado para fornecer análises para você e o afiliado. Os dados de clique ajudam a medir o desempenho dos links, detectar fraudes e otimizar estratégias promocionais.

### Dados Capturados por Clique

Navegue até **Afiliado > Clicles** para ver todos os cliques registrados. Cada entrada contém:

| Campo | Descrição |
|-------|-------------|
| **Link** | Qual link de rastreamento foi clicado |
| **Afiliado** | Quem possui o link |
| **Endereço IP** | IP do cliente (para detecção de fraudes) |
| **User Agent** | Informações do navegador e do dispositivo |
| **Referrer** | A página onde o cliente clicou no link (exemplo: "https://instagram.com") |
| **ID de Sessão** | Identificador único para esta sessão de navegação |
| **Timestamp** | Data e hora exatas do clique |

### Limitação de Taxa

Para prevenir fraudes de clique e abuso de bots, o Spwig limita os cliques a **100 por minuto por endereço IP**. Se o mesmo IP ultrapassar esse limite, cliques adicionais são ignorados e não incrementam as contagens de cliques.

Essa proteção impede atores maliciosos de inflar estatísticas de cliques sem bloquear o tráfego legítimo. Clientes reais quase nunca ultrapassam 100 cliques por minuto.

### Considerações de Privacidade

Os dados de clique contêm endereços IP e user agents para fins de detecção de fraudes. Certifique-se de que sua política de privacidade divulgue que você rastreia referências de afiliados e compartilha dados de desempenho anonimizados com os afiliados.

## Visualizando Links de Afiliados

Todos os links de rastreamento gerados por afiliados aparecem em seu painel de administração para monitoramento e gerenciamento.

### Acessando a Lista de Links

Navegue até **Afiliado > Links** para visualizar todos os links de rastreamento de todos os afiliados e programas. A visualização da lista exibe:

- **Código do Link**: O identificador único de 12 caracteres
- **Afiliado**: Quem criou o link
- **Programa**: Qual estrutura de comissão se aplica
- **Rótulo**: Descrição opcional fornecida pelo afiliado
- **Destino**: Onde o link redireciona os clientes
- **Total de Clicles**: Contagem total de cliques
- **Status Ativo**: Se o link está atualmente rastreando

### Filtros de Links

Use os filtros do painel de administração para estreitar a lista:
- **Por Afiliado**: Veja todos os links para um parceiro específico
- **Por Programa**: Visualize links promovendo uma estrutura de comissão específica
- **Por Status Ativo**: Encontre links desativados

Esses filtros ajudam você a analisar a distribuição de links em sua rede de afiliados e identificar os links com melhor desempenho.

## Estatísticas de Link

Cada link de rastreamento acumula métricas de desempenho que ajudam os afiliados a otimizar suas estratégias promocionais e ajudam você a identificar seus melhores parceiros.

### Clique em um registro de link para ver estatísticas detalhadas:

| Métrica | Descrição | Cálculo |
|--------|-------------|-------------|
| **Total de Clicles** | Todos os cliques registrados desde a criação do link | Contagem de registros de cliques |
| **Clicles (7 dias)** | Indicador de atividade recente | Clicles nos últimos 7 dias |
| **Conversões** | Pedidos atribuídos a este link | Contagem de comissões deste código de link |
| **Taxa de Conversão** | Percentual de cliques que resultaram em compras | (Conversões ÷ Total de Clicles) × 100 |
| **Receita Total** | Soma de todos os valores de pedido deste link | Soma dos totais de pedidos para cliques convertidos |

### Usando Estatísticas para Otimização

**Para Afiliados**: Esses números mostram quais canais promocionais funcionam melhor. Se um link do perfil do Instagram tiver uma taxa de conversão de 5% mas um link de postagem de blog tiver 15%, o afiliado deve focar mais no conteúdo do blog.

**Para Merchants**: As estatísticas de link revelam quais afiliados geram tráfego de qualidade. Altas contagens de cliques com taxas de conversão baixas sugerem que o público do afiliado não é uma boa correspondência para seus produtos.

## Gerenciamento de Links

Você pode gerenciar links de afiliados a partir do painel de administração para manutenção e resolução de problemas.

### Desativando Links

Para impedir que um link específico rastreie novos cliques enquanto preserva os dados históricos:

1. Navegue até **Afiliado > Links**
2. Clique no link que deseja desativar
3. Desmarque **Ativo**
4. Clique em **Salvar**

Links desativados ainda redirecionam os clientes para o destino, mas não definem cookies de rastreamento nem registram cliques. Isso é útil quando um afiliado está executando uma campanha temporária ou você precisa desativar um canal promocional específico.

### Editando Detalhes do Link

Você pode modificar:
- **Rótulo**: Atualize a descrição fornecida pelo afiliado
- **Destino**: Mude para onde o link redireciona (útil se você mover uma página de produto)
- **Status Ativo**: Ative ou desative o rastreamento

Você não pode editar o código do link — ele é permanente e está vinculado a todos os dados históricos de cliques e comissões.

### Excluindo Links Inativos

Exclua links que não estão mais em uso e não têm cliques ou conversões históricas. Isso mantém sua lista de links limpa sem perder dados analíticos valiosos.

**Aviso**: Excluir um link remove todos os registros de cliques associados. Apenas exclua links com zero cliques ou quando você estiver absolutamente certo de que não precisa dos dados históricos.

## Modelo de Atribuição

Entender a lógica de atribuição do Spwig ajuda você a estabelecer expectativas com os afiliados e resolver disputas sobre comissões.

### Atribuição por Último Clique

Como mencionado anteriormente, o Spwig usa atribuição por último clique: se um cliente clicar em vários links de afiliados antes de comprar, apenas o último afiliado a clicar ganha a comissão.

**Vantagens**:
- Simples de entender e explicar
- Impede comissões duplas
- Recompensa afiliados que fecham a venda

**Desvantagens**:
- Afiliados que introduziram o cliente não recebem crédito
- Não reflete jornadas de clientes com múltiplos toques
- Pode incentivar "hijacking de link" (afiliados alvo de clientes com alta intenção que já foram referenciados por alguém else)

### Período de Vida do Cookie Determina a Qualificação

Apenas compras dentro da janela de período de vida do cookie geram comissões. Se o cookie expirar antes do checkout, nenhuma comissão será criada, mesmo que o cliente retorne por meio de um bookmark.

**Exemplo**: Período de vida do cookie de 30 dias
- Cliente clica no link em 1 de janeiro → Cookie definido, expira em 31 de janeiro
- Cliente compra em 25 de janeiro → Comissão criada
- Cliente compra em 5 de fevereiro → Nenhuma comissão (cookie expirado)

### Rastreamento de Sessão

Além do cookie, o Spwig rastreia o ID da sessão para cada clique. Isso permite a atribuição de múltiplas visitas dentro da mesma sessão, mesmo que os cookies sejam bloqueados ou limpos.

Se um cliente clicar em um link, carregar várias páginas da sua loja e depois fazer uma compra — tudo na mesma sessão — o afiliado recebe crédito mesmo sem um cookie persistente.

## Solução de Problemas

Problemas comuns de rastreamento e como resolvê-los:

### Link Não Rastreando Clicles

**Sintomas**: A contagem de cliques permanece em zero apesar de relatos do afiliado de que compartilhou o link.

**Causas e soluções**:
1. **Link desativado**: Verifique o status **Ativo** na página de detalhes do link
2. **Programa inativo**: Navegue até **Afiliado > Programas** e verifique se o status do programa é **Ativo**
3. **Conta do afiliado desativada**: Verifique o status da conta do afiliado em **Afiliado > Afiliados**
4. **Limitação de taxa**: Verifique se o mesmo IP está gerando cliques excessivos (tráfego de bots)

### Taxa de Conversão Baixa

**Sintomas**: Altas contagens de cliques, mas poucas ordens atribuídas.

**Causas e soluções**:
1. **Período de vida do cookie muito curto**: Aumente o período de vida do programa se seus produtos exigirem pesquisa e consideração
2. **Qualidade da página de destino**: Verifique a página de destino — ela é compatível com dispositivos móveis? Carrega rapidamente? O produto está em estoque?
3. **Mau ajuste do público**: O público do afiliado pode não ser a correspondência certa para seus produtos
4. **Navegadores bloqueando cookies**: Alguns ferramentas de privacidade bloqueiam cookies de terceiros, embora o Spwig use cookies de primeira parte, que são menos prováveis de serem bloqueados

### Registros de Clique Duplicados

**Sintomas**: O mesmo cliente gera múltiplos registros de clique em sequência rápida.

**Causa**: Isso é comportamento normal. Cada carregamento de página do link de rastreamento cria um registro de clique. Se um cliente clicar, a página carregar lentamente e clicar novamente, você verá múltiplos registros.

**Solução**: Nenhuma ação necessária. O limitador de taxa previne abusos (100 cliques/minuto/IP), e cliques duplicados da mesma sessão não afetam a atribuição — apenas um cookie é definido.

## Dicas

- **Teste o rastreamento antes do lançamento** — Crie uma conta de afiliado de teste, gere um link de rastreamento, clique nele em um navegador anônimo e complete uma compra de teste. Verifique se a comissão aparece com a atribuição correta do afiliado.
- **Eduque os afiliados sobre o período de vida do cookie** — Certifique-se de que os afiliados entendam que só ganham comissões por compras dentro da janela do cookie. Isso ajuda-os a estabelecer expectativas realistas e focar no tráfego de alta intenção.
- **Monitore padrões de clique para fraudes** — Contagens de clique anormalmente altas de um único IP ou cliques sem string de user agent podem indicar tráfego de bots. Revise cuidadosamente esses afiliados antes de aprovar comissões.
- **Use rótulos de link consistentemente** — Incentive os afiliados a rotular seus links por canal (Instagram, Blog, E-mail) para que vocês possam analisar quais canais promocionais geram as melhores conversões.
- **Considere períodos de vida do cookie mais longos para produtos de alto valor** — Se o valor médio do pedido for alto e os clientes geralmente pesquisam antes de comprar, estenda o período de vida do cookie para 60–90 dias para capturar essas conversões atrasadas.
- **Verifique os dados de referrer para insights de canal** — O campo de referrer mostra de onde os cliques vêm. Se você ver muitos cliques de "instagram.com" ou "youtube.com", você sabe quais plataformas sociais seus afiliados usam com mais eficácia.