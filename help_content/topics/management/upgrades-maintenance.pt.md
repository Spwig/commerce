---
title: Atualizações & Manutenção
---

Spwig recebe atualizações regulares com novas funcionalidades, melhorias de desempenho e correções de segurança. Este guia aborda como atualizar sua instalação, usar a ferramenta de diagnóstico e lidar com tarefas de manutenção.

## Atualizando o Spwig

### Antes de atualizar

1. **Crie um backup** — vá para **Gerenciamento > Métricas do Sistema > Criar Backup Completo** ou execute o script de backup a partir da linha de comando. Este é seu rede de segurança caso algo dê errado.
2. **Verifique a versão atual** — visível em **Gerenciamento > Métricas do Sistema** ou no rodapé do painel de administração.
3. **Revise o que mudou** — abra a página **Atualização do Sistema** para ler as notas completas de lançamento da nova versão antes de instalá-la, incluindo quaisquer etapas adicionais que o lançamento mencione (veja abaixo).

### Revisando o que é novo na página de Atualização do Sistema

Quando o Spwig detecta uma versão mais recente, **Painel do Sistema** mostra uma ação rápida **Atualização Disponível**. Clique nela — ou navegue até **Painel do Sistema > Atualizações do Plataforma** primeiro para visualizar o log de alterações, depois continue — para abrir a página **Atualização do Sistema**.

A página mostra:

- **Versão Atual** e **Versão Disponível** cards, para que você possa confirmar exatamente quais versões você está se movendo entre
- Uma seção **O que é novo em {versão}** — um resumo breve do lançamento, seguido pelas notas completas de lançamento formatadas com títulos e listas de itens, exatamente como os mantenedores as escreveram
- **Verificações Pré-Atualização** — espaço em disco, conexão com o banco de dados, um backup recente, permissões de escrita e conectividade com o servidor de atualização do Spwig. Clique em **Executar Verificações Pré-Voo**; o botão **Iniciar Atualização** permanece desativado até que todas as verificações passem
- Um banner **Antes de Atualizar** que lembra que um backup é criado automaticamente, sua loja entra em modo de manutenção brevemente durante a atualização, e você não deve fechar a página ou navegar para outro lugar enquanto ela estiver em execução

Leia cuidadosamente as **Notas de Atualização** na seção O que é novo — algumas liberações mencionam etapas que você precisa executar pessoalmente após a atualização. Por exemplo, uma liberação que adiciona um novo formato de imagem pode pedir que você regenere suas miniaturas de produto a partir de **Biblioteca de Mídia > Processamento de Imagem** para que as imagens já na sua biblioteca aproveitem a melhoria; novas uploads obtêm isso automaticamente, mas seu catálogo existente precisa de uma atualização manual.

Depois que as verificações pré-voo passarem, clique em **Iniciar Atualização** para começar pelo navegador. Uma barra de progresso acompanha cada etapa, e a página se recarrega automaticamente uma vez que a atualização for concluída. Este é o caminho recomendado para a maioria dos comerciantes — use o script baseado em SSH abaixo se você precisar de mais controle direto sobre o processo.

### Executando uma atualização

SSH em seu servidor e navegue até o diretório de instalação do Spwig (normalmente `/opt/spwig`):

```bash
./upgrade.sh
```

O script de atualização:

1. **Verificações pré-voo** — verifica o espaço em disco, saúde do Docker e status do serviço
2. **Migrações de banco de dados em modo seco** — testa se as alterações no banco de dados serão aplicadas limparmente sem realmente alterar nada
3. **Entrar em modo de manutenção** — sua loja mostra uma página de manutenção para visitantes durante a atualização
4. **Criar um backup** — backup de segurança automático antes de fazer alterações
5. **Drenar trabalhadores de fundo** — aguarda que tarefas em andamento (envios de e-mail, traduções) terminem de forma adequada
6. **Puxar novas imagens** — baixa a aplicação atualizada do registro do Spwig
7. **Aplicar migrações de banco de dados** — atualiza o esquema do banco de dados para a nova versão
8. **Reiniciar serviços** — inicia a aplicação com a nova versão
9. **Verificação de saúde** — verifica se todos os serviços estão funcionando corretamente
10. **Sair do modo de manutenção** — sua loja está de volta online

Se a verificação de saúde falhar após a atualização, o script **reverte automaticamente** para a versão anterior e restaura o backup.

### Opções de atualização

```bash
./upgrade.sh              # Atualização padrão com modo de manutenção
./upgrade.sh --dry-run    # Verifique o que mudaria sem aplicar
```

## A ferramenta de diagnóstico

