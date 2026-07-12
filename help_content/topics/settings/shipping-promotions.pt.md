---
title: Promoções de Envio
---

Regras de envio aplicam ajustes condicionais de custo aos métodos de envio com base no conteúdo do carrinho, atributos do cliente e zonas de entrega — ofereça automaticamente envio gratuito acima de $50, adicione sobretaxas para áreas remotas ou desconte o envio para clientes VIP. As regras usam execução baseada em prioridade (prioridade mais alta primeiro) com bandeiras de parada opcionais para impedir o processamento adicional. Cada regra avalia múltiplas condições (valor do carrinho, peso, zonas, produtos, grupos de clientes) e executa um dos 6 tipos de ajuste quando todas as condições forem atendidas.

Use promoções de envio quando precisar de custos de envio dinâmicos que mudam com base no contexto do pedido, e não apenas em taxas estáticas dos métodos de envio.

## Tipos de Promoções de Envio

As regras de envio aplicam 6 tipos de ajustes de custo:

### Desconto em Percentual

**O que ele faz**: Reduz o custo de envio em percentual (ex.: 25% de desconto).

**Fórmula**: `new_cost = base_cost × (1 - percent/100)`

**Exemplo**:
```
Custo base: $20
Desconto: 25%
Resultado: $15
```

**Casos de uso**:
- Desconto para clientes VIP (20% de desconto em todos os envios)
- Promoções sazonais (15% de desconto no envio em dezembro)
- Desconto para pedidos em grande quantidade (10% de desconto no envio para 5+ itens)

---

### Desconto Fixo

**O que ele faz**: Subtrai um valor fixo do custo de envio.

**Fórmula**: `new_cost = base_cost - amount` (mínimo $0)

**Exemplo**:
```
Custo base: $15
Desconto: $5
Resultado: $10
```

**Casos de uso**:
- Bônus para clientes novos ($5 de desconto no envio do primeiro pedido)
- Recompensa por inscrição no boletim informativo ($3 de desconto no envio)
- Benefício do programa de fidelidade ($10 de desconto no envio por mês)

---

### Substituir Custo

**O que ele faz**: Substitui o custo de envio por um valor específico.

**Fórmula**: `new_cost = fixed_amount`

**Exemplo**:
```
Custo base: $25
Definir para: $9.99
Resultado: $9.99
```

**Casos de uso**:
- Venda flash (envio fixo de $5 para todos os pedidos hoje)
- Envio específico por categoria (livros sempre com envio de $3.99)
- Promoções baseadas no tempo (envio limitado a $9.99 nesta semana)

---

### Envio Grátis

**O que ele faz**: Define o custo de envio como $0.

**Fórmula**: `new_cost = $0`

**Exemplo**:
```
Custo base: $18
Regra aplicada
Resultado: $0
```

**Casos de uso**:
- Envio grátis acima de $50
- Envio grátis para produtos específicos (itens promocionais)
- Envio grátis para clientes VIP
- Envio grátis para pedidos com 3+ itens

---

### Sobretaxa (Fixa)

**O que ela faz**: Adiciona um valor fixo ao custo de envio.

**Fórmula**: `new_cost = base_cost + amount`

**Exemplo**:
```
Custo base: $12
Sobretaxa: $5
Resultado: $17
```

**Casos de uso**:
- Taxa de entrega para áreas remotas
- Taxa de manuseio de itens oversized
- Sobretaxa para entrega no sábado
- Taxa de embalagem para itens frágeis

---

### Sobretaxa (Percentual)

**O que ela faz**: Aumenta o custo de envio em percentual.

**Fórmula**: `new_cost = base_cost × (1 + percent/100)`

**Exemplo**:
```
Custo base: $20
Sobretaxa: 15%
Resultado: $23
```

**Casos de uso**:
- Sobretaxa de pico (20% durante as festas)
- Sobretaxa para entrega expressa (50% de sobretaxa)
- Sobretaxa de combustível (variável com base nas taxas atuais)

---

