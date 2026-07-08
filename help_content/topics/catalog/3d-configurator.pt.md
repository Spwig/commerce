---
title: Configurador de Produtos 3D
---

O Configurador 3D permite que seus clientes visualizem produtos configuráveis em um visualizador 3D interativo diretamente na página do produto. À medida que os clientes selecionam opções — como cores, materiais ou variações de componentes — o modelo 3D é atualizado em tempo real para refletir suas escolhas. Em dispositivos móveis compatíveis, os clientes também podem visualizar o produto em realidade aumentada (AR), colocando-o virtualmente no seu próprio espaço antes de comprar.

O Configurador 3D funciona com produtos configuráveis. Cada produto configurável pode ter uma configuração de cena 3D que vincula um arquivo de modelo GLB ao conjunto de opções de configuração do produto.

## Antes de começar

Para configurar uma cena 3D, você precisa de:

- Um **produto configurável** já criado em seu catálogo
- Um **modelo 3D base** carregado em sua Biblioteca de Mídia como um arquivo GLB — este é o modelo montado que aparece por padrão
- Opcionalmente, outros arquivos GLB para trocas de geometria (por exemplo, formas diferentes de colarinho), e imagens de textura para variações de material

Se você ainda não criou o produto configurável e suas opções de configuração, faça isso primeiro antes de configurar a cena 3D.

## Criando uma configuração de cena

1. Navegue até **Catálogo > Configurações de Cena 3D**
2. Clique em **+ Adicionar Configuração de Cena 3D**
3. Selecione o **Produto** a que esta cena pertence — apenas produtos configuráveis estão disponíveis
4. Escolha o **Modelo 3D Base** da sua Biblioteca de Mídia — este é o arquivo GLB que carrega por padrão
5. Configure as configurações do visualizador (veja abaixo)
6. Salve o registro

Após salvar, o campo **Árvore de Nós** é preenchido automaticamente. Isso é o gráfico de cena analisado extraído do seu arquivo GLB — ele lista cada nó nomeado dentro do modelo, que você referenciará ao adicionar mapeamentos de nós.

## Configurações do visualizador

Essas configurações controlam como o visualizador 3D aparece na página do produto.

### Câmera e iluminação