O Spwig inclui uma ferramenta de diagnóstico integrada que verifica sua instalação completa para problemas:

```bash
./doctor.sh
```

O doctor verifica:

| Categoria | O que ele verifica |
|----------|---------------|
| **Sistema** | Espaço em disco, uso de RAM, carga da CPU |
| **Docker** | Saúde do motor Docker, estados dos contêineres, versões das imagens |
| **Banco de dados** | Conectividade com PostgreSQL, status de migração, saúde do pool de conexões |
| **Cache** | Conectividade com Redis, uso de memória |
| **Armazenamento de objetos** | Conectividade com MinIO, acessibilidade do bucket |
| **Rede** | Resolução de DNS, acessibilidade de portas, validade do certificado SSL |
| **Aplicativo** | Pontos de verificação de saúde dos serviços, status dos trabalhadores de fundo |

Cada verificação mostra um resultado de pass/fail com detalhes se algo estiver errado.

### Modo de correção automática

Para problemas comuns, o doctor pode tentar reparos automáticos:

```bash
./doctor.sh --fix
```

A correção automática pode resolver:

- Contêineres parados (reinicia-os)
- Conexões de banco de dados antigas (recicla o pool de conexões)
- Certificados SSL expirados (dispara renovação)
- Disco cheio de imagens Docker antigas (limpa imagens não usadas)

O doctor sempre explica o que vai corrigir antes de tomar uma ação.

## Modo de manutenção

O modo de manutenção mostra aos visitantes uma página "loja temporariamente indisponível" enquanto você faz alterações. Seu painel de administração permanece acessível.

### Habilitando o modo de manutenção

Do painel de administração: **Configurações da loja > Manutenção > Habilitar modo de manutenção**

Ou do terminal de comando:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Desabilitando o modo de manutenção

Do painel de administração: ative o interruptor de modo de manutenção para desativá-lo.

Ou do terminal de comando:

```bash
./go-live.sh
```

### Bypass de acesso durante manutenção

Enquanto o modo de manutenção está ativo, você pode acessar a loja normalmente adicionando um parâmetro secreto à URL. O segredo de bypass é mostrado no seu arquivo de configuração `.env` sob `MAINTENANCE_SECRET`.

## Gerenciamento de serviços

### Verificando o status dos serviços

Verifique o status de todos os serviços do Spwig:

```bash
docker compose ps
```

Isso mostra cada serviço, seu estado (em execução, parado, reiniciando) e seu status de saúde.

### Verificando logs

Verifique os logs de um serviço específico:

```bash
docker logs spwig_shop          # Logs do aplicativo
docker logs spwig_celery         # Logs dos trabalhadores de fundo
docker logs spwig_nginx          # Logs de acesso do servidor web
docker logs spwig_db             # Logs do banco de dados
```

Adicione `--tail 100` para ver as últimas 100 linhas, ou `--follow` para assistir aos logs em tempo real.

### Reiniciando um serviço

Se um serviço específico precisar ser reiniciado:

```bash
docker compose restart shop      # Reiniciar o aplicativo
docker compose restart celery    # Reiniciar os trabalhadores de fundo
docker compose restart nginx     # Reiniciar o servidor web
```

Para reiniciar todos os serviços:

```bash
docker compose restart
```

## Atualizações de componentes

O Spwig tem um mercado de componentes onde você pode instalar temas, provedores de pagamento, integrações de envio e outras extensões. Os componentes são atualizados independentemente da plataforma principal.

Navegue até **Gerenciamento > Atualizações de Componentes** para verificar atualizações de componentes disponíveis. As atualizações são baixadas e aplicadas automaticamente quando você as aprovar.

## Dicas

- **Atualize regularmente** — manter-se na versão mais recente garante que você tenha correções de segurança e acesso a novas funcionalidades
- **Leia a seção What's New antes de clicar em Start Upgrade** — é a forma mais rápida de identificar uma migração de banco de dados necessária, uma correção de segurança ou uma **Nota de atualização** que você precisa agir após
- **Sempre faça um backup primeiro** — mesmo que o script de atualização crie um backup automático, ter o seu próprio fornece segurança extra
- **Execute o doctor após problemas** — se sua loja comportar-se de forma inesperada, `./doctor.sh` é a forma mais rápida de identificar problemas
- **Agende atualizações para horários de baixa demanda** — o modo de manutenção interrompe temporariamente o acesso dos clientes, então atualize durante horários de baixa atividade
- **Mantenha espaço em disco disponível** — as atualizações precisam de espaço temporário para novas imagens e backups. Mantenha pelo menos 5 GB livres.