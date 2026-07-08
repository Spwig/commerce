---
title: Papeis e Permissões de Funcionários
---

Os papeis de funcionários permitem que você controle exatamente o que cada membro da equipe pode ver e fazer — tanto no painel de administração quanto no terminal POS. Defina papeis com permissões específicas, depois atribua-os aos membros da equipe. Um usuário pode ter múltiplos papeis, e suas permissões efetivas são a combinação de todos os papeis atribuídos.

![Papeis de funcionários](/static/core/admin/img/help/staff-roles/role-list.webp)

## Como Funciona

1. Você cria **papeis** que definem um conjunto de permissões (ex: "Gerente de Pedidos", "Caixa")
2. Cada papel controla dois tipos de acesso: **permissões do painel de administração** e **permissões do POS**
3. Você **atribui papeis** a membros da equipe a partir da página do perfil
4. As permissões efetivas de um membro da equipe são a **união** de todos os seus papeis — se qualquer papel conceder acesso, o usuário tem acesso
5. As permissões são **armazenadas em cache** para desempenho e atualizadas automaticamente quando os papeis mudam

## Papeis Predefinidos

O Spwig inclui 7 papéis integrados que cobrem as estruturas de equipe mais comuns. Esses não podem ser excluídos, mas você pode criar papéis personalizados para necessidades mais específicas.

| Papel | Acesso | Descrição |
|------|--------|-------------|
| **Proprietário da Loja** | Admin + POS | Acesso completo a tudo. Para o administrador principal da loja. |
| **Gerente da Loja** | Admin + POS | Operações diárias — acesso completo a produtos, pedidos, clientes, marketing e busca. Apenas visualização para design, e-mail, pagamentos e configurações. |
| **Editor de Conteúdo** | Admin | Gerencia páginas, posts de blog, design e mídia. Apenas visualização para produtos. |
| **Gerente de Pedidos** | Admin | Gerencia pedidos, envios, devoluções e atendimento ao cliente. Apenas visualização para produtos. |
| **Gerente de Marketing** | Admin | Gerencia promoções, cupons, afiliados, programas de fidelidade e indicações. Apenas visualização para produtos, clientes e mídia. |
| **Caixa** | POS apenas | Funcionário de linha de frente do POS. Pode processar vendas e verificar saldos de cartões-presente. Nenhuma permissão para descontos, devoluções ou gestão de caixa. |
| **Caixa Sênior** | POS apenas | Funcionário experiente do POS. Pode processar devoluções, aplicar descontos (até 25%), gerenciar o caixa e fechar turnos. |

## Criando um Papel Personalizado

Navegue até **Configurações > Papeis de Funcionários** e clique em **Adicionar Papel**.

### Configurações Gerais

| Configuração | Descrição |
|---------|-------------|
| **Nome de Exibição** | O nome do papel mostrado no painel de administração (ex: "Funcionário de Armazém") |
| **Descrição** | Uma breve explicação do que esse papel é para |
| **Ordem de Classificação** | Controla a ordem de exibição na lista de papéis |
| **Ícone** | Escolha entre 20 ícones para identificar visualmente o papel |
| **Cor do Badge** | Cor usada para badges de papel (Azul, Verde, Laranja, Vermelho, Ciano, Cinza) |
| **Painel de Administração** | Ative se esse papel concede acesso ao backend de administração |
| **Terminais POS** | Ative se esse papel concede acesso a terminais POS |

### Categorias de Permissão de Administração

A guia de permissões de administração organiza todas as funcionalidades da plataforma em 13 categorias. Para cada categoria, você define um dos três níveis de acesso:

- **Nenhum** — Nenhum acesso a essa área (itens de menu são ocultos)
- **Visualizar** — Acesso somente leitura (pode ver dados, mas não alterá-los)
- **Completo** — Acesso completo (pode visualizar, criar, editar e excluir)

