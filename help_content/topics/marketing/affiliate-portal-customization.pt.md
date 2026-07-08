---
title: Personalização do Portal de Afiliados
---

O Portal de Afiliados do Spwig é a página inicial pública onde potenciais afiliados aprendem sobre seu programa e se inscrevem. Personalizar este portal permite que você alinhe a mensagem, a marca e o call-to-action com a posição única de sua loja. Um portal bem projetado atrai afiliados de alta qualidade e converte visitantes em parceiros ativos.

## O que é o Portal de Afiliados?

O portal de afiliados está acessível em `/affiliate/` no domínio de sua loja. Ele serve como:

- **Página de descoberta** — Onde potenciais afiliados aprendem sobre sua estrutura de comissão, benefícios e requisitos
- **Ponto de entrada para inscrição** — Formulário de inscrição para novos afiliados (inscrição como visitante ou baseada em conta)
- **Porta de login** — Afiliados existentes podem fazer login para acessar seu painel
- **Exibição da marca** — Reflete a identidade de sua loja e a proposta de valor do programa de afiliados

O portal é totalmente personalizável através das configurações de afiliados no painel de administração, incluindo a mensagem do herói, destaque de recursos, fluxos passo a passo e opções de inscrição.

![Página Inicial do Portal de Afiliados](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Acessando Configurações

Navegue até **Marketing > Programa de Afiliados > Configurações do Portal** para personalizar o portal.

O modelo de configurações de afiliados é um **singleton** — você tem exatamente um registro de configurações para toda a sua loja. Todos os campos são **traduzíveis** usando o sistema de tradução do Spwig, então você pode personalizar a mensagem para cada idioma que sua loja suporta.

## Seção de Herói

A seção de herói é a primeira coisa que os potenciais afiliados veem. Ela inclui:

- **Título** — Cabeçalho principal (ex: "Junte-se ao Nosso Programa de Afiliados")
- **Subtítulo** — Texto de suporte explicando o valor do programa (ex: "Ganhe comissões promovendo produtos premium para sua audiência")
- **Estatísticas** — Métricas exibidas automaticamente:
  - Total de programas ativos
  - Total de afiliados ativos
  - Taxa média de comissão (calculada em todos os programas ativos)
- **Botões CTA** — Gerados automaticamente:
  - **Entrar** — Para afiliados existentes
  - **Torne-se um Afiliado** — Inicia o fluxo de inscrição

### Personalizando a Mensagem do Herói

| Campo | Valor Exemplo | Propósito |
|-------|--------------|---------|
| **Título do Herói** | "Parceiro Conosco & Ganhe" | Atrair atenção com um cabeçalho focado em benefícios |
| **Subtítulo do Herói** | "Junte-se a 500+ afiliados ganhando comissões competitivas em cada venda que você refere" | Fornecer prova social e esclarecer a oferta |

As estatísticas são **calculadas automaticamente** e atualizam em tempo real com base em seus programas e afiliados ativos. Você não pode editar manualmente esses valores.

## Seção de Recursos

A seção de recursos destaca **6 cartões de benefícios personalizáveis** que explicam por que os afiliados devem se juntar ao seu programa. Cada cartão de recurso contém:

- **Ícone** — Classe de ícone FontAwesome (ex: `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Título** — Cabeçalho do benefício (ex: "Comissões Competitivas")
- **Descrição** — Explicação de 1-2 frases (ex: "Ganhe até 15% em cada venda que você refere")

### Recursos Padrão

O Spwig fornece recursos padrão quando você instala pela primeira vez o aplicativo de afiliados:

| Ícone | Título | Descrição |
|------|-------|-------------|
| `fa-dollar-sign` | Comissões Competitivas | Ganhe comissões generosas em cada venda que você refere |
| `fa-link` | Links de Rastreamento Fáceis | Obtenha links de rastreamento únicos que funcionam em qualquer lugar |
| `fa-chart-line` | Análises em Tempo Real | Rastreie cliques, conversões e ganhos no seu painel |
| `fa-calendar-check` | Pagamentos Confiáveis | Receba seu pagamento no prazo via PayPal ou transferência bancária |
| `fa-headset` | Suporte Especializado | Nosso time está aqui para ajudá-lo a ser bem-sucedido |
| `fa-gift` | Materiais de Marketing | Acesse banners, imagens e conteúdo promocional |

### Personalizando Recursos

Os recursos são armazenados como um **array JSON** no banco de dados. Edite-os diretamente no formulário de administração:

```json
[
  {
    "icon": "fa-percent",
    "title": "Até 20% de Comissão",
    "description": "Ganhe comissões líderes do setor em vendas de produtos premium"
  },
  {
    "icon": "fa-rocket",
    "title": "Aprovação Rápida",
    "description": "Obtenha aprovação em 24 horas e comece a promover imediatamente"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Painel Móvel",
    "description": "Gerencie seus links e rastreie ganhos de qualquer dispositivo"
  }
]
```

**Referência de Ícone:** Use qualquer classe de ícone gratuita FontAwesome 5. Navegue pelos ícones em [fontawesome.com/icons](https://fontawesome.com/icons) e use o nome da classe (ex: `fa-trophy`, `fa-users`, `fa-star`).

## Seção Como Funciona

A seção "Como Funciona" exibe um **fluxo visual de 4 etapas** que explica a jornada do afiliado. Cada etapa inclui:

- **Título** — Nome da etapa (ex: "Cadastrar")
- **Descrição** — Explicação de 1-2 frases do que acontece

### Etapas Padrão

| Etapa | Título | Descrição |
|------|-------|-------------|
| 1 | Cadastrar | Crie sua conta de afiliado gratuita em minutos |
| 2 | Obter Seus Links | Gere links de rastreamento únicos para qualquer produto ou página |
| 3 | Promover | Compartilhe seus links com sua audiência por meio de conteúdo, mídia social ou e-mail |
| 4 | Ganhar Comissões | Receba pagamento quando os clientes comprarem usando seus links de indicação |

### Personalizando Etapas

As etapas são armazenadas como um **array JSON**. Você pode editá-las no painel de administração:

```json
[
  {
    "title": "Candidate-se para Participar",
    "description": "Envie sua candidatura e nos conte sobre sua plataforma"
  },
  {
    "title": "Obtenha Aprovação",
    "description": "Nosso time revisa sua candidatura dentro de 24 horas"
  },
  {
    "title": "Criar Links",
    "description": "Acesse seu painel e gere links de rastreamento instantaneamente"
  },
  {
    "title": "Comece a Ganhar",
    "description": "Ganhe comissões em cada venda que você refere — pago mensalmente via PayPal"
  }
]
```

O fluxo visual numera automaticamente cada etapa (1, 2, 3, 4) na página inicial.

## Seção CTA

A seção final antes do formulário de inscrição é a **Seção de Chamada para Ação (CTA)**. Ela fornece um último empurrão para encorajar as inscrições.

| Campo | Valor Exemplo | Propósito |
|-------|--------------|---------|
| **Título CTA** | "Pronto para Começar a Ganhar?" | Pergunta direta cria urgência |
| **Descrição CTA** | "Junte-se ao nosso programa de afiliados hoje e comece a ganhar comissões em produtos que já ama e recomenda." | Reforçar benefícios e eliminar fricção |

A seção CTA exibe automaticamente o botão **Torne-se um Afiliado** abaixo do texto.

## Configurações de Inscrição

Controle como novos afiliados se inscrevem e quais informações eles fornecem.

### Formulário de Inscrição Personalizado

**Campo:** `custom_form` (Chave estrangeira para o formulário do FormBuilder)

Se você tem um formulário de inscrição personalizado construído com o FormBuilder do Spwig, selecione-o aqui. Isso permite que você colete informações adicionais durante a inscrição (ex: URL do site, tamanho da audiência, canais de promoção).

**Deixe em branco** para usar o formulário padrão de inscrição de afiliados (e-mail, senha, detalhes de pagamento).

### Permitir Inscrição de Visitantes

**Campo:** `allow_guest_registration` (Booleano)

- **Marcado** — Visitantes podem se candidatar sem criar uma conta do Spwig primeiro
- **Não marcado** — Visitantes devem fazer login ou criar uma conta de cliente antes de se candidatar

**Recomendação:** Ative a inscrição de visitantes para reduzir a fricção. Você sempre pode exigir aprovação para verificar afiliados antes de ativá-los.

### Requerer Aprovação

**Campo:** `require_approval` (Booleano)

- **Marcado** — Novos afiliados devem aguardar aprovação manual antes de acessar seu painel
- **Não marcado** — Novos afiliados são aprovados automaticamente e podem criar links imediatamente

**Recomendação:** Ative a aprovação manual se quiser verificar afiliados para adequação à marca, prevenção de fraudes ou programas exclusivos.

### URL de Termos e Condições

**Campo:** `terms_url` (URL)

Link opcional para os termos e condições do seu programa de afiliados. Se fornecido, o formulário de inscrição exibe um checkbox exigindo que os afiliados concordem com seus termos antes de se inscreverem.

**Exemplo:** `/pages/affiliate-terms/`

### Mensagem de Boas-vindas

**Campo:** `welcome_message` (Texto)

Mensagem exibida aos afiliados imediatamente após a inscrição bem-sucedida. Use isso para:

- Agradecer por se juntarem
- Explicar os próximos passos (ex: "Revisaremos sua candidatura em 24 horas")
- Linkar a recursos para começar

**Exemplo:"
```
Bem-vindo ao nosso programa de afiliados! Recebemos sua candidatura e a revisaremos em 24 horas. Verifique seu e-mail para confirmação de aprovação e instruções de login.
```

## Suporte Multilíngue

Todos os campos de texto nas Configurações de Afiliados são **traduzíveis** usando o widget de tradução do Spwig:

- Título do Herói
- Subtítulo do Herói
- Recursos (JSON traduzido por idioma)
- Etapas Como Funciona (JSON traduzido por idioma)
- Título CTA
- Descrição CTA
- Mensagem de Boas-vindas

### Como Funciona a Tradução

Quando você edita um campo traduzível, você verá um widget de tradução que permite que você forneça conteúdo para cada idioma habilitado. Para campos JSON (recursos, etapas), você fornece objetos JSON separados por idioma:

**Inglês:"
```json
[
  {"icon": "fa-dollar-sign", "title": "Comissões Competitivas", "description": "Ganhe até 15% em cada venda"}
]
```

**Espanhol:"
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Ganar hasta el 15% en cada venta"}
]
```

O portal exibe automaticamente a versão correta do idioma com base na preferência de idioma do visitante.

## Visualizar Suas Alterações

Depois de personalizar as configurações do portal:

1. **Salve** suas alterações no painel de administração
2. Visite `/affiliate/` no frontend de sua loja (abrir em uma nova guia)
3. **Teste o fluxo de inscrição** clicando em "Torne-se um Afiliado"
4. **Verifique a consistência da marca** — o portal corresponde ao design e mensagem da sua loja?

Você pode fazer alterações iterativas e atualizar a página para ver as atualizações imediatamente.

## Exemplos de Personalizações

### Cenário 1: Loja de Moda E-Commerce

**Objetivo:** Recrutar influenciadores e blogueiros de moda.

| Configuração | Valor |
|---------|-------|
| Título do Herói | "Promova Estilos que Você Ama & Ganhe" |
| Subtítulo do Herói | "Junte-se a 1.200+ influenciadores ganhando 12% de comissão em cada venda" |
| Recurso 1 | Ícone: `fa-tshirt`, Título: "Coleções de Moda Curadas", Descrição: "Promova roupas premium e acessórios" |
| Recurso 2 | Ícone: `fa-percentage`, Título: "12% de Comissão", Descrição: "Taxas líderes do setor em todos os produtos" |
| Recurso 3 | Ícone: `fa-camera`, Título: "Conteúdo Exclusivo", Descrição: "Acesse fotos, vídeos e ativos de campanha de produtos" |
| Permitir Inscrição de Visitantes | Marcado |
| Requerer Aprovação | Marcado (revisão manual para adequação à marca) |

### Cenário 2: Programa de Parceria SaaS B2B

**Objetivo:** Recrutar consultores e agências para indicações de software empresarial.

| Configuração | Valor |
|---------|-------|
| Título do Herói | "Parceiro Conosco para Crescer a Receita" |
| Subtítulo do Herói | "Ganhe $500 por indicação de empresas através do nosso programa de parceria B2B" |
| Recurso 1 | Ícone: `fa-handshake`, Título: "$500 por Indicação", Descrição: "Comissão fixa para leads de empresas qualificados" |
| Recurso 2 | Ícone: `fa-clock`, Título: "Cookie de 180 Dias", Descrição: "Janela longa de atribuição para ciclos de vendas complexos" |
| Recurso 3 | Ícone: `fa-user-tie`, Título: "Gerente de Parceiro Especializado", Descrição: "Suporte de luxo para seus clientes" |
| Permitir Inscrição de Visitantes | Não marcado (B2B requer conta) |
| Requerer Aprovação | Marcado (programa convidado apenas) |
| URL de Termos | `/pages/partner-program-terms/` |

## Dicas

- Personalize seu **título do herói** para focar em benefícios, não em recursos — "Ganhe Enquanto Dorme" é mais convincente do que "Inscrição no Programa de Afiliados"
- Use **prova social** no subtítulo (ex: "Junte-se a 500+ afiliados") para construir confiança e credibilidade
- Escolha **ícones FontAwesome** que reforcem visualmente cada benefício — o ícone deve comunicar imediatamente o valor
- Mantenha as descrições dos recursos em **1-2 frases** — o portal é sobre conversão, não explicações exaustivas
- Teste o **fluxo de inscrição** você mesmo antes de promover o portal — identifique pontos de fricção como campos de formulário confusos ou links quebrados
- Ative a **inscrição de visitantes** para reduzir a fricção de inscrição, depois use **requerer aprovação** para verificar afiliados após a submissão
- Use a **mensagem de boas-vindas** para estabelecer expectativas (cronograma de aprovação, próximos passos, contato de suporte) e reduzir perguntas de suporte
- Atualize o portal **estacionalmente** para alinhar com campanhas — destaque promoções de comissão especiais ou lançamentos de produtos