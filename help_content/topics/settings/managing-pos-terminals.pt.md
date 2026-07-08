---
title: Gerenciamento de Terminais POS
---

O gerenciamento de terminais POS é a base das operações de varejo. Cada terminal representa um dispositivo físico (tablete, computador ou hardware POS dedicado) onde o pessoal processa vendas. Configure terminais com atribuições de armazém, autorizações de pessoal, integrações de hardware e configurações de sincronização offline. Monitore a saúde dos terminais com rastreamento de batimento cardíaco em tempo real e desbloqueie remotamente terminais quando surgirem problemas. Um gerenciamento adequado dos terminais garante operações suaves no local e evita conflitos de configuração entre locais.

Navegue até **POS > Terminais** para registrar novos terminais, visualizar o status online/offline e gerenciar todas as configurações do terminal.

![Lista de Terminais](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Visão da Lista de Terminais

A lista de terminais exibe todos os terminais registrados com informações de status importantes:

**Nome do Terminal** - Rótulo descritivo para o terminal (ex.: "Caixa 1", "Caixa Principal", "Terminal Móvel")

**UUID** - Identificador único gerado automaticamente na criação (usado internamente para identificação do dispositivo)

**Armazém** - Local físico atribuído a este terminal (determina a disponibilidade de estoque e atribuição de pedidos)

**Status Online** - Indicador em tempo real mostrando se o terminal está atualmente conectado:
- **Ponto verde** - Online (batimento cardíaco recebido nos últimos 5 minutos)
- **Ponto vermelho** - Offline (sem batimento cardíaco há mais de 5 minutos)
- **Ponto cinza** - Nunca pareado (terminal criado, mas o dispositivo nunca se conectou)

**Último Batimento Cardíaco** - Carimbo de tempo do último ping do terminal (atualiza a cada 5 minutos quando online)

**Código de Pareamento** - Código alfanumérico de 8 caracteres usado para o pareamento inicial do dispositivo (oculto após o primeiro uso)

**Usuários Atribuídos** - Contagem de funcionários autorizados a usar este terminal

## Criando um Novo Terminal

Clique em **+ Adicionar Terminal** para registrar um novo dispositivo POS:

![Formulário de Adição de Terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Configuração Básica

**Nome do Terminal** - Escolha um nome descritivo que indique:
- Local físico: "Caixa de Entrada Norte"
- Função: "Terminal de Devoluções"
- Sequência: "Caixa 1", "Caixa 2", "Caixa 3"

Os nomes ajudam o pessoal a identificar terminais durante a atribuição de turnos e solução de problemas. Use convenções de nomenclatura consistentes em todos os locais.

**Armazém** - **REQUERIDO** - Selecione o armazém do qual este terminal opera:
- Determina quais estoques estão disponíveis para venda
- Pedidos colocados neste terminal são atribuídos a este armazém
- Verificações de reservas de estoque verificam a disponibilidade no armazém atribuído
- **Não é possível processar vendas sem atribuição de armazém**

Se você tiver múltiplas lojas, crie um armazém separado para cada local e atribua os terminais conforme necessário.

**Ativo** - Ative/desative o terminal sem excluir a configuração:
- Terminais inativos não podem ser pareados
- Sessões existentes em terminais inativos expiram imediatamente
- Use para desativar temporariamente terminais roubados ou danificados

### Atribuição de Pessoal

**Usuários Atribuídos** - Selecione quais funcionários podem acessar este terminal:
- Apenas usuários atribuídos podem fazer login no terminal
- Os usuários devem também ter permissões POS em seu papel de funcionário
- Atribuir zero usuários efetivamente bloqueia o terminal
- Padrão comum: Atribuir todos os funcionários da loja a todos os terminais da loja

**Exemplos de Casos de Uso**:
- **Loja Geral**: Atribuir todos os funcionários a todos os terminais (qualquer caixa pode trabalhar em qualquer caixa)
- **Loja de Departamentos**: Atribuir funcionários específicos de departamento aos terminais de departamento
- **Multi-local**: Atribuir funcionários específicos de local aos terminais de local
- **Gerentes**: Atribuir gerência a todos os terminais para acesso de supervisão

Usuários sem atribuição de terminal veem o erro "Não autorizado para este terminal" ao tentar fazer login.

### Configuração de Hardware

O campo **Configuração de Hardware** é uma estrutura JSON definindo dispositivos periféricos:

**Impressora Térmica**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**Leitor de Códigos de Barras USB**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Caixa Registradora** (conectada à impressora):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Exemplo Completo**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Deixe em branco se o terminal não tiver hardware periférico (adequado para terminais móveis ou tablets sem impressora/leitor de códigos de barras).

### Configurações de Cache Offline

Configure quanto de dados o terminal armazena localmente para operação offline:

**Dias de Sincronização de Pedidos** (7-30 dias, padrão: 14):
- Número de dias de pedidos recentes para armazenar localmente
- Valores mais altos = mais dados históricos disponíveis offline
- Valores mais baixos = sincronização mais rápida, menos armazenamento usado
- **Recomendação**: 7 dias para terminais de alto volume, 14 dias para uso normal, 30 dias para operações com auditoria intensa

**Limite de Sincronização de Pedidos** (200-1000 pedidos, padrão: 500):
- Número máximo de pedidos para armazenar, independentemente do intervalo de datas
- Impede o uso excessivo de armazenamento em terminais de alto volume
- **Recomendação**: 200 para tablets com armazenamento limitado, 500 para terminais padrão, 1000 para dispositivos POS dedicados

**Compromissos**:
- **Configurações mais altas**: Melhor acesso offline a dados históricos, sincronização inicial mais lenta, mais armazenamento usado
- **Configurações mais baixas**: Sincronização mais rápida, menos armazenamento, histórico offline limitado

O terminal baixa os X pedidos mais recentes (dentro de Y dias) em cada ciclo de sincronização. Se o terminal processar 50 pedidos/dia e sync_days for 14, espere ~700 pedidos armazenados (pode atingir o limite de sincronização).

## Fluxo de Trabalho de Pareamento de Terminal

Depois de criar um terminal, pareie o dispositivo físico:

1. **Gerar Código de Pareamento** - Criado automaticamente ao salvar o terminal (8 caracteres alfanuméricos)

2. **Anote o Código** - Exibido na lista de terminais e na visão detalhada (expira após o primeiro pareamento bem-sucedido)

3. **Navegue até o Dispositivo Terminal** - No dispositivo físico (tablete/computador), abra o navegador e vá para: `https://yourstore.com/pos/`

4. **Digite o Código de Pareamento** - Digite o código de 8 caracteres quando solicitado

5. **Terminal Baixa a Configuração** - O dispositivo recebe:
   - Atribuição de armazém
   - Configuração de hardware (impressora, leitor de códigos de barras, caixa registradora)
   - Configurações de cache offline
   - Lista de usuários atribuídos
   - Sincronização inicial do catálogo de produtos

6. **Tela de Login Aparece** - O terminal exibe a tela de login para usuários atribuídos

7. **Funcionário Faz Login** - Digite as credenciais para o usuário atribuído a este terminal

8. **Sincronização Inicial Completa** - O terminal baixa:
   - Pedidos recentes (conforme sync_days e sync_limit)
   - Catálogo completo de produtos para o armazém atribuído
   - Banco de dados de clientes
   - Configurações de promoções

9. **Terminal Pronto** - A tela "Pronto para Vender" aparece com a barra de pesquisa

10. **Código de Pareamento Consumido** - O código é removido do administrador; gere um novo código se for necessário re-parear

**Regeneração do Código de Pareamento**: Se você precisar re-parear um terminal (redefinição do dispositivo, cache do navegador limpo, novo hardware), use a ação de administrador **Regenerar Código de Pareamento**. Isso invalida o código antigo e cria um novo.

## Monitoramento do Status do Terminal

### Sistema de Batimento Cardíaco

Os terminais enviam um sinal de batimento cardíaco ao servidor a cada **5 minutos**, contendo:
- UUID do terminal
- Carimbo de tempo atual
- Contagem de usuários online
- Carimbo de tempo da última sincronização
- Status do Service Worker

**Indicador de Status Online**:
- **Verde** - Batimento cardíaco recebido nos últimos 5 minutos (terminal online e operacional)
- **Vermelho** - Nenhum batimento cardíaco há mais de 5 minutos (terminal offline ou desconectado)
- **Cinza** - Terminal nunca pareado (nenhum batimento cardíaco recebido)

**Casos de Uso**:
- **Abertura diária**: Verifique se todos os terminais estão online antes do início das operações da loja
- **Solução de problemas**: Identifique quais terminais estão experimentando problemas de conectividade
- **Auditoria**: Verifique se os terminais estão ativos durante o horário de funcionamento

### Carimbo de Tempo do Último Batimento Cardíaco

Exibe a data e hora exatas do último batimento cardíaco. Use isso para:
- Determinar há quanto tempo um terminal está offline
- Identificar padrões (ex.: terminal vai offline todas as noites no fechamento)
- Verificar a frequência de sincronização (deve atualizar a cada ~5 minutos quando online)

## Funcionalidade de Desbloqueio Remoto

Quando um terminal se torna inoperante ou fica preso em uma tela (falha de software, problemas de tempo de sessão, travamento do navegador), use a ação de administrador **Desbloqueio Remoto**:

**Como Funciona**:
1. Selecione o terminal problemático na lista de administrador
2. Escolha **Desbloqueio Remoto** no menu de ações de administrador
3. Confirme a ação
4. O servidor envia um sinal de desbloqueio via resposta do batimento cardíaco
5. O terminal recebe o sinal no próximo ciclo de batimento cardíaco (<5 min)
6. O terminal força o logout do usuário atual e retorna à tela de login

**Quando Usar**:
- Terminal travado na tela de transação
- Funcionários não conseguem sair (botão de logout não responde)
- Sessão parece ativa, mas o terminal está inoperante
- Navegador travou, mas o cookie de sessão persiste

**Importante**: O desbloqueio remoto NÃO reinicia o dispositivo ou navegador — ele apenas força um logout e limpeza da sessão. Se o terminal estiver completamente travado, o pessoal pode precisar reiniciar manualmente o navegador ou o dispositivo.

## Editando a Configuração do Terminal

Clique em um terminal na lista para editar sua configuração:

![Formulário de Edição de Terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Seguro Alterar Enquanto o Terminal Estiver Online**:
- Nome do terminal
- Usuários atribuídos
- Configuração de hardware (toma efeito após o terminal reiniciar o aplicativo)
- Configurações de cache offline (toma efeito na próxima sincronização)

**Requer Re-Pareamento**:
- Atribuição de armazém (mudar de armazém requer re-pareamento para sincronizar o novo estoque)

**Não Pode Alterar**:
- UUID (identificador imutável)

Mudanças na maioria das configurações aplicam-se no próximo ciclo de batimento cardíaco/sincronização. Mudanças na configuração de hardware exigem que o pessoal feche e reabra o aplicativo POS (ou atualize o navegador).

## Solução de Problemas com Problemas Comuns

**Terminal Mostra "Não Autorizado" no Login**:
- Verifique se o usuário está na lista **Usuários Atribuídos** para este terminal
- Verifique se o usuário tem permissões POS em **Funcionários e Permissões > Papéis**
- Verifique se o terminal está marcado como **Ativo**

**Terminal Não Consegue Parear (Código Inválido)**:
- Códigos de pareamento expiram após o primeiro uso — gere um novo se necessário
- Códigos são sensíveis a maiúsculas e minúsculas — verifique a capitalização
- Verifique se o terminal está marcado como **Ativo**

**Terminal Mostra Offline (Ponto Vermelho)**:
- Verifique se o dispositivo tem conectividade com a internet
- Verifique se o terminal está realmente em execução (navegador aberto para o URL /pos/)
- Certifique-se de que o firewall não está bloqueando solicitações de batimento cardíaco
- Aguarde 5 minutos para o próximo ciclo de batimento cardíaco

**Terminal Lento para Sincronizar**:
- Reduza **Dias de Sincronização de Pedidos** de 30 para 7
- Reduza **Limite de Sincronização de Pedidos** de 1000 para 200
- Verifique a velocidade da rede no local do terminal
- Verifique se o servidor não está sob carga pesada

**Impressora Não Funcionando**:
- Verifique o IP e a porta da impressora em **Configuração de Hardware**
- Teste a conectividade da impressora a partir do dispositivo do terminal (ping no IP)
- Verifique se a impressora é compatível com ESC/POS
- Verifique se a impressora está ligada e online

## Dicas

- **A convenção de nomenclatura importa** - Use nomenclatura consistente (local + número) para simplificar o gerenciamento em larga escala
- **Sempre atribua armazém antes de parear** - Terminais não podem processar vendas sem atribuição de armazém
- **Teste a configuração de hardware antes de implantar** - Imprima um recibo de teste para verificar a integração da impressora/caixa registradora
- **Monitore o batimento cardíaco diariamente** - Estabeleça uma rotina para verificar se todos os terminais estão online no início das operações da loja
- **Reduza os limites de sincronização para terminais móveis** - Tablets e smartphones beneficiam-se de sync_days: 7, sync_limit: 200
- **Use o desbloqueio remoto com parcimônia** - O logout forçado interrompe transações ativas; confirme se o terminal realmente está travado antes de usá-lo
- **Documente os códigos de pareamento** - Anote o código antes de implantar o terminal no chão de loja (em caso de que a configuração leve mais tempo do que o esperado)
- **Atribua gerentes a todos os terminais** - Garante que supervisores possam acessar qualquer caixa para cancelamentos, reembolsos e solução de problemas

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.