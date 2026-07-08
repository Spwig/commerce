---
title: Descontos para Pessoal do POS e Segurança do Terminal
---

As configurações de descontos para o pessoal do POS permitem que você controle quanto de desconto cada membro da equipe pode aplicar no momento da venda. Os eventos de bloqueio do terminal fornecem um rastro de auditoria de cada vez que um terminal foi bloqueado ou desbloqueado — ajudando você a acompanhar quem acessou o terminal e se houve tentativas de login falhas.

## Limites de desconto do pessoal

Cada membro da equipe que usa o POS pode ter permissões de desconto individuais. Por padrão, o pessoal pode aplicar até 10% de desconto em itens ou no carrinho inteiro. Você pode aumentar ou diminuir esse limite por pessoa, ou designar membros da equipe como gerentes que podem aprovar descontos que excedam os limites padrão.

### Configurando o limite de desconto de um membro da equipe

1. Navegue até **POS > Descontos para Pessoal**
2. Clique em **+ Adicionar Desconto para Pessoal do POS** ou clique em um membro da equipe existente para editar
3. Selecione o **Membro da Equipe** da lista
4. Defina os limites de desconto:

| Campo | Descrição |
|-------|-------------|
| **Máximo de Desconto %** | Percentual máximo de desconto que essa pessoa pode aplicar (ex: `10` para 10%) |
| **Máximo de Valor de Desconto** | Valor fixo máximo por transação (deixe em branco para não haver limite fixo) |
| **Pode Aplicar Descontos em Itens** | Permitir desconto em itens individuais |
| **Pode Aplicar Descontos no Carrinho** | Permitir desconto no total do carrinho |
| **Requer Motivo** | Quando marcado, o membro da equipe deve digitar um motivo antes de aplicar qualquer desconto |

5. Clique em **Salvar**

### Como os limites de desconto funcionam no POS

Quando um caixa tenta aplicar um desconto:
- Se o desconto estiver dentro do seu limite, ele é aplicado imediatamente
- Se o desconto exceder seu limite, o terminal solicitará **aprovação de gerente**
- Um gerente digita seu PIN para autorizar a alteração, e o desconto é aplicado

Esse fluxo de trabalho impede descontos de alto valor não autorizados, enquanto permite flexibilidade quando descontos reais forem necessários.

## Papel de gerente

Membros da equipe com a bandeira **É Gerente** podem aprovar descontos que excedam os limites de outros membros da equipe. Os gerentes são identificados no terminal por um PIN que eles digitam quando uma aprovação é solicitada.

### Configurando um gerente

1. Abra o registro de desconto de um membro da equipe
2. Marque **É Gerente**
3. Digite um **PIN do Gerente** (4-6 dígitos) — esse PIN é criptografado com segurança ao ser salvo
4. Clique em **Salvar**

O PIN do gerente é separado do PIN do caixa usado para bloqueio/desbloqueio do terminal. Um gerente pode ter tanto um PIN do gerente (para aprovação de descontos) quanto um PIN do caixa (para acesso ao terminal).

### Segurança do PIN do Gerente

Quando você digita um PIN no formulário de administração e salva, o Spwig o criptografa automaticamente — o PIN em texto plano nunca é armazenado. O campo do PIN em texto plano limpa após o salvamento, o que é um comportamento esperado.

## PINs de caixa e acesso por cartão

Cada membro da equipe também pode ter um **PIN de Caixa** para bloquear e desbloquear o terminal:

- **PIN de Caixa** — PIN de 4 a 6 dígitos usado para desbloquear o terminal após ele se bloquear automaticamente ou ser bloqueado manualmente
- **Identificador de Cartão** — Um cartão registrado (cartão de swipe ou NFC) também pode ser usado para desbloquear o terminal

Para configurar um PIN de caixa, digite-o no campo **PIN de Caixa** e salve. Assim como o PIN do gerente, ele é criptografado automaticamente ao ser salvo.

## Eventos de bloqueio do terminal

Cada vez que um terminal é bloqueado ou desbloqueado, o Spwig registra um evento de bloqueio do terminal. Isso cria um rastro de auditoria de segurança completo.

### Visualizando eventos de bloqueio

Navegue até **POS > Eventos de Bloqueio do Terminal** para ver o histórico completo. Você pode filtrar eventos por:
- Terminal
- Tipo de evento
- Faixa de datas

### Tipos de eventos

| Evento | Significado |
|-------|---------|
| **Bloqueio Manual** | Um membro da equipe bloqueou deliberadamente o terminal |
| **Bloqueio Automático (Tempo de Inatividade)** | O terminal foi bloqueado automaticamente devido à inatividade |
| **Desbloqueio pelo Caixa** | O caixa autenticou-se e desbloqueou o terminal |
| **Desbloqueio pelo Gerente** | Um gerente usou suas credenciais para desbloquear |
| **Desbloqueio pela Carteira** | O terminal foi desbloqueado usando uma carteira registrada |
| **Desbloqueio por Biométrica** | O terminal foi desbloqueado usando impressão digital ou reconhecimento facial |
| **Tentativa de Desbloqueio Falhada** | Uma tentativa de desbloqueio foi feita com credenciais incorretas |
| **Bloqueio (3+ falhas)** | O terminal foi bloqueado após tentativas repetidas de falha |

### O que os registros de eventos de bloqueio contêm

Cada evento registra:
- O **Terminal** envolvido
- O **Tipo de Evento**
- Quem realizou a ação (**Realizado Por**) e quem estava logado quando o bloqueio ocorreu (**Bloqueado Por**)
- Se um **Sobrescrita por Gerente** foi usada
- O **Método de Desbloqueio** (PIN, cartão ou biométrico)
- **Tentativas Falhadas** antes deste evento (útil para identificar padrões de força bruta)
- O **Total do Carrinho** e a quantidade de itens no momento do evento
- O endereço IP da solicitação

### Investigando uma preocupação de segurança

Se você suspeitar de acesso não autorizado a um terminal:

1. Navegue até **POS > Eventos de Bloqueio do Terminal**
2. Filtrar pelo terminal em questão
3. Procure eventos do tipo **Tentativa de Desbloqueio Falhada** ou **Bloqueio** — esses indicam acesso repetido falhado
4. Verifique o campo **Realizado Por** em desbloqueios bem-sucedidos para ver quem obteve acesso
5. Cancele com os registros de turno (**POS > Turnos**) para verificar o caixa que deveria estar de serviço

## Dicas

- Defina limites de desconto com base na senioridade da equipe — funcionários novos podem começar com 5%, funcionários experientes com 10-15%, e gerentes podem aprovar qualquer valor mais alto.
- Ative **Requer Motivo** para qualquer funcionário com limites de desconto mais altos. Ter um motivo registrado ajuda você a analisar padrões de desconto e identificar qualquer uso indevido.
- Revise os eventos de bloqueio do terminal semanalmente se sua loja tiver múltiplos funcionários ou alta rotatividade de funcionários — padrões de acesso irregulares são mais fáceis de identificar antes que se tornem um problema.
- Se um funcionário sair, remova imediatamente seu PIN de caixa e identificador de cartão para impedir o acesso ao terminal.
- Use o evento de bloqueio para identificar terminais que podem precisar de seu tempo de bloqueio automático ajustado — se os clientes estiverem frequentemente acionando bloqueios acidentais, o tempo de inatividade pode estar configurado muito curto.
- Os PINs de gerente devem ser alterados periodicamente. Atualize-os no registro de desconto da equipe — o novo PIN é criptografado ao salvar.