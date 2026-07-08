---
title: Modelos de SMS
---

Modelos de SMS controlam o texto de todas as notificações que sua loja envia aos clientes por meio de mensagens de texto. Cada modelo corresponde a um evento específico — como uma confirmação de pedido ou uma atualização de envio — e usa variáveis de espaço reservado que o Spwig substitui pelos detalhes reais do pedido quando a mensagem é enviada.

Navegue até **Sistema de SMS > Modelos de SMS** para visualizar e editar seus modelos.

![Lista de modelos de SMS](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Tipos de modelo disponíveis

O Spwig inclui os seguintes tipos de modelo pré-instalados:

| Tipo de Modelo | Quando é enviado |
|---------------|-----------------|
| Confirmação de Pedido | Quando um cliente faz um pedido |
| Atualização de Envio | Quando o status de rastreamento de um pedido muda |
| Notificação de Entrega | Quando um pedido é marcado como entregue |
| Redefinição de Senha | Quando um cliente solicita a redefinição de senha |
| Código de Verificação | Quando um código de uso único é necessário para a verificação da conta |
| Recibo POS | Quando uma venda é processada em um terminal de ponto de venda |
| Marketing | Para campanhas promocionais (requer consentimento separado) |
| Personalizado | Para qualquer outra notificação que você criar |

## Editando um modelo

1. Navegue até **Sistema de SMS > Modelos de SMS**
2. Clique no modelo que deseja editar
3. Atualize o campo **Mensagem** com o texto desejado
4. Use espaços reservados `{variável}` para incluir informações específicas do pedido (veja as variáveis abaixo)
5. Marque **Ativo** para habilitar o modelo — modelos inativos não são enviados
6. Clique em **Salvar**

![Editando um modelo de SMS](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Usando variáveis

Variáveis são espaços reservados escritos entre chaves — por exemplo, `{nome}` ou `{número_do_pedido}`. Quando o Spwig envia a mensagem, ele substitui cada espaço reservado pelo valor real para esse cliente ou pedido.

### Variáveis comuns

| Variável | Substituído por |
|----------|---------------|
| `{nome}` | O nome do cliente |
| `{número_do_pedido}` | O número de referência do pedido |
| `{total}` | O valor total do pedido |
| `{número_de_rastreamento}` | O número de rastreamento do envio |
| `{nome_da_loja}` | O nome da sua loja |
| `{código}` | Um código de verificação ou redefinição de senha |

**Exemplo de mensagem:**

```
Olá {nome}, seu pedido #{número_do_pedido} foi confirmado. Total: {total}. Nós o atualizaremos quando for enviado. - {nome_da_loja}
```

Quando enviado, isso se torna:

```
Olá Sarah, seu pedido #10045 foi confirmado. Total: $89,00. Nós o atualizaremos quando for enviado. - The Garden Shop
```

> Inclua apenas variáveis disponíveis para um tipo de modelo específico. Por exemplo, `{número_de_rastreamento}` está disponível em um modelo de Atualização de Envio, mas não em um modelo de Redefinição de Senha. Se você usar uma variável indisponível, ela aparecerá como está (sem substituição) na mensagem.

## Limites de caracteres e comprimento da mensagem

Mensagens de SMS padrão são limitadas a **160 caracteres** para um único segmento. Mensagens mais longas são divididas em vários segmentos e enviadas como uma (SMS concatenado), mas os operadores contam cada segmento separadamente para fins de cobrança.

**Dicas para permanecer dentro do limite:**
- Mantenha as mensagens concisas — uma finalidade por mensagem
- Abrevie frases comuns onde natural (ex: "Ord" em vez de "Order")
- Evite palavras desnecessárias

O Spwig não impõe um limite rígido de caracteres no editor, portanto, conte seus caracteres (incluindo os valores das variáveis) antes de salvar.

## Ativar e desativar modelos

O interruptor **Ativo** em cada modelo controla se esse tipo de notificação é enviado. Se um modelo estiver inativo, o Spwig pulará o envio dessa notificação totalmente — a mensagem aparecerá como **Pulada** na Caixa de Saída de SMS com a razão `template_inactive`.

Para ativar um modelo:
1. Abra o modelo
2. Marque a caixa **Ativo**
3. Salve

Para desativar (parar de enviar um tipo de notificação sem excluir o modelo):
1. Abra o modelo
2. Desmarque **Ativo**
3. Salve

## Dicas
Preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos.

- Escreva mensagens na mesma voz da sua marca — o SMS é um canal direto e pessoal, então um tom amigável funciona bem
- Sempre inclua o nome da sua loja na mensagem para que os clientes saibam quem está os enviando uma mensagem
- Mantenha as mensagens de confirmação de pedido curtas: o número do pedido, o total e uma nota sobre os próximos passos são suficientes
- Teste as mensagens colocando um pedido de teste em sua própria loja (usando um número de telefone que você controla) para ver exatamente o que os clientes recebem
- Se uma notificação estiver gerando confusão ou reclamações, desative o modelo e revise-o em vez de excluí-lo — dessa forma, você poderá reativá-lo depois que as atualizações forem feitas
- Modelos de marketing devem ser enviados apenas para clientes que tenham se inscrito explicitamente para marketing por SMS, conforme exigido pelas regulamentações de telecomunicações em mostriques países