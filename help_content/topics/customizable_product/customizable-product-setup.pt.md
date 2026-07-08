---
title: Configurando um Produto Personalizável
---

Este guia o orienta pelo processo completo de configuração de um produto personalizável, desde a criação do produto até a configuração de superfícies, preços e restrições de upload. Dois exemplos práticos são usados ao longo do texto: uma **camisa personalizada** (roupa com múltiplas superfícies) e um **pôster personalizado** (impressão em uma única superfície).

## Etapa 1: Criar o produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina **Tipo de Produto** como **Produto Personalizável**
3. Preencha o nome do produto, descrição, imagens e preços como faria para qualquer produto
4. Salve o produto

Após salvar, um novo botão **Abrir Editor de Design** aparece no formulário do produto. Isso o leva para a página dedicada de configuração, onde você configura o editor de design visual.

## Etapa 2: Acessar a configuração do editor de design

1. Abra o produto que acabou de criar no painel de administração
2. Clique no botão **Abrir Editor de Design** (na seção Produto Personalizável)
3. A página de configuração abre com três abas: **Superfícies**, **Configurações** e **Preços**

A página de configuração é onde você define tudo sobre o editor de design para este produto.

## Etapa 3: Adicionar superfícies de design

Uma superfície representa uma face personalizável do seu produto. Clique em **+ Adicionar Superfície** para criar cada superfície.

### Exemplo de camisa: 3 superfícies

| Superfície | Nome | Dimensões | Zona de design | Notas |
|-----------|------|-----------|----------------|-------|
| 1 | Frente | 300 x 400 mm | Área central do peito | Área principal de design |
| 2 | Costas | 300 x 400 mm | Área superior das costas | Área secundária de design |
| 3 | Manga esquerda | 100 x 100 mm | Área superior do braço | Apenas área para logotipo pequeno |

### Exemplo de pôster: 1 superfície

| Superfície | Nome | Dimensões | Zona de design | Notas |
|-----------|------|-----------|----------------|-------|
| 1 | Frente | 210 x 297 mm (A4) | Área totalmente impressível | Uma única superfície, alta DPI |

### Configurando cada superfície

Para cada superfície, você configura o seguinte:

**Informações básicas:**
- **Nome** — O que os clientes veem nas abas de superfície (ex: "Frente", "Costas")
- **Slug** — Identificador seguro para URL, gerado automaticamente a partir do nome
- **Ordem de classificação** — Controla a ordem em que as superfícies aparecem (números mais baixos primeiro)

**Imagem de mockup:**
- Clique na área da imagem de mockup para abrir a Biblioteca de Mídia e selecionar uma foto do produto mostrando esta superfície
- Use uma foto de alta qualidade do seu produto do ângulo correto

**Posicionamento da zona de design:**
- Após selecionar uma imagem de mockup, uma sobreposição retangular aparece na pré-visualização
- **Arraste** a sobreposição para posicionar onde a zona de design deve estar na imagem de mockup
- **Redimensione** a sobreposição arrastando suas bordas para definir os limites da área de design
- A zona é armazenada como coordenadas baseadas em porcentagem, então ela se ajusta a qualquer tamanho de tela

A zona de design informa ao editor exatamente onde na imagem do produto o design do cliente aparecerá. Posicione-a com cuidado para corresponder à área realmente impressível do seu produto.

**Dimensões físicas:**
- **Largura** e **Altura** — As dimensões reais da área de design
- **Unidade** — Milímetros, polegadas ou pixels
- Essas dimensões determinam a proporção do canvas de design e são usadas para calcular a DPI de impressão

**Configurações de impressão:**
- **DPI mínimo** — A menor DPI aceitável. Os clientes veem um aviso se suas imagens carregadas estiverem abaixo desse valor. Padrão: 150
- **DPI recomendado** — A resolução ideal para a melhor qualidade de impressão. Padrão: 300
- **Bleed (mm)** — Margem extra fora da área de design para impressão de bleed. Defina como 0 se não for necessário (comum para roupas), ou 3 mm para produtos de impressão profissional
- **Máximo de cores** — Para impressão em tela, você pode limitar o número de cores. Deixe em branco para ilimitado (impressão digital)
- **Cor de fundo** — Cor padrão do fundo do canvas

