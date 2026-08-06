---
title: Regras de Envio
---

As regras de envio aplicam ajustes de custo condicionais aos métodos de envio com base no conteúdo do carrinho, atributos do cliente e zonas de entrega: ofereça automaticamente envio gratuito acima de $50, adicione taxas para áreas remotas ou desconte o envio para clientes VIP. As regras usam execução baseada em prioridade (maior prioridade primeiro) com sinalizadores de parada opcionais para evitar processamento adicional. Cada regra avalia múltiplas condições (valor do carrinho, peso, zonas, produtos, grupos de clientes) e executa um dos 6 tipos de ajuste quando todas as condições forem atendidas.

Use regras de envio quando precisar de custos de envio dinâmicos que mudem com o contexto do pedido, e não apenas taxas fixas dos métodos de envio.

## Tipos de Regras de Envio

As regras de envio aplicam 6 tipos de ajustes de custo:

### Desconto Percentual

**O que Ele Faz**: Reduz o custo de envio em porcentagem (ex: 25% de desconto).

**Fórmula**: `novo_custo = custo_base × (1 - percentual/100)`

**Exemplo**:
```
Custo base: $20
Desconto: 25%
Resultado: $15
```

**Casos de Uso**:
- Desconto para cliente VIP (20% de desconto em todos os envios)
- Promoções sazonais (15% de desconto no envio em dezembro)
- Desconto para pedidos em massa (10% de desconto no envio para 5+ itens)

---

### Desconto Fixo

**O que Ele Faz**: Subtrai valor fixo do custo de envio.

**Fórmula**: `novo_custo = custo_base - valor` (mínimo $0)

**Exemplo**:
```
Custo base: $15
Desconto: $5
Resultado: $10
```

**Casos de Uso**:
- Bônus para cliente pela primeira vez ($5 de desconto no envio da primeira compra)
- Recompensa por inscrição na newsletter ($3 de desconto no envio)
- Benefício do programa de fidelidade ($10 de desconto no envio por mês)

---

### Custo Definido

**O que Ele Faz**: Substitui o custo de envio para um valor específico.

**Fórmula**: `novo_custo = valor_fixo`

**Exemplo**:
```
Custo base: $25
Definir para: $9.99
Resultado: $9.99
```

**Casos de Uso**:
- Venda com desconto (frete fixo de $5 para todos os pedidos hoje)
- Frete específico por categoria (livros sempre com frete de $3.99)
- Promoções com base no tempo (frete limitado a $9.99 esta semana)

---

### Frete Grátis

**O que Ele Faz**: Define o custo de envio para $0.

**Fórmula**: `novo_custo = $0`

**Exemplo**:
```
Custo base: $18
Regra aplicada
Resultado: $0
```

**Casos de Uso**:
- Frete grátis acima de $50
- Frete grátis para produtos específicos (itens promocionais)
- Frete grátis para clientes VIP
- Frete grátis em pedidos com 3+ itens

---

### Taxa Adicional (Fixa)

**O que Ele Faz**: Adiciona valor fixo ao custo de envio.

**Fórmula**: `novo_custo = custo_base + valor`

**Exemplo**:
```
Custo base: $12
Taxa: $5
Resultado: $17
```

**Casos de Uso**:
- Taxa de entrega em áreas remotas
- Tratamento de itens oversized
- Taxa de entrega no sábado
- Taxa de embalagem de itens frágeis

---

### Taxa Adicional (Percentual)

**O que Ele Faz**: Aumenta o custo de envio em porcentagem.

**Fórmula**: `novo_custo = custo_base × (1 + percentual/100)`

**Exemplo**:
```
Custo base: $20
Taxa: 15%
Resultado: $23
```

**Casos de Uso**:
- Taxa de pico sazonal (20% durante as férias)
- Premium de entrega expressa (taxa de 50%)
- Taxa de combustível (variável com base nas taxas atuais)

---

## Condições da Regra

