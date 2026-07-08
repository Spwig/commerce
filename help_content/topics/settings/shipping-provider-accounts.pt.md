---
title: Contas de Provedores de Envio
---

Contas de provedores de envio conectam sua loja às APIs dos transportadores (FedEx, UPS, DHL) para cálculo de taxas em tempo real e compra automática de etiquetas. Cada conta armazena credenciais criptografadas da API, monitora a saúde da conexão e vincula-se a métodos de envio em tempo real. Os provedores obtêm taxas ao vivo no checkout com base nas dimensões do pacote, peso, origem e destino — eliminando a manutenção manual de tabelas de taxas e garantindo preços precisos dos transportadores.

Use contas de provedores quando precisar de taxas de envio calculadas pelo transportador ou geração automática de etiquetas em vez da criação manual de envios.

## Provedores de Envio Suportados

Spwig suporta principais transportadores por meio de componentes de provedores instaláveis:

### FedEx

**Serviços**: Ground, Express, International
**API**: FedEx Web Services
**Funcionalidades**: Taxas em tempo real, compra de etiquetas, rastreamento, taxas internacionais

### UPS

**Serviços**: Ground, Air, Worldwide
**API**: UPS Developer API
**Funcionalidades**: Taxas em tempo real, geração de etiquetas, rastreamento, validação de endereços

### DHL

**Serviços**: Express, eCommerce, International
**API**: DHL Express API
**Funcionalidades**: Taxas internacionais, documentos de alfândegas, rastreamento

### Provedores Adicionais

Instale a partir do mercado de componentes conforme necessário (USPS, Canada Post, Australia Post, etc.)

---

## Configuração da Conta do Provedor

Cada conta do provedor requer:

### Informações Básicas

- **Nome de Exibição**: Como a conta aparece no painel de administração (ex.: "Conta de Produção do FedEx")
- **Provedor**: Selecione o componente do provedor instalado a partir do menu suspenso
- **Ativo**: Ative/desative sem excluir as credenciais
- **Padrão**: Defina como conta padrão para este provedor (apenas uma conta padrão por provedor)

### Credenciais da API (Criptografadas)

**Varia conforme o provedor**, normalmente inclui:

**FedEx**:
- Número da Conta
- Número do Medidor
- Chave da API
- Segredo da API

**UPS**:
- Número da Licença de Acesso
- ID do Usuário
- Senha
- Número da Conta

**DHL**:
- ID do Site
- Senha
- Número da Conta

**Todas as credenciais são criptografadas em repouso** e são descriptografadas apenas quando realizando chamadas da API.

### Endereço de Origem

- **Endereço Padrão de Envio**: Endereço do depósito/origem para cálculo de taxas
- Alguns provedores exigem configuração específica de origem em seus dashboards

### Configurações

Opções específicas do provedor (varia conforme o transportador):

- **Modo de Teste**: Use os pontos de extremidade de sandbox/teste do transportador
- **Taxas Negociadas**: Use as taxas negociadas com o transportador (se disponíveis)
- **Incluir Seguro**: Cite automaticamente seguro nas taxas
- **Taxa Residencial**: Aplique taxas de entrega residencial
- **Assinatura Necessária**: Requisições de assinatura padrão

---

## Criando uma Conta de Provedor

**Processo de Configuração em 6 Etapas**:

**Etapa 1: Obter Acesso à API do Transportador**
1. Crie conta com o transportador (FedEx.com, UPS.com, DHL.com)
2. Solicite acesso à API/Desenvolvedor
3. Complete o onboarding da API do transportador (pode levar 1-3 dias úteis)
4. Receba as credenciais da API por e-mail ou portal do desenvolvedor

**Etapa 2: Instale o Componente do Provedor** (se não pré-instalado)
1. Vá para Configurações > Componentes > Mercado
2. Procure pelo nome do transportador (ex.: "FedEx")
3. Instale o componente do provedor de envio
4. Aguarde a instalação ser concluída

**Etapa 3: Crie a Conta do Provedor no Spwig**
1. Navegue até Configurações > Envio > Contas de Provedor
2. Clique em "Adicionar Conta de Provedor"
3. Selecione o provedor a partir do menu suspenso
4. Insira o nome de exibição

**Etapa 4: Insira as Credenciais da API**
1. Preencha os campos de credencial (varia conforme o provedor)
2. As credenciais são criptografadas automaticamente ao salvar
3. Opcional: Ative o modo de teste para testes iniciais

**Etapa 5: Teste a Conexão**
1. Clique no botão "Testar Conexão"
2. O sistema tenta fazer uma chamada à API do transportador
3. Verifique se o status "Conectado" aparece
4. Verifique o carimbo de tempo last_tested_at

**Etapa 6: Vincule a um Método de Envio**
1. Crie ou edite um método de envio (Configurações > Carrinho > Métodos de Envio)
2. Defina method_type = "Real-Time"
3. Selecione a conta do provedor a partir do menu suspenso
4. Salve o método

---

## Monitoramento do Status da Conexão

Contas de provedores rastreiam a saúde da conexão:

### Valores de Status

**Desconhecido** (cinza): Nunca testado ou ainda não conectado

**Conectado** (verde): Última chamada à API bem-sucedida, credenciais válidas

