---
title: Teste A/B
---

O **teste A/B** do Campaign Studio permite experimentar de dois a quatro **variantes** — diferentes versões da mesma campanha — em uma parte do seu público antes de comprometer-se com o envio completo. Altere apenas a linha de assunto ou crie conteúdo totalmente diferente para cada variante. O Spwig divide uma amostra da sua lista igualmente entre as variantes, observa o desempenho de cada uma e envia automaticamente a variante com melhor desempenho para todos que não viram o teste.

## Configuração de um teste

Primeiro, crie sua campanha normalmente no construtor visual do Campaign Studio — escreva uma linha de assunto, projete seu conteúdo e escolha o **Segmento** que deseja alcançar. Essa campanha se torna o **contêiner** do teste. Uma vez que você anexe um teste A/B a ela, o próprio contêiner nunca é enviado diretamente — sua função é manter as configurações, e o público definido para alcançá-lo é exatamente o pool contra o qual o teste é executado.

Dois locais abrem o assistente de teste A/B:

- O botão **Teste A/B** na barra de ferramentas do construtor visual.
- O ícone **Teste A/B** no cartão da campanha em **Campaign Studio > Campanhas**.

Uma vez que um teste existe em uma campanha, esse mesmo botão leva você diretamente aos seus resultados em vez do assistente, e o cartão da campanha recebe um pequeno distintivo **A/B** para que você possa identificá-lo na lista de relance.

## O que testar

A primeira etapa do assistente pergunta o que deve diferir entre as variantes:

| Opção | O que muda | Medido por |
|--------|--------------|-------------|
| **Linha de assunto** | Cada variante envia exatamente o mesmo conteúdo — apenas a linha de assunto difere. O teste mais comum. | Taxa de abertura |
| **Conteúdo** | Cada variante é um design separado que você cria no construtor visual. | Taxa de cliques |

