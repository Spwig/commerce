---
title: Compartilhamento Social
---

Botões de compartilhamento social permitem que os clientes compartilhem seus produtos, posts de blog e páginas em redes sociais diretamente a partir de sua loja virtual. Você controla quais plataformas aparecem, como os botões parecem, onde são colocados e se a atividade de compartilhamento é rastreada e contada.

## Configurando as configurações de compartilhamento social

Todo o comportamento de compartilhamento social é controlado a partir de uma única página de configurações. Navegue até **Marketing > Configurações de Compartilhamento Social** (a página redireciona automaticamente para o formulário de configurações — há apenas um registro de configuração).

### Localização: onde os botões aparecem

A seção **Localização** controla quais tipos de conteúdo mostram automaticamente os botões de compartilhamento.

| Configuração | Descrição |
|---------|-------------|
| **Habilitar em Produtos** | Mostrar botões de compartilhamento nas páginas de detalhes do produto |
| **Habilitar em Categorias** | Mostrar botões de compartilhamento nas páginas de listagem de categorias |
| **Habilitar em Posts de Blog** | Mostrar botões de compartilhamento nas páginas de posts de blog |
| **Habilitar em Páginas Personalizadas** | Mostrar botões de compartilhamento em páginas personalizadas da loja |

Marque os tipos de conteúdo onde você deseja que os botões apareçam. Você pode habilitar qualquer combinação — por exemplo, apenas produtos e posts de blog.

**Posição de Localização** controla onde os botões são exibidos na página:

| Opção | Descrição |
|--------|-------------|
| **Abaixo do Conteúdo** (padrão) | Exibido após o conteúdo principal |
| **Acima do Conteúdo** | Exibido antes do conteúdo principal |
| **Barra Lateral** | Exibido na barra lateral da página |
| **Flutuante (fixo)** | Fixo ao lado da janela de visualização conforme o visitante rola |

### Aparência: como os botões parecem

A seção **Aparência** controla quais plataformas são mostradas e como os botões são estilizados.

**Plataformas Habilitadas** — deixe em branco para mostrar todas as plataformas suportadas, ou insira um array JSON para restringir quais plataformas aparecem:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Chaves de plataforma suportadas: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Estilo do Botão** opções:

| Estilo | Descrição |
|-------|-------------|
| **Ícone Apenas** (padrão) | Mostra apenas o ícone da plataforma |
| **Ícone + Rótulo** | Mostra o ícone e o nome da plataforma |
| **Apenas Rótulo** | Mostra apenas o nome da plataforma como texto |

**Tamanho do Botão** — escolha **Pequeno**, **Médio** (padrão) ou **Grande** para combinar com o design da sua loja virtual.

**Direção de Layout** — organize os botões **Horizontalmente** (padrão, lado a lado) ou **Verticalmente** (empilhados).

**Mostrar Título** — quando marcado, um cabeçalho "Compartilhar" aparece acima do grupo de botões.

**Visibilidade em Dispositivos Móveis** controla a exibição dos botões em telas pequenas:

| Opção | Descrição |
|--------|-------------|
| **Sempre Mostrar** (padrão) | Botões visíveis em todos os dispositivos |
| **Ocultar em Móvel** | Botões ocultos em dispositivos móveis |
| **Apenas Móvel** | Botões exibidos apenas em dispositivos móveis |

### Configurações de rastreamento

**Mostrar Contagens de Compartilhamento** — quando marcado, uma insígnia de contagem aparece em cada botão mostrando quantas vezes essa plataforma foi compartilhada. As contagens são atualizadas em tempo real conforme os compartilhamentos são registrados.

**Rastrear Compartilhamentos** — quando marcado, cada clique de compartilhamento é registrado nas estatísticas de compartilhamento. Desativar isso para de salvar novos registros, mas não apaga os dados existentes. O rastreamento também concede medalhas de fidelidade aos clientes que compartilham (se o programa de fidelidade estiver ativo).

Clique em **Salvar** no final do formulário para aplicar suas alterações. As configurações têm efeito imediatamente.

## Visualizando atividade de compartilhamento

