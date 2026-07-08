---
title: Modelos de E-mail
---

Modelos de e-mail controlam o design e o conteúdo de todos os e-mails automatizados que sua loja envia aos clientes e a você — confirmações de pedidos, atualizações de envio, redefinições de senha, notificações de reembolso e muito mais. A edição de um modelo altera todos os e-mails futuros desse tipo; os e-mails anteriores já na caixa de saída não são afetados.

Navegue até **Sistema de E-mail > Modelos de E-mail** para visualizar e gerenciar seus modelos.

![Lista de modelos de e-mail](/static/core/admin/img/help/email-templates/templates-list.webp)

## Tipos de modelo

Sua loja inclui modelos para uma ampla gama de eventos. Eles são agrupados por categoria:

### E-mails de ordem para o cliente
| Modelo | Enviado quando |
|----------|-----------|
| Confirmação de Pedido | Um cliente completa uma compra |
| Confirmação de Pagamento | Um pagamento é processado com sucesso |
| Pedido Enviado | Uma ordem é marcada como enviada |
| Confirmação de Envio | Um número de rastreamento de envio é adicionado |
| Confirmação de Entrega | Uma ordem é marcada como entregue |
| Pedido Cancelado | Uma ordem é cancelada |
| Notificação de Atraso | Um atraso é registrado em uma ordem |
| Notificação de Reembolso | Um reembolso é emitido |

### E-mails de conta
| Modelo | Enviado quando |
|----------|-----------|
| Bem-vindo à Conta | Um cliente cria uma conta |
| Convite para Conta | Você convida um cliente a criar uma conta |
| Verificação de E-mail | Um cliente verifica seu endereço de e-mail |
| Redefinição de Senha | Um cliente solicita uma redefinição de senha |

### Devoluções
| Modelo | Enviado quando |
|----------|-----------|
| Devoluções: Solicitação Recebida | Um cliente envia uma solicitação de devolução |
| Devoluções: Aprovada | Uma solicitação de devolução é aprovada |
| Devoluções: Recusada | Uma solicitação de devolução é recusada |
| Devoluções: Pacote Recebido | O item devolvido chega ao seu local |
| Devoluções: Reembolso Processado | O reembolso para uma devolução é emitido |

### Notificações de administrador (enviadas para você)
| Modelo | Enviado quando |
|----------|-----------|
| Admin: Nova Ordem | Uma nova ordem é colocada |
| Admin: Pagamento Falhou | Um tentativa de pagamento falha |
| Admin: Relatório de Vendas Diário | O resumo diário de vendas é gerado |
| Admin: Alerta de Estoque Baixo | Um produto cai abaixo do limite de estoque |
| Admin: Resumo Semanal | O resumo semanal da loja é gerado |

Modelos adicionais cobrem marcos de rastreamento de envio, atividades do programa de afiliados, confirmações de reserva (se o recurso de reservas estiver ativado) e eventos do programa de fidelidade.

## Editando um modelo

1. Navegue até **Sistema de E-mail > Modelos de E-mail**
2. Encontre o modelo que deseja editar. Você pode filtrar por **Tipo de Modelo**, **Idioma** ou **Status** usando os filtros à direita
3. Clique no modelo para abri-lo
4. Edite a **Linha do Assunto** (o assunto do e-mail mostrado na caixa de entrada do cliente)
5. Edite o **Conteúdo HTML** para a versão de design completo do e-mail
6. Edite opcionalmente o **Conteúdo de Texto** — uma alternativa de texto simples para clientes de e-mail que não suportam HTML
7. Clique em **Salvar**

> **E-mails HTML:** O campo de conteúdo HTML aceita HTML padrão, incluindo CSS inline. O Spwig renderiza isso em um e-mail formatado corretamente. Se você usar marcação MJML, ela será compilada automaticamente ao salvar.

## Visualizando um modelo

Antes de salvar, você pode visualizar como o modelo será exibido em um cliente de e-mail:

