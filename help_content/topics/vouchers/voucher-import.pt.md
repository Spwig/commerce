---
title: Importar em Lote Códigos de Voucher
---

O assistente de importação de vouchers permite que você crie centenas de códigos de voucher de uma vez, carregando uma planilha CSV ou XLSX. Isso é ideal quando você tem códigos pré-impressos, códigos de programas de fidelidade de um sistema de terceiros ou simplesmente precisa lançar uma campanha grande sem adicionar cada código manualmente.

![Lista de vouchers com botão Importar](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Começando uma importação

Navegue até **Marketing > Vouchers** e clique no botão **Importar** na área superior direita da página. Isso abre o assistente de importação de três etapas.

## Etapa 1: Carregue seu arquivo e defina as configurações do lote

![Formulário de upload de importação](/static/core/admin/img/help/voucher-import/import-upload.webp)

A primeira página tem duas partes: o upload do arquivo e as configurações de desconto do lote.

### Preparando seu arquivo

Carregue um arquivo `.csv` ou `.xlsx` com até 5 MB. O arquivo deve ter uma linha de cabeçalho como primeira linha. O requisito mínimo é uma única coluna contendo os códigos de voucher — todas as outras colunas são opcionais.

O importador reconhece automaticamente nomes de colunas comuns. Se seu arquivo usar qualquer um dos nomes abaixo, o Spwig pré-selecionará a mapeamento correto na próxima página sem cliques extras:

| Seu nome da coluna | Mapeia para |
|------------------|-----------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Códigos de voucher |
| `name`, `title`, `campaign` | Nome interno |
| `description`, `details`, `note` | Descrição voltada ao cliente |
| `external_id`, `member_id`, `reference` | ID externo |

**Dica:** Baixe primeiro o modelo XLSX (veja [Exportar vouchers como um modelo](#exporting-vouchers-as-a-template) abaixo) — ele usa os nomes exatos de coluna que o importador espera, então o mapeamento de coluna é automático.

### Limites de arquivo

- Tamanho máximo do arquivo: **5 MB**
- Máximo de linhas por importação: **5.000 códigos**

### Definindo as configurações de desconto do lote

Todos os vouchers no lote compartilharão as mesmas configurações de desconto que você configurar nesta página. Preencha os campos como faria ao criar um único voucher:

**Seção de desconto**

| Campo | Descrição |
|-------|-----------|
| **Tipo de desconto** | Percentual, Valor Fixo ou Frete Grátis |
| **Valor do desconto** | O percentual (0–100) ou valor fixo a ser deduzido |
| **Valor máximo do desconto** | Limite opcional para descontos percentuais (ex: limite um desconto de 20% em $50) |
| **Âmbito da aplicação** | Todo o carrinho, Produtos Específicos ou Categorias Específicas |

**Seção de validade**

| Campo | Descrição |
|-------|-----------|
| **Data de início** | Quando os códigos se tornam ativos (padrão é agora se deixado em branco) |
| **Data de término** | Quando os códigos expiram (deixe em branco para não expirar) |
| **Dias válidos** | Alternativa à data de término — os códigos expiram após esse número de dias desde a criação |

**Seção de limites de uso**

| Campo | Descrição |
|-------|-----------|
| **Máximo de usos totais** | Número total de redemptions permitidos para todos os clientes (em branco = ilimitado) |
| **Máximo de usos por cliente** | Quantas vezes um cliente pode usar qualquer código desse lote |
| **Valor mínimo do pedido** | Valor mínimo do carrinho necessário antes que o código seja aplicado |

**Restrições**

Marque qualquer combinação de:
- **Não pode ser aplicado a itens em promoção** — impede que o código seja acumulado com produtos já descontados
- **Não pode ser combinado com outros vouchers** — impede que os clientes usem dois códigos no mesmo pedido
- **Não pode ser combinado com itens em promoção** — semelhante ao acima, mas direcionado a itens com preço promocional
- **Apenas para clientes novos** — restringe o código a clientes sem pedidos concluídos anteriormente
- **Ativar imediatamente** — deixe marcado para tornar os códigos ativos assim que forem importados

Quando estiver satisfeito com as configurações, clique em **Continuar para a pré-visualização**.

## Etapa 2: Mapear colunas e revisar

![Página de mapeamento de colunas e pré-visualização](/static/core/admin/img/help/voucher-import/import-preview.webp)

A página de pré-visualização mostra quatro contadores de resumo no topo:

- **Linhas analisadas** — total de linhas de dados encontradas no seu arquivo

- **Serão importadas** — novos códigos que serão criados

- **Duplicatas** — códigos que já existem no seu catálogo

- **Serão ignoradas (inválidas)** — linhas rejeitadas devido a erros de validação (código vazio, código muito longo, etc.)

### Mapeamento de colunas

A tabela **Mapeamento de colunas** permite que você informe ao Spwig qual coluna no seu arquivo corresponde a cada campo do voucher. O Spwig detecta automaticamente nomes de cabeçalho comuns (veja a tabela acima), mas você pode alterar qualquer mapeamento usando o menu suspenso em cada linha.

Apenas a coluna **Código do voucher** é obrigatória. Os outros campos — **Nome interno**, **Descrição voltada ao cliente** e **ID externo** — são opcionais. Se você os ignorar, o Spwig usará valores padrão sensíveis (o nome interno padrão será "Voucher importado {code}").

### Estratégia de código duplicado

Se algum código no seu arquivo já existir no seu catálogo, você deve escolher como lidar com eles:

| Estratégia | O que acontece |

|----------|-------------|

| **Ignorar duplicatas** | Os códigos existentes permanecem exatamente como estão. Apenas novos códigos são criados. |

| **Substituir configurações** | Os códigos existentes são atualizados com as configurações de desconto deste lote. Seus códigos, contagens de uso e datas de criação são preservados. |

| **Falhar na importação** | A importação inteira é cancelada se mesmo uma duplicata for encontrada. Use isso quando você precisar de uma garantia de que nenhum código existente será afetado. |

Quaisquer códigos duplicados encontrados são listados em um painel expansível para que você possa revisá-los antes de decidir.

### Tabela de pré-visualização de dados

O final da página mostra as primeiras 20 linhas do seu arquivo para que você possa confirmar se o mapeamento de colunas parece correto antes de confirmar. Linhas que correspondem a códigos existentes são destacadas.

Quando tudo parecer certo, clique em **Importar N vouchers** para confirmar o lote.

## Etapa 3: Revisar o resultado

![Página de resultado da importação](/static/core/admin/img/help/voucher-import/import-result.webp)

Após a importação ser concluída, você verá um resumo mostrando:

- **Importados** — códigos criados com sucesso

- **Ignorados** — códigos que não foram criados (duplicatas ou linhas inválidas)

- **Linhas processadas** — total de linhas do seu arquivo que foram avaliadas

- **Falhados** — linhas que encontraram um erro inesperado

Clique em **Ver vouchers importados** para abrir a lista de vouchers filtrada apenas pelos códigos deste lote, tornando fácil verificar o resultado ou ativar em massa os novos códigos.

Se algo parecer errado — por exemplo, o tipo de desconto incorreto foi aplicado — você pode usar a estratégia **Substituir configurações** em uma nova importação para corrigir o lote sem precisar excluir e recriar os códigos.

Clique em **Importar outro lote** para iniciar um novo upload, ou em **Voltar para a lista de vouchers** para retornar ao seu catálogo completo.

## Exportar vouchers como um modelo

A lista de vouchers suporta uma ação de exportação XLSX que gera um arquivo na mesma ordem de colunas que o importador espera. Este é o método mais fácil para obter um modelo formatado corretamente:

1. Navegue até **Marketing > Vouchers**

2. Selecione os vouchers que deseja exportar (ou selecione todos)

3. Escolha **Exportar vouchers selecionados para XLSX** no menu suspenso **Ação**

4. Clique em **Ir**

O arquivo baixado possui todas as 21 colunas que o importador entende, incluindo campos que são de nível de lote no assistente de importação (tipo de desconto, datas, limites de uso, etc.). Você pode usar esse arquivo como referência ou fazer um ciclo de edição → re-importação dos seus códigos existentes usando a estratégia **Substituir configurações**.

## Dicas

Preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos.

- Faça o download de uma exportação XLSX primeiro para usá-la como modelo — os nomes das colunas estão pré-formatados para que o mapeamento automático os reconheça sem nenhuma ajuste na página de pré-visualização.
- Execute um lote de teste pequeno com 5–10 códigos antes de importar centenas para verificar se seu mapeamento de colunas e configurações do lote estão corretos.
- Use **Dias válidos** em vez de uma data de **Fim fixa** quando os códigos serão distribuídos ao longo do tempo — a expiração de cada código então conta a partir do momento em que foi importado, em vez de uma data do calendário única.
- Se você receber códigos de um sistema de fidelidade de terceiros, mapeie a referência de membro ou cliente do fornecedor para a coluna **ID Externo** para que você possa reconciliar as redemptions posteriormente.
- Após uma importação grande, clique em **Ver vouchers importados** na página de resultados para filtrar a lista apenas para o novo lote — você pode então editar em lote, ativar ou desativar como um grupo.
- Uma importação com falha (usando a estratégia de **Falha** para duplicatas) deixa seu catálogo inalterado, então é seguro corrigir o arquivo e tentar novamente quantas vezes for necessário.