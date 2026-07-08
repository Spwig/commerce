---
title: Configuração do Fornecedor de SMS
---

As notificações por SMS mantêm seus clientes informados em cada etapa do pedido — desde a confirmação até a entrega. Para enviar mensagens de SMS ou WhatsApp do seu loja, você conecta uma conta de fornecedor de SMS com suas credenciais. Uma vez conectado, o Spwig usa essa conta para enviar todas as mensagens de texto saídas.

Navegue até **Sistema de SMS > Contas de Fornecedores de SMS** para gerenciar seus fornecedores de SMS.

![Lista de contas de fornecedores de SMS](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Adicionar um fornecedor de SMS

Você pode adicionar um fornecedor usando o **Assistente de Configuração** (recomendado para a primeira configuração) ou o formulário manual.

### Usando o assistente de configuração

1. Navegue até **Sistema de SMS > Contas de Fornecedores de SMS**
2. Clique em **Assistente de Configuração** na barra de ferramentas
3. Siga as etapas guiadas:
   - **Etapa 1**: Escolha seu fornecedor da lista de fornecedores disponíveis
   - **Etapa 2**: Insira suas credenciais do fornecedor (chaves de API, SID da conta, etc.)
   - **Etapa 3**: Defina o nome de exibição e as configurações padrão, depois salve
4. O assistente testa a conexão automaticamente antes de salvar

### Adicionar um fornecedor manualmente

1. Navegue até **Sistema de SMS > Contas de Fornecedores de SMS**
2. Clique em **Explorar Fornecedores** para explorar os fornecedores de SMS disponíveis, ou clique em **+ Adicionar Conta de Fornecedor de SMS** diretamente
3. No campo **Fornecedor**, selecione seu fornecedor de SMS da lista suspensa
4. Depois que você selecionar um fornecedor, os campos de credencial aparecem automaticamente com base no que esse fornecedor requer
5. Preencha os campos de credencial necessários (esses variam conforme o fornecedor — veja as seções abaixo para fornecedores comuns)
6. Insira um **Nome de Exibição** para identificar essa conta (ex: `Twilio — Principal`)
7. Defina as **Configurações Padrão** (veja abaixo)
8. Clique em **Salvar**

## Credenciais do fornecedor

### Twilio

| Campo | Onde encontrá-lo |
|-------|-----------------|
| Account SID | Console do Twilio → Dashboard |
| Auth Token | Console do Twilio → Dashboard |
| From Number | Seu número de telefone do Twilio no formato E.164 (ex: `+15551234567`) |

### Outros fornecedores

Outros componentes de fornecedores de SMS instalados mostrarão seus próprios campos de credencial específicos ao serem selecionados. Consulte a documentação do seu fornecedor para os valores exatos necessários — normalmente uma chave de API ou token de acesso e um identificador de remetente.

## Configurações padrão

Depois de inserir as credenciais, configure como essa conta será usada:

- **Ativo** — ative ou desative essa conta. Contas inativas não são usadas para enviar, mesmo se definidas como padrão
- **Conta de SMS Padrão** — ao marcar, todas as notificações de SMS do seu loja usam essa conta. Apenas uma conta pode ser a conta de SMS padrão de cada vez
- **Conta de WhatsApp Padrão** — se esse fornecedor suportar WhatsApp (ex: Twilio via WhatsApp Business API), marque para usá-lo como padrão para mensagens de WhatsApp

## Testando a conexão

Depois de salvar uma conta de fornecedor, teste se as credenciais funcionam:

1. Navegue até **Sistema de SMS > Contas de Fornecedores de SMS**
2. Clique na sua conta de fornecedor para abri-la
3. Clique no botão **Testar Conexão**
4. O Spwig envia uma solicitação de teste ao fornecedor e atualiza o campo **Status da Conexão**

| Status | Significado |
|--------|---------|
| Conectado | Credenciais são válidas e o fornecedor está acessível |
| Falha na Conexão | Credenciais estão incorretas ou o fornecedor não está acessível |
| Não Testado | A conexão ainda não foi testada |

Se o teste falhar, verifique novamente suas credenciais e certifique-se de que sua conta tenha as permissões necessárias no painel do fornecedor.

## Coluna de status da conexão

A lista de Contas de Fornecedores de SMS mostra um **badge de conexão** colorido para cada conta:

- **Conectado** (verde) — conta está funcionando
- **Falha na Conexão** (vermelho) — credenciais falharam — atualize-as
- **Não Testado** (cinza) — conta ainda não foi testada

## Dicas

- Use o Assistente de Configuração para seu primeiro fornecedor — ele guia você por cada campo e testa a conexão antes de salvar
- Apenas uma conta pode ser a Conta de SMS Padrão de cada vez.

Se você adicionar uma segunda conta e marcá-la como padrão, a anterior padrão será automaticamente desmarcada
- Mantenha anotado as credenciais da API do seu provedor em um local seguro.

Se as credenciais mudarem, atualize-as aqui imediatamente para evitar notificações falhas
- Contas inativas permanecem na lista, mas não são usadas para enviar — útil para manter credenciais de backup sem ativá-las
- A maioria dos provedores cobra por mensagem enviada — monitore o uso no painel do seu provedor para evitar contas inesperadas