---
title: Visão Geral do Programa de Afiliados
---

O recurso de programa de afiliados do Spwig permite que você recrute parceiros que promovem seus produtos em troca de comissões. Esse canal de marketing amplia seu alcance por meio de influenciadores, blogueiros, criadores de conteúdo e embaixadores de marca que compartilham links de rastreamento únicos com seus públicos. Quando alguém clica em um link de afiliado e faz uma compra, o afiliado ganha uma comissão e você ganha um cliente.

Este resumo explica o que é o programa de afiliados, para quem ele é e como os vendedores usam ele para construir uma rede de parceiros que impulsionam as vendas.

![Painel do Vendedor](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Conceitos Principais

Entender esses termos fundamentais ajudará você a configurar e gerenciar seu programa de afiliados:

| Termo | Definição |
|------|------------|
| **Afiliado** | Um parceiro que promove seus produtos e ganha comissões por vendas referenciadas |
| **Programa** | Uma estrutura de comissão com taxas, regras e configurações (você pode criar múltiplos programas) |
| **Link de Rastreamento** | Um URL único contendo o código do afiliado (ex.: `yourstore.com/?ref=CODE`) |
| **Comissão** | O pagamento que um afiliado recebe por uma venda referenciada, calculado com base nas regras do programa |
| **Duração do Cookie** | Quanto tempo (em dias) o cookie de rastreamento persiste após um cliente clicar em um link de afiliado |
| **Pagamento** | Um pagamento em massa que liquida múltiplas comissões aprovadas de uma só vez |
| **Painel do Vendedor** | Seu interface de administração para gerenciar programas, afiliados, comissões e pagamentos |
| **Portal do Afiliado** | O painel público onde os afiliados visualizam seus ganhos, obtêm links de rastreamento e solicitam pagamentos |

## Como Funciona

O fluxo de trabalho do afiliado segue quatro etapas principais:

### 1. Candidatar-se
Afiliados descobrem seu programa e submetem candidaturas pelo portal público de afiliados em `/affiliate/` no seu loja. Você pode habilitar **aprovação automática** para programas abertos ou **revisão manual** para parcerias convidadas.

### 2. Aprovar
Você revisa as candidaturas pendentes em **Marketing > Afiliados**. Verifique o site de cada candidato, sua presença nas redes sociais e a adequação do público antes de aprovar. Após a aprovação, o afiliado recebe as credenciais de login e pode acessar seu painel.

### 3. Promover
Afiliados aprovados recebem links de referência únicos do seu portal. Eles compartilham esses links em posts de blog, redes sociais, newsletters por e-mail ou onde quer que se conectem com seu público. O Spwig define um cookie de rastreamento quando alguém clica no link.

### 4. Ganhar
Quando um cliente referenciado completa uma compra dentro do período de validade do cookie, o Spwig cria um registro de comissão. Você revisa e aprova as comissões em **Marketing > Comissões**, depois processa os pagamentos quando os afiliados atingem o limite mínimo de pagamento.

## Visão Geral do Fluxo de Trabalho do Vendedor

Como vendedor, você gerencia o ciclo de vida inteiro do programa a partir do seu painel de administração:

### Criando Programas
Comece criando um ou mais programas de afiliados em **Marketing > Programas de Afiliados**. Cada programa tem sua própria estrutura de comissão, duração do cookie e configurações de aprovação. Você pode criar programas separados para influenciadores (comissão mais alta) versus parcerias gerais (comissão mais baixa).

### Revisando Candidaturas
Novas candidaturas de afiliados aparecem em **Marketing > Afiliados** com o status **Pendente**. Revise cada candidatura para verificar se o parceiro é uma boa escolha para sua marca. Aprova para ativar sua conta ou rejeite com uma razão.

### Aprovando Comissões
Quando os afiliados geram vendas, as comissões aparecem em **Marketing > Comissões** com o status **Pendente**. Revise o pedido vinculado para verificar se é legítimo (não uma auto-referência, não um pedido devolvido), depois aprovado ou rejeitado conforme necessário.

### Processando Pagamentos
Uma vez que os afiliados acumulem comissões aprovadas acima do seu limite mínimo de pagamento, processe pagamentos em massa em **Marketing > Pagamentos**. O Spwig integra-se com PayPal e Airwallex para pagamentos automatizados, ou você pode registrar transferências bancárias manuais.

## Visão Geral do Fluxo de Trabalho do Afiliado

Entender como os afiliados experimentam seu programa ajuda você a projetar uma melhor onboarding e suporte:

### Candidatar-se
Afiliados visitam seu portal de afiliados, leem os detalhes do programa (taxa de comissão, duração do cookie, termos de pagamento) e submetem uma candidatura com suas informações de contato e canais de promoção.

### Criar Links
Após a aprovação, os afiliados entram no seu painel para gerar links de rastreamento. Eles podem criar links gerais para a loja ou links para produtos/categorias específicas que desejam promover.

### Promover
Afiliados compartilham seus links de rastreamento onde quer que se conectem com potenciais clientes — posts de blog, vídeos do YouTube, histórias do Instagram, newsletters por e-mail ou sites de comparação.

### Solicitar Pagamentos
Afiliados rastreiam seus ganhos em tempo real pelo painel do portal de afiliados. Quando seu saldo aprovado atinge o limite mínimo de pagamento, eles podem solicitar um pagamento.

## Onde Encontrar Cada Funcionalidade

| Funcionalidade | Localização no Admin | Descrição |
|---------|---------------|-------------|
| **Programas** | Marketing > Programas de Afiliados | Crie e configure estruturas de comissão |
| **Afiliados** | Marketing > Afiliados | Revisar candidaturas, gerenciar contas de afiliados |
| **Comissões** | Marketing > Comissões | Revisar e aprovar comissões pendentes |
| **Pagamentos** | Marketing > Pagamentos | Processar pagamentos em massa para afiliados |
| **Configurações** | Marketing > Configurações de Afiliados | Configurações globais, provedores de pagamento, personalização do portal |
| **Painel** | Marketing > Painel de Afiliados | Visão de análise com cliques, pedidos e totais de comissão |

O portal voltado para afiliados está automaticamente disponível em `/affiliate/` no URL público da sua loja.

## Casos de Uso Comuns

Aqui estão quatro formas comprovadas de como os vendedores usam o programa de afiliados do Spwig para crescer seu negócio:

### Parcerias com Influenciadores
Parceirar com influenciadores de mídia social que têm públicos engajados em seu nicho. Ofereça taxas de comissão mais altas (15–20%) para atrair influenciadores de qualidade que podem gerar tráfego significativo. Use links de rastreamento para medir o ROI de cada parceria.

### Embaixadores de Marca
Construa uma rede de clientes fiéis que se tornam defensores da marca. Ofereça contas de afiliados a esses clientes recorrentes para que eles ganhem comissões quando referirem amigos e familiares. Isso funciona especialmente bem para produtos de nicho com comunidades apaixonadas.

### Criadores de Conteúdo
Contrate blogueiros, YouTubers e podcasters que criam guias de compras, resenhas ou conteúdo de comparação. Afiliados com conteúdo permanente podem gerar referências consistentes mês após mês.

### Redes de Indicações
Permita que clientes existentes participem do seu programa e ganhem comissões ao compartilharem produtos que amam. Isso cria um ciclo viral onde clientes satisfeitos se tornam promotores, trazendo novos clientes que podem também se tornarem afiliados.

## Dicas

- **Comece com um programa** — Crie um programa de parceiro geral com uma taxa de comissão de 10% e duração do cookie de 30 dias. Você pode adicionar programas especializados depois que entender quais parceiros performam melhor.
- **Estabeleça expectativas claras** — Documente seu processo de aprovação, cronograma de comissões e agenda de pagamento no portal de afiliados. A transparência constrói confiança e reduz solicitações de suporte.
- **Monitore fraudes** — Revise cuidadosamente as comissões para sinais vermelhos como auto-indicações (afiliados comprando de seus próprios links), taxas de devolução anormalmente altas ou padrões de cliques suspeitos. Rejeite imediatamente comissões fraudulentas.
- **Comunique-se regularmente** — Envie atualizações mensais aos seus afiliados com notícias do programa, destaque do calendário promocional e reconhecimento de melhores desempenhos. Comunicação ativa mantém os afiliados engajados e promovendo.
- **Otimize para mobile** — A maioria dos afiliados compartilha links em redes sociais onde a maioria dos cliques vem de dispositivos móveis. Teste seu fluxo de checkout em telefones para garantir uma experiência suave para clientes referenciados.
- **Forneça ativos criativos** — Facilite a promoção dos produtos pelos afiliados fornecendo imagens de banner, fotos de produtos e cópias pré-escritas que eles possam usar em seu conteúdo.