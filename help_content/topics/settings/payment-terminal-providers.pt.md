---
title: Fornecedores de Terminal de Pagamento
---

Fornecedores de terminal de pagamento permitem a aceitação de cartões de crédito e débito nos seus terminais de POS. O Stripe Terminal é o principal provedor suportado, oferecendo leitores de cartões modernos (S700, WisePOS E, P400), taxas de processamento competitivas e integração sem embaraço. Configure contas de provedores com credenciais de API, monitore o status da conexão em tempo real e gerencie múltiplos provedores se estiver operando em diferentes regiões. O sistema de provedores é extensível — processadores de pagamento adicionais podem ser integrados via o framework de provedores se o Stripe Terminal não operar em seu mercado.

Use provedores de pagamento para aceitar pagamentos por cartão de forma segura, acompanhar o status do processamento de pagamentos e gerenciar atribuições de leitores entre terminais.

![Lista de Fornecedores de Pagamento](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Visão Geral de Fornecedores de Pagamento

Fornecedores de pagamento são serviços de terceiros que processam pagamentos por cartão em nome do seu negócio:

**Responsabilidades do Fornecedor**:
- Autorizar transações de cartão em tempo real
- Comunicar-se com leitores físicos de cartão
- Lidar com a segurança do pagamento (conformidade PCI, criptografia)
- Transferir fundos para sua conta bancária (liquidação)
- Fornecer relatórios de transação e gestão de disputas

**Papel do Spwig**:
- Roteia solicitações de pagamento para o provedor configurado
- Armazena credenciais do provedor criptografadas
- Monitora o status da conexão
- Associa leitores a terminais
- Registra os resultados dos pagamentos nos pedidos

## Stripe Terminal (Provedor Principal)

O Stripe Terminal é o provedor de pagamento recomendado para a maioria dos varejistas:

**Funcionalidades**:
- Leitores de cartões de chip EMV modernos
- Suporte a pagamentos sem contato (NFC) (Apple Pay, Google Pay, cartões de toque)
- Gestão de disputas integrada
- Autorização em tempo real
- API amigável para desenvolvedores
- Disponível em 40+ países

**Preços** (até 2024, verifique as taxas atuais):
- Taxas de transação: 2,7% + $0,05 por transação presencial (EUA)
- Nenhuma taxa mensal, nenhuma taxa de instalação, nenhuma taxa de conformidade PCI
- Hardware do leitor de cartão: Compra única ($59-$299 dependendo do modelo)

**Regiões Suportadas**:
- Estados Unidos, Canadá, Reino Unido, União Europeia, Austrália, Cingapura e mais
- Verifique a disponibilidade do Stripe: https://stripe.com/terminal

**Leitores Suportados**:
- BBPOS WisePOS E (terminal Android all-in-one)
- Stripe Reader S700 (leitor de balcão)
- Verifone P400 (leitor legado, ainda suportado)

## Configuração do Stripe Terminal

**Etapa 1: Criar Conta do Stripe**
- Registre-se em stripe.com
- Complete a verificação do negócio (conta bancária, ID fiscal)
- Ative os pagamentos

**Etapa 2: Habilitar o Stripe Terminal**
- No painel do Stripe, navegue até **Produtos > Terminal**
- Clique em **Começar**
- Aceite os termos de serviço do Terminal

**Etapa 3: Criar Localização**
- O Stripe Terminal requer uma "Localização" que representa seu site de varejo físico
- Navegue até **Terminal > Localizações**
- Clique em **Criar Localização**
- Insira o endereço e detalhes da loja
- Salve o ID da localização (parece `tml_1ABC123...`)

**Etapa 4: Gerar Chave de API**
- Navegue até **Desenvolvedores > Chaves de API**
- Localize sua **Chave Secreta** (começa com `sk_live_...` para produção, `sk_test_...` para testes)
- Copie a chave secreta (não compartilhe publicamente)

**Etapa 5: Configurar no Spwig**
- Navegue até **POS > Fornecedores de Pagamento**
- Clique em **+ Adicionar Fornecedor de Pagamento**
- Selecione **Fornecedor**: "Stripe Terminal"
- Insira **Chave de API Secreta** (do passo 4)
- Insira **ID da Localização** (do passo 3)
- Salvar

**Etapa 6: Testar Conexão**
- Após salvar, o status do provedor deve mudar para "Conectado" (verde)
- Se o status mostrar "Erro" (vermelho), verifique a chave de API e o ID da localização
- Verifique a mensagem de erro na visão de detalhes do provedor

![Formulário de Adição de Fornecedor de Pagamento](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Campos de Configuração do Fornecedor

**Chave do Fornecedor** - Selecione o processador de pagamento:
- **stripe_terminal** - Stripe Terminal (recomendado)
- **manual** - Entrada de pagamento manual (apenas para testes, sem processamento real)
- Provedores adicionais podem aparecer se instalados via sistema de componentes

**Credenciais (Criptografadas)** - Estrutura JSON contendo credenciais de API:
- Criptografadas automaticamente antes do armazenamento
- Nunca visíveis em texto simples após o salvamento
- Estrutura de exemplo (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Configurações do Fornecedor** - Configuração adicional (específica do provedor):
- Descrição da declaração (aparece na declaração de cartão de crédito do cliente)
- Captura automática (capturar pagamentos autorizados imediatamente vs captura manual)
- Sobrescrita de moeda (se a conta do provedor usar uma moeda diferente da loja)

**Status da Conexão** - Indicador de status em tempo real:
- **Conectado** (verde) - O provedor está acessível e configurado corretamente
- **Erro** (vermelho) - Conexão falhou ou credenciais inválidas
- **Desconhecido** (cinza) - Não testado ainda (imediatamente após a criação)

**Última Testada** - Carimbo de tempo da última testagem de conexão
- Atualiza automaticamente quando transações são processadas
- Acione o teste manualmente via ação de administrador **Testar Conexão**

## Monitoramento do Status da Conexão

O sistema monitora a conectividade do provedor para alertar você sobre problemas antes que os clientes tentem pagamentos:

**Teste Automático**:
- Cada transação de pagamento aciona um teste de conexão (por necessidade)
- Trabalho de fundo testa a conexão a cada 6 horas (monitoramento preventivo)

**Significados de Status**:

**Conectado** - API do provedor está acessível, credenciais são válidas, pronta para processar pagamentos

**Erro** - Causas comuns:
- Chave de API inválida (revogada, expirada ou incorreta)
- ID de localização inválido (localização excluída no Stripe, ID incorreto inserido)
- Problemas de conectividade de rede (firewall bloqueando API do Stripe)
- Interrupção de serviço do Stripe (raro)

**Desconhecido** - Provedor nunca testado ainda (conta nova pendente da primeira transação)

**Resolvendo o Status de Erro**:
1. Verifique a mensagem de erro na visão de detalhes do provedor (explica o problema específico)
2. Verifique se a chave de API ainda é válida no painel do Stripe
3. Verifique se o ID da localização ainda existe no painel do Stripe
4. Teste a conexão manualmente via ação de administrador **Testar Conexão**
5. Atualize as credenciais se necessário

![Detalhes do Fornecedor de Pagamento](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Comparação de Leitores de Cartão Suportados

O Stripe Terminal oferece várias opções de hardware de leitores:

| Modelo | Tipo | Métodos de Pagamento | Display | Melhor Para | Preço |
|-------|------|---------------------|---------|------------|-------|
| **WisePOS E** | All-in-one | Chip EMV, NFC, swipe | Tela sensível ao toque colorida de 5" | POS de varejo completo com recursos | ~$299 |
| **S700** | Balcão | Chip EMV, NFC, swipe | LCD monocromático | Checkout de varejo padrão | ~$249 |
| **P400** | Balcão | Chip EMV, NFC, swipe | LCD monocromático | Implantações legadas | ~$299 |

**Vantagens do WisePOS E**:
- Baseado em Android (executa aplicativos, pode exibir conteúdo personalizado)
- Tela sensível ao toque colorida (melhor UX para solicitações de gorjeta, captura de assinatura)
- Impressora de recibos integrada (opcional)
- Velocidade de transação mais rápida

**Vantagens do S700**:
- Custo mais baixo do que o WisePOS E
- Pés de apoio compactos
- Design resistente a respingos

**P400** (modelo mais antigo):
- Ainda suportado, mas não recomendado para novas implantações
- Processamento de cartões de chip mais lento do que S700/WisePOS E

Todos os leitores se conectam ao POS do Spwig via API do Stripe Terminal (não é necessária conexão direta USB/Bluetooth com o dispositivo POS).

## Considerações de Segurança

**Criptografia de Credenciais**:
- Todas as credenciais do provedor são criptografadas em repouso no banco de dados
- A criptografia usa a chave secreta do aplicativo (definida nas configurações do aplicativo)
- Credenciais nunca aparecem em logs ou mensagens de erro

**Permissões da Chave de API**:
- Use **chaves de API restritas** em produção (limite as permissões apenas ao Terminal)
- Não use chaves secretas irrestritas (acesso mais amplo do que o necessário = risco de segurança)
- No painel do Stripe, crie uma chave restrita com apenas **permissões de Terminal**

**Conformidade com PCI**:
- O Stripe Terminal lida com a conformidade com PCI (os dados do cartão nunca tocam os servidores do Spwig)
- Números de cartões são processados totalmente no hardware do leitor → servidores do Stripe → redes de cartões
- O Spwig apenas armazena os resultados dos pagamentos (aprovado/recusado), nunca detalhes do cartão

**Rotação de Chaves**:
- Roteie chaves de API anualmente como prática de segurança recomendada
- Ao rotacionar, atualize as credenciais na configuração do provedor
- Chaves antigas podem ser revogadas no painel do Stripe após confirmar que a nova chave funciona

## Múltiplos Provedores

Alguns varejistas precisam de múltiplas contas de provedor:

**Operações com Múltiplas Moedas**:
- Lojas nos EUA usam conta do Stripe EUA (processa USD)
- Lojas na Europa usam conta do Stripe EUA (processa EUR)
- Configure um provedor separado por moeda

**Provedores de Backup**:
- Provedor principal (Stripe Terminal)
- Provedor de backup (entrada manual) quando os leitores apresentarem falhas
- O caixa seleciona o provedor ao iniciar o pagamento

**Teste vs Produção**:
- Provedor de teste com chave de API `sk_test_...`
- Provedor de produção com chave de API `sk_live_...`
- Mude os provedores após a fase de teste

## Solução de Problemas com Problemas Comuns

**Problema 1: Status mostra "Erro" com a mensagem "Chave de API inválida"**
- **Causa**: Chave de API revogada ou copiada incorretamente
- **Solução**: Gere uma nova chave de API no painel do Stripe, atualize as credenciais do provedor, teste a conexão

**Problema 2: Leitor não descoberto durante o pagamento**
- **Causa**: Leitor não registrado à localização do provedor
- **Solução**: No painel do Stripe, verifique se o leitor está registrado à mesma ID de localização usada na configuração do provedor

**Problema 3: Pagamentos recusados apesar de cartão válido**
- **Causa**: Conta do Stripe não totalmente ativada (verificação pendente)
- **Solução**: Complete a verificação do negócio no painel do Stripe (conta bancária, ID fiscal)

**Problema 4: Status da conexão mostra "Desconhecido" e nunca atualiza**
- **Causa**: Provedor nunca testado (nenhuma transação tentada)
- **Solução**: Use a ação de administrador **Testar Conexão** para acionar manualmente o teste de conectividade

## Dicas

- **Modo de teste antes da produção** - Use chaves de API de teste do Stripe (`sk_test_...`) para configuração inicial e testes
- **Um provedor por moeda** - Não tente processar EUR com conta do Stripe baseada em USD; crie provedores separados
- **Monitore o status da conexão semanalmente** - Monitoragem proativa previne falhas de pagamento no checkout
- **Restrinja permissões da chave de API** - Limite as chaves de API do Stripe apenas às permissões do Terminal (princípio do menor privilégio)
- **Documente IDs de localização** - Mantenha um registro de qual localização do Stripe corresponde a qual loja física
- **Teste atribuição de leitores** - Após a configuração do provedor, teste o pagamento com leitor de cartão real para verificar o fluxo de ponta a ponta
- **Mantenha contato do Stripe atualizado** - Certifique-se de que as informações de contato do negócio no Stripe correspondam às atuais (importante para disputas, conformidade)