![Categorias de permissão](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Categoria | O que Controla |
|----------|-----------------|
| **Catálogo de Produtos** | Produtos, categorias, marcas, atributos, estoque, armazéns, ativos digitais |
| **Pedidos e Conclusão** | Pedidos, devoluções, devoluções, envios, configuração de envio |
| **Clientes** | Perfil de clientes, segmentos, análises |
| **Conteúdo e Páginas** | Páginas, posts de blog, anúncios, formulários |
| **Design e Tema** | Temas, modelos de cabeçalho/rodapé, menus, tokens de design, CSS personalizado |
| **Marketing e Promoções** | Promoções, cupons, afiliados, programas de fidelidade, indicações, feeds de produtos |
| **Biblioteca de Mídia** | Imagens, vídeos, pastas, tags |
| **Sistema de E-mail** | Contas de e-mail, modelos, fila de entrega |
| **Pagamentos e Faturamento** | Fornecedores de pagamento, transações, webhooks, assinaturas, taxas de câmbio |
| **Busca** | Configurações de busca, sinônimos, redirecionamentos, análises |
| **Configurações da Loja** | Configurações do site, geolocalização, mapeamento de países, regras de negócios |
| **Gerenciamento POS** | Terminais POS, turnos, movimentos de dinheiro, modelos de recibos |
| **Usuários e Papeis** | Contas de usuários de staff, papeis, tokens de API |

Quando um usuário tem múltiplos papeis, o **maior** nível de acesso vence. Por exemplo, se o Papel A concede "Visualizar" para Produtos e o Papel B concede "Completo", o usuário tem acesso "Completo".

### Bandeiras de Permissão POS

Se o papel concede acesso ao POS, a guia de Permissões POS permite que você ajuste exatamente o que um operador POS pode fazer. Essas são separadas das permissões de administração e são verificadas no terminal POS.

![Permissões POS](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Grupo | Permissão | Descrição |
|-------|-----------|-------------|
| **Geral** | Acesso ao POS | Pode usar o sistema POS em todos os momentos |
| **Vendas e Descontos** | Descontos Manuais | Pode aplicar descontos manuais em itens ou no nível do carrinho |
| | Percentual Máximo de Desconto | O maior percentual de desconto permitido (0–100) |
| | Sobrescrita de Preço | Pode sobrescrever os preços dos produtos no caixa |
| **Devoluções e Anulações** | Processar Devoluções | Pode processar devoluções em pedidos POS |
| | Anular Pedidos | Pode anular pedidos POS do turno atual |
| **Cartões-presente** | Emitir Cartões-presente | Pode emitir novos cartões-presente no caixa |
| | Verificar Saldo do Cartão-presente | Pode verificar os saldos dos cartões-presente |
| **Gestão de Dinheiro** | Gestão de Dinheiro | Pode realizar operações de entrada e saída de dinheiro |
| | Abrir Caixa | Pode abrir o caixa sem uma venda |
| | Fechar Turnos | Pode fechar turnos e realizar reconciliação de dinheiro |
| **Relatórios** | Ver Relatórios POS | Pode ver relatórios de turnos e resumos de vendas |
| **Estoque** | Ajustes de Estoque | Pode ajustar os níveis de estoque (receber, danos, reccontagem, devoluções) |

Para permissões booleanas, se **qualquer** um dos papeis do usuário as habilitar, o usuário tem acesso. Para o Percentual Máximo de Desconto, o **maior** valor entre todos os papeis se aplica.

## Gerenciando Membros da Equipe

Navegue até **Configurações > Gerenciamento de Funcionários** para visualizar e gerenciar sua equipe.

### Lista de Funcionários

A lista de funcionários mostra todos os usuários com acesso de funcionário. Para cada membro, você pode ver:
- **Nome e e-mail**
- **Papeis atribuídos** (mostrados como badges coloridos)
- **Tipo de acesso** — Apenas Admin, Apenas POS ou Ambos
- **Status de 2FA** — Se a autenticação de dois fatores está ativada
- **Status Ativo/Inativo**

Use os filtros para estreitar por papel, tipo de acesso ou status de 2FA.

### Atribuindo Papeis a Funcionários

1. Clique em um membro da equipe para abrir seu perfil
2. Na seção **Papeis**, você verá cartões para cada papel disponível
3. Clique no interruptor de qualquer cartão de papel para atribuir ou remover
4. As alterações têm efeito imediatamente — não é necessário clicar em um botão de salvar
5. A resumo **Permissões Efetivas** abaixo mostra o resultado combinado de todos os papeis atribuídos

### Adicionando um Novo Membro da Equipe

1. Navegue até **Configurações > Gerenciamento de Funcionários** e clique em **Adicionar Membro da Equipe**
2. Insira o e-mail, nome e sobrenome do usuário
3. Defina uma senha temporária
4. Atribua um ou mais papeis
5. O usuário agora pode fazer login com o acesso fornecido pelos seus papeis

## Clonando Papeis

Para criar um novo papel com base em um existente:

1. Abra o papel que deseja copiar
2. Clique em **Clonar Papel** no final da página
3. Um novo papel é criado com todas as mesmas permissões
4. Renomeie-o e ajuste as permissões conforme necessário
5. Salve o novo papel

Isso é útil quando você precisa de um papel semelhante a um existente, mas com pequenas diferenças — por exemplo, um "Gerente Júnior" baseado em "Gerente de Loja" mas com menos permissões.

## Como as Permissões são Aplicadas

### Painel de Administração

- **Visibilidade do menu** — Seções do menu lateral são ocultas para categorias onde o usuário tem acesso "Nenhum"
- **Acesso a páginas** — Tentar visitar uma página restrita mostra um erro de permissão
- **Restrições de ação** — Com acesso "Visualizar", os botões de edição e exclusão são ocultos e as ações de salvar são bloqueadas
- **Bypass de superusuário** — Contas de superusuário sempre têm acesso completo, independentemente das atribuições de papel

### Terminal POS

- **Porta de login** — Apenas usuários com pelo menos um papel que tenha "Terminais POS" habilitado podem fazer login no POS
- **Comutadores de funcionalidade** — Botões e ações do POS (devolução, desconto, anulação, etc.) são mostrados ou ocultos com base nas permissões POS combinadas do usuário
- **Limite de desconto** — O Percentual Máximo de Desconto impõe um limite rígido sobre o tamanho do desconto que um operador POS pode aplicar
- **Enforce no API** — Todas as permissões do POS são verificadas no lado do servidor na camada de API, e não apenas na interface do usuário

## Dicas

- **Comece com papeis predefinidos** — Os 7 papéis integrados cobrem a maioria das estruturas de equipe. Crie papeis personalizados apenas quando precisar de controles de acesso mais específicos.
- **Use a funcionalidade de clonagem** — Quando você precisar de um papel semelhante a um existente, clone-o e faça ajustes em vez de construir do zero.
- **Atribua múltiplos papeis quando necessário** — Um membro da equipe que lida com pedidos e marketing pode ser atribuído aos papeis "Gerente de Pedidos" e "Gerente de Marketing". As permissões se combinam automaticamente.
- **Separe o acesso ao admin e ao POS** — Caixas geralmente não precisam de acesso ao admin, e funcionários de escritório não precisam de acesso ao POS. Use os interruptores de acesso para manter as coisas limpas.
- **Defina limites de desconto para funcionários do POS** — O Percentual Máximo de Desconto impede que os caixas apliquem descontos excessivos. Defina-o para 0 para descontos nulos, ou um limite razoável como 10–25% para funcionários sêniores.
- **Revise os papeis periodicamente** — À medida que sua equipe cresce, faça uma auditoria das atribuições de papeis para garantir que os funcionários tenham o mínimo de acesso necessário para o seu trabalho. Remova os papeis quando as pessoas mudarem de posição.
- **Ative 2FA para papeis sensíveis** — Funcionários com acesso a pagamentos, configurações ou gerenciamento de usuários devem ter a autenticação de dois fatores ativada para segurança.

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.