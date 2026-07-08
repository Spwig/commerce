---
title: Gerador de SEO com IA
---

O Gerador de SEO com IA escreve automaticamente títulos meta, descrições meta e outros conteúdos de SEO para seus produtos usando um provedor de IA. Em vez de escrever manualmente o conteúdo de SEO para cada produto, você pode gerar conteúdo preciso e otimizado em massa com uma única ação.

Sua loja vem com um gerador de SEO integrado que funciona imediatamente. Você também pode instalar componentes adicionais de provedores de IA no mercado de componentes Spwig para ter acesso a modelos de linguagem mais poderosos.

## Como o gerador de SEO funciona

O gerador de SEO lê o nome, a descrição, a categoria e os atributos do produto, depois usa o provedor de IA configurado para escrever conteúdo de SEO personalizado para esse produto. O conteúdo gerado é salvo diretamente nos campos de SEO do produto.

Você pode gerar conteúdo de SEO para produtos individuais a partir da página de edição do produto, ou executar geração em massa em vários produtos a partir da lista de produtos.

## Configurando um provedor de SEO

### Usando o provedor integrado

Sua loja inclui um provedor de SEO integrado que gera conteúdo de SEO de forma determinística a partir dos dados do produto — não são necessárias chaves de API externas. Ele é automaticamente definido como o provedor principal em novas instalações.

Para verificar se ele está ativo:

1. Navegue até **Marketing > Provedores de SEO**
2. Verifique se o provedor integrado aparece com um badge **PRINCIPAL** e um status **ATIVO**
3. Se nenhum provedor estiver listado, clique em **+ Adicionar Conta de Provedor de SEO** e defina **Chave do Provedor** como `deterministic`

### Conectando um componente de provedor de IA

Para conteúdo de SEO mais rico e contextual, você pode instalar um componente de provedor de IA (como um provedor baseado em OpenAI ou Claude) no mercado de componentes Spwig.

1. Instale o componente do provedor por meio do sistema de atualização de componentes (peça ao administrador da loja)
2. Navegue até **Marketing > Provedores de SEO**
3. Clique em **+ Adicionar Conta de Provedor de SEO**
4. Preencha o formulário:

**Seção de Informações do Provedor:**
- **Site** — selecione sua loja
- **Componente do Provedor** — escolha o componente de provedor de IA instalado
- **Chave do Provedor** — deixe em branco ao usar um provedor baseado em componente
- **Nome da Conta** — um nome descritivo, como `Provedor de SEO OpenAI`

**Seção de Configuração:**
- **Ativo** — marque para ativar este provedor
- **Principal** — marque para usar este como o provedor padrão para toda a geração de SEO
- **Prioridade** — números mais baixos são tentados primeiro na cadeia de fallback
- **Configurações** — configurações específicas do provedor como um objeto JSON (ex.: nome do modelo, tom, idioma)

5. Clique em **Salvar**

Apenas um provedor pode ser definido como principal. Se você marcar um novo provedor como principal, o anterior será automaticamente despromovido.

### Cadeia de fallback do provedor

Se seu provedor principal falhar (por exemplo, devido a uma interrupção de API), sua loja cairá automaticamente para o próximo provedor ativo na ordem de prioridade. Isso garante que a geração de SEO continue funcionando mesmo se um provedor estiver temporariamente indisponível.

## Gerando conteúdo de SEO para um produto

### Produto individual

1. Navegue até **Produtos > Produtos** e abra qualquer produto
2. Role até a seção **SEO** do formulário do produto
3. Clique no botão **Gerar SEO**
4. O provedor de IA gera um título meta e uma descrição meta com base nos detalhes do produto
5. Revise o conteúdo gerado e edite-o se necessário
6. Clique em **Salvar** para aplicar as alterações

### Geração em massa

Para gerar ou atualizar conteúdo de SEO para vários produtos de uma vez:

1. Navegue até **Produtos > Produtos**
2. Selecione os produtos que deseja atualizar usando os checkboxes, ou selecione todos
3. Abra o menu suspenso **Ação**
4. Escolha **Gerar Conteúdo de SEO** (ou nome de ação semelhante — verifique o menu suspenso para o rótulo exato)
5. Clique em **Ir**

O Spwig filas as tarefas de geração e as processa em segundo plano. Atualize a lista de produtos após um ou dois minutos para ver os campos de SEO atualizados.

## Revisando a cobertura de SEO

O gerador de SEO rastreia quais produtos já possuem conteúdo de SEO. Para identificar produtos que ainda precisam de SEO:

1.

Navegue até **Produtos > Produtos**
2.


Use o **Status SEO** (se disponível) para mostrar produtos com títulos meta ou descrições ausentes
3.

Selecione esses produtos e execute a ação de geração em lote

## Configurações do provedor

O campo **Configurações** em uma conta de provedor de SEO aceita um objeto JSON com configurações específicas do provedor. Opções comuns incluem:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Essas configurações variam por componente do provedor. Consulte a documentação do provedor para obter a lista completa de opções disponíveis.

## Gerenciamento de múltiplos provedores

Se você tiver mais de uma conta de provedor de SEO configurada, a lista de provedores mostra o status de cada um em uma visão geral:

- **badge PRINCIPAL** — este provedor é usado para toda a geração de SEO por padrão
- **badge ATIVO** — o provedor está habilitado
- **badge INATIVO** — o provedor está desabilitado e não será usado

Para alterar qual provedor é o principal, abra a conta do provedor que deseja promover, marque a caixa **É Principal** e salve. O sistema garante automaticamente que apenas um provedor tenha o status de principal em qualquer momento.

## Dicas

- Gere conteúdo SEO para novos produtos imediatamente após criá-los — leva apenas segundos e fornece algo útil para os motores de busca indexarem imediatamente
- Revise as descrições meta geradas por IA antes de publicar, se seus produtos tiverem nomes incomuns ou técnicos; o gerador funciona melhor com nomes de produtos claros e descritivos
- Defina "max_title_length": 60 e "max_description_length": 160 nas configurações do provedor para manter o conteúdo gerado dentro dos limites de caracteres recomendados pelo Google
- Execute a geração em lote de SEO após importar um catálogo de produtos grande para preencher rapidamente todos os campos de SEO
- Se você atualizar significativamente a descrição de um produto, gere novamente seu conteúdo SEO para manter as tags meta alinhadas com o novo texto
- O provedor determinístico embutido é um bom ponto de partida; atualize para um componente com IA quando seu catálogo estiver configurado e você quiser cópias de SEO mais ricas e com um tom mais natural