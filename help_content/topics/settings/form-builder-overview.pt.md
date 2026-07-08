---
title: Visão Geral do Construtor de Formulários
---

O Form Builder cria formulários personalizados para coleta de dados — formulários de contato, pesquisas, aplicações, inscrições e muito mais. Crie formulários visualmente com campos arrastáveis e soltáveis, configure regras de validação, habilite fluxos de trabalho em múltiplas etapas e colete respostas com análises detalhadas. Os formulários se integram perfeitamente com elementos do Page Builder, podendo ser embutidos em qualquer lugar do seu site. Todas as submissões são armazenadas no banco de dados com metadados completos (endereço IP, navegador, tempo para completar) para análise e exportação.

Use o Form Builder quando precisar coletar dados estruturados de clientes, seja informações de contato simples ou aplicações complexas em várias páginas.

## O que é o Form Builder?

O Form Builder é uma ferramenta visual de arrastar e soltar para criar formulários personalizados sem código:

**Tipos de Formulário Suportados**:
- Formulários de contato (nome, e-mail, mensagem)
- Pesquisas de clientes (avaliações, feedback, NPS)
- Registros de produtos (garantia, suporte)
- Candidaturas a empregos (carregar currículo, em várias etapas)
- Inscrições em eventos (informações do participante, preferências)
- Solicitações de serviço (requisitos detalhados)
- Inscrições em newsletters (com caixas de seleção para preferências)

**Recursos Principais**:
- **22 tipos de campos** - Texto, e-mail, telefone, upload de arquivo, avaliações, seletores de produto e mais
- **Formulários em múltiplas etapas** - Divida formulários longos em etapas lógicas com rastreamento de progresso
- **Lógica condicional** - Mostre/oculte campos com base nas respostas do usuário
- **Regras de validação** - Campos obrigatórios, comprimento mínimo/máximo, padrões personalizados de regex
- **Proteção contra spam** - Campos honeypot ou Google reCAPTCHA v3
- **Análise de respostas** - Rastreie tempo de conclusão, endereço IP, navegador, remetente
- **Exportação CSV** - Faça o download de todas as respostas para análise no Excel/Google Sheets
- **Multilíngue** - Traduza rótulos e mensagens do formulário para todos os idiomas ativos

## Criando Seu Primeiro Formulário

Navegue até **Configurações > Páginas > Formulários** para acessar o gerenciador de formulários:

**Etapa 1: Criar Novo Formulário**
- Clique em **+ Criar Novo Formulário**
- Insira o nome do formulário (identificador interno, não mostrado aos clientes)
- Insira o título do formulário (exibido como cabeçalho acima do formulário)
- Opcional: Adicione uma descrição (texto de ajuda exibido abaixo do título)

**Etapa 2: Adicionar Campos**
- Clique em **Editar Design do Formulário** para abrir o construtor visual
- Arraste os tipos de campos do painel lateral esquerdo para o canvas
- Clique no campo para configurá-lo no painel direito
- Defina rótulo, placeholder, texto de ajuda
- Ative o status obrigatório
- Adicione regras de validação

**Etapa 3: Configurar Configurações do Formulário**
- Defina o texto do botão de envio (padrão: "Enviar")
- Personalize a mensagem de sucesso (exibida após o envio)
- Escolha a proteção contra spam (recomendado honeypot)
- Ative "Requer Login" se necessário
- Ative "Formulário em Múltiplas Etapas" para formulários complexos

**Etapa 4: Ativar Formulário**
- Ative o status **Ativo**
- Apenas formulários ativos aceitam submissões
- Salve o formulário

**Etapa 5: Usar no Page Builder**
- Adicione o elemento **Formulário** a qualquer página
- Selecione seu formulário no menu suspenso
- O formulário herda o estilo da página
- Submissões são enviadas automaticamente para o backend

## Formulários de Página Única vs. Formulários em Múltiplas Etapas

**Formulários de Página Única** (padrão):
- Todos os campos exibidos de uma vez
- Role para ver todos os campos
- Botão de envio no final
- Melhor para: Formulários de contato, pesquisas curtas, coleta de dados simples

**Formulários em Múltiplas Etapas**:
- Campos organizados em etapas numeradas
- Barra de progresso mostra a etapa atual
- Botões de Navegação para Trás/Próximo
- Envio apenas na última etapa
- Opcional: Salvar respostas parciais (modo rascunho)
- Melhor para: Candidaturas a empregos, inscrições, pesquisas complexas, fluxos de checkout

