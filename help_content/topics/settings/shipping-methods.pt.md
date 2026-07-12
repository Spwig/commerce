---
title: Métodos de Envio
---

Métodos de envio são as opções de entrega visíveis ao cliente durante o checkout — cada método calcula os custos de envio usando estratégias de precificação diferentes. O Spwig oferece 7 tipos de métodos, variando de taxas fixas simples até precificação em tempo real calculada por transportadoras complexas. Métodos podem ser restringidos por valor mínimo/máximo do pedido, peso e zonas geográficas. Os clientes selecionam seu método preferido durante o checkout, e o custo calculado é adicionado ao total do pedido.

Use este guia para configurar métodos de envio que correspondam ao seu modelo de negócios, desde o envio com taxa fixa básica até a precificação em camadas baseada em zonas sofisticada.

## Tipos de Métodos de Envio

O Spwig oferece 7 tipos de métodos de envio, cada um com lógica diferente de cálculo de custo:

### Envio com Taxa Fixa

**O que é**: Custo fixo, independentemente do conteúdo do carrinho, destino ou peso.

**Quando usar**:
- Lojas simples com custos de envio previsíveis
- Um único tipo de produto (tamanho/peso semelhante)
- Envio nacional apenas com taxas de transportadora padrão
- Promoções de envio gratuito (use com promoções de envio)

**Configuração**:
- Defina **Tipo de Método** = Taxa Fixa
- Insira **Custo Fixo** (ex., $9.99)
- Opcional: Defina restrições de valor mínimo/máximo do pedido

**Exemplo**: "Envio Padrão - $9.99" para todos os pedidos nacionais.

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
- Funciona bem com promoções de envio para envio gratuito condicional

**Exemplo**: "Envio Grátis em Pedidos Acima de $50" com min_order_value = $50.

---

### Envio com Base no Peso

**O que é**: Custo calculado com base em uma tabela de taxas em camadas com base no peso total do carrinho.

**Quando usar**:
- Produtos com pesos variáveis (livros, hardware, mercadorias)
- Modelos de precificação de transportadora com base no peso
- Relação previsível de peso para custo