| Campo | Descrição | Padrão |
|-------|-------------|---------|
| **Orbita da Câmera** | Posição inicial da câmera no formato `ângulo elevação distância` (ex: `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Alvo da Câmera** | O ponto em que a câmera olha, em metros a partir do centro do modelo (ex: `0m 0m 0m`) | `0m 0m 0m` |
| **Imagem do Ambiente** | Uma imagem HDR da sua Biblioteca de Mídia usada para iluminação baseada em imagem — fornece reflexos e sombras mais realistas | Nenhum |
| **Exposição** | Brilho geral da cena — valores mais baixos são mais escuros, valores mais altos são mais brilhantes | `1.0` |

### Sombras

| Campo | Descrição | Padrão |
|-------|-------------|---------|
| **Intensidade da Sombra** | Quão forte a sombra projetada sob o modelo aparece — `0` é nenhuma sombra, `1` é intensidade total | `0.5` |
| **Suavidade da Sombra** | Quão desfocada a borda da sombra é — `0` é nítida, `1` é muito suave | `0.5` |

### Correção de cor

| Campo | Descrição |
|-------|-------------|
| **Mapeamento de Tom** | O algoritmo de correção de cor aplicado à cena. **Comércio** produz cores vibrantes e amigáveis para produtos. **Neutro** é preciso em cores. **ACES** oferece um aspecto cinematográfico de filme. |
| **Força do Efeito de Brilho** | Adiciona um efeito de brilho a partes emissivas (autoiluminadas) do modelo. `0` desativa o brilho. Valores entre `1` e `5` produzem efeitos de brilho sutis a dramáticos. |

### Comportamento e fundo

| Campo | Descrição | Padrão |
|-------|-------------|---------|
| **Rotação Automática** | Se o modelo gira lentamente ao carregar para atrair a atenção do cliente | Ligar |
| **AR Ativado** | Se os clientes em dispositivos compatíveis veem um botão **Ver em AR** | Ligar |
| **Fundo** | A cor de fundo ou gradiente CSS do visualizador — insira uma cor hexadecimal (ex: `#f5f5f5`) ou um valor de gradiente CSS | `#ffffff` |

### Miniatura

O campo **Miniatura** contém uma captura de tela de pré-visualização do visualizador 3D, mostrada antes que o visualizador carregue. Você pode capturar uma captura de tela da página do produto ativa e carregá-la em sua Biblioteca de Mídia, depois vinculá-la aqui para uma experiência de carregamento de página mais suave.

## Habilitando e desabilitando o visualizador 3D

O interruptor **Habilitado** controla se o visualizador 3D é exibido na página do produto.

Quando desativado, o produto volta para o configurador de imagem 2D padrão.

Isso permite que você prepare uma configuração de cena antes de torná-la visível para os clientes.

## Conectando opções de configuração a ações 3D

Depois que a cena base estiver configurada, você pode vincular cada opção de slot de configuração a uma mudança visual no modelo 3D. Esses links são chamados **Node Mappings** e são adicionados na seção **Node Mappings** no final do formulário de configuração da cena.

### Campos de mapeamento de nó

| Campo | Descrição |
|-------|-------------|
| **Opção de Slot** | A opção de configuração que aciona essa mudança (ex.: "Couro Vermelho") |
| **Tipo de Ação** | O que acontece visualmente (veja os tipos de ação abaixo) |
| **Nó Alvo** | O nome do nó da árvore de cena que muda — escolha entre os nomes listados em sua **Árvore de Nós** |
| **Dados da Ação** | Dados específicos da ação, como um código de cor hexadecimal, URL de textura ou URL de arquivo GLB |
| **Ordem de Classificação** | Controla a ordem na qual várias mapeamentos para a mesma opção são aplicados |

### Tipos de ação

| Ação | O que ela faz |
|--------|-------------|
| **Cor do Material** | Muda a cor de um material no nó alvo — forneça uma cor hexadecimal em **Dados da Ação** |
| **Textura do Material** | Troca a textura aplicada a um material — vincule a uma imagem de textura em **Dados da Ação** |
| **Troca de Geometria** | Substitui uma parte do modelo por um arquivo GLB diferente — útil para mudanças estruturais, como uma forma diferente de alça |
| **Visibilidade** | Mostra ou oculta um nó na cena — defina `visible: true` ou `visible: false` em **Dados da Ação** |

Vários mapeamentos podem ser adicionados para uma única opção de slot. Por exemplo, selecionar "Azul Jeans" pode mudar a cor do material *e* ocultar um nó de acabamento de couro ao mesmo tempo.

## Ativos de geometria

Se sua configuração incluir ações de **Troca de Geometria**, você precisa registrar os arquivos GLB de substituição como Ativos de Geometria. Eles são adicionados na seção **Ativos de Geometria** do formulário de configuração da cena.

| Campo | Descrição |
|-------|-------------|
| **Rótulo** | Nome descritivo para este ativo de geometria, por exemplo, "Colar de Gola V" |
| **Arquivo GLB** | O arquivo GLB de substituição do seu Banco de Mídia |
| **Nó Alvo** | Qual nó no modelo base esta geometria substitui |

Após salvar um Ativo de Geometria, os nomes dos nós são analisados do GLB e armazenados em **Dados do Nó**, tornando-os disponíveis como nós alvo em seus mapeamentos.

## Ativos de textura

Imagens de textura usadas em mapeamentos de **Textura do Material** podem ser registradas como Ativos de Textura para referência mais fácil. Eles são adicionados na seção **Ativos de Textura**.

| Campo | Descrição |
|-------|-------------|
| **Rótulo** | Nome descritivo, por exemplo, "Couro Vermelho" |
| **Imagem de Textura** | A imagem de textura do seu Banco de Mídia |
| **Tipo de Textura** | O canal PBR ao qual esta textura se aplica — Cor Base, Mapa Normal, Mapa de Rugosidade, Mapa de Metalicidade, Occlusão Ambiental ou Mapa Emissivo |

## Exemplo: jaqueta configurável com opções de cor

**Cenário:** Uma jaqueta que pode ser encomendada em Preto, Azul Marinho ou Burgo, com cada cor aplicada à malha do corpo da jaqueta.

**Configuração:**

1. Crie uma configuração de cena para o produto da jaqueta com o arquivo GLB da jaqueta montada como modelo base
2. Defina **Tone Mapping** como Comércio e **Auto Rotate** como ativo
3. Na seção Node Mappings, adicione três entradas — uma por opção de cor:

| Opção de Slot | Tipo de Ação | Nó Alvo | Dados da Ação |
|-------------|-------------|-------------|-------------|
| Preto | Cor do Material | JacketBody | `{"color": "#1a1a1a"}` |
| Azul Marinho | Cor do Material | JacketBody | `{"color": "#1b2a4a"}` |
| Burgo | Cor do Material | JacketBody | `{"color": "#6b2737"}` |

Quando um cliente selecionar Azul Marinho na página do produto, o visualizador atualiza instantaneamente a cor do material JacketBody para azul marinho.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- Nomeie seus nós GLB de forma clara ao criar seu modelo 3D — nomes de nós como "JacketBody" ou "CollarMesh" são muito mais fáceis de trabalhar do que nomes gerados automaticamente, como "Mesh_023"
- Use o mapeamento de tom **Commerce** para a maioria dos produtos — ele está ajustado para uma apresentação de produto vibrante e atraente
- Desative o **Auto Rotate** para produtos em que o ângulo de câmera padrão já mostra as características mais importantes, para evitar desorientar o cliente ao carregar
- Teste o botão AR em um dispositivo móvel real antes de promovê-lo — a disponibilidade de AR depende do dispositivo e do navegador do cliente (iOS Safari e Android Chrome com suporte a WebXR são os mais confiáveis)
- Faça o upload de uma imagem **Thumbnail** para cada configuração de cena — isso evita que uma caixa branca em branco flique enquanto o visualizador 3D carrega
- Se o visualizador 3D ainda não estiver pronto, desative-o com o interruptor **Enabled** para que os clientes vejam o configurador de imagem padrão em vez disso