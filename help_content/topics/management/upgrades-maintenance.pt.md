---
title: Atualizações & Manutenção
---

Spwig recebe atualizações regulares com novas funcionalidades, melhorias de desempenho e correções de segurança. Este guia aborda como atualizar sua instalação, usar a ferramenta de diagnóstico e lidar com tarefas de manutenção.

## Atualizando o Spwig

### Antes de atualizar

1. **Crie um backup** — vá para **Gerenciamento > Métricas do Sistema > Criar Backup Completo** ou execute o script de backup a partir da linha de comando. Este é seu rede de segurança caso algo dê errado.
2. **Verifique a versão atual** — visível em **Gerenciamento > Métricas do Sistema** ou no rodapé do painel de administração.
3. **Leia as notas de lançamento** — disponíveis no painel de administração sob **Gerenciamento > Atualizações de Componentes** quando uma nova versão for detectada.

### Executando uma atualização

SSH no seu servidor e navegue até o diretório de instalação do Spwig (normalmente `/opt/spwig`):

```bash
./upgrade.sh
```

O script de atualização:

1. **Verificações pré-voo** — verifica o espaço em disco, saúde do Docker e status dos serviços
2. **Migrações de banco de dados em modo seco** — testa se as alterações no banco de dados serão aplicadas limparmente sem realmente alterar nada
3. **Entrar no modo de manutenção** — seu loja mostra uma página de manutenção para visitantes durante a atualização
4. **Criar um backup** — backup de segurança automático antes de fazer alterações
5. **Drenar trabalhadores de fundo** — aguarda que tarefas em andamento (envios de e-mail, traduções) terminem de forma adequada
6. **Puxar novas imagens** — baixa a versão atualizada do aplicativo do registro do Spwig
7. **Aplicar migrações de banco de dados** — atualiza o esquema do banco de dados para a nova versão
8. **Reiniciar serviços** — inicia o aplicativo com a nova versão
9. **Verificação de saúde** — verifica se todos os serviços estão funcionando corretamente
10. **Sair do modo de manutenção** — sua loja está de volta online

Se a verificação de saúde falhar após a atualização, o script **reverte automaticamente** para a versão anterior e restaura o backup.

### Opções de atualização

```bash
./upgrade.sh              # Atualização padrão com modo de manutenção
./upgrade.sh --dry-run    # Verificar o que mudaria sem aplicar
```

## A ferramenta de diagnóstico

O Spwig inclui uma ferramenta de diagnóstico embutida que verifica sua instalação inteira para problemas:

```bash
./doctor.sh
```

O médico verifica:

| Categoria | O que ele verifica |
|----------|---------------|
| **Sistema** | Espaço em disco, uso de RAM, carga da CPU |
| **Docker** | Saúde do motor Docker, estados do contêiner, versões da imagem |
| **Banco de dados** | Conectividade com PostgreSQL, status de migração, saúde do pool de conexões |
| **Cache** | Conectividade com Redis, uso de memória |
| **Armazenamento de objetos** | Conectividade com MinIO, acessibilidade do bucket |
| **Rede** | Resolução de DNS, acessibilidade de porta, validade do certificado SSL |
| **Aplicativo** | Pontos de verificação de saúde do serviço, status do trabalhador de fundo |

Cada verificação mostra um resultado de pass/fail com detalhes se algo estiver errado.

### Modo de auto-reparação

Para problemas comuns, o médico pode tentar reparos automáticos:

```bash
./doctor.sh --fix
```

Auto-reparação pode resolver:

- Contêineres parados (reinicia-os)
- Conexões de banco de dados antigas (recicla o pool de conexões)
- Certificados SSL expirados (dispara renovação)
- Disco cheio de imagens antigas do Docker (limpa imagens não usadas)

O médico sempre explica o que ele vai consertar antes de tomar ação.

## Modo de manutenção

O modo de manutenção mostra aos visitantes uma página "loja temporariamente indisponível" enquanto você faz alterações. Seu painel de administração permanece acessível.

### Ativar o modo de manutenção

Do painel de administração: **Configurações da Loja > Manutenção > Ativar Modo de Manutenção**

Ou a partir da linha de comando:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Desativar o modo de manutenção

Do painel de administração: ative o interruptor de modo de manutenção para desligar.

Ou a partir da linha de comando:

```bash
./go-live.sh
```

### Bypass de acesso durante manutenção

Enquanto o modo de manutenção estiver ativo, você pode acessar a loja normalmente adicionando um parâmetro secreto à URL. O segredo de bypass é mostrado em seu arquivo de configuração `.env` sob `MAINTENANCE_SECRET`.

## Gerenciando serviços

### Visualizando o status dos serviços

# Verificando o status dos serviços Spwig:

```bash
docker compose ps
```

Isso mostra cada serviço, seu estado (em execução, parado, reiniciando) e seu status de saúde.

### Visualizando logs

Verifique os logs de um serviço específico:

```bash
docker logs spwig_shop          # Logs da aplicação
docker logs spwig_celery         # Logs do worker de fundo
docker logs spwig_nginx          # Logs de acesso do servidor web
docker logs spwig_db             # Logs do banco de dados
```

Adicione `--tail 100` para ver as últimas 100 linhas, ou `--follow` para assistir aos logs em tempo real.

### Reiniciando um serviço

Se um serviço específico precisar ser reiniciado:

```bash
docker compose restart shop      # Reiniciar a aplicação
docker compose restart celery    # Reiniciar os workers de fundo
docker compose restart nginx     # Reiniciar o servidor web
```

Para reiniciar todos os serviços:

```bash
docker compose restart
```

## Atualizações de componentes

O Spwig possui um mercado de componentes onde você pode instalar temas, provedores de pagamento, integrações de envio e outras extensões. Os componentes são atualizados independentemente da plataforma principal.

Navegue até **Management > Component Updates** para verificar atualizações de componentes disponíveis. As atualizações são baixadas e aplicadas automaticamente quando você as aprovar.

## Dicas

- **Atualize regularmente** — manter-se na versão mais recente garante que você tenha correções de segurança e acesso a novas funcionalidades
- **Sempre faça um backup primeiro** — embora o script de atualização crie um backup automático, ter o seu próprio oferece segurança extra
- **Execute o doctor após problemas** — se seu loja comportar-se de forma inesperada, `./doctor.sh` é a maneira mais rápida de identificar problemas
- **Agende atualizações para períodos de baixo tráfego** — o modo de manutenção interrompe temporariamente o acesso dos clientes, então atualize durante horários de baixa atividade
- **Mantenha espaço em disco disponível** — as atualizações precisam de espaço temporário para novas imagens e backups. Mantenha pelo menos 5 GB livres.