1. Abra o modelo que deseja visualizar
2. Clique no botão **Visualizar** (visível na lista de modelos ou na página de detalhes do modelo)
3. Uma visualização abre em uma nova guia do navegador mostrando o e-mail renderizado

Isso permite que você verifique o layout, formatação e aparência das variáveis de espaço reservado antes que o modelo seja publicado.

## Variáveis de modelo

Variáveis são espaços reservados em seu modelo que o Spwig substitui por dados reais ao enviar o e-mail. Elas são escritas como `{{ variable_name }}`.

Variáveis comuns disponíveis na maioria dos modelos:

| Variável | Substituída por |
|----------|---------------|
| `{{ customer_name }}` | O nome completo do cliente |
| `{{ order_number }}` | O número de referência do pedido |
| `{{ order_total }}` | O valor total do pedido |
| `{{ store_name }}` | O nome do seu loja |
| `{{ store_url }}` | O endereço web do seu loja |
| `{{ tracking_number }}` | O número de rastreamento do envio |
| `{{ tracking_url }}` | Um link clicável para rastrear o envio |

As variáveis exatas disponíveis dependem do tipo de modelo. Variáveis relevantes para um modelo relacionado a pedido (como `{{ order_number }}`) não estão disponíveis em um modelo de conta (como Redefinição de Senha). Se você incluir uma variável que não se aplique, ela aparecerá em branco ou não será substituída.

## Suporte a idiomas

Cada tipo de modelo pode ter uma versão para cada idioma que sua loja suporta. O campo **Idioma** em cada modelo controla qual versão de idioma está ativa.

O Spwig seleciona automaticamente a versão correta do idioma com base na preferência de idioma do cliente ao enviar. Se não houver um modelo para o idioma do cliente, o Spwig recorrerá à versão em inglês.

Para adicionar um modelo para um novo idioma:
1. Abra um modelo existente
2. Clique em **Clonar Modelo** no menu **Ações**
3. Defina o **Código do Idioma** no clone para o novo idioma
4. Traduza o conteúdo
5. Ative o modelo clonado

## Clonagem, ativação e desativação de modelos

### Clonar um modelo

A clonagem cria uma cópia exata de um modelo — útil para criar variantes de idioma ou testar diferentes versões sem afetar o modelo ativo.

1. Selecione um ou mais modelos na lista
2. Escolha **Clonar modelos selecionados** no menu suspenso **Ações**
3. O clone é criado como inativo — edite-o e ative-o quando estiver pronto

### Ativar e desativar modelos

Um modelo deve estar **Ativo** para ser usado para envio. Apenas um modelo ativo por tipo e combinação de idioma é usado de cada vez.

Para ativar ou desativar em lote:
1. Selecione os modelos
2. Escolha **Ativar modelos selecionados** ou **Desativar modelos selecionados** no menu suspenso **Ações**

Ou abra um modelo individual e ative/desative a caixa de seleção **Ativo**.

## Modelos do sistema

Modelos marcados com um **Sistema** são os modelos padrão semeados pelo Spwig. Eles não podem ser excluídos. Você pode editá-los diretamente ou cloná-los para criar uma versão personalizada.

## Dicas

- Sempre pré-visualize um modelo após editar para identificar problemas de formatação antes que os clientes os vejam
- Mantenha os assuntos curtos e específicos — `Seu pedido #10045 foi enviado` tem um desempenho melhor do que assuntos genéricos como `Atualização da nossa loja`
- Edite também o conteúdo em texto simples — alguns clientes de e-mail mostram apenas a versão em texto simples, e alguns clientes preferem isso
- Clone a versão em inglês de um modelo como ponto de partida antes de criar uma versão traduzida
- Se quiser testar uma alteração sem afetar os e-mails ativos, clone o modelo, edite a cópia e deixe ambas ativas brevemente enquanto verifica a pré-visualização — depois desative o original
- Modelos de notificação do administrador (como **Administrador: Novo Pedido**) são enviados para o endereço de e-mail do administrador da sua loja — certifique-se de que esse endereço de e-mail esteja correto nas configurações da sua loja