### Configurações de impressão para camisa vs pôster

| Configuração | Camisa | Pôster |
|--------------|--------|--------|
| DPI mínimo | 150 | 200 |
| DPI recomendado | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Máximo de cores | 6 (impressão em tela) | Em branco (ilimitado) |
| Cor de fundo | Correspondente à cor da roupa | `#ffffff` (branco) |

## Passo 4: Restrições por superfície

Cada superfície pode substituir as configurações globais de recurso. Isso permite que você permita ferramentas diferentes em superfícies diferentes.

As opções de restrição são:

| Configuração | Opções | Descrição |
|---------|---------|-------------|
| **Permitir Texto** | Herdar / Sim / Não | Se os clientes podem adicionar texto nesta superfície |
| **Permitir Upload de Imagem** | Herdar / Sim / Não | Se os clientes podem carregar imagens nesta superfície |
| **Permitir Clipart** | Herdar / Sim / Não | Se os clientes podem usar clipart nesta superfície |
| **Máximo de Elementos** | Número ou em branco | Número máximo de elementos de design permitidos nesta superfície |

Quando definido como **Herdar**, a superfície usa o que estiver configurado nas configurações globais (Passo 6). Quando definido como **Sim** ou **Não**, ele substitui a configuração global para essa superfície específica.

### Exemplo: Restrição de manga de camiseta

Para a superfície da manga da camiseta, você pode querer restringir a personalização a apenas um logotipo pequeno:

| Configuração | Valor | Motivo |
|---------|-------|--------|
| Permitir Texto | Não | Muito pequeno para texto legível |
| Permitir Upload de Imagem | Sim | Permitir o upload de um logotipo pequeno |
| Permitir Clipart | Não | Manter simples |
| Máximo de Elementos | 1 | Apenas um logotipo |

As superfícies da frente e da parte de trás permaneceriam definidas como **Herdar**, permitindo todas as ferramentas conforme definido nas configurações globais.

### Exemplo: Restrição de pôster

Para um pôster, todas as superfícies normalmente herdam da configuração global, já que há apenas uma superfície e todas as ferramentas devem estar disponíveis. Não são necessárias substituições por superfície.

## Passo 5: Configurar restrições de upload

Na guia **Configurações**, configure como os clientes podem carregar arquivos:

| Configuração | Descrição | Exemplo de camiseta | Exemplo de pôster |
|---------|-------------|-----------------|----------------|
| **Tamanho Máximo de Upload** | Tamanho máximo de arquivo por upload | 10 MB | 20 MB |
| **Máximo de Uploads por Superfície** | Quantidade de imagens por superfície | 5 | 3 |
| **Tipos de Upload Permitidos** | Formatos de arquivo aceitos | JPG, PNG, WebP | JPG, PNG, WebP |

Limites maiores de tamanho de arquivo são recomendados para produtos de impressão onde os clientes precisam carregar imagens de alta resolução.

## Passo 6: Configurações do editor

Na guia **Configurações**, configure o comportamento global do editor:

**Modo do Editor:**
- **Editor de Cânon** — Editor visual completo com pré-visualização em tempo real do cânon. Recomendado para a maioria dos produtos.
- **Formulário Simples** — Campos de formulário tradicionais para personalização básica (ex.: texto gravado apenas).

**Opções de recurso (padrões globais):**
- **Permitir Texto** — Permitir que os clientes adicionem elementos de texto
- **Permitir Upload de Imagem** — Permitir que os clientes carreguem suas próprias imagens
- **Permitir Clipart** — Permitir que os clientes naveguem e usem sua biblioteca de clipart

Essas configurações globais se aplicam a todas as superfícies, a menos que sejam substituídas por restrições por superfície (Passo 4).

## Passo 7: Configurar preços

