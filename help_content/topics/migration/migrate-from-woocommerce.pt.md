---
title: Migrando do WooCommerce
---

Se sua loja atualmente funciona no WooCommerce, o assistente de migração do Spwig pode importar seus produtos, clientes, pedidos e conteúdo diretamente via API REST do WooCommerce. Este guia abrange a obtenção das credenciais da API, a execução da importação e duas funcionalidades específicas do WooCommerce que você deve saber antes: o plugin opcional Migration Bridge para dados de afiliados e o suporte embutido para várias extensões populares do WooCommerce.

## Antes de Começar

O WooCommerce tem o maior suporte entre todas as plataformas de origem no assistente de migração. A importação limpa os seguintes itens: categorias (com hierarquia), produtos, imagens e variantes, clientes e endereços, pedidos, avaliações, cupons e posts de blog com suas categorias, tags e imagens.

Perfis de afiliados, registros de comissão e histórico de pagamentos também podem ser importados, mas apenas se você instalar primeiro o plugin Spwig Migration Bridge — veja abaixo. Sem ele, esses dados são simplesmente ignorados.

Também lembre-se:

- Produtos de certas extensões do WooCommerce (assinaturas, pacotes, reservas, cartões-presente) são importados para o recurso correspondente do Spwig, mas nem todos os detalhes são transferidos — veja **Suporte a extensões do WooCommerce** abaixo.
- Campos personalizados em seus produtos, clientes e pedidos são detectados automaticamente e precisam de mapeamento em uma etapa posterior. Veja [Mapeamento de Campos de Migração](migration-field-mapping).
- As opções **Importar configurações de impostos** e **Importar zonas e métodos de envio** do assistente não são aplicadas aos dados importados. Configure as taxas de impostos e envio no Spwig depois — veja [Depois da Migração](after-migration-review).
- A opção **Ajuste de preço** na mesma etapa *faz* efeito para importações do WooCommerce, alterando o preço base de cada produto conforme ele é criado. Deixe-a definida como **Nenhum** a menos que você deseje deliberadamente alterar todos os preços.

Tenha à mão o login de administrador do WordPress e saiba aproximadamente quantos produtos, clientes e pedidos você está importando para que possa verificar os números que o assistente mostrar.

## Obter Credenciais da API REST

O Spwig se conecta ao WooCommerce usando uma chave de API REST gerada do seu administrador do WordPress. Essa chave só precisa de **Leitura** — o Spwig só lê da sua loja durante a migração, ele nunca escreve nada de volta.

1. No WordPress, vá para **WooCommerce > Configurações > Avançado > API REST**
2. Clique em **Adicionar chave**
3. Dê a ela uma descrição (por exemplo, `Spwig Migration`) e defina **Permissões** para **Leitura**
4. Clique em **Gerar chave de API**
5. Copie a **Chave do Consumidor** (`ck_...`) e o **Segredo do Consumidor** (`cs_...`) para um local seguro

> **Importante:** O WooCommerce mostra o Segredo do Consumidor apenas uma vez, no momento em que você o gera. Se você navegar embora antes de copiá-lo, precisará gerar uma nova chave.

## Conectando Sua Loja

Vá para **Importação e Exportação de Dados > Iniciar Nova Migração** no administrador do Spwig e escolha **WooCommerce** na etapa 1. Na etapa 2, insira:

- **URL da Loja** — o endereço completo da web da sua loja, por exemplo `https://mystore.com`
- **Chave do Consumidor** e **Segredo do Consumidor** — os valores que você acabou de copiar

Deixe **Testar a conexão antes de prosseguir** marcado (ativado por padrão) para que o Spwig confirme que pode acessar sua loja e autenticar antes de você continuar — isso detecta erros de digitação e problemas de permissão imediatamente, em vez de meio caminho na importação. Clique em **Próximo** uma vez que ele tenha sucesso.

## Revisando e Selecionando Dados

A etapa 3 puxa contagens em tempo real da sua loja — categorias, produtos, clientes, pedidos, avaliações e cupons — mais uma amostra dos primeiros cinco produtos para que você possa confirmar que está lendo o site certo. Cada checkbox de tipo de dado é automaticamente marcado quando a contagem é superior a zero e desativado quando é zero.

**Opções de Importação**:

- **Pular itens existentes** (ligado) — corresponde os registros entrantes com o que já está no Spwig (SKU para produtos, e-mail para clientes) e pula os duplicados.

Deixe-o ativado a menos que esteja começando com uma loja vazia.
- **Importar imagens de produtos** (ativado) — mais lento, mas compensa.
- **Manter os IDs originais quando possível** (desativado) — o próprio assistente rotula isso como "não recomendado". Deixe-o desativado a menos que você tenha um motivo técnico específico para manter os IDs numéricos do WooCommerce.
- **Tamanho do lote** — 10, 25 (padrão), 50 ou 100 registros por vez.

Lotes menores são adequados para conexões instáveis; lotes maiores terminam mais rápido em uma conexão estável.

## O Plugin Spwig Migration Bridge

O WooCommerce não tem um conceito embutido de programa de afiliados, então, se você opera um por meio de uma extensão de afiliados do WooCommerce, esses dados vivem em tabelas que a API REST padrão não pode ver. O **Spwig Migration Bridge** é um pequeno plugin complementar que você instala no seu site WordPress para expô-los.

