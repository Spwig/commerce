---
title: Regras de Visibilidade
---

# Regras de Visibilidade

As regras de visibilidade permitem que você mostre ou esconda partes da sua loja, dependendo de quem está visitando e de onde eles estão. Você pode restringir **elementos de página**, **itens de menu** e **widgets de cabeçário/rodapé** pelas mesmas condições — o mercado ou região do cliente, o idioma ou moeda em que eles estão visualizando, a hora do dia ou sinais por visitante, como se eles estão conectados ou não.

Tudo é construído a partir de **grupos de regras**: um conjunto nomeado, reutilizável de uma ou mais condições. Você cria um grupo de regras uma vez (por exemplo, "mercado da Nova Zelândia" ou "membros conectados") e depois o associa a qualquer elemento, item de menu ou widget que queira controlar. Um item sem grupo de regras associado é sempre visível.

## Como a visibilidade é decidida

Quando mais de um grupo de regra está associado a um item, o item é exibido se **algum** grupo associado combinar (eles se combinam com OR). Dentro de um único grupo, você escolhe se **todos** ou **algum** dos seus critérios devem combinar.

As regras se dividem em duas famílias, e o Spwig as trata de forma diferente para que sua loja permaneça rápida e amigável aos mecanismos de busca:

- **Regras de mercado** — condições baseadas em região, mercado, idioma, moeda e horário. Essas são decididas no servidor para cada URL de mercado, então a mesma página é entregue de forma idêntica a cada visitante (e a cada mecanismo de busca) nesse endereço. Isso mantém as páginas cacheáveis e seguras para SEO.
- **Regras por visitante** — status de conexão, conteúdo do carrinho, dispositivo e localização precisa. Essas dependem do visitante individual, então o Spwig as resolve de forma privada para cada pessoa após o carregamento da página. Elas nunca são incorporadas em uma página compartilhada, em cache.

Se você desativar um grupo de regras, ele simplesmente deixa de ser aplicado — o item ao qual estava associado retorna para ser visível. Desativar um grupo não é uma forma de esconder algo.

## Criando e anexando regras

Existem duas formas de trabalhar com grupos de regras.

### Anexe-as onde você estiver projetando

Em qualquer lugar em que você possa restringir conteúdo, você verá um **controle de visibilidade** (o ícone de olho):

- **Editor de Páginas** — selecione um elemento, abra suas propriedades e use o controle de visibilidade.
- **Editor de Menu** — selecione um item de menu e abra a aba **Visibilidade**. Isso funciona em **qualquer** item, incluindo um item de submenu (dropdown) aninhado em outro — uma regra em um filho esconde apenas esse filho, deixando o restante do menu intacto.
- **Editor de Cabeçário & Rodapé** — selecione um widget e abra a seção **Grupos de Regras de Visibilidade** nas configurações dele.

Regras que dependem do visitante individual — se eles estão conectados, o que há no seu carrinho ou seu dispositivo — são resolvidas para cada cliente sem atrapalhar a loja ou afetar os mecanismos de busca. Seu site permanece rápido e cacheável, e cada visitante ainda vê apenas a navegação destinada a ele.

No editor de visibilidade, você pode:

- **Anexar** qualquer um dos seus grupos de regras existentes marcando-os.
- **Regra rápida** — crie um grupo de regra simples no local (por exemplo, "apenas membros", um único mercado, uma moeda, um dispositivo ou um valor mínimo no carrinho) e o anexe em um passo.
- **Gerenciar grupos de regras** — vá para o construtor completo para regras avançadas.

Clique em **Aplicar** e o item será restringido imediatamente.

### Crie regras avançadas

Para qualquer coisa mais complexo — combinando várias condições, aninhando grupos ou operadores granulares — vá para **Design → Regras de Visibilidade** (grupos de regras). Lá, você pode montar regras com lógica AND/OR e reutilizá-las em toda a sua loja.

## Condições comuns

Preserve todos os formatos de markdown, caminhos de imagem, blocos de código e termos técnicos.

| Condição | Use para... |
|-----------|------------|
| **Região / mercado** | Exibir um bloco somente para visitantes em um mercado específico (por exemplo, Nova Zelândia) |
| **Moeda selecionada** | Exibir observações sobre preços ou ofertas somente quando uma determinada moeda estiver ativa |
| **Idioma selecionado** | Exibir conteúdo somente em um idioma específico |
| **Data / hora / dia / horário comercial** | Executar um banner durante uma janela de venda ou somente durante os horários de funcionamento |
| **Status de login** | Exibir conteúdo "somente para membros" ou um convite para se cadastrar para convidados |
| **Tipo de dispositivo** | Exibir ou ocultar algo em dispositivos móveis, tablets ou desktop |
| **Valor do carrinho / itens** | Exibir uma dica de frete grátis assim que o carrinho ultrapassar um limite |

## Pré-visualização

Na pré-visualização do Page Builder, você pode **visualizar como um mercado** e **visualizar como um visitante** (logado ou convidado, com um carrinho de compras de exemplo) para ver exatamente o que cada público veria — incluindo as regras específicas para cada visitante que normalmente são resolvidas de forma privada.

## Dicas

- Crie um pequeno conjunto de grupos de regras bem nomeados ("Mercado da Nova Zelândia", "Membros", "Somente dispositivos móveis") e os reutilize em todos os lugares — é mais fácil de gerenciar do que regras únicas.
- As regras de mercado são a escolha segura para qualquer coisa que você queira indexada pelos mecanismos de busca, porque o resultado é o mesmo para todos em uma URL de mercado específica.
- Se um item desaparecer inesperadamente, verifique seus grupos de regra associados — um item é oculto somente quando ele tem um grupo ativo e nenhum dos seus grupos combina com o visitante atual.