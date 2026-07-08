---
title: Produtos Digitais
---

Os produtos digitais permitem vender arquivos para download, licenças de software e outros bens não-físicos. O Spwig suporta produtos digitais independentes, bem como produtos híbridos que combinam entrega física e digital.

![Provedores de licença](/static/core/admin/img/help/digital-products/license-providers.webp)

## Tipos de Produtos Digitais

### Produto Digital Independente

Defina o **Tipo de Produto** como **Produto Digital** para itens puramente digitais:
- Aplicativos de software
- E-books e PDFs
- Música e arquivos de áudio
- Arte digital e templates

### Produtos Híbridos

Qualquer tipo de produto pode incluir entrega digital marcando **É Produto Digital** na aba Informações Básicas. Isso é útil para:
- **Produtos digitais variáveis** — Software com edições Básica/Pro/Empresarial
- **Produtos digitais personalizáveis** — Ativos digitais personalizados
- **Pacotes físico + digital** — Um livro que inclui um download digital

## Configurando um Produto Digital

### Passo 1: Criar o Produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina o **Tipo de Produto** como **Produto Digital** (ou marque **É Produto Digital** em outro tipo de produto)
3. Preencha os detalhes do produto (nome, descrição, preço)
4. Salve o produto

### Passo 2: Adicionar Arquivos para Download

1. Vá para a aba **Estoque** do produto
2. Na seção **Arquivos Digitais**, faça upload dos arquivos que os clientes receberão após a compra
3. Para cada arquivo, você pode definir:
   - **Nome do arquivo** — Nome de exibição mostrado aos clientes
   - **Limite de downloads** — Número máximo de vezes que o arquivo pode ser baixado (0 = ilimitado)
   - **Dias de expiração** — Número de dias que o link de download permanece ativo

### Passo 3: Configurar Entrega de Licença (Opcional)

Se seu produto digital requer chaves de licença:

1. Navegue até **Configurações > Gerenciamento de Licenças**
2. Conecte um provedor de licenças (veja abaixo)
3. No formulário de edição do produto, atribua o provedor de licenças

## Provedores de Licenças

Provedores de licenças são serviços externos que geram e gerenciam chaves de licença de software automaticamente quando um cliente compra seu produto.

### Tipos de Provedores Disponíveis

| Provedor | Descrição |
|----------|-----------|
| **Servidor de Licenças Integrado do Spwig** | Geração simples de chaves de licença integrada à plataforma |
| **Keygen.sh** | API completa de gerenciamento de licenças |
| **LicenseSpring** | Gerenciamento de licenças empresarial |
| **Cryptlex** | Licenciamento de software com suporte offline |
| **API Personalizada** | Conecte qualquer sistema de licenças via REST API |

### Conectando um Provedor de Licenças

1. Navegue até **Configurações > Gerenciamento de Licenças**
2. Clique em **Conectar Provedor**
3. Siga o assistente de configuração:
   - **Passo 1** — Selecione o tipo de provedor
   - **Passo 2** — Configure as configurações gerais
   - **Passo 3** — Insira as credenciais da API
4. Teste a conexão para verificar se funciona
5. Salve a configuração

### Cartão do Provedor

Cada provedor conectado exibe:
- **Indicadores de status** — Ativo/Inativo e status da conexão
- **Endpoint da API** — A URL do servidor configurada
- **Capacidades de sincronização** — Suporte a sincronização de Pedido, Ativação e Desativação
- **Botões de ação** — Configurar, Testar e Sincronizar Agora

### Capacidades de Sincronização

Provedores de licenças podem sincronizar em três eventos:

- **Pedido** — Gerar automaticamente uma chave de licença quando um cliente conclui uma compra
- **Ativação** — Rastrear quando um cliente ativa sua licença
- **Desativação** — Lidar com desativação de licença para reembolsos ou transferências

## Experiência do Cliente

### Após a Compra

Quando um cliente compra um produto digital:

1. **Confirmação do pedido** — Mostra que a entrega digital está incluída
2. **Entrega por e-mail** — Links de download e/ou chaves de licença são enviados automaticamente
3. **Página da conta** — Clientes podem acessar seus downloads pelo painel da conta
4. **Página de download** — Links de download seguros com tempo limitado

### Segurança de Download

Os downloads de arquivos digitais são protegidos por:
- Tokens de download únicos com tempo limitado
- Limites opcionais de contagem de downloads
- Datas de expiração após as quais os links se tornam inativos
- Exigência de login (para clientes registrados)

## Dicas

- Defina limites de download razoáveis (3-5 downloads) para prevenir abuso enquanto permite re-downloads.
- Use dias de expiração que correspondam ao seu período de suporte (ex.: 365 dias para um ano de acesso).
- Teste o fluxo completo de compra com um pedido de teste para garantir que links de download e chaves de licença sejam entregues corretamente.
- Para produtos de software, conecte um provedor de licenças para automatizar a geração de chaves em vez de gerenciar chaves manualmente.
- Use o recurso de produto híbrido ao vender bens físicos que incluem extras digitais (ex.: livro impresso + PDF).
