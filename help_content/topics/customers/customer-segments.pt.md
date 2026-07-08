---
title: Segmentos de Clientes
---

Segmentos de clientes permitem que você classifique automaticamente seus clientes em grupos significativos com base no comportamento de compra deles. Uma vez segmentados, você pode usar esses grupos para focar seus esforços de marketing — por exemplo, oferecer recompensas de fidelidade a clientes VIP ou enviar campanhas de recuperação a clientes que não compraram há algum tempo.

O Spwig avalia os critérios de segmento contra as métricas de cada cliente e os atribui ao segmento de maior prioridade para o qual o cliente é elegível. Isso acontece automaticamente à medida que os dados do cliente são atualizados.

## Tipos de segmento disponíveis

O Spwig vem com um conjunto de tipos de segmento pré-definidos. Cada tipo de segmento tem um identificador interno fixo, mas você pode personalizar o nome de exibição, a descrição, os critérios e a cor para corresponder à forma como você pensa sobre seus clientes.

| Tipo de Segmento | Uso Típico |
|---|---|
| **Cliente Convidado** | Clientes que finalizaram a compra sem criar uma conta |
| **Novo Cliente** | Clientes que recentemente fizeram sua primeira compra |
| **Cliente Regular** | Clientes com um histórico de compras consistente |
| **Comprador Frequente** | Clientes que compram com frequência (intervalo curto entre pedidos) |
| **Alto Valor** | Clientes com gastos totais altos |
| **Cliente VIP** | Seus clientes mais valiosos e fiéis |
| **Caçador de Ofertas** | Clientes que tendem a comprar durante promoções |
| **Em Risco** | Clientes que não compraram há algum tempo |
| **Inativo** | Clientes que estiveram ausentes por um período prolongado |

## Entendendo os critérios de segmento

Cada segmento é definido por uma combinação de critérios. O Spwig verifica esses critérios contra as métricas armazenadas de cada cliente. Todos os critérios dentro de um segmento são combinados — o cliente deve satisfazer todas as condições definidas para ser elegível.

### Critérios de gastos

- **Mínimo Gasto Total** — o cliente deve ter gasto pelo menos esse valor em todas as ordens concluídas
- **Máximo Gasto Total** — o cliente não deve ter gasto mais do que esse valor

Use uma faixa de gastos para identificar uma camada específica. Por exemplo, definir Mínimo para $500 e Máximo para $2.000 identificaria clientes da camada média.

### Critérios de quantidade de pedidos

- **Mínimo de Pedidos** — o cliente deve ter pelo menos esse número de pedidos concluídos
- **Máximo de Pedidos** — o cliente não deve ter mais do que esse número de pedidos concluídos

Combinar Mínimo de Pedidos com um mínimo de gasto é uma maneira confiável de definir clientes VIP: eles compram com frequência *e* gastam generosamente.

### Critérios de recentezas

- **Mínimo de Dias desde a Última Compra** — a compra mais recente do cliente deve ter ocorrido pelo menos esse número de dias atrás
- **Máximo de Dias desde a Última Compra** — a compra mais recente do cliente deve ter ocorrido dentro desse número de dias

Critérios de recentezas são essenciais para segmentos de clientes em risco e inativos. Por exemplo, definir Mínimo de Dias para 90 e Máximo de Dias para 365 identificaria clientes que se tornaram silenciosos, mas ainda não foram completamente perdidos.

## Prioridade de segmento

Quando um cliente é elegível para mais de um segmento, o segmento com o **valor de prioridade mais alto** vence. Você pode definir a prioridade para cada segmento na seção **Configurações de Exibição** do formulário do segmento.

O segmento **Cliente Convidado** sempre é avaliado primeiro, independentemente da ordem de prioridade, porque o status de convidado é determinado pelo tipo de conta e não pelos critérios de compra.

## Visualizando e gerenciando segmentos

Navegue até **Clientes > Segmentos de Clientes** para ver todos os seus segmentos configurados. A lista mostra o nome de exibição de cada segmento, o tipo interno, a cor atribuída, a prioridade, a contagem atual de clientes correspondentes e se o segmento está ativo.

