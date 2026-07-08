---
title: Migração Completa do Sistema
---

A Migração Completa do Sistema transfere toda a sua loja – configurações, produtos, clientes, pedidos, arquivos de mídia e todos os outros dados – de uma instalação do Spwig para outra. Use isso ao migrar para um novo servidor ou configurar uma cópia completa de sua loja.

## Quando Usar a Migração Completa

- **Reposição de servidor**: Mover sua loja para um novo provedor de hospedagem ou servidor
- **Criar uma cópia de staging**: Configurar um ambiente de staging completo a partir do ambiente de produção
- **Recuperação de desastre**: Restaurar uma loja completa a partir de uma instância de backup

A Migração Completa inclui tudo que a Sincronização de Configurações faz, mais todos os dados transacionais (produtos, clientes, pedidos, avaliações, estoque, mídia, etc.).

## O Que É Migrado

A Migração Completa pode transferir todas as categorias de configurações mais estas categorias de dados:

| Categoria | Descrição |
|----------|-------------|
| **Componentes Instalados** | Temas, integrações de provedores e componentes utilitários com seus arquivos de pacote |
| **Produtos, Categorias & Marcas** | Produtos, variantes, imagens, categorias, marcas e atributos |
| **Biblioteca de Mídia** | Todos os arquivos de mídia carregados e ativos |
| **Clientes & Endereços** | Contas de clientes, perfis e endereços |
| **Histórico de Pedidos** | Pedidos, itens de pedido e registros de transação |
| **Avaliações de Produtos** | Avaliações e notas dos clientes |
| **Níveis de Estoque** | Quantidades de estoque por depósito e pontos de reposição |
| **Produtos Digitais & Licenças** | Ativos digitais, modelos de licença e pools de licença |
| **Cartões-presente & Uso de Cupons** | Saldo de cartões-presente e registros de uso de cupons |
| **Crédito da Loja & Carteiras** | Saldo das carteiras dos clientes e histórico de transações |
| **Membros do Programa de Fidelidade** | Membros de fidelidade, pontos, transações e conquistas |
| **Assinaturas Ativas** | Planos de assinatura, assinaturas ativas e histórico de cobrança |
| **Envios & Rastreamento** | Registros de envio e eventos de rastreamento |
| **Reembolsos, Devoluções & Notas de Pedido** | Registros de reembolso, solicitações de devolução e notas |
| **Membros de Afiliados** | Contas de afiliados, códigos de indicação e histórico de comissões |

## Guia Passo a Passo

### Passo 1: Conectar-se à Instância de Origem

1. Navegue até **Data Migration > Spwig-to-Spwig Sync** no menu lateral do administrador
2. Clique em **Start Full Migration**
3. Conecte-se à loja de origem (a loja da qual você está migrando):
   - Insira a URL da loja de origem
   - Cole o token de sincronização da loja de origem
   - Nomeie a conexão (ex.: "Old Production Server")
4. Clique em **Test Connection** para verificar
5. Clique em **Next**

> **Importante:** A Migração Completa sempre **puxa** dados da loja conectada para esta loja. Execute o assistente na loja de **destino** (nova) store.

### Passo 2: Escolher o Escopo

Selecione quais categorias de dados incluir na migração. As categorias estão organizadas em grupos:

- **Configurações**: Configuração da loja, temas, provedores, conteúdo
- **Dados**: Produtos, clientes, pedidos, mídia e outros dados transacionais

Algumas categorias têm dependências (ex.: Pedidos dependem de Clientes e Produtos). As dependências são incluídas automaticamente ao selecionar uma categoria.

Categorias com indicadores especiais:
- **Ícone de chave**: Contém credenciais que são transferidas com segurança
- **Ícone de arquivo**: Inclui arquivos binários (imagens, mídia, pacotes)
- **Ícone de aviso**: Considerações especiais para ambientes de produção

### Passo 3: Verificações Pré-Execução

Antes de iniciar a migração, verificações automáticas de pré-execução confirmam:

- **Saúde da conexão**: A loja de origem está acessível e autenticada
- **Compatibilidade de versão**: Ambas as lojas estão executando versões compatíveis do Spwig
- **Espaço em disco**: Há armazenamento suficiente disponível para arquivos de mídia
- **Prontidão do banco de dados**: O banco de dados de destino pode receber os dados

Se qualquer verificação falhar, você verá orientações específicas sobre como resolver o problema antes de continuar.

### Passo 4: Progresso da Migração

A migração é executada em segundo plano. Você pode navegar livremente – o processo continuará.


A página de progresso mostra:
- Percentual geral com tempo estimado restante
- Status de conclusão por categoria
- Registro de atividade em tempo real com detalhes da transferência
- Estatísticas de transferência de mídia (arquivos e bytes transferidos) para a categoria de mídia

Para lojas grandes com muitos produtos e arquivos de mídia, a migração pode levar algum tempo. A fase de transferência de mídia é normalmente a mais longa.

### Etapa 5: Resultados

Após a migração ser concluída, a página de resultados mostra:

- Estatísticas resumidas (itens migrados, pulados e falhos)
- Quebra de detalhes por categoria com status
- Detalhes de erro para quaisquer itens falhos

## Checklist pós-migração

Após uma migração bem-sucedida, conclua estas etapas em sua nova loja:

1. **Ative sua licença** na nova instalação
2. **Reinsira as credenciais do provedor de pagamento** que foram puladas durante a migração (chaves de sandbox/teste não são transferidas para produção)
3. **Configure o DNS** para apontar seu domínio para o novo servidor
4. **Teste o fluxo de checkout** com um pedido de teste
5. **Verifique se o envio de e-mails** está funcionando corretamente
6. **Verifique os arquivos de mídia** e se as imagens estão carregando corretamente

## Rollback

Após uma Migração Completa, você tem **24 horas** para fazer um rollback. Um rollback exclui todos os dados migrados da loja de destino, restaurando-a ao estado anterior à migração.

Para fazer um rollback:
1. Vá para a página de resultados ou para o Painel de Sincronização
2. Clique em **Rollback Migration** e confirme
3. Aguarde o rollback ser concluído

> **Aviso:** O rollback remove permanentemente todos os dados migrados. Quaisquer alterações feitas na loja de destino após a migração (novos pedidos, inscrições de clientes, etc.) também serão afetadas.

Após 24 horas, a opção de rollback expira.

## Dicas

- **Execute na loja de destino**: O assistente de Migração Completa deve ser executado na **nova** loja, puxando dados da antiga
- **Migre para uma instalação limpa**: Para os melhores resultados, execute a migração em uma instalação limpa do Spwig antes de ir ao ar
- **Verifique o espaço em disco**: Certifique-se de que o destino tenha armazenamento suficiente para todos os arquivos de mídia
- **Mantenha a fonte em execução**: Não desligue a loja de origem até que você tenha verificado que tudo funciona na loja de destino
- **Planeje a transição do DNS**: Após verificar a migração, atualize seus registros DNS para apontar para o novo servidor