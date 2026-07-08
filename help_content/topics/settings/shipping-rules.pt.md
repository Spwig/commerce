---
title: Regras de Envio
---

Regras de envio aplicam ajustes condicionais de custo aos métodos de envio com base no conteúdo do carrinho, atributos do cliente e zonas de entrega — oferecem automaticamente envio gratuito acima de $50, adicionam sobretaxas para áreas remotas ou descontam o envio para clientes VIP. As regras usam execução baseada em prioridade (maior prioridade primeiro) com bandeiras de parada opcionais para impedir o processamento adicional. Cada regra avalia múltiplas condições (valor do carrinho, peso, zonas, produtos, grupos de clientes) e executa um dos 6 tipos de ajuste quando todas as condições forem atendidas.

Use regras de envio quando você precisar de custos de envio dinâmicos que mudam com base no contexto do pedido, e não apenas em taxas estáticas dos métodos de envio.

## Tipos de Regras de Envio

Regras de envio aplicam 6 tipos de ajustes de custo:

### Desconto em Percentual

**O que ele faz**: Reduz o custo de envio em percentual (exemplo: 25% de desconto).

**Fórmula**: `new_cost = base_cost × (1 - percent/100)`

**Exemplo**:
```
Custo base: $20
Desconto: 25%
Resultado: $15
```

**Casos de uso**:
- Desconto para clientes VIP (20% de desconto em todos os envios)
- Promoções sazonais (15% de desconto em envios em dezembro)
- Desconto para pedidos em grande quantidade (10% de desconto em envios para 5+ itens)

---

### Desconto Fixo

**O que ele faz**: Subtrai uma quantidade fixa do custo de envio.

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

### Custo Fixo

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

**O que ela faz**: Adiciona uma quantidade fixa ao custo de envio.

**Fórmula**: `new_cost = base_cost + amount`

**Exemplo**:
```
Custo base: $12
Sobretaxa: $5
Resultado: $17
```

**Casos de uso**:
- Taxa de entrega para áreas remotas
- Custo de manuseio de itens oversized
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
- Sobretaxa de pico (20% durante feriados)
- Sobretaxa para entrega expressa (50% de sobretaxa)
- Sobretaxa de combustível (variável com base nas taxas atuais)

---

## Condições da Regra

As regras avaliam **Todas as condições devem ser atendidas** para que a regra seja aplicada:

### Validade Temporal

- **Data de início**: A regra só está ativa após essa data
- **Data de término**: A regra só está ativa antes dessa data
- **Caso de uso**: Promoções sazonais, ofertas com tempo limitado

**Exemplo**: Envio grátis apenas no final de semana do Black Friday
```
Início: 2026-11-27 00:00
Término: 2026-11-30 23:59
```

---

### Faixa de Valor do Carrinho

- **Valor mínimo do carrinho**: O subtotal do carrinho deve ser ≥ valor
- **Valor máximo do carrinho**: O subtotal do carrinho deve ser ≤ valor
- **Caso de uso**: Limites para envio grátis, descontos em níveis

**Exemplo**: Envio grátis para pedidos de $50 a $200
```
Mínimo: $50
Máximo: $200
```

---

### Faixa de Peso do Carrinho

- **Peso mínimo**: O peso total do carrinho deve ser ≥ valor
- **Peso máximo**: O peso total do carrinho deve ser ≤ valor
- **Caso de uso**: Descontos para envios leves, sobretaxas para itens pesados

**Exemplo**: Sobretaxa de $5 para pedidos acima de 20kg
```
Peso mínimo: 20kg
Peso máximo: null (ilimitado)
```

---

### Faixa de Quantidade de Itens

- **Quantidade mínima de itens**: O carrinho deve ter ≥ quantidade de itens
- **Quantidade máxima de itens**: O carrinho deve ter ≤ quantidade de itens
- **Caso de uso**: Descontos para pedidos em grande quantidade, taxas para itens únicos

**Exemplo**: Envio grátis para 5+ itens
```
Itens mínimos: 5
Itens máximos: null
```

---

### Zona de Envio

- **Zonas**: A regra só se aplica se o endereço do cliente corresponder a pelo menos uma zona selecionada
- **Seleção vazia**: A regra se aplica a TODAS as zonas
- **Caso de uso**: Sobretaxas ou descontos específicos de zona

**Exemplo**: Envio grátis apenas para a zona Doméstica
```
Zonas: ["Doméstico EUA"]
```

---

### Método de Envio

