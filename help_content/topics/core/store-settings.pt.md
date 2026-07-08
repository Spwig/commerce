---
title: Configurando Configurações da Loja
---

Configurações da Loja é o local central para configurar a identidade, localização, branding e preferências operacionais da sua loja. Navegue até **Configurações > Configurações da Loja** para começar.

![Guia geral de configurações da loja](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Guia Geral

O guia **Geral** contém as configurações de identidade central da sua loja.

### Identidade da Loja

- **Nome da Loja** — O nome exibido em títulos de página, e-mails e cabeçalho do painel administrativo.
- **Slogan** — Uma breve descrição da sua loja, usada em SEO e compartilhamento em redes sociais.
- **URL do Site** — O endereço web público da sua loja. É usado em e-mails, geração de mapa do site e construção de links.

### Informações de Contato

- **E-mail de Contato** — Recebe notificações de pedidos e é exibido em comunicações com clientes.
- **Número de Telefone** — Número de telefone opcional de suporte exibido no rodapé e e-mails.

### Endereço Comercial

Insira seu endereço completo (rua, cidade, estado, código postal, país). É usado para:
- Cálculos de origem de envio
- Cálculos de impostos
- Requisitos legais e notas fiscais

## Branding

### Logotipo

Carregue o logotipo da sua loja (recomendado PNG ou SVG, ~200x50px com fundo transparente). O logotipo aparece em:
- Cabeçalho do site
- Modelos de e-mail
- Painel administrativo

### Favicon

Carregue um favicon quadrado (ICO ou PNG, 32x32px). Ele aparece como:
- Ícone da guia do navegador
- Ícone de favorito
- Ícone da tela inicial do mobile

## Localização

### Idioma Padrão

Escolha o idioma principal da sua loja entre 10 opções suportadas:

| Idioma | Código |
|----------|------|
| Inglês | en |
| Espanhol | es |
| Francês | fr |
| Alemão | de |
| Português | pt |
| Japonês | ja |
| Chinês Simplificado | zh-hans |
| Chinês Tradicional | zh-hant |
| Russo | ru |
| Árabe | ar |

O idioma padrão controla o idioma da interface administrativa e o fallback para conteúdo do site.

### Fuso Horário

Selecione o fuso horário da sua loja para timestamps precisos de pedidos, promoções agendadas e relatórios.

### Moeda

- **Moeda Padrão** — A moeda principal para preços e contabilidade.
- **Multi-Moeda** — Ative para permitir que os clientes vejam os preços em sua moeda preferida com conversão automática usando taxas de câmbio em tempo real.

Configure moedas adicionais em **Configurações > Configurações da Loja > Moeda**.

## Configurações de E-Commerce

### Checkout para Visitantes

Permita compras sem criar uma conta:
- Fluxo de checkout mais rápido
- Menos atrito para compradores novos
- Captura menos dados do cliente

### Formato do Número do Pedido

Personalize como os números dos pedidos aparecem:
- **Prefixo** — por exemplo, "ORD-"
- **Número Inicial** — O primeiro número do pedido
- **Preenchimento** — por exemplo, 00001

### Configurações Padrão de Estoque

- **Rastrear Estoque** — Ative o rastreamento de estoque globalmente
- **Limite de Estoque Baixo** — Nível de alerta (padrão: 5 unidades)
- **Permitir Pedidos com Estoque Baixo** — Aceite pedidos quando estiver fora de estoque

## Configurações de E-mail

### Informações do Remetente

- **Nome do Remetente** — Aparece como o remetente do e-mail (normalmente o nome da sua loja)
- **E-mail do Remetente** — Deve ser de um domínio verificado
- **E-mail de Resposta** — Onde as respostas dos clientes são direcionadas

### Provedor de E-mail

Configure seu serviço de entrega de e-mail em **Configurações > Configuração de E-mail**. Provedores suportados incluem SMTP, SendGrid, Mailgun e Amazon SES.

## Legal & Conformidade

Adicione as políticas da sua loja para atender aos requisitos legais:

- **Termos e Condições** — Necessário para checkout; os clientes devem aceitar antes de comprar
- **Política de Privacidade** — Conformidade com GDPR/CCPA; vinculado no rodapé
- **Política de Devolução** — Defina seu período de devolução, condições e processo de reembolso

## Modo de Manutenção

Ative o modo de manutenção para desligar temporariamente sua loja:
- Exibe uma mensagem personalizada de manutenção para os visitantes
- Restringe o acesso apenas aos usuários do painel administrativo
- Útil durante atualizações importantes ou migrações

## Configurações de Imposto

Configure a coleta de impostos em **Configurações > Configurações de Imposto**:

1. **Método de Cálculo** — Por endereço de envio, endereço de cobrança ou localização da loja
2. **Taxas de Imposto** — Defina taxas por região e classe de imposto do produto
3. **Exibição de Imposto** — Mostre preços com imposto, sem imposto ou ambos

## Dicas

- Defina seu fuso horário corretamente antes de processar qualquer pedido — afeta todos os timestamps e relatórios.
- Ative o checkout para visitantes para melhorar as taxas de conversão.
- Preencha seu endereço comercial para cálculos precisos de envio e impostos.
- Carregue tanto um logotipo quanto um favicon para uma experiência profissional e com branding.
- Revise suas páginas legais regularmente para manter a conformidade com as regulamentações locais.

## Solução de Problemas

**Alterações não aparecendo no site:**
- Limpe o cache do seu navegador
- Execute uma limpeza de cache do painel administrativo
- Verifique se o modo de manutenção foi acidentalmente ativado

**E-mails não enviando:**
- Verifique as configurações do provedor de e-mail em Configuração de E-mail
- Confira se o domínio do e-mail do remetente está verificado
- Teste a conexão a partir da página de configuração do provedor

**Conversão de moeda não funcionando:**
- Verifique se seu provedor de taxa de câmbio está conectado
- Confira as credenciais da API nas configurações de taxa de câmbio
- Tente atualizar as taxas manualmente

