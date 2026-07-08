---
title: Configuração de GeoIP
---

O GeoIP permite que sua loja detecte automaticamente de onde cada visitante está vindo com base em seu endereço IP. Isso ativa recursos baseados em localização em toda a sua loja — desde exibir a moeda correta por padrão, até executar regras comerciais geográficas, até ver quebras de nível de país em seus analytics.

Sua loja vem pré-configurada com o serviço de GeoIP da Spwig, então a detecção geográfica funciona pronta para uso. Você também pode conectar provedores adicionais para maior precisão, usar um banco de dados que você baixar sozinho ou depender de cabeçalhos de um CDN para consultas sem latência.

## Como os provedores funcionam

Navegue até **Clientes > Provedores de GeoIP** para ver os provedores configurados para sua loja. Cada provedor lida com consultas de IP para localização usando um método diferente. Quando um visitante chega, sua loja consulta os provedores ativos na ordem de prioridade e usa o primeiro resultado bem-sucedido.

Vários provedores podem estar ativos ao mesmo tempo — os números de prioridade mais baixos são tentados primeiro. Se o provedor de maior prioridade falhar ou retornar nenhum dado, o próximo é tentado automaticamente.

### Tipos de provedores disponíveis

| Provedor | Descrição |
|----------|-------------|
| **Spwig GeoIP** | Consulta baseada em nuvem padrão via serviço da Spwig. Não requer configuração. |
| **MaxMind GeoLite2** | Banco de dados offline da MaxMind. Alta precisão. Requer uma chave de licença gratuita. |
| **DB-IP Lite** | Banco de dados offline da DB-IP. Baixe do site deles. |
| **IP2Location LITE** | Banco de dados offline da IP2Location. Requer um registro gratuito. |
| **Cabeçalhos de Borda do CDN** | Lê cabeçalhos de localização injetados pelo seu CDN (ex: Cloudflare). Zero de latência. |
| **Dicas do Navegador** | Usa o fuso horário/idioma fornecido pelo navegador como um sinal de localização suave. |
| **Provedor Personalizado** | Um componente de provedor instalado do mercado de componentes da Spwig. |

## Adicionando um provedor

### Usando o serviço Spwig GeoIP (padrão)

O provedor Spwig GeoIP é adicionado automaticamente em novas instalações. Verifique se ele aparece na lista e se **Ativo** está marcado. Nenhuma configuração adicional é necessária.

### Adicionando um banco de dados MaxMind GeoLite2

A MaxMind oferece um banco de dados offline gratuito que fornece resultados precisos sem enviar consultas para um serviço externo.

1. Registre-se para uma conta gratuita em maxmind.com e gere uma chave de licença
2. Navegue até **Clientes > Provedores de GeoIP** e clique em **+ Adicionar Provedor de GeoIP**
3. Preencha o formulário:
   - **Nome**: `MaxMind GeoLite2` (ou qualquer nome descritivo)
   - **Tipo de Provedor**: MaxMind GeoLite2
   - **Ativo**: marcado
   - **Prioridade**: `1` (mais baixa que o padrão da Spwig para tentar primeiro, ou mais alta para usar como fallback)
   - **Chave de Licença**: cole sua chave de licença da MaxMind
   - **URL do Banco de Dados**: o URL de download do seu painel de controle da conta da MaxMind
4. Clique em **Salvar**

Após salvar, selecione o provedor na lista e use a ação **Atualizar bancos de dados do provedor selecionado** para verificar se o URL do banco de dados está acessível.

### Adicionando cabeçalhos de borda do CDN

Se sua loja estiver atrás de um CDN que injeta cabeçais de geolocalização (como o `CF-IPCountry` do Cloudflare), você pode usar esses cabeçais para detecção de país instantânea, sem latência.

1. Navegue até **Clientes > Provedores de GeoIP** e clique em **+ Adicionar Provedor de GeoIP**
2. Defina **Tipo de Provedor** para **Cabeçalhos de Borda do CDN**
3. Defina **Prioridade** para `0` (maior prioridade, já que cabeçais são a fonte mais rápida)
4. No campo **Configuração**, especifique qual cabeçalho seu CDN usa:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Clique em **Salvar**

## Testando um provedor

Após adicionar um provedor, você pode verificar se ele está funcionando corretamente:

1. Na lista de Provedores de GeoIP, selecione o provedor usando seu checkbox
2. Abra o menu suspenso **Ação** e escolha **Testar provedores selecionados**
3. Clique em **Ir**

A Spwig enviará uma consulta de teste para um endereço IP conhecido (o DNS público da Google, `8.8.8.8`) e mostrará o resultado. Um teste bem-sucedido exibe o país retornado e o tempo de resposta em milissegundos.

## Definindo a prioridade do provedor

Quando múltiplos provedores estão ativos, o campo **Prioridade** controla qual é tentado primeiro.

Números mais baixos significam maior prioridade.

Por exemplo, para usar os cabeçalhos do CDN primeiro (mais rápido) e recorrer ao Spwig GeoIP:

| Provedor | Prioridade |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Você pode editar a prioridade diretamente na visão de lista — a coluna **Prioridade** é editável diretamente no local.

## Monitoramento do desempenho do provedor

Cada registro do provedor rastreia suas próprias estatísticas de precisão:

- **Total de Consultas** — número total de consultas de IP tentadas
- **Consultas Bem-sucedidas** — consultas que retornaram um resultado
- **Consultas com Falha** — consultas que retornaram nenhum dado ou um erro
- **Média de Resposta (ms)** — tempo médio de resposta em milissegundos
- **Precisão** — porcentagem de consultas bem-sucedidas

Se um provedor mostrar uma taxa de precisão baixa ou tempos de resposta altos, considere ajustar sua prioridade ou desativá-lo em favor de uma opção com melhor desempenho.

## Mapeamentos de país

Navegue até **Clientes > Mapeamentos de País** para configurar os valores padrão por país para moeda, idioma, imposto e envio. Cada entrada de país controla:

- **Moeda Padrão** — a moeda pré-selecionada para visitantes desse país
- **Idioma Padrão** — o idioma exibido para visitantes desse país
- **Taxa de Imposto** — a porcentagem padrão de imposto aplicada para esse país
- **É Membro da UE** / **Requer IVA** — usado para a lógica de conformidade com impostos da UE
- **Zona de Envio** — vincula o país a uma zona de envio
- **Suporta Pagamento na Entrega** — habilita o pagamento na entrega para esse país

Você pode editar os campos **Ativo**, **Moeda Padrão** e **Idioma Padrão** diretamente na lista, sem abrir cada registro.

## Dicas

- O provedor Spwig GeoIP funciona imediatamente, sem configuração — adicione provedores adicionais apenas se precisar de maior precisão ou operação offline
- Se você usar o Cloudflare, o provedor CDN Edge Headers é a melhor escolha: ele não adiciona latência e não conta contra qualquer cota de API
- Mantenha apenas os provedores que realmente precisar ativos — ter muitos provedores ativos não melhora a precisão se o primeiro já tiver sucesso
- Verifique as estatísticas de precisão semanalmente e desative qualquer provedor com uma taxa de sucesso inferior a 80%
- Os mapeamentos de país são usados como valores padrão; os clientes sempre podem alterar sua moeda e idioma manualmente no site de vendas