## Condições de Promoção

As promoções avaliam **TODAS as condições devem ser atendidas** para que a regra seja aplicada:

### Validade Temporal

- **Data de Início**: A regra só está ativa após essa data
- **Data de Fim**: A regra só está ativa antes dessa data
- **Casos de uso**: Promoções sazonais, ofertas limitadas no tempo

**Exemplo**: Envio grátis apenas no final de semana do Black Friday
```
Início: 2026-11-27 00:00
Fim: 2026-11-30 23:59
```

---

### Faixa de Valor do Carrinho

- **Valor Mínimo do Carrinho**: O subtotal do carrinho deve ser ≥ valor
- **Valor Máximo do Carrinho**: O subtotal do carrinho deve ser ≤ valor
- **Casos de uso**: Limites para envio grátis, descontos em níveis

**Exemplo**: Envio grátis para pedidos de $50 a $200
```
Mínimo: $50
Máximo: $200
```

---

### Faixa de Peso do Carrinho

- **Peso Mínimo**: O peso total do carrinho deve ser ≥ valor
- **Peso Máximo**: O peso total do carrinho deve ser ≤ valor
- **Casos de uso**: Descontos para envios leves, sobretaxas para itens pesados

**Exemplo**: Sobretaxa de $5 para pedidos acima de 20kg
```
Peso Mínimo: 20kg
Peso Máximo: null (ilimitado)
```

---

### Faixa de Quantidade de Itens


- **Min Item Count**: O carrinho deve ter ≥ quantidade de itens
- **Max Item Count**: O carrinho deve ter ≤ quantidade de itens
- **Use Case**: Descontos para pedidos em grande quantidade, taxas para itens únicos

**Exemplo**: Frete grátis para 5+ itens
```
Min Items: 5
Max Items: null
```

---

### Zona de Envio

- **Zones**: A regra só se aplica se o endereço do cliente corresponder a pelo menos uma zona selecionada
- **Empty selection**: A regra se aplica a TODAS as zonas
- **Use Case**: Sobretaxas ou descontos específicos de zona

**Exemplo**: Frete grátis apenas para a zona Doméstica
```
Zones: ["Domestic USA"]
```

---

### Método de Envio

- **Methods**: A regra só se aplica a métodos de envio específicos
- **Empty selection**: A regra se aplica a TODOS os métodos
- **Use Case**: Promoções específicas de método

**Exemplo**: 25% de desconto no envio Express
```
Methods: ["Express Delivery"]
```

---

### Requisitos do Produto

**Requires Products**: O carrinho deve conter pelo menos um desses produtos

**Requires Categories**: O carrinho deve conter pelo menos um produto dessas categorias

**Use Case**: Frete específico para produtos, pacotes promocionais

**Exemplo**: Frete grátis quando o carrinho contém "Item de Promoção A"
```
Requires Products: [Product ID 123]
```

---

### Exclusão de Produtos

**Excludes Products**: A regra não se aplica se o carrinho contiver qualquer um desses produtos

**Excludes Categories**: A regra não se aplica se o carrinho contiver qualquer produto dessas categorias

**Use Case**: Excluir itens pesados ou de tamanho excessivo do frete grátis

**Exemplo**: Frete grátis, exceto para a categoria Móveis
```
Excludes Categories: [Furniture]
```

---

### Grupo de Clientes

- **Customer Groups**: A regra só se aplica a clientes nos grupos selecionados (VIP, Atacado, etc.)
- **Empty selection**: A regra se aplica a TODOS os grupos de clientes
- **Use Case**: Benefícios VIP, descontos para atacado

**Exemplo**: Desconto de 15% no frete para membros VIP
```
Customer Groups: ["VIP"]
```

---

### Cliente Primeiro Tempo

- **First Time Customer**: Ative para restringir a regra a clientes sem pedidos anteriores
- **Use Case**: Ofertas de boas-vindas para novos clientes

**Exemplo**: $5 de desconto no frete para o primeiro pedido
```
First Time Customer: Yes
```

