---
title: Configuração do Display do Cliente
---

Um display do cliente é uma segunda tela que é voltada para o cliente durante uma venda. Enquanto você processa a transação, o cliente vê cada item conforme é escaneado, o subtotal em andamento, a quebra de preço e impostos, e — quando nenhuma venda está em andamento — um carrossel de slides promocionais do seu conteúdo."
    },
    {
      "type": "paragraph",
      "content": "Este guia abrange o lado de hardware e emparelhamento da configuração do seu display do cliente: habilitar o recurso em um terminal, emparelhar um dispositivo separado como tela de exibição e lidar com cenários comuns de configuração. Para informações sobre os slides promocionais exibidos durante os períodos ociosos, consulte [Slides Promocionais do Display do Cliente](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "O que o display do cliente mostra"
    },
    {
      "type": "paragraph",
      "content": "Quando uma venda está ativa, o display do cliente mostra:"
    },
    {
      "type": "list",
      "content": [
        "Cada item conforme é adicionado ou removido, com quantidade e preço",
        "O subtotal do carrinho, quaisquer descontos aplicados e a quebra de impostos",
        "O total devido e, durante o pagamento, o valor oferecido e o troco"
      ]
    },
    {
      "type": "paragraph",
      "content": "Quando o terminal está ocioso (sem transação ativa), o display muda para um carrossel promocional. Você controla o conteúdo desse carrossel separadamente — consulte [Slides Promocionais do Display do Cliente](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Configurações de hardware comuns"
    },
    {
      "type": "paragraph",
      "content": "Há três maneiras práticas de configurar uma tela voltada para o cliente:"
    },
    {
      "type": "list",
      "content": [
        "**Tablet ou monitor separado em um suporte** — a configuração mais comum para vendas no balcão. Um pequeno tablet apoiado em um suporte está voltado para o cliente enquanto seu terminal principal está voltado para você. Você emparelha os dois dispositivos usando um código de curta duração (descrito abaixo).",
        "**Segundo monitor em modo de desktop estendido** — se seu terminal principal for um laptop ou desktop, conecte um segundo monitor, estenda seu desktop para ele, depois arraste a janela do display para o segundo monitor e maximize-a. Ambas as telas funcionam no mesmo dispositivo; nenhum código de emparelhamento é necessário.",
        "**Display dedicado em coluna** — uma unidade de exibição de hardware montada em uma coluna, normalmente conectada ao terminal do balcão via USB ou posicionada no balcão. Abra `/pos/display/` no navegador do dispositivo da coluna e emparelhe-o usando o código do terminal principal."
      ]
    },
    {
      "type": "heading",
      "content": "Habilitando o display do cliente em um terminal"
    },
    {
      "type": "paragraph",
      "content": "O recurso de display do cliente é habilitado por terminal através da configuração de hardware do terminal."
    },
    {
      "type": "list",
      "content": [
        "Navegue até **POS > Terminais** e abra o terminal que deseja configurar (ou clique em **+ Adicionar Terminal POS** para um novo um).",
        "Clique na guia **Dispositivo**.",
        "Role até o cartão **Configuração de Hardware**. Você verá um campo JSON.",
        "Adicione `"customer_display": true` ao objeto JSON. Por exemplo:"
      ]
    },
    {
      "type": "code-block",
      "content": "{'customer_display': true}"
    },
    {
      "type": "paragraph",
      "content": "Se o campo já contém outras configurações de hardware (como configuração de impressora ou scanner), adicione `"customer_display": true` junto com elas:"
    },
    {
      "type": "code-block",
      "content": "{'printer': 'HP LaserJet', 'scanner': 'Datalogic', 'customer_display': true}"
    },
    {
      "type": "list",
      "content": [
        "Clique em **Salvar**."
      ]
    },
    {
      "type": "image",
      "content": "![Configuração de hardware do terminal com customer_display habilitado](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)"
    },
    {
      "type": "paragraph",
      "content": "Depois de habilitado, o aplicativo POS nesse terminal abrirá a visualização do display do cliente em uma segunda janela ou aba do navegador quando uma sessão começar."
    },
    {
      "type": "heading",
      "content": "Emparelhar um dispositivo separado como o display"
    },
    {
      "type": "paragraph",
      "content": "Se você estiver usando um dispositivo físico separado para a tela do cliente (um tablet, telefone ou segundo computador), emparelhe-o ao terminal usando um código de 6 dígitos de curta duração."
    },
    {
      "type": "heading",
      "content": "Etapa 1: Gerar um código de emparelhamento no terminal principal

Abra o aplicativo POS no seu terminal principal e vá para as configurações de exibição ou seção de emparelhamento da interface do terminal.

Solicite um novo código de emparelhamento de exibição.

O código é um número de 6 dígitos e é válido por **5 minutos**.

Ao gerar um novo código, quaisquer códigos anteriores não utilizados para este terminal são automaticamente cancelados.

### Etapa 2: Abra a URL da exibição no dispositivo do cliente

No dispositivo voltado para o cliente, abra um navegador da web e acesse:

```
https://your-store-domain.com/pos/display/
```

Nenhuma autenticação é necessária — a página de exibição está publicamente acessível. Isso é intencional: o dispositivo de exibição não precisa de credenciais de funcionários, e o código de emparelhamento fornece o link entre a exibição e o terminal correto.

![Visão de exibição do cliente em estado inativo](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Etapa 3: Insira o código de emparelhamento

No dispositivo do cliente, insira o código de 6 dígitos do terminal principal. A exibição será emparelhada com esse terminal e começará a mostrar dados do carrinho em tempo real.

Uma vez usado, o código é imediatamente invalidado e não pode ser reutilizado.

## Regenerar um código de emparelhamento

Se o código de emparelhamento expirar antes que você possa inseri-lo, ou se você precisar reemparar o dispositivo de exibição (por exemplo, se um dispositivo de exibição for substituído ou redefinido), gere um novo código a partir do aplicativo POS no terminal principal.

Gerar um novo código cancela automaticamente qualquer código existente não utilizado para esse terminal. O novo código é válido por 5 minutos.

Você não precisa alterar nada no administrador para regenerar um código — isso é feito totalmente dentro do aplicativo POS.

## Configuração de múltiplas telas em um único dispositivo

Se seu terminal principal for um laptop ou um desktop com duas telas:

1. Conecte a segunda tela e defina-a para **modo de desktop estendido** nas configurações de exibição do seu sistema operacional (não em modo de espelhamento).
2. Abra o aplicativo POS na tela principal como de costume.
3. O aplicativo POS abrirá a exibição do cliente em uma segunda janela. Arraste essa janela para a segunda tela.
4. Maximizar ou ir para tela cheia na segunda tela.

Nenhum código de emparelhamento é necessário, pois ambas as janelas estão rodando no mesmo dispositivo e se comunicam diretamente.

## Comportamento em estado inativo

Quando não há venda ativa, a exibição do cliente mostra um carrossel de imagens promocionais em rotação. Você cria e gerencia esses slides separadamente em **POS > Slides Promocionais**.

Para detalhes sobre a criação de slides, direcionamento para lojas específicas e gerenciamento de conteúdo sazonal, consulte [Slides Promocionais da Exibição do Cliente](customer-display-promo-slides).

Se nenhum slide estiver configurado, a exibição mostrará uma tela de boas-vindas simples com o nome da sua loja.

## Solução de problemas

**A exibição ficou em branco ou parou de atualizar**

A exibição se comunica com o terminal principal em tempo real. Se a conexão for interrompida, a exibição pode ficar em branco ou mostrar dados desatualizados. Recarregue o navegador no dispositivo do cliente. Se isso não resolver, gere um novo código de emparelhamento e reempare o dispositivo.

**A exibição está mostrando o carrinho de um terminal errado**

Cada exibição está emparelhada com um terminal específico. Se você tiver múltiplos terminais, certifique-se de que gerou o código de emparelhamento no terminal correto e o inseriu na exibição. Para corrigir uma discordância, gere um novo código no terminal correto e reempare o dispositivo de exibição.

**O código de emparelhamento expirou antes que eu pudesse inseri-lo**

Os códigos são válidos por 5 minutos. Gere um novo código a partir do aplicativo POS e insira-o no dispositivo de exibição com urgência. Mantenha os dois dispositivos próximos durante o processo de emparelhamento.

**O código de emparelhamento foi inserido, mas a exibição não se conectou**

Verifique se o dispositivo do cliente pode acessar o domínio da sua loja (ele precisa de acesso à rede). Além disso, verifique se `"customer_display": true` está definido na configuração de hardware do terminal e que o terminal foi salvo.

**A URL da exibição retorna um erro**

Certifique-se de que você está navegando para `/pos/display/` no domínio da sua loja, e não na URL do administrador. A visualização da exibição não requer login — se você estiver sendo solicitado a fazer login, verifique novamente a URL.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- **Mantenha a sessão de emparelhamento curta** — tenha o dispositivo do cliente pronto e o navegador aberto em `/pos/display/` antes de gerar o código de emparelhamento.

Você tem 5 minutos, mas concluir isso em menos de um minuto evita o tempo limite.
- **Teste antes de abrir** — conclua uma venda de teste com o display conectado para verificar se os clientes verão os itens e totais corretos antes da sua primeira transação real.
- **Adicione um favorito ao URL do display** — configure o navegador do dispositivo do cliente para abrir `/pos/display/` ao iniciar, para que ele sempre esteja pronto.
- **Use o modo de desktop estendido para simplicidade** — se o seu terminal tiver uma porta HDMI extra e uma tela disponível, o método de desktop estendido não requer emparelhamento contínuo e nunca expira.
- **Adicione slides promocionais antes de abrir** — um display ocioso que mostra apenas uma tela de boas-vindas em branco é uma oportunidade perdida.

Configure pelo menos alguns slides promocionais para que o display seja útil mesmo quando nenhuma venda estiver em andamento.

Veja [Slides Promocionais do Display do Cliente](customer-display-promo-slides).
- **Proteja o dispositivo do display** — o URL do display é acessível publicamente por design, mas ele só mostra dados do carrinho ativo quando emparelhado a um terminal ativo.

Mesmo assim, considere usar o modo de navegador de kiosco no dispositivo do cliente para impedir que os clientes naveguem para outros lugares.