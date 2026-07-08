---
title: Gerenciamento de Turnos POS e Caixa
---

Turnos POS rastreiam períodos de trabalho de caixas e garantem uma contabilidade precisa do caixa. Cada turno representa o tempo de um caixa em um terminal — desde abrir o caixa com um valor inicial de dinheiro até encerrar o turno com um valor final e reconciliação. O sistema calcula automaticamente o valor esperado de dinheiro com base nas vendas reais e compara com a contagem física, destacando discrepâncias para investigação. Movimentos de dinheiro durante os turnos (adições de dinheiro, saques de numerário) são rastreados com razões para garantir um histórico completo de auditoria.

Navegue até **POS > Turnos** para visualizar todos os turnos, monitorar turnos ativos, revisar relatórios de reconciliação de caixa e auditar atividades históricas.

![Lista de Turnos](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Entendendo Turnos POS

Um turno é um período de trabalho durante o qual um caixa opera um terminal. Os turnos garantem a responsabilidade pelo dinheiro — cada caixa é responsável pelo dinheiro em seu caixa durante seu turno.

**Ciclo de Vida do Turno**:
1. **Abertura** - O caixa inicia o turno, conta o dinheiro inicial e registra o valor
2. **Durante o Turno** - Processa vendas, aceita pagamentos, emite reembolsos
3. **Encerramento** - O caixa conta o dinheiro, registra o valor final, o sistema calcula a discrepância
4. **Reconciliado** - O turno é finalizado e bloqueado para fins de auditoria

**Métricas Principais Rastreadas**:
- **Dinheiro Inicial** - Valor inicial de dinheiro no caixa no início do turno
- **Dinheiro Final** - Dinheiro físico no caixa no final do turno
- **Dinheiro Esperado** - Calculado: Dinheiro inicial + vendas em dinheiro - reembolsos em dinheiro + movimentos de dinheiro
- **Diferença de Dinheiro** - Discrepância: Dinheiro final - dinheiro esperado (positivo = excesso, negativo = falta)
- **Total de Vendas** - Soma de todas as transações de venda durante o turno
- **Total de Reembolsos** - Soma de todas as transações de reembolso durante o turno
- **Contagem de Transações** - Número de pedidos processados

## Visão da Lista de Turnos

A lista de turnos exibe todos os turnos com informações-chave:

**Status do Turno**:
- **Aberto** (badge verde) - Turno ativo atualmente
- **Fechado** (badge cinza) - Turno concluído
- **Reconciliado** (badge azul) - Finalizado e bloqueado para auditoria

**Terminal** - Qual terminal POS o turno estava

**Caixa** - Funcionário que trabalhou o turno

**Dinheiro Inicial** - Valor inicial de dinheiro

**Dinheiro Final** - Valor final de dinheiro (em branco se o turno ainda estiver aberto)

**Dinheiro Esperado** - Valor esperado calculado pelo sistema com base nas transações

**Diferença de Dinheiro** - Discrepância (destacada em vermelho se negativa, verde se positiva, preto se zero)

**Duração** - Duração do turno (tempo de início ao tempo de término)

**Total de Vendas** - Receita gerada durante o turno

Use filtros para visualizar:
- Apenas turnos abertos (monitorar terminais ativos)
- Turnos com discrepâncias (diferença de dinheiro ≠ 0)
- Turnos por intervalo de data (relatórios de reconciliação diária)
- Turnos por caixa (auditoria de desempenho)

## Abrindo um Turno

Os caixas abrem turnos diretamente a partir do terminal POS (não pode ser aberto a partir do admin). O fluxo de trabalho no terminal:

1. **Funcionário Faz Login** - Insere credenciais para acessar o terminal

2. **Contar o Dinheiro Inicial** - Conta fisicamente todo o dinheiro no caixa (notas e moedas)

3. **Inserir o Valor Inicial** - Registra o valor contado no aplicativo POS

4. **Turno Inicia** - O terminal está pronto para processar vendas

**Diretrizes para Dinheiro Inicial**:
- O dinheiro inicial padrão (flutuante) é tipicamente de $100-$300 dependendo do tamanho da loja
- Conte duas vezes para garantir precisão — erros na abertura se propagam para discrepâncias no encerramento
- Se o caixa estiver vazio, o dinheiro inicial é $0.00 (dinheiro adicionado via movimento de dinheiro)
- Documente notas de alto valor (> $50) separadamente para rastrear seu movimento

![Formulário de Adição de Turno](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Durante o Turno

Enquanto o turno está aberto, o sistema rastreia automaticamente:

**Vendas em Dinheiro** - Qualquer transação em que o cliente paga com dinheiro físico (adiciona ao dinheiro esperado)

**Reembolsos em Dinheiro** - Qualquer reembolso emitido em dinheiro (subtrai do dinheiro esperado)

**Vendas com Cartão** - Transações com cartões de crédito/débito (sem impacto no dinheiro)

**Pagamento Dividido** - Dinheiro parcial + cartão parcial (apenas a parte em dinheiro afeta o dinheiro esperado)

**Cartões-presente e Cupons** - Métodos de pagamento não em dinheiro (sem impacto no dinheiro)

Os caixas continuam processando vendas normalmente. O sistema mantém um cálculo contínuo do dinheiro esperado em segundo plano.

## Movimentos de Dinheiro

Movimentos de dinheiro são ajustes no caixa durante um turno:

**Adições de Flutuante** - Adicionar dinheiro ao caixa:
- Motivo: "Adicionar troco para notas de alto valor"
- Valor: +$100.00
- O dinheiro esperado aumenta em $100.00

**Retiradas de Numerário** - Remover dinheiro para despesas:
- Motivo: "Compra de materiais de escritório"
- Valor: -$25.00
- O dinheiro esperado diminui em $25.00

**Depósitos Bancários** - Remover dinheiro excessivo para segurança:
- Motivo: "Depósito seguro - mais de $500 no caixa"
- Valor: -$300.00
- O dinheiro esperado diminui em $300.00

**Registrar Movimentos de Dinheiro no Terminal**:
1. Toque em **Menu** > **Movimento de Dinheiro**
2. Selecione o tipo: Adicionar ou Remover
3. Insira o valor
4. Insira o motivo (requerido para o histórico de auditoria)
5. Confirme

Todos os movimentos de dinheiro aparecem no relatório de detalhes do turno com timestamps, valores e razões.

## Encerrando um Turno

Quando um caixa termina seu período de trabalho, ele encerra o turno:

1. **Toque em Encerrar Turno** - No menu do terminal

2. **Processar Transações Restantes** - Concluir qualquer carrinho parado ou vendas pendentes

3. **Contar o Dinheiro Final** - Contar fisicamente todo o dinheiro no caixa
   - Contar notas por denominação ($100s, $50s, $20s, $10s, $5s, $1s)
   - Contar moedas por tipo (quarters, dimes, nickels, pennies)
   - Total = valor final do dinheiro

4. **Inserir o Valor Final** - Registrar o total contado

5. **Sistema Calcula a Discrepância**:
   - Dinheiro esperado = Dinheiro inicial + vendas em dinheiro - reembolsos em dinheiro + movimentos de dinheiro
   - Diferença de dinheiro = Dinheiro final - dinheiro esperado
   - Exemplo: Dinheiro final $485.00 - Esperado $480.00 = +$5.00 excesso

6. **Revisar a Discrepância** - O terminal exibe a diferença:
   - **Exato ($0.00)** - Reconciliação perfeita
   - **Excesso pequeno (+$1 a +$5)** - Arredondamento aceitável ou gorjeta do cliente
   - **Falta pequena (-$1 a -$5)** - Erro de contagem menor, aceitável
   - **Discrepância grande (>$5)** - Recontagem necessária

7. **Recontar se necessário** - Se a discrepância for grande (>$10), o caixa deve recontar o dinheiro final antes de finalizar

8. **Finalizar o Turno** - Confirmar o valor final, o status do turno muda para "Fechado"

9. **Imprimir Relatório do Turno** - O terminal imprime um recibo de reconciliação de dinheiro para os registros do caixa

![Detalhes do Turno](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Fórmula de Reconciliação de Dinheiro

O sistema calcula o dinheiro esperado usando esta fórmula:

```
Dinheiro Esperado = Dinheiro Inicial
                + Vendas em Dinheiro
                - Reembolsos em Dinheiro
                + Adições de Dinheiro (movimentos)
                - Remoções de Dinheiro (movimentos)
```

**Exemplo**:
- Dinheiro Inicial: $200.00
- Vendas em Dinheiro: $450.00 (de 15 transações)
- Reembolsos em Dinheiro: -$30.00 (1 devolução)
- Adição de Dinheiro: +$100.00 (dinheiro adicionado durante o turno)
- Remoção de Dinheiro: -$50.00 (saque de numerário)
- **Dinheiro Esperado: $200 + $450 - $30 + $100 - $50 = $670.00**

Se o caixa contar $675.00 no encerramento:
- Diferença de Dinheiro: $675.00 - $670.00 = **+$5.00 excesso**

## Relatórios e Auditoria de Turnos

Relatórios de turnos fornecem informações detalhadas de reconciliação:

**Seção de Resumo**:
- Dinheiro inicial e final
- Cálculo do dinheiro esperado
- Diferença de dinheiro (excesso/falta)
- Total de vendas e reembolsos
- Contagem de transações
- Duração do turno

**Detalhes da Transação**:
- Todas as vendas durante o turno (IDs de pedidos, valores, métodos de pagamento)
- Todos os reembolsos emitidos
- Timestamp de cada transação

**Log de Movimentos de Dinheiro**:
- Todas as adições e remoções
- Motivos fornecidos
- Timestamps

**Casos de Uso**:
- **Reconciliação diária** - Revisar todos os turnos no final do dia comercial
- **Desempenho do caixa** - Identificar padrões de discrepâncias por funcionário
- **Detecção de roubo** - Falta grande e consistente pode indicar roubo
- **Necessidade de treinamento** - Discrepâncias frequentes pequenas sugerem problemas de precisão na contagem
- **Histórico de auditoria** - Registro completo para fins contábeis e fiscais

## Gerenciamento de Caixa com Múltiplos Terminais

Para lojas com múltiplos terminais executando turnos simultâneos:

**Caixas Separados**: Cada terminal tem seu próprio caixa — os turnos são independentes. O caixa A no Terminal 1 e o caixa B no Terminal 2 executam turnos separados com reconciliação separada.

**Caixa Compartilhado**: Algumas lojas compartilham um único caixa entre múltiplos terminais (não recomendado). Se fizerem isso:
- Apenas um turno pode estar aberto por caixa compartilhado de cada vez
- Os caixas devem encerrar o turno ao passar para o próximo caixa
- Movimentos de dinheiro rastreiam todas as adições/remoções durante as transferências
- Discrepâncias são mais difíceis de atribuir a caixas específicos

**Melhor Prática**: Um caixa por terminal, um turno por caixa por sessão. Isso garante responsabilidade clara e reconciliação simplificada.

## Lidando com Discrepâncias

Quando o dinheiro fechado não corresponde ao dinheiro esperado:

**Discrepâncias Pequenas (<$5)**:
- Aceitáveis devido a arredondamento, erros de contagem ou gorjetas do cliente
- Documente nos comentários do turno
- Nenhuma ação adicional necessária, a menos que um padrão emerge

**Discrepâncias Médias ($5-$20)**:
- Reconte o dinheiro antes de finalizar o turno
- Revise o log de transações para erros (troco incorreto fornecido, transação cancelada não processada)
- Documente as circunstâncias nos comentários do turno
- Recomendado revisão por gerente

**Discrepâncias Grandes (>$20)**:
- Recontagem obrigatória
- Aprovação do gerente necessária para encerrar o turno
- Revise todas as transações e movimentos de dinheiro
- Investigue possíveis causas (roubo, toque no caixa, dinheiro inicial incorreto)
- Pode exigir ação disciplinar dependendo das circunstâncias

**Faltas Consistentes**:
- Padrão de discrepâncias negativas do mesmo caixa = problema de treinamento ou roubo
- Implemente supervisão adicional (verificação aleatória do gerente durante o turno)
- Revise os procedimentos de treinamento do POS
- Considere atualizações nas políticas de manipulação de dinheiro

## Dicas

- **Conte o dinheiro inicial duas vezes** - Erros na abertura se propagam para discrepâncias no encerramento; precisão no início evita problemas no final
- **Registre movimentos de dinheiro imediatamente** - Não espere até o encerramento para documentar adições de flutuante ou saques de numerário
- **Sempre forneça razões para os movimentos** - "Adicionado $100" é inútil para auditoria; "Adicionado $100 para troco (falta de notas de $5)" é açãoável
- **Reconte se a discrepância for >$10** - Não finalize o turno com uma discrepância grande sem recontagem
- **Imprima relatórios de turnos diariamente** - Anexe aos documentos de reconciliação diária para contabilidade
- **Revise padrões, não discrepâncias individuais** - Uma falta de -$3.00 é aceitável; cinco faltas consecutivas de -$3.00 é um problema
- **Feche os turnos no final do dia** - Não deixe os turnos abertos durante a noite; discrepâncias são mais fáceis de investigar quando recentes
- **Treine os caixas na contagem por denominação** - A maioria dos erros vem de contagem incorreta de notas (pensar que uma nota de $5 é uma de $10)
- **Use embalagens para moedas** - Moedas pré-embaladas reduzem erros de contagem e aceleram a reconciliação