As regras avaliam **todas as condições devem ser atendidas** para a regra ser aplicada:

### Validação de Tempo

- **Data de Início**: A regra só é ativa após esta data
- **Data de Fim**: A regra só é ativa antes desta data
- **Caso de Uso**: Promoções sazonais, ofertas por tempo limitado

**Exemplo**: Frete grátis no fim de semana de Black Friday apenas
```
Início: 2026-11-27 00:00
Fim: 2026-11-30 23:59
```

---

### Faixa de Valor do Carrinho

- **Valor Mínimo do Carrinho**: O subtotal do carrinho deve ser ≥ valor
- **Valor Máximo do Carrinho**: O subtotal do carrinho deve ser ≤ valor
- **Caso de Uso**: Limites de frete grátis, descontos em níveis

**Exemplo**: Frete grátis para pedidos de $50 a $200
```
Mínimo: $50
Máximo: $200
```

---

### Faixa de Peso do Carrinho

- **Peso Mínimo**: O peso total do carrinho deve ser ≥ valor
- **Peso Máximo**: O peso total do carrinho deve ser ≤ valor
- **Caso de Uso**: Descontos para envios leves, taxas para itens pesados

**Exemplo**: Taxa de $5 para pedidos acima de 20kg
```
Peso Mínimo: 20kg
Peso Máximo: null (ilimitado)
```

---

### Faixa de Quantidade de Itens


- **Min Item Count**: Carrinho deve ter ≥ quantidade de itens
- **Max Item Count**: Carrinho deve ter ≤ quantidade de itens
- **Caso de uso**: Descontos para pedidos em lote, taxas para itens únicos

**Exemplo**: Frete grátis para 5+ itens
```
Min Items: 5
Max Items: null
```


### Zona de Entrega

- **Zonas**: A regra se aplica somente se o endereço do cliente corresponder a pelo menos uma zona selecionada
- **Seleção vazia**: A regra se aplica a TODAS as zonas
- **Caso de uso**: Taxas ou descontos específicos da zona

**Exemplo**: Frete grátis somente para a zona Doméstica
```
Zones: ["Domestic USA"]
```


### Método de Entrega

- **Métodos**: A regra se aplica somente aos métodos de envio específicos
- **Seleção vazia**: A regra se aplica a TODOS os métodos
- **Caso de uso**: Promoções específicas do método

**Exemplo**: 25% de desconto no envio expresso
```
Methods: ["Express Delivery"]
```


### Requisitos de Produto

**Requer Produtos**: O carrinho deve conter pelo menos um desses produtos

**Requer Categorias**: O carrinho deve conter pelo menos um produto dessas categorias

**Caso de uso**: Frete grátis específico para produtos, pacotes promocionais

**Exemplo**: Frete grátis quando o carrinho contém "Produto de Promoção A"
```
Requires Products: [Produto ID 123]
```


### Exclusão de Produtos

**Exclui Produtos**: A regra não se aplica se o carrinho contiver algum desses produtos

**Exclui Categorias**: A regra não se aplica se o carrinho contiver produtos de alguma dessas categorias

**Caso de uso**: Excluir itens pesados/maiores do frete grátis

**Exemplo**: Frete grátis, exceto pela categoria Móveis
```
Excludes Categories: [Móveis]
```


### Grupo de Clientes

- **Grupos de Clientes**: A regra se aplica somente aos clientes nos grupos selecionados (VIP, Atacado, etc.)
- **Seleção vazia**: A regra se aplica a TODOS os grupos de clientes
- **Caso de uso**: Benefícios para VIP, descontos para atacado

**Exemplo**: Desconto de 15% no frete para membros VIP
```
Customer Groups: ["VIP"]
```


### Cliente Novato

- **Cliente Pela Primeira Vez**: Ative para restringir a regra a clientes sem pedidos anteriores
- **Caso de uso**: Ofertas de boas-vindas para novos clientes

**Exemplo**: $5 de desconto no frete para o primeiro pedido
```
First Time Customer: Yes
```


