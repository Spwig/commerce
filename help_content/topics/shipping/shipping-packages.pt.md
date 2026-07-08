---
title: Pacotes de Envio
---

# Pacotes de Envio

Pacotes de envio definem tamanhos pré-definidos de caixas e envelopes para cálculo de taxas e empacotamento automático – especifique dimensões internas (espaço útil), espessura das paredes (dimensões externas para APIs de transportadoras), limites de peso e custo de embalagem. As transportadoras usam dimensões externas para calcular o peso dimensional para cotações de taxas precisas. Os pacotes têm prioridade de ordenação para algoritmos de empacotamento automático que selecionam automaticamente combinações ótimas de pacotes para acomodar itens do carrinho.

Configure pacotes ao usar APIs de transportadoras para taxas em tempo real ou quando você precisar de cálculos precisos de peso dimensional.

## Configuração de Pacotes

Cada pacote define:

**Dimensões**:
- **Comprimento Interno**: Espaço útil dentro (cm)
- **Largura Interna**: Espaço útil dentro (cm)
- **Altura Interna**: Espaço útil dentro (cm)
- **Espessura da Parede**: Espessura do material de embalagem (cm)

**Dimensões Externas** (calculadas automaticamente):
```
Comprimento Externo = Comprimento Interno + (2 × Espessura da Parede)
Largura Externa = Largura Interna + (2 × Espessura da Parede)
Altura Externa = Altura Interna + (2 × Espessura da Parede)
```

**Peso e Custo**:
- **Peso Bruto**: Peso da embalagem vazia (gramas)
- **Peso Máximo**: Capacidade de carga máxima (gramas)
- **Custo**: Custo do material de embalagem (para otimização de custos)

**Propriedades**:
- **Nome**: Identificador do pacote (ex.: "Caixa Pequena", "Envelope Grande")
- **Tipo**: Caixa ou Envelope
- **Prioridade**: Ordem de seleção automática (menor = maior prioridade)
- **Ativo**: Alternar disponibilidade

---

## Por Que as Dimensões Externas Importam

As transportadoras calculam **peso dimensional** a partir das dimensões externas:

**Fórmula de Peso Dimensional**:
```
Peso Dimensional = (Comprimento × Largura × Altura) / Divisor

Divisores Comuns:
- DHL: 5000
- FedEx/UPS: 5000 (nacional), 6000 (internacional)
```

**Exemplo**:
```
Caixa Pequena:
Interno: 20cm × 15cm × 10cm
Espessura da Parede: 0,5cm
Externo: 21cm × 16cm × 11cm

Peso Dimensional = (21 × 16 × 11) / 5000 = 0,74kg

Se o peso real = 0,5kg → A transportadora fatura com 0,74kg (peso dimensional maior)
```

**Por Que a Precisão Importa**: Dimensões imprecisas → cotações de taxas incorretas → cliente cobrado em excesso ou em falta.

---

## Tamanhos de Pacotes Comuns

### Envelope Pequeno com Enchimento

```
Interno: 25cm × 18cm × 2cm
Espessura da Parede: 0,3cm
Peso Máximo: 500g
Tipo: Envelope
Uso: Documentos, livros, joias
```

### Caixa Pequena

```
Interno: 20cm × 15cm × 10cm
Espessura da Parede: 0,5cm
Peso Máximo: 5kg
Tipo: Caixa
Uso: Pequenos eletrodomésticos, cosméticos, acessórios
```

### Caixa Média

```
Interno: 30cm × 25cm × 20cm
Espessura da Parede: 0,5cm
Peso Máximo: 15kg
Tipo: Caixa
Uso: Roupas, sapatos, itens de cozinha
```

### Caixa Grande

```
Interno: 45cm × 35cm × 30cm
Espessura da Parede: 0,6cm
Peso Máximo: 30kg
Tipo: Caixa
Uso: Itens em grande quantidade, múltiplos produtos, eletrodomésticos grandes
```

---

## Algoritmo de Empacotamento Automático

O sistema seleciona automaticamente pacotes para itens do carrinho:

**Como Funciona**:
1. Calcule o volume total dos itens do carrinho
2. Ordene os pacotes por prioridade (números mais baixos primeiro)
3. Tente acomodar os itens em um único pacote
4. Se não couber, tente o próximo tamanho de pacote
5. Se nenhum pacote único couber, combine múltiplos pacotes
6. Otimize com base na configuração `optimize_for`