**Ativar Formulário em Múltiplas Etapas**:
1. Ative "Formulário em Múltiplas Etapas" nas configurações do formulário
2. Clique na guia **Etapas** no painel direito
3. Adicione uma etapa (ex: "Informações Pessoais", "Detalhes de Contato", "Preferências")
4. Atribua campos a etapas usando o menu suspenso de etapas ao editar o campo
5. Reordene as etapas arrastando-as
6. Defina propriedades da etapa: título, descrição, passível de pular

**Benefícios de Formulários em Múltiplas Etapas**:
- Reduz a abandono de formulários (psicológico: "apenas 3 perguntas nesta página")
- Agrupamento lógico melhora a experiência do usuário
- Indicador de progresso motiva a conclusão
- Salvar rascunho opcional para formulários longos

## Explicação das Configurações do Formulário

**Configurações Básicas**:
- **Nome Interno** - Como você identifica o formulário no painel de administração (não visível aos clientes)
- **Slug** - Identificador amigável para URL (gerado automaticamente, usado em endpoints de API)
- **Título do Formulário** - Cabeçalho exibido acima do formulário
- **Descrição** - Texto de ajuda opcional exibido abaixo do título
- **Texto do Botão de Envio** - Personalize o rótulo do botão (ex: "Enviar Mensagem", "Candidate-se Agora")

**Mensagens**:
- **Mensagem de Sucesso** - Exibida após o envio bem-sucedido (padrão: "Obrigado por sua submissão!")
- **Mensagem de Erro** - Exibida se o envio falhar (padrão: "Ocorreu um erro. Por favor, tente novamente.")

**Segurança e Acesso**:
- **Ativo** - Apenas formulários ativos aceitam submissões (formulários inativos mostram "Formulário indisponível")
- **Requer Login** - Restringe apenas a usuários autenticados (usuários anônimos veem o prompt de login)

**Proteção Contra Spam**:
- **Nenhuma** - Nenhuma proteção (não recomendado, bots enviarão spam)
- **Campo Honeypot** - Campo invisível que captura bots (recomendado para a maioria dos varejistas)
- **Google reCAPTCHA v3** - Requer chaves de site e segredo do Google (proteção mais forte)

**Recursos Avançados**:
- **Formulário em Múltiplas Etapas** - Ative fluxo de trabalho passo a passo
- **Salvar Respostas Parciais** - Permita que usuários salvem o progresso e retomem depois (apenas formulários em múltiplas etapas)

## Opções de Proteção Contra Spam

**Campo Honeypot (Recomendado)**:
- Campo invisível adicionado ao formulário
- Bots preenchem (usuários não podem vê-lo)
- Submissões com campo honeypot preenchido são rejeitadas
- Nenhuma configuração necessária
- Nenhuma frustração com CAPTCHA para usuários
- Efetivo contra 95%+ dos bots de spam

**Google reCAPTCHA v3**:
- Pontuação de fundo invisível (0,0-1,0)
- Nenhuma "desafio clique nos semáforos"
- Requer configuração:
  1. Crie conta em google.com/recaptcha/admin
  2. Gere a chave de site e chave secreta
  3. Insira as chaves nas configurações do construtor de formulários
- Mais robusto que honeypot
- Use quando honeypot for insuficiente

**Nenhuma**:
- Nenhuma proteção contra spam
- Use apenas para formulários internos ou testes
- Formulários públicos serão spamados pesado

## Gerenciando Respostas de Formulário

Veja todas as submissões em **Configurações > Páginas > Formulários > [Nome do Formulário] > Respostas**:

**Visualização da Lista de Respostas**:
- Status: rascunho, submetido, concluído
- Submissor: e-mail (se logado) ou "Anônimo"
- Endereço IP e localização (se GeoIP estiver ativado)
- Data/hora de submissão
- Tempo para completar (segundos)

**Detalhes da Resposta**:
- Todos os valores dos campos com rótulos
- Metadados: navegador, remetente, idioma
- Rastreamento de progresso (formulário em múltiplas etapas): etapa atual, etapas concluídas
- Resultados de ações (se o formulário acionar ações)

**Filtragem de Respostas**:
- Filtrar por formulário, status, intervalo de data
- Pesquisar por e-mail do submissor ou endereço IP
- Ordenar por data de submissão, tempo de conclusão

**Exportação de Respostas**:
- Clique no botão **Exportar para CSV**
- Baixe `{form-slug}_responses_{date}.csv`
- Linha de cabeçalho: Submitted At, User, IP, Status, [Rótulos dos Campos]
- Uma resposta por linha
- Abra no Excel, Google Sheets ou ferramentas de análise de dados

## Usando Formulários em Páginas

**Inserindo Formulários**:
1. Abra a página no Page Builder
2. Adicione o elemento **Formulário** do painel de elementos
3. Selecione o formulário no menu suspenso
4. Personalize o estilo do contêiner do formulário (fundo, preenchimento, borda)
5. Salve e publique a página

**Formulário Renderiza Com**:
- Título e descrição do formulário (do formulário settings)
- Todos os campos em ordem (página única) ou etapa atual (múltiplas etapas)
- Botão de envio com texto personalizado
- Mensagens de sucesso/erro após o envio

**Herança de Estilo**:
- Formulários herdam o estilo do tema da página
- Botões usam estilos de botão do tema
- Campos de entrada usam estilos de entrada do tema
- Classe CSS personalizada pode ser adicionada aos campos para estilização específica

## Interface do Form Builder

**Barra Lateral Esquerda - Biblioteca de Campos**:
- Organizados por categoria (Texto, Seleção, Avaliação, Avançado)
- Arraste o campo para o canvas ou clique para adicionar
- Pesquisar para encontrar rapidamente tipos de campos

**Canvas Principal - Editor de Campos**:
- Handle de arrasto (≡) para reordenar campos
- Clique no campo para selecionar e editar
- Botão de exclusão (×) em cada campo
- Visualização prévia do campo conforme configurado
- Estado vazio com instruções de zona de arrasto

**Barra Lateral Direita - Painel de Propriedades**:
- **Guia Configurações do Formulário** - Informações básicas, mensagens, proteção contra spam
- **Guia Configurações do Campo** - Configure o campo selecionado (rótulo, validação, etc.)
- **Guia Etapas** - Gerenciar etapas (apenas formulários em múltiplas etapas)
- **Guia Regras Condicionais** - Adicione lógica de mostrar/ocultar com base nas respostas

**Funcionalidades da Barra de Ferramentas**:
- **Desfazer/Refazer** - Histórico completo de edição
- **Visualizar** - Teste a funcionalidade do formulário
- **Salvar** - Salva automaticamente a cada 3 segundos enquanto está editando
- **Traduções** - Traduza o texto do formulário para outros idiomas

## Exemplos Comuns de Formulários

**Formulário de Contato**:
- Campos: Nome Completo (obrigatório), E-mail (obrigatório), Telefone, Mensagem (obrigatório)
- Botão de envio: "Enviar Mensagem"
- Sucesso: "Obrigado por nos contatar! Nós responderemos dentro de 24 horas." 

**Pesquisa de Feedback de Produto**:
- Etapa 1: Avaliação com estrelas, escala de concordância de Likert
- Etapa 2: Ponto NPS, sugestões de melhorias
- Condicional: Se avaliação < 3, exija feedback de melhorias

**Candidatura a Emprego**:
- Etapa 1: Informações pessoais (nome, e-mail, telefone)
- Etapa 2: Experiência (carregar currículo, anos de experiência, referências)
- Etapa 3: Disponibilidade (data de início, expectativas salariais)
- Salvar parcial ativado (candidatos podem retomar depois)

**Inscrição em Newsletter com Preferências**:
- E-mail (obrigatório)
- Grupo de caixas de seleção: Interesses (Produtos, Vendas, Atualizações do Blog)
- reCAPTCHA ativado (impede inscrições falsas)

## Dicas

- **Comece com página única** - Adicione etapas múltiplas apenas se o formulário tiver mais de 10 campos
- **Use honeypot primeiro** - Apenas atualize para reCAPTCHA se o spam persistir
- **Teste antes de publicar** - Use o modo de visualização para verificar validação e fluxo
- **Exporte regularmente** - Faça o download do CSV de respostas semanalmente para backup
- **Monitore o tempo de conclusão** - Se a média for >5 minutos, o formulário pode estar muito longo
- **Use lógica condicional** - Oculte campos irrelevantes para reduzir a percepção de comprimento do formulário
- **Ative o salvamento parcial para formulários longos** - Reduz o abandono em candidaturas em múltiplas etapas
- **Traduza os rótulos do formulário** - Use o sistema de tradução integrado para sites multilíngues
- **Requer login para dados sensíveis** - Impede spam anônimo, vincula submissões a contas de usuários
- **Mantenha as mensagens de sucesso específicas** - "Nós responderemos dentro de 24 horas" é melhor que "Obrigado"