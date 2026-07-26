---
title: Após sua migração
---

Uma migração concluída é o início da sua revisão, não o fim. A etapa 6 do assistente fornece um resumo do que foi transferido, uma ferramenta para corrigir links que ainda apontam para seu antigo site e um relatório que você pode baixar para seus registros. Este tópico passa por revisão do que verificar antes de considerar a migração concluída, incluindo o trabalho de impostos, envio e ativação que o assistente em si não faz por você.

## Lendo seus resultados

No topo da página de conclusão, você verá uma linha de cartões de estatísticas — um por tipo de dado (Produtos, Categorias, Clientes, Pedidos, etc.) — seguida por uma tabela **Resumo de Importação** com as colunas Importado, Pulado, Falhado e Total para cada etapa que foi executada.

- **Importado** — itens criados com sucesso no Spwig.
- **Pulado** — itens que sua plataforma de origem tinha, mas o Spwig não criou. Isso quase sempre é esperado: com **Pular itens existentes** ativado na etapa 3, qualquer coisa que corresponda a um item já existente no Spwig (por SKU, e-mail, etc.) é deixada como está, em vez de ser duplicada. Uma contagem alta de pulados após uma tentativa de repetição normalmente significa apenas que a primeira tentativa já criou esses registros.
- **Falhado** — itens que o Spwig tentou criar, mas não conseguiu, devido a um problema de dados, uma dependência ausente ou um erro na plataforma de origem. Uma contagem de falhas diferente de zero vale a pena investigar; veja [Resolução de Problemas de Migração](migration-troubleshooting) para saber como ler os logs e quais são suas opções de limpeza.

> **Nota:** Se alguma etapa mostrar falhas, não assuma que o armazém revertiu algo para compensar — ele não faz isso. O que foi importado antes da falha está no seu armazém ao lado de tudo que foi bem-sucedido. Revise-o da mesma forma que você faria com um resultado parcial normal.

## Reescrita de links

Produtos, páginas e posts de blog importados da sua plataforma antiga frequentemente contêm links de volta ao seu domínio original — uma URL de imagem, um link de "produto relacionado", uma referência cruzada interna. Se o Spwig detectar qualquer um desses links no conteúdo que acabou de importar, um painel **Reescrita de Links** aparecerá na página de conclusão.

Cada link detectado é agrupado pela página ou produto do qual veio e mostrado com:

- **URL Original** — o link exatamente como apareceu no conteúdo importado.
- **URL Sugerido** — a melhor estimativa do Spwig para a página equivalente no seu novo armazém, se uma for encontrada.
- **Correspondência** — uma porcentagem de confiança para essa sugestão. Links sem uma correspondência razoável aparecem como **Nenhum** e não têm nenhuma URL sugerida para aprovar.

Para cada link, você pode **Aprovar** a sugestão ou **Pular** ela, uma de cada vez. **Aprovar automaticamente as altas confianças** aprova todas as sugestões com 85% ou mais em um único clique — uma economia de tempo, mas ainda vale a pena verificar aleatoriamente depois. Sugestões abaixo desse limite são as que valem a pena abrir manualmente: uma correspondência de 50-70% pode ser o produto certo com o nome errado, ou pode estar bem longe, e apenas uma olhada humana pode dizer.

Aprovar ou pular marca apenas um link — nada no seu conteúdo muda até que você clique em **Aplicar Links Aprovados**, que reescreve todos os links aprovados de uma só vez. Isso significa que é seguro trabalhar pela lista em mais de uma sessão antes de comprometer.

> **Dica:** Deixe qualquer link que você não tenha certeza como **Pular** em vez de aprovar uma suposição. Você sempre pode corrigir manualmente um link antigo de domínio aleatório depois; uma reescrita errada aplicada a dezenas de produtos é mais trabalho para desfazer.

## Verificando seus dados

Trate os cartões de estatísticas como um ponto de partida, não como prova de que tudo está correto. Gaste alguns minutos verificando aleatoriamente:

- **Produtos** — Abra uma dúzia de produtos, especialmente aqueles com variações (tamanho, cor, etc.), e confirme se as opções de variação e preços vieram corretamente, e se as imagens estão anexadas e exibidas no site de vendas, e não apenas no administrador.
- **Categorias** — Confirme se a hierarquia de categorias parece correta, especialmente se você migrou do Shopify, onde coleções são importadas como uma lista plana em vez de uma árvore aninhada.
- **Contas de clientes** — Verifique aleatoriamente e-mails e endereços em alguns registros.

Clientes migrados não levam sua antiga senha consigo — o Spwig não tem como lê-la da plataforma de origem — então **os clientes precisarão redefinir sua senha** na primeira vez que fizerem login.

Considere enviar um e-mail de aviso uma vez que você estiver online.
- **Pedidos** — Verifique se os totais, status e itens de um conjunto de pedidos correspondem ao que você viu na antiga plataforma.
- **Produtos derivados de extensões** — Se você migrou do WooCommerce com extensões como Subscriptions, Bundles, Gift Cards, Composite Products ou Bookings, verifique produtos que usaram essas extensões.

