---
title: Configurando as Configurações da Loja
---

Configurações da Loja é o local central para configurar a identidade, localização, marca e preferências operacionais da sua loja. Navegue até **Configurações > Configurações da Loja** para começar.

![Guia Geral das Configurações da Loja](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Guia Geral

A **Guia Geral** contém as configurações principais da identidade da sua loja.

### Identidade da Loja

- **Nome da Loja** — O nome exibido nos títulos das páginas, e-mails e no cabeçalho do painel de administração.
- **Slogan** — Uma breve descrição da sua loja, usada em SEO e compartilhamento em redes sociais.
- **URL do Site** — O endereço web público da sua loja. É usado em e-mails, geração de mapas do site e construção de links.

### Informações de Contato

- **E-mail de Contato** — Recebe notificações de pedidos e é exibido nas comunicações com os clientes.
- **Número de Telefone** — Número de suporte opcional exibido no rodapé e nos e-mails.

### Endereço da Empresa

Digite seu endereço completo (rua, cidade, estado, CEP, país). Ele é usado para:
- Cálculos da origem do envio
- Cálculos de impostos
- Requisitos legais e notas fiscais

## Marca

### Logotipo

Faça o upload do logotipo da sua loja (PNG ou SVG recomendado, ~200x50px com fundo transparente). O logotipo aparece em:
- O cabeçalho da loja
- Modelos de e-mail
- O painel de administração

### Ícone da Página (Favicon)

Faça o upload de um favicon quadrado (ICO ou PNG, 32x32px). Ele aparece como:
- O ícone da aba do navegador
- O ícone de marcador
- O ícone da tela inicial do celular

## Localização

### Idioma Padrão

Escolha o idioma principal da sua loja entre 10 opções suportadas:

| Idioma | Código |
|----------|------|
| Inglês | en |
| Espanhol | es |
| Francês | fr |
| Alemão | de |
| Português | pt |
| Japonês | ja |
| Chines Simplificado | zh-hans |
| Chines Tradicional | zh-hant |
| Russo | ru |
| Árabe | ar |

O idioma padrão controla o idioma da interface do administrador e o fallback para o conteúdo da loja.

### Fuso Horário

Selecione o fuso horário da sua loja para obter datas e horários de pedidos precisos, promoções agendadas e relatórios.

### Moeda

- **Moeda Padrão** — A moeda principal para preços e contabilidade.
- **Múltiplas Moedas** — Ative para permitir que os clientes vejam preços na moeda preferida deles com conversão automática usando taxas de câmbio em tempo real.

Configure moedas adicionais em **Configurações > Configurações da Loja > Moeda**.

## Configurações de Comércio Eletrônico

### Compra sem Cadastro

Permita compras sem criar uma conta:
- Fluxo de checkout mais rápido
- Menos atrito para compradores pela primeira vez
- Captura de menos dados dos clientes

### Tempo para Criação de Conta

Controle em que momento os clientes são convidados a criar uma conta:

| Opção | Descrição |
|--------|-------------|
| **Após a Compra (Recomendado)** | Incentive a criação de conta após um pedido bem-sucedido — aproveite o bom will pós-venda para melhorar a conversão |
| **Durante o Checkout** | Crie uma conta antes do processamento do pagamento |
| **Antes do Checkout** | Exija uma conta antes de fazer compras (não recomendado — reduz a conversão) |

Você também pode definir uma **Mensagem de Criação de Conta** personalizada para explicar os benefícios do cadastro.

### Padrões de Estoque

- **Rastrear Estoque** — Ative o controle de estoque globalmente
- **Limite de Estoque Baixo** — Nível de estoque em que alertas de estoque baixo são enviados para o e-mail do administrador (padrão: 10 unidades)

### Inteligência de Estoque

![Cartão de Inteligência de Estoque mostrando os campos Default Reorder Lead Time, Safety Stock Multiplier, Velocity Calculation Window, Allow Backorders by Default, e Low Stock Alert Frequency](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Essas configurações ajustam os cálculos automáticos de reposição, estoque de segurança e velocidade de vendas, e controlam como situações de falta de estoque e estoque baixo são tratadas.

- **Prazo Padrão para Reposição (Dias)** — Quantos dias normalmente levam para receber o reabastecimento do seu fornecedor uma vez que você faça o pedido (padrão: 14).

A previsão usa isso para sinalizar produtos que precisam de reposição *agora* para evitar falta de estoque antes da chegada do novo fornecimento.
- **Multiplicador de Estoque de Segurança** — Uma margem aplicada sobre a demanda esperada para absorver picos de vendas ou atrasos do fornecedor.

Por exemplo, um multiplicador de `1.5` cria uma margem de 50% acima do seu estoque de segurança calculado; `2.0` o dobra.

Aumente este valor para produtos onde a falta de estoque é custosa (mais vendidos, itens sazonais); reduza-o para estoque de giro lento que você não deseja supercomprar.
- **Janela de Cálculo de Velocidade (Dias)** — A janela de retrospecto que o Spwig usa para calcular a velocidade de vendas de cada produto, o que por sua vez impulsiona as sugestões de reposição e as figuras de dias de suprimento (padrão: 30).

Uma janela mais curta reage mais rapidamente às mudanças recentes na demanda; uma janela mais longa suaviza os picos sazonais para que uma única semana movimentada não distorça a previsão.
- **Permitir Pedidos Pendentes por Padrão** — A configuração inicial de pedidos pendentes aplicada a novos produtos (desativada por padrão).

Cada produto ainda pode sobrescrevê-la individualmente em sua própria página de produto, e os produtos existentes mantêm a configuração que já possuem — alterar isso apenas muda o padrão com que os novos produtos começam, não atualiza retroativamente seu catálogo.
- **Frequência de Alertas de Estoque Baixo** — Com que frequência seu aplicativo móvel Spwig é notificado sobre estoque baixo: **Tempo real** envia uma notificação push no momento em que um produto ultrapassa seu limite de estoque baixo; **Resumo Diário** e **Resumo Semanal** enviam, em vez disso, uma única notificação push resumindo todos os produtos atualmente com estoque baixo nessa programação.

Esta configuração só tem efeito enquanto **Alertas de Estoque Baixo** (Configurações de E-mail, abaixo) estiver ativado — com os alertas desativados, nenhuma notificação é enviada em nenhuma frequência.

### Documentos e Faturamento

![Cartão de Documentos e Faturamento mostrando os campos Tax ID / VAT Number, Invoice Footer Text, Packing Slip Footer Text e Document Logo Width preenchidos com valores de exemplo](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Estes campos preenchem as faturas e notas de embalagem geradas pelo Spwig para pedidos — por exemplo, quando um comerciante baixa ou envia por e-mail uma fatura em PDF, ou imprime uma nota de embalagem para um envio.

- **Tax ID / VAT Number** — Seu número de identificação fiscal da empresa. Impresso nas faturas geradas para que elas atendam aos requisitos locais de documentação fiscal.
- **Invoice Footer Text** — Texto livre exibido na parte inferior de todas as faturas geradas. Usos comuns: condições de pagamento ("Pagamento devido em 30 dias"), uma mensagem de agradecimento ou detalhes de transferência bancária.
- **Packing Slip Footer Text** — Texto livre exibido na parte inferior de todas as notas de embalagem geradas. Usos comuns: instruções de devolução ou uma nota para a equipe de armazém/fulfillment.
- **Document Logo Width (px)** — A largura do logotipo da sua loja conforme aparece nas faturas em PDF e notas de embalagem geradas (padrão: 200px). A altura escala automaticamente para corresponder, preservando as proporções do seu logotipo. A própria imagem do logotipo vem do seu **Logo** (Branding, acima) — logotipos SVG não são desenhados em documentos PDF, então faça upload de uma versão PNG ou JPG do seu logotipo se você usar arte vetorial na loja.

## Configurações de E-mail

Configure as configurações de entrega de e-mail em **Settings > Email Accounts** e **Settings > Email Templates**. Veja [Email Configuration](/help/email-configuration) para detalhes completos.

Principais configurações de e-mail disponíveis nas Configurações da Loja:

- **Order Confirmation Emails** — Ativar ou desativar e-mails de confirmação automáticos
- **Shipping Notification Emails** — Ativar ou desativar notificações de atualização de envio
- **Low Stock Alerts** — Enviar alertas para o e-mail do administrador quando o estoque ficar abaixo do limite
- **Email Delivery Mode** — Ao vivo (entrega normal), Pausado (segurar todos os e-mails) ou Apenas Log (registrar, mas nunca enviar)
- **Test Redirect Email** — Redirecionar todos os e-mails de saída para um único endereço para testes

## Configurações de Segurança

### Autenticação de Dois Fatores (2FA)

Controle se os funcionários são obrigados a usar a autenticação de dois fatores:


| Configuração | Descrição |
|---------|-------------|
| **Opcional** | O pessoal pode escolher ativar 2FA, mas não é obrigatório |
| **Recomendado** | O pessoal vê um aviso incentivando-os a configurar o 2FA |
| **Obrigatório** | O pessoal não pode acessar o painel de administração até que o 2FA esteja ativado |

- **Período de Graça (Dias)** — Quantos dias o pessoal têm para configurar o 2FA após a ativação da regra
- **Permitir Dispositivos Confiáveis** — Permita que o pessoal pulem a verificação do 2FA em dispositivos reconhecidos por um número definido de dias

## Consentimento de Cookies

Configure o banner de consentimento de cookies exibido aos visitantes da loja:

- **Consentimento de Cookies Habilitado** — Mostre ou oculte o banner de cookies
- **Posição do Banner** — Onde o banner aparece na tela (barra inferior, popup no canto, etc.)
- **Modo de Consentimento** — Notícia simples, opt-in ou opt-out
- **Título e Texto do Banner** — Cabeçalho e descrição personalizáveis exibidos aos visitantes
- **Descrições de Categoria** — Descrições separadas para cookies de análise, marketing e funcional

Todos os campos de texto do banner suportam traduções para lojas multilíngues.

## Comunicações

A aba **Comunicações** controla como sua loja obtém, confirma e permite que os clientes gerencie o consentimento para e-mails e SMS de marketing. Essas configurações moldam sua postura de conformidade legal (GDPR para e-mails, TCPA para SMS), então revise-as com seu próprio aconselhador jurídico antes do lançamento — Spwig fornece os controles, não o aconselhamento.

![Aba Comunicações mostrando os cartões de Consentimento de Marketing por E-mail, Preferências & Cancelamento e Consentimento de SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consentimento de Marketing por E-mail

- **Ativar Confirmação Dupla para E-mails de Marketing** — Quando ativado, um cliente que opta por marketing por e-mail recebe um e-mail de confirmação e deve clicar no link dele antes de Spwig enviá-lo qualquer mensagem de marketing. Quando desativado, marcar a caixa de opção de inscrição em marketing é suficiente. Ativado por padrão, de acordo com as melhores práticas do GDPR.
- **Estado Padrão de Inscrição em Marketing** — O estado inicial de inscrição em marketing aplicado a novas contas de clientes. Desativado por padrão (opt-out do GDPR), então novos clientes começam sem inscrição em e-mails de marketing até que ativamente optem por isso.

Quando a confirmação dupla estiver ativada, optar por inscrição aciona um e-mail de confirmação com um link de verificação. Até que o cliente clique nele, ele é registrado como inscrito, mas não confirmado, e os envios de marketing os ignoram — e-mails transacionais (confirmações de pedidos, atualizações de envio, redefinições de senha) nunca são afetados por essa configuração.

### Preferências & Cancelamento

- **Ativar Centro de Preferências do Cliente** — Quando ativado, os clientes podem gerenciar suas preferências de e-mail e SMS em uma página de autogestão vinculada ao seu painel de conta. Quando desativado, essa página e sua API de suporte retornam indisponíveis e o link do painel de controle é ocultado. Links de cancelamento de uma só vez nos seus e-mails funcionam da mesma forma — esse escape é necessário para conformidade e não é afetado por esse interruptor.
- **Coletar Motivos de Cancelamento** — Quando ativado, a página de cancelamento de um só toque pergunta ao cliente um breve motivo antes da confirmação: *Recebo muitos e-mails*, *O conteúdo não é relevante para mim*, *Nunca me inscrevi nisso*, *Já não estou mais interessado*, ou *Outro*. O motivo escolhido pelo cliente é registrado no histórico de auditoria de consentimento para que você possa revisar os padrões de cancelamento ao longo do tempo.

### Consentimento de SMS

- **Exigir Verificação de SMS** — Quando ativado (o padrão), um cliente deve verificar seu número de telefone com um código de uma vez antes de Spwig enviá-lo qualquer SMS, incluindo mensagens de marketing. Quando desativado, marcar a caixa de opção de inscrição em SMS é suficiente para iniciar o envio. Esse padrão foi alterado para **ativado** para segurança TCPA — desative-o somente se tiver outro passo de verificação em seu fluxo de inscrição.

## Modo de Manutenção

Ative o modo de manutenção para manter sua loja offline temporariamente:
- Exibe uma mensagem de manutenção personalizada aos visitantes
- Você pode vincular uma **Página de Manutenção** construída no Page Builder para uma experiência de marca completa de manutenção
- Restringe o acesso somente aos usuários do admin
- Útil durante atualizações ou migrações importantes

## Redes Sociais

Vincule os perfis de redes sociais da sua loja. Eles aparecem no rodapé e nos modelos de e-mail:

- **URL do Facebook**
- **URL do Twitter**
- **URL do Instagram**
- **URL do LinkedIn**

## Padrões de SEO

Defina as metatags padrão usadas quando as páginas não possuem configurações de SEO próprias:

- **Meta Title** — Título padrão da página (máximo de 60 caracteres)
- **Meta Description** — Descrição padrão exibida nos resultados de busca (máximo de 160 caracteres)
- **Meta Keywords** — Palavras-chave padrão separadas por vírgulas

## Configurações de Impostos

Configure a coleta de impostos em **Settings > Tax Settings**:

1. **Método de Cálculo** — Pelo endereço de entrega, endereço de cobrança ou localização da loja
2. **Alíquotas de Imposto** — Defina alíquotas por região e classe fiscal do produto
3. **Exibição de Impostos** — Exibir preços com imposto, sem imposto ou ambos

## Dicas

- Defina seu fuso horário corretamente antes de processar qualquer pedido — isso afeta todos os timestamps e relatórios.
- Ative o checkout como convidado para melhorar as taxas de conversão.
- Preencha o endereço da sua empresa para cálculos precisos de frete e impostos.
- Envie tanto um logotipo quanto um favicon para uma experiência profissional e com marca.
- Use o momento de criação de conta **After Purchase** para obter as melhores taxas de registro.
- Ative a aplicação da autenticação de dois fatores para funcionários para proteger o admin da sua loja.
- Teste os fluxos de e-mail usando a configuração **Test Redirect Email** antes de ir ao ar.
- Defina o **Default Reorder Lead Time** para corresponder ao seu fornecedor regular mais lento — a previsão de reposição aplica este único valor em todo o seu catálogo, então seja cauteloso com os produtos de maior tempo de entrega.
- Encurte a **Velocity Calculation Window** se você realiza promoções frequentes ou reposições e deseja que a previsão reaja rapidamente às vendas dos últimos dias; alongue-a para uma visão mais estável e menos sujeita a picos da demanda.
- Se você ativar **Allow Backorders by Default**, lembre-se de que isso apenas define o ponto de partida para produtos criados *após* a alteração — revise os produtos existentes individualmente se deseja que os backorders sejam habilitados em todo o seu catálogo atual também.
- Ajuste a **Low Stock Alert Frequency** à forma como você gerencia o estoque: **Real-time** para catálogos de alta rotatividade onde cada risco de falta de estoque precisa de atenção imediata, **Daily Digest** ou **Weekly Summary** para evitar fadiga de alertas em um catálogo maior.
- Preencha seu **Tax ID / VAT Number** e o texto do rodapé antes que a primeira fatura real seja enviada a um cliente — ambos os campos estão em branco por padrão.
- Se o seu **Logo** for um SVG, envie também uma versão PNG ou JPG — **Document Logo Width** não tem efeito em PDFs porque o Spwig não pode desenhar arte SVG em faturas e notas de embalagem geradas.
- Deixe **Enable Double Opt-In for Marketing Emails** ativado, a menos que tenha um motivo específico para desativá-lo — é o padrão mais seguro para o GDPR e protege a reputação do seu remetente mantendo endereços não verificados fora dos seus envios de marketing.
- Deixe **Default Marketing Opt-In State** desativado. Pré-marcar o consentimento de marketing para novas contas compromete o requisito de opt-in do GDPR, mesmo que um cliente possa tecnicamente desmarcá-lo.
- Não desative **Enable Customer Preference Center** apenas para simplificar o painel da sua conta — sem ele, os clientes ainda podem se desinscrever de um único tipo de mensagem, mas perdem a capacidade de ajustar preferências (por exemplo, manter atualizações de envio, mas cancelar o boletim).
- Mantenha **Require SMS Verification** ativado, a menos que seu fluxo de inscrição já confirme números de telefone de outra forma (por exemplo, um login baseado em SMS) — a configuração existe especificamente para mantê-lo dentro das regras do TCPA.

## Solução de Problemas

**Alterações não aparecendo na loja virtual:**
- Limpe o cache do seu navegador
- Execute a limpeza de cache a partir do painel administrativo
- Verifique se o modo de manutenção não está acidentalmente ativado

**E-mails não sendo enviados:**
- Verifique as configurações do seu provedor de e-mail na Configuração de E-mail
- Verifique se o **Email Delivery Mode** está definido como **Live**
- Certifique-se de que o **Test Redirect Email** está em branco se deseja que os e-mails sejam enviados para destinatários reais

**A conversão de moeda não está funcionando:**
- Verifique se seu provedor de taxa de câmbio está conectado
- Verifique as credenciais da API nas configurações de taxa de câmbio
- Tente atualizar as taxas manualmente

**E-mails de marketing não estão chegando aos clientes que se inscreveram:**
- Verifique se **Ativar o Duplo Opt-In para E-mails de Marketing** está ligado — se sim, o cliente deve clicar no link de confirmação no e-mail de verificação antes que o marketing retome
- Peça ao cliente para verificar o spam/cartão de lixo para o e-mail de confirmação
- Confirme que o opt-in do cliente para marketing ainda está ativado em suas preferências — um clique de cancelamento de assinatura o desativa novamente

**Os clientes dizem que não conseguem encontrar o centro de preferências:**
- Verifique se **Ativar o Centro de Preferências do Cliente** está ligado — quando desligado, o link do painel de controle é oculto e a página não está disponível por design
- O link de cancelamento de assinatura em qualquer e-mail de marketing sempre funciona, independentemente deste recurso, então aponte os clientes para ele como alternativa