O plugin Bridge libera:

- **Perfis de afiliados** — detalhes dos seus afiliados e códigos de referência
- **Registros de comissão** — histórico de comissões vinculado a cada afiliado
- **Histórico de pagamentos** — pagamentos anteriores feitos aos afiliados

É totalmente opcional — pule-o se você não operar um programa de afiliados ou não precisar desse histórico no Spwig.

> **Nota:** Os dados de afiliados só podem ser importados se os pedidos e clientes também estiverem sendo importados na mesma migração, já que comissões e pagamentos estão vinculados a pedidos e clientes específicos.

Para instalar:

1. Na etapa 3, se o plugin ainda não for detectado no seu site, você verá um botão **Download Bridge Plugin** com instruções de instalação
2. Faça o download do arquivo ZIP do plugin
3. No WordPress, vá para **Plugins > Adicionar Novo > Carregar Plugin**, selecione o ZIP, clique em **Instalar Agora**, depois em **Ativar**
4. Volte para o assistente do Spwig e atualize a página — uma caixa de seleção **Afiliados** e um bloco **Dados do Programa de Afiliados** aparecerão, mostrando as contagens encontradas

Você pode desativar e remover o plugin Bridge do WordPress uma vez que sua migração esteja completa.

## Suporte a Extensões do WooCommerce

Se sua loja usar certas extensões populares, os produtos que elas criam são reconhecidos durante a importação e mapeados para a funcionalidade correspondente do Spwig, em vez de serem importados como produtos comuns:

| Extensão do WooCommerce | Local de destino |
|---|---|
| Subscriptions | Planos de assinatura do Spwig |
| Product Add-Ons | Acessórios de produto do Spwig |
| Product Bundles | Pacotes de produto do Spwig |
| Gift Cards (WooCommerce, YITH e PW variantes) | Cartões-presente do Spwig |
| Composite Products | Produtos compostos do Spwig |
| Bookings and Accommodation Bookings | Reservas do Spwig |

> **Nota:** A importação de dados de extensões nunca bloqueia a criação do produto subjacente. Se os dados específicos da extensão de um produto não puderem ser lidos, o produto ainda será importado — apenas como um produto comum, sem sua configuração de assinatura, pacote, reserva ou cartão-presente.

Faça uma verificação aleatória de seus produtos de assinatura, pacote, reserva e cartão-presente após a importação para confirmar que suas configurações específicas da extensão foram transferidas, em vez de assumir que uma importação bem-sucedida carregou todos os detalhes.

## Campos Personalizados

Se você adicionou campos meta personalizados aos seus produtos, clientes ou pedidos do WooCommerce, o Spwig amostra cerca de dez registros de cada tipo para detectar quais campos existem. Você mapeará cada um para um slot de campo personalizado do Spwig ou para um campo de Metadados Geral na etapa 4. Veja [Mapping de Campos de Migração](migration-field-mapping) para o walkthrough completo, incluindo como os mapeamentos são salvos para futuras migrações.

## Executando a Importação

Uma vez que você revisou a etapa 3 e confirmou seus mapeamentos na etapa 4, inicie a importação. Ela é executada em segundo plano — você pode fechar a janela do navegador e ela continua. A etapa 5 mostra o progresso em tempo real com uma linha por tipo de dado (categorias, produtos, clientes, pedidos, avaliações, cupons, posts de blog e afiliados/comissões/pagamentos se o plugin Bridge foi usado) mais um log de atividade expansível.

A etapa 6 mostra seus resultados: o que foi importado, pulado ou falhou, mais uma ferramenta de **Reescrita de Links** se links internos para seu domínio antigo do WooCommerce foram encontrados no conteúdo importado.

Revise com cuidado o resumo, em seguida, siga o checklist em [After Your Migration](after-migration-review) — ele abrange a verificação dos seus dados, a configuração de taxas tributárias e envio (que o assistente não configura para você) e a reescrita de links internos.

## Revogue sua Chave de API

Depois de confirmar que a migração foi concluída com sucesso, volte para **WooCommerce > Configurações > Avançado > API REST** no WordPress e revogue ou exclua a chave que você criou para o Spwig. Não há razão para deixar uma chave de API ativa em sua loja antiga depois que você terminar com ela.

## Dicas

- **Gerar a chave de API imediatamente antes de precisar dela** — como o Segredo do Consumidor é exibido apenas uma vez, crie-a imediatamente antes de iniciar o passo 2 em vez de antecipadamente.
- **Apenas leitura realmente é suficiente** — nunca conceda permissões de Escrita ou Leitura/Escrita; o Spwig apenas lê dados da sua loja WooCommerce.
- **Instale o plugin Bridge antes de iniciar a importação** — você precisará adicioná-lo e atualizar o assistente antes de importar, então verifique se ele está disponível antes de começar em vez de durante o processo.
- **Faça uma verificação parcial de produtos com base em extensões** — assinaturas, pacotes, reservas e cartões-presente são os produtos mais prováveis de precisarem de uma verificação manual após a importação.
- **Uma importação parcial não é limpa automaticamente** — consulte [Migration Troubleshooting](migration-troubleshooting) antes de tentar novamente uma importação falha.
- **Revogue a chave de API quando terminar** — não deixe integrações antigas ativas em uma loja da qual você migrou.