Na guia **Preços**, defina as taxas de design que são adicionadas ao preço base do produto:

| Taxa | Descrição |
|-----|-------------|
| **Taxa de Design Base** | Taxa fixa adicionada quando qualquer personalização é aplicada |
| **Taxa por Superfície** | Taxa adicional para cada superfície usada além da primeira |
| **Taxa por Upload** | Taxa para cada imagem carregada pelo cliente |
| **Taxa por Texto** | Taxa para cada elemento de texto adicionado |

### Exemplo: Preços de camiseta

| Taxa | Valor | Racional |
|-----|--------|-----------|
| Taxa de Design Base | $5,00 | Cobrir o custo de setup para qualquer pedido personalizado |
| Taxa por Superfície | $2,00 | Cada superfície adicional adiciona custo de impressão |
| Taxa por Upload | $1,00 | Imagens personalizadas requerem processamento |
| Taxa por Texto | $0,50 | Texto é mais simples de produzir do que imagens |

**Exemplo de cálculo:** Um cliente cria uma camiseta com texto na frente e um logotipo na parte de trás:
- Taxa de design base: $5,00
- 1 superfície extra (traseira): $2,00
- 1 logotipo carregado: $1,00
- 1 elemento de texto: $0,50
- **Total da taxa de design: $8,50** (adicionado ao preço base do produto)

### Exemplo: Preços de pôster


| Taxa | Valor | Razoão |
|-----|--------|-----------|
| Taxa de Design Básico | $0.00 | Nenhuma taxa básica — o preço do produto cobre isso |
| Taxa por Superfície | $0.00 | É uma superfície única, não aplicável |
| Taxa por Upload | $2.00 | Processamento de alta resolução |
| Taxa por Texto | $0.00 | O texto é incluído na experiência básica |

**Exemplo de cálculo:** Um cliente cria um póster com 2 fotos carregadas e 3 elementos de texto:
- Taxa de design básico: $0.00
- 2 fotos carregadas: $4.00
- 3 elementos de texto: $0.00
- **Total da taxa de design: $4.00**

A taxa de design é exibida aos clientes em tempo real à medida que eles adicionam elementos, para que possam ver o impacto de custo de cada adição antes de adicionar ao carrinho.

## Comparativo de configuração à primeira vista

| Aspecto | Camisa Personalizada | Póster Personalizado |
|--------|---------------|---------------|
| Superfícies | 3 (frente, verso, manga) | 1 (frente) |
| Imagens de mockup | 3 fotos do produto | 1 foto do produto |
| Posicionamento da zona | Áreas de peito/verso/braço | Área imprimível completa |
| Dimensões | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI mínimo | 150 | 200 |
| Bleed | 0 mm | 3 mm |
| Número máximo de cores | 6 | Ilimitado |
| Restrições por superfície | Manga restrita | Nenhuma necessária |
| Modelo de preço | Básico + superfície + upload + texto | Apenas taxas de upload |

## Dicas

- Sempre teste o editor de design do ponto de vista do cliente após concluir a configuração. Visite a página do produto no site de vendas e tente adicionar texto, carregar uma imagem e alternar superfícies.
- Carregue imagens de mockup que sejam muito próximas à aparção real do produto. Para camisas, faça fotos de cada ângulo separadamente. Para pósters, use uma foto limpa de lay-flat ou um mockup de moldura.
- Posicione a zona de design de forma conservadora — é melhor definir uma zona um pouco menor do que ter designs imprimindo em costuras ou bordas.
- Defina o DPI mínimo com base no seu método de impressão: 150 para impressão em tela, 200 para impressão digital padrão, 300 para impressão offset de alta qualidade.
- Use 3 mm de bleed para qualquer produto que será recortado após a impressão (pósters, cartão de negócios, folhetos). Defina o bleed para 0 para produtos onde o design é aplicado a uma superfície existente (camisas, xícaras, capas de celular).
- Comece com um preço simples e ajuste com base no feedback dos clientes. Muitos varejistas começam com apenas uma taxa de design básico e adicionam taxas por elemento depois.