![A etapa "O que você deseja testar?", com Linha de assunto selecionada](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Escolhendo suas variantes

O que você insere a seguir depende do que você escolheu:

- **Linha de assunto** — digite um assunto para cada variante (2–4). Duas linhas são mostradas no início; clique em **Adicionar outro assunto** para uma terceira ou quarta.
- **Conteúdo** — apenas escolha quantas variantes você deseja (2–4). Cada variante começa como uma cópia exata do design atual do seu contêiner, então você só precisa alterar o que está testando.

De qualquer forma, o Spwig rotula as variantes como **A**, **B**, **C** e **D** na ordem em que você as insere — você as verá como "Variante A", "Variante B" e assim por diante a partir daqui.

![A etapa de Variantes com três linhas de assunto inseridas para as variantes A, B e C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Para um teste de conteúdo, você não projeta as variantes no próprio assistente — após criar o teste, o cartão de cada variante no hub de resultados recebe um pequeno ícone de lápis que o abre no mesmo construtor visual que você usou para o contêiner. Isso está disponível apenas enquanto o teste ainda está em **Rascunho**; uma vez que você iniciar o teste, os designs são travados para que o que você está medindo não mude durante o teste.

## Configurações do teste

A última etapa do assistente cobre como o teste é executado e decidido:

| Configuração | O que faz |
|---------|--------------|
| **Amostra do teste** | A parte do seu público usada para o teste, dividida igualmente entre as variantes: 20%, 30%, 50% ou 100%. O restante — o **holdout** — recebe o vencedor posteriormente. Escolher 100% testa sua lista inteira de uma vez, então não há holdout restante para enviar um vencedor. |
| **Vencedor decidido por** | **Taxa de abertura** ou **Taxa de cliques**. Padrão é taxa de abertura para um teste de linha de assunto e taxa de cliques para um teste de conteúdo, já que é isso que cada um realmente mede — mas você pode alterá-lo de qualquer forma. |
| **Janela do teste (horas)** | Quanto tempo para coletar aberturas e cliques antes de escolher um vencedor, de 1 a 168 horas (uma semana completa). |
| **Enviar automaticamente o vencedor para o restante do público** | Ativado por padrão. Quando marcado, o Spwig envia a variante vencedora para o holdout assim que a janela terminar, sem nenhuma ação adicional da sua parte. |

Um cartão de revisão curto na parte inferior resume suas escolhas antes de você confirmar.

![A etapa Configurações com as opções de amostra, métrica, janela e envio automático definidas, além de um cartão de revisão](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Iniciando o teste

Clique em **Criar teste** para salvar a configuração — isso ainda não envia nada. Você será direcionado ao hub de resultados do teste com o status **Rascunho**, mostrando cada variante com zero destinatários até o momento e dois botões: **Iniciar teste** e **Cancelar teste**.

![Um teste recém-criado com status Rascunho, mostrando três variantes prontas para iniciar](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Clique em **Iniciar teste** quando estiver pronto. O Spwig divide sua amostra de teste igualmente entre as variantes e envia e-mails para cada uma imediatamente — você não precisa fazer mais nada; um job em segundo plano verifica quando a janela do teste tiver passado e decide o vencedor por conta própria. O status da própria campanha contêiner permanece como **Rascunho** durante todo esse processo — isso é esperado, pois são as variantes (e depois o vencedor) que realmente são enviadas, nunca o contêiner.

Seu público precisa ser grande o suficiente para que cada variante receba um número significativo de destinatários. O Spwig impede o início de um teste se qualquer variante terminar com zero pessoas, mas um teste que realmente valha a pena ser lido precisa de mais do que o mínimo — mire em algumas centenas de destinatários ou mais antes de confiar no resultado.

## Durante a execução do teste

Uma vez iniciado, o hub muda para **Testando** e exibe "Teste em execução — o vencedor é decidido automaticamente em torno de" a data e a hora em que a janela termina. As contagens de destinatários e as taxas de abertura/clique ao vivo são atualizadas a cada visita, juntamente com um gráfico de barras comparando a taxa de abertura e a taxa de clique de cada variante lado a lado — não apenas a métrica que você escolheu para decidir o vencedor.

![Um teste em execução mostrando contagens de destinatários ao vivo, taxas de abertura/clique e um gráfico de comparação](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

Você também pode acompanhar todos os testes a partir do **painel do Campaign Studio**: seu painel *Testes A/B recentes* lista seus testes em execução e recentemente decididos — cada um com sua confiança à vista — e links diretos para os resultados, juntamente com cartões contando quantos testes estão em execução e quantos foram decididos nos últimos 30 dias.

## Lendo os resultados

Quando a janela do teste termina, o Spwig escolhe a variante com a maior taxa na métrica escolhida, marca o teste como **Concluído** e — se **Enviar automaticamente o vencedor** estiver marcado e houver um grupo de controle para enviar — envia essa variante por e-mail para todos que não fizeram parte do teste. O cartão da variante vencedora é destacado e carrega um selo **Vencedor**; o gráfico de comparação permanece no lugar para que você possa ver como as variantes se compararam.

![Um teste concluído com a variante vencedora destacada e um selo Vencedor](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Tenha em mente que os números nesta página são sempre para a amostra do teste, não para sua lista inteira — com uma amostra de 20%, você está lendo como um quinto do seu público respondeu, não todos.

## Quão confiável é o resultado?

Uma taxa de abertura ou clique mais alta nem sempre significa que uma variante é genuinamente melhor — com um público pequeno, uma variante pode sair na frente puramente por acaso. Por isso, junto com o vencedor, o Spwig mostra **quão confiante ele está de que o resultado é real**, com base no tamanho da diferença e no número de destinatários. Você verá uma de três leituras:

- **Um resultado claro** — O Spwig tem pelo menos 95% de confiança de que a variante líder genuinamente supera as outras. Este é um resultado sobre o qual você pode agir.
- **Muito apertado para decidir** — há um líder, mas a diferença é pequena o suficiente para poder ser acaso. A porcentagem mostrada é o quão confiante o Spwig está, abaixo da marca de 95%. Considere reexecutar com um público maior ou uma janela de teste mais longa antes de tirar conclusões.
- **Dados insuficientes até o momento** — poucos destinatários (ou poucas aberturas e cliques) para distinguir as variantes de alguma forma. Isso é comum em listas pequenas; aumente o público ou deixe o teste rodar por mais tempo.

[![](A completed test showing a clear result — the winning variant carries a confidence badge and the summary reads "statistically clear"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp))

O mesmo resultado aparece enquanto um teste está em andamento, então você pode acompanhar o resultado se firmar — ou não — antes do fim do período. Como a confiança depende muito do tamanho da audiência, este é o motivo prático para visar algumas centenas ou mais destinatários por teste: em uma lista muito pequena, mesmo uma diferença aparentemente grande normalmente será lida como "demasiado próxima para ser definida".

Observe que, quando o envio automático estiver ativado, o Spwig ainda enviará a variante com a maior taxa para o restante da sua audiência, mesmo que o resultado seja inconclusivo — a leitura da confiança serve para lhe dizer quão confiável é o resultado, e não para impedir o envio.

## Cancelando um teste

**Cancelar teste** está disponível enquanto um teste está em **Rascunho** ou **Teste**, e o interrompe sem que nenhum vencedor seja enviado. Serve para quando você mudou de ideia ou cometeu um erro na configuração — não algo que deva ser usado com frequência, pois, uma vez que um teste seja cancelado (ou tenha sido concluído normalmente), não haverá botão para configurar um novo nele mesmo. Se quiser executar outra comparação no futuro, crie uma nova campanha para isso.

## Dicas

- Escolha primeiro um teste de **Assunto** — é o mais simples de configurar e a razão mais comum para fazer um teste A/B.
- Use um teste de **Conteúdo** quando quiser comparar designs ou ofertas verdadeiramente diferentes, e não apenas palavras no assunto.
- Finalize o design de todas as variantes de um teste de conteúdo — usando o ícone de lápis em cada cartão — antes de clicar em **Iniciar teste**. Você não pode editar o design de uma variante após o início do teste.
- Mantenha o **Amostra de teste** abaixo de 100% se quiser que o Spwig envie automaticamente o vencedor para o restante da lista após o teste — em 100% não haverá ninguém para ele alcançar.
- Dê ao período do teste tempo suficiente para abranger os hábitos normais de leitura dos seus inscritos (24 horas cobre confortavelmente um dia inteiro de fuso horário e caixas de entrada) em vez de decidir um vencedor apenas com as primeiras horas ou dois.