- **Métodos**: A regra só se aplica a métodos de envio específicos
- **Seleção vazia**: A regra se aplica a TODOS os métodos
- **Caso de uso**: Promoções específicas de método

**Exemplo**: 25% de desconto no envio Express
```
Métodos: ["Entrega Express"]
```

---

### Requisitos de Produto

**Requer produtos**: O carrinho deve conter pelo menos um desses produtos

**Requer categorias**: O carrinho deve conter pelo menos um produto dessas categorias

**Caso de uso**: Envio grátis específico para produtos, pacotes promocionais

**Exemplo**: Envio grátis quando o carrinho contém "Item de Promoção A"
```
Requer produtos: [ID do Produto 123]
```

---

### Exclusão de Produtos

**Exclui produtos**: A regra não se aplica se o carrinho contiver qualquer um desses produtos

**Exclui categorias**: A regra não se aplica se o carrinho contiver qualquer produto dessas categorias

**Caso de uso**: Excluir itens pesados/oversized do envio grátis

**Exemplo**: Envio grátis, exceto para a categoria Móveis
```
Exclui categorias: [Móveis]
```

---

### Grupo de Cliente

- **Grupos de clientes**: A regra só se aplica a clientes nos grupos selecionados (VIP, Atacado, etc.)
- **Seleção vazia**: A regra se aplica a TODOS os grupos de clientes
- **Caso de uso**: Benefícios VIP, descontos de atacado

**Exemplo**: Desconto de 15% no envio para membros VIP
```
Grupos de clientes: ["VIP"]
```

---

### Cliente Primeiro Pedido

- **Cliente primeiro pedido**: Alternar para restringir a regra a clientes sem pedidos anteriores
- **Caso de uso**: Ofertas de boas-vindas para novos clientes

**Exemplo**: $5 de desconto no envio para o primeiro pedido
```
Cliente primeiro pedido: Sim
```

---

## Prioridade e Execução da Regra

As regras são executadas em **ordem de prioridade** (número maior = execução mais cedo):

### Mecânica de Prioridade

**Exemplo de execução**:
```
Regra A (Prioridade 100): Envio grátis se o carrinho > $50
Regra B (Prioridade 50): 10% de desconto em todos os envios
Regra C (Prioridade 1): Sobretaxa de $2 para zonas remotas

Carrinho: $60, Zona remota
Custo de envio base: $15

Passo 1: Regra A é avaliada (Prioridade 100)
  Carrinho > $50? SIM
  Aplicar: Definir custo para $0
  Custo agora: $0

Passo 2: Regra B é avaliada (Prioridade 50)
  Aplicar 10% de desconto a $0
  Custo agora: $0 (ainda grátis)

Passo 3: Regra C é avaliada (Prioridade 1)
  Adicionar sobretaxa de $2 a $0
  Custo agora: $2

Custo final: $2
```

**Bandeira de Parada de Regras Adicionais**:

Se a Regra A tiver `stop_further_rules = True`:
```
Regra A (Prioridade 100, stop_further_rules=True): Envio grátis se o carrinho > $50
Regra B (Prioridade 50): 10% de desconto
Regra C (Prioridade 1): Sobretaxa de $2

Carrinho: $60
Custo base: $15

Passo 1: Regra A aplica, define custo para $0
        stop_further_rules = True → PARAR

Custo final: $0 (Regras B e C nunca são executadas)
```

---

## Criando Regras de Envio

**Fluxo de Trabalho Passo a Passo**:

1. **Navegue até as Regras**
   - Configurações > Envio > Regras de Envio
   - Clique em "Adicionar Regra de Envio"

2. **Configuração Básica**
   - **Nome**: Identificador interno (exemplo: "Envio Grátis Acima de $50")
   - **Descrição**: Notas opcionais (não mostradas aos clientes)
   - **Ativo**: Alternar para habilitar/desabilitar
   - **Prioridade**: Defina a ordem de execução (100 para alta prioridade, 1 para baixa)

3. **Escolher Tipo de Regra**
   - Selecione o tipo de ajuste (desconto %, desconto fixo, custo fixo, grátis, sobretaxa %, sobretaxa fixa)
   - Insira o valor ou percentual

4. **Definir Bandeira de Parada** (Opcional)
   - Marque "Parar Regras Adicionais" se essa regra deve impedir que regras de menor prioridade sejam executadas
   - Use para regras finais/absolutas (exemplo: envio grátis não deve ter sobretaxas adicionadas depois)

