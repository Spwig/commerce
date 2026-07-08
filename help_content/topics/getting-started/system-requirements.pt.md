---
title: Requisitos do Sistema
---

O Spwig funciona em mostas servidores Linux modernos. Esta págna cobre as especificações mínimas e recomendadas, o que acontece em servidores menores e quais provedores de nuvem funcionam bem.

## Requisitos mínimos

| Recurso | Mínimo | Recomendado |
|----------|---------|-------------|
| **Sistema operacional** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS ou Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB ou mais |
| **Espaço em disco** | 20 GB | 40 GB ou mais |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Arquitetura** | x86_64 (AMD64) | x86_64 |
| **Rede** | Endereço IP público (para modo standalone) | Endereço IP público estático |
| **Portas** | 80 e 443 (standalone) ou qualquer porta alternativa (sidecar) | 80 e 443 |

> **Nota:** Servidores baseados em ARM (por exemplo, AWS Graviton, Oracle Ampere) não são atualmente suportados.

## Níveis de recursos

O instalador detecta automaticamente a RAM disponível no seu servidor e seleciona o nível de recurso apropriado.

### Nível padrão (6 GB+ de RAM)

Todos os serviços funcionam com todas as capacidades:

- Serviço de **tradução com IA** ativado — traduza descrições de produtos, conteúdo de páginas e texto de SEO para múltiplos idiomas diretamente a partir do seu painel de administração
- Alocação completa de memória para a aplicação, banco de dados e trabalhadores de fundo
- Concorrência de trabalhadores de fundo otimizada para a contagem de CPU

### Nível pequeno (4–6 GB de RAM)

O instalador se adapta para economizar memória:

- O serviço de tradução com IA está **desativado** para economizar aproximadamente 2 GB de RAM. Você ainda pode gerenciar traduções manualmente ou usar ferramentas de tradução externas — apenas o tradutor com IA embutido é afetado.
- Limites de memória para aplicação e trabalhadores são reduzidos
- Todas as outras funcionalidades funcionam exatamente como no nível padrão

> **Dica:** Se você iniciar em um servidor pequeno e depois atualizar para 6 GB+ de RAM, execute novamente o instalador para ativar o serviço de tradução.

## Provedores de nuvem recomendados

O Spwig funciona em qualquer servidor Linux que atenda aos requisitos. Esses provedores foram testados e oferecem bom valor:

| Provedor | Plano recomendado | RAM | Disco | Custo aproximado |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Droplet Básico | 4 GB | 80 GB | $24/mês |
| **Linode (Akamai)** | Compartilhado 4 GB | 4 GB | 80 GB | $24/mês |
| **Vultr** | Computação em nuvem | 4 GB | 100 GB | $24/mês |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8/mês |
| **OVH** | VPS Inicial | 4 GB | 80 GB | €7/mês |

Para lojas que esperam tráfego significativo ou catálogos de produtos grandes (10.000+ produtos), comece com 8 GB de RAM e 2+ vCPUs.

## Uso do espaço em disco

Uma instalação nova do Spwig usa aproximadamente 8 GB de espaço em disco:

| Componente | Tamanho |
|-----------|------|
| Imagens do Docker | ~4 GB |
| Banco de dados (loja vazia) | ~200 MB |
| Modelos de tradução com IA (se ativado) | ~2 GB |
| Arquivos da aplicação e configuração | ~500 MB |
| Sistema operacional e motor do Docker | ~3 GB |

Planeje espaço adicional para:

- **Imagens de produtos e mídia** — depende do tamanho do seu catálogo. Orçamento de 1–5 GB para uma loja típica com centenas de produtos.
- **Crescimento do banco de dados** — cresce com pedidos, clientes e dados de análise. Uma loja processando 100 pedidos por dia normalmente cresce por ~1 GB por ano.
- **Backups** — se armazenar backups localmente, cada backup completo é aproximadamente o tamanho do seu banco de dados mais mídia. Com uma política de retenção de 30 dias, orçamento de 2–3× o tamanho dos seus dados atuais.

## Domínio e DNS

Um nome de domínio é opcional durante a instalação, mas necessário para uso em produção. Você precisa de:

- Um domínio ou subdomínio (por exemplo, `shop.example.com`)
- Um **registro A** apontando para o endereço IP público do seu servidor
- Propagação do DNS concluída (normalmente 5–60 minutos após adicionar o registro)

O instalador obtém automaticamente um certificado SSL gratuito do Let's Encrypt quando um domínio válido é detectado. Você também pode adicionar um domínio após a instalação usando o script `./configure-domain.sh`.

## Firewall

Se seu servidor tiver um firewall (a maioria dos provedores de nuvem ativa um por padrão), certifique-se de que essas portas estejam abertas:

| Porta | Protocolo | Propósito |
|------|----------|---------|
| **22** | TCP | Acesso SSH (para você gerenciar o servidor) |
| **80** | TCP | HTTP (necessário para a validação do certificado Let's Encrypt) |
| **443** | TCP | HTTPS (tráfego seguro da sua loja) |

Em modo sidecar, abra a porta alternativa atribuída pelo instalador em vez de 80/443.

## Requisitos de software

O instalador lida com a instalação de todos os softwares automaticamente. Para referência, esses são os componentes que ele instala ou verifica:

- **Docker Engine** — tempo de execução de contêiner (instalado automaticamente se estiver faltando)
- **Docker Compose** — orquestração de serviços (incluído com o Docker Engine)
- **curl** — usado pelo próprio instalador (presente na maioria dos sistemas Linux)

Nenhum outro software precisa ser instalado previamente. O Spwig não exige que você instale Python, Node.js, PostgreSQL, Redis ou Nginx manualmente — tudo executa dentro de contêineres Docker.