---
title: Configuração de Impostos
---

As taxas de imposto definem os impostos sobre vendas, IVA e outros impostos sobre consumo aplicados no checkout com base na localização do cliente e no tipo de produto - configure taxas a nível de país/estado/cidade com isenções de categorias de produtos opcionais. O Spwig suporta imposto composto (imposto sobre imposto), seleção de taxas com base em prioridade e grupos de impostos pré-definidos para a rápida configuração de sistemas fiscais regionais (IVA da UE, Imposto sobre Vendas dos EUA). As taxas podem isentar tipos específicos de produtos (alimentos, livros, bens digitais) ou categorias para conformidade com as leis fiscais locais.

Use a configuração de impostos para garantir a conformidade legal com os requisitos de coleta de impostos nas jurisdições onde vende.

## Configuração da Taxa de Imposto

Cada taxa de imposto define:

**Escopo Geográfico**:
- País (obrigatório)
- Estado/Província (opcional)
- Cidade (opcional)
- Padrão de Código Postal (opcional, regex)

**Detalhes da Taxa**:
- **Taxa de Imposto**: Percentagem (ex., 8,5%)
- **Nome**: Nome de exibição (ex., "Imposto sobre Vendas da Califórnia")
- **Prioridade**: Prioridade mais alta vence quando várias taxas coincidem
- **Ativo**: Alternar sem exclusão

**Isenções**:
- **Tipos de Produtos Isentos**: Bens digitais, bens físicos, serviços
- **Categorias Isentas**: Categorias específicas de produtos (Alimentos, Livros, Médicos)

**Imposto Composto**:
- **É Composto**: Aplicar esta taxa sobre impostos anteriores (imposto sobre imposto)
- Exemplo: O PST do Quebec compõe-se sobre o IVA

---

## Cenários Comuns de Imposto

### Imposto sobre Vendas dos EUA (Nível de Estado)

```
Nome: Imposto sobre Vendas da Califórnia
País: EUA
Estado: CA
Taxa: 7,25%
Prioridade: 50
```

### IVA da UE (Nível de País)

```
Nome: IVA do Reino Unido
País: GB
Taxa: 20%
Prioridade: 50

Nome: IVA da Alemanha
País: DE
Taxa: 19%
Prioridade: 50
```

### IVA/GST do Canadá (Composto)

```
Taxa 1: IVA Federal
País: CA
Taxa: 5%
Prioridade: 100
É Composto: Não

Taxa 2: PST do Quebec
País: CA
Estado: QC
Taxa: 9,975%
Prioridade: 50
É Composto: Sim  (aplica-se ao subtotal + IVA)
```

### Imposto a Nível de Cidade

```
Nome: Imposto sobre Vendas de Seattle
País: EUA
Estado: WA
Cidade: Seattle
Taxa: 10,1%
Prioridade: 100
```

---

## Isenções de Imposto

### Isenções por Tipo de Produto

Iseste tipos inteiros de produtos:

- **Bens Digitais**: Software, e-books, música
- **Bens Físicos**: Produtos tangíveis
- **Serviços**: Consultoria, instalação

Exemplo: O IVA da UE não se aplica a bens digitais para consumidores (em alguns casos)

### Isenções por Categoria

Iseste categorias específicas de produtos:

- Alimentos e Produtos Alimentares (muitas vezes isentos ou com taxa reduzida)
- Livros e Materiais Educativos
- Materiais Médicos e Farmacêuticos
- Roupas (algumas jurisdições)

Configuração:
```
Nome: Imposto sobre Vendas da Califórnia
Taxa: 7,25%
Categorias Isentas: ["Alimentos e Bebidas", "Medicamentos de Prescrição"]
```

---

## Grupos de Impostos Pré-definidos

Carregue rapidamente configurações comuns de impostos:

**Predefinição de Imposto sobre Vendas dos EUA**:
- Todos os 50 estados + DC
- Taxas a nível de estado
- Atualizações automáticas quando as taxas mudam

**Predefinição de IVA da UE**:
- Todos os 27 estados-membros da UE
- Taxas padrão de IVA
- Lógica de cobrança reversa para B2B

**Para Usar Predefinições**:
1. Configurações > Carrinho > Predefinições de Imposto
2. Selecione o grupo de predefinição (ex., "Imposto sobre Vendas dos EUA 2026")
3. Clique em "Carregar Predefinição"
4. Taxas importadas automaticamente
5. Personalize conforme necessário

---

## Resolução de Prioridade

Quando várias taxas coincidem, a prioridade mais alta vence:

Exemplo:
```
Cliente em Seattle, WA:

Taxa A: Federal dos EUA (Prioridade 1) - 0%
Taxa B: Estado de Washington (Prioridade 50) - 6,5%
Taxa C: Cidade de Seattle (Prioridade 100) - 3,6%

Resultado: Aplica-se a taxa de Seattle (10,1% no total)
```

---

## Opções de Exibição de Imposto

Configure em Configurações > Carrinho > Configurações de Imposto:

- **Preços Incluem Imposto**: Exiba preços com imposto incluído (estilo da UE)
- **Exiba Imposto Separadamente**: Mostre o imposto como item de linha (estilo dos EUA)
- **Arredondar Imposto**: Por item ou por pedido
- **Rótulo de Imposto**: Personalize o rótulo ("IVA", "Imposto sobre Vendas", "IVA")

---

## Teste a Configuração de Imposto

Antes de ir ao ar:

1. Crie pedidos de teste de diferentes jurisdições
2. Verifique se a taxa de imposto correta foi aplicada
3. Verifique se as isenções funcionam para categorias excluídas
4. Teste o cálculo de imposto composto
5. Revise os itens de imposto nas faturas

---

## Notas de Conformidade

- **EUA**: As regras de nexus exigem a coleta de impostos em estados onde você tem presença física ou nexus econômico
- **UE**: Empresas registradas no IVA devem coletar IVA de clientes da UE
- **Canadá**: O IVA/HST/PST varia por província
- **Consulte um profissional fiscal**: As leis fiscais mudam frequentemente, verifique os requisitos atuais

---

## Dicas

- **Use predefinições de imposto** - Mais rápido do que a entrada manual, atualizações automáticas
- **Monitore os limites de nexus** - Rastreie vendas por estado para nexus econômico dos EUA
- **Defina a prioridade corretamente** - Cidade > Estado > País
- **Teste o imposto composto** - Verifique se os cálculos correspondem aos valores esperados
- **Atualize anualmente** - As taxas de imposto mudam, revise a cada janeiro
- **Documente as isenções** - Mantenha registros do motivo pelo qual as categorias estão isentas
- **Use nomes descritivos** - "Imposto sobre Vendas da Califórnia 2026" é melhor do que "Imposto 1"
- **Ative o imposto por padrão** - Mais seguro do que esquecer de aplicar o imposto

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.