## Prioridade e Execução da Regra

As regras são executadas na **ordem de prioridade** (número maior = execução mais cedo):

### Mecânica de Prioridade

**Exemplo de Execução**:
```
Regra A (Prioridade 100): Frete grátis se o carrinho > $50
Regra B (Prioridade 50): Desconto de 10% em todos os envios
Regra C (Prioridade 1): Taxa de $2 para zonas remotas

Carrinho: $60, Zona remota
Custo base de envio: $15

Etapa 1: A Regra A é avaliada (Prioridade 100)
  Carrinho > $50? SIM
  Aplicar: Definir custo para $0
  Custo agora: $0

Etapa 2: A Regra B é avaliada (Prioridade 50)
  Aplicar desconto de 10% no $0
  Custo agora: $0 (ainda grátis)

Etapa 3: A Regra C é avaliada (Prioridade 1)
  Adicionar taxa de $2 no $0
  Custo agora: $2

Custo final: $2
```

**Flag de Parada de Regras Adicionais**:

Se a Regra A tiver `stop_further_rules = True`:
```
Regra A (Prioridade 100, stop_further_rules=True): Frete grátis se o carrinho > $50
Regra B (Prioridade 50): Desconto de 10% no envio
Regra C (Prioridade 1): Taxa de $2 para zonas remotas

Carrinho: $60
Base: $15

Etapa 1: A Regra A é aplicada, define o custo para $0
        stop_further_rules = True → PARAR

Custo final: $0 (Regras B e C nunca são executadas)
```


## Criando Regras de Frete

**Etapas do Fluxo de Trabalho**:

1. **Navegue até Regras**
   - Configurações > Frete > Regras de Frete
   - Clique em "Adicionar Regra de Frete"

2. **Configuração Básica**
   - **Nome**: Identificador interno (ex.: "Frete Grátis Acima de $50")
   - **Descrição**: Observações opcionais (não exibidas aos clientes)
   - **Ativo**: Ative/desative para habilitar/desabilitar
   - **Prioridade**: Defina a ordem de execução (100 para alta prioridade, 1 para baixa)

3. **Escolha o Tipo de Regra**
   - Selecione o tipo de ajuste (desconto %, desconto fixo, custo definido, grátis, taxa %, taxa fixa)
   - Insira o valor ou porcentagem

4. **Defina a Flag de Parada** (Opcional)
   - Marque "Parar Regras Adicionais" se essa regra deve impedir que regras de menor prioridade sejam executadas
   - Use para regras finais/absolutas (ex.: frete grátis não deve ter taxas adicionadas após)

5. **Definir Condições** (Opcional - deixe em branco para "aplicar sempre")
  - Validez de tempo: datas de início/fim
  - Valor do carrinho: Mín/Máx
  - Peso do carrinho: Mín/Máx
  - Quantidade de itens: Mín/Máx
  - Zonas: Selecione as zonas aplicáveis
  - Métodos: Selecione os métodos aplicáveis
  - Produtos: Necessários ou excluídos
  - Clientes: Grupos ou apenas pela primeira vez

6. **Salvar Regra**
  - Clique em Salvar
  - O regra entra em vigor imediatamente (se o interruptor ativo estiver em Sim)


## Cenários Comuns de Regras de Frete

### Cenário 1: Frete Grátis Acima de $50

**Objetivo**: Oferecer frete grátis quando o subtotal do carrinho ≥ $50.

**Configuração**:
```
Nome: Frete Grátis Acima de $50
Tipo: Frete Grátis
Prioridade: 100
Condições:
  Valor Mínimo do Carrinho: $50
Pare Regras Adicionais: Sim
```


### Cenário 2: Taxa por Área Remota

**Objetivo**: Adicionar taxa de $10 para entregas em zonas remotas.

