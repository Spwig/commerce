---
title: Feeds de Produtos
---

Feeds de produtos permitem que você exporte seu catálogo para plataformas de compras, como Google Shopping e Facebook Catalog. Uma vez conectado, os dados dos seus produtos são sincronizados automaticamente em um horário pré-estabelecido, para que seus anúncios sempre reflejam os preços, estoque e detalhes dos produtos atuais.

Sua loja usa um sistema de componentes de provedores para feeds. Cada provedor de feed (Google, Facebook ou outros) é instalado como um componente e depois conectado por meio de uma conta de provedor. Você pode executar vários provedores de feed ao mesmo tempo — por exemplo, um feed para Google Shopping e outro separado para Facebook.

## Conectando um provedor de feed

Antes de sincronizar seu catálogo, você precisa instalar e conectar pelo menos um componente de provedor de feed.

### Instalando um componente de provedor

Componentes de provedor estão disponíveis no mercado de componentes Spwig. Seu administrador de loja os instala por meio do sistema de atualização de componentes. Uma vez instalado, o componente do provedor aparece como uma opção ao criar uma conta de provedor de feed.

### Criando uma conta de provedor de feed

1. Navegue até **Marketing > Provedores de Feed**
2. Clique em **+ Adicionar Conta de Provedor de Feed**
3. Preencha o formulário:

**Seção de Informações do Provedor:**
- **Site** — selecione sua loja (existe apenas uma)
- **Componente do Provedor** — escolha o provedor de feed instalado (ex: Google Shopping, Facebook Catalog)
- **Nome da Conta** — um nome descritivo, como `Google Shopping — Principal` ou `Facebook Catalog — EUA`

**Seção de Configuração:**
- **Ativo** — marque para habilitar a geração e sincronização de feed
- **Principal** — marque se este é seu provedor de feed principal para este tipo de plataforma
- **Prioridade** — controla a ordem de classificação na lista (números mais baixos aparecem primeiro)
- **Config** — configurações específicas do provedor (veja abaixo)

4. Clique em **Salvar**

### Opções de configuração de feed

O campo **Config** aceita um objeto JSON com as seguintes opções:

| Opção | Valores | Descrição |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Quão frequentemente o feed é regenerado automaticamente |
| `format_preference` | `xml`, `csv`, `json` | Formato de saída (a maioria das plataformas prefere XML) |
| `include_variants` | `true` / `false` | Incluir variantes de produto como entradas de feed separadas |
| `target_country` | Código do país, por exemplo, `"US"` | País-alvo para o feed |
| `content_language` | Código de idioma, por exemplo, `"en"` | Idioma dos dados do produto |

#### Exemplo de configuração para feed XML diário com destino aos EUA:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtrando quais produtos aparecem no feed

Você pode controlar exatamente quais produtos são incluídos adicionando uma seção `product_filter` à configuração:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Opção de filtro | Descrição |
|---------------|-------------|
| `status` | Incluir apenas produtos com esses status. Use `["published"]` para incluir apenas produtos ativos. |
| `in_stock_only` | Defina como `true` para excluir produtos fora de estoque |
| `categories` | Limitar a IDs específicas de categoria |
| `brands` | Limitar a IDs específicas de marca |

Você também pode excluir produtos específicos por seus IDs usando `exclude_products`:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Monitorando o status da sincronização

A lista de contas de provedor de feed mostra o status de sincronização de cada feed conectado com uma visão geral:

- **PENDENTE** — nenhuma sincronização foi executada ainda, ou o feed está aguardando para ser gerado
- **SINCRONIZANDO** — uma sincronização está em andamento
- **SUCESSO** — a última sincronização foi concluída sem erros
- **ERRO** — a última sincronização falhou; a mensagem de erro é mostrada na página de detalhes da conta

A lista também mostra o número de produtos no feed atual e quando a última sincronização foi executada.

## Visualizando feeds gerados

Navegue até **Marketing > Feeds de Produtos** para ver os arquivos de feed gerados. Cada entrada representa uma captura de feed gerada e mostra:

- **Conta do Fornecedor** — a qual conta de fornecedor este feed pertence
- **Formato** — XML, CSV ou JSON
- **Contagem de Produtos** — número de produtos incluídos
- **Tamanho** — tamanho do arquivo do feed gerado
- **Gerado em** — quando foi criado
- **Expira em** — quando esta versão armazenada em cache expira
- **Status** — se o feed ainda é válido ou expirou
- **Contagem de Downloads** — quantas vezes este feed foi baixado

Os feeds são somente leitura no admin — eles são gerados automaticamente pelo processo de sincronização.

## Visualizando histórico de sincronização

Navegue até **Marketing > Logs de Sincronização de Feed** para ver um histórico completo de todas as tentativas de sincronização para todas as suas contas de feed. Cada entrada de log registra:

- A conta de fornecedor que foi sincronizada
- O tipo de sincronização (Completa, Incremental, Manual ou Agendada)
- Status (Sucesso, Parcialmente Sucesso, Falhou, etc.)
- Produtos sincronizados, falhados e pulados
- Duração da sincronização
- Quaisquer mensagens de erro

O painel de logs de sincronização no topo da página mostra estatísticas gerais: total de sincronizações, taxa de sucesso e duração média da sincronização. Use os filtros **Conta** e **Tipo de Sincronização** para se concentrar em um feed específico.

### O que fazer quando uma sincronização falhar

1. Navegue até **Marketing > Logs de Sincronização de Feed** e localize a entrada falhada
2. Clique na entrada do log para visualizar a **Mensagem de Erro** e **Detalhes do Erro** completos
3. Causas comuns incluem:
   - Campos de produto obrigatórios ausentes (título, preço, imagem)
   - Credenciais de API inválidas ou expiradas — reinstale o componente do fornecedor para atualizar as credenciais
   - Erros de rede ao se conectar à API do fornecedor
4. Uma vez que o problema seja resolvido, a próxima sincronização agendada será executada automaticamente, ou você pode disparar uma sincronização manual a partir da conta do fornecedor

## Dicas

- Defina `"sync_interval": "daily"` para a maioria dos casos de uso — o Google e o Facebook não exigem atualizações mais frequentes, a menos que você tenha uma volatilidade de preço muito alta
- Sempre inclua `"in_stock_only": true` em seu filtro de produto para evitar anunciar produtos que os clientes não podem comprar
- Use um nome descritivo para a conta que inclua a plataforma e o mercado-alvo (ex: `Google Shopping — UK`) para facilitar o gerenciamento de múltiplos feeds
- A contagem de **Produtos no Feed** na conta do fornecedor informa imediatamente se menos produtos do que o esperado estão sendo incluídos — verifique suas configurações de filtro de produto se a contagem parecer baixa
- Marque uma conta como **Feed Principal** para cada tipo de fornecedor; algumas ferramentas de relatório usam isso para identificar seu feed principal
- Revise o log de sincronização após quaisquer alterações em massa no seu catálogo de produtos para confirmar que os dados atualizados foram coletados corretamente