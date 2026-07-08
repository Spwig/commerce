---
title: Serviço de Tradução
---

O serviço de tradução fornece traduções automatizadas por IA para as descrições dos produtos, conteúdo de páginas, posts de blog, campos de SEO e outros conteúdos do vendedor. As traduções são executadas localmente no seu servidor ou por meio de provedores externos, então seu conteúdo permanece privado e as traduções ocorrem em segundos.

![Gerenciamento de idiomas](/static/core/admin/img/help/translation-service/language-management.webp)

## Como Funciona

1. Você **ativa idiomas** para sua loja (ex: Inglês, Alemão, Japonês)
2. Ao criar ou editar conteúdo (produtos, páginas, posts de blog), você escreve no seu idioma padrão
3. Clique em **Traduzir** em qualquer campo traduzível para gerar traduções automatizadas para seus idiomas ativos
4. As traduções são armazenadas junto com o conteúdo original e servidas automaticamente com base no idioma do visitante

## Gerenciamento de Idiomas

Navegue até **Configurações > Idiomas** para gerenciar os idiomas da sua loja.

### Painel de Idiomas

O painel mostra:
- **Total de Idiomas** — Todos os idiomas disponíveis no sistema (100+)
- **Idiomas Ativos** — Idiomas atualmente habilitados para sua loja
- **Cobertura do Modelo** — Quantos idiomas o modelo de tradução instalado suporta

### Ativar Idiomas

1. Encontre o idioma na coluna **Idiomas Disponíveis**
2. Clique no idioma para movê-lo para a coluna **Idiomas Ativos**
3. O idioma fica imediatamente disponível para traduções e aparece no seletor de idiomas da sua loja

### Idioma Padrão

Um idioma é marcado como **padrão**. Isso é:
- O idioma em que você escreve o conteúdo
- O fallback quando uma tradução não existe
- O idioma exibido quando os visitantes não selecionaram uma preferência

## Modelos de Tradução

O Spwig inclui um motor de tradução local de IA que roda totalmente no seu servidor — nenhuma dados é enviado para serviços externos.

### Modelos Disponíveis

| Modelo | Idiomas | Velocidade | Qualidade |
|--------|---------|-----------|----------|
| **M2M100-418M** | 100 | Rápido | Boa para pares de idiomas comuns |
| **M2M100-1.2B** | 100 | Moderada | Qualidade melhor, uso maior de recursos |
| **NLLB-200** | 200+ | Moderada | Melhor cobertura, incluindo idiomas raros |

### Seleção de Modelo

A página de gerenciamento de idiomas mostra qual modelo está instalado e sua cobertura de idioma. O modelo roda como um serviço local usando CTranslate2 para inferência eficiente.

## Provedores Externos

Para lojas que preferem tradução baseada em nuvem ou precisam de qualidade em idiomas específicos, o Spwig suporta provedores de tradução externos.

| Provedor | Descrição |
|----------|-------------|
| **DeepL** | Qualidade premium de tradução para idiomas europeus e asiáticos |
| **Google Translate** | Amplas cobertura de idiomas com tradução de máquina neural |
| **Azure Translator** | Serviço de tradução neural da Microsoft |
| **AWS Translate** | Tradução de máquina da Amazon com suporte a terminologia personalizada |

### Conectando um Provedor

1. Navegue até **Configurações > Provedores de Tradução**
2. Selecione o provedor e insira sua chave de API
3. Defina o provedor como o motor de tradução preferido
4. As traduções usarão o provedor externo em vez do modelo local

Você pode usar provedores externos junto com o modelo local — por exemplo, use DeepL para idiomas europeus e o modelo local para tudo o mais.

## Traduzindo Conteúdo

### Tradução em Nível de Campo

Campos traduzíveis (nomes de produtos, descrições, títulos de SEO, etc.) mostram um **botão de traduzir** ao lado do campo. Clique nele para:

1. **Traduzir para todos os idiomas ativos** — Gera traduções para todos os idiomas ativos de uma só vez
2. **Traduzir para um idioma específico** — Escolha idiomas individuais para traduzir

As traduções aparecem nas guias de idioma do editor. Você pode revisar e editar manualmente qualquer tradução gerada por máquina.

### Empresas de Tradução em Lote

Para grandes volumes de conteúdo, use **empresas de tradução em lote**:

1. Navegue até **Configurações > Empresas de Tradução**
2. Crie um novo trabalho selecionando:
   - **Tipo de conteúdo** — Produtos, páginas, posts de blog, categorias, etc.
   - **Idioma de origem** — O idioma do qual você deseja traduzir
   - **Idiomas de destino** — Um ou mais idiomas para os quais você deseja traduzir
   - **Escopo** — Todos os conteúdos, ou apenas os campos não traduzidos
3. Submeta o trabalho — ele é executado em segundo plano por meio de uma fila de tarefas
4. Monitore o progresso na lista de trabalhos (em fila → processando → concluído)

Empresas de tradução em lote são úteis quando você ativa um novo idioma e deseja traduzir todo o seu catálogo de uma só vez.

## Gerenciamento de Traduções

### Revisando Traduções

Cada campo traduzido rastreia:
- **Status da tradução** — Se o campo foi traduzido automaticamente, editado manualmente ou está faltando
- **Status de bloqueio** — Traduções bloqueadas não serão substituídas por futuras traduções automáticas
- **Última tradução** — Quando a tradução foi gerada ou editada pela última vez

### Bloqueando Traduções

Se você editar manualmente uma tradução gerada por máquina para melhorá-la, **bloqueie** o campo para evitar que ele seja substituído na próxima vez que uma tradução em lote for executada. Campos bloqueados são ignorados durante traduções automáticas.

### Cobertura de Tradução

O rastreador de cobertura mostra a porcentagem de conteúdo traduzido para cada idioma. Navegue até **Configurações > Idiomas** para ver:
- Percentuais de conclusão por idioma
- Quais tipos de conteúdo têm lacunas
- Campos que ainda precisam de tradução

## Sobrescritas de Tradução da Interface do Usuário

Além do conteúdo de produtos e páginas, você pode personalizar as traduções de **strings da interface do frontend** — botões, rótulos, mensagens e outros textos da interface exibidos aos visitantes.

Navegue até **Configurações > Sobrescritas da Interface** para:
1. Pesquisar uma string específica (ex: "Adicionar ao Carrinho")
2. Inserir sua tradução preferida para cada idioma
3. Salvar — a sobrescrita entra em vigor imediatamente

Há aproximadamente 300 strings da interface do frontend disponíveis para personalização. As sobrescritas têm prioridade sobre as traduções padrão.

## Dicas

- Comece ativando apenas os idiomas que seus clientes realmente usam — você sempre pode adicionar mais depois.
- Use o **modelo local de IA** para traduções diárias — é rápido, privado e não tem custo por tradução.
- Considere **DeepL** se você precisar da maior qualidade para idiomas europeus principais — ele produz consistentemente traduções mais naturais do que modelos genéricos.
- Sempre **revisar traduções automatizadas** para nomes de produtos, termos de marca e cópia de marketing — a IA lida bem com conteúdo técnico, mas pode perder nuances em textos criativos.
- **Bloquear** qualquer tradução que você tenha refinado manualmente para protegê-la de ser substituída durante execuções de tradução em lote.
- Use **empresas de tradução em lote** ao ativar um novo idioma para traduzir todo o seu catálogo em uma única passada em vez de traduzir produtos um por um.
- Personalize **sobrescritas da interface** para corresponder à voz da sua marca — por exemplo, altere "Adicionar ao Carrinho" para "Comprar Agora" se isso for mais adequado para sua loja.

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.