Dados de extensão que não podem ser lidos não bloqueiam a importação do produto — ele ainda chega, apenas sem essa configuração extra — então esses produtos são os mais prováveis de precisarem de um ajuste manual.

## Configurando impostos e envio

As opções do passo 4 do assistente para importar configurações de impostos e zonas de envio registram suas preferências, mas elas não são aplicadas à importação — nenhuma taxa de imposto ou zona de envio é criada a partir delas. Isso é esperado: **a configuração de impostos e envio é um passo normal e separado que você completa diretamente no Spwig** após a importação de dados ser concluída, da mesma forma que você faria ao configurar uma nova loja.

O controle **Ajuste de Preço** no mesmo passo é a exceção — ele realmente entra em vigor para importações de WooCommerce, CSV e Shopify, alterando o preço base de cada produto conforme ele é criado. Se você definir um e os preços parecerem errados, essa é a origem da alteração. Veja [Mapping de Campos de Migração](migration-field-mapping) para os detalhes.

Antes de ir ao ar, configure:

- Suas taxas de imposto — veja [Configuração de Imposto](tax-configuration) para configurar taxas por país, estado ou região, incluindo quaisquer isenções que seus produtos necessitem.
- Suas zonas e métodos de envio — veja [Configuração de Envio](setup-shipping) para recriar as opções de envio que seus clientes tinham na antiga plataforma.

Faça isso antes de testar o checkout, para que seu pedido de teste reflita os totais reais.

## Baixando seu relatório

A página de conclusão oferece três downloads:

- **Baixar PDF** — um resumo formatado com metadados da tarefa, contagens por etapa e uma lista de erros, limitada aos **primeiros 20 erros**.
- **Baixar CSV** — o mesmo resumo em formato de planilha, limitado aos **primeiros 50 erros**.
- **Baixar Logs** — todas as entradas de log para a tarefa, sem limite.

Se o número de falhas for pequeno, o PDF ou CSV será suficiente. Para uma migração com um grande número de falhas, baixe os logs em vez disso — o único dos três com o registro completo em vez de uma amostra truncada.

> **Dica:** Registros de tarefas de migração — incluindo seus logs e relatórios — permanecem no Spwig indefinidamente; nada os remove em um cronograma. Baixe uma cópia de qualquer forma se quiser usá-la para registros offline ou compartilhá-la com alguém que não tenha acesso de administrador, mas não há um cronômetro forçando você a fazê-lo hoje.

## Ir ao ar

Uma vez que você estiver satisfeito com sua configuração de dados, impostos e envio:

1. **Teste o checkout do início ao fim.** Adicione um produto ao carrinho, conclua o checkout e confirme que impostos, envio e pagamento são calculados e processados corretamente, idealmente com um método de pagamento real no modo de teste.
2. **Atualize seu DNS** para apontar seu domínio apenas para o Spwig após esse teste ter sucesso. Não mude o DNS primeiro e depois depure — os clientes poderiam encontrar um checkout quebrado no meio do caminho.
3. **Mantenha sua loja antiga disponível, em um estado somente leitura ou "fechado",** até que você esteja confiante de que a nova está lidando com pedidos corretamente. Isso lhe dá uma alternativa sem colocar em risco pedidos sendo feitos na antiga plataforma após a mudança.

## Revogando credenciais da plataforma de origem

Uma vez que você tenha verificado que a migração está completa e não espera executá-la novamente, volte para sua plataforma de origem e revogue ou exclua a chave de API, o aplicativo ou a integração que criou para ela (veja [Migrando do WooCommerce](migrate-from-woocommerce) ou o guia equivalente da plataforma para onde essa credencial está localizada).

O Spwig não precisa de acesso contínuo à sua loja antiga após o importe ser concluído, então removê-lo fecha uma credencial que você não usa mais.

## Dicas

- **Skipped é normalmente aceitável, failed não é** — uma grande quantidade de skipped após uma tentativa com Skip existing items ativado é esperada; uma contagem não nula de failed merece uma verificação nos logs.
- **Não se apresse ao clicar em Apply Approved Links** — aprovações e skips podem ser alteradas livremente até que você clique em Apply, então tenha cuidado com os de baixa confiança.
- **Configure impostos e frete antes da sua primeira venda ao vivo**, e não depois — o importe não faz isso por você, e uma taxa de imposto não configurada é fácil de ser ignorada até que um cliente reclame.
- **Avise os clientes sobre redefinições de senha** se você estiver enviando um e-mail para sua lista de clientes sobre a migração, para que o primeiro login não seja uma surpresa.
- **Baixe seu relatório antes do marco de 90 dias** se precisar dele para registros contábeis ou de conformidade.
- **Mantenha a loja antiga disponível, somente leitura, por um tempo** — custa pouco e fornece uma rede de segurança durante seus primeiros dias ativos no Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Página de conclusão da migração mostrando as cartões de estatísticas e a tabela de resumo Imported/Skipped/Failed/Total
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Painel de Reescrita de Links com sugestões agrupadas, porcentagens de confiança e os controles Approve/Skip/Apply Approved Links
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->