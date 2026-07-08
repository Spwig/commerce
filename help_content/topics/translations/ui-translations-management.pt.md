---
title: Gerenciamento de Traduções da Interface do Usuário
---

A página de Traduções da Interface do Usuário permite que você personalize como as strings da interface do frontend—botões, rótulos, mensagens de erro e outros textos da interface—parecem em cada idioma. Ao contrário das traduções de conteúdo de produtos ou páginas, estas são os elementos fixos da interface que os clientes veem em toda a sua loja. Personalize-as para corresponder à voz da sua marca ou melhorar a clareza para seu público específico.

Essa página mostra todas as strings da interface que podem ser traduzidas e permite que você substitua as traduções padrão fornecidas pelo Spwig.

## Entendendo Traduções da Interface do Usuário

As traduções da interface são as strings de texto que compõem a interface da sua loja:

**Exemplos de Strings da Interface do Usuário**:
- Botões: "Adicionar ao Carrinho", "Finalizar Compra", "Buscar"
- Rótulos: "Preço", "Quantidade", "Endereço de Entrega"
- Mensagens: "Item adicionado ao carrinho", "Pedido confirmado", "Endereço de e-mail inválido"
- Navegação: "Início", "Loja", "Entre em Contato"
- Campos de formulário: "E-mail", "Senha", "Nome"

O Spwig inclui traduções padrão para aproximadamente 300 strings da interface em todos os idiomas suportados. A página de Traduções da Interface do Usuário permite que você substitua qualquer uma dessas traduções padrão por suas próprias traduções personalizadas.

## Por Que Personalizar Traduções da Interface do Usuário?

**Voz da Marca**: Altere "Adicionar ao Carrinho" para "Comprar Agora" ou "Obtenha o Seu" para corresponder à personalidade da sua marca

**Variações Regionais**: Ajuste as traduções para mercados específicos (inglês britânico vs. americano, espanhol europeu vs. latino-americano)

**Clareza**: Se a tradução padrão não fizer sentido para seus produtos ou público, substitua-a por um texto mais claro

**Termos Específicos do Setor**: Use a terminologia que seus clientes esperam (por exemplo, "Marque um Agendamento" em vez de "Adicionar ao Carrinho" para lojas baseadas em serviços)

## Buscando por Strings

Use a caixa de pesquisa para encontrar strings específicas da interface do usuário:

**Buscar por texto em inglês**: Digite "add to cart" para encontrar as traduções desse botão

**Buscar por tradução**: Digite texto em qualquer idioma para encontrar traduções correspondentes

**Buscar por chave**: Se você souber a chave de tradução (por exemplo, `cart.add_item`), procure-a diretamente

A página é atualizada instantaneamente enquanto você digita, mostrando apenas as strings correspondentes.

## Visualizando Detalhes das Traduções

Cada string da interface mostra:

**Texto em Inglês de Origem** - A versão padrão em inglês (seu ponto de referência)

**Chave de Tradução** - O identificador interno usado no código (por exemplo, `cart.add_to_cart`)

**Colunas de Idioma** - A tradução atual para cada idioma ativo

**Status de Substituição** - Se você personalizou a tradução (destacada se substituída)

## Criando Substituições de Traduções

Para personalizar a tradução de uma string da interface:

1. **Encontre a string** usando a busca (por exemplo, procure "add to cart")
2. **Clique na célula do idioma** que deseja personalizar
3. **Digite sua tradução personalizada** no editor pop-up
4. **Salvar** - Sua substituição entra em vigor imediatamente

A tradução padrão original é preservada - você está criando uma substituição que tem prioridade.

## Revertendo para as Traduções Padrão

Para remover uma substituição personalizada e restaurar a tradução padrão:

1. **Clique na tradução substituída** (essas são destacadas)
2. **Clique em "Revert to Default"** no editor
3. **Confirmar** - A tradução padrão é restaurada imediatamente

Você pode reverter substituições de idioma individuais sem afetar suas substituições em outros idiomas.

## Filtrando por Status de Substituição

Use o menu suspenso de filtro para visualizar:

**Todas as Strings** - Cada string da interface no sistema (~300 no total)

**Apenas Substituídas** - Strings nas quais você criou traduções personalizadas

**Apenas Padrões** - Strings que ainda usam as traduções padrão do Spwig

Isso ajuda você a revisar quais strings você personalizou e identificar lacunas.

## Exemplos Comuns de Personalização

| Tradução Padrão em Inglês | Substituição Personalizada | Caso de Uso |
|--------------------------|--------------------------|------------|
| Adicionar ao Carrinho | Comprar Agora | Chamada para ação mais direta |
| Finalizar Compra | Finalizar Compra Segura | Enfatizar segurança |
| Buscar | Encontrar Produtos | Mais específico para comércio eletrônico |
| Entre em Contato | Fale Conosco | Tom mais amigável |
| Inscrever-se | Participe de Nosso Boletim | Proposta de valor mais clara |

## Validação de Traduções

Ao inserir traduções personalizadas, valide que:

**O comprimento se encaixe no espaço da interface** - As traduções podem ser mais longas ou curtas que o inglês (palavras alemãs, por exemplo, são frequentemente mais longas)

**Mantenha o significado** - Não altere a funcionalidade na tradução (um botão "Cancelar" não deveria dizer "Excluir")

**Terminologia consistente** - Use a mesma tradução para termos repetidos em toda a interface

**Formalidade apropriada** - Corresponda ao tom do seu mercado-alvo (formal vs. informal)

## Consistência em Múltiplos Idiomas

Ao personalizar uma string para múltiplos idiomas:

1. **Comece com seu idioma padrão** - Defina a base

2. **Personalize outros idiomas** para corresponder à mesma intenção

3. **Teste em cada idioma** para verificar o layout e o significado

4. **Use falantes nativos** quando possível para revisar personalizações em idiomas não-ingleses

Personalizações inconsistentes em diferentes idiomas criam uma experiência confusa para os clientes.

## Exportação/Importação em Lote

Para personalizações extensas, considere usar o fluxo de trabalho de exportação/importação:

1. **Exportar** as traduções atuais como JSON ou CSV

2. **Editar em planilha** ou editor de texto (mais fácil para alterações em lote)

3. **Importar** as traduções atualizadas de volta ao sistema

Esse fluxo de trabalho está disponível através da página de Trabalhos de Tradução para gerenciar projetos de tradução em larga escala.

## Dicas

- **Procure antes de personalizar** - Certifique-se de que está editando a string correta; algumas strings semelhantes servem para propósitos diferentes
- **Teste na interface do frontend após salvar** - Verifique se sua tradução personalizada aparece corretamente na interface real
- **Mantenha as traduções concisas** - Mais curto é geralmente melhor para botões e rótulos
- **Documente suas substituições** - Mantenha anotações sobre por que personalizou strings específicas para referência futura
- **Use terminologia consistente** - Se você personalizar "Carrinho" para "Cesta", faça isso consistentemente em todas as strings relacionadas
- **Considere layouts móveis** - Traduções longas podem se quebrar ou truncar em telas pequenas
- **Revise após atualizações de idioma** - Quando o Spwig adicionar novas traduções padrão, revise e personalize-as para manter a consistência

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.