### Eventos de compartilhamento individuais

Navegue até **Marketing > Compartilhamentos Sociais** para ver um registro de cada evento de compartilhamento registrado. Cada entrada mostra:

- **Plataforma** — qual rede social foi usada (mostrada como uma insígnia colorida)
- **Conteúdo Compartilhado** — o tipo e o nome do conteúdo que foi compartilhado (ex: `produto: Blue Widget`)
- **Usuário** — o cliente que compartilhou, ou "Anônimo" para visitantes que não estavam logados
- **Tipo de Dispositivo** — desktop, mobile ou tablet
- **Compartilhado em** — a data e hora do compartilhamento

O log de compartilhamento é somente leitura — as entradas são criadas automaticamente quando os clientes clicam nos botões de compartilhamento.

Use os filtros **Plataforma** e **Tipo de Dispositivo** para explorar padrões de compartilhamento, e a hierarquia de datas para analisar períodos de tempo específicos.

### Contagens de compartilhamento por conteúdo

Navegue até **Marketing > Contagens de Compartilhamento** para ver totais agregados de compartilhamentos agrupados por item de conteúdo e plataforma. Essa visão facilita a identificação dos seus produtos e posts mais compartilhados.

Cada entrada mostra:
- **Conteúdo** — o tipo e o nome do item (ex.: `produto: Blue Widget`)
- **Plataforma** — a rede social
- **Contagem de Compartilhamento** — total de compartilhamentos registrados nessa plataforma
- **Última Atualização** — quando a contagem foi recalculada pela última vez

A lista está ordenada por contagem de compartilhamento em ordem decrescente, então o seu conteúdo mais viral aparece no topo. As contagens de compartilhamento são atualizadas automaticamente sempre que um novo evento de compartilhamento é registrado — não há necessidade de atualizá-las manualmente.

## Entendendo como os compartilhamentos são rastreados

Quando um cliente clica em um botão de compartilhamento, o Spwig registra:

1. Em qual plataforma ele compartilhou
2. O que foi compartilhado (produto, post de blog, página, etc.)
3. Se ele estava logado (se sim, o compartilhamento é vinculado à sua conta para integração de fidelidade)
4. O tipo de dispositivo
5. O URL que foi compartilhado

A contagem de compartilhamento para essa plataforma e item de conteúdo é incrementada automaticamente. Se **Mostrar Contagens de Compartilhamento** estiver ativado, a contagem atualizada aparecerá no botão na próxima vez que a página for carregada.

## Integração de fidelidade

Se seu programa de fidelidade estiver ativo e **Rastrear Compartilhamentos** estiver ativado, os clientes que estão logados ganham selos de fidelidade quando compartilham conteúdo. O selo de compartilhamento social faz parte das regras baseadas em ações do programa de fidelidade.

Para configurar recompensas de pontos por compartilhamento, navegue até **Clientes > Regras de Fidelidade** e procure por regras do tipo **Baseadas em Ações** e tipo de ação **Compartilhamento Social**.

## Dicas

- Ative o compartilhamento em produtos e posts de blog primeiro — esses são os tipos de conteúdo mais prováveis de serem compartilhados organicamente pelos clientes
- O Pinterest é particularmente valioso para categorias de produtos visuais, como moda, decoração de interiores e alimentos — priorize-o na lista `enabled_platforms` para lojas dessas categorias
- O compartilhamento via WhatsApp impulsiona fortemente conversões de indicações quentes, especialmente em dispositivos móveis; considere usar o modo de exibição **Apenas Móvel** para WhatsApp, mantendo outras plataformas visíveis em todos os dispositivos
- Se você notar que as contagens de compartilhamento estão infladas, verifique se o tráfego de testes (de sessões de administrador) foi contado antes do sinalizador **Is Admin Traffic** estar totalmente funcionando — você pode redefinir as contagens limpando as entradas do analytics de compartilhamento
- Revise a lista de Contagens de Compartilhamento mensalmente para identificar seus produtos mais compartilhados e destacá-los mais visivelmente em sua homepage ou em e-mails de marketing