---

## Prioridade e Execução da Promoção

As promoções são executadas na **ordem de prioridade** (número mais alto = execução mais cedo):

### Mecânica de Prioridade

**Exemplo de Execução**:
```
Promotion A (Priority 100): Frete grátis se o carrinho > $50
Promotion B (Priority 50): 10% de desconto em todos os fretes
Promotion C (Priority 1): $2 de sobretaxa para zonas remotas

Carrinho: $60, Zona remota
Custo de frete base: $15

Passo 1: A promoção A é avaliada (Priority 100)
  Carrinho > $50? SIM
  Aplicar: Definir custo para $0
  Custo agora: $0

Passo 2: A promoção B é avaliada (Priority 50)
  Aplicar 10% de desconto em $0
  Custo agora: $0 (ainda grátis)

Passo 3: A promoção C é avaliada (Priority 1)
  Adicionar $2 de sobretaxa a $0
  Custo agora: $2

Custo final: $2
```

**Flag para Parar Promoções Posteriores**:

Se a promoção A tiver `stop_further_promotions = True`:
```
Promotion A (Priority 100, stop_further_promotions=True): Frete grátis se o carrinho > $50
Promotion B (Priority 50): 10% de desconto
Promotion C (Priority 1): $2 de sobretaxa

Carrinho: $60
Base: $15

Passo 1: A promoção A é aplicada, define o custo para $0
        stop_further_promotions = True → PARAR

Custo final: $0 (As regras B e C nunca são executadas)
```

---

## Criando Promoções de Envio

**Workflow passo a passo**:

1. **Navegue até as Regras**
   - Configurações > Envio > Promoções de Envio
   - Clique em "Adicionar Promoção de Envio"

2. **Configuração Básica**
   - **Name**: Identificador interno (ex: "Frete Grátis acima de $50")
   - **Description**: Notas opcionais (não mostradas aos clientes)
   - **Active**: Ative para habilitar/desabilitar
   - **Priority**: Defina a ordem de execução (100 para alta prioridade, 1 para baixa)

3. **Escolher Tipo de Promoção**
   - Selecione o tipo de ajuste (desconto %, desconto fixo, definir custo, grátis, sobretaxa %, sobretaxa fixa)
   - Insira o valor ou porcentagem


4. **Definir bandeira de parada** (Opcional)
   - Marque "Parar promoções futuras" se esta regra deve impedir que promoções de menor prioridade sejam executadas
   - Use para regras finais/absolutas (ex.: frete grátis não deve ter taxas adicionais aplicadas depois)

5. **Definir Condições** (Opcional - deixe vazio para "sempre aplicar")
   - Validade por tempo: datas de início/fim
   - Valor do carrinho: mínimo/máximo
   - Peso do carrinho: mínimo/máximo
   - Quantidade de itens: mínimo/máximo
   - Zonas: selecione zonas aplicáveis
   - Métodos: selecione métodos aplicáveis
   - Produtos: necessários ou excluídos
   - Cliente: grupos ou apenas primeiros compradores

6. **Salvar Regra**
   - Clique em Salvar
   - A regra se torna ativa imediatamente (se o interruptor de ativo estiver em Sim)

---

## Cenários Comuns de Promoção de Frete

### Cenário 1: Frete Grátis acima de $50

**Objetivo**: Oferecer frete grátis quando o subtotal do carrinho for ≥ $50.

**Configuração**:
```
Nome: Frete Grátis acima de $50
Tipo: Frete Grátis
Prioridade: 100
Condições:
  Valor Mínimo do Carrinho: $50
Parar Promoções Futuras: Sim
```

---

### Cenário 2: Taxa para Áreas Remotas

**Objetivo**: Adicionar uma taxa de $10 para entregas em zonas remotas.

**Configuração**:
```
Nome: Taxa para Áreas Remotas
Tipo: Taxa (Fixa)
Valor: $10
Prioridade: 50
Condições:
  Zonas: ["Áreas Remotas"]
Parar Promoções Futuras: Não
```

