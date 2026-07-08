---
title: Sincronização de Configurações
---

A Sincronização de Configurações permite que você copie a configuração da loja entre duas instalações do Spwig. Isso é ideal para manter ambientes de staging e produção, onde você configura e testa alterações no staging antes de implantá-las em sua loja ativa.

## Quando Usar a Sincronização de Configurações

- **Staging para Produção**: Configure as configurações em sua loja de staging, depois envie-as para a produção
- **Produção para Staging**: Puxe as configurações da produção para o staging para começar com um ambiente correspondente
- **Backup de Configuração**: Puxe as configurações da produção para uma instância de backup como medida de segurança

A Sincronização de Configurações lida apenas com dados de configuração — ela não transfere produtos, clientes, pedidos ou arquivos de mídia. Para uma transferência de dados completa, use a Migração de Sistema Completa em vez disso.

## O Que Pode Ser Sincronizado

A Sincronização de Configurações suporta as seguintes categorias:

| Grupo | Categorias |
|-------|-----------|
| **Configurações** | Configurações do Site, Imposto & Moeda, Taxas de Imposto, Idiomas, Configurações do Blog, Compartilhamento Social, Regiões de Venda & Armazéns, Configuração de Pesquisa, Campos Personalizados, Papéis da Equipe, Análise de Clientes |
| **Design** | Design & Tema, Cabeçalhos/Rodapés/Menus |
| **Fornecedores** | E-mail, SMS/WhatsApp, Fornecedores de Pagamento, Envio, Fornecedores de SEO, Feeds de Produtos, Conectores Sociais do Blog, Configuração do POS |
| **Conteúdo** | Páginas & Modelos, Posts do Blog, Anúncios, Formulários, Coleções de Produtos |
| **Comércio** | Regras de Comércio (Vales, Promoções, Fidelidade, Assinaturas), Programa de Afiliados, Webhooks & Integrações |

> **Nota:** Categorias que contêm credenciais (fornecedores de pagamento, contas de envio, etc.) são marcadas com um ícone de chave. Chaves de API e segredos são transferidos de forma segura, mas podem precisar ser reentrados para integrações baseadas em OAuth.

## Guia Passo a Passo

### Etapa 1: Configurar uma Conexão

1. Navegue até **Migração de Dados > Sincronização Spwig para Spwig** no menu lateral do administrador
2. Clique em **Iniciar Sincronização de Configurações**
3. Selecione uma conexão salva ou crie uma nova:
   - Insira a URL da loja remota (ex.: `https://staging.yourstore.com`)
   - Cole o token de sincronização gerado na loja remota
   - Dê à conexão um nome descritivo
   - Defina o papel (Staging, Produção, Backup ou Outro)
4. Clique em **Testar Conexão** para verificar se funciona
5. Clique em **Próximo** para continuar

### Etapa 2: Escolher Categorias e Direção

**Direção:**
- **Puxar** — Copia as configurações da loja conectada para esta loja
- **Empurrar** — Copia as configurações desta loja para a loja conectada

**Modo de Sincronização:**
- **Adicionar & Atualizar** — Adiciona novos itens e atualiza os existentes, mas nunca exclui nada. Esta é a opção mais segura.
- **Cópia Exata** — Faz com que o destino corresponda exatamente à fonte, incluindo a remoção de itens que existem no destino, mas não na fonte. Use com cuidado.

Selecione as categorias que deseja incluir, depois clique em **Próximo**.

### Etapa 3: Visualizar as Alterações

Antes que qualquer alteração seja aplicada, você verá uma pré-visualização detalhada mostrando exatamente o que será adicionado, modificado ou removido para cada categoria. Revise isso com cuidado.

Se estiver empurrando para uma conexão de produção, você precisará confirmar que entende que as alterações afetarão sua loja ativa.

Clique em **Iniciar Sincronização** quando estiver pronto.

### Etapa 4: Monitorar o Progresso

A sincronização é executada em segundo plano. Você pode navegar livremente para longe da página de progresso — a sincronização continuará rodando.

A página de progresso mostra:
- Percentual de conclusão geral com tempo estimado restante
- Progresso por categoria com contagens de sucesso/falha
- Um log de atividade ao vivo que você pode expandir para saída detalhada

## Rollback

Após uma sincronização ser concluída, você tem **24 horas** para desfazer as alterações. Um rollback restaura o estado anterior de todas as configurações afetadas.

Para desfazer:
1. Vá para o **Painel de Sincronização**
2. Encontre o trabalho concluído
3. Clique em **Rollback** e confirme

Após 24 horas, a opção de rollback expira e as alterações tornam-se permanentes.

## Dicas

Preserve todos os formatos de markdown, caminhos de imagem, blocos de código e termos técnicos.

- **Teste no ambiente de staging primeiro**:

Sempre sincronize com um ambiente de staging primeiro para verificar os resultados antes de enviar para produção

- **Use o modo Adicionar & Atualizar**:

Este é o modo mais seguro, pois nunca exclui dados existentes

- **Verifique cuidadosamente a pré-visualização**:

A pré-visualização de diferença mostra exatamente o que será alterado antes de qualquer coisa ser aplicada

- **Conexões de produção mostram avisos**:

Ao enviar para uma conexão marcada como Produção, são necessárias confirmações de segurança adicionais