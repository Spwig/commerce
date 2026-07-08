---
title: Gerenciamento de Chaves de Licença
---

O gerenciamento de chaves de licença permite que você controle como as chaves de licença de software são geradas, armazenadas e entregues aos clientes quando eles compram produtos digitais. O Spwig oferece geração de chaves embutida, pools de chaves pré-carregados e integrações com serviços externos de gerenciamento de licenças.

## Visão Geral

Existem três maneiras de gerenciar chaves de licença no Spwig:

| Método | Melhor para |
|--------|---------|
| **Modelos de licença** | Gerar automaticamente chaves únicas em um formato personalizado no momento da compra |
| **Pools de licença** | Gerar previamente um lote de chaves para distribuição em massa |
| **Fornecedores externos** | Delegar a geração e o gerenciamento de chaves a um serviço terceirizado, como Keygen.sh |

Esses métodos podem ser combinados — por exemplo, um pool pode usar um modelo personalizado para definir o formato da chave e, opcionalmente, sincronizar as chaves geradas com um fornecedor externo.

## Modelos de chaves de licença

Um modelo de chave de licença define o *formato* das chaves geradas. Os modelos usam um padrão com espaços reservados que o Spwig preenche no momento da geração.

### Criando um modelo

1. Navegue até **Catálogo > Modelos de Chaves de Licença**
2. Clique em **+ Adicionar Modelo de Chave de Licença**
3. Insira um **Nome** (ex.: `Licença de Aplicativo Padrão`)
4. Configure o **Padrão** usando espaços reservados (veja abaixo)
5. Defina o **Prefixo** e **Sufixo** se necessário (ex.: um prefixo de `MYAPP` adiciona `MYAPP-` a cada chave)
6. Escolha o **Caractere Separador** (padrão: `-`)
7. Defina o **Conjunto de Caracteres** — os caracteres usados para segmentos aleatórios. O padrão exclui caracteres ambíguos como `0` e `O`, `1` e `I`
8. Defina **Comprimento Mínimo/Máximo** para validação
9. Clique em **Salvar**

### Espaços reservados do padrão

| Espaço Reservado | Descrição | Saída de exemplo |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N caracteres aleatórios do conjunto de caracteres | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | N dígitos de verificação para validação | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | O valor do prefixo do modelo | `MYAPP` |
| `{SUFFIX}` | O valor do sufixo do modelo | `PRO` |
| `{ORDER_ID}` | O número do pedido | `10045` |
| `{PRODUCT_SKU}` | O SKU do produto | `SOFTPRO` |
| `{DATE:FORMAT}` | Data formatada | `{DATE:YYMMDD}` → `260318` |

**Exemplo de padrão**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Isso gera chaves como: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Visualizando chaves

Após salvar um modelo, uma ação **Gerar Chave de Exemplo** está disponível na lista de modelos. Use isso para verificar se seu padrão gera chaves no formato esperado antes de atribuir o modelo a um produto.

## Pools de licença

Um pool de licença é um lote de chaves pré-geradas para um produto. Os pools são úteis quando:
- Você precisa de chaves para embalagem física (caixas de varejo, cartões impressos)
- Você trabalha com revendedores que precisam de lotes de chaves
- Você deseja gerar chaves com antecedência em vez de sob demanda

### Criando um pool de licença

1. Navegue até **Catálogo > Pools de Licença**
2. Clique em **+ Adicionar Pool de Licença**
3. Preencha os detalhes do pool:

| Campo | Descrição |
|-------|-------------|
| **Nome** | Nome descritivo (ex.: `Pacote de Varejo Q1 2026`) |
| **Produto** | O produto para o qual essas chaves são destinadas |
| **Modelo de Licença** | Modelo para o formato da chave (padrão é o modelo do produto) |
| **Total de Chaves** | Quantas chaves gerar |
| **Tipo de Chave** | Perpétua, assinatura ou teste |
| **Ativações Máximas** | Quantos dispositivos cada chave pode ativar |
| **Expira Após Dias** | Dias até que a licença expire após a primeira ativação (deixe em branco para não expirar) |
| **Pool Expira Em** | Data após a qual as chaves não utilizadas desse pool se tornam inválidas |
| **Sincronizar com Fornecedor** | Sincronizar opcionalmente as chaves geradas com um provedor de licenças externo |

4. Clique em **Salvar** — o Spwig começa a gerar as chaves em segundo plano

### Status do pool

