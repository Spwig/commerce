---
title: Peso de Relevância e Indexação Profunda
---

Peso de relevância e indexação profunda controlam como os resultados de busca são classificados e quais dados do produto são pesquisados. Os pesos são multiplicadores de importância - um peso de 2,0 significa que os correspondências nesse campo são duas vezes mais importantes que um peso de 1,0. A indexação profunda determina se a busca vai além dos nomes básicos dos produtos para incluir SKUs, atributos, avaliações e até o conteúdo de documentos. Este guia explica ambos os sistemas, quando ajustá-los e as implicações críticas de desempenho.

Os valores padrão funcionam bem para a maioria das lojas de comércio eletrônico. Ajuste somente se tiver necessidades específicas de classificação ou indexação.

![Peso de Relevância](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Entendendo Peso de Relevância

Os pesos são multiplicadores (escala de 0,0-2,0) aplicados quando há correspondências de texto encontradas em diferentes campos. Pesos mais altos significam que as correspondências nesse campo classificam mais alto nos resultados.

**Exemplo**: Se um produto tiver "laptop" no nome (peso 1,50) e na descrição (peso 0,80):
- Correspondência no nome contribui 1,50 para a pontuação de relevância
- Correspondência na descrição contribui 0,80
- A pontuação combinada determina a classificação em relação a outros produtos

Os pesos permitem que você priorize certos campos em relação a outros ao classificar os resultados da busca.

## Categorias de Peso e Valores Padrão

Navegue até **Configurações de Busca > Aba Peso** para visualizar todas as configurações de peso:

| Campo | Peso Padrão | Raciocínio |
|-------|---------------|-----------|
| **weight_name** | 1,50 | Nomes de produtos são os mais importantes - os clientes esperam correspondências exatas de nomes no topo |
| **weight_sku** | 1,20 | SKUs são identificadores específicos - importantes para comércio B2B e clientes recorrentes |
| **weight_description** | 0,80 | Descrições fornecem contexto, mas são menos importantes que correspondências exatas de nomes |
| **weight_categories** | 0,80 | Correspondências de categorias são úteis para navegação, mas não tão específicas quanto nome/SKU |
| **weight_attributes** | 0,70 | Buscas por cor, tamanho, material - úteis, mas informações de suporte |
| **weight_brands** | 0,70 | Filtro por marca é importante, mas não é o critério principal de busca para a maioria das lojas |
| **weight_blog_posts** | 0,60 | Conteúdo de blog menos importante em busca focada em comércio eletrônico (prioridade mais baixa) |
| **weight_reviews** | 0,50 | Conteúdo gerado pelo usuário menos controlado - menor peso |

Esses valores padrão assumem uma loja de comércio eletrônico típica onde a descoberta de produtos é o principal objetivo da busca.

## Quando Ajustar Peso

Ajuste os pesos quando as prioridades da sua loja forem diferentes dos padrões comuns de comércio eletrônico:

**Lojas com Foco em SKU (B2B, Atacado)** - Aumente o `weight_sku` para 1,8-2,0 para que as buscas por código de produto dominem os resultados. Os clientes B2B geralmente buscam por códigos de produto exatos.

**Lojas com Foco em Marca** - Aumente o `weight_brands` para 1,2-1,5 quando os clientes compram principalmente por marca (roupas de designer, produtos de luxo).

**Lojas com Conteúdo** - Aumente o `weight_blog_posts` para 0,9-1,2 se você for um editor de conteúdo ou vendedor educacional onde os posts de blog são tão importantes quanto os produtos.

**Lojas com Foco em Atributos (Moda)** - Aumente o `weight_attributes` para 1,0-1,2 quando os clientes buscam frequentemente por atributos de cor, tamanho, estilo.

## Exemplos de Ajuste de Peso

| Tipo de Loja | Ajustes Recomendados |
|-----------|------------------------|
| **Varejo B2B** | weight_sku: 2,0, weight_name: 1,3, weight_description: 0,6 - Priorizar códigos de produto |
| **Loja de Moda** | weight_attributes: 1,2, weight_brands: 1,2, weight_name: 1,4 - Cor/estilo/marca importante |
| **Editor de Conteúdo** | weight_blog_posts: 1,2, weight_name: 1,3, weight_reviews: 0,7 - Conteúdo tão importante quanto produtos |
| **Comércio Eletrônico Geral** | Use os padrões - Equilibrado para lojas online típicas |

Ajuste um peso de cada vez e teste antes de fazer alterações adicionais.

## Visão Geral da Indexação Profunda

⚠️ **AVISO DE DESEMPENHO** - Cada opção de indexação profunda adiciona complexidade e sobrecarga às consultas.

A indexação profunda estende a busca além do nome/descrição básico do produto para outros dados:

![Aba de Indexação Profunda](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Navegue até **Configurações de Busca > Aba de Indexação Profunda** para configurar.

## Indexar SKUs

**Padrão**: LIGADO, **Impacto no Desempenho**: Baixo

Inclui SKUs de produtos e variantes no índice de busca. Aciona JOIN de variantes (custo mínimo).

**Quando manter LIGADO**: Essencial para lojas B2B onde os clientes conhecem os códigos de produto. Também útil para clientes recorrentes que lembram o SKU de pedidos anteriores.

**Quando desativar**: Nunca, a menos que você não tenha SKUs atribuídos. O impacto no desempenho é insignificante.

## Indexar Atributos

**Padrão**: LIGADO, **Impacto no Desempenho**: Médio

Inclui atributos do produto (cor, tamanho, material, atributos personalizados) no índice de busca. Realiza JOIN com a tabela de atributos.

**Quando manter LIGADO**: Importante para lojas de moda, produtos configuráveis ou qualquer loja onde os clientes buscam por características do produto ("vestido vermelho", "camisa grande").

**Quando desativar**: Catálogos com mais de 20.000 produtos com muitos atributos por produto podem ter uma sobrecarga de 50-100ms. Apenas desative se o desempenho for crítico e os clientes não buscarem por atributos.

## Indexar Campos Personalizados

**Padrão**: LIGADO, **Impacto no Desempenho**: Médio

Inclui campos personalizados definidos pelo vendedor do JSONField no índice de busca. Requer percorrimento do JSONField.

**Quando manter LIGADO**: Se você usar campos personalizados para dados do produto pesquisáveis (informações de garantia, especificações, detalhes de compatibilidade).

**Quando desativar**: Se você não usar campos personalizados, ou campos personalizados contiverem dados não pesquisáveis (notas internas, códigos contábeis). Desativar economiza a sobrecarga de processamento do JSONField.

## Indexar Avaliações

**Padrão**: LIGADO, **Impacto no Desempenho**: Médio-Alto

Inclui títulos e comentários de avaliações aprovadas na busca. Realiza JOIN com a tabela de avaliações e adiciona sobrecarga de busca de texto.

**Quando manter LIGADO**: Catálogos com muitas avaliações onde os clientes buscam produtos com base no conteúdo das avaliações ("mochila impermeável para laptop" pode aparecer no texto da avaliação).

**Quando desativar**: Catálogos com mais de 20.000 produtos ou lojas com muitas avaliações por produto. Adiciona 100-200ms de sobrecarga em catálogos grandes.

## Indexar Documentos

**Padrão**: DESLIGADO, **Impacto no Desempenho**: MUITO ALTO 🚨

**NUNCA ATIVE DE FORMA CASUAL** - Funcionalidade de busca mais cara.

O indexação de documentos extrai texto de arquivos PDF, DOCX e XLSX anexados a produtos digitais, tornando o conteúdo dos arquivos pesquisável.

**Detalhes Técnicos**:
- Usa bibliotecas PyPDF2, python-docx e openpyxl
- I/O de arquivo síncrono e extração de texto na busca
- Rastreia arquivos via checksum MD5 (reindexa apenas quando o arquivo mudar)
- Potenciais tempos limite em arquivos grandes (>10MB PDFs)

**Impacto no Desempenho**:
- Muito caro para indexação inicial (minutos a horas para bibliotecas grandes)
- Sobrecarga significativa nas consultas (latência adicional de 100-500ms)
- Intensivo em memória para documentos grandes

**Apenas ative se**:
- Você vende produtos digitais com documentos pesquisáveis (e-books, relatórios, manuais)
- Catálogo é pequeno (<500 produtos digitais)
- Servidor tem recursos adequados
- Você testou o impacto de forma completa

**Para lojas de produtos digitais**: Considere se os clientes realmente precisam pesquisar o conteúdo dos documentos, ou se pesquisar o nome/descrição do produto é suficiente.

## Tabela de Impacto no Desempenho

| Funcionalidade | Padrão | Impacto | Use Quando |
|---------|---------|--------|----------|
| Indexar SKUs | LIGADO | Baixo | Sempre (essencial para B2B) |
| Indexar Atributos | LIGADO | Médio | Produtos configuráveis |
| Indexar Campos Personalizados | LIGADO | Médio | Usando campos personalizados |
| Indexar Avaliações | LIGADO | Médio-Alto | Loja com muitas avaliações |
| Indexar Documentos | DESLIGADO | Muito Alto | Apenas produtos digitais (testar primeiro) |

O impacto assume catálogos típicos. Catálogos grandes (>50.000 produtos) experimentam sobrecarga proporcionalmente maior.

## Testando Alterações de Peso

Ao ajustar pesos, siga este fluxo de trabalho de testes:

1. **Mude um peso de cada vez** - Não ajuste múltiplos pesos simultaneamente; você não saberá qual mudança causou os resultados
2. **Ajustes pequenos** - Ajuste em ±0,2 por vez (ex: 1,0 → 1,2, não 1,0 → 1,8)
3. **Teste com consultas reais** - Use termos de busca reais dos clientes do analytics, não testes aleatórios
4. **Monitore analytics** - Compare a relevância dos resultados antes e depois usando as consultas principais
5. **Espere 1-2 semanas** - Dê aos clientes tempo para interagir com as novas classificações
6. **Meça as taxas de cliques** - Os clientes estão clicando mais/menos nos resultados do que antes?

## Compromisso entre Desempenho e Precisão

Mais indexação = melhores resultados de busca, mas desempenho mais lento:

**Cenário: Catálogo Pequeno (<1.000 produtos)**
- Ative todas as opções de indexação (SKUs, atributos, campos personalizados, avaliações)
- Impacto no desempenho mínimo
- Capacidades de busca abrangentes

**Cenário: Catálogo Médio (1.000-10.000 produtos)**
- Mantenha SKUs, atributos, campos personalizados LIGADOS
- Considere desativar avaliações se a média for >10 avaliações por produto
- Monitore os tempos de resposta

**Cenário: Catálogo Grande (>10.000 produtos)**
- Mantenha SKUs LIGADOS (impacto baixo)
- Desative indexação de avaliações (alto impacto)
- Desative campos personalizados se não forem usados
- NUNCA ative indexação de documentos
- Considere Elasticsearch em >50.000 produtos

Equilibre com base no tamanho do seu catálogo e nos recursos do servidor.

## Sobrescritas de Peso Específicas do Motor

Ao criar um motor de busca via assistente (Etapa 3), você pode sobrescrever os pesos globais para esse motor específico.

**Caso de Uso**: Motor com foco em blog
- Crie o motor "blog"
- Sobrescreva `weight_blog_posts` para 1,5 (vs global 0,60)
- Conteúdo do blog agora classifica mais alto em buscas do motor de blog

A maioria dos motores NÃO deve sobrescrever pesos - deixe em branco para herdar as configurações globais.

## Dicas

- **NUNCA ative indexação de documentos a menos que seja absolutamente crítico** - Maior custo de desempenho de qualquer funcionalidade de busca
- **Lojas B2B: Aumente weight_sku para 2,0** - Códigos de produto são o método principal de busca
- **Teste alterações de peso em horários de baixa audiência** - Observe o impacto no desempenho antes dos horários de pico
- **Monitore os tempos de resposta após ativar a indexação** - Verifique o painel de analytics para lentidões
- **Desative indexação de avaliações em catálogos >20K produtos** - Impacto de desempenho significativo
- **Ajuste um peso de cada vez para testes** - Não é possível determinar causa/efeito com alterações simultâneas
- **Extração de documentos requer PyPDF2/docx/openpyxl** - Verifique se essas bibliotecas estão instaladas antes de ativar a indexação de documentos

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.