5. **Definir Condições** (Opcional - deixe vazio para "sempre aplicar")
   - Validade temporal: datas de início/fim
   - Valor do carrinho: mínimo/máximo
   - Peso do carrinho: mínimo/máximo
   - Quantidade de itens: mínimo/máximo
   - Zonas: selecione zonas aplicáveis
   - Métodos: selecione métodos aplicáveis
   - Produtos: requisitos ou exclusões
   - Cliente: grupos ou apenas primeiro pedido

6. **Salvar Regra**
   - Clique em Salvar
   - A regra se torna ativa imediatamente (se o toggle ativo estiver em Sim)

---

## Cenários Comuns de Regras de Envio

### Cenário 1: Envio Grátis Acima de $50

**Objetivo**: Oferecer envio grátis quando o subtotal do carrinho ≥ $50.

**Configuração**:
```
Nome: Envio Grátis Acima de $50
Tipo: Envio Grátis
Prioridade: 100
Condições:
  Valor mínimo do carrinho: $50
Parar regras adicionais: Sim
```

---

### Cenário 2: Sobretaxa para Áreas Remotas

**Objetivo**: Adicionar uma sobretaxa de $10 para entregas em áreas remotas.

**Configuração**:
```
Nome: Sobretaxa para Áreas Remotas
Tipo: Sobretaxa (Fixa)
Valor: $10
Prioridade: 50
Condições:
  Zonas: ["Áreas Remotas"]
Parar regras adicionais: Não
```

---

### Cenário 3: Desconto de 20% para Clientes VIP

**Objetivo**: Clientes VIP recebem 20% de desconto em todos os envios.

**Configuração**:
```
Nome: Desconto de Envio para VIP
Tipo: Desconto (Percentual)
Percentual: 20
Prioridade: 75
Condições:
  Grupos de clientes: ["VIP"]
Parar regras adicionais: Não
```

---

### Cenário 4: Taxa Fixa em Dezembro

**Objetivo**: Limitar todos os envios a $9.99 durante o mês de dezembro.

**Configuração**:
```
Nome: Promoção de Taxa Fixa em Dezembro
Tipo: Custo Fixo
Valor: $9.99
Prioridade: 100
Condições:
  Data de início: 2026-12-01
  Data de término: 2026-12-31
Parar regras adicionais: Sim
```

---

### Cenário 5: Sobretaxa para Itens Pesados

**Objetivo**: Adicionar uma taxa de $15 para pedidos acima de 25kg.

**Configuração**:
```
Nome: Sobretaxa para Pedidos Pesados
Tipo: Sobretaxa (Fixa)
Valor: $15
Prioridade: 50
Condições:
  Peso mínimo: 25kg
Parar regras adicionais: Não
```

---

### Cenário 6: Envio Grátis para Primeiro Pedido

**Objetivo**: Novos clientes recebem envio grátis no primeiro pedido.

**Configuração**:
```
Nome: Envio Grátis para Primeiro Pedido
Tipo: Envio Grátis
Prioridade: 100
Condições:
  Cliente primeiro pedido: Sim
Parar regras adicionais: Sim
```

---

### Cenário 7: Envio Grátis para Categoria Promocional

**Objetivo**: Envio grátis para pedidos contendo itens da categoria promocional.

**Configuração**:
```
Nome: Envio Grátis para Categoria Promocional
Tipo: Envio Grátis
Prioridade: 90
Condições:
  Requer categorias: ["Promoções"]
Parar regras adicionais: Sim
```

---

### Cenário 8: Excluir Móveis do Envio Grátis

**Objetivo**: Envio grátis acima de $50, exceto se o carrinho contiver móveis.

**Solução**: Duas regras

**Regra 1**:
```
Nome: Envio Grátis Geral
Tipo: Envio Grátis
Prioridade: 50
Condições:
  Valor mínimo do carrinho: $50
  Exclui categorias: ["Móveis"]
Parar regras adicionais: Não
```

**Regra 2**:
```
Nome: Desconto de $5 para Pedidos de Móveis
Tipo: Desconto (Fixo)
Valor: $5
Prioridade: 40
Condições:
  Requer categorias: ["Móveis"]
  Valor mínimo do carrinho: $50
Parar regras adicionais: Não
```

---

## Estratégias de Combinar Regras

### Estratégia 1: Empilhar Descontos

**Permitir que múltiplos descontos sejam empilhados**:
```
Regra A (Prioridade 100): 10% de desconto para VIP → stop_further_rules=Não
Regra B (Prioridade 50): 15% de desconto para pedidos >$100 → stop_further_rules=Não

Cliente VIP com pedido de $120:
Custo base: $15
Após a Regra A: $13.50 (10% de desconto)
Após a Regra B: $11.48 (15% de desconto de $13.50)
```

