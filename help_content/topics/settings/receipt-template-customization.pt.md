---
title: Personalizaçāo de Modelos de Recibo
---

Modelos de recibo controlam a aparência e o conteúdo dos recibos impressos em impressoras térmicas nos seus terminais de POS. Personalize o cabeçalho e o rodapé, adicione seu logotipo, configure campos de conformidade (IDs fiscais, números de registro comercial) e inclua códigos QR promocionais. Os modelos suportam alvo de escopo - crie um modelo padrão para todas as lojas, modelos específicos para grupos para regiões ou modelos específicos para lojas para locais individuais. O sistema usa regras de precedência de escopo para determinar qual modelo é aplicado ao imprimir um recibo.

Use modelos de recibo para manter a consistência da marca, atender aos requisitos de conformidade regional e aumentar o engajamento do cliente por meio de elementos promocionais.

![Lista de Modelos de Recibo](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Básicos de Modelos de Recibo

Modelos de recibo definem a estrutura e o conteúdo dos recibos impressos por impressoras térmicas ESC/POS. Cada modelo especifica:

**Configuração Física**:
- Largura do papel (58mm ou 80mm)
- Imagem do logotipo (monocromática para impressão térmica)
- Tamanho da fonte e espaçamento

**Seções de Conteúdo**:
- Texto do cabeçalho (nome da loja, endereço, informações de contato)
- Dados dinâmicos da transação (itens, preços, totais, métodos de pagamento)
- Texto do rodapé (política de devolução, mensagem de agradecimento, mídia social)
- Campos de conformidade (IDs fiscais, números de registro comercial)
- Código QR promocional com rótulo

**Alvo de Escopo**:
- Modelo padrão (aplica-se a todas as lojas, a menos que seja substituído)
- Modelo de grupo (aplica-se a todas as lojas em um grupo)
- Modelo de loja (aplica-se a uma loja específica/depósito)

## Regras de Precedência de Escopo

Quando um terminal imprime um recibo, o sistema seleciona um modelo usando esta hierarquia (maior prioridade para menor):

| Prioridade | Escopo | Exemplo | Caso de Uso |
|------------|--------|---------|-------------|
| **1** | Específico da loja | Modelo da loja de Paris | Requisitos de conformidade fiscais únicos da França |
| **2** | Específico do grupo | Modelo de lojas europeias | Exibição de IVA para todas as localizações da UE |
| **3** | Padrão | Modelo global | Fallback para todas as lojas não configuradas |

**Como Funciona**:
1. Verifique se a loja tem um modelo dedicado (específico do depósito)
2. Se não, verifique se o grupo da loja tem um modelo de grupo
3. Se não, use o modelo padrão

**Exemplo**:
- Modelo padrão: "Recibo Padrão" (sem atribuição de escopo)
- Modelo de grupo: "Recibo da UE" (atribuído ao grupo de lojas europeias) - inclui registro de IVA
- Modelo de loja: "Recibo de Paris" (atribuído ao depósito de Paris) - inclui número SIRET francês

**Resultado**:
- Terminal da loja de Paris: Usa "Recibo de Paris" (mais específico)
- Terminal da loja de Berlim (no grupo de lojas europeias, sem modelo de loja): Usa "Recibo da UE" (nível de grupo)
- Terminal da loja de Nova York (sem grupo, sem modelo de loja): Usa "Recibo Padrão" (fallback padrão)

## Configuração da Largura do Papel

Impressoras de recibo térmico usam papel de 58mm ou 80mm. Escolha com base no hardware da sua impressora:

| Largura do Papel | Caracteres por Linha | Melhor Para | Uso Típico |
|------------------|----------------------|-------------|------------|
| **58mm** | ~32 caracteres | Pequeno footprint, portátil | Caminhões de comida, POS móvel, quiosques |
| **80mm** | ~48 caracteres | Varejo padrão | Maioria das lojas de varejo, restaurantes |

**Não misturar larguras**: Todos os terminais usando o mesmo modelo devem ter impressoras com a mesma largura de papel. Se você tiver tipos de impressoras mistos, crie modelos separados para cada largura.

**Limites de Tamanho do Logotipo**:
- **58mm**: Largura máxima 384 pixels (recomendado: 350px)
- **80mm**: Largura máxima 576 pixels (recomendado: 550px)

Logos que excedem a largura máxima são automaticamente reduzidos, o que pode reduzir a qualidade.

## Configuração do Logotipo

Logos de recibo devem ser **monocromáticos** (apenas preto e branco) para compatibilidade com impressoras térmicas:

**Requisitos do Logotipo**:
- Formato do arquivo: PNG, JPG ou WebP
- Modo de cor: Monocromático (pixels pretos em fundo branco)
- Dimensões recomendadas:
  - Papel 58mm: 350px de largura × 100-150px de altura
  - Papel 80mm: 550px de largura × 150-200px de altura
- Tamanho do arquivo: <100KB (impressoras térmicas têm memória limitada)

**Criando Logos Monocromáticos**:
1. Comece com seu logotipo regular (cor ou escala de cinza)
2. Use um editor de imagem para converter em preto e branco puro (sem cinzas)
3. Aumente o contraste para garantir que os elementos pretos sejam sólidos
4. Exporte como PNG com fundo transparente ou branco

**Posicionamento do Logotipo**:
- Sempre centralizado horizontalmente
- Impresso no topo do recibo (acima do texto do cabeçalho)
- Seguido por espaçamento automático (evita aglomeração com conteúdo)

**Selecionando o Logotipo**:
- Clique em **Procurar Biblioteca de Mídia** no formulário do modelo
- Selecione o ativo do logotipo monocromático
- A pré-visualização mostra como o logotipo aparecerá no recibo

**Sem Logotipo**: Deixe o campo de logotipo em branco se preferir branding apenas com texto (o texto do cabeçalho pode incluir o nome da loja).

## Texto do Cabeçalho

O texto do cabeçalho aparece imediatamente após o logotipo (ou no topo se não houver logotipo). Conteúdo típico:

**Nome da Loja e Endereço**:
```
Your Store Name
123 Main Street
City, State 12345
Phone: (555) 123-4567
```

**Horário de Funcionamento**:
```
Monday-Friday: 9am-9pm
Saturday-Sunday: 10am-6pm
```

**Slogan ou Tagline**:
```
Quality Products, Exceptional Service
```

**Formatação**:
- Use quebras de linha para separar informações
- Alinhamento centralizado automaticamente
- Mantenha as linhas abaixo do limite de caracteres para a largura do papel (32 caracteres para 58mm, 48 para 80mm)

**Variáveis Disponíveis** (opcional):
- `{store_name}` - Substituído pelo nome do depósito
- `{order_date}` - Substituído pela data da transação
- `{order_number}` - Substituído pelo número do pedido

A maioria dos varejistas usa texto estático em vez de variáveis para consistência do cabeçalho.

## Texto do Rodapé

O texto do rodapé aparece após os detalhes da transação (itens, totais, pagamento). Conteúdo típico:

**Política de Devolução**:
```
Returns within 30 days with receipt
Store credit or exchange only
```

**Mensagem de Agradecimento**:
```
Thank you for shopping with us!
Follow us @yourstore
```

**Atendimento ao Cliente**:
```
Questions? Call (555) 123-4567
or email support@yourstore.com
```

**Dicas de Formatação**:
- Mantenha as informações mais importantes primeiro (política de devolução, contato)
- Use quebras de linha para legibilidade
- Considere adicionar uma linha de separação (`---`) entre as seções

## Campos de Conformidade

Muitas jurisdições exigem informações específicas nos recibos:

**Rótulo do ID Fiscal** - Rótulo personalizável para o número de identificação fiscal:
- EUA: "Tax ID" ou "EIN"
- UE: "VAT Number" ou "VAT Reg No"
- Canadá: "GST/HST Number"
- Austrália: "ABN"

**Valor do ID Fiscal** - O número de identificação real:
- Inserido uma vez no modelo, aparece em todos os recibos
- Exemplo: "VAT Number: GB123456789"

**Rótulo de Registro Empresarial** - Rótulo personalizável para o registro empresarial:
- França: "SIRET"
- Alemanha: "Handelsregister"
- Reino Unido: "Company Registration Number"

**Valor de Registro Empresarial** - O número real de registro:
- Exemplo: "SIRET: 123 456 789 00010"

**Mostrar Powered by Spwig** - Alternar para exibir ou ocultar o branding "Powered by Spwig" (habilitado por padrão - apoia o desenvolvimento da plataforma) - desative para operações de branco (white-label)

**Exemplos de Conformidade por Região**:

**União Europeia**:
- Rótulo do ID Fiscal: "VAT Number"
- Valor do ID Fiscal: "GB123456789"
- Exiba o número de registro da empresa se exigido pelo país

**Estados Unidos**:
- Geralmente, não há exigência de ID fiscal em recibos (varia por estado)
- Pode incluir EIN para transações B2B

**França (Específica)**:
- SIRET obrigatório em todos os recibos
- Rótulo de Registro Empresarial: "SIRET"
- Valor de Registro Empresarial: "123 456 789 00010"

**Austrália**:
- ABN (Número de Empresas Australianas) recomendado para empresas registradas no GST
- Rótulo do ID Fiscal: "ABN"

Verifique os requisitos locais de recibos antes de ir ao ar.

## Promoções com Código QR

Inclua um código QR no final dos recibos para impulsionar o engajamento do cliente:

**URL do Código QR** - O destino ao ser escaneado:
- Revisão: `https://yourstore.com/reviews/leave-review`
- Programa de fidelidade: `https://yourstore.com/loyalty/join`
- Desconto para próxima compra: `https://yourstore.com/discount/THANKYOU`
- Mídia social: `https://instagram.com/yourstore`
- Página inicial do site: `https://yourstore.com`

**Rótulo do Código QR** - Texto exibido acima do código QR:
- "Escaneie para deixar uma avaliação e obtenha 10% de desconto na próxima compra"
- "Junte-se ao nosso programa de fidelidade - escaneie aqui"
- "Siga-nos no Instagram - escaneie para se conectar"
- "Avalie sua experiência"

**Melhores Práticas para Código QR**:
- Use URLs curtas (URLs longas criam códigos densos e difíceis de escanear)
- Teste o código QR com várias câmeras de celular antes de implantar
- Inclua uma proposta de valor clara no rótulo (o que o cliente obtém ao escanear)
- Rastreie os escaneios do código QR para medir a eficácia (use URL com parâmetro de rastreamento)

**Códigos QR Dinâmicos** (Avançado):
- Use um serviço de redirecionamento de QR (bit.ly, tinyurl) para criar uma URL curta
- Aponte o redirecionamento para destinos diferentes sazonalmente, sem reimprimir recibos
- Exemplo: `https://bit.ly/yourstoreqr` → redireciona para a promoção atual

## Criando Modelos para Diferentes Escopos

**Modelo Padrão** (recomendado como ponto de partida):
1. Navegue até **POS > Modelos de Recibo**
2. Clique em **+ Adicionar Modelo de Recibo**
3. Deixe os campos **Depósito** e **Grupo de Lojas** em branco (isso torna-o o padrão)
4. Configure a largura do papel correspondente ao seu tipo de impressora mais comum
5. Adicione logotipo, cabeçalho, rodapé
6. Configure campos de conformidade para seu mercado principal
7. Salve

Este modelo se aplica a todas as lojas, a menos que seja substituído.

**Modelo de Grupo** (para variações regionais):
1. Crie um novo modelo
2. Selecione **Grupo de Lojas** (ex: "Lojas Europeias")
3. Deixe **Depósito** em branco
4. Ajuste os campos de conformidade para a região (ex: formatação de IVA)
5. Ajuste o texto do cabeçalho (ex: endereço regional)
6. Salve

Este modelo se aplica a todas as lojas no grupo.

**Modelo de Loja** (para necessidades específicas de local):
1. Crie um novo modelo
2. Selecione **Depósito** (ex: "Loja de Paris")
3. Ajuste todos os campos para esse local específico
4. Salve

Este modelo se aplica apenas a essa uma loja.

**Testando Modelos**:
- Processar transação de teste no terminal
- Imprimir recibo
- Verificar clareza do logotipo, alinhamento do texto, campos de conformidade, escaneabilidade do código QR
- Ajustar o modelo e retestar se necessário

## Layouts Comuns de Recibo

**Recibo Mínimo** (caminhões de comida, pop-ups):
- Nenhum logotipo (economia de espaço)
- Cabeçalho: Nome da loja e telefone apenas
- Rodapé: Mensagem de agradecimento
- Nenhum código QR

**Recibo de Varejo Padrão**:
- Logotipo (marca monocromática)
- Cabeçalho: Nome completo da loja, endereço, horário
- Conformidade: ID fiscal
- Rodapé: Política de devolução, mensagem de agradecimento
- Código QR: Solicitação de avaliação

**Recibo de Varejo Premium**:
- Logotipo (marca completa da palavra)
- Cabeçalho: Slogan, endereço, contato
- Conformidade: ID fiscal, registro empresarial
- Rodapé: Política de devolução, atendimento ao cliente, mídia social
- Código QR: Inscrição no programa de fidelidade

**Cadeia de Múltiplas Localizações**:
- Modelo padrão: Marca corporativa, políticas padrão
- Modelos de grupo: Conformidade regional (IVA para UE, GST para Canadá)
- Modelos de loja: Endereço e telefone específicos da localização

## Gerenciando Múltiplos Modelos

**Convenção de Nomenclatura de Modelo**:
- Use o escopo no nome: "Recibo Padrão", "Recibo do Grupo da UE", "Recibo da Loja de Paris"
- Ajuda a identificar qual modelo se aplica onde ao revisar a lista

**Alterações de Modelo**:
- As alterações são aplicadas imediatamente aos recibos futuros
- Recibos anteriores (já impressos) não são afetados
- Teste as alterações em um terminal de baixo tráfego antes de implantar em todas as lojas

**Duplicação de Modelos**:
- Ao criar um novo modelo semelhante a um existente, duplique o modelo existente e modifique
- Evita começar do zero

**Exclusão de Modelos**:
- Não pode excluir o modelo padrão enquanto existirem terminais (deve haver um fallback)
- Pode excluir modelos de grupo/loja (terminais recorrem ao próximo nível na hierarquia)
- Confirme que nenhum terminal está usando ativamente o modelo antes de excluir

## Dicas

- **Comece com 80mm se tiver dúvidas** - A largura padrão de papel funciona para a maioria do varejo; 58mm é especializado
- **Teste o logotipo em uma impressora real** - O que parece bom na tela pode imprimir mal; teste cedo
- **Mantenha os campos de conformidade atualizados** - Registros fiscais expirados em recibos criam problemas legais
- **Códigos QR com proposta de valor escaneiam melhor** - "Escaneie para 10% de desconto" supera "Escaneie aqui" por 10x
- **Revise os limites de caracteres** - O texto que se quebra arruina a formatação; conte os caracteres por linha antes de implantar
- **Um modelo por largura de papel** - Não atribua um modelo de 80mm a um terminal com impressora de 58mm (o logotipo não caberá)
- **Imprima recibos de teste mensalmente** - Impressoras degradam com o tempo; verifique se a qualidade ainda é aceitável
- **Use variáveis com parcimônia** - Texto estático é mais confiável do que variáveis dinâmicas (menos pontos de falha)
- **Faça backup da configuração do modelo** - Faça screenshot ou exporte a configuração do modelo antes de alterações importantes (facilita o rollback)
- **A conformidade regional varia** - Pesquise os requisitos locais de recibos antes de implantar; multas por não conformidade podem ser severas

Lembre-se: Mantenha todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.