**Modos de Otimização**:
- **Custo**: Minimize o custo de embalagem
- **Volume**: Minimize o espaço desperdiçado
- **Contagem**: Minimize o número de pacotes

**Exemplo**:
```
Itens do Carrinho:
- Item A: 10cm × 8cm × 5cm, 200g
- Item B: 15cm × 12cm × 8cm, 400g

Pacotes (por prioridade):
1. Caixa Pequena (20×15×10, prioridade=1)
2. Caixa Média (30×25×20, prioridade=2)

Algoritmo:
Tente Caixa Pequena: Ambos os itens cabem
Resultado: 1× Caixa Pequena (otimizado para contagem)
```

---

## Prioridade de Pacotes

**A prioridade determina a ordem de empacotamento**:

Prioridade 1 (mais alta): Pacotes pequenos são tentados primeiro
Prioridade 10: Pacotes grandes são último recurso

**Estratégia**:
- Pacotes pequenos = números de prioridade baixos (1-3)
- Pacotes médios = prioridade média (4-6)
- Pacotes grandes = números de prioridade altos (7-10)

**Por Que**: Comece com o pacote mais pequeno, aumente se necessário → minimiza o custo de envio.

---

## Precisão da Espessura da Parede

Meça a embalagem real:

**Como Medir**:
1. Pegue uma caixa vazia
2. Meça as dimensões internas (internas)
3. Meça as dimensões externas (externas)
4. Calcule: `(Externo - Interno) / 2 = Espessura da Parede`

**Exemplo**:
```
Largura Interna: 20cm
Largura Externa: 21cm
Espessura da Parede: (21 - 20) / 2 = 0,5cm
```

**Espessuras Comuns**:
- Envelope com enchimento: 0,2-0,4cm
- Cartão de uma parede: 0,4-0,6cm
- Cartão de duas paredes: 0,8-1,0cm

---

## Criando Preset de Pacote

**Passo a Passo**:

1. Configurações > Envio > Pacotes de Envio
2. Clique em "Adicionar Pacote de Envio"
3. Insira o nome (ex.: "Caixa Média")
4. Selecione o tipo (Caixa ou Envelope)
5. Insira as dimensões internas (L × W × H em cm)
6. Insira a espessura da parede (cm)
7. O sistema calcula automaticamente as dimensões externas
8. Insira o peso bruto (peso da embalagem vazia em gramas)
9. Insira o peso máximo (capacidade de carga em gramas)
10. Opcional: Insira o custo (para otimização de custos)
11. Defina a prioridade (1-10)
12. Ative = Sim
13. Salvar

---

## Testando a Seleção de Pacotes

**Teste Manual**:
1. Adicione produtos ao carrinho de teste
2. Proceda para o checkout
3. Selecione o método de envio em tempo real (usa pacotes)
4. Verifique se a taxa retornada é razoável
5. Verifique a resposta da transportadora (logs da API mostram os pacotes selecionados)

**Visualização de Empacotamento Automático**:
- Alguns contas de provedores de envio mostram a quebra de pacotes
- Veja quais pacotes foram selecionados para o carrinho
- Verifique o empacotamento otimizado

---

## Dicas

- **Meça com precisão** - Dimensões imprecisas → taxas incorretas da transportadora
- **Inclua a espessura da parede** - Crítica para o peso dimensional
- **Comece com 3-4 tamanhos** - Pequeno, médio, grande cobre a maioria dos cenários
- **Defina pesos máximos realistas** - Capacidade da caixa, não limite teórico
- **Use a prioridade com sabedoria** - Caixas pequenas prioridade 1, caixas grandes prioridade 10
- **Teste com produtos reais** - Verifique se o empacotamento automático seleciona os tamanhos corretos
- **Atualize quando houver mudanças na embalagem** - Novo fornecedor = re-meça as dimensões
- **Considere itens especiais** - Itens frágeis podem precisar de tamanhos de caixa específicos
- **Mantenha pacotes ativos mínimos** - Muitas opções desaceleram o algoritmo de empacotamento automático
- **Documente a embalagem** - Anote quais produtos cabem em quais pacotes
