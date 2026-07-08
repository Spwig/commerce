---
title: Slides de Promo para Exibição ao Cliente
---

Slides de promoção são exibidos na tela voltada para o cliente quando o terminal POS está ocioso (sem transação ativa). Crie um carrossel de imagens que destaque promoções sazonais, lançamentos de novos produtos, políticas da loja, eventos próximos e benefícios do programa de fidelidade. Os slides podem ser direcionados para lojas ou grupos específicos usando a atribuição de escopo - execute promoções de feriados apenas nas lojas dos EUA, ou exiba informações sobre eventos locais apenas nas localizações relevantes. Slides ativos ciclam automaticamente a cada 5-10 segundos, criando uma sinalização digital envolvente que mantém os clientes informados enquanto esperam.

Use slides de promoção para aumentar a conscientização sobre promoções atuais, educar os clientes sobre políticas e impulsionar o engajamento com programas de fidelidade e eventos.

![Lista de Slides de Promoção](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Comportamento da Exibição ao Cliente

Quando um terminal POS está ocioso (sem cliente no caixa, sem transação em andamento), a tela voltada para o cliente mostra:

**Modo Carrossel**:
- Cicla por todos os slides ativos
- Cada slide é exibido por 5-10 segundos (configurável por terminal)
- Transições suaves entre os slides
- Reproduz continuamente até que a transação comece

**Durante a Transação**:
- O carrossel para imediatamente
- A tela muda para a visão da transação (itens, total acumulado, prompts de pagamento)
- O carrossel retoma quando a transação é concluída e o terminal retorna ao modo ocioso

**Nenhum Slide Configurado**:
- A tela mostra uma mensagem de "Bem-vindo" com a identidade visual da loja
- Tela estática (sem carrossel)

**Requisitos Técnicos**:
- A tela do cliente pode ser um monitor separado ou a mesma tela do caixa (o aplicativo POS suporta modo de janela em janela)
- A sincronização é feita via API BroadcastChannel (comunicação no mesmo dispositivo) ou WebSocket (tela em dispositivos separados)

## Direcionamento por Escopo

Como os modelos de recibos, os slides de promoção suportam direcionamento baseado em escopo (prioridade mais alta para mais baixa):

| Prioridade | Escopo | Exemplo | Caso de Uso |
|------------|--------|---------|-------------|
| **1** | Específico da loja | Slides da loja de Paris | Slide sobre evento de festa de verão em Paris |
| **2** | Específico do grupo | Slides das lojas europeias | Slide sobre política de privacidade da GDPR apenas para a UE |
| **3** | Todas as lojas | Slides globais | "Frete grátis em pedidos >$50" (promoção corporativa) |

**Como o Escopo Funciona**:
- O terminal exibe slides correspondentes ao escopo da loja (slides específicos da loja)
- Mais slides correspondentes ao escopo do grupo (se a loja estiver em um grupo)
- Mais slides sem atribuição de escopo (slides globais)
- Resultado: A loja pode mostrar 3-5 slides (mistura de escopados e globais)

**Exemplo**:
- Slide global: "Novo Programa de Fidelidade - Participe Hoje!" (sem escopo)
- Slide do grupo: "Venda de Memorial Day - 30% de Desconto" (apenas grupo de lojas dos EUA)
- Slide da loja: "Grand Opening - Loja de Nova York" (apenas loja de Nova York)

**Terminal da Loja de Nova York** exibe todos os 3 slides (loja + grupo + global)
**Terminal da Loja de Londres** exibe apenas o slide global (não está no grupo de lojas dos EUA, nem é a loja de Nova York)

## Requisitos de Imagem

Slides de promoção são imagens em tela cheia otimizadas para monitores de exibição ao cliente:

**Proporção de Aspecto**: 16:9 (widescreen)

**Resolução Recomendada**: 1920×1080 pixels (Full HD)
- Escala limpa para a maioria das telas modernas
- Equilíbrio de tamanho do arquivo (qualidade vs velocidade de carregamento)

**Resoluções Aceitáveis**:
- Mínimo: 1280×720 (HD)
- Ótimo: 1920×1080 (Full HD)
- Máximo: 3840×2160 (4K) - não recomendado (tamanho de arquivo grande, carregamento mais lento)

**Formato do Arquivo**: JPG, PNG ou WebP
- JPG para fotografias
- PNG para gráficos com transparência (embora fundos sejam recomendados)
- WebP para o menor tamanho de arquivo

**Tamanho do Arquivo**: <500KB por slide
- Arquivos maiores atrasam o carregamento do carrossel
- Comprima as imagens antes de carregá-las (use a otimização da Biblioteca de Mídia)

**Recomendações de Design**:
- Alto contraste para legibilidade à distância (clientes a 2-6 pés da tela)
- Texto grande (mínimo 48pt para texto principal, 72pt+ para títulos)
- Fontes grossas (fontes finas desaparecem em algumas telas)
- Evite detalhes pequenos (não serão visíveis do ponto de vista do cliente)
- Inclua um call-to-action (o que o cliente deve fazer: "Pergunte ao caixa sobre os detalhes", "Cadastre-se hoje")

## Criando um Slide de Promoção

Navegue até **POS > Slides de Promoção** e clique em **+ Adicionar Slide de Promoção**:

![Formulário de Adição de Slide de Promoção](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Imagem** - Carregue ou selecione da Biblioteca de Mídia:
- Clique em **Procurar na Biblioteca de Mídia** para selecionar uma imagem existente
- Ou carregue uma nova imagem que atenda aos requisitos acima
- A pré-visualização mostra como a imagem aparecerá na tela

**Título** (Opcional) - Texto sobreposto no topo do slide:
- Máximo de 60 caracteres (texto mais longo é truncado)
- Aparece em uma barra escura semi-transparente no topo da imagem
- Use para o título do slide ("Venda de Verão", "Novidades")
- Deixe em branco se a imagem já incluir texto de título

**Subtítulo** (Opcional) - Texto sobreposto abaixo do título:
- Máximo de 120 caracteres
- Aparece abaixo do título na mesma barra semi-transparente
- Use para detalhes complementares ("Até 50% de desconto", "Presente grátis com compra")
- Deixe em branco se a imagem for autossuficiente

**Ativo** - Alternar para habilitar/desabilitar o slide:
- Apenas slides ativos aparecem no carrossel
- Use para ativação sazonal (desative após o fim da promoção)
- Desativar preserva o slide para reativação futura

**Ordem de Classificação** - Controla a posição do slide no carrossel:
- Números mais baixos aparecem primeiro na rotação
- Use múltiplos de 10: 10, 20, 30 (permite inserir slides entre existentes)
- Exemplo: Venda de feriado (ordem de classificação 10) aparece antes do programa de fidelidade geral (ordem de classificação 20)

**Atribuição de Escopo** (Opcional):
- **Armazém** - Selecione para mostrar apenas em uma loja específica
- **Grupo de Lojas** - Selecione para mostrar apenas em lojas do grupo
- **Deixe ambos em branco** - Mostra em todas as lojas (slide global)

## Ordem de Classificação e Fluxo do Carrossel

**Exemplo de Carrossel** (terminal da loja de Nova York):
- Slide 1 (ordem de classificação 10): "Grand Opening - Loja de Nova York" (específico da loja)
- Slide 2 (ordem de classificação 15): "Venda de Memorial Day - 30% de Desconto" (grupo de lojas dos EUA)
- Slide 3 (ordem de classificação 20): "Novo Programa de Fidelidade - Participe Hoje!" (global)
- Slide 4 (ordem de classificação 30): "Siga-nos @yourstore" (global)

O carrossel repete: 1 → 2 → 3 → 4 → 1 → 2 → ...

**Terminal da Loja de Londres** (não está no grupo de lojas dos EUA, loja diferente):
- Slide 1 (ordem de classificação 20): "Novo Programa de Fidelidade - Participe Hoje!" (global)
- Slide 2 (ordem de classificação 30): "Siga-nos @yourstore" (global)

O carrossel repete: 1 → 2 → 1 → 2 → ...

Use a ordem de classificação para priorizar o conteúdo mais importante primeiro na rotação.

## Estratégia de Ativação Sazonal

**Problema**: Criar/excluir slides para cada promoção sazonal é trabalhoso.

**Solução**: Crie slides uma vez, ative/desative sazonalmente:

1. **Crie Slides para Eventos Principais**:
   - "Venda de Verão" (Ativo: Não, criado com antecedência)
   - "Volta às Aulas" (Ativo: Não, criado com antecedência)
   - "Black Friday" (Ativo: Não, criado com antecedência)
   - "Venda de Feriados" (Ativo: Não, criado com antecedência)

2. **Ative Quando Relevante**:
   - 1 de junho: Defina "Venda de Verão" → Ativo: Sim
   - 15 de agosto: Defina "Venda de Verão" → Ativo: Não, defina "Volta às Aulas" → Ativo: Sim
   - 20 de novembro: Defina "Black Friday" → Ativo: Sim
   - 1 de dezembro: Defina "Black Friday" → Ativo: Não, defina "Venda de Feriados" → Ativo: Sim

3. **Desative Após o Evento**:
   - Mantém a biblioteca de slides organizada
   - Reutilize slides ano após ano (atualize a imagem se necessário, mantenha a configuração)

## Exemplos de Casos de Uso

**Caso de Uso 1: Promoção Sazonal**
- Imagem: Fundo vermelho com texto branco "VENDA DE VERÃO - ATÉ 60% DE DESCONTO"
- Título: "Venda de Verão"
- Subtítulo: "Até 50-60% de desconto em itens selecionados. Pergunte ao caixa sobre os detalhes."
- Escopo: Todas as lojas (global)
- Ordem de classificação: 10 (prioridade mais alta durante o verão)
- Ativo: Apenas junho a agosto

**Caso de Uso 2: Política da Loja**
- Imagem: Infográfico mostrando os passos da política de devoluções
- Título: "Devoluções Fáceis"
- Subtítulo: "30 dias com o recibo. Nenhuma pergunta feita."
- Escopo: Todas as lojas (global)
- Ordem de classificação: 40 (prioridade mais baixa do que promoções)
- Ativo: Todo o ano

**Caso de Uso 3: Lançamento de Novo Produto**
- Imagem: Foto do produto principal do novo item
- Título: "NOVO: Fones de Ouvido Sem Fio Pro"
- Subtítulo: "Agora disponível em lojas e online. $199,99"
- Escopo: Todas as lojas (global)
- Ordem de classificação: 5 (prioridade mais alta durante a semana de lançamento)
- Ativo: Apenas durante a semana de lançamento, depois desative

**Caso de Uso 4: Evento Local**
- Imagem: Cartaz de corrida de caridade local
- Título: "Apoie o Local"
- Subtítulo: "Junte-se a nós na Corrida da Comunidade no dia 15 de junho!"
- Escopo: Loja específica (apenas loja de Nova York)
- Ordem de classificação: 8 (prioridade para esta loja)
- Ativo: 2 semanas antes do evento

**Caso de Uso 5: Programa de Fidelidade**
- Imagem: Visual do cartão de fidelidade com exemplos de pontos
- Título: "Ganhe Recompensas"
- Subtítulo: "Participe do nosso programa de fidelidade e ganhe 1 ponto por $1 gasto"
- Escopo: Todas as lojas (global)
- Ordem de classificação: 30 (conteúdo permanente)
- Ativo: Todo o ano

## Gerenciamento de Slides

**Visualização da Lista de Slides**:
- Mostra todos os slides com pré-visualização da imagem, título, escopo e status
- Filtre por ativo/inativo
- Filtre por escopo (veja todos os slides globais, todos os slides de grupo, etc.)

**Ativação/Desativação em Lote**:
- Selecione vários slides na lista
- Use a ação de administração para ativar ou desativar todos de uma vez
- Útil para transições sazonais (desative todas as slides de verão, ative todas as slides de outono)

**Teste os Slides**:
- Após criar/atualizar um slide, navegue até o terminal POS
- Deixe o terminal ficar ocioso (sem transação)
- Verifique se o slide aparece no carrossel
- Confira a qualidade da imagem, legibilidade do texto sobreposto e o tempo de exibição

**Atualização de Slides Ativos**:
- As alterações têm efeito na próxima atualização do carrossel (geralmente <30 segundos)
- Não é necessário reiniciar os terminais

## Dicas

- **Projete para distância** - Os clientes veem a tela de 2-6 pés de distância; use texto grande e alto contraste
- **Mantenha a mensagem simples** - O slide é exibido por <10 segundos; uma mensagem clara por slide
- **Use desativação sazonal** - Crie uma vez, ative/desative anualmente em vez de recriar
- **Priorize com ordem de classificação** - As promoções mais importantes devem ter a menor ordem de classificação (aparecem primeiro)
- **Teste no hardware real** - A calibração de cor da tela varia; verifique se os slides parecem bons em seus monitores específicos
- **Limite o número de slides ativos** - 3-5 slides ativos por loja é ideal; 10+ slides significa que cada um aparece com pouca frequência
- **Inclua CTAs** - Diga aos clientes o que fazer ("Pergunte ao caixa", "Visite o site", "Escaneie o código QR no recibo")
- **Atualize regularmente** - Promoções antigas (vendas expiradas, eventos passados) reduzem a confiança dos clientes
- **Use escopo estrategicamente** - Promoções regionais (escopo de grupo) e eventos locais (escopo de loja) parecem mais relevantes do que conteúdo global constante

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.