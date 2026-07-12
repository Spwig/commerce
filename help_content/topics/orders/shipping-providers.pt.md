---
title: Fornecedores de Envio
---

Fornecedores de envio conectam sua loja a APIs de transportadoras para taxas de envio em tempo real, geração de rótulos e rastreamento de pacotes. O Spwig suporta transportadoras principais em todo o mundo e também permite que você crie tabelas de taxas manuais para transportadoras sem integração de API.

![Fornecedores de envio](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Fornecedores Disponíveis

| Fornecedor | Regiões | Recursos Principais |
|-----------|--------|------------------|
| **FedEx** | Global | Taxas em tempo real, impressão de rótulos, rastreamento, múltiplos pacotes |
| **UPS** | Global | Taxas em tempo real, impressão de rótulos, rastreamento, validação de endereço |
| **USPS** | Estados Unidos | Taxas nacionais e internacionais, rastreamento |
| **NinjaVan** | Sudeste Asiático | Entrega de última milha, suporte a pagamento em dinheiro |
| **Canada Post** | Canadá | Nacionais e internacionais, taxas de pacotes e cartas |
| **Australia Post** | Austrália | Nacionais e internacionais, pacotes e expressos |

## Conectar um Fornecedor

Navegue até **Configurações > Fornecedores de Envio** e clique em **Conectar Fornecedor** para iniciar o assistente de configuração.

### Etapa 1: Selecione o Fornecedor

Escolha entre os fornecedores de envio disponíveis. Cada cartão mostra as regiões e recursos suportados pelo fornecedor.

### Etapa 2: Instruções de Configuração

Revise o guia de configuração específico do fornecedor:
- Como criar uma conta de desenvolvedor/empresa com o fornecedor
- Onde encontrar suas credenciais de API
- Configurações de conta necessárias (ex.: número do remetente, número de metro)

### Etapa 3: Insira as Credenciais

Insira as credenciais de API da conta do seu fornecedor. Os campos necessários variam conforme o fornecedor:

- **Chave de API / Segredo** — Credenciais de autenticação
- **Número da Conta** — Seu número de conta ou remetente do fornecedor
- **Número de Metro** — Requerido por alguns fornecedores (ex.: FedEx)
- **Modo de Ambiente de Teste** — Ative para testar com a API de ambiente de teste do fornecedor antes de ir ao vivo

### Etapa 4: Testar Conexão

Clique em **Testar Conexão** para verificar suas credenciais. O assistente confirma:
- A autenticação da API é bem-sucedida
- As permissões da conta são válidas
- As consultas de taxa retornam resultados esperados

### Etapa 5: Configurar e Salvar

Finalize as configurações:
- **Ativo** — Ative ou desative o fornecedor
- **Nome de Exibição** — O nome exibido aos clientes no checkout
- **Endereço de Origem** — O endereço do depósito ou local de atendimento para cálculo de taxas

## Zonas de Envio

Zonas de envio definem áreas geográficas para cálculo de taxas. Navegue até **Configurações > Zonas de Envio** para gerenciá-las.

### Criar uma Zona

1. Clique em **+ Adicionar Zona**
2. Dê um nome à zona (ex.: "Nacional", "Europa", "Ásia-Pacífico")
3. Defina a cobertura da zona usando uma ou mais das seguintes opções:
   - **Países** — Selecione países específicos
   - **Estados/Províncias** — Restrinja a regiões específicas dentro de um país
   - **Padrões de Códigos Postais** — Corresponda códigos postais/ZIP usando padrões (ex.: "90*" para a área de Los Angeles)
4. Defina a **Prioridade** — Quando as zonas se sobrepõem, a zona com a prioridade mais alta é usada

### Correspondência de Zona

Quando um cliente insere seu endereço de envio no checkout, o sistema:
1. Verifica primeiros os padrões de códigos postais (mais específicos)
2. Depois, correspondências de estado/província
3. Depois, correspondências de país
4. Usa a zona com a prioridade mais alta correspondente

## Promoções de Envio

Promoções de envio aplicam modificadores condicionais às taxas de envio. Navegue até **Configurações > Promoções de Envio** para configurá-las.

### Tipos de Promoção

| Tipo de Promoção | Descrição |
|----------------|-----------|
| **Desconto %** | Reduz a taxa de envio por um percentual |
| **Desconto Fixo** | Reduz a taxa de envio por um valor fixo |
| **Substituir Custo** | Substitui a taxa por um valor específico |
| **Envio Grátis** | Define o custo de envio como zero |
| **Taxa Adicional %** | Adiciona uma taxa adicional em percentual à taxa |
| **Taxa Adicional Fixa** | Adiciona uma taxa adicional fixa à taxa |

### Condições

Cada promoção pode ter uma ou mais condições que devem ser atendidas:

| Condição | Exemplo |
|-----------|---------|
| **Valor do Carrinho** | Frete grátis para pedidos acima de $100 |
| **Peso Total** | Taxa adicional para pedidos acima de 30 kg |
| **Quantidade de Itens** | Desconto para pedidos com 5+ itens |
| **Zona de Envio** | Aplicar promoção apenas para envios nacionais |
| **Método de Envio** | Aplicar a métodos específicos de transportadora |
| **Produtos** | Tarifas especiais para produtos específicos |
| **Grupo de Clientes** | Clientes VIP têm frete grátis |
| **Intervalo de Data** | Promoções de envio de feriados |

### Prioridade da Promoção

- As promoções são avaliadas na ordem de prioridade (número mais baixo primeiro)
- **Parar outras promoções** — Quando ativado, se essa promoção corresponder, nenhuma outra promoção será verificada
- Múltiplas promoções podem se sobrepôr (ex: uma promoção de desconto de 10% mais uma promoção de frete grátis com limite de valor)

## Tabelas de Taxas

As tabelas de taxas fornecem preços em níveis com base em atributos do pedido. Navegue até **Configurações > Tabelas de Taxas de Envio** para configurá-las.

### Tipos de Tabela

Crie níveis de taxas com base em:
- **Peso** — Níveis de preço com base no peso total do pedido (ex: 0-1 kg = $5, 1-5 kg = $10)
- **Valor do Pedido** — Níveis de preço com base no subtotal do carrinho
- **Quantidade** — Níveis de preço com base na contagem de itens

### Criando uma Tabela de Taxa

1. Clique em **+ Adicionar Tabela de Taxa**
2. Nomeie a tabela e selecione o tipo de nível
3. Adicione níveis com intervalos mínimos/máximos e preços
4. Atribua a tabela de taxa a uma zona de envio

As tabelas de taxas são úteis quando você não usa taxas de API de transportadora e deseja definir sua própria estrutura de preços.

## Pacotes de Envio

Defina tamanhos padrão de embalagem para cálculos de taxa precisos. Navegue até **Configurações > Pacotes de Envio**.

Para cada tipo de pacote, defina:
- **Nome** — Descrição (ex: "Caixa Pequena", "Grande Taxa Fixa")
- **Dimensões** — Comprimento, largura, altura
- **Peso Máximo** — Peso máximo que o pacote pode conter
- **Padrão** — Use este pacote quando nenhuma embalagem específica for atribuída

As transportadoras usam as dimensões do pacote para cálculos de peso dimensional, o que pode afetar as taxas de envio.

## Transportadoras Manuais (Configurações de Transportadora)

Para transportadoras sem integração de API, crie configurações de transportadora manuais:

1. Navegue até **Configurações > Configurações de Transportadora**
2. Clique em **+ Adicionar Configuração**
3. Configure:
   - **Nome da Transportadora** — Nome exibido no checkout
   - **Modelo da URL de Rastreamento** — Padrão de URL com um espaço reservado {tracking_number} (ex: `https://track.carrier.com/?id={tracking_number}`)
   - **Entrega Estimada** — Intervalo de tempo de entrega a ser exibido aos clientes
4. Associe a uma tabela de taxas para preços

As transportadoras manuais fornecem links de rastreamento e estimativas de entrega sem integração de API em tempo real.

## Envio com Múltiplos Depósitos

Se você tiver múltiplos depósitos, o envio pode ser calculado a partir de origens diferentes:

- **Depósito Específico por País** — Atribua depósitos a países específicos para distâncias de envio mais curtas
- **Cadeia de Backup** — Defina qual depósito envia quando o depósito principal estiver fora de estoque
- **Atribuição por Produto** — Alguns produtos podem ser enviados apenas a partir de depósitos específicos

O sistema seleciona automaticamente o melhor depósito com base na localização do cliente e na disponibilidade do produto.

## Dicas

- Conecte APIs de transportadora para **taxas em tempo real** sempre que possível — elas são mais precisas do que tabelas de taxas fixas e ajustam-se ao peso, dimensões e destino.
- Crie uma **zona de envio "Resto do Mundo"** como uma opção para países não cobertos por zonas específicas.
- Use o tipo de promoção **Frete Grátis** com uma condição de valor do carrinho como incentivo de venda (ex: "Frete grátis para pedidos acima de $75").
- Teste os cálculos de taxas de envio com endereços e conteúdos de carrinho diferentes antes de ir ao ar.
- Configure **Configurações de Transportadora** com modelos de URL de rastreamento para qualquer transportadora local que não tenha integrações de API — os clientes ainda recebem links de rastreamento.
- Use **Pacotes de Envio** para obter preços precisos de peso dimensional de transportadoras como FedEx e UPS.