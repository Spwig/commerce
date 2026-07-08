---
title: Configurações de Transportadoras
---

Configurações de transportadoras definem transportadoras manuais (DHL, FedEx, UPS, transportadoras personalizadas) para remessas criadas sem integração de API — cada configuração fornece logotipo da transportadora, modelo de URL de rastreamento e configurações de exibição. Configurações do sistema (DHL, FedEx, UPS, USPS) já estão pré-configuradas e não podem ser excluídas, enquanto as configurações personalizadas permitem que os vendedores adicionem transportadoras regionais ou especializadas. As configurações de transportadoras vinculam-se a remessas manuais, onde os vendedores inserem números de rastreamento manualmente, em vez de comprar etiquetas por meio de APIs dos provedores.

Use configurações de transportadoras ao criar remessas manuais ou quando quiser links de rastreamento sem integração completa de API.

## Configurações do Sistema vs. Configurações Personalizadas

**Configurações do Sistema** (Pré-instaladas):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Não podem ser excluídas (is_system=True)
- É possível substituir a URL de rastreamento ou o logotipo
- Modelos de URL de rastreamento padrão fornecidos

**Configurações Personalizadas** (Criadas pelo vendedor):
- Transportadoras regionais (OnTrac, LaserShip, transportadoras regionais de correios)
- Transportadoras especializadas (transporte de carga, entrega de mão branca)
- Podem ser editadas ou excluídas
- Requer modelo de URL de rastreamento manual

---

## Configuração de Configurações de Transportadora

Cada configuração define:

**Configurações Básicas**:
- **Nome**: Nome de exibição da transportadora (ex: "DHL Express", "Correio Local")
- **Código**: Identificador interno (ex: "dhl", "local_courier")
- **Logotipo**: Imagem do logotipo da transportadora (opcional, usa ícone se não fornecido)
- **Ícone**: Ícone FontAwesome como alternativa (ex: "fa-truck")
- **Ativo**: Alternar visibilidade

**Configuração de Rastreamento**:
- **Modelo de URL de Rastreamento**: Padrão de URL com marcador de posição {tracking_id}
- **Substituição da URL de Rastreamento**: URL personalizada (substitui o modelo padrão)

**Configurações do Sistema** (apenas configurações do sistema):
- **É do Sistema**: Não pode ser excluído
- **É Padrão**: Uma padrão por tipo de transportadora

---

## Modelos de URLs de Rastreamento

As URLs de rastreamento usam o marcador de posição {tracking_id}:

**Exemplos**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Personalizado: `https://track.localcourier.com/tracking/{tracking_id}`

**Como Funciona**:
1. O vendedor cria uma remessa com o número de rastreamento "1234567890"
2. O sistema substitui {tracking_id} pelo número real
3. O cliente clica no link de rastreamento → redireciona para o site da transportadora
4. Resultado: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Criando uma Configuração de Transportadora Personalizada

**Passo a Passo**:

1. Navegue até Configurações > Envio > Configurações de Transportadora
2. Clique em "Adicionar Configuração de Transportadora"
3. Insira o nome (ex: "OnTrac")
4. Insira o código (slug: "ontrac")
5. Opcional: Carregue o logotipo da imagem
6. Selecione o ícone (fa-truck, fa-shipping-fast, etc.)
7. Insira o modelo de URL de rastreamento com {tracking_id}
8. Ative a opção = Sim
9. Salve

**Exemplo - OnTrac**:
```
Nome: OnTrac
Código: ontrac
URL de Rastreamento: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Ícone: fa-truck
Ativo: Sim
```

---

## Substituindo URLs de Rastreamento de Configurações do Sistema

As configurações do sistema podem ter substituições de URLs de rastreamento:

**Caso de Uso**: Sua conta de transportadora tem portal de rastreamento especial

**Como Substituir**:
1. Edite a configuração do sistema (ex: DHL)
2. Insira a URL de substituição no campo "Substituição da URL de Rastreamento"
3. A substituição tem prioridade sobre o modelo padrão
4. Salve

**Exemplo**:
```
Sistema: DHL
URL Padrão: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
URL de Substituição: https://track.dhl.com/special-account/{tracking_id}
Resultado: URL de substituição usada para todas as remessas DHL
```

---

## Logotipos de Transportadoras

**Diretrizes para Logotipos**:
- Formato: PNG ou SVG (SVG preferido por escalabilidade)
- Tamanho: 200×60px recomendado
- Fundo: Transparente ou branco
- Cor: Marca completa da transportadora

**Ícone de Alternativa**:
Se nenhum logotipo for carregado, o sistema exibe o ícone FontAwesome:
- fa-truck (padrão)
- fa-shipping-fast (expresso)
- fa-plane (transporte aéreo de carga)
- fa-box (pacote)

---

## Usando Configurações de Transportadora em Remessas

Ao criar uma remessa manual:

1. Pedidos > Detalhes do Pedido > Criar Remessa
2. Selecione o modo "Remessa Manual"
3. Escolha a transportadora a partir do menu suspenso de configurações
4. Insira o número de rastreamento
5. Opcional: Substitua a URL de rastreamento para esta remessa
6. Salve

**Exibição da Remessa**:
- Logotipo da transportadora exibido (ou ícone)
- Número de rastreamento exibido
- Link clicável de rastreamento (usa o modelo de URL da configuração)

---

## Transportadora Padrão

Uma configuração pode ser definida como padrão por sistema:

**Caso de Uso**: A transportadora mais comumente usada é automaticamente selecionada na criação de remessas

**Como Definir**:
1. Edite a configuração da transportadora
2. Marque "É Padrão"
3. Salve
4. A configuração padrão anterior (se houver) é automaticamente desmarcada

**Apenas uma configuração padrão é permitida** — definir uma nova configuração padrão remove a bandeira de configuração padrão anterior.

---

## Dicas

- **Use nomes descritivos** — "DHL Express" é melhor que "DHL"
- **Teste URLs de rastreamento** — Verifique se o modelo funciona com números de rastreamento reais
- **Carregue logotipos de transportadoras** — Aparência profissional em e-mails para clientes
- **Não exclua configurações do sistema** — Elas estão corretamente pré-configuradas
- **Use substituições com moderação** — Apenas quando a transportadora mudar o sistema de rastreamento
- **Defina a configuração padrão para a transportadora principal** — Economiza tempo durante a criação de remessas
- **Mantenha as configurações ativas** — Desative apenas se a transportadora for encerrada
- **Documente transportadoras personalizadas** — Adicione notas sobre transportadoras regionais