**Configuração**:
1. Defina **Tipo de Método** = com Base no Peso
2. Crie **Tabela de Taxas de Envio** com basis_type = "weight"
3. Adicione **Camadas de Taxas de Envio** (ex., 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
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
- Incentive valores maiores no carrinho (taxa mais baixa por dólar em camadas superiores)
- Alternativa simples ao envio com base no peso para itens com preços semelhantes

**Configuração**:
1. Defina **Tipo de Método** = com Base no Preço
2. Crie **Tabela de Taxas de Envio** com basis_type = "price"
3. Adicione **Camadas de Taxas de Envio** (ex., $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Exemplo**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Grátis
```

**Como Funciona**: O carrinho calcula o subtotal → localiza a camada correspondente → retorna a taxa da camada.

---

### Taxas de Transportadora em Tempo Real

**O que é**: Taxas em tempo real obtidas de APIs de transportadora (FedEx, UPS, DHL) no checkout.

**Quando usar**:
- Custos de envio variáveis por destino
- Múltiplas opções de transportadora para clientes
- Precificação precisa de transportadora sem tabelas de taxas manuais
- Envio internacional com precificação complexa

**Configuração**:
1. Defina **Tipo de Método** = em Tempo Real
2. Crie **Conta do Fornecedor** (Configurações > Envio > Contas de Fornecedor)
3. Insira as credenciais da API da transportadora (número da conta, chave da API, segredo)
4. Vincule a conta do fornecedor ao método de envio
5. Opcional: Adicione uma porcentagem de markup ou markup fixo

**Requisitos**:
- Conta ativa da transportadora (FedEx, UPS, DHL, etc.)
- Credenciais da API da transportadora
- Pacotes de envio definidos (para cálculo de peso dimensional)

**Exemplo**: O método "FedEx Ground" obtém taxas vitais do FedEx com base no peso do carrinho, dimensões e destino no momento do checkout.

**Como Funciona**:
1. O cliente insere o endereço no checkout
2. O sistema chama a API do transportador com origem, destino, dimensões do pacote e peso
3. O transportador retorna a cotação de taxa
4. Markup opcional aplicado
5. A taxa é exibida ao cliente

---

### Retirada Local

**O Que É**: O cliente retira o pedido em uma localização física (sem custo de entrega).

**Quando Usar**:
- Lojas retails oferecendo retirada
- Opções de retirada em armazéns
- Eventos ou feiras
- Eliminar custos de envio para clientes locais

**Configuração**:
1. Defina **Tipo de Método** = Retirada Local
2. Crie **Localização** (Configurações > Envio > Localizações)
   - Defina endereço, horário de funcionamento, capacidade de retirada
3. Vincule localização(s) ao método
4. Opcional: Defina o tempo de preparação de retirada (ex.: "Pronto em 2 horas")

**Experiência do Cliente**:
- Seleciona "Retirada Local" no checkout
- Escolhe a localização de retirada (se houver múltiplas)
- Escolhe data/hora de retirada com base na disponibilidade
- Recebe notificação quando o pedido estiver pronto

**Exemplo**: "Retirada na Loja - Grátis" com 3 lojas de varejo, pronta em 24 horas.

---

### Envio por Tabela

**O Que É**: Preços flexíveis com base em peso, preço ou quantidade com alvo de zona avançado.

**Quando Usar**:
- Preços complexos (taxas diferentes por zona E peso)
- Necessita de mais controle do que apenas baseado em peso ou preço
- Múltiplos fatores de preço (ex.: peso + destino + quantidade)

**Configuração**:
1. Defina **Tipo de Método** = Tabela de Envio
2. Crie **Tabela de Taxa de Envio**
3. Defina **basis_type**: peso, preço ou quantidade
4. Adicione **Níveis de Taxa de Envio** com valores mínimos/máximos
5. Opcional: Restrinja níveis a zonas específicas ou países

**Diferença da Baseada em Peso/Preço**: A tabela de envio suporta restrições geográficas por nível, permitindo taxas diferentes para o mesmo peso/preço em zonas diferentes.

**Exemplo**:
```
Zona A (Doméstica):
  0-5kg: $10
  5-10kg: $15

Zona B (Remota):
  0-5kg: $18
  5-10kg: $25
```

**Como Funciona**: O carrinho calcula o valor da base (peso/preço/quantidade) → encontra o nível correspondente para a zona do cliente → retorna a taxa do nível.

---

## Configuração do Método de Envio

Todos os métodos de envio compartilham essas configurações comuns:

### Configurações Básicas

- **Nome**: Identificador interno (não mostrado aos clientes)
- **Nome para Exibição**: Nome voltado ao cliente no checkout (ex.: "Envio Padrão", "Entrega Express")
- **Descrição**: Texto de ajuda opcional mostrado no checkout (ex.: "Entrega em 3-5 dias úteis")
- **Tipo de Método**: Um dos 7 tipos acima
- **Ativo**: Alternar para habilitar/desabilitar o método sem exclusão

### Configurações de Custo

- **Custo Fixo**: Apenas para métodos de taxa fixa
- **Tabela de Taxa**: Para métodos baseados em peso, preço, tabela de taxa
- **Conta do Fornecedor**: Para métodos de envio em tempo real com transportadores
- **Classe de Imposto**: Aplicar imposto ao custo de envio (se aplicável)

### Restrições

**Restrições de Valor do Pedido**:
- **Valor Mínimo do Pedido**: O método só está disponível se o subtotal do carrinho for ≥ valor (ex.: envio gratuito acima de $50)
- **Valor Máximo do Pedido**: O método é oculto se o subtotal do carrinho > valor (ex.: taxa fixa apenas para pedidos abaixo de $100)

**Restrições de Peso**:
- **Peso Mínimo**: O método só está disponível se o peso do carrinho for ≥ valor
- **Peso Máximo**: O método é oculto se o peso do carrinho > valor (comum para opções de envio leves)

**Restrições Geográficas**:
- **Zonas de Envio**: Vincule o método a zonas específicas (domésticas, internacionais, regionais)
- Zonas vazias = disponível para todos os endereços
- Múltiplas zonas = disponível para qualquer zona correspondente

### Configurações Avançadas

- **Prioridade**: Ordem de exibição no checkout (número menor = mais alto na lista)
- **Taxa de Manuseio**: Taxa adicional fixa adicionada ao custo calculado
- **Limite de Envio Grátis**: Defina automaticamente o custo para $0 se o subtotal do carrinho ≥ limite (alternativa ao min_order_value)

---

## Criando um Método de Envio

**Fluxo de Trabalho Passo a Passo**:

1. **Navegue até Métodos de Envio**
   - Vá para Configurações > Carrinho > Métodos de Envio
   - Clique em "Adicionar Método de Envio"


2. **Escolher Tipo de Método**
   - Selecione o tipo apropriado com base em sua estratégia de preços
   - O tipo determina os campos de configuração de custo disponíveis

3. **Configurar Informações Básicas**
   - Nome: Referência interna (ex.: "domestic_ground")
   - Nome para Exibição: Para o cliente (ex.: "Ground Shipping")
   - Descrição: Prazo de entrega (ex.: "5-7 dias úteis")

4. **Definir Cálculo de Custo**
   - **Taxa Fixa**: Insira um custo fixo
   - **Peso/Preço/Tabela de Taxas**: Crie uma tabela de taxas (veja abaixo)
   - **Em Tempo Real**: Vincule a conta do provedor
   - **Grátis/Retirada Local**: Nenhuma configuração de custo necessária

5. **Adicionar Restrições (Opcional)**
   - Valor mínimo/máximo do pedido
   - Peso mínimo/máximo
   - Zonas de envio

6. **Definir Prioridade**
   - Números mais baixos aparecem primeiro no checkout
   - Ordem recomendada: Grátis (1), Retirada Local (2), Padrão (3), Expresso (4)

7. **Ativar o Método**
   - Ative o botão "Ativo" = Sim
   - Salvar

---

## Criando Tabelas de Taxas

Para métodos baseados em peso, preço e tabela de taxas:

**Etapa 1: Criar Tabela de Taxas**
- Vá para Configurações > Envio > Tabelas de Taxas
- Clique em "Adicionar Tabela de Taxas"
- Defina **Nome** (ex.: "Domestic Weight Tiers")
- Defina **Tipo de Base**: peso, preço ou quantidade

**Etapa 2: Adicionar Níveis**
- Clique em "Adicionar Nível"
- Defina **Valor Mínimo** e **Valor Máximo** (intervalo para correspondência)
- Defina **Taxa** (custo para este nível)
- Opcional: Restrinja a zonas ou países específicos
- Salve o nível

**Etapa 3: Repetir para Todos os Níveis**
- Cubra o intervalo completo (0 ao valor máximo esperado)
- Certifique-se de não haver lacunas (ex.: 0-5, 5-10, 10-20, 20+)
- Use `null` para o valor máximo no último nível (ilimitado)

**Etapa 4: Vincular ao Método de Envio**
- Edite o método de envio
- Selecione a tabela de taxas do menu suspenso
- Salve

**Exemplo de Tabela Baseada em Peso**:
```
Nome: Domestic Weight Tiers
Base: Peso

Níveis:
1. Mín.: 0g, Máx.: 2000g, Taxa: $8
2. Mín.: 2000g, Máx.: 5000g, Taxa: $12
3. Mín.: 5000g, Máx.: 10000g, Taxa: $18
4. Mín.: 10000g, Máx.: null, Taxa: $25
```

---

## Cenários Comuns de Envio

### Cenário 1: Envio Doméstico Básico

**Objetivo**: Taxa fixa de $9,99 para todos os pedidos domésticos.

**Solução**:
- Tipo de Método: Taxa Fixa
- Custo Fixo: $9,99
- Zona de Envio: "Doméstico" (apenas seu país)

---

### Cenário 2: Envio Grátis acima de $50

**Objetivo**: Incentivar valores maiores no carrinho com um limite de envio grátis.

**Opção de Solução A** (Recomendada):
- Tipo de Método: Envio Grátis
- Valor Mínimo do Pedido: $50
- Nome para Exibição: "Envio Grátis (Pedidos $50+)")

**Opção de Solução B** (Usando Regras):
- Tipo de Método: Taxa Fixa
- Custo Fixo: $9,99
- Crie uma Promoção de Envio:
  - Condição: Valor do carrinho ≥ $50
  - Ação: Defina o custo para $0

---

### Cenário 3: Envio Baseado em Peso Doméstico + Internacional

**Objetivo**: Taxas diferentes para doméstico versus internacional com base no peso.

**Solução**:
1. Crie 2 zonas: "Doméstico", "Internacional"
2. Crie 2 tabelas de taxas: "Domestic Weight", "International Weight"
3. Crie 2 métodos:
   - "Envio Doméstico" → vincula à zona Doméstico + tabela de peso doméstico
   - "Envio Internacional" → vincula à zona Internacional + tabela de peso internacional

---

### Cenário 4: Múltiplas Opções de Transportadora

**Objetivo**: Permitir que os clientes escolham entre FedEx Ground, FedEx Express, UPS Ground.

**Solução**:
1. Crie uma Conta de Provedor para a API do FedEx
2. Crie uma Conta de Provedor para a API da UPS
3. Crie 3 métodos em tempo real:
   - "FedEx Ground" → provedor FedEx, código de serviço = "FEDEX_GROUND"
   - "FedEx Express" → provedor FedEx, código de serviço = "FEDEX_EXPRESS"
   - "UPS Ground" → provedor UPS, código de serviço = "UPS_GROUND"
4. Todos os 3 métodos consultam as APIs dos transportadores no checkout e exibem taxas em tempo real

---

### Cenário 5: Retirada Local + Envio

**Objetivo**: Loja retails oferece opções de retirada local e envio.

**Solução**:
1. Crie Localização: "Loja Principal" com endereço, horários e tempo de preparo
2. Crie 2 métodos:
   - "Retirada Local" → tipo Retirada Local, vincula à localização Loja Principal
   - "Envio Padrão" → Taxa Fixa $9,99
3. Os clientes veem ambas as opções no checkout

---

## Testando Métodos de Envio

Antes de ir ao ar, teste todos os métodos:

1. **Criar Carrinho de Teste**
   - Adicionar produtos com diversos pesos/preços
   - Prosseguir para o checkout

2. **Testar Cada Método**
   - Inserir endereços em diferentes zonas
   - Verificar se os métodos corretos aparecem
   - Verificar se os custos calculados correspondem às expectativas

3. **Testar Restrições**
   - Adicionar itens até atingir o valor mínimo de pedido → verificar se o frete grátis aparece
   - Adicionar itens pesados → verificar se as camadas baseadas em peso funcionam
   - Testar restrições de zona → verificar se os métodos são ocultos para zonas excluídas

4. **Testar Métodos em Tempo Real** (se aplicável)
   - Usar credenciais de teste do transportador
   - Verificar se as taxas são retornadas com sucesso
   - Verificar a precisão das taxas contra o site do transportador

---

## Solução de Problemas

**Problema 1: Método não aparece no checkout**

**Causas**:
- Método inativo
- Carrinho não atende ao valor mínimo/máximo de pedido
- Carrinho não atende ao peso mínimo/máximo
- Endereço do cliente não corresponde a nenhuma zona vinculada
- Nenhuma camada da tabela de taxas cobre o peso/preço do carrinho

**Solução**: Verificar restrições, verificar o status ativo, garantir que zonas/camadas cubram a situação do cliente.

---

**Problema 2: Taxas em tempo real falhando**

**Causas**:
- Credenciais de API inválidas
- Conta do provedor inativa
- Nenhuma embalagem de envio definida (o provedor precisa de dimensões)
- Endereço de origem não definido
- API do transportador fora do ar

**Solução**: Testar a conexão com o provedor, verificar as credenciais, garantir que as embalagens estejam configuradas, verificar o endereço de origem nas configurações.

---

**Problema 3: Custo calculado incorreto**

**Causas**:
- Camadas da tabela de taxas têm lacunas ou sobreposições
- Valores mínimos/máximos das camadas estão em unidades incorretas (gramas vs kg)
- Taxa de manuseio adicionada inesperadamente
- Regra de envio modificando o custo

**Solução**: Revisar as camadas da tabela de taxas, verificar as unidades, verificar a prioridade das promoções de envio.

---

## Dicas

- **Comece simples** - Use taxa fixa para o primeiro método, adicione complexidade conforme necessário
- **Teste de forma abrangente** - Verifique que todos os métodos funcionam no ambiente de staging antes de habilitá-los em produção
- **Use nomes descritivos** - "Entrega Padrão (5-7 dias)" é melhor que "Método 1"
- **Defina tempos de entrega realistas** - Subestime, entregue mais rápido para a satisfação do cliente
- **Ofereça coleta, se possível** - Reduz custos de envio, melhora a conveniência do cliente
- **Monitore a confiabilidade da API do transportador** - Tenha uma taxa fixa como alternativa se as taxas em tempo real falharem
- **Use zonas para internacional** - Taxas diferentes por região evitam perdas em destinos caros
- **Combine com promoções de envio** - Regras adicionam lógica condicional (promoções de frete grátis, sobretaxas para áreas remotas)
- **Mantenha os métodos limitados** - 2-4 opções no checkout evitam a paralisia de decisão
- **Atualize as tabelas de taxas sazonalmente** - As taxas dos transportadores mudam, revise anualmente
- **Use a prioridade com sabedoria** - Coloque opções gratuitas/baratas primeiro, opções caras por último