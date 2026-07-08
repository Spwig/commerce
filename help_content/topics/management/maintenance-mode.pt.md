---
title: Modo de Manutenção
---

O modo de manutenção desativa temporariamente sua loja online e exibe uma mensagem de "voltaremos em breve" aos clientes. Seu backend de administração permanece totalmente acessível durante a manutenção — você pode continuar trabalhando enquanto os clientes ficam na página de manutenção.

Use o modo de manutenção antes de fazer alterações que possam causar um estado temporariamente inconsistente, como executar uma importação de produtos grande, aplicar uma redesign de tema importante ou aguardar a conclusão de uma operação de restauração.

![Comutador de modo de manutenção no painel do sistema](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Ativar o modo de manutenção

1. Navegue até **Gerenciamento > Métricas do Sistema**
2. Clique em **Painel do Sistema** na barra de ferramentas
3. No painel **Status da Loja**, clique em **Ativar Modo de Manutenção**
4. Opcionalmente, insira um **Motivo** — isso é apenas para sua referência e não é exibido aos clientes (ex: `Atualização do catálogo de produtos em andamento`)
5. Confirme clicando em **Ativar**

Sua loja online começa imediatamente a mostrar a página de manutenção para todos os visitantes. O backend de administração não é afetado e você pode continuar trabalhando normalmente.

## O que os clientes veem

Quando o modo de manutenção está ativo, todas as páginas da sua loja online (a loja, páginas de produtos, checkout e páginas de conta) exibem uma notificação de manutenção com marcação. A mensagem informa aos clientes que a loja está temporariamente indisponível e os encoraja a voltarem em breve.

Clientes que estiverem no meio de uma sessão ou no meio do checkout no momento em que o modo de manutenção for ativado também verão a página de manutenção na próxima solicitação. Nenhuma ordem em andamento será perdida — os dados ainda estarão disponíveis quando você desativar o modo de manutenção.

## Desativar o modo de manutenção

1. Navegue até **Gerenciamento > Métricas do Sistema**
2. Clique em **Painel do Sistema**
3. No painel **Status da Loja**, você verá um banner confirmando que o modo de manutenção está ativo
4. Clique em **Desativar Modo de Manutenção**
5. Confirme quando solicitado

A loja online volta online imediatamente. Os clientes podem navegar e comprar normalmente.

## Quando o Spwig ativa o modo de manutenção automaticamente

Certas operações do sistema ativam o modo de manutenção automaticamente e reativam a loja quando terminam:

- **Atualizações da plataforma** — o processo de atualização ativa o modo de manutenção antes de aplicar alterações e o desativa quando a atualização estiver completa
- **Operações de restauração** — restaurar a partir de um backup coloca a loja em modo de manutenção durante a duração da restauração

Se uma operação automatizada terminar inesperadamente, o modo de manutenção pode permanecer ativo. Nesse caso, siga as etapas acima para desativá-lo manualmente.

## Dicas

- Sempre informe sua equipe antes de ativar o modo de manutenção — ele afeta todos os visitantes da sua loja online
- Mantenha os períodos de manutenção tão curtos quanto possível; mesmo alguns minutos offline podem afetar a confiança dos clientes
- Use o campo de motivo como um lembrete para você sobre o motivo pelo qual o modo de manutenção foi ativado — ele aparece no log do sistema
- Se você notar que o modo de manutenção está ativo, mas não o ativou pessoalmente, verifique o log do sistema para operações automatizadas que possam tê-lo ativado
- Planeje os períodos de manutenção durante horários de baixa demanda (noites ou madrugadas) para minimizar o impacto nas vendas