---

### Cenário 3: Desconto de 20% para Clientes VIP

**Objetivo**: Clientes VIP recebem 20% de desconto em todos os fretes.

**Configuração**:
```
Nome: Desconto de Frete VIP
Tipo: Desconto (Percentual)
Percentual: 20
Prioridade: 75
Condições:
  Grupos de Clientes: ["VIP"]
Parar Promoções Futuras: Não
```

---

### Cenário 4: Taxa Fixa de Natal

**Objetivo**: Limitar todos os fretes a $9,99 durante o mês de dezembro.

**Configuração**:
```
Nome: Promoção de Taxa Fixa de Dezembro
Tipo: Substituir Custo
Valor: $9,99
Prioridade: 100
Condições:
  Data de Início: 2026-12-01
  Data de Fim: 2026-12-31
Parar Promoções Futuras: Sim
```

---

### Cenário 5: Taxa para Itens Pesados

**Objetivo**: Adicionar uma taxa de $15 para pedidos com mais de 25kg.

**Configuração**:
```
Nome: Taxa para Pedidos Pesados
Tipo: Taxa (Fixa)
Valor: $15
Prioridade: 50
Condições:
  Peso Mínimo: 25kg
Parar Promoções Futuras: Não
```

---

### Cenário 6: Frete Grátis para Primeiro Pedido

**Objetivo**: Novos clientes recebem frete grátis no primeiro pedido.

**Configuração**:
```
Nome: Frete Grátis para Primeiro Pedido
Tipo: Frete Grátis
Prioridade: 100
Condições:
  Cliente Primeiro Tempo: Sim
Parar Promoções Futuras: Sim
```

---

### Cenário 7: Frete Grátis para Categorias Específicas

**Objetivo**: Frete grátis para pedidos que contenham itens da categoria promocional.

**Configuração**:
```
Nome: Frete Grátis para Categoria Promocional
Tipo: Frete Grátis
Prioridade: 90
Condições:
  Requer Categorias: ["Promoções"]
Parar Promoções Futuras: Sim
```

---

### Cenário 8: Excluir Móveis do Frete Grátis

**Objetivo**: Frete grátis acima de $50, exceto se o carrinho contiver móveis.

**Solução**: Duas regras

**Promoção 1**:
```
Nome: Frete Grátis Geral
Tipo: Frete Grátis
Prioridade: 50
Condições:
  Valor Mínimo do Carrinho: $50
  Exclui Categorias: ["Móveis"]
Parar Promoções Futuras: Não
```

**Promoção 2**:
```
Nome: Desconto de $5 para Pedidos de Móveis
Tipo: Desconto (Fixo)
Valor: $5
Prioridade: 40
Condições:
  Requer Categorias: ["Móveis"]
  Valor Mínimo do Carrinho: $50
Parar Promoções Futuras: Não
```

---

## Estratégias de Combinar Promoções

### Estratégia 1: Acumular Descontos

**Permitir que múltiplos descontos sejam acumulados**:
```
Promoção A (Prioridade 100): 10% de desconto para VIP → stop_further_promotions=Não
Promoção B (Prioridade 50): 15% de desconto para pedidos >$100 → stop_further_promotions=Não

Cliente VIP com pedido de $120:
Base: $15
Após Promoção A: $13,50 (10% de desconto)
Após Promoção B: $11,48 (15% de desconto sobre $13,50)
```

### Estratégia 2: Regras Exclusivas

**Apenas uma regra se aplica** (prioridade mais alta):
```
Promoção A (Prioridade 100): Frete grátis >$50 → stop_further_promotions=Sim
Promoção B (Prioridade 50): 20% de desconto em todos os fretes → stop_further_promotions=Sim

Carrinho > $50:
Promoção A aplica → Frete grátis → PARAR
Promoção B nunca é executada
```

### Estratégia 3: Taxas Condicionais


