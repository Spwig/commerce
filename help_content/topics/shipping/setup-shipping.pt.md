---
title: Configuração de Envio
---

Este guia explica como configurar o envio para sua loja — desde a criação de métodos de envio básicos até a conexão com integrações de transportadoras para tarifas em tempo real.

## Visão Geral do Envio

O Spwig oferece duas abordagens para envio:

- **Métodos de Envio Manuais** — Métodos com tarifa fixa que você define (ex.: "Envio Padrão — R$29,99")
- **Integrações com Transportadoras** — Tarifas em tempo real de provedores como FedEx, UPS e DHL

Você pode usar qualquer uma das abordagens ou combinar ambas.

## Métodos de Envio

Os métodos de envio são as opções que seus clientes veem no checkout. Navegue até **Pedidos > Envios** na barra lateral para gerenciá-los.

![Shipping methods](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Criando um Método de Envio

1. Clique em **Adicionar Método de Envio**
2. Preencha os detalhes:
   - **Nome** — Nome de exibição mostrado aos clientes (ex.: "Entrega Expressa")
   - **Descrição** — Breve descrição do serviço
   - **Preço** — Custo fixo de envio
   - **Prazo Estimado de Entrega** — Estimativa do tempo de entrega (ex.: "3-5 dias úteis")
3. Clique em **Salvar**

## Zonas de Envio

As zonas de envio definem regiões geográficas onde seus métodos de envio se aplicam. Navegue até a seção **Zonas de Envio** para gerenciá-las.

![Shipping zones](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Criando uma Zona

1. Clique em **Adicionar Zona de Envio**
2. Configure a zona:
   - **Nome da Zona** — Nome interno (ex.: "Nacional", "Europa")
   - **Países** — Selecione quais países pertencem a esta zona
   - **Estados/Regiões** — Opcionalmente, restrinja a estados específicos
   - **Padrões de CEP** — Use padrões como "9*" para direcionar áreas específicas
3. Atribua métodos de envio a esta zona
4. Clique em **Salvar**

### Prioridade de Zona

Quando o endereço de um cliente corresponde a várias zonas, a zona mais específica tem prioridade. Uma zona com segmentação em nível estadual tem precedência sobre uma zona em nível de país.

## Integrações com Transportadoras

Conecte-se a transportadoras para oferecer tarifas calculadas em tempo real no checkout.

![Shipping carriers](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Provedores Disponíveis

Navegue e instale provedores de envio a partir do marketplace.

![Shipping providers](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

As transportadoras suportadas incluem:

- **FedEx** — Terrestre, Expresso, Internacional
- **UPS** — Terrestre, 2 Dias, Noturno, Mundial
- **DHL** — Expresso, eCommerce
- **USPS** — Prioritário, Primeira Classe, Media Mail
- E mais disponíveis através do Marketplace

### Configurando uma Transportadora

1. Vá à página de provedores de envio e clique em **Instalar** na transportadora desejada
2. Siga o assistente de configuração:
   - **Etapa 1** — Revisar detalhes do provedor
   - **Etapa 2** — Configurar ajustes gerais
   - **Etapa 3** — Inserir suas credenciais de API (número da conta, chave de API, etc.)
   - **Etapa 4** — Habilitar serviços específicos (Terrestre, Expresso, etc.)
   - **Etapa 5** — Testar a conexão
3. Uma vez conectado, as tarifas da transportadora aparecem automaticamente no checkout

### Credenciais de API

Cada transportadora requer uma conta de API:

- **FedEx** — Registre-se no Portal de Desenvolvedores da FedEx, crie um aplicativo e copie sua chave e segredo de API
- **UPS** — Registre-se no Kit de Desenvolvedores da UPS, solicite uma chave de acesso
- **DHL** — Entre em contato com a DHL para obter credenciais de API através do portal empresarial

## Regras de Envio

Crie regras avançadas para controlar quando e como os métodos de envio são oferecidos.

### Regras Comuns

- **Frete grátis acima de R$200** — Defina um valor mínimo do carrinho para frete grátis
- **Tarifa fixa para pedidos leves** — Tarifa fixa quando o peso do pedido está abaixo de um limite
- **Desabilitar expresso para áreas remotas** — Ocultar opções expressas baseado em CEPs
- **Acréscimo percentual** — Adicionar uma taxa de manuseio como percentual das tarifas da transportadora

### Criando uma Regra

1. Navegue até a seção de regras de envio
2. Clique em **Adicionar Regra**
3. Defina as condições (total do carrinho, peso, zona, etc.)
4. Defina a ação (ajustar tarifa, ocultar método, habilitar frete grátis)
5. Salve a regra

As regras são avaliadas em ordem — a primeira regra correspondente é aplicada.

## Frete Grátis

### Frete Grátis em Toda a Loja

Habilite o frete grátis globalmente em **Configurações > Configurações da Loja**:

- Ative o **Frete Grátis**
- Opcionalmente, defina um valor mínimo de pedido
- Escolha quais regiões se qualificam

### Frete Grátis Promocional

Crie ofertas de frete grátis por tempo limitado:

1. Vá para **Marketing > Vendas e Promoções**
2. Crie uma nova promoção
3. Defina a condição: "Total do carrinho acima de X"
4. Defina a ação: "Frete grátis"
5. Configure as datas de início e término

## Envio Internacional

Para pedidos internacionais, certifique-se de que seus produtos tenham:

- **Código HS** — Classificação tarifária do Sistema Harmonizado
- **País de Origem** — País de fabricação
- **Valor Aduaneiro** — Valor declarado para a alfândega

Esses campos estão na aba **Inventário** de cada produto. As transportadoras usam essas informações para gerar a documentação aduaneira automaticamente.

## Dicas

- Comece com métodos de envio manuais para colocar sua loja em funcionamento rapidamente, depois adicione integrações com transportadoras.
- Crie zonas de envio para seus destinos mais comuns primeiro.
- Sempre teste sua configuração de envio fazendo pedidos de teste com diferentes endereços.
- Use o recurso de acréscimo de tarifa para cobrir custos de manuseio e embalagem.
- Configure limites de frete grátis para aumentar o valor médio dos pedidos.
