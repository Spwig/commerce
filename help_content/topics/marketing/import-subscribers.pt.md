---
title: Importando assinantes de um CSV
---

Se você já tem uma lista de e-mails em outro lugar — uma antiga ferramenta de e-mail, uma planilha de inscrições para boletins, uma pilha de escaneamentos de crachás de feiras — não precisa adicionar esses contatos ao Spwig um a um. A importação de assinantes do Campaign Studio lê um arquivo CSV ou Excel e adiciona todos os contatos válidos ao seu público de uma só vez, prontos para receber tags, segmentação e e-mails.

## Antes de importar: consentimento

Cada importação exige que você marque uma caixa confirmando: **"Estes contatos concordaram em receber e-mails de marketing de mim."** Isso não é uma formalidade — importe apenas contatos que realmente optaram por receber e-mails de marketing de você. Isso é importante por dois motivos:

- **É um requisito legal na maioria dos lugares.** Enviar e-mails de marketing para pessoas que nunca concordaram em recebê-los viola as leis de consentimento em muitas jurisdições.
- **Protege a entregabilidade dos seus e-mails.** Enviar e-mails para pessoas que nunca optaram por recebê-los gera reclamações de spam e rejeições, que os provedores de caixa de entrada usam para decidir se *qualquer* um dos seus e-mails — incluindo para pessoas que optaram por recebê-los — chega à caixa de entrada.

Se uma lista não vem claramente de inscrições com opt-in, não a importe.

## Preparando seu arquivo

O importador aceita um arquivo `.csv` ou `.xlsx` com uma linha de cabeçalho. Apenas uma coluna é obrigatória:

| Coluna | Obrigatória? | Observações |
|--------|-----------|-------|
| **E-mail** | Sim | Deve ser um endereço de e-mail válido. |
| **Nome** | Não | Usado para personalizar e-mails. |
| **Sobrenome** | Não | Usado para personalizar e-mails. |
| **Idioma** | Não | O código de idioma preferido do assinante (ex.: `en`, `es`). |

As colunas são correspondidas a esses campos automaticamente pelo nome do cabeçalho, então você não precisa renomear nada antes — variações comuns como `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname` ou `Locale` são todas reconhecidas.

Cada importação é limitada a **5 MB** e **5.000 linhas**. Se sua lista for maior que isso, divida-a em arquivos menores e importe-os um após o outro.

## Importando seus contatos

1. Abra **Campaign Studio > Subscribers** e clique em **Import CSV**.
2. Escolha seu arquivo `.csv` ou `.xlsx`.
3. Escolha o que acontece **para contatos já na sua lista** — veja [Tratamento de duplicatas](#handling-duplicates) abaixo.
4. Opcionalmente, escolha uma tag em **Tag imported contacts as** para rotular todos nesta importação (ex.: `Event 2026`) — veja [Subscriber Tags](/help/subscriber-tags) para mais sobre tags.
5. Marque **These contacts have agreed to receive marketing email from me**.
6. Clique em **Continue**.

![O formulário de upload de importação com um arquivo escolhido, uma tag selecionada e consentimento confirmado](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

O Spwig então mostra uma pré-visualização antes que qualquer coisa seja realmente importada:

![A pré-visualização da importação mostrando contagens de novos, existentes e ignorados inválidos com motivos](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Novos contatos** — linhas que criarão um assinante totalmente novo.
- **Já na sua lista** — linhas cujo endereço de e-mail corresponde a um assinante existente.
- **Ignorados (inválidos)** — linhas que não puderam ser lidas, cada uma listada com seu número de linha e o motivo (um formato de e-mail inválido, uma célula de e-mail vazia ou uma duplicata de uma linha anterior no mesmo arquivo).

Verifique esses números, então clique em **Import now** para confirmar a importação, ou **Cancel** para desistir sem alterar nada.

## Tratamento de duplicatas

Uma linha é contada como duplicata quando seu endereço de e-mail corresponde a um assinante que você já possui. Você escolhe como o Spwig trata essas linhas no formulário de upload:

| Opção | O que acontece |
|--------|--------------|
| **Deixá-los inalterados** *(padrão)* | O nome e o idioma do assinante existente são mantidos como estão. |
| **Atualizar seu nome / idioma** | O primeiro nome, sobrenome e idioma do assinante existente são atualizados a partir do arquivo (apenas para os campos que o arquivo realmente fornece). |

A tag que você escolher para a importação é aplicada a **todos no arquivo** — novos e contatos existentes — independentemente da opção de duplicata escolhida.

Portanto, importar sua "lista VIP" com a tag **VIP** também marca as pessoas que você já possui.

A opção de duplicados controla apenas se o *nome e o idioma* de um contato existente serão sobrescritos.

## Após a importação

Cada contato criado por uma importação é registrado com a origem **Importação** e marcado como consentido no momento em que você executou a importação (não em uma data anterior em que possam ter optado por participar em outro lugar). Seu primeiro e último nome — se o arquivo os forneceu — são armazenados em seu registro de assinante, o que significa que os campos de mesclagem `[[first_name]]` e `[[last_name]]` em suas campanhas agora se personalizam corretamente para eles também, mesmo que nunca tenham criado uma conta Spwig.

## Dicas

- Exporte sua lista de origem para um CSV ou `.xlsx` de uma única folha com uma linha de cabeçalho limpa antes de fazer o upload — folhas extras, células mescladas ou linhas de resumo podem confundir o correspondência de colunas.
- Use **Marcar contatos importados como** para criar imediatamente a audiência exata que você desejará segmentar em seguida — veja [Tags de Assinantes](/help/subscriber-tags) para construir um segmento a partir dela.
- Sempre leia os motivos de **Ignorado (inválido)** antes de assumir que uma importação falhou — algumas linhas ignoradas com motivos claros são normais para a maioria das listas do mundo real.
- Reexecutar o mesmo arquivo é seguro: os contatos que você já importou são tratados como duplicados na segunda vez, e não recriados.
- Se você estiver consolidando várias listas pequenas, marque cada importação de forma diferente (por exemplo, `Importação: Evento de Janeiro`, `Importação: Feira Comercial`) para que possa diferenciá-las mais tarde, mesmo depois que todas forem misturadas em sua audiência principal.
- Para listas com mais de 5.000 linhas, divida por um limite óbvio (alfabético, por origem ou por data de coleta) em vez de um corte arbitrário, para que cada lote permaneça fácil de identificar posteriormente.