![Lista de Segmentos de Clientes](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Criando ou editando um segmento

1.

Navegue até **Clientes > Segmentos de Clientes**
2.

Clique em um segmento existente para editá-lo, ou clique em **+ Adicionar Segmento de Cliente** para criar um novo
3.

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

Preencha a guia **Informações do Segmento**:
   - **Nome** — selecione o tipo de segmento interno do menu suspenso
   - **Nome de Exibição** — o nome legível para humanos exibido no administrador (ex.: "Clientes VIP")
   - **Descrição** — uma nota interna breve explicando o que este segmento representa
4.

Defina critérios nas guias relevantes:
   - **Critérios - Gastos** — gasto total mínimo e máximo
   - **Critérios - Pedidos** — número mínimo e máximo de pedidos
   - **Critérios - Recência** — dias mínimos e máximos desde a última compra
5.

Configure **Configurações de Exibição**:
   - **Cor** — uma cor em formato hexadecimal usada para identificar visualmente este segmento em listas
   - **Prioridade** — um número maior significa que este segmento será avaliado primeiro
   - **Ativo** — desmarque para desativar o segmento sem excluí-lo
6.

Clique em **Salvar** para aplicar as alterações

### Exemplo: Configurando um segmento VIP

Aqui está um exemplo realista para um segmento VIP de alto valor:

| Campo | Valor |
|---|---|
| Nome | `vip` |
| Nome de Exibição | Clientes VIP |
| Gasto Mínimo Total | $1.000 |
| Pedidos Mínimos | 5 |
| Máximo de Dias desde a Última Compra | 180 |
| Prioridade | 90 |
| Cor | `#FFD700` |

Isso significa: um cliente é considerado VIP se tiver gasto pelo menos $1.000, realizado pelo menos 5 pedidos e feito uma compra dentro dos últimos 6 meses.

### Exemplo: Configurando um segmento de Risco

| Campo | Valor |
|---|---|
| Nome | `at_risk` |
| Nome de Exibição | Em Risco |
| Dias Mínimos desde a Última Compra | 60 |
| Dias Máximos desde a Última Compra | 180 |
| Prioridade | 30 |
| Cor | `#FF6B35` |

## Usando segmentos para marketing direcionado

Os segmentos são exibidos nos perfis de clientes em todo o administrador, então sua equipe saberá imediatamente a qual camada cada cliente pertence. Use essa informação para:

- **Executar campanhas de cupons direcionados** — crie cupons restritos a clientes de um segmento específico, depois use seu sistema de e-mail para enviá-los apenas a esse grupo
- **Priorizar o suporte** — marque clientes VIP ou de alto valor para que sua equipe possa fornecer suporte prioritário
- **Planejar re-engajamento** — revise regularmente os segmentos Em Risco e Inativos para identificar clientes que precisam de um e-mail de re-engajamento ou oferta especial
- **Ajustar o orçamento de marketing** — foque o orçamento de aquisição em canais que trazem clientes de alto valor analisando quais coortes de segmentos eles convertem

## Dicas

- Comece com os tipos de segmentos pré-configurados antes de criar critérios personalizados — eles cobrem as necessidades de segmentação mais comuns prontas para uso
- Revise regularmente a contagem de clientes em cada segmento; um segmento VIP com zero clientes ou um segmento Em Risco crescendo rapidamente ambos valem a pena investigar
- Use o campo **Prioridade** com cuidado — se os critérios se sobrepuserem entre segmentos (ex.: um cliente qualifica-se para ambos Comprador Frequente e Alto Valor), o segmento com maior prioridade vence
- Desative segmentos que não estão sendo usados no momento em vez de excluí-los — você pode reativá-los posteriormente sem reconfigurar os critérios
- Os critérios de segmento são verificados contra métricas de clientes armazenadas, que são recalculadas automaticamente. Se as contagens de segmento parecerem desatualizadas, as métricas podem ser recalculadas na seção Métricas de Cliente do administrador