---
title: Solicitações de Devolução & Processamento
---

As solicitações de devolução acompanham as devoluções dos clientes desde o início até a conclusão do reembolso — os clientes selecionam itens para devolver com razões, os vendedores aprovam ou rejeitam as solicitações, geram rótulos de devolução, inspecionam os itens devolvidos e processam os reembolsos. O fluxo de trabalho avança por 9 estágios de status (pendente → aprovado → rótulo_enviado → em_transito → recebido → inspecionado → concluído/rejeitado/cancelado) com razões de devolução por item, notas de inspeção e taxas de reposição opcionais.

Use esta página de administração para revisar, aprovar e processar solicitações de devolução dos clientes de forma eficiente.

## Fluxo de Trabalho de Solicitações de Devolução

**Processo de 9 Etapas**:

### 1. Pendente (Cliente Inicia)

Cliente envia solicitação de devolução:
- Seleciona itens do pedido
- Fornece razão de devolução por item
- Notas do cliente (opcionais)
- Status: `pendente`

### 2. Aprovado/Rejeitado (Vendedor Revisa)

Vendedor revisa a solicitação:
- **Aprovar**: Devolução permitida, prosseguir para geração do rótulo
- **Rejeitar**: Devolução negada com razão de rejeição
- Status: `aprovado` ou `rejeitado`

### 3. Rótulo Enviado (Envio de Devolução)

Rótulo de devolução gerado:
- Vendedor cria envio de devolução (opcional)
- Rótulo de devolução é enviado por e-mail ao cliente
- Cliente envia os itens de volta
- Status: `rótulo_enviado`

### 4. Em Trânsito (Cliente Envia)

Cliente envia os itens:
- Rastreamento mostra movimento
- Atualização automática de status a partir do webhook do transportador
- Status: `em_transito`

### 5. Recebido (Chega no Armazém)

Itens chegam:
- O armazém escaneia o envio
- Itens são verificados
- Status: `recebido`

### 6. Inspecionado (Verificação de Qualidade)

Vendedor inspeciona os itens:
- Registra o estado do item (excelente/bom/aceitável/estragado/defeituoso)
- Adicione notas de inspeção
- Aplique taxa de reposição se aplicável
- Status: `inspecionado`

### 7. Concluído (Processamento do Reembolso)

Reembolso emitido:
- Crie reembolso associado
- Pagamento processado
- Devolução fechada
- Status: `concluído`

**Resultados Alternativos**:
- **Cancelado**: Cliente cancela antes do envio
- **Rejeitado**: Vendedor nega após revisão

---

## Processamento de Solicitações de Devolução

**Passo a Passo**:

**Passo 1: Revisar Solicitações Pendentes**
- Navegue até Pedidos > Solicitações de Devolução
- Filtrar por status = "Pendente"
- Clique na solicitação para visualizar detalhes

**Passo 2: Avaliar Solicitação**
- Revisar detalhes do pedido
- Verificar razões de devolução
- Verificar conformidade com a política de devolução (dentro do período de devolução, itens elegíveis)

**Passo 3: Aprovar ou Rejeitar**
- Clique em "Aprovar" para aceitar a devolução
- OU clique em "Rejeitar" e insira a razão da rejeição
- Salve a decisão

**Passo 4: Gerar Rótulo de Devolução** (se aprovado)
- Clique em "Criar Envio de Devolução"
- Selecione transportadora/serviço
- O sistema gera o rótulo de devolução
- O rótulo é automaticamente enviado por e-mail ao cliente
- Status → `rótulo_enviado`

**Passo 5: Monitorar Trânsito**
- Atualizações de rastreamento sincronizadas automaticamente a partir do webhook do transportador
- Status avança automaticamente para `em_transito` quando o transportador escanear o pacote

**Passo 6: Receber Itens**
- Quando os itens chegarem, clique em "Marcar como Recebido"
- Status → `recebido`

**Passo 7: Inspeção dos Itens**
- Abra a solicitação de devolução
- Selecione o estado do item a partir do menu suspenso:
  - Excelente (como novo, reembalável)
  - Bom (uso mínimo, reembalável)
  - Aceitável (desgaste visível, reembalável com desconto)
  - Estragado (não reembalável)
  - Defeituoso (defeito de fabricação)
- Adicione notas de inspeção
- Opcional: Aplique taxa de reposição (percentual ou fixa)
- Status → `inspecionado`

