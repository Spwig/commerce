<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <strong>Português</strong> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>Comércio eletrônico auto-hospedado para lojistas que querem ser donos da própria loja.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Site</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Documentação</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Comunidade</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/pt/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/pt/demos">Demonstrações ao vivo</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## O que é o Spwig?

O Spwig é uma plataforma completa de comércio eletrônico: catálogo, carrinho,
checkout, pedidos, clientes, pagamentos, entregas, temas, construtor de páginas,
API de administração, POS, assinaturas, fidelidade, blog, SEO — a pilha inteira.
Construído com **Django 5**, **PostgreSQL** e **Redis**, distribuído como um
conjunto de contêineres Docker, roda em um VPS de US$ 5 ou no seu próprio
hardware.

Diferente das plataformas hospedadas, **você é dono do código, do banco de
dados e dos dados dos clientes.** Sem taxas por transação. Sem aprisionamento.
Se quiser dar um fork e seguir seu próprio caminho, a licença permite isso
explicitamente.

<br />

## Edições

Mesmo binário. Um arquivo de licença assinado alterna os feature flags em tempo
de execução. A edição Community é o que você obtém por padrão ao rodar
`docker compose up`; fazer upgrade é apenas colar uma chave no admin.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| Comércio eletrônico completo, temas, construtor de páginas, interface POS | ✓ | ✓ | ✓ |
| Traga seus próprios provedores de pagamento | ✓ | ✓ | ✓ |
| Traga seus próprios provedores de entrega | ✓ | ✓ | ✓ |
| Acesso ao marketplace (temas premium + integrações) | ✓ | ✓ | ✓ |
| Autocompletar de endereço hospedado pelo Spwig | Grátis · limitado por taxa | Limite maior | Limite máximo |
| GeoIP hospedado pelo Spwig (localização do visitante) | Grátis · limitado por taxa | Limite maior | Limite máximo |
| Notificações push (app admin iOS) | Grátis · limitado por taxa | Limite maior | Limite máximo |
| Ponto de venda (suporte a terminal POS) | – | ✓ | ✓ |
| Gateway de e-mail hospedado com IPs aquecidos + DKIM | – | ✓ | ✓ |
| Suporte prioritário | – | ✓ | ✓ |
| SSO corporativo (Azure AD, Okta) | – | – | ✓ |

<br />

## Início rápido

### Opção 1 — Instalação em uma linha (recomendado)