**Configuração**:
```
Nome: Taxa por Área Remota
Tipo: Taxa (Fixa)
Valor: $10
Prioridade: 50
Condições:
  Zonas: ["Áreas Remotas"]
Pare Regras Adicionais: Não
```


### Cenário 3: Desconto de 20% para Clientes VIP

**Objetivo**: Clientes VIP recebem 20% de desconto em todos os fretes.

**Configuração**:
```
Nome: Desconto de Frete para VIP
Tipo: Desconto (Percentual)
Percentual: 20
Prioridade: 75
Condições:
  Grupos de Clientes: ["VIP"]
Pare Regras Adicionais: Não
```


### Cenário 4: Frete Fixo durante o Natal

**Objetivo**: Todos os fretes limitados a $9,99 durante dezembro.

**Configuração**:
```
Nome: Promoção de Frete Fixo de Dezembro
Tipo: Custo Definido
Valor: $9,99
Prioridade: 100
Condições:
  Data de Início: 2026-12-01
  Data de Fim: 2026-12-31
Pare Regras Adicionais: Sim
```


### Cenário 5: Taxa por Itens Pesados

**Objetivo**: Adicionar taxa de $15 para pedidos acima de 25kg.

**Configuração**:
```
Nome: Taxa por Pedido Pesado
Tipo: Taxa (Fixa)
Valor: $15
Prioridade: 50
Condições:
  Peso Mínimo: 25kg
Pare Regras Adicionais: Não
```


### Cenário 6: Frete Grátis na Primeira Compra

**Objetivo**: Clientes novos recebem frete grátis na primeira compra.

**Configuração**:
```
Nome: Frete Grátis na Primeira Compra
Tipo: Frete Grátis
Prioridade: 100
Condições:
  Cliente Novo: Sim
Pare Regras Adicionais: Sim
```


### Cenário 7: Frete Grátis por Categoria

**Objetivo**: Frete Grátis para pedidos que contenham itens da categoria promocional.

**Configuração**:
```
Nome: Frete Grátis por Categoria Promocional
Tipo: Frete Grátis
Prioridade: 90
Condições:
  Categorias Necessárias: ["Promoções"]
Pare Regras Adicionais: Sim
```


### Cenário 8: Excluir Móveis do Frete Grátis

**Objetivo**: Frete Grátis acima de $50, exceto se o carrinho contiver móveis.

**Solução**: Duas regras

**Regra 1**:
```
Nome: Frete Grátis Geral
Tipo: Frete Grátis
Prioridade: 50
Condições:
  Valor Mínimo do Carrinho: $50
  Exclui Categorias: ["Móveis"]
Pare Regras Adicionais: Não
```

**Regra 2**:
```
Nome: Desconto de $5 para Pedidos de Móveis
Tipo: Desconto (Fixo)
Valor: $5
Prioridade: 40
Condições:
  Categorias Necessárias: ["Móveis"]
  Valor Mínimo do Carrinho: $50
Pare Regras Adicionais: Não
```


## Estratégias de Combinação de Regras

### Estratégia 1: Descontos Empilháveis

**Permitir que múltiplos descontos sejam empilhados**:
```
Regra A (Prioridade 100): 10% de desconto para VIP → stop_further_rules=Não
Regra B (Prioridade 50): 15% de desconto em pedidos >$100 → stop_further_rules=Não

Cliente VIP com pedido de $120:
Base: $15
Após a Regra A: $13,50 (10% de desconto)
Após a Regra B: $11,48 (15% de desconto de $13,50)
```

### Estratégia 2: Regras Exclusivas

**Apenas uma regra se aplica** (maior prioridade):
```
Regra A (Prioridade 100): Frete Grátis >$50 → stop_further_rules=Sim
Regra B (Prioridade 50): 20% de desconto em todos os fretes → stop_further_rules=Sim

Carrinho > $50:
Regra A se aplica → Frete Grátis → PARAR
Regra B nunca é executada
```

### Estratégia 3: Taxas Condicionais