**Passo 8: Processar Reembolso**
- Clique em "Criar Reembolso"
- O sistema calcula o valor do reembolso:
  - Preço original do item
  - Menos taxa de reposição (se aplicável)
  - Menos custo de envio (se não reembolsável)
- Crie reembolso (vinculado à solicitação de devolução)
- Status → `concluído`

---

## Razões de Devolução por Item

Os clientes selecionam a razão por item:

**Razões Comuns**:
- Item errado recebido
- Item defeituoso/estragado
- Mudou de opinião/não precisa mais
- Item não corresponde à descrição
- Encontrou um preço melhor
- Pedido por engano
- Qualidade não conforme o esperado

**Use Razões Para**:
- Análise (rastrear causas comuns de devoluções)
- Controle de qualidade (identificar produtos defeituosos)
- Melhoria de processos (reduzir devoluções evitáveis)

---

## Taxas de Reposição

Aplique taxas para compensar custos de processamento de devoluções:

**Configuração**:
- **Tipo**: Percentual (ex., 15%) ou Fixo (ex., $5)
- **Quando aplicar**: Devoluções sem defeito, itens abertos, pedidos especiais

**Exemplo**:
```
Compra original: $100
Taxa de reposição: 15%
Valor do reembolso: $85
```

**Melhores Práticas**:
- Comunique claramente a política de taxas de reposição
- Não aplique a itens defeituosos
- Considere isentar para clientes VIP

---

## Diretrizes de Inspeção de Devoluções

Estabeleça critérios de inspeção consistentes:

**Excelente**:
- Embalagem original não aberta
- Nenhum desgaste visível
- Todos os acessórios incluídos
- Totalmente reembalável ao preço integral

**Bom**:
- Aberto, mas uso mínimo
- Desgaste mínimo da embalagem
- Todos os componentes presentes
- Reembalável ao preço integral

**Aceitável**:
- Uso/ desgaste visível
- Embalagem danificada
- Acessórios não essenciais ausentes
- Reembalável com desconto

**Estragado**:
- Danificado fisicamente
- Peças faltando
- Não reembalável
- Necessário descartar ou reparar

**Defeituoso**:
- Defeito de fabricação
- Falha funcional
- Reivindicação de garantia
- Devolver ao fabricante

---

## Opções de Envio de Devoluções

**Opção 1: Cliente Paga o Envio de Devolução**
- Nenhum rótulo de devolução fornecido
- Cliente seleciona próprio transportador
- Entrada manual do número de rastreamento

**Opção 2: Vendedor Fornece Rótulo Pré-pago**
- Gerar rótulo de devolução por meio da conta do provedor
- Custo deduzido do reembolso OU vendedor absorve
- Rastreamento sincronizado automaticamente

**Opção 3: Envio de Devolução Grátis**
- Vendedor absorve o custo de envio de devolução
- Melhora a satisfação do cliente
- Aumenta a taxa de devoluções (considere o equilíbrio)

---

## Filtragem & Relatórios

**Filtros Úteis**:
- Status: Pendente (precisa de ação)
- Faixa de datas: Últimos 30 dias
- Pedido: Pesquisa por pedido específico
- Razão: Rastrear causas de devoluções

**Análise de Devoluções**:
- Taxa de devolução por produto
- Principais razões de devolução
- Tempo médio de processamento (pendente → concluído)
- Receita de taxas de reposição

---

## Dicas

- **Estabeleça uma política clara de devolução** - Comunique o período (30 dias), condições, taxas
- **Processar solicitações com rapidez** - Responda a solicitações pendentes dentro de 24 horas
- **Inspecione detalhadamente** - Documente o estado para evitar disputas
- **Rastrear razões de devolução** - Use os dados para melhorar produtos/descrições
- **Automatize onde possível** - Webhooks de transportador atualizam automaticamente o status de trânsito
- **Comunique-se com os clientes** - Envie atualizações por e-mail em cada mudança de status
- **Seja justo com taxas de reposição** - Aplique consistentemente, isentar para defeitos
- **Monitore fraudes de devolução** - Marque clientes com excesso de devoluções
- **Melhore o embalagem** - Reduza devoluções relacionadas a danos
- **Atualize o estoque com rapidez** - Restabeleça o estoque após inspeção
- **Aprenda com padrões** - Alta taxa de devoluções para produtos específicos pode indicar problema de qualidade
