---
title: Gerenciamento de Leitores de Cartão
---

O gerenciamento de leitores de cartão acompanha dispositivos físicos de hardware de pagamento, atribui-os a terminais POS e monitora seu status operacional. Cada leitor de cartão representa hardware real (Stripe S700, WisePOS E ou P400) registrado com seu provedor de pagamento. Os leitores têm uma relação um-para-um com os terminais — cada caixa registradora tem seu próprio leitor de cartão. Monitore o status do leitor (online, offline, ocupado) em tempo real, personalize telas de splash com sua marca e resolva problemas de conectividade antes que afetem a experiência de checkout dos clientes.

Use o gerenciamento de leitores de cartão para garantir que o hardware de pagamento esteja configurado, atribuído e operacional em todas as localizações.

![Lista de Leitores de Cartão](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Entendendo Leitores de Cartão

Leitores de cartão são dispositivos de hardware físicos que processam pagamentos com cartões de crédito e débito:

**Componentes de Hardware**:
- Encaixe para cartões com chip EMV
- Antena NFC (sem contato/pagamento por toque)
- Leitor de faixa magnética (legado, raramente usado)
- Tela de exibição (mostra o valor, solicita PIN, assinatura)
- Conectividade de rede (Wi-Fi ou Ethernet, dependendo do modelo)

**Integração de Software**:
- Os leitores se conectam à API do Stripe Terminal (baseada em nuvem, não conexão direta com o dispositivo POS)
- O terminal POS solicita pagamento via API
- O Stripe roteia a solicitação para o leitor registrado
- O leitor processa o cartão e retorna o resultado para o POS
- Não é necessária conexão USB/Bluetooth entre o POS e o leitor

**Um Leitor por Terminal**:
- Cada terminal POS deve ter exatamente um leitor de cartão atribuído
- A relação um-para-um garante responsabilidade clara e simplifica a solução de problemas
- Múltiplos terminais não podem compartilhar um leitor (causa conflitos)

## Tipos de Leitores de Cartão

O Spwig POS suporta leitores de cartão Stripe Terminal:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Terminal Android todo-em-um com tela sensível ao toque de 5 polegadas de cor
- Opção de impressora integrada (recibo térmico)
- Melhor para: Checkout de varejo completo, restaurantes (prompt de gorjeta na tela colorida)
- Conectividade: apenas Wi-Fi
- Tela de splash: cor completa 480×800 retrato

**Stripe Reader S700** (`stripe_s700`):
- Leitor de balcão com tela LCD monocromática
- Design compacto, resistente à água
- Melhor para: Varejo padrão, balcões de checkout compactos
- Conectividade: Wi-Fi ou Ethernet
- Tela de splash: monocromática 480×800 retrato

**Verifone P400** (`verifone_p400`):
- Leitor de balcão legado (modelo mais antigo)
- Ainda suportado, mas não recomendado para novas implantações
- Melhor para: Implantações existentes (não substitua o hardware funcionando)
- Conectividade: Wi-Fi ou Ethernet
- Tela de splash: monocromática 480×800 retrato

**Compatibilidade Futura**:
- Modelos adicionais de leitores podem ser adicionados conforme o Stripe Terminal expande suas ofertas de hardware
- O menu suspenso de tipo de leitor é preenchido automaticamente com base nas capacidades do provedor

## Fluxo de Trabalho de Registro de Leitores

**Etapa 1: Comprar e Receber o Hardware**
- Ordene o leitor no Stripe (stripe.com/terminal) ou em revendedor autorizado
- Desembale e ligue o leitor
- Conecte-se à rede Wi-Fi (siga o processo de configuração na tela do leitor)

**Etapa 2: Registrar no Painel de Controle do Stripe**
- Navegue até **Painel de Controle do Stripe > Terminal > Leitores**
- Clique em **Registrar Novo Leitor**
- Siga o processo de emparelhamento na tela (o leitor exibe o código de registro)
- Atribua o leitor a uma localização do Stripe (deve corresponder à localização na configuração do provedor de pagamento)
- Anote o **ID do Leitor** (parece `tmr_ABC123...`)

**Etapa 3: Sincronizar com o Spwig (Automático)**
- O Spwig descobre automaticamente os leitores registrados em sua localização do Stripe
- Uma tarefa em segundo plano sincroniza a cada 30 minutos
- Novos leitores aparecem na lista **POS > Leitores de Cartão** dentro de 30 minutos

**Etapa 4: Atribuir a um Terminal (Manual)**
- Navegue até **POS > Leitores de Cartão**
- Encontre o leitor descoberto recentemente na lista
- Clique para editar
- Selecione **Terminal** para atribuir o leitor
- Salve

**Etapa 5: Testar Pagamento**
- No terminal POS, processe uma transação de teste
- Selecione o método de pagamento com cartão
- O POS deve descobrir o leitor atribuído
- Use o cartão de teste do Stripe (4242 4242 4242 4242) para concluir o teste
- Verifique se o pagamento é concluído com sucesso

Se o leitor não aparecer durante o teste, verifique a atribuição do terminal e o status do leitor.

## Monitoramento do Status do Leitor

Os leitores relatam o status para a API do Stripe Terminal, que o Spwig sincroniza a cada 5 minutos:

**Online** (verde) - O leitor está ligado, conectado à rede e pronto para aceitar pagamentos

**Offline** (vermelho) - O leitor está desligado, desconectado da rede ou inacessível

**Ocupado** (amarelo) - O leitor está processando atualmente uma transação de pagamento

**Última vez visto** - Carimbo de data/hora da última verificação do leitor com a API do Stripe
- Atualiza a cada ~2 minutos quando o leitor está online
- Útil para diagnosticar problemas de conectividade ("leitor saiu offline há 3 horas" = problema de energia ou rede durante o horário de funcionamento)

**Casos de Uso do Status**:
- **Verificação pré-abertura**: Verifique se todos os leitores da loja estão online antes de abrir as portas
- **Solução de problemas**: "Caixa registradora 3 não está aceitando cartões" → Verifique o status do leitor → Mostra offline → Verifique energia/rede
- **Auditoria**: "Foram processados pagamentos no Terminal 5 ontem?" → Verifique o carimbo de data/hora da última vez vista

## Atribuição de Terminal

Os leitores de cartão usam uma **relação um-para-um** com os terminais:

**Por que a Atribuição Importa**:
- Durante o pagamento, o POS precisa saber qual leitor comunicar
- Múltiplos terminais compartilhando um leitor causam conflitos (dois caixas não podem usar o mesmo leitor simultaneamente)
- Leitores não atribuídos não serão usados (hardware orfã)

**Regras de Atribuição**:
- Cada terminal pode ter **exatamente um** leitor de cartão atribuído
- Cada leitor de cartão pode ser atribuído a **exatamente um** terminal
- Atribuir um leitor ao Terminal A automaticamente o desvincula do terminal anterior

**Alterando Atribuições**:
- Edite o registro do leitor
- Altere o campo **Terminal** para o novo terminal
- Salve
- O terminal anterior perde a atribuição do leitor de cartão (mostrará o erro "Nenhum leitor atribuído" durante o pagamento)

**Leitores Não Atribuídos**:
- Os leitores descobertos recentemente começam não atribuídos
- Os leitores não atribuídos aparecem na lista, mas não são utilizáveis
- Atribua-os a um terminal para ativar

## Personalização da Tela de Splash

As telas de splash dos leitores exibem a marca na tela voltada para o cliente quando ocioso:

**O que é Tela de Splash?**
- Imagem mostrada na tela do leitor quando não está processando um pagamento
- Substitui o logotipo padrão do Stripe pela sua marca
- Visível aos clientes enquanto aguardam no checkout

**Splash Gerado Automaticamente vs Personalizado**:

**Splash Gerado Automaticamente** (padrão):
- O Spwig gera a tela de splash a partir do logotipo da loja (se o logotipo estiver configurado nas configurações da loja)
- Automaticamente dimensionado para as especificações do leitor (480×800 retrato)
- Monocromático para S700/P400, colorido para WisePOS E
- Nenhuma configuração necessária

**Splash Personalizado** (avançado):
- Carregue sua própria imagem personalizada de tela de splash
- Controle total sobre o design e a marca
- Deve atender aos requisitos da imagem (veja abaixo)

**Requisitos para Splash Personalizado**:
- **Resolução**: Exatamente 480×800 pixels (orientação retrato)
- **Formato**: PNG ou JPG
- **S700/P400**: Apenas monocromático (preto e branco, sem cinza)
- **WisePOS E**: Cor completa suportada
- **Tamanho do arquivo**: <200KB

**Definindo Splash Personalizado**:
1. Edite o registro do leitor de cartão
2. Carregue a imagem no campo **Imagem de Sobrescrita de Splash** (ou selecione da Biblioteca de Mídia)
3. Salve
4. O splash sincroniza com o leitor dentro de 5 minutos

**Removendo Splash Personalizado**:
- Limpe o campo **Imagem de Sobrescrita de Splash**
- Salve
- O leitor retorna ao splash gerado automaticamente (ou ao padrão do Stripe se não houver logotipo da loja)

**Testando Splash**:
- Após carregar, espere 5 minutos para sincronização
- Visite o dispositivo do leitor
- Verifique se o splash aparece na tela ociosa
- Verifique a qualidade da imagem, centralização e contraste

## Configuração de Splash do Stripe

Atrás dos bastidores, o Spwig gerencia a configuração da tela de splash do Stripe Terminal:

**stripe_splash_file_id** - ID interno do Stripe para o arquivo de imagem de splash carregado
- Automaticamente definido quando o splash é carregado
- Usado para referenciar o splash na API do Stripe

**stripe_splash_config_id** - ID interno do Stripe para a configuração de splash
- Liga o arquivo de splash ao leitor
- Gerenciado automaticamente ao atribuir o splash ao leitor

Esses campos são somente leitura e gerenciados automaticamente — você não precisa interagir com eles diretamente.

## Solução de Problemas de Problemas Comuns

**Problema 1: Leitor mostra offline, mas está ligado**
- **Causas**: Problema de conectividade de rede, senha Wi-Fi alterada, leitor fora do alcance
- **Solução**: Verifique as configurações de rede do leitor, reconecte-se ao Wi-Fi, verifique se a API do Stripe está acessível a partir da rede

**Problema 2: POS diz "Nenhum leitor atribuído" durante o pagamento**
- **Causa**: Leitor não atribuído ao terminal, ou atribuição incompleta
- **Solução**: Edite o leitor, atribua ao terminal, salve, teste o pagamento novamente

**Problema 3: Leitor ocupado indefinidamente (preso na tela de pagamento)**
- **Causa**: Transação expirou ou travou, estado do leitor não foi redefinido
- **Solução**: Reinicie o leitor (ciclo de energia), entre em contato com o suporte do Stripe se persistir

**Problema 4: Splash personalizado não aparece**
- **Causas**: Imagem com resolução incorreta, não sincronizada ainda, requisito de monocromático não atendido (S700/P400)
- **Solução**: Verifique se a imagem é exatamente 480×800, espere 5 minutos para sincronização, garanta monocromático para leitores sem cor

**Problema 5: Leitor registrado no Stripe, mas não aparece no Spwig**
- **Causa**: Leitor registrado em uma localização do Stripe diferente da ID da localização do provedor
- **Solução**: No Painel de Controle do Stripe, verifique se a localização do leitor corresponde à ID da localização do provedor

## Dicas

- **Um leitor por terminal** - Não compartilhe leitores entre terminais; evita conflitos e simplifica a responsabilidade
- **Registre os leitores antes de implantar no chão** - Conclua o registro no Stripe e a atribuição no Spwig antes de colocar o leitor no checkout
- **Teste telas de splash no local** - A variação de contraste varia por modelo de leitor e iluminação; verifique se o splash parece bom no ambiente real
- **Monitore o status antes da abertura** - Verifique a lista de leitores todas as manhãs para garantir que todos os leitores estejam online antes da abertura da loja
- **Etique o hardware fisicamente** - Use um fabricante de etiquetas para marcar o leitor com o nome do terminal ("Leitor do Terminal 1") para identificação fácil durante a solução de problemas
- **Mantenha os leitores em energia ininterruptível** - Interrupções de energia durante transações podem corromper o estado do leitor; recomenda-se um UPS
- **Documente os números de série dos leitores** - Mantenha um registro dos números de série para garantia e suporte (encontrado na etiqueta do hardware do leitor)
- **Atualize o firmware dos leitores** - O Stripe envia atualizações de firmware automaticamente, mas verifique periodicamente se os leitores estão na versão mais recente (verifique o Painel de Controle do Stripe)

