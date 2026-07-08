---
title: Produtos Reserváveis
---

Produtos reserváveis permitem que os clientes reservem uma data e hora específica ao comprar. Isso suporta consultas, aluguéis, aulas, eventos e reservas de acomodações — tudo gerenciado diretamente do seu painel de administração do Spwig.

## Tipos de reserva

| Tipo | Melhor para |
|------|----------|
| **Consulta** | Serviços: consultas, cortes de cabelo, treinamento personalizado |
| **Aluguel** | Aluguel de equipamentos, veículos, salas |
| **Aula / Workshop** | Sessões em grupo com capacidade definida |
| **Acomodação** | Estadias de várias noites com horários de check-in/check-out |
| **Evento** | Eventos com ingressos, únicos ou recorrentes |

## Configurando um produto reservável

### Etapa 1: Crie o produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina **Tipo de Produto** como **Produto de Reserva**
3. Preencha os campos padrão do produto (nome, descrição, preço)
4. Salve o produto

### Etapa 2: Configure as configurações de reserva

Após salvar, uma seção **Configuração de Reserva** aparece no formulário de edição do produto. Preencha as configurações de reserva:

#### Tipo de reserva e duração

- **Tipo de Reserva** — Selecione o tipo que melhor corresponde ao seu serviço (Consulta, Aluguel, Aula, etc.)
- **Tipo de Duração** — Escolha **Duração Fixa** para sessões com duração definida, ou **Cliente Escolhe a Duração** para permitir que os clientes escolham quanto tempo precisam
- **Duração** e **Unidade de Duração** — Defina o comprimento (ex: `60` minutos, `1` hora, `2` dias)
- **Duração Mínima/Máxima** — Se os clientes podem escolher a duração, defina o intervalo permitido

#### Tempo de buffer

O tempo de buffer é adicionado automaticamente entre reservas para permitir preparação ou limpeza:
- **Buffer Antes** — Minutos reservados antes do início da reserva
- **Buffer Depois** — Minutos reservados após o término da reserva

Por exemplo, uma consulta de massagem de 60 minutos com um buffer de 15 minutos após dá 15 minutos para se preparar para o próximo cliente.

#### Janela de reserva antecipada

- **Notificação Mínima de Antecedência** — Quanto tempo antes o cliente deve reservar (ex: `24 horas` para não permitir reservas do mesmo dia)
- **Janela Máxima de Antecedência** — Quanto tempo no futuro os clientes podem reservar (ex: `365 dias`)

#### Capacidade

- **Máximo de Reservas por Lote** — Para aulas e eventos, defina quantos clientes podem reservar o mesmo horário. Defina como `1` para consultas privadas.

#### Confirmação

- **Requer Confirmação Manual** — Quando marcado, as reservas não são confirmadas automaticamente. Você deve aprovar manualmente cada reserva na lista de reservas. Útil quando deseja verificar os clientes antes de confirmar.

#### Política de cancelamento

- **Cancelamento Permitido** — Se os clientes podem cancelar sua reserva
- **Prazo para Cancelamento** — Quantas horas/dias antes da reserva os clientes podem cancelar (ex: `24 horas`)

#### Exibição do calendário

Como os clientes selecionam sua data e hora na página do produto:

| Modo de Exibição | Melhor para |
|-------------|----------|
| **Visão de Calendário** | Uso geral — calendário completo do mês |
| **Seletor de Data** | Seleção simples de uma data |
| **Dropdown de Datas Disponíveis** | Produtos com poucas vagas disponíveis |
| **Seletor de Intervalo de Data** | Acomodações e aluguéis de vários dias |

#### Depósitos

Para exigir um depósito no checkout em vez de pagamento total:
1. Marque **Depósito Ativado**
2. Defina **Tipo de Depósito** como **Valor Fixo** ou **Porcentagem do Total**
3. Insira o **Valor do Depósito** (ex: `50` para $50, ou `25` para 25%)

#### Configurações específicas de acomodação

Para reservas de acomodações, campos adicionais aparecem:
- **Horário de Check-in** e **Horário de Check-out** — Horários padrão para a propriedade
- **Ocupação Padrão** — Número padrão de hóspedes incluídos na taxa base

### Etapa 3: Adicionar recursos de reserva (opcional)

Recursos são os itens físicos ou membros da equipe que são atribuídos a uma reserva — por exemplo, "Sala 1", "Quadra A" ou "Instrutor Sam".

1. No formulário de edição do produto, vá para a seção **Recursos de Reserva**
2. Clique em **Adicionar Recurso**
3. Dê ao recurso um **Nome** e defina sua **Capacidade** (quantas reservas ele pode lidar simultaneamente)
4. Adicione opcionalmente imagens do recurso

Recursos permitem que você acompanhe a disponibilidade por ativo ou membro da equipe individual, e não apenas por horário.

### Passo 4: Definir regras de disponibilidade

As regras de disponibilidade definem quando os agendamentos podem ser feitos:

1. Na seção **Disponibilidade** do produto, clique em **Adicionar Regra de Disponibilidade**
2. Selecione o **Recurso** a que essa regra se aplica
3. Defina os **Dias da Semana** em que os agendamentos estão disponíveis
4. Defina o **Horário de Início** e o **Horário de Término** da janela disponível
5. Defina opcionalmente um intervalo de datas (**Válido a partir de** / **Válido até**) para disponibilidade sazonal
6. Salvar

## Visualizando e gerenciando agendamentos

### Lista de agendamentos

Navegue até **Catálogo > Agendamentos** para ver todos os agendamentos. Você pode filtrar por:
- Status (Aguardando Confirmação, Confirmado, Cancelado, Concluído, Não Compareceu)
- Produto
- Intervalo de datas

### Status dos agendamentos

| Status | Significado |
|--------|---------|
| **Aguardando Confirmação** | Aguardando aprovação manual (se confirmação for necessária) |
| **Confirmado** | O agendamento está confirmado e ativo |
| **Cancelado** | O agendamento foi cancelado pelo cliente ou por você |
| **Concluído** | A data do agendamento passou e foi cumprida |
| **Não Compareceu** | O cliente não compareceu |

### Confirmar um agendamento pendente

1. Abra o agendamento em **Catálogo > Agendamentos**
2. Altere o **Status** para **Confirmado**
3. Salvar — o cliente recebe automaticamente um e-mail de confirmação

### Cancelar um agendamento

1. Abra o agendamento
2. Altere o **Status** para **Cancelado**
3. Insira um **Motivo de Cancelamento** (exibido no e-mail do cliente)
4. Salvar

## Gerenciando a lista de espera

Quando um horário estiver totalmente reservado, os clientes podem adicionar-se à lista de espera. O Spwig notifica automaticamente os clientes da lista de espera quando uma cancelação criar uma vaga.

### Visualizando a lista de espera

Navegue até **Catálogo > Lista de Espera de Agendamentos** para ver todas as entradas da lista de espera. Cada entrada mostra:
- Nome e e-mail do cliente
- O produto e a data desejada
- Status: **Esperando**, **Notificado**, **Convertido para Agendamento** ou **Expirado**

### Status da lista de espera

| Status | Significado |
|--------|---------|
| **Esperando** | O cliente está na fila, o horário ainda não está disponível |
| **Notificado** | O cliente foi notificado por e-mail sobre uma vaga disponível |
| **Convertido para Agendamento** | O cliente ocupou o horário e completou um agendamento |
| **Expirado** | A data desejada passou sem que uma vaga ficasse disponível |

### Notificando manualmente um cliente da lista de espera

Se quiser se comunicar com um cliente específico da lista de espera antes da notificação automática:
1. Abra a entrada da lista de espera
2. Copie seu endereço de e-mail e entre em contato diretamente com ele
3. Uma vez que ele complete um agendamento, o status da entrada da lista de espera é atualizado para **Convertido para Agendamento**

## Dicas

- Ative a confirmação manual para agendamentos de alto valor (ex.: sessões de fotografia, eventos privados) para que você possa verificar a disponibilidade e combinar os requisitos antes de comprometer-se.
- Defina um tempo de buffer generosamente no início — você sempre pode reduzi-lo depois que entender as necessidades reais de turnaround.
- Para aulas em grupo, defina **Máximo de Agendamentos por Horário** para a capacidade da aula e ative a lista de espera para que sessões populares criem automaticamente uma fila.
- Use o modo de exibição do seletor de intervalo de datas para produtos de hospedagem — os clientes esperam selecionar juntas as datas de chegada e saída.
- Defina um aviso mínimo de antecedência para evitar agendamentos de último momento se você precisar de tempo para preparação (ex.: aviso mínimo de 48 horas para pedidos de catering personalizado).
- Revise regularmente sua lista de espera durante as estações ocupadas — o contato manual com clientes da lista de espera pode preencher cancelações mais rapidamente do que a notificação automática.