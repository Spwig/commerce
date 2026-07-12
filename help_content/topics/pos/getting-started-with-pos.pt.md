---
title: Começando com o POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

O Spwig POS transforma qualquer tablet ou navegador em um caixa registrador completo — conectado ao seu catálogo de produtos, estoque e histórico de pedidos. Este checklist guia você desde uma instalação nova até realizar sua primeira venda. Cada etapa vincula-se a um tópico dedicado se você quiser os detalhes completos.

![Dashboard do POS](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Etapa 1: Ativar o POS para um local de loja

Os terminais POS estão vinculados a um local físico de loja. No Spwig, os locais de loja são armazéns marcados como locais de varejo.

1. Navegue até **Catálogo > Armazéns** no seu menu lateral de administração.
2. Abra o armazém que deseja usar como loja, ou crie um novo.
3. Ative o interruptor **Local de varejo** e insira um **nome de exibição do POS** (ex: "Loja da Avenida Principal"). Esse nome aparece nos recibos e no seletor de terminal.
4. Salve o armazém.

Se você tiver várias lojas ou quiser agrupá-las para relatórios regionais, crie primeiro um **Grupo de Lojas** em **POS > Grupos de Lojas**, depois atribua cada armazém a esse grupo. Os grupos de lojas permitem que você defina uma moeda, fuso horário e modelo de recibo compartilhados que todos os locais no grupo herdam.

## Etapa 2: Criar ou verificar pelo menos uma conta de funcionário com acesso ao POS

Seus funcionários logam no POS usando as mesmas credenciais que usam para o admin do Spwig. Qualquer conta de funcionário com status **Ativo** e pelo menos a permissão `pos_admin` pode acessar o POS.

Para verificar ou conceder acesso, vá até **Configurações > Gerenciamento de Funcionários**, abra a conta do funcionário e confirme se ele tem o papel de POS adequado atribuído. Não é necessário uma conta de POS separada.

## Etapa 3: Registrar seu primeiro terminal POS

Um terminal representa um único caixa ou dispositivo. Você o registra no admin, depois associa um dispositivo físico a ele usando um código de emparelhamento único.

1. Navegue até **POS > Terminais POS** e clique em **+ Adicionar Terminal POS**.
2. Dê ao terminal um nome (ex: "Caixa da Frente") e atribua-o ao local de loja que ativou na Etapa 1.
3. Salve o terminal. O Spwig gera um **código de emparelhamento de 8 caracteres** — você verá ele na página de detalhes do terminal.
4. No dispositivo que deseja usar como caixa, abra um navegador e acesse `/pos/`.
5. Insira o código de emparelhamento quando solicitado. O dispositivo agora está vinculado a este terminal.

O código de emparelhamento é de uso único. Se você precisar reemparelhar um dispositivo, abra o terminal no admin e clique em **Regenerar código de emparelhamento**.

Para opções de configuração de hardware (impressoras de recibos, leitores de código de barras, caixas registradoras), consulte [Configuração do Terminal POS](pos-terminal-setup).

## Etapa 4: Configurar um provedor de pagamento

O provedor de pagamento conecta seus leitores de cartão a uma rede de pagamento, como o Stripe Terminal ou o Square. Use o assistente de configuração de 5 etapas para inserir suas credenciais.

1. Navegue até **POS > Provedores de Pagamento** e clique em **Configurar provedor**.
2. O assistente abre em `/admin/pos/terminal-provider/wizard/step1/`.

![Assistente do Provedor de Pagamento](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Selecione seu provedor (ex: **Stripe Terminal**) e siga as instruções na tela por todas as cinco etapas: selecionar provedor → instruções de configuração → inserir credenciais → testar conexão → configurar local.
4. Um distintivo verde **Conectado** confirma que a integração está ativa.

Se você precisar apenas de dinheiro e entrada manual de cartão, selecione **Manual** como provedor — nenhuma credencial é necessária.

Para campos de credenciais detalhados para cada provedor compatível, veja [Configuração do Provedor de Pagamento POS](pos-payment-provider-setup).

## Etapa 5: Emparelhar um leitor de cartão

Com um provedor de pagamento conectado, você pode emparelhar um leitor de cartão físico a um de seus terminais usando o assistente de 3 etapas do leitor.

1. Navegue até **POS > Leitores de Cartão** e clique em **Adicionar leitor**.
2. O assistente de leitor começa em `/admin/pos/reader/wizard/step1/`.
3. Selecione seu provedor, depois escolha **Registrar novo dispositivo** (insira o código mostrado na tela do leitor) ou **Descobrir existente** (Spwig busca leitores já registrados com o provedor).
4. Na etapa final, atribua o leitor ao terminal que você criou na Etapa 3.

Cada terminal suporta um leitor de cartão atribuído. Você pode reatribuir leitores a qualquer momento da lista de Leitores de Cartão.

## Etapa 6: Projetar seu recibo (opcional para o primeiro dia)

Spwig cria um modelo de recibo padrão automaticamente. Você pode começar a vender imediatamente sem tocar nele — o padrão imprime o nome da sua loja, endereço, venda detalhada, método de pagamento e um rodapé "Obrigado pela sua compra!".

Quando estiver pronto para personalizar, vá até **POS > Modelos de Recibo**. As opções incluem seu logotipo, número de identificação fiscal, promoção de código QR, política de devolução e largura de papel (58mm ou 80mm para impressoras térmicas). Você pode criar modelos separados por loja ou por grupo de lojas.

## Etapa 7: Abrir seu primeiro turno

Turnos rastreiam quem processou as vendas e quanto dinheiro deve estar na caixa. Os caixas abrem e fecham turnos no próprio POS.

1. No dispositivo emparelhado, vá para `/pos/` e faça login com suas credenciais de funcionário.
2. Selecione o terminal e a localização da loja.
3. Spwig solicita que você **conte o saldo inicial** — insira o valor em dinheiro já presente na caixa (insira `0` se a caixa estiver vazia).
4. Toque em **Abrir Turno**. O caixa agora está pronto para vender.

Para uma explicação completa sobre turnos, movimentos de dinheiro e relatórios de reconciliação, veja [Gerenciamento de Turnos POS](pos-shifts).

## Etapa 8: Efetuar sua primeira venda

Uma vez que um turno esteja aberto, vender é direto:

1. Procure produtos pelo nome, escaneie um código de barras ou navegue por categorias para adicionar itens ao carrinho.
2. Aplique um desconto ou um código de voucher, se necessário.
3. Toque em **Cobrar** para iniciar o pagamento. Escolha o método de pagamento (dinheiro, cartão via leitor ou pagamento dividido).
4. Para pagamentos com cartão, o leitor solicita ao cliente que toque ou insira seu cartão.
5. O recibo é impresso automaticamente (ou exibe uma opção de recibo digital). O pedido é salvo no seu histórico de pedidos em tempo real.

## Etapa 9: Fechar o turno no final do dia

Fechar um turno bloqueia o caixa e gera um resumo de reconciliação.

1. No menu POS, toque em **Fechar Turno**.
2. Conte o dinheiro na caixa e insira o total quando solicitado.
3. Spwig calcula o dinheiro esperado com base no saldo inicial, vendas em dinheiro e quaisquer movimentos de dinheiro durante o turno, e mostra a diferença para você.
4. Confirme para fechar. O relatório do turno é salvo e visível em **POS > Turnos** no seu painel de administração.

Registre qualquer dinheiro removido ou adicionado à caixa durante o dia como **movimentos de dinheiro** (via menu de turno) em vez de ajustar o total de fechamento — isso mantém sua reconciliação precisa.

## Dicas

- Conclua as Etapas 1 a 5 antes do seu primeiro dia de negócios.

As Etapas 6 a 9 podem ser feitas no dia.
- Use uma senha forte, mas memorável para os funcionários — os funcionários do POS digitam suas credenciais no caixa, então senhas excessivamente complexas os atrasam.
- Se o leitor de cartão não aparecer online, clique em **Sincronizar leitores** na página de Leitores de Cartão para buscar o status mais recente do seu provedor.
- Teste o fluxo completo (abrir turno → venda → recibo → fechar turno) com uma transação de teste de $0,01 antes do período de negócios movimentado.
- O POS funciona offline para vendas básicas em dinheiro.

Pagamentos com terminal de cartão requerem uma conexão com a internet para autorizar.
- Você pode ter múltiplos terminais em uma única localização de loja — adicione um novo registro de terminal no administrador e associe-o a um dispositivo diferente.