**Descontos primeiro, taxas por último**:
```
Regra A (Prioridade 100): Frete Grátis >$75
Regra B (Prioridade 75): 15% de desconto para VIP
Regra C (Prioridade 50): 10% de desconto geral
Regra D (Prioridade 25): $5 de taxa por área remota
Regra E (Prioridade 1): 10% de taxa de combustível

Pedido: $80, zona remota, cliente VIP
Base: $20
A: $80 > $75 → Frete Grátis ($0)
B: VIP → 15% de desconto de $0 = $0
C: 10% de desconto de $0 = $0
D: Remoto +$5 = $5
E: Combustível +10% de $5 = $5,50
```

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Final: R$5,50 (não é gratuito devido a taxas)
```

**Para evitar isso, use stop_further_rules=Sim**:
```
Regra A (Prioridade 100, stop=Sim): Frete grátis >$75

Mesmo pedido:
A: $80 > $75 → Frete Grátis ($0) → PARAR
Final: $0 (verdadeiramente gratuito)
```

---

## Testando Regras de Frete

**Antes de ir para produção**:

1. **Crie Carrinhos de Teste**
   - Carrinho A: $25 (abaixo do limite)
   - Carrinho B: $55 (acima do limite)
   - Carrinho C: $200 + zona remota
   - Carrinho D: Cliente VIP

2. **Teste Cada Regra**
   - Prossiga para o checkout
   - Verifique se o custo de frete correto é exibido
   - Confirme a ordem de execução das regras

3. **Teste a Resolução de Prioridade**
   - Múltiplas regras que se aplicam
   - Verifique se a maior prioridade é executada primeiro
   - Confirme o comportamento de stop_further_rules

4. **Teste Casos Extremos**
   - Valor do carrinho exatamente no limite
   - Múltiplas condições que se aplicam
   - Regras conflitantes

---

## Solução de Problemas

**Problema 1: Regra não está sendo aplicada**

**Causas**:
- A regra está inativa
- Uma ou mais condições não foram atendidas
- Uma regra com maior prioridade definida com stop_further_rules=Sim
- O período de validade está fora da data atual

**Solução**: Revise todas as condições, verifique a prioridade e confirme o status ativo.

---

**Problema 2: Desconto inesperado**

**Causas**:
- Múltiplas regras se acumulando
- Porcentagem aplicada a um custo já com desconto
- Prioridade incorreta da regra

**Solução**: Verifique a ordem de prioridade, revise as bandeiras stop_further_rules e rastreie manualmente a execução.

---

**Problema 3: Frete grátis não está funcionando**

**Causas**:
- Uma regra de taxa com menor prioridade adiciona custo após a regra de frete grátis
- O carrinho não atende ao valor mínimo
- Produtos excluídos no carrinho

**Solução**: Use stop_further_rules=Sim na regra de frete grátis, verifique as condições e confirme as exclusões.

---

## Dicas

- **Use alta prioridade para frete grátis** - Prioridade 100 garante que ela seja executada antes de outros ajustes
- **Defina stop_further_rules para regras absolutas** - Frete grátis deve parar o processamento adicional
- **Teste combinações de regras** - Múltiplas regras podem interagir de forma inesperada
- **Use nomes descritivos** - "Desconto VIP de 20% (Prioridade 75)" é melhor do que "Regra 3"
- **Documente lógica complexa** - Adicione observações no campo de descrição
- **Comece com regras simples** - Adicione complexidade gradualmente
- **Monitore o desempenho das regras** - Verifique se as regras estão sendo usadas ou causando confusão
- **Evite excesso de regras** - Muitas regras tornam o checkout lento, use no máximo 5-10
- **Use zonas para geografia** - Melhor do que múltiplas regras semelhantes por país
- **Combine com métodos** - Regras + Métodos funcionam juntos para precificação sofisticada
- **Defina janelas de horário claras** - Sempre inclua datas de término para promoções
- **Teste casos extremos** - Exatamente $50, exatamente 5 itens, etc.