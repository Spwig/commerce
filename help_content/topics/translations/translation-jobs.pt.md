---
title: Trabalhos de Tradução
---

Trabalhos de Tradução automatizam a tradução em massa de grandes volumes de conteúdo. Em vez de traduzir manualmente cada produto um por um, crie um trabalho que traduza seu catálogo inteiro — ou subconjuntos específicos — em segundo plano. Os trabalhos são executados de forma assíncrona, então você pode continuar trabalhando enquanto centenas ou milhares de campos são traduzidos automaticamente.

Use trabalhos de tradução ao ativar novos idiomas, importar novos produtos ou preencher lacunas de conteúdo não traduzido.

## O que são Trabalhos de Tradução?

Um trabalho de tradução é uma tarefa em segundo plano que:

1. **Varre o conteúdo** em busca de campos traduzíveis (produtos, páginas, posts de blog, etc.)
2. **Identifica campos não traduzidos ou desatualizados** com base no escopo do trabalho
3. **Envia os campos para o motor de tradução** (modelo de IA local ou provedor externo)
4. **Salva as traduções** de volta ao seu conteúdo
5. **Relata a conclusão** com estatísticas sobre os campos traduzidos

Os trabalhos são executados via fila de tarefas Celery, então eles não bloqueiam sua interface de administração.

## Quando usar Trabalhos de Tradução

**Lançamento de um novo idioma**:
- Ative o alemão como novo idioma
- Crie um trabalho: traduzir todos os produtos do inglês para o alemão
- Resultado: todo o catálogo estará disponível em alemão em minutos/horas (dependendo do tamanho)

**Importação de novos produtos**:
- Importe 500 novos produtos em inglês
- Crie um trabalho: traduzir novos produtos para todos os idiomas ativos
- Resultado: o novo estoque estará imediatamente disponível em todos os mercados

**Preenchimento de lacunas**:
- O relatório de cobertura mostra que os Produtos estão apenas 60% traduzidos para o francês
- Crie um trabalho: traduzir apenas os campos de produto faltantes em francês
- Resultado: a cobertura em francês aumenta para ~100%

**Atualização de traduções desatualizadas**:
- O modelo de tradução foi melhorado ou um novo provedor está disponível
- Crie um trabalho: re-traduzir todos os produtos para o espanhol
- Resultado: traduções em espanhol de maior qualidade em todo o catálogo

## Criando um Trabalho de Tradução

Navegue até **Configurações > Trabalhos de Tradução** e clique em **+ Criar Trabalho**.

### Configuração do Trabalho

**Nome do Trabalho** - Rótulo descritivo (ex.: "Traduzir produtos para o alemão", "Novos posts de blog - todos os idiomas")

**Tipo de Conteúdo** - O que traduzir:
- Produtos
- Categorias de produtos
- Páginas
- Posts de blog
- Metadados SEO
- Modelos de e-mail
- Todos os tipos de conteúdo

**Idioma de Origem** - O idioma do qual você está traduzindo (normalmente seu idioma padrão)

**Idioma(s) de Destino** - Um ou mais idiomas para os quais você deseja traduzir (selecione múltiplos para tradução paralela)

**Escopo** - Qual subconjunto de conteúdo:
- **Todos os itens** - Traduzir tudo, independentemente das traduções existentes
- **Apenas os não traduzidos** - Pular campos que já têm traduções
- **Criados/alterados desde a data** - Apenas conteúdo novo ou recentemente alterado
- **Itens específicos** - Selecione produtos/páginas individuais (filtragem avançada)

**Motor de Tradução** - Qual serviço usar:
- Modelo de IA local (padrão, sem custos de API)
- Provedor externo específico (DeepL, Google, Azure, AWS)
- Auto-selecionar (usa a preferência configurada)

**Bloquear Traduções** - Se deseja bloquear os campos traduzidos contra sobreescrita futura automática (útil para traduções revisadas)

### Opções Avançadas

**Ignorar Campos Bloqueados** - Se ativado, respeita as traduções bloqueadas existentes (recomendado)

**Sobrescrever Existente** - Re-traduzir mesmo que existam traduções (use para melhorias de qualidade)

**Filtros de Campo** - Traduzir apenas campos específicos (ex.: nomes e descrições de produtos, ignorar atributos)

**Tamanho do Lote** - Quantos itens processar de uma vez (padrão: 50, aumente para processamento mais rápido se o servidor puder lidar)

**Prioridade** - Trabalhos com alta prioridade são executados antes dos normais (use com parcimônia)

## Ciclo de Vida e Status do Trabalho

Os trabalhos passam por esses estados:

**Fila** - Trabalho criado, aguardando que um trabalhador o pegue

**Processando** - Trabalhador está ativamente traduzindo o conteúdo

**Concluído** - Todas as traduções foram concluídas com sucesso

**Falhou** - O trabalho encontrou erros (verifique o log de erros)

**Cancelado** - Parado manualmente pelo administrador

**Pausado** - Pausado temporariamente (pode ser retomado)