### Estratégia 2: Regras Exclusivas

**Apenas uma regra se aplica** (maior prioridade):
```
Regra A (Prioridade 100): Envio grátis >$50 → stop_further_rules=Sim
Regra B (Prioridade 50): 20% de desconto em todos os envios → stop_further_rules=Sim

Carrinho > $50:
Regra A aplica → Envio grátis → PARAR
Regra B nunca é executada
```

### Estratégia 3: Sobretaxas Condicionais

**Descontos primeiro, sobretaxas depois**:
```
Regra A (Prioridade 100): Envio grátis >$75
Regra B (Prioridade 75): 15% de desconto VIP
Regra C (Prioridade 50): 10% de desconto geral
Regra D (Prioridade 25): Sobretaxa de $5 para zonas remotas
Regra E (Prioridade 1): Sobretaxa de 10% de combustível

Pedido: $80, Zona remota, Cliente VIP
Custo base: $20
A: $80 > $75 → Grátis ($0)
B: VIP → 15% de desconto de $0 = $0
C: 10% de desconto de $0 = $0
D: Zona remota +$5 = $5
E: Combustível +10% de $5 = $5.50

Final: $5.50 (não grátis devido às sobretaxas)

**Para evitar isso, use stop_further_rules=Sim**:
```
Regra A (Prioridade 100, stop=Sim): Envio grátis >$75

Mesmo pedido:
A: $80 > $75 → Grátis ($0) → PARAR
Final: $0 (verdadeiramente grátis)
```

---

## Testando Regras de Envio

**Antes de ir ao vivo**:

1. **Crie Carrinhos de Teste**
   - Carrinho A: $25 (abaixo do limite)
   - Carrinho B: $55 (acima do limite)
   - Carrinho C: $200 + Zona remota
   - Carrinho D: Cliente VIP

2. **Teste Cada Regra**
   - Proceda ao checkout
   - Verifique se o custo de envio exibido está correto
   - Verifique a ordem de execução das regras

3. **Teste a Resolução de Prioridade**
   - Múltiplas regras correspondentes
   - Verifique se a prioridade mais alta é executada primeiro
   - Verifique o comportamento de stop_further_rules

4. **Teste Casos de Extremo**
   - Valor do carrinho exatamente no limite
   - Múltiplas condições correspondentes
   - Regras conflitantes

---

## Solução de Problemas

**Problema 1: Regra não aplicando**

**Causas**:
- A regra está inativa
- Uma ou mais condições não foram atendidas
- Uma regra de maior prioridade definiu stop_further_rules=Sim
- Validade temporal fora da data atual

**Solução**: Revise todas as condições, verifique a prioridade, confirme o status ativo.

---

**Problema 2: Valor de desconto inesperado**

**Causas**:
- Múltiplas regras empilhadas
- Percentual aplicado a um custo já descontado
- Prioridade da regra incorreta

**Solução**: Verifique a ordem de prioridade, revise as bandeiras de parada de regras adicionais, trace a execução manualmente.

---

**Problema 3: Envio grátis não funcionando**

**Causas**:
- Uma regra de sobretaxa de menor prioridade adiciona custo após a regra de envio grátis
- O carrinho não atende ao limite mínimo de valor
- Produtos excluídos no carrinho

**Solução**: Use stop_further_rules=Sim na regra de envio grátis, verifique as condições, verifique as exclusões.

---

## Dicas

- **Use alta prioridade para envio grátis** - Prioridade 100 garante que ela seja executada antes de outros ajustes
- **Defina stop_further_rules para regras absolutas** - Envio grátis deve parar o processamento adicional
- **Teste combinações de regras** - Múltiplas regras podem interagir de forma inesperada
- **Use nomes descritivos** - "Desconto de 20% para VIP (Prioridade 75)" é melhor que "Regra 3"
- **Documente lógica complexa** - Adicione notas no campo de descrição
- **Comece com regras simples** - Adicione complexidade gradualmente
- **Monitore o desempenho das regras** - Verifique se as regras estão sendo usadas ou causando confusão
- **Evite regras excessivas** - Muitas regras desaceleram o checkout, use 5-10 no máximo
- **Use zonas para geografia** - Melhor que múltiplas regras similares por país
- **Combine com métodos** - Regras + Métodos funcionam juntos para preços sofisticados
- **Defina janelas de tempo claras** - Sempre inclua datas de término para promoções
- **Teste casos de extremo** - Exatamente $50, exatamente 5 itens, etc.

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.