O [instalador do Spwig](https://github.com/Spwig/spwig) configura tudo com um
único comando: Docker, PostgreSQL, Redis, MinIO, TLS via Cloudflare ou
autoassinado, assistente de primeira inicialização e usuário administrador.
Imagens assinadas puxadas de `registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Os upgrades acontecem pelo admin — veja [UPGRADING.md](UPGRADING.md).

### Opção 2 — A partir do código-fonte

Você quer compilar a partir deste repositório, mexer nele ou lançar um fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Loja em `http://localhost`, admin em `http://localhost/pt/admin/`.
A edição Community é ativada automaticamente na primeira inicialização — sem
ida e volta ao servidor de licenças, sem chave necessária. Faça upgrade depois
com `git pull` e `docker compose build`.

<br />

## Recursos

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Loja e checkout</h3>
      <p>Renderizado no servidor por padrão — tempo até o primeiro byte
      rápido, funciona sem JavaScript, mobile-first (80% do tráfego vem de
      telas pequenas). Modo headless opcional via
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> e <a href="https://github.com/Spwig/react">componentes
      React</a>.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>Construtor de páginas</h3>
      <p>Os lojistas montam páginas da loja a partir de widgets reutilizáveis
      — seções hero, grades de produtos, depoimentos, embeds — e visualizam ao
      vivo no admin. Widgets são instalados a partir do marketplace ou do seu
      próprio repositório de componentes.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Gestão de pedidos e clientes</h3>
      <p>Todo pedido, reembolso, renovação de assinatura, download digital e
      ponto de contato com o cliente em um só lugar. Operações em lote,
      papéis de equipe com permissões limitadas, exportação para CSV/XLSX,
      app admin móvel (iOS) com notificações push.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>Temas e identidade visual</h3>
      <p>Design tokens (cores, tipografia, espaçamento) governam cada
      superfície — loja e admin. Altere um token e tudo se atualiza. Os
      temas ficam em
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      e são instalados pelo marketplace; crie o seu com o
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Ponto de venda (Pro+)</h3>
      <p>Terminal POS completo para lojistas com loja física:
      leitura de código de barras, pagamentos divididos, impressão de
      cupom, integração com gaveta de dinheiro, display voltado para o
      cliente, modo offline. A edição Community traz o código, mas a
      superfície admin exibe um CTA de upgrade — sinta-se à vontade
      para removê-lo se der um fork.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>Ecossistema de provedores</h3>
      <p>Tudo que conversa com um sistema externo — pagamentos,
      entregas, taxas de câmbio, tradução, GeoIP, SMS, e-mail — é um
      provedor plugável. Construa o seu com os
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>,
      publique no marketplace ou hospede um registry privado.</p>
    </td>
  </tr>
</table>

<br />

## Arquitetura

- **Single-tenant.** Cada instalação é uma loja, um lojista, um
  Django Site. Lojistas com múltiplas lojas rodam uma instalação do Spwig
  por loja.
- **Monólito modular.** Não é uma malha de microsserviços. Um único processo
  Django cuida da loja + admin + REST API + workers Celery.
  Simples de implantar, de raciocinar sobre e de dar fork.
- **Gates de recurso em tempo de execução.** Community/Pro/Enterprise rodam o
  mesmo binário. Uma licença assinada alterna as flags — sem remoção de código.

Passeio completo: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Comunidade e suporte

- **Discussões.** Perguntas abertas, ideias, mostrar-e-contar:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Fórum da comunidade.** [community.spwig.com](https://community.spwig.com)
  — threads longas, receitas de boas práticas, vitrines de extensões.
- **Relatórios de bugs.** [Issues](https://github.com/Spwig/commerce/issues)
  com passos de reprodução. Veja [SECURITY.md](SECURITY.md) para
  divulgação de vulnerabilidades.
- **Suporte comercial.** Disponível para licenças Pro e Enterprise.

<br />

## Contribuindo

Usamos **DCO** (Developer Certificate of Origin) — todo commit é
assinado com `git commit -s`. Sem burocracia, sem CLA. Guia completo em
[CONTRIBUTING.md](CONTRIBUTING.md).

As notas para assistentes de codificação com IA que trabalham no repositório
estão em [CLAUDE.md](CLAUDE.md).

<br />

## Ecossistema

Projetos de código aberto relacionados na [organização Spwig](https://github.com/Spwig):

| Repositório | O que é |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Este repositório — a plataforma principal (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Instalador em uma linha |
| [Spwig/components](https://github.com/Spwig/components) | Temas, integrações e utilitários (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK para criação de temas (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDKs para criar provedores de pagamento / entrega / etc. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK cliente headless / de API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Biblioteca de componentes React (Apache-2.0) |

<br />

## Licença

O Spwig é [AGPL-3.0-or-later](LICENSE). Você pode executá-lo, modificá-lo,
distribuí-lo, oferecê-lo como serviço hospedado — tudo permitido. Versões
modificadas oferecidas por uma rede devem disponibilizar o código-fonte aos
seus usuários. Esse é justamente o ponto da AGPL em relação à GPL.

Integrações de provedores criadas com os SDKs são Apache-2.0, então construir
uma integração proprietária de pagamento / entrega / SMS em cima dos SDKs
não aciona a AGPL. Isso é intencional — queremos um ecossistema de provedores
próspero.

<br />

## Privacidade e telemetria

O Spwig envia um ping anônimo por dia para `updates.spwig.com/api/v1/telemetry/`:

- UUID de instalação (gerado na primeira inicialização, armazenado localmente)
- Versão do Spwig
- Edição (community / pro / enterprise / trial / dev)
- País (resolvido a partir do IP na entrada; o IP em si não é armazenado)
- Contagens agrupadas de feature flags (provedores de pagamento configurados,
  temas instalados) — nunca dados brutos de clientes ou pedidos

**Opte por não participar** com `SPWIG_TELEMETRY=0` no seu ambiente. Isso
inverte `settings.SPWIG_TELEMETRY_ENABLED` e a tarefa diária vira um no-op.

<br />

<p align="center">
  <sub>
    Feito com carinho em Singapura.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">comunidade</a>
  </sub>
</p>