## Monitoramento do Progresso do Trabalho

A página de detalhes do trabalho mostra:

**Barra de Progresso** - Percentual concluído

**Estatísticas**:
- Total de itens para traduzir
- Itens concluídos
- Itens restantes
- Tempo estimado restante

**Log em Tempo Real** - Fluxo de atividade de tradução (útil para depuração)

**Contagem de Erros** - Quantos campos falharam na tradução (com razões)

## Resultados e Estatísticas do Trabalho

Quando um trabalho é concluído, a página de resultados mostra:

**Resumo**:
- Total de campos processados
- Traduzidos com sucesso
- Traduções falhadas
- Pular (já traduzidos, bloqueados ou excluídos pelos filtros)

**Quebra-Down por Item**:
- Quais produtos/páginas foram traduzidas
- Quantos campos por item
- Quaisquer erros encontrados

**Métricas de Desempenho**:
- Tempo total decorrido
- Média de traduções por segundo
- Motor de tradução usado

## Lidando com Traduções Falhadas

Se algumas traduções falharem:

**Revise o log de erros** - Identifica quais campos falharam e por quê

**Causas comuns de falha**:
- Limite de taxa de API atingido (provedor externo)
- Timeout do motor de tradução (texto muito longo)
- Formato de campo inválido (erro de análise JSON)
- Modelo não suporta par de idiomas

**Opções de tentativa**:
- Corrija o problema subjacente
- Crie um novo trabalho apenas para os itens falhados
- Use um motor de tradução diferente

## Cancelando e Pausando Trabalhos

**Cancelar** - Para o trabalho imediatamente, descarta qualquer tradução em andamento (traduções concluídas são salvas)

**Pausar** - Pausa temporariamente o trabalho, pode retomar depois de onde parou

**Retomar** - Continua um trabalho pausado

Use pausar/retomar quando precisar liberar recursos do servidor temporariamente.

## Estratégias de Trabalhos em Lote

**Estratégia 1: Idioma por Idioma**:
- Crie trabalhos separados para cada idioma de destino
- Mais fácil monitorar o progresso por idioma
- Pode priorizar idiomas importantes
- Distribui a carga ao longo do tempo

**Estratégia 2: Tudo de Uma Vez**:
- Um único trabalho traduzindo para todos os idiomas ativos
- Conclusão mais rápida overall
- Maior carga no servidor durante o processamento
- Gerenciamento de trabalho mais simples

**Estratégia 3: Tipo de Conteúdo por Tipo de Conteúdo**:
- Traduza primeiro produtos (prioridade mais alta)
- Depois categorias, páginas, posts de blog
- Permite rollout progressivo
- Mais fácil testar e verificar traduções

Escolha com base na capacidade do servidor, urgência e tamanho do catálogo.

## Agendamento de Trabalhos

Agende trabalhos recorrentes para lidar com conteúdo novo automaticamente:

**Trabalhos Diários** - Traduzir quaisquer produtos criados/atualizados nas últimas 24 horas

**Trabalhos Semanais** - Preencher lacunas de tradução semanalmente

**Após Importação** - Acione o trabalho automaticamente após a importação em massa de produtos

**Ao Ativar Idioma** - Crie automaticamente um trabalho ao ativar um novo idioma

Trabalhos agendados mantêm as traduções atualizadas sem intervenção manual.

## Considerações de Desempenho

**Modelo de IA Local**:
- ~100-500 traduções/segundo (depende do servidor)
- Intensivo em CPU durante o processamento
- Nenhuma limitação de taxa de API
- Grátis (sem custo por tradução)

**Provedores Externos**:
- Limites de taxa variam (DeepL: 500k caracteres/mês na camada gratuita)
- Latência da API adiciona sobrecarga
- Melhor qualidade, mas custa dinheiro
- Limites de solicitações simultâneas

**Trabalhos grandes** (>10.000 campos):
- Execute durante horários de baixa demanda
- Monitore os recursos do servidor
- Considere dividir em lotes menores
- Teste com um subconjunto primeiro

## Dicas

- **Comece pequeno** - Teste trabalhos em um subconjunto (ex.: 10 produtos) antes de executar a tradução do catálogo completo
- **Use o escopo "Apenas os não traduzidos"** - Mais rápido e evita re-traduzir conteúdo já bom
- **Monitore o primeiro trabalho de perto** - Observe erros ou problemas de qualidade antes de lançar trabalhos maiores
- **Agende trabalhos durante períodos de baixa tráfego** - A tradução é intensiva em CPU/API
- **Bloqueie traduções revisadas** - Impede que trabalhos em massa sobrescrevam suas edições manuais
- **Mantenha os trabalhos focados** - Trabalhos menores e direcionados são mais fáceis de depurar do que trabalhos massivos de "traduzir tudo"
- **Revise amostras após a conclusão** - Verifique traduções aleatórias para qualidade antes de considerar o trabalho concluído
- **Exportar/backup antes de trabalhos importantes** - Caso precise reverter alterações em massa

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.