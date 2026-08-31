---
title: Tags de Assinantes
---

Tags são rótulos que você cria para organizar seu público do Campaign Studio — marcadores curtos como `VIP`, `atacado` ou `evento-2026` que você define e aplica aos assinantes que se encaixam neles. Assim que um tag existir, você pode filtrar sua lista de assinantes por ele, aplicar ou removê-lo de qualquer número de pessoas de uma vez e — mais útilmente — usá-lo como condição ao construir um Segmento, para que seus campanhas e jornadas possam atingir exatamente as pessoas que você rotulou.

## O que são tags

Um tag é simplesmente um nome que você escolhe. O Spwig não vem com nenhuma tag interna e nunca aplica uma automaticamente — você decide como elas se chamam e quem recebe uma. Isso as torna adequadas para qualquer coisa específica ao seu próprio negócio que não se enquadre em um status que o Spwig já acompanhe: um nível de lealdade, uma conta de atacado, todos os que se inscreveram em uma feira, ou uma lista de evento única como `evento-2026`.

Cada tag também recebe um **Slug** — uma versão simplificada, compatível com URLs — gerado automaticamente quando você cria a tag. Segmentos e filtros usam o slug internamente; como comerciante, você quase nunca precisará olhar para ele.

## Criando um tag

Tags têm sua própria seção no admin. Abra **Campaign Studio > Assinantes**, depois clique em **Campaign Studio** no topo da página para ver a lista completa das seções do Campaign Studio e escolha **Tags de assinantes**.

1. Clique em **Adicionar tag de assinante**.
2. Insira um **Nome** — leituras curtas e específicas funcionam melhor, por exemplo `VIP`, `Atacado` ou `Evento 2026`.
3. O Spwig preenche um **Slug** correspondente enquanto você digita. Você pode deixá-lo como gerado.
4. Um campo opcional **Cor** também está disponível se você quiser registrar uma cor hexadecimal (ex. `#2563eb`) contra a tag para sua referência.
5. Clique em **Salvar**.

Você não precisa deixar o que estiver fazendo para criar um — um sinal verde **+** ao lado do campo **Tags** em qualquer página de edição de assinante abre o mesmo formulário "adicionar uma tag" em um popup. E se você tentar marcar vários assinantes antes de criar quaisquer tags, o seletor de tags oferece um atalho **Criar uma tag** que o leva diretamente lá.

## Atribuindo tags aos assinantes

O modo mais comum de aplicar uma tag é em lote, a partir da lista de assinantes:

1. Abra **Campaign Studio > Assinantes**.
2. Marque a caixa de seleção de cada assinante que deseja rotular (ou **Selecionar todos nesta página**).
3. Na lista suspensa **Ações em lote**, escolha **Adicionar tag aos selecionados…** (ou **Remover tag dos selecionados…** para desmarcar as pessoas).
4. Clique em **Ir**.
5. Escolha a tag da lista e clique em **Adicionar tag** (ou **Remover tag**).

![O seletor de tags em lote após escolher "Adicionar tag aos selecionados..." para quatro assinantes](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Após aplicado, um tag aparece como um pequeno chip na carta do assinante na lista, ao lado de seus selos de status e origem. Um filtro **Tag** também aparece no painel de filtros da lista de assinantes assim que você tiver pelo menos uma tag, para que você possa reduzir a lista a todos os que carregam uma tag específica — útil para verificar quem está em um público antes de construir uma campanha em torno dele.

![A lista de assinantes filtrada para a tag VIP, com o botão Importar CSV e os chips de tag visíveis](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Você também pode adicionar ou remover as tags de um único assinante diretamente da própria página de edição dele, usando o mesmo campo **Tags** que a ação em lote gerencia.

## Usando tags em segmentos

Segmentos são audiências salvas baseadas em regras às quais você aponta campanhas e jornadas. Assim que você tiver criado pelo menos uma tag, uma condição **Tem tag** se torna disponível no construtor de regras do segmento — ela não aparece em uma instalação limpa com nenhuma tag definida, então você não verá uma opção inútil antes de ela ser útil para você.

Para usá-la, abra **Campaign Studio > Segmentos**, adicione (ou edite) um segmento dinâmico e clique em **+ Adicionar condição**:

1. Defina o campo da condição como **Tem tag**.
2. Escolha um operador — **é** para uma única tag, ou **é algum de** quando você quiser frisar dessa forma.
3. Escolha a tag na lista suspensa.

![Uma condição "Tem tag" definida como VIP, exibindo uma contagem ao vivo dos assinantes correspondentes](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

A contagem no canto superior direito é atualizada à medida que você constrói a regra, permitindo que você veja exatamente quantos assinantes atualmente se qualificam antes de salvar. Cada condição **Tem tag** atualmente corresponde a uma tag por vez — se você deseja uma audiência que corresponda a *qualquer* uma de várias tags (por exemplo, `VIP` ou `Wholesale`), adicione uma condição **Tem tag** por tag e defina **Correspondência** como **qualquer**.

É isso que torna as tags úteis além da organização: um segmento construído com base em **Tem tag** se torna uma audiência que você pode selecionar como **Segmento** em um broadcast ou campanha recorrente, ou como a configuração **Somente para segmento** de uma jornada — assim, "todos marcados como VIP" podem ter sua própria série de boas-vindas, seu próprio boletim recorrente, ou simplesmente serem quem você seleciona na próxima vez que enviar um anúncio único.

## Dicas

- Mantenha os nomes das tags curtos e específicos — eles aparecem como chips compactos nos cartões de assinantes, então `VIP` é mais legível do que `Very Important Person - Tier 1`.
- Use o filtro **Tag** para verificar quem realmente está marcado antes de construir um segmento ou enviar uma campanha em torno dele.
- A marcação é aditiva — remover uma tag de um assinante nunca afeta nenhuma outra tag que ele tenha e nunca altera seu status, origem ou consentimento.
- Combine tags com outras condições do construtor de regras (como **Optou por marketing** ou **Total gasto**) no mesmo segmento para uma audiência mais precisa, não apenas uma tag isolada.
- Um assinante pode ter quantas tags você quiser — não há limite, então é perfeitamente aceitável usá-las para vários propósitos sobrepostos (uma camada de fidelidade *e* uma lista de eventos *e* uma nota de origem).
- Se uma tag deixar de ser útil, excluí-la de **Tags de assinantes** a remove de todos os assinantes a quem foi aplicada e de qualquer regra de segmento que a referenciava — os segmentos que a usavam simplesmente deixarão de corresponder a essa condição.