**Erro** (vermelho): Última chamada à API falhou, credenciais podem ser inválidas

### Último Testado

- **Carimbo de Tempo**: Quando a conexão foi verificada pela última vez
- **Atualizações Automáticas**: Toda vez que o provedor for usado (busca de taxa, compra de etiqueta)
- **Teste Manual**: Clique no botão "Testar Conexão" a qualquer momento

### Solução para Conexões com Falha

**Causas Comuns**:
- Credenciais da API incorretas (erros de digitação, copiadas com espaço extra)
- Chave da API do transportador expirada ou revogada
- Modo de teste ativado, mas usando credenciais de produção (ou vice-versa)
- Endereço IP não incluído na lista branca com o transportador
- Downtime da API do transportador

**Passos de Solução**:
1. Verifique se as credenciais correspondem exatamente ao painel do transportador
2. Verifique se a configuração do modo de teste corresponde ao tipo de credencial
3. Revise a página de status da API do transportador para interrupções
4. Entre em contato com o suporte do transportador para verificação da conta

---

## Fluxo de Busca de Taxas

Como as taxas em tempo real funcionam no checkout:

**1. Cliente Insere Endereço**
- Endereço de envio inserido
- Carrinho calcula peso total + dimensões

**2. Sistema Prepara Solicitação de Taxa**
- Obtém credenciais da conta do provedor (descriptografadas)
- Calcula dimensões do pacote a partir dos itens do carrinho (usa pacotes de envio se definidos)
- Prepara solicitação da API com origem, destino, pacotes

**3. API do Provedor Chamada**
- Solicitação enviada à API do transportador com credenciais de autenticação
- Transportador calcula taxa com base na zona, peso, dimensões
- Resposta inclui opções de serviço (Ground, Express, etc.)

**4. Taxas Exibidas**
- Sistema analisa resposta do transportador
- Normaliza para formato padrão
- Markup opcional aplicado (se configurado)
- Taxas mostradas ao cliente no checkout

**5. Cliente Seleciona Serviço**
- Cliente escolhe a opção preferida
- Taxa selecionada salva no pedido

**Exemplo de Fluxo de API**:
```
Solicitação para API do FedEx:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // gramas
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

Resposta do FedEx:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Compra de Etiqueta (Opcional)

Se o provedor suportar geração de etiqueta:

**Fluxo de Trabalho**:
1. Cliente completa o pedido
2. Vendedor cria o envio (Pedidos > Detalhes do Pedido > Criar Envio)
3. Selecione a conta do provedor + serviço
4. Sistema chama a API de etiqueta do provedor
5. PDF da etiqueta gerado e anexado ao envio
6. Número de rastreamento preenchido automaticamente
7. Etiqueta pronta para impressão

**Benefícios**:
- Nenhuma necessidade de login manual no site do transportador
- Rastreamento sincronizado automaticamente
- Formulários de alfândegas gerados automaticamente (internacional)
- Geração de etiquetas em lote possível

---

## Markup de Taxas

Adicione markup do vendedor às taxas do transportador:

**Configuração** (em método de envio, não em conta do provedor):
- **Tipo de Markup**: Percentual ou Fixo
- **Valor do Markup**: Ex.: 15% ou $2,50

**Exemplo**:
```
Taxa do Transportador: $12,50
Markup: 15%
Cliente Paga: $14,38

OU

Taxa do Transportador: $12,50
Markup: $2,50 (fixo)
Cliente Paga: $15,00
```

**Casos de Uso**:
- Cobrir custos de embalagem/manuseio
- Adicionar margem de lucro ao envio
- Compensar taxas de cartão de crédito no envio

---

## Múltiplas Contas de Provedor

Você pode criar múltiplas contas para o mesmo provedor:

**Casos de Uso**:
1. **Teste vs Produção**
   - Conta de Teste: Credenciais do sandbox do transportador
   - Conta de Produção: Credenciais de produção

2. **Múltiplos Depósitos**
   - Conta do Depósito A: Origem = Los Angeles
   - Conta do Depósito B: Origem = Nova York

3. **Diferentes Taxas Negociadas**
   - Conta A: Taxas padrão
   - Conta B: Taxas de desconto por volume

**Cada conta pode vincular-se a diferentes métodos de envio** para configuração flexível.

---

## Dicas

- **Teste no sandbox primeiro** - Use credenciais de teste do transportador antes de ir ao vivo
- **Monitore o status da conexão** - Verifique regularmente o painel para status de erro
- **Defina pacotes de envio** - Dimensões precisas melhoram as cotações de taxas
- **Use taxas negociadas** - Ative se tiver descontos por volume com o transportador
- **Defina origem realista** - Use endereço real de envio para zonas precisas
- **Mantenha credenciais seguras** - Nunca compartilhe chaves da API, atualize periodicamente
- **Tenha método de backup** - Mantenha método de taxa fixa ativo se a API do transportador falhar
- **Monitore limites da API do transportador** - Alguns transportadores limitam chamadas da API por dia
- **Atualize credenciais com urgência** - Quando o transportador rotacionar chaves, atualize imediatamente
- **Use nomes descritivos** - "FedEx LA Warehouse" é melhor que "FedEx 1"