**Descontos primeiro, cobranças adicionais por último**:
```
Promoção A (Prioridade 100): Frete grátis >$75
Promoção B (Prioridade 75): Desconto VIP de 15%
Promoção C (Prioridade 50): Desconto geral de 10%
Promoção D (Prioridade 25): Cobrança de área remota de $5
Promoção E (Prioridade 1): Cobrança de combustível de 10%

Pedido: $80, Zona remota, cliente VIP
Base: $20
A: $80 > $75 → Frete grátis ($0)
B: VIP → 15% de $0 = $0
C: 10% de $0 = $0
D: Zona remota +$5 = $5
E: Combustível +10% de $5 = $5,50

Final: $5,50 (não gratuito devido às cobranças adicionais)
```

**Para evitar isso, use stop_further_promotions=Yes**:
```
Promoção A (Prioridade 100, stop=Yes): Frete grátis >$75

Mesmo pedido:
A: $80 > $75 → Frete grátis ($0) → PARAR
Final: $0 (verdadeiramente gratuito)
```

---

## Testando promoções de frete

**Antes de ir ao ar**:

1. **Crie carrinhos de teste**
   - Carrinho A: $25 (abaixo do limite)
   - Carrinho B: $55 (acima do limite)
   - Carrinho C: $200 + Zona remota
   - Carrinho D: Cliente VIP

2. **Teste cada regra**
   - Proceda para o checkout
   - Verifique se o custo de frete exibido está correto
   - Verifique a ordem de execução das regras

3. **Teste a resolução de prioridade**
   - Múltiplas regras correspondentes
   - Verifique se a regra com maior prioridade é executada primeiro
   - Verifique o comportamento de stop_further_promotions

4. **Teste casos extremos**
   - Valor do carrinho exatamente no limite
   - Múltiplas condições correspondentes
   - Regras conflitantes

---

## Solução de problemas

**Problema 1: Promoção não está sendo aplicada**

**Causas**:
- A regra está inativa
- Uma ou mais condições não estão sendo atendidas
- Uma regra com prioridade mais alta tem stop_further_promotions=Yes
- A validade da regra está fora da data atual

**Solução**: Revise todas as condições, verifique a prioridade, confirme o status ativo.

---

**Problema 2: Valor do desconto inesperado**

**Causas**:
- Múltiplas promoções se acumulando
- Percentual aplicado ao custo já descontado
- Prioridade da regra incorreta

**Solução**: Verifique a ordem de prioridade, revise os indicadores de stop_further_promotions, trace a execução manualmente.

---

**Problema 3: Frete grátis não está funcionando**

**Causas**:
- Uma regra de cobrança adicional com prioridade mais baixa está adicionando custo após a promoção de frete grátis
- O carrinho não atende ao limite mínimo de valor
- Produtos excluídos no carrinho

**Solução**: Use stop_further_promotions=Yes na promoção de frete grátis, verifique as condições, verifique as exclusões.

---

## Dicas

- **Use alta prioridade para frete grátis** - Prioridade 100 garante que ela seja executada antes de outras ajustes
- **Defina stop_further_promotions para regras absolutas** - O frete grátis deve parar o processamento adicional
- **Teste combinações de regras** - Múltiplas promoções podem interagir de forma inesperada
- **Use nomes descritivos** - "Desconto VIP de 20% (Prioridade 75)" é melhor que "Promoção 3"
- **Documente lógica complexa** - Adicione notas no campo de descrição
- **Comece com promoções simples** - Adicione complexidade gradualmente
- **Monitore o desempenho das regras** - Verifique se as regras estão sendo usadas ou causando confusão
- **Evite excesso de promoções** - Muitas promoções atrasam o checkout, use 5-10 no máximo
- **Use zonas para geografia** - É melhor que múltiplas regras semelhantes por país
- **Combine com métodos** - Regras + Métodos funcionam juntos para precificação sofisticada
- **Defina janelas de tempo claras** - Sempre inclua datas de término para promoções
- **Teste casos extremos** - Exatamente $50, exatamente 5 itens, etc.