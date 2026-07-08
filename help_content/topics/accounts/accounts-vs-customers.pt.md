---
title: Contas vs. Clientes
---

Muitos comerciantes perguntam: "Qual a diferença entre uma conta e um cliente?" Essa confusão é comum porque cada cliente é uma conta, mas nem toda conta é um cliente. Este guia esclarece a distinção e explica quando usar cada interface de administrador.

![Lista de Usuários](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## O que é uma Conta?

Uma **conta** é o objeto central de autenticação no Spwig. Qualquer pessoa que possa fazer login em sua plataforma — funcionário ou cliente — tem uma conta. As contas são gerenciadas no sistema de autenticação do Spwig e são armazenadas no modelo `User`.

Todas as contas têm:
- **Endereço de e-mail** — O identificador principal e credencial de login
- **Nome de usuário** — Um nome de usuário único (gerado automaticamente a partir do e-mail por padrão)
- **Senha** — Hashada e armazenada com segurança
- **sinalizador is_staff** — Determina se a conta pode acessar o backend de administrador

As contas também podem autenticar via provedores de OAuth (Google, Facebook, etc.) configurados em **Configurações > Autenticação**.

## O que é um Cliente?

Um **cliente** é um tipo especial de conta com `is_staff=False`. Os clientes compram em sua loja virtual, fazem pedidos e gerenciam seus perfis. Cada conta de cliente é automaticamente estendida com:

- **CustomerProfile** — Armazena preferências, status de inscrição em newsletters e valores de campos personalizados
- **CustomerMetrics** — Rastreia valor de vida (LTV), pontuação RFM, histórico de pedidos e dados de segmentação
- **OrderHistory** — Link para todos os pedidos feitos por este cliente

Os clientes podem ser:
- **Clientes registrados** — Criados via registro na loja virtual ou pela interface de administrador
- **Usuários convidados** — Contas temporárias criadas durante o checkout como convidado (nome de usuário começa com `guest_`)
- **Clientes importados** — Migrados de outras plataformas via importação CSV

## A Diferença Principal

| Atributo | Conta | Cliente |
|-----------|---------|----------|
| **Propósito** | Autenticação e autorização | Compras, pedidos e análise |
| **Âmbito** | Funcionários e clientes | Apenas clientes |
| **sinalizador is_staff** | Verdadeiro ou falso | Sempre falso |
| **Dados estendidos** | Nenhum (apenas campos principais) | CustomerProfile + CustomerMetrics |
| **Localização no administrador** | Configurações > Usuários | Clientes > Perfis de Cliente |
| **Pode fazer login** | Sim | Sim |
| **Pode fazer pedidos** | Apenas se tiver CustomerProfile | Sim |
| **Pode acessar o administrador** | Apenas se is_staff=True | Não |

Resumindo:
- Uma **conta** é qualquer pessoa que possa fazer login
- Um **cliente** é uma conta que compra e faz pedidos

## Funcionários também são Contas

Funcionários são contas com `is_staff=True`. Eles podem fazer login no backend de administrador e executar ações com base nas permissões de **StaffRole** atribuídas.

Funcionários podem opcionalmente ter um **CustomerProfile** se também comprarem na loja virtual. Por exemplo, se você (o comerciante) fizer um pedido de teste em sua própria loja, um CustomerProfile é criado para sua conta de funcionário. Isso NÃO afeta seu acesso ao administrador.

As permissões de funcionários são controladas por:
- **StaffRole** — Define quais seções e ações do administrador o funcionário pode acessar
- **sinalizador is_superuser** — Concede acesso completo e irrestrito (use com cuidado)

Gerencie funcionários em **Configurações > Gerenciamento de Funcionários**.

## Usuários Convidados

O checkout como convidado cria contas temporárias com nomes de usuário gerados automaticamente que começam com `guest_`. Essas contas:
- Têm `is_staff=False` (são clientes)
- Têm um CustomerProfile (para associação de pedidos)
- Têm uma senha aleatória (o convidado não pode fazer login a menos que converta para registrado)
- São excluídas por padrão das análises de clientes

Os convidados podem se converter em clientes registrados por:
1. Criar uma conta na loja virtual com o mesmo e-mail
2. Verificar seu endereço de e-mail
3. O sistema mescla o histórico de pedidos do convidado na nova conta registrada

Gerencie as configurações de conversão de convidados em **Configurações > Checkout > Checkout como Convidado**.

## Onde Encontrar Cada Um

| Localização no Administrador | O que Você Gerencia | Casos de Uso Principais |
|----------------|-----------------|---------------|
| **Configurações > Usuários** | Todas as contas (funcionários + clientes) | Redefinir senhas, ativar/desativar contas, atribuir permissões de funcionários |
| **Configurações > Gerenciamento de Funcionários** | Apenas contas de funcionários (is_staff=True) | Atribuir papéis, gerenciar acesso de membros da equipe, configurar permissões |
| **Clientes > Perfis de Cliente** | Apenas contas de clientes (is_staff=False) | Ver preferências do cliente, histórico de pedidos, LTV, pontuação RFM, segmentos |
| **Clientes > Análise** | Métricas e segmentos de clientes | Analisar comportamento do cliente, criar segmentos de marketing, acompanhar retenção |

![Lista de Perfis de Cliente](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Quando Usar Cada Interface

Use **Configurações > Usuários** quando você precisar de:
- Redefinir a senha de um cliente
- Desativar uma conta comprometida
- Criar manualmente uma conta de cliente
- Ver conexões de login OAuth
- Ver todas as contas (funcionários + clientes) em uma lista

Use **Configurações > Gerenciamento de Funcionários** quando você precisar de:
- Adicionar um novo membro da equipe
- Atribuir ou alterar o papel de um funcionário
- Configurar permissões detalhadas
- Auditoria de logs de atividade de funcionários

Use **Clientes > Perfis de Cliente** quando você precisar de:
- Ver o histórico de pedidos de um cliente
- Ver preferências do cliente e valores de campos personalizados
- Ver o status de inscrição em newsletters
- Revisar o LTV e as pontuações RFM do cliente
- Gerenciar segmentos de clientes

Use **Clientes > Análise** quando você precisar de:
- Identificar clientes de alto valor
- Criar segmentos de marketing (ex.: "clientes que não fizeram pedidos em 90 dias")
- Analisar tendências de valor de vida do cliente
- Exportar listas de clientes para campanhas

## Dicas

- **Perfis de clientes são criados automaticamente** — Quando um cliente faz seu primeiro pedido (como convidado ou registrado), o Spwig cria um registro de CustomerProfile e CustomerMetrics para análise.
- **Funcionários também podem ser clientes** — Se um funcionário fizer um pedido na loja virtual, ele obterá um CustomerProfile. Isso é normal e não afeta seu acesso ao administrador.
- **Contas de convidados poluem a lista de usuários** — Use a interface de perfil do cliente para focar em clientes reais e engajados. A lista de usuários inclui todas as contas de convidados.
- **Segmentar por is_staff=False** — Ao exportar listas de clientes para campanhas de e-mail, sempre filtre para `is_staff=False` para excluir membros da equipe.
- **Contas OAuth também são contas** — Quando um cliente faz login via Google ou Facebook, o Spwig cria uma conta e a vincula ao seu perfil OAuth. O campo de e-mail é preenchido a partir do provedor OAuth.