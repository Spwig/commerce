---
title: Configurando as Configurações da Loja
---

As Configurações da Loja é o local central para configurar a identidade, localização, marca e preferências operacionais da sua loja. Navegue até **Configurações > Configurações da Loja** para começar.

![aba geral das configurações da loja](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## aba geral

A **aba Geral** contém as configurações principais da identidade da sua loja.

### Identidade da Loja

- **Nome da Loja** — O nome exibido nos títulos das páginas, e-mails e cabeçalho do painel de administração.
- **Slogan** — Uma breve descrição da sua loja, usada em SEO e compartilhamento em redes sociais.
- **URL do Site** — O endereço web público da sua loja. É usado em e-mails, geração de sitemap e construção de links.

### Informações de Contato

- **E-mail de Contato** — Recebe notificações de pedidos e é exibido nas comunicações com os clientes.
- **Número de Telefone** — Número de telefone opcional exibido no rodapé e e-mails.

### Endereço da Empresa

Digite seu endereço completo (rua, cidade, estado, CEP, país). Isso é usado para:
- Cálculos da origem do envio
- Cálculos de impostos
- Requisitos legais e notas fiscais

## Branding

### Logotipo

Faça o upload do logotipo da sua loja (PNG ou SVG recomendado, ~200x50px com fundo transparente). O logotipo aparece em:
- Cabeçalho da loja
- Modelos de e-mail
- Painel de administração

### Ícone de Favorito (Favicon)

Faça o upload de um ícone quadrado (ICO ou PNG, 32x32px). Ele aparece como:
- Ícone da aba do navegador
- Ícone de favorito
- Ícone da tela inicial do celular

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
- **Múltiplas Moedas** — Ative para permitir que os clientes vejam preços na moeda de preferência com conversão automática usando taxas de câmbio em tempo real.

Configure moedas adicionais em **Configurações > Configurações da Loja > Moeda**.

## Configurações de Comércio Eletrônico

### Checkout como Visitante

Permita compras sem criar uma conta:
- Fluxo de checkout mais rápido
- Menos fricção para compradores pela primeira vez
- Captura menos dados dos clientes

### Tempo para Criação de Conta

Controle quando os clientes são convidados a criar uma conta:

| Opção | Descrição |
|--------|-------------|
| **Após a Compra (Recomendado)** | Peça para criar uma conta após um pedido bem-sucedido — aproveita a boa vontade pós-compra para melhorar a conversão |
| **Durante o Checkout** | Crie uma conta antes do processamento do pagamento |
| **Antes do Checkout** | Exija uma conta antes de fazer compras (não recomendado - reduz a conversão) |

Você também pode definir uma **Mensagem de Criação de Conta** personalizada para explicar os benefícios do cadastro.

### Padrões de Estoque

- **Rastrear Estoque** — Ative o controle de estoque globalmente
- **Limite de Estoque Baixo** — Nível de estoque em que alertas de estoque baixo são enviados para o e-mail do administrador (padrão: 10 unidades)

## Inteligência de Estoque

![cartão de inteligência de estoque mostrando os campos Prazo Padrão de Reabastecimento e Multiplicador de Estoque de Segurança](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Essas configurações ajustam os cálculos automáticos de reposição, estoque de segurança e velocidade de vendas, e controlam como situações de falta de estoque e estoque baixo são tratadas.

- **Prazo Padrão de Reabastecimento (dias)** — Quantos dias normalmente levam para receber o reabastecimento do seu fornecedor uma vez que você coloca o pedido (padrão: 14).

A previsão usa isso para sinalizar produtos que precisam ser reabastecidos *agora* para evitar falta de estoque antes que o novo estoque chegue.
- **Multiplicador de Estoque de Segurança** — Um buffer aplicado sobre a demanda esperada para absorver picos de vendas ou atrasos no fornecedor.

Por exemplo, um multiplicador de `1,5` inclui um buffer de 50% acima do estoque de segurança calculado; `2,0` o duplica.

Aumente esse valor para produtos em que faltar estoque é caro (vendas populares, itens sazonais); reduza-o para estoque de baixa rotação que você não deseja encomendar em excesso.
- **Período de Cálculo de Velocidade (dias)** — O período de consulta que o Spwig usa para calcular a velocidade de vendas de cada produto, o que por sua vez influencia as sugestões de reposição e os valores de dias de estoque (padrão: 30 dias).

Um período mais curto reage mais rapidamente às mudanças recentes na demanda; um período mais longo suaviza os picos sazonais, de modo que uma única semana movimentada não distorça a previsão.
- **Permitir Pedidos de Devolução por Padrão** — A configuração inicial de pedidos de devolução aplicada a novos produtos (desativado por padrão).

Cada produto ainda pode substituí-lo individualmente na própria página do produto, e os produtos existentes mantêm qualquer configuração que já tenham — alterar isso só muda o que os novos produtos começam com, não atualiza retroativamente seu catálogo.
- **Frequência do Alerta de Estoque Baixo** — Com que frequência o aplicativo móvel Spwig é notificado sobre estoque baixo: **Em tempo real** envia uma notificação por push no momento em que um produto ultrapassa seu limite de estoque baixo; **Resumo Diário** e **Resumo Semanal** enviam, em vez disso, uma única notificação por push resumindo todos os produtos com estoque baixo naquela programação.

Este ajuste entra em vigor somente enquanto **Alertas de Estoque Baixo** (Configurações de E-mail, abaixo) estiver ativado — com os alertas desativados, nenhuma notificação é enviada em qualquer frequência.

### Documentos e Notas Fiscais

![Cartão de Documentos e Notas Fiscais mostrando os campos Tax ID / Número de IVA, Texto do Rodapé da Nota Fiscal e Texto do Rodapé da Nota de Embalagem preenchidos com valores de exemplo](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Esses campos preenchem as notas fiscais e os recibos de embalagem gerados pelo Spwig para pedidos — por exemplo, quando um comerciante baixa ou envia por e-mail uma nota fiscal em PDF, ou imprime um recibo de embalagem para um envio.

- **Tax ID / Número de IVA** — Seu número de identificação fiscal da empresa. Impresso nas notas fiscais geradas para que atendam aos requisitos locais de documentação fiscal.
- **Texto do Rodapé da Nota Fiscal** — Texto livre exibido no final de cada nota fiscal gerada. Usos comuns: termos de pagamento ("Pagamento devido dentro de 30 dias"), uma mensagem de agradecimento ou detalhes de transferência bancária.
- **Texto do Rodapé da Nota de Embalagem** — Texto livre exibido no final de cada recibo de embalagem gerado. Usos comuns: instruções de devolução ou uma nota para a equipe de armazém/fulfillment.
- **Largura do Logotipo do Documento (px)** — A largura do logotipo da loja conforme aparece nas notas fiscais e recibos de embalagem em PDF (padrão: 200px). A altura escala automaticamente para combinar, preservando as proporções do logotipo. A imagem do logotipo vem de seu **Logotipo** (Marca, acima) — logotipos SVG não são desenhados em documentos PDF, então faça o upload de uma versão PNG ou JPG do seu logotipo se você usar arte vetorial na loja.

## Configurações de E-mail

Configure as configurações de envio de e-mail em **Configurações > Contas de E-mail** e **Configurações > Modelos de E-mail**. Veja [Configuração de E-mail](/help/email-configuration) para detalhes completos.

Configurações-chave de e-mail disponíveis nas Configurações da Loja:

- **E-mails de Confirmação de Pedido** — Ative ou desative e-mails automáticos de confirmação
- **E-mails de Notificação de Envio** — Ative ou desative notificações de atualizações de envio
- **Alertas de Estoque Baixo** — Envie alertas para o e-mail do administrador quando o estoque cair abaixo do limite
- **Modo de Entrega de E-mail** — Live (entrega normal), Pausado (manter todos os e-mails) ou Apenas Registro (registrar, mas nunca enviar)
- **E-mail de Redirecionamento de Teste** — Redirecione todos os e-mails de saída para um endereço único para testes

## Configurações de Segurança

### Autenticação de Dois Fatores (2FA)

Controle se os funcionários são obrigados a usar autenticação de dois fatores:

| Configuração | Descrição |
|---------|-------------|
| **Opcional** | Os funcionários podem escolher ativar a 2FA, mas não é obrigatório |
| **Recomendado** | Os funcionários veem um aviso incentivando-os a configurar a 2FA |
| **Obrigatório** | Os funcionários não podem acessar o painel de administração até que a 2FA esteja ativada |

Preserve todos os formatos de markdown, caminhos de imagens, blocos de código e termos técnicos.

- **Período de Carência (Dias)** — Quantos dias os funcionários têm para configurar 2FA após a ativação
- **Permitir Dispositivos Confiáveis** — Permita que os funcionários pulam a verificação de 2FA em dispositivos reconhecidos por um número definido de dias

## Consentimento de Cookies

Configure o banner de consentimento de cookies exibido aos visitantes da loja:

- **Consentimento de Cookies Habilitado** — Exibir ou ocultar o banner de cookies
- **Posição do Banner** — Onde o banner aparece na tela (barra inferior, pop-up de canto, etc.)
- **Modo de Consentimento** — Notícia simples, opt-in ou opt-out
- **Título e Texto do Banner** — Título e descrição personalizáveis exibidos aos visitantes
- **Descrições de Categoria** — Descrições separadas para cookies de análise, marketing e funcionais

Todos os campos de texto do banner suportam traduções para lojas multilíngues.

## Comunicações

A aba **Comunicações** controla como sua loja obtém, confirma e permite que os clientes gerenciem o consentimento para e-mails e SMS de marketing. Essas configurações moldam sua postura de conformidade legal (GDPR para e-mails, TCPA para SMS), então revise-as com seu próprio aconselhador jurídico antes do lançamento — Spwig fornece os controles, não o aconselhamento.

![A aba Comunicações mostra os cartões de Consentimento de Marketing por E-mail, Preferências & Cancelamento e Consentimento de SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consentimento de Marketing por E-mail

- **Ativar Otimização Dupla para E-mails de Marketing** — Quando ativado, um cliente que opta por e-mails de marketing recebe um e-mail de confirmação e deve clicar no link dele antes de Spwig enviá-lo qualquer mensagem de marketing. Quando desativado, marcar a caixa de opção de opt-in de marketing é suficiente. Ativado por padrão, de acordo com as melhores práticas do GDPR.
- **Estado Padrão de Opt-In de Marketing** — O estado inicial de opt-in de marketing aplicado a novas contas de clientes. Desativado por padrão (opt-out do GDPR), então novos clientes começam sem inscrição em e-mails de marketing até que ativamente optem por isso.

Quando a otimização dupla estiver ativada, optar por inscrever-se aciona um e-mail de confirmação com um link de verificação. Até que o cliente clique nele, ele é registrado como optado, mas não confirmado, e os envios de marketing pulam-no — e-mails transacionais (confirmações de pedido, atualizações de envio, redefinições de senha) nunca são afetados por esta configuração.

### Preferências & Cancelamento

- **Ativar Centro de Preferências do Cliente** — Quando ativado, os clientes podem gerenciar seus e-mails e SMS de preferências em uma página de autosserviço vinculada ao seu painel de controle. Quando desativado, essa página e sua API de suporte retornam indisponíveis e o link do painel de controle é ocultado. Links de cancelamento de um clique em seus e-mails continuam funcionando da mesma forma — esse escape é necessário para conformidade e não é afetado por este interruptor.
- **Coletar Motivos de Cancelamento** — Quando ativado, a página de cancelamento de um clique pergunta ao cliente um breve motivo antes da confirmação: *Recebo muitos e-mails*, *O conteúdo não é relevante para mim*, *Nunca me inscrevi nisso*, *Já não estou mais interessado*, ou *Outro*. A razão pela qual o cliente seleciona é registrada no histórico de auditoria de consentimento para que você possa revisar os padrões de cancelamento ao longo do tempo.

### Consentimento de SMS

- **Exigir Verificação de SMS** — Quando ativado (padrão), um cliente deve verificar seu número de telefone com um código de uma vez antes de Spwig enviá-lo qualquer SMS, incluindo mensagens de marketing. Quando desativado, marcar a caixa de opção de opt-in de SMS é suficiente para iniciar o envio. Este padrão foi alterado para **ativado** para segurança TCPA — desative-o somente se tiver outro passo de verificação em seu fluxo de inscrição.

## Modo de Manutenção

Ative o modo de manutenção para manter sua loja offline temporariamente:
- Exibe uma mensagem de manutenção personalizada aos visitantes
- Você pode vincular uma **Página de Manutenção** construída no Page Builder para uma experiência de marca completa de manutenção
- Restringe o acesso somente aos usuários do admin
- Útil durante atualizações ou migrações importantes

## Mídia Social

Link seu perfis de mídia social da loja. Eles aparecem no rodapé e nos modelos de e-mail:

- **URL do Facebook**
- **URL do Twitter**
- **URL do Instagram**
- **URL do LinkedIn**

## Padrões de SEO

Preserve todos os formatações de markdown, caminhos de imagem, blocos de código e termos técnicos.

Defina tags meta padrão usados quando as páginas não tiverem configurações de SEO próprias:

- **Título Meta** — Título padrão da página (máx. 60 caracteres)
- **Descrição Meta** — Descrição padrão exibida nos resultados de busca (máx. 160 caracteres)
- **Palavras-Chave Meta** — Palavras-chave separadas por vírgula padrão

## Configurações de Impostos

Configure a cobrança de impostos em **Configurações > Configurações de Impostos**:

1. **Método de Cálculo** — Pelo endereço de envio, endereço de cobrança ou localização da loja
2. **Alíquotas de Impostos** — Defina as alíquotas por região e classe de produto
3. **Exibição de Preços** — Exibir preços com impostos, sem impostos ou ambos

## Dicas

- Defina o fuso horário corretamente antes de processar quaisquer pedidos — ele afeta todos os registros de data/hora e relatórios.
- Ative o checkout como convidado para melhorar as taxas de conversão.
- Preencha o endereço da sua empresa para cálculos precisos de frete e impostos.
- Faça o upload de um logotipo e favicon para uma experiência profissional e com marca registrada.
- Use o timing de criação de conta **Após a Compra** para obter melhores taxas de registro.
- Ative a execução da autenticação de dois fatores para o pessoal para proteger o administrador da loja.
- Teste os fluxos de e-mail usando a configuração **Redirecionamento de E-mail de Teste** antes de ir para a produção.
- Defina o **Tempo Padrão para Reordenação** para corresponder ao fornecedor mais lento — a previsão de reordenação aplica esse único valor em toda a sua catalogação, então fique do lado do produto com o tempo de entrega mais longo.
- Preencha seu **ID de Imposto / Número de CPF** e texto do rodapé antes da primeira fatura real enviada ao cliente — ambos os campos estão em branco por padrão.
- Deixe **Ativar Confirmação Dupla para E-mails de Marketing** ligado, a menos que você tenha um motivo específico para desativá-lo — é o padrão mais seguro para o GDPR e protege sua reputação de remetente mantendo endereços não verificados fora de seus envios de marketing.
- Deixe **Estado Padrão de Consentimento para Marketing** desligado. Marcar como selecionado o consentimento de marketing para novas contas prejudica o requisito de opt-in do GDPR, mesmo que um cliente possa tecnicamente desmarcar.
- Não desative **Ativar o Centro de Preferências do Cliente** apenas para simplificar seu painel de controle — sem ele, os clientes ainda podem se descadastrar de um tipo de mensagem, mas perdem a capacidade de ajustar preferências (ex.: manter atualizações de envio, mas descartar o boletim informativo).
- Mantenha **Exigir Verificação por SMS** ligado, a menos que seu fluxo de inscrição já confirme os números de telefone de outra forma (ex.: login baseado em SMS) — o recurso existe especificamente para mantê-lo dentro das regras TCPA.

## Solução de Problemas

**Mudanças não aparecem na loja virtual:**
- Limpe o cache do navegador
- Execute uma limpeza de cache pelo painel de administração
- Verifique se o modo de manutenção está ativado acidentalmente

**E-mails não estão sendo enviados:**
- Verifique as configurações do provedor de e-mail na Configuração de E-mail
- Verifique se o **Modo de Entrega de E-mail** está definido para **Live**
- Certifique-se de que o **E-mail de Redirecionamento de Teste** esteja em branco, se quiser que os e-mails sejam enviados para destinatários reais

**Conversão de moeda não está funcionando:**
- Verifique se seu provedor de taxa de câmbio está conectado
- Verifique as credenciais da API nas configurações da taxa de câmbio
- Tente atualizar as taxas manualmente

**E-mails de marketing não estão chegando aos clientes que optaram por recebê-los:**
- Verifique se **Ativar Confirmação Dupla para E-mails de Marketing** está ligado — se sim, o cliente deve clicar no link de confirmação no e-mail de verificação antes que os envios de marketing voltem a funcionar
- Peça ao cliente para verificar o spam/junk por causa do e-mail de confirmação
- Confirme se o opt-in de marketing do cliente ainda está ativo em suas preferências — um clique de cancelamento desativa-o

**Clientes dizem que não conseguem encontrar o centro de preferências:**
- Verifique se **Ativar o Centro de Preferências do Cliente** está ligado — quando desativado, o link do painel de controle é ocultado e a página fica indisponível por design
- O link de cancelamento em qualquer e-mail de marketing sempre funciona, independentemente desse recurso, então aponte os clientes para ele como alternativa