| Status | Meaning |
|--------|---------|
| **Gerando** | As chaves estão sendo criadas em segundo plano |
| **Pronto** | Todas as chaves foram geradas e estão disponíveis para distribuição |
| **Esgotado** | Todas as chaves foram atribuídas a pedidos |
| **Expirado** | A data de validade do pool passou |

### Monitoramento de um pool

A lista de pools mostra quantas chaves foram distribuídas versus o total de chaves geradas. Abra um pool para ver a lista completa de chaves e seus status individuais.

## Fornecedores de licenças externos

Fornecedores externos são serviços de gerenciamento de licenças de terceiros que lidam com a geração de chaves e o rastreamento de ativações. Quando um cliente conclui uma compra, o Spwig se comunica com o fornecedor para gerar e registrar a chave.

### Fornecedores compatíveis

| Fornecedor | Tipo |
|----------|------|
| **Servidor de Licenças Integrado do Spwig** | Integrado — não é necessário uma conta externa |
| **Keygen.sh** | API de gerenciamento de licenças baseada em nuvem |
| **LicenseSpring** | Gerenciamento de licenças empresarial |
| **Cryptlex** | Gerenciamento de licenças com suporte offline |
| **API Personalizada** | Qualquer sistema de licença baseado em REST |

### Conectar um fornecedor

1. Navegue até **Catálogo > Fornecedores de Licenças**
2. Clique em **+ Adicionar Fornecedor de Licenças**
3. Preencha os detalhes do fornecedor:

| Campo | Descrição |
|-------|-------------|
| **Nome** | Um rótulo para esta conexão (ex.: `Keygen Produção`) |
| **Tipo de Fornecedor** | Selecione entre os fornecedores compatíveis |
| **Ponto de Extremidade da API** | URL base da API do fornecedor |
| **Chave da API** | Chave de autenticação para o fornecedor |
| **Segredo da API** | Se exigido pelo fornecedor |

4. Configure o comportamento de sincronização:
   - **Sincronizar no Pedido** — Sincronize automaticamente quando um cliente concluir uma compra
   - **Sincronizar na Ativação** — Relate ativações de dispositivos ao fornecedor
   - **Sincronizar na Desativação** — Relate desativações (útil para transferências de licenças e reembolsos)
   - **Sincronização Bidirecional** — Permita que o fornecedor atualize os registros do Spwig via webhooks

5. Clique em **Salvar**, depois clique em **Testar Conexão** para verificar se as credenciais funcionam

### Status da conexão

Cada fornecedor mostra um dos três status de conexão:

| Status | Meaning |
|--------|---------|
| **Não Testado** | A conexão ainda não foi verificada |
| **Conectado** | O último teste foi bem-sucedido |
| **Erro** | O teste de conexão falhou — verifique a mensagem de erro |

### Sincronização de licenças existentes

Para enviar manualmente chaves de licença existentes para um fornecedor (para configuração inicial ou após uma sincronização falhada), use a ação **Sincronizar Agora** da lista de fornecedores.

## Monitoramento da atividade de sincronização

Navegue até **Catálogo > Sincronizações de Licenças Externas** para revisar o log de sincronização. Cada registro mostra:
- A chave de licença que foi sincronizada
- O fornecedor para o qual foi enviada
- Direção (Spwig → Fornecedor ou Fornecedor → Spwig)
- Status (Pendente, Sucesso, Falhado)
- Detalhes do erro para sincronizações falhadas

As sincronizações falhadas são reprovadas automaticamente. Você também pode forçar uma repetição editando o registro e limpando o erro.

## Dicas

- Use o conjunto de caracteres padrão (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) para evitar caracteres ambíguos que os clientes frequentemente confundem — ele exclui `0`, `O`, `1` e `I`.
- Adicione um segmento `{CHECKSUM}` ao seu padrão de template para que os clientes e sua equipe de suporte possam detectar rapidamente chaves digitadas incorretamente.
- Para produtos de alto volume, use um pool em vez de geração sob demanda para garantir que as chaves sejam entregues instantaneamente no checkout.
- Defina **Pool Expires At** em lotes de chaves sazonais ou com prazo limitado para que chaves antigas e não utilizadas sejam invalidadas automaticamente.
- Sempre teste a conexão do fornecedor após a configuração e após quaisquer alterações nas credenciais — uma conexão quebrada significa que os clientes não recebem suas chaves.
- Se estiver usando sincronização bidirecional, configure a URL do webhook do seu fornecedor para apontar para o ponto de extremidade de webhook de licença do seu loja.