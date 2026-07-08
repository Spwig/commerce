---
title: Backups do Banco de Dados
---

Backups regulares protegem os dados do seu loja — pedidos, clientes, produtos e configurações — contra falhas de hardware, exclusões acidentais e outros eventos inesperados. O sistema de backup do Spwig permite que você crie backups sob demanda, defina agendamentos automáticos, faça o download de backups localmente, restaure a partir de qualquer backup salvo e copie backups para destinos de armazenamento remoto, como Amazon S3 ou Google Drive.

Navegue até **Gerenciamento > Métricas do Sistema** e use os links da barra de ferramentas para acessar as ferramentas de backup.

![Painel do Sistema com ferramentas de backup](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Criando um backup manual

Execute um backup a qualquer momento antes de fazer alterações significativas — como uma importação de produtos, uma atualização de tema ou uma atualização da plataforma.

1. Navegue até **Gerenciamento > Métricas do Sistema**
2. Clique em **Criar Backup Completo** na barra de ferramentas
3. Insira um **Nome** descritivo para o backup (ex.: `before-july-import`)
4. Adicione opcionalmente uma **Descrição** para lembrar por que esse backup foi feito
5. Escolha um **Tipo de Backup**:
   - **Sistema Completo** — faz backup do banco de dados e de todos os arquivos de mídia (recomendado)
   - **Apenas Banco de Dados** — faz backup apenas dos dados da loja, excluindo imagens e arquivos carregados
6. Escolha a **Compactação** (`gzip` é o padrão e funciona bem para a maioria das lojas)
7. Clique em **Criar Backup**

O Spwig cria o backup em segundo plano. Um indicador de progresso mostra a etapa atual. Quando concluído, o backup aparece na lista **Backups do Banco de Dados** com o status **Concluído** e seu tamanho de arquivo.

## Fazer o download de um backup

Você pode baixar qualquer backup concluído para manter uma cópia local no seu computador.

1. Navegue até **Gerenciamento > Backups do Banco de Dados**
2. Localize o backup que deseja baixar
3. Clique no botão **Download** ao lado dele

O arquivo de backup é baixado como um arquivo compactado. Armazene-o em um local seguro — em um dispositivo separado ou em armazenamento em nuvem — para que você tenha uma cópia independente do seu servidor.

## Agendar backups automáticos

Backups automáticos são executados em segundo plano, sem nenhuma ação sua, então seus dados são protegidos mesmo que você esqueça de criar backups manuais.

1. Navegue até **Gerenciamento > Métricas do Sistema**
2. Clique em **Agendamento de Backup**
3. Marque **Habilitar Backups Automáticos**
4. Defina a **Frequência**:
   - **Diária** — executa uma vez por dia no horário que você especificar
   - **Semanal** — executa uma vez por semana no dia que você escolher
   - **Mensal** — executa em um dia específico do mês
5. Defina o **Horário** em que o backup deve ser executado (hora do servidor, normalmente UTC — 03:00 AM é um bom horário de baixa demanda)
6. Escolha o **Tipo de Backup** (Sistema Completo ou Apenas Banco de Dados)
7. Defina **Dias de Retenção** — backups mais antigos do que esse número de dias são excluídos automaticamente (padrão: 30 dias)
8. Marque opcionalmente **Criptografar Backup** para criptografar o arquivo de backup em repouso
9. Se você tiver destinos de armazenamento remoto configurados, selecione-os em **Destinos Remotos** para carregar automaticamente os backups agendados
10. Clique em **Salvar Agendamento**

O carimbo de tempo **Próxima Execução** é atualizado imediatamente e mostra quando a próxima cópia de segurança automática ocorrerá.

## Restaurando a partir de um backup

A restauração substitui os dados atuais da sua loja pelos conteúdos de um backup. Use isso para recuperar-se de perda de dados ou para desfazer alterações indesejadas.

> **Importante:** A restauração substituirá todos os dados atuais pelos dados do backup. Sua loja será colocada em modo de manutenção durante a restauração. Informe sua equipe antes de executar uma restauração.

1. Navegue até **Gerenciamento > Métricas do Sistema**
2. Clique em **Restaurar** na barra de ferramentas
3. A lista de restauração mostra todos os backups disponíveis com suas datas e tamanhos
4. Clique em **Restaurar** ao lado do backup que deseja usar
5. Revise a tela de confirmação — ela lista exatamente o que será substituído
6. Digite a frase de confirmação, se solicitado, e clique em **Executar Restauração**

O Spwig mostra uma barra de progresso enquanto a restauração passa por suas etapas (fazendo backup do estado atual, baixando o backup se remoto, restaurando o banco de dados, restaurando arquivos de mídia). Quando concluída, a loja sai automaticamente do modo de manutenção.

## Configurando armazenamento remoto

O armazenamento remoto copia automaticamente seus backups para um destino externo — Amazon S3, Google Drive, Dropbox ou um servidor SFTP. Isso protege você contra falhas no nível do servidor.

1. Navegue até **Gerenciamento > Métricas do Sistema**
2. Clique em **Armazenamento Remoto**
3. Clique em **Adicionar Destino**
4. O assistente de configuração o guia por três etapas:
   - **Etapa 1**: Escolha o tipo de armazenamento (S3, Google Drive, Dropbox ou SFTP)
   - **Etapa 2**: Insira as credenciais para o provedor escolhido (veja os detalhes abaixo)
   - **Etapa 3**: Nomeie o destino e teste a conexão
5. Após o teste de conexão ser bem-sucedido, clique em **Salvar**

### Amazon S3 (e serviços compatíveis com S3)

Você precisará de:
- **Access Key ID** e **Secret Access Key** do seu usuário IAM da AWS
- **Bucket Name** — o bucket S3 para fazer upload dos backups
- **Region** — a região AWS onde o bucket está localizado (ex.: `us-east-1`)
- Opcionalmente um **Prefix** (caminho da pasta dentro do bucket, ex.: `spwig-backups/`)

Serviços compatíveis com S3 (Backblaze B2, Wasabi, MinIO, etc.) funcionam da mesma forma — insira a URL do endpoint personalizado quando solicitado.

### Google Drive

Clique em **Conectar com o Google** na etapa de credenciais. O Spwig abre uma janela de autenticação do Google OAuth — faça login e conceda permissão para fazer upload de arquivos. Não há credenciais para copiar manualmente.

### Dropbox

Clique em **Conectar com o Dropbox** na etapa de credenciais. Faça login no Dropbox e aprovê a permissão. Os backups são carregados para uma pasta `Apps/Spwig` no seu Dropbox.

### SFTP

Você precisará de:
- **Hostname** do seu servidor SFTP
- **Port** (padrão: 22)
- **Username** e **Password** (ou chave privada SSH)
- **Remote Path** — o diretório no servidor para fazer upload dos backups

### Definindo um destino como padrão

Na página **Armazenamento Remoto**, clique no botão de alternância ao lado de qualquer destino para torná-lo o **padrão**. O destino padrão recebe automaticamente todos os backups — manuais e agendados — sem a necessidade de selecioná-lo a cada vez.

## Dicas

- Execute um backup manual antes de cada mudança significativa: importação de produtos, edições de tema, atualizações da plataforma ou campanhas de desconto
- Agende backups diários em um horário de baixa demanda (ex.: 03:00 AM) para minimizar qualquer impacto no desempenho
- Configure pelo menos um destino de armazenamento remoto para que os backups sobrevivam mesmo se o próprio servidor tiver um problema
- A configuração **Retention Days** controla por quanto tempo os backups locais são mantidos — 30 dias é um valor padrão razoável para a maioria das lojas, mas aumente-o se o espaço de armazenamento permitir
- Após uma restauração, verifique algumas ordens e produtos para confirmar que os dados parecem corretos antes de sair do modo de manutenção manualmente
- Backups criptografados adicionam uma camada de segurança, mas exigem a chave de descriptografia para restaurar — não perca-a