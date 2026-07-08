---
title: Campos do Construtor de Formulários e Validação
---

Campos de formulário são os blocos de construção dos seus formulários — cada campo coleta um pedaço de dados dos usuários. O Form Builder oferece 22 tipos de campos, variando de entradas de texto simples até escalas de avaliação avançadas e seletores de produtos. Configure cada campo com rótulos, regras de validação, texto de ajuda e lógica condicional para criar formulários dinâmicos que se adaptam com base nas respostas dos usuários. Os campos podem ser obrigatórios ou facultativos, validados com padrões regex e estilizados com classes CSS personalizadas.

Use este guia para entender todos os tipos de campos disponíveis, quando usar cada um e como configurar validação e lógica condicional.

## Configuração Básica de Campos

Cada campo compartilha estas configurações comuns:

**Identidade**:
- **Nome do Campo** - Nome de máquina para armazenamento de dados (sem espaços, use sublinhados: `email_address`)
- **Tipo de Campo** - Determina o comportamento de entrada e renderização
- **Atribuição de Etapa** - Qual etapa este campo pertence (apenas para formulários de múltiplas etapas)

**Exibição**:
- **Rótulo** - Pergunta ou prompt mostrado aos usuários (ex: "Qual é o seu endereço de e-mail?")
- **PlaceHolder** - Texto de dica dentro da entrada (ex: "você@exemplo.com")
- **Texto de Ajuda** - Orientação adicional abaixo do campo (ex: "Nunca compartilharemos seu e-mail")
- **Valor Padrão** - Valor preenchido (os usuários podem alterá-lo)

**Layout**:
- **Largura** - Total (100%), Meio (50%) ou Um-Terceiro (33%) da largura do formulário
- **Classe CSS** - Classes adicionais de estilo para design personalizado
- **Ordem** - Posição dentro da etapa (arraste para reordenar)

**Validação**:
- **Obrigatório** - Ative o status obrigatório (asterisco vermelho aparece no rótulo)
- **Min/Max de Caracteres** - Limites de caracteres (campos de texto)
- **Min/Max de Valor** - Limites numéricos (campos numéricos)
- **Padrão de Validação** - Padrão regex personalizado para validação complexa
- **Mensagem de Erro** - Texto personalizado mostrado quando a validação falhar

## Campos de Entrada de Texto

**Texto de Linha Única** (`text`):
- Entrada de texto básica para respostas curtas
- Validação: min/max de caracteres, padrão regex
- Caso de uso: Nomes, endereços, códigos de produto, respostas curtas
- Exemplo: "Nome Completo", "Endereço de Rua", "Nome da Empresa"

**Texto de Múltiplas Linhas** (`textarea`):
- Área de texto expansível para conteúdo mais longo (3-10 linhas)
- Validação: min/max de caracteres
- Caso de uso: Comentários, feedback, descrições detalhadas, mensagens
- Exemplo: "Conte-nos sobre sua experiência", "Notas adicionais"

**Endereço de E-mail** (`email`):
- Validação específica para e-mail (requer @ e domínio)
- Teclados móveis mostram o botão @ de forma proeminente
- Caso de uso: E-mail de contato, inscrições em newsletters, criação de conta
- Exemplo: "Endereço de E-mail", "E-mail de Trabalho"

**Número de Telefone** (`phone`):
- Formata números de telefone automaticamente
- Teclados móveis mostram layout numérico
- Validação: padrão configurável (formatos internacionais suportados)
- Caso de uso: Número de contato, contato de emergência, agendamento de consultas
- Exemplo: "Número de Telefone", "Celular", "Número de Contato"

**Número** (`number`):
- Entrada numérica com controles de incremento/diminuição
- Validação: min/max de valor, incremento de passo
- Retorna número (não string) nas respostas
- Caso de uso: Quantidades, idades, anos de experiência, montantes de orçamento
- Exemplo: "Quantos funcionários você tem?", "Sua idade", "Anos em negócios"

**URL** (`url`):
- Validação de URL (requer http:// ou https://)
- Teclados móveis mostram o botão .com
- Caso de uso: Site, perfil do LinkedIn, link do portfólio
- Exemplo: "Site da Empresa", "URL do Portfólio"

## Campos de Seleção

**Seletor de Dropdown** (`select`):
- Seleção única de opção de menu suspenso
- Configuração: array de {value, label} opções
- Suporta seleção padrão
- Caso de uso: Categorias, estados/países, seleção de status
- Exemplo: "Selecione seu país", "Departamento", "Como você soube de nós?"
- Melhor para: 5+ opções (menos opções usem botões de rádio)

**Botões de Rádio** (`radio`):
- Escolha única de opções visíveis (todas as opções exibidas)
- Configuração: array de {value, label} opções
- Melhor experiência do usuário do que select para 2-4 opções
- Caso de uso: Perguntas sim/não, gênero, preferências com poucas opções
- Exemplo: "Você recomendaria a nós?", "Método de contato preferido"

**Caixa de Seleção** (`checkbox`):
- Caixa de seleção única (ligado/desligado)
- Retorna verdadeiro/falso nas respostas
- Caso de uso: Aceitação de termos, acordos, preferência única
- Exemplo: "Concordo com os termos e condições", "Assinar newsletter"

**Grupo de Caixas de Seleção** (`checkbox_group`):
- Seleção múltipla de opções (usuários podem selecionar 0, 1 ou muitas)
- Configuração: array de {value, label} opções
- Retorna array de valores selecionados
- Caso de uso: Preferências de múltipla seleção, interesses, recursos necessários
- Exemplo: "Quais temas o interessam?", "Selecione todos que se aplicam"

## Campos de Avaliação

**Avaliação com Estrelas** (`rating_stars`):
- Escala visual de avaliação com estrelas (normalmente 1-5 estrelas)
- Configuração:
  - `max_stars`: 3-10 estrelas (padrão: 5)
  - `allow_half`: true/false para avaliações com meia-estrela
  - `icon`: fa-star (padrão) ou fa-heart
  - `color`: código de cor hex (padrão: #FFD700 dourado)
- Caso de uso: Avaliação de produtos, qualidade do serviço, pontuação de satisfação
- Exemplo: "Avalie sua experiência", "Como foi nosso serviço?"

**Escala Likert** (`rating_likert`):
- Escala de avaliação de afirmação: fortemente discordo → fortemente concordo
- Configuração:
  - `scale_type`: 5_point (1-5) ou 7_point (1-7)
  - `labels`: personalizar texto dos pontos finais (esquerda: "Fortemente Discordo", direita: "Fortemente Concordo")
- Retorna valor numérico (1-5 ou 1-7)
- Caso de uso: Afirmações de pesquisa, escalas de concordância, medição de sentimento
- Exemplo: "O produto atende às minhas necessidades", "O atendimento ao cliente foi útil"

**Pontuação de Promotor Neto (NPS)** (`rating_nps`):
- Escala de 0-10: "Nenhuma probabilidade" a "Extremamente provável"
- Configuração:
  - `low_label`: texto do ponto final esquerdo (padrão: "Nenhuma probabilidade")
  - `high_label`: texto do ponto final direito (padrão: "Extremamente provável")
- Retorna valor de 0-10 (0-6 = detratores, 7-8 = passivos, 9-10 = promotores)
- Caso de uso: Pesquisas NPS, probabilidade de recomendação, medição de fidelidade
- Exemplo: "Qual a probabilidade de você recomendar a nós a um amigo?"

## Campos Avançados

**Upload de Arquivo** (`file`):
- Upload de um ou mais arquivos
- Configuração:
  - `max_size_mb`: limite de tamanho do arquivo por arquivo (padrão: 5MB)
  - `allowed_types`: array de extensões (ex., ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: número máximo de arquivos (1 para único, 2+ para múltiplos)
- Retorna o(s) caminho(s) do(s) arquivo(s) nas respostas
- Arquivos armazenados em `/media/form_uploads/{form-slug}/`
- Caso de uso: uploads de currículos, submissão de documentos, anexos de fotos
- Exemplo: "Carregue seu currículo", "Anexe documentos de suporte"

**Seletor de Produto** (`product_select`):
- Seleção múltipla do seu catálogo de produtos
- Configuração:
  - `category_filters`: limite a categorias específicas (array de IDs de categoria)
  - `max_selections`: 1 para um único produto, 2+ para múltiplos
  - `display_mode`: "list" (padrão) ou "grid" (com miniaturas)
- Retorna IDs/SKUs dos produtos nas respostas
- Caso de uso: recomendações de produtos, listas de desejos, pesquisas de feedback, pacotes
- Exemplo: "Quais produtos você está interessado(a)?", "Selecione seus itens favoritos"

**Data** (`date`):
- Interface de seleção de data (popup de calendário)
- Retorna no formato ISO (YYYY-MM-DD)
- Validação: data mínima/máxima
- Caso de uso: datas de nascimento, datas de eventos, agendamento de consultas, prazos
- Exemplo: "Data de Nascimento", "Data de Agendamento Preferida"

**Hora** (`time`):
- Seletor de hora (horas e minutos)
- Retorna no formato de hora ISO (HH:MM)
- Caso de uso: horários de consultas, janelas de disponibilidade
- Exemplo: "Horário Preferido", "Disponível Após"

**Data e Hora** (`datetime`):
- Seletor combinado de data e hora
- Retorna data e hora ISO completas
- Caso de uso: agendamento de eventos, reservas de consultas
- Exemplo: "Data e Hora de Início do Evento", "Janela de Entrega"

## Campos de Layout (Não de Entrada)

**Cabeçalho de Seção** (`heading`):
- Texto de cabeçalho para organizar seções do formulário
- Configuração: nível do cabeçalho (h2, h3, h4)
- Nenhuma coleta de dados
- Caso de uso: quebrar formulários longos em seções lógicas
- Exemplo: "Informações Pessoais", "Detalhes de Contato", "Preferências"

**Parágrafo Descritivo** (`paragraph`):
- Bloco de texto rico para instruções ou informações
- Nenhuma coleta de dados
- Suporta formatação básica (negrito, itálico, links)
- Caso de uso: instruções de etapas, desclaimer legal, explicações
- Exemplo: aviso de política de privacidade, explicação de consentimento GDPR

**Linha de Divisor** (`divider`):
- Linha horizontal visual separadora
- Nenhuma coleta de dados
- Caso de uso: organização visual entre seções

**Campo Oculto** (`hidden`):
- Campo invisível com valor programático
- Configuração: `default_value` (obrigatório)
- Nenhuma etiqueta ou texto de ajuda mostrado aos usuários
- Caso de uso: parâmetros UTM, dados de rastreamento, IDs de sessão, códigos de indicação
- Exemplo: campo oculto com valor de parâmetro da URL

## Regras de Validação de Campo

**Campos Obrigatórios**:
- Ative a caixa de seleção "Obrigatório" nas configurações do campo
- Aparece um asterisco vermelho (*) ao lado da etiqueta
- O formulário não pode ser submetido se os campos obrigatórios estiverem vazios
- Erro personalizado: "Este campo é obrigatório" (ou mensagem personalizada)

**Comprimento Mínimo/Máximo** (campos de texto):
- Defina o número mínimo de caracteres: impede respostas muito curtas
- Defina o número máximo de caracteres: impede entrada excessiva
- Exemplo: campo de mensagem requer mínimo de 10 caracteres (impede respostas como "ok")

**Valor Mínimo/Máximo** (campos numéricos):
- Defina o valor numérico mínimo: impede idades negativas, quantidades
- Defina o valor numérico máximo: limita a entrada a uma faixa razoável
- Exemplo: campo de idade requer mínimo 18, máximo 120

**Padrão de Validação** (expressão regular):
- Expressão regular personalizada para validação complexa
- Padrões comuns:
  - CEP: `^\d{5}(-\d{4})?$` (formato dos EUA)
  - Telefone: `^\(\d{3}\) \d{3}-\d{4}$` (formato dos EUA)
  - Código de produto: `^[A-Z]{2}\d{4}$` (2 letras, 4 dígitos)
- Mensagem de erro personalizada necessária ao usar padrões

**Validação de Arquivo**:
- Tamanho máximo do arquivo: impede uploads grandes (padrão 5MB)
- Tipos permitidos: lista branca de extensões específicas (segurança)
- Exemplo: campo de currículo permite ["pdf", "doc", "docx"], máximo 2MB

## Lógica Condicional

Crie formulários dinâmicos onde os campos aparecem ou desaparecem com base nas respostas do usuário:

**Como as Regras Condicionais Funcionam**:
1. O usuário responde ao "campo fonte" (o gatilho)
2. O sistema avalia a regra: operador + valor de comparação
3. Se a condição for verdadeira, a ação é executada (mostrar/ocultar/requerir campo ou etapa)
4. Múltiplas regras podem encadear (regra A gera regra B)

**Operadores Disponíveis**:
- **Igual** (`equals`): correspondência exata (ex., país igual a "US")
- **Não Igual** (`not_equals`): qualquer coisa exceto o valor
- **Contém** (`contains`): texto inclui substring (case-insensitive)
- **Maior Que** (`greater_than`): comparação numérica (ex., idade > 18)
- **Menor Que** (`less_than`): comparação numérica (ex., avaliação < 3)
- **Vazio** (`is_empty`): campo não tem valor
- **Não Vazio** (`is_not_empty`): campo tem qualquer valor
- **Na Lista** (`in_list`): valor é um de ["Opção1", "Opção2"]

**Ações Disponíveis**:
- **Mostrar Campo** - Exibir campo oculto
- **Ocultar Campo** - Ocultar campo (valor limpo se ocultado)
- **Requerir Campo** - Tornar campo obrigatório
- **Não Requerir Campo** - Tornar campo opcional
- **Definir Valor** - Preencher campo com um valor
- **Mostrar Etapa** - Exibir etapa oculta (apenas em formulários de múltiplas etapas)
- **Ocultar Etapa** - Ocultar etapa (apenas em formulários de múltiplas etapas)
- **Pular para Etapa** - Pular para etapa específica (apenas em formulários de múltiplas etapas)

**Exemplos de Regras**:
- SE `contact_method` IGUAL A "phone" ENTÃO mostrar_campo `phone_number`
- SE `rating` MENOR QUE "3" ENTÃO requerir_campo `improvement_feedback`
- SE `country` NA_LISTA ["US", "CA"] ENTÃO mostrar_etapa `shipping_details`
- SE `budget` MAIOR QUE "10000" ENTÃO mostrar_campo `enterprise_features`

**Criando Regras Condicionais**:
1. Clique na aba "Regras Condicionais" no painel direito
2. Clique em "Adicionar Regra"
3. Selecione o campo fonte (gatilho)
4. Selecione o operador (como comparar)
5. Insira o valor de comparação (o que comparar)
6. Selecione a ação (o que fazer)
7. Selecione o alvo (campo ou etapa afetada)
8. Opcional: Defina a prioridade (regras com prioridade mais alta são avaliadas primeiro)
9. Salve a regra


**Prioridade de Regra**:
- Números mais altos são avaliados primeiro (prioridade 100 antes da prioridade 10)
- Use prioridade quando as regras conflitam ou se cascatarem
- Exemplo: Regra A (prioridade 100) mostra o campo, Regra B (prioridade 50) o exige (A é executada primeiro, depois B)

## Padrões Comuns de Campo

**Formulário de Contato**:
- Nome Completo (texto, obrigatório)
- Email (email, obrigatório)
- Telefone (telefone)
- Assunto (seleção com opções: "Vendas", "Suporte", "Parceria")
- Mensagem (textarea, obrigatório, mínimo 10 caracteres)

**Feedback de Produto**:
- Produto (product_select, seleção única)
- Avaliação Geral (rating_stars, 5 estrelas)
- Condicional: SE avaliação < 3 ENTÃO exija "O que podemos melhorar?" (textarea)
- Recomendação (rating_nps)

**Candidatura para Vaga**:
- Etapa 1: Pessoal (nome, email, telefone)
- Etapa 2: Currículo (upload de arquivo, permitido ["pdf", "doc"], máximo 2MB)
- Etapa 3: Disponibilidade (data para início, grupo de caixas de seleção para dias de trabalho)
- Condicional: SE "years_experience" > 5 ENTÃO mostre o campo "experiência de liderança"

## Dicas

- **Use os tipos de campo apropriados** - Campo de email para emails (não texto), fornece validação e teclados móveis melhores
- **Mantenha os rótulos curtos** - Use texto de ajuda para detalhes, não nos rótulos
- **Agrupe campos relacionados** - Use títulos e divisórias para organização visual
- **Teste a validação** - Visualize o formulário e tente enviar com dados inválidos
- **Limite o tamanho do upload de arquivos** - Máximo de 5MB evita sobrecarga do servidor com arquivos grandes
- **Use lógica condicional com moderação** - Muitas regras confundem os usuários; mantenha os formulários simples
- **Defina valores máximos realistas** - Máximo de idade de 120, máximo de quantidade de 100 (evita erros de digitação como 1000)
- **Forneça exemplos de padrão** - Se usar validação com regex, mostre um exemplo no texto de ajuda
- **Torne óbvios os campos obrigatórios** - Nome e email em formulários de contato, sempre obrigatórios
- **Use opções de rádio para 2-4 opções** - Dropdown para 5+ opções (melhora a UX)
- **Campos de metade da largura para entradas curtas** - Telefone e CEP podem ser de metade da largura, economiza espaço vertical
- **Seletor de produtos para listas de desejos** - Permita que os clientes selecionem múltiplos produtos para recomendações