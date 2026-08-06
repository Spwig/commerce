---
title: Atualizações da Plataforma
---

Sua instalação do Spwig é composta por uma coleção de componentes — temas, widgets, integrações, elementos do construtor de páginas e conexões com provedores — cada um com sua própria versão que pode ser atualizada de forma independente. O Registro de Componentes oferece uma visão central de tudo que está instalado, mostra quais componentes têm atualizações pendentes e permite que você instale ou reverta atualizações a qualquer momento.

![Visão Geral do Registro de Componentes](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Entendendo o registro de componentes

Navegue até **Painel do Sistema > Atualizações de Componentes** para ver cada componente instalado em sua loja. Cada linha mostra:

- **Nome** — o nome de exibição do componente
- **Tipo** — qual tipo de componente é (tema, widget, integração, etc.)
- **Versão Atual** — a versão que está em execução em sua loja
- **Status da Atualização** — se uma atualização está disponível
- **Canal** — qual canal de atualização o componente segue
- **Atualização Automática** — se as atualizações são instaladas automaticamente
- **Bloqueado** — se o componente está congelado na sua versão atual

O painel no topo da página mostra contagens resumidas: total de componentes instalados, quantos têm atualizações disponíveis e quantos estão atualizados.

### Tipos de componentes

| Tipo | O que é |
|------|------------|
| Tema | O design visual da sua loja |
| Widget | Blocos reutilizáveis do construtor de páginas |
| Elemento do Construtor de Páginas | Elementos personalizados para o construtor de páginas |
| Utilitário do Construtor de Páginas | Ferramentas e utilitários do editor |
| Modelo de Cabeçalho / Rodapé | Layouts de cabeçalho e rodapé |
| Provedor de Envio | Integrações com transportadoras (FedEx, UPS, etc.) |
| Provedor de E-mail | Serviços de entrega de e-mail |
| Provedor de Pagamento | Integrações com gateways de pagamento |
| Provedor de Taxas de Câmbio | Fontes de dados de taxas de câmbio |
| Provedor de Tradução | Serviços de tradução com IA |
| Pacote de Idioma | Arquivos de tradução da interface |

## Canais de atualização

Cada componente segue um canal de atualização que controla quais lançamentos ele recebe. Você pode atribuir cada componente a um canal diferente com base no nível de risco que estiver disposto a aceitar.

| Canal | Descrição | Melhor para |
|---------|-------------|----------|
| **Estável** | Lançamentos prontos para produção, totalmente testados | Todos os componentes em lojas em funcionamento |
| **Beta** | Construções pré-lançamento para testar novos recursos antes de tornarem estáveis | Componentes não críticos que deseja visualizar |
| **Desenvolvimento** | Recursos mais recentes, que podem ser instáveis | Ambientes de teste apenas |
| **Segurança** | Correções críticas de segurança, entregues com a maior prioridade | Componentes para os quais a estabilidade é essencial |

Para alterar o canal de um componente, clique no seu nome para abrir a visão detalhada, depois selecione um novo valor no campo **Canal de Atualização** e salve.

## Verificando atualizações

O Spwig verifica atualizações automaticamente no intervalo configurado nas configurações do servidor de atualização (padrão: a cada 24 horas). Para verificar imediatamente:

1. Navegue até **Painel do Sistema > Atualizações de Componentes**
2. Clique no botão **Verificar Atualizações** no topo da página
3. O sistema entra em contato com o servidor de atualização do Spwig e atualiza o status de atualização para todos os componentes
4. Componentes com atualizações disponíveis são destacados, e a contagem **Atualizações Disponíveis** é atualizada

Você também pode disparar uma verificação de atualização para componentes individuais usando a ação **Verificar Atualizações** no menu de ações da lista.

## Instalando atualizações

### Atualizando um único componente

1. Navegue até **Painel do Sistema > Atualizações de Componentes**
2. Encontre o componente que deseja atualizar — componentes com atualizações disponíveis mostram um indicador de atualização ao lado de sua versão
3. Clique no botão **Instalar Atualização** na linha desse componente
4. Confirme a atualização quando solicitado
5. A atualização é baixada, verificada e instalada — um indicador de progresso mostra cada etapa
6. Uma vez concluída, a versão atual do componente é atualizada para o novo número de versão

### Atualizando múltiplos componentes

1.

Selecione as caixas de seleção ao lado dos componentes que deseja atualizar
2.



Escolha **Instalar atualizações** no menu suspenso **Ação**
3.

Clique em **Ir** para continuar
4.

As atualizações são instaladas na ordem de dependência — componentes nos quais outros dependem são atualizados primeiro

### O que acontece durante uma atualização

O processo de atualização passa por estas etapas:

1. **Verificando** — confirma que a atualização está disponível e sua licença é válida
2. **Baixando** — recupera o pacote do servidor de atualização Spwig
3. **Verificando integridade** — verifica a integridade do pacote contra um checksum SHA-256
4. **Extraindo** — descompacta os novos arquivos
5. **Implantando** — ativa a nova versão
6. **Verificação de saúde** — verifica se o componente está funcionando após a atualização

Se qualquer etapa falhar, o sistema tentará automaticamente restaurar a versão anterior.

## Atualizações no nível da plataforma

Além dos componentes individuais, o Spwig pode receber atualizações no nível da plataforma que atualizam o próprio motor de loja. Essas atualizações passam por um processo mais rigoroso, incluindo migrações de banco de dados e uma breve janela de manutenção.

Navegue até **Painel do Sistema > Atualizações da Plataforma** para visualizar e gerenciar atualizações no nível da plataforma separadamente dos componentes individuais.

### Revisar o que é novo antes de instalar

Clique em **Verificar Atualizações** para ver se uma nova versão da plataforma está disponível. Quando uma é encontrada, a carta **Atualização Disponível** mostra a mudança de versão (ex. `v1.7.0 → v1.7.1`), o **Tamanho do Pacote**, **Tempo Estimado**, e o **Canal** da atualização — e uma pré-visualização de **O que é novo** para que você veja o que mudou antes de decidir instalar:

- Uma linha resumida descrevendo o lançamento
- Uma lista em item com as principais mudanças naquela versão (até cinco, com uma nota se houver mais)

Se a atualização alterar o esquema do seu banco de dados, uma notificação **Requer migração do banco de dados** aparece com um tempo estimado. As atualizações de segurança mostram um **badge de atualização de segurança** recomendando que você instale imediatamente. Leia a pré-visualização de **O que é novo** antes de instalar — é a forma mais rápida de ver se um lançamento precisa de atenção extra, como etapas destacadas após a conclusão da atualização.

O histórico de atualizações da plataforma está visível mais abaixo na página. Cada entrada mostra a transição de versão (ex. `v1.3.2 → v1.3.3`), o status e a duração do processo de atualização.

As atualizações de segurança são marcadas separadamente e, se **Instalar automaticamente atualizações de segurança** estiver habilitado na configuração do seu servidor de atualização, instalam-se automaticamente, sem exigir ação manual.

## Visualizando o histórico de versões

Para ver todas as versões anteriormente instaladas de um componente:

1. Clique no nome do componente para abrir sua visão detalhada
2. Role até a seção **Versões do Componente** no final da página
3. Cada entrada de versão mostra o número da versão, quando foi instalada, o método de instalação e seu status de saúde

O sistema mantém as três últimas versões instaladas disponíveis para reverter. Versões além disso são removidas automaticamente.

## Reverter um componente

Se uma atualização causar problemas, você pode reverter para uma versão anterior:

1. Abra a visão detalhada do componente
2. Role até a seção **Reverter**
3. Selecione a versão que deseja restaurar
4. Clique em **Reverter para esta versão**

Apenas versões marcadas como **Reversão disponível** podem ser restauradas. O registro de log de reversão indica quem iniciou a reversão e quando.

## Bloquear componentes

Bloquear um componente impede que qualquer atualização seja instalada, incluindo as automáticas. Isso é útil quando você tem personalizações ou integrações que dependem de uma versão específica.

1. Abra a visão detalhada do componente
2. Marque a caixa **Bloqueado** na seção **Bloquear e Congelar**
3. Insira um motivo em **Motivo do Bloqueio** para que sua equipe saiba por que está congelado
4. Salve o registro

Componentes bloqueados são mostrados com um indicador de bloqueio na lista do registro. Para desbloquear, desmarque **Bloqueado** e salve.

## Lendo logs de atualização

O log de atualização registra todas as operações de instalação, atualização, reversão e verificação de saúde:

1.

Abra a visão detalhada de um componente
2.

Os **Logs de Atualização** estão visíveis inline no final da página
3.



Cada entrada mostra: a ação realizada, horários de início e fim, versões antiga e nova, se foi automática ou manual, e quaisquer mensagens de erro, se a operação falhou

Entradas de log com status **Failed** incluem a mensagem de erro completa para ajudar no troubleshooting.

## Habilitando atualizações automáticas

Você pode permitir que o Spwig instale atualizações automaticamente conforme elas ficarem disponíveis:

1. Abra a visualização de detalhes do componente
2. Marque **Auto Update** na seção **Version & Update Status**
3. Salve o registro

Com a atualização automática habilitada, o sistema instala as atualizações durante o próximo ciclo de verificação agendado. As atualizações de segurança seguem a configuração global **Auto Install Security Updates**, independentemente das configurações individuais do componente.

## Dicas

- Sempre atualize no canal **Stable** para temas e provedores de pagamento — esses são os componentes mais voltados para o cliente e a estabilidade é mais importante
- Bloqueie um componente antes de fazer modificações personalizadas nele, e registre claramente o motivo para que futuros membros da equipe saibam não atualizá-lo
- Verifique as **Release Notes** na entrada de versão do componente antes de instalar um aumento de versão principal — alterações quebram são marcadas lá
- Antes de instalar uma atualização de plataforma, leia o preview **What's New** na página **Platform Updates** — para uma visão completa das notas de lançamento, incluindo quaisquer etapas adicionais que você possa precisar, continue para a página **System Upgrade**
- Após uma atualização, navegue até a área afetada de sua loja para confirmar que tudo parece e funciona conforme o esperado antes de declarar a atualização completa
- Se a atualização automática estiver habilitada em um componente, monitore periodicamente os **Update Logs** para garantir que as atualizações automáticas estejam sendo concluídas com sucesso