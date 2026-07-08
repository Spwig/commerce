---
title: Métodos de Envio
---

Métodos de envio são as opções de entrega visíveis ao cliente durante o checkout — cada método calcula os custos de envio usando diferentes estratégias de precificação. O Spwig oferece 7 tipos de métodos, variando de taxas fixas simples até precificação em tempo real calculada por transportadoras complexas. Métodos podem ser restringidos por valor mínimo/máximo do pedido, peso e zonas geográficas. Os clientes selecionam seu método preferido durante o checkout, e o custo calculado é adicionado ao total do pedido.

Use este guia para configurar métodos de envio que correspondam ao seu modelo de negócios, desde o envio com taxa fixa básica até a precificação em camadas baseada em zonas sofisticada.

## Tipos de Métodos de Envio

O Spwig oferece 7 tipos de métodos de envio, cada um com lógica diferente de cálculo de custos:

### Envio com Taxa Fixa

**O que é**: Custo fixo, independentemente do conteúdo do carrinho, destino ou peso.

**Quando usar**:
- Lojas simples com custos de envio previsíveis
- Um único tipo de produto (tamanho/peso semelhante)
- Envio doméstico apenas com taxas padrão de transportadoras
- Promoções de envio gratuito (use com regras de envio)

**Configuração**:
- Defina **Tipo de Método** = Taxa Fixa
- Insira **Custo Fixo** (ex., $9.99)
- Opcional: Defina restrições de valor mínimo/máximo do pedido

**Exemplo**: "Envio Padrão - $9.99" para todos os pedidos domésticos.

---

### Envio Grátis

**O que é**: Opção de envio sem custo (sem cobrança ao cliente).

**Quando usar**:
- Promoções de envio gratuito
- Pedidos de alto valor (combine com valor mínimo do pedido)
- Alternativa para coleta local
- Benefícios de programas de fidelidade

**Configuração**:
- Defina **Tipo de Método** = Envio Grátis
- Opcional: Defina **Valor Mínimo do Pedido** (ex., gratuito acima de $50)
- Funciona bem com regras de envio para envio gratuito condicional

**Exemplo**: "Envio Grátis em Pedidos Acima de $50" com min_order_value = $50.

---

### Envio com Base no Peso

**O que é**: Custo calculado com base em uma tabela de taxas em camadas com base no peso total do carrinho.

**Quando usar**:
- Produtos com pesos variáveis (livros, hardware, produtos de supermercado)
- Modelos de precificação de transportadoras baseados em peso
- Relação previsível de peso para custo

**Configuração**:
1. Defina **Tipo de Método** = Baseado em Peso
2. Crie **Tabela de Taxa de Envio** com basis_type = "weight"
3. Adicione **Camadas de Taxa de Envio** (ex., 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opcional: Restrinja a zonas específicas

**Exemplo**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Como Funciona**: O carrinho calcula o peso total → localiza a camada correspondente → retorna a taxa da camada.

---

### Envio com Base no Preço

**O que é**: Custo calculado com base em uma tabela de taxas em camadas com base no subtotal do carrinho.

**Quando usar**:
- Custo de envio correlacionado ao valor do pedido
- Incentivar valores de carrinho mais altos (taxa por dólar mais baixa em camadas mais altas)
- Alternativa simples ao baseado em peso para itens com preços semelhantes

**Configuração**:
1. Defina **Tipo de Método** = Baseado em Preço
2. Crie **Tabela de Taxa de Envio** com basis_type = "price"
3. Adicione **Camadas de Taxa de Envio** (ex., $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Exemplo**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Grátis
```

**Como Funciona**: O carrinho calcula o subtotal → localiza a camada correspondente → retorna a taxa da camada.

---

### Taxas de Envio em Tempo Real

**O que é**: Taxas em tempo real obtidas de APIs de transportadoras (FedEx, UPS, DHL) no checkout.

**Quando usar**:
- Custos de envio variáveis por destino
- Múltiplas opções de transportadoras para clientes
- Precificação precisa de transportadoras sem tabelas de taxas manuais
- Envio internacional com precificação complexa

**Configuração**:
1. Defina **Tipo de Método** = Tempo Real
2. Crie **Conta do Fornecedor** (Configurações > Envio > Contas de Fornecedor)
3. Insira as credenciais da API da transportadora (número da conta, chave da API, segredo)
4. Vincule a conta do fornecedor ao método de envio
5. Opcional: Adicione uma porcentagem de markup ou markup fixo

**Requisitos**:
- Conta ativa da transportadora (FedEx, UPS, DHL, etc.)
- Credenciais da API da transportadora
- Pacotes de envio definidos (para cálculo de peso dimensional)

**Exemplo**: O método "Envio Ground da FedEx" obtém taxas em tempo real da FedEx com base no peso do carrinho, dimensões e destino no checkout.

**Como Funciona**:
1. O cliente insere o endereço no checkout
2. O sistema chama a API da transportadora com origem, destino, dimensões do pacote e peso
3. A transportadora retorna a cotação de taxa
4. Markup opcional aplicado
5. A taxa é exibida ao cliente

---

### Coleta Local

**O que é**: O cliente retira o pedido em um local físico (sem custo de entrega).

**Quando usar**:
- Lojas de varejo oferecendo coleta
- Opções de coleta em centros de distribuição
- Eventos ou feiras de mercado
- Eliminar custos de envio para clientes locais

**Configuração**:
1. Defina **Tipo de Método** = Coleta Local
2. Crie **Local** (Configurações > Envio > Locais)
   - Defina endereço, horário de funcionamento, capacidade de coleta
3. Vincule local(is) ao método
4. Opcional: Defina o tempo de preparação para coleta (ex., "Pronto em 2 horas")

**Experiência do Cliente**:
- Seleciona "Coleta Local" no checkout
- Escolhe o local de coleta (se houver múltiplos)
- Escolhe data/hora de coleta com base na disponibilidade
- Recebe notificação quando o pedido estiver pronto

**Exemplo**: "Coleta na Loja - Grátis" com 3 locais de varejo, prontos em 24 horas.

---

### Taxas de Envio por Tabela

**O que é**: Preços em camadas flexíveis com base em peso, preço ou quantidade com alvo avançado de zona.

**Quando usar**:
- Precificação complexa (taxas diferentes por zona E peso)
- Precisa de mais controle do que apenas baseado em peso ou preço
- Múltiplos fatores de precificação (ex., peso + destino + quantidade)

**Configuração**:
1. Defina **Tipo de Método** = Taxa por Tabela
2. Crie **Tabela de Taxa de Envio**
3. Defina **basis_type**: peso, preço ou quantidade
4. Adicione **Camadas de Taxa de Envio** com valores mínimos/máximos
5. Opcional: Restrinja camadas a zonas ou países específicos

**Diferença em relação a Baseado em Peso/Preço**: A taxa por tabela suporta restrições geográficas por camada, permitindo taxas diferentes para o mesmo peso/preço em zonas diferentes.

**Exemplo**:
```
Zona A (Doméstica):
  0-5kg: $10
  5-10kg: $15

Zona B (Remota):
  0-5kg: $18
  5-10kg: $25
```

**Como Funciona**: O carrinho calcula o valor da base (peso/preço/quantidade) → localiza a camada correspondente para a zona do cliente → retorna a taxa da camada.

---

## Configuração de Métodos de Envio

Todos os métodos de envio compartilham essas configurações comuns:

### Configurações Básicas

- **Nome**: Identificador interno (não mostrado aos clientes)
- **Nome para Exibição**: Nome visível ao cliente no checkout (ex., "Envio Padrão", "Entrega Express")
- **Descrição**: Texto de ajuda opcional mostrado no checkout (ex., "Entrega em 3-5 dias úteis")
- **Tipo de Método**: Um dos 7 tipos acima
- **Ativo**: Alternar para habilitar/desabilitar o método sem excluí-lo

### Configurações de Custo

- **Custo Fixo**: Apenas para métodos de taxa fixa
- **Tabela de Taxa**: Para métodos baseados em peso, preço, taxa por tabela
- **Conta do Fornecedor**: Para métodos de envio em tempo real
- **Classe de Imposto**: Aplicar imposto ao custo de envio (se aplicável)

### Restrições

**Restrições de Valor do Pedido**:
- **Valor Mínimo do Pedido**: O método só está disponível se o subtotal do carrinho for ≥ valor (ex., envio gratuito acima de $50)
- **Valor Máximo do Pedido**: O método é oculto se o subtotal do carrinho for > valor (ex., taxa fixa apenas para pedidos abaixo de $100)

**Restrições de Peso**:
- **Peso Mínimo**: O método só está disponível se o peso do carrinho for ≥ valor
- **Peso Máximo**: O método é oculto se o peso do carrinho for > valor (comum para opções de envio leves)

**Restrições Geográficas**:
- **Zonas de Envio**: Vincule o método a zonas específicas (domésticas, internacionais, regionais)
- Zonas vazias = disponível para todos os endereços
- Múltiplas zonas = disponível para qualquer zona correspondente

### Configurações Avançadas

- **Prioridade**: Ordem de exibição no checkout (número menor = mais alto na lista)
- **Taxa de Manuseio**: Taxa adicional fixa adicionada ao custo calculado
- **Limite de Envio Grátis**: Defina automaticamente o custo para $0 se o subtotal do carrinho for ≥ limite (alternativa ao min_order_value)

---

## Criando um Método de Envio

**Fluxo de Trabalho Passo a Passo**:

1. **Navegue até Métodos de Envio**
   - Vá para Configurações > Carrinho > Métodos de Envio
   - Clique em "Adicionar Método de Envio"

2. **Escolha o Tipo de Método**
   - Selecione o tipo apropriado com base em sua estratégia de precificação
   - O tipo determina os campos de configuração de custo disponíveis

3. **Configure Informações Básicas**
   - Nome: Referência interna (ex., "domestic_ground")
   - Nome para Exibição: Visível ao cliente (ex., "Envio Padrão")
   - Descrição: Prazo de entrega (ex., "5-7 dias úteis")

4. **Defina o Cálculo de Custo**
   - **Taxa Fixa**: Insira o custo fixo
   - **Peso/Preço/Tabela de Taxa**: Crie uma tabela de taxas (veja abaixo)
   - **Tempo Real**: Vincule a conta do fornecedor
   - **Grátis/Coleta**: Nenhuma configuração de custo necessária

5. **Adicione Restrições (Opcional)**
   - Valor mínimo/máximo do pedido
   - Peso mínimo/máximo
   - Zonas de envio

6. **Defina a Prioridade**
   - Números menores aparecem primeiro no checkout
   - Ordem recomendada: Grátis (1), Coleta Local (2), Padrão (3), Expresso (4)

7. **Ative o Método**
   - Ative o "Ativo" = Sim
   - Salve

---

## Criando Tabelas de Taxas

Para métodos baseados em peso, preço e tabela de taxas:

**Etapa 1: Criar Tabela de Taxas**
- Vá para Configurações > Envio > Tabelas de Taxas
- Clique em "Adicionar Tabela de Taxas"
- Defina **Nome** (ex., "Tiers de Peso Doméstico")
- Defina **Tipo de Base**: peso, preço ou quantidade

**Etapa 2: Adicionar Camadas**
- Clique em "Adicionar Camada"
- Defina **Valor Mínimo** e **Valor Máximo** (intervalo para correspondência)
- Defina **Taxa** (custo para esta camada)
- Opcional: Restrinja a zonas ou países específicos
- Salve a camada

**Etapa 3: Repetir para Todas as Camadas**
- Cubra o intervalo completo (0 ao valor máximo esperado)
- Certifique-se de não haver lacunas (ex., 0-5, 5-10, 10-20, 20+)
- Use `null` para o valor máximo na última camada (ilimitado)

**Etapa 4: Vincular à Tabela de Taxas**
- Edite o método de envio
- Selecione a tabela de taxas do menu suspenso
- Salve

**Exemplo de Tabela Baseada em Peso**:
```
Nome: Tiers de Peso Doméstico
Base: Peso

Camadas:
1. Mín: 0g, Máx: 2000g, Taxa: $8
2. Mín: 2000g, Máx: 5000g, Taxa: $12
3. Mín: 5000g, Máx: 10000g, Taxa: $18
4. Mín: 10000g, Máx: null, Taxa: $25
```

---

## Cenários Comuns de Envio

### Cenário 1: Envio Doméstico Básico

**Objetivo**: Taxa fixa simples de $9.99 para todos os pedidos domésticos.

**Solução**:
- Tipo de Método: Taxa Fixa
- Custo Fixo: $9.99
- Zona de Envio: "Doméstico" (apenas seu país)

---

### Cenário 2: Envio Grátis Acima de $50

**Objetivo**: Incentivar valores de carrinho mais altos com um limite de envio gratuito.

**Opção de Solução A** (Recomendada):
- Tipo de Método: Envio Grátis
- Valor Mínimo do Pedido: $50
- Nome para Exibição: "Envio Grátis (Pedidos $50+)")

**Opção de Solução B** (Usando Regras):
- Tipo de Método: Taxa Fixa
- Custo Fixo: $9.99
- Crie uma Regra de Envio:
  - Condição: Valor do carrinho ≥ $50
  - Ação: Defina o custo para $0

---

### Cenário 3: Envio Baseado em Peso Doméstico + Internacional

**Objetivo**: Taxas diferentes para doméstico vs internacional com base no peso.

**Solução**:
1. Crie 2 zonas: "Doméstico", "Internacional"
2. Crie 2 tabelas de taxas: "Taxas de Peso Doméstico", "Taxas de Peso Internacional"
3. Crie 2 métodos:
   - "Envio Doméstico" → vincula a zona doméstica + tabela de taxas doméstica
   - "Envio Internacional" → vincula a zona internacional + tabela de taxas internacional

---

### Cenário 4: Múltiplas Opções de Transportadora

**Objetivo**: Permitir que os clientes escolham entre FedEx Ground, FedEx Express, UPS Ground.

**Solução**:
1. Crie Conta do Fornecedor para API do FedEx
2. Crie Conta do Fornecedor para API da UPS
3. Crie 3 métodos em tempo real:
   - "FedEx Ground" → provedor FedEx, código de serviço = "FEDEX_GROUND"
   - "FedEx Express" → provedor FedEx, código de serviço = "FEDEX_EXPRESS"
   - "UPS Ground" → provedor UPS, código de serviço = "UPS_GROUND"
4. Todos os 3 métodos consultam APIs de transportadora no checkout e exibem taxas em tempo real

---

### Cenário 5: Coleta Local + Entrega

**Objetivo**: Loja de varejo oferece opções de coleta e entrega.

**Solução**:
1. Crie Local: "Loja Principal" com endereço, horários, tempo de preparação
2. Crie 2 métodos:
   - "Coleta Local" → tipo de coleta local, vincula ao local da loja principal
   - "Entrega Padrão" → taxa fixa $9.99
3. Os clientes veem ambas as opções no checkout

---

## Testando Métodos de Envio

Antes de ir ao ar, teste todos os métodos:

1. **Crie um Carrinho de Teste**
   - Adicione produtos com diferentes pesos/preços
   - Proceda ao checkout

2. **Teste Cada Método**
   - Insira endereços em diferentes zonas
   - Verifique se os métodos corretos aparecem
   - Confira se os custos calculados correspondem às expectativas

3. **Teste Restrições**
   - Adicione itens até atingir o valor mínimo do pedido → verifique se o envio gratuito aparece
   - Adicione itens pesados → verifique se as camadas baseadas em peso funcionam
   - Teste restrições de zona → verifique se os métodos são ocultos para zonas excluídas

4. **Teste Métodos em Tempo Real** (se aplicável)
   - Use credenciais de teste da transportadora
   - Verifique se as taxas são retornadas com sucesso
   - Confira a precisão das taxas contra o site da transportadora

---

## Solução de Problemas

**Problema 1: Método não aparece no checkout**

**Causas**:
- O método está inativo
- O carrinho não atende aos valores mínimos/máximos do pedido
- O carrinho não atende aos valores mínimos/máximos de peso
- O endereço do cliente não corresponde a nenhuma zona vinculada
- Nenhuma camada da tabela de taxas cobre o peso/preço do carrinho

**Solução**: Verifique as restrições, verifique o status ativo, certifique-se de que as zonas/camadas cubram o cenário do cliente.

---

**Problema 2: Taxas em tempo real falhando**

**Causas**:
- Credenciais da API inválidas
- Conta do fornecedor inativa
- Nenhum pacote de envio definido (a transportadora precisa de dimensões)
- Endereço de origem não definido
- API da transportadora fora do ar

**Solução**: Teste a conexão do fornecedor, verifique as credenciais, certifique-se de que os pacotes estão configurados, verifique o endereço de origem nas configurações.

---

**Problema 3: Custo calculado incorreto**

**Causas**:
- Camadas da tabela de taxas têm lacunas ou sobreposições
- Valores mínimos/máximos da camada em unidades incorretas (gramas vs kg)
- Taxa de manuseio adicionada inesperadamente
- Regra de envio modificando o custo

**Solução**: Revise as camadas da tabela de taxas, verifique as unidades, verifique a prioridade das regras de envio.

---

## Dicas

- **Comece simples** - Use taxa fixa para o primeiro método, adicione complexidade conforme necessário
- **Teste amplamente** - Verifique se todos os métodos funcionam no ambiente de staging antes de habilitar no produção
- **Use nomes descritivos** - "Envio Padrão (5-7 dias)" é melhor que "Método 1"
- **Defina prazos de entrega realistas** - Subestime, entregue mais para satisfação do cliente
- **Ofereça coleta, se possível** - Reduz custos de envio, melhora a conveniência do cliente
- **Monitore a confiabilidade da API da transportadora** - Tenha uma taxa fixa como fallback se as taxas em tempo real falharem
- **Use zonas para envio internacional** - Taxas diferentes por região evitam perdas em destinos caros
- **Combine com regras de envio** - Regras adicionam lógica condicional (promoções de envio gratuito, sobretaxas para áreas remotas)
- **Mantenha os métodos limitados** - 2-4 opções no checkout evitam paralisia de decisão
- **Atualize tabelas de taxas sazonalmente** - Taxas de transportadoras mudam, revise anualmente
- **Use a prioridade com sabedoria** - Coloque opções gratuitas/baratas primeiro, opções caras por último

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.