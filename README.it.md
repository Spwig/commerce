<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <strong>Italiano</strong> |
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
  <strong>E-commerce self-hosted per i commercianti che vogliono possedere il proprio negozio.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Sito web</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Documentazione</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Comunità</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/it/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/it/demos">Demo dal vivo</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Cos'è Spwig?

Spwig è una piattaforma e-commerce completa: catalogo, carrello, checkout,
ordini, clienti, pagamenti, spedizioni, temi, page builder, API di
amministrazione, POS, abbonamenti, fidelizzazione, blog, SEO — l'intero
stack. Costruita con **Django 5**, **PostgreSQL** e **Redis**, viene
distribuita come un insieme di container Docker, funziona su un VPS da 5
dollari o sul tuo hardware.

A differenza delle piattaforme ospitate, **possiedi il codice, il database
e i dati dei clienti.** Nessuna commissione per transazione. Nessun
lock-in. Se vuoi farne un fork e seguire la tua strada, la licenza lo
permette esplicitamente.

<br />

## Edizioni

Stesso binario. Un file di licenza firmato attiva i feature flag a runtime.
Community è ciò che ottieni per impostazione predefinita quando esegui
`docker compose up`; per aggiornare basta incollare una chiave nel pannello
di amministrazione.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| E-commerce completo, temi, page builder, interfaccia POS | ✓ | ✓ | ✓ |
| Provider di pagamento a scelta | ✓ | ✓ | ✓ |
| Provider di spedizione a scelta | ✓ | ✓ | ✓ |
| Accesso al marketplace (temi premium + integrazioni) | ✓ | ✓ | ✓ |
| Autocompletamento indirizzi ospitato da Spwig | Gratuito · con limite di frequenza | Limite più alto | Limite massimo |
| GeoIP ospitato da Spwig (posizione del visitatore) | Gratuito · con limite di frequenza | Limite più alto | Limite massimo |
| Notifiche push (app admin iOS) | Gratuito · con limite di frequenza | Limite più alto | Limite massimo |
| Punto vendita (supporto terminale POS) | – | ✓ | ✓ |
| Gateway email ospitato con IP caldi + DKIM | – | ✓ | ✓ |
| Supporto prioritario | – | ✓ | ✓ |
| SSO aziendale (Azure AD, Okta) | – | – | ✓ |

<br />

## Avvio rapido

### Opzione 1 — Installazione in un comando (consigliata)

L'[installer Spwig](https://github.com/Spwig/spwig) configura tutto con un
solo comando: Docker, PostgreSQL, Redis, MinIO, TLS tramite Cloudflare o
auto-firmato, procedura guidata al primo avvio, utente amministratore.
Immagini firmate scaricate da `registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Gli aggiornamenti avvengono tramite il pannello di amministrazione — vedi
[UPGRADING.md](UPGRADING.md).

### Opzione 2 — Dal codice sorgente

Vuoi compilare da questo repository, modificarlo o distribuire un fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Vetrina su `http://localhost`, amministrazione su `http://localhost/it/admin/`.
L'edizione Community si attiva automaticamente al primo avvio — nessun
round-trip verso un server di licenze, nessuna chiave richiesta. Aggiorna in
seguito con `git pull` e `docker compose build`.

<br />

## Funzionalità

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Vetrina e checkout</h3>
      <p>Renderizzato lato server per impostazione predefinita — tempo al
      primo byte rapido, funziona senza JavaScript, mobile-first (l'80%
      del traffico proviene da schermi piccoli). Modalità headless
      opzionale tramite l'<a href="https://github.com/Spwig/headless-sdk">SDK
      headless Spwig</a> e i <a href="https://github.com/Spwig/react">componenti
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
      <h3>Page builder</h3>
      <p>I commercianti costruiscono le pagine della vetrina con widget
      riutilizzabili — sezioni hero, griglie di prodotti, testimonianze,
      contenuti embed — e visualizzano l'anteprima dal vivo nel pannello
      di amministrazione. I widget si installano dal marketplace o dal
      tuo repository personale di componenti.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Gestione ordini e clienti</h3>
      <p>Ogni ordine, rimborso, rinnovo di abbonamento, download digitale
      e punto di contatto con il cliente in un unico posto. Operazioni in
      blocco, ruoli dello staff con permessi granulari, esportazione in
      CSV/XLSX, app admin mobile (iOS) con notifiche push.</p>
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
      <h3>Temi e branding</h3>
      <p>I design token (colori, tipografia, spaziatura) governano ogni
      superficie — vetrina e amministrazione. Cambia un token e tutto si
      aggiorna. I temi risiedono in
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      e si installano tramite il marketplace; scrivi il tuo con il
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Punto vendita (Pro+)</h3>
      <p>Terminale POS completo per i commercianti fisici: scansione di
      codici a barre, pagamenti divisi, stampa di ricevute, integrazione
      con cassetto contanti, display rivolto al cliente, modalità
      offline. L'edizione Community include il codice ma l'interfaccia
      admin mostra una CTA di upgrade — se fai un fork puoi rimuoverla,
      va bene.</p>
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
      <h3>Ecosistema di provider</h3>
      <p>Tutto ciò che comunica con un sistema esterno — pagamenti,
      spedizioni, tassi di cambio, traduzione, GeoIP, SMS, email — è un
      provider collegabile. Costruisci il tuo con i
      <a href="https://github.com/Spwig/provider-sdks">provider SDK</a>,
      pubblica sul marketplace o auto-ospita un registro privato.</p>
    </td>
  </tr>
</table>

<br />

## Architettura

- **Single-tenant.** Ogni installazione è un negozio, un commerciante, un
  Django Site. I commercianti con più negozi eseguono un'installazione
  Spwig per ciascun negozio.
- **Monolite modulare.** Non una rete di microservizi. Un singolo
  processo Django gestisce vetrina + amministrazione + API REST + worker
  Celery. Semplice da distribuire, comprendere e forkare.
- **Feature gate a runtime.** Community/Pro/Enterprise eseguono tutti lo
  stesso binario. Una licenza firmata attiva i flag — nessuna rimozione
  di codice.

Panoramica completa: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Comunità e supporto

- **Discussioni.** Domande aperte, idee, show-and-tell:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Forum della comunità.** [community.spwig.com](https://community.spwig.com)
  — thread approfonditi, ricette di best practice, vetrine di estensioni.
- **Segnalazioni di bug.** [Issues](https://github.com/Spwig/commerce/issues)
  con passaggi per la riproduzione. Vedi [SECURITY.md](SECURITY.md) per
  la divulgazione delle vulnerabilità.
- **Supporto commerciale.** Disponibile per le licenze Pro ed Enterprise.

<br />

## Contribuire

Utilizziamo il **DCO** (Developer Certificate of Origin) — ogni commit
viene firmato con `git commit -s`. Nessuna burocrazia, nessun CLA. Guida
completa in [CONTRIBUTING.md](CONTRIBUTING.md).

Le note per gli assistenti di codifica AI che lavorano sul repository
sono in [CLAUDE.md](CLAUDE.md).

<br />

## Ecosistema

Progetti open-source correlati sotto l'[organizzazione Spwig](https://github.com/Spwig):

| Repo | Cos'è |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Questo repository — la piattaforma principale (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Installer in un solo comando |
| [Spwig/components](https://github.com/Spwig/components) | Temi, integrazioni e utilità (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK per costruire temi (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDK per costruire provider di pagamento / spedizione / ecc. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK client headless / API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Libreria di componenti React (Apache-2.0) |

<br />

## Licenza

Spwig è [AGPL-3.0-or-later](LICENSE). Puoi eseguirlo, modificarlo,
distribuirlo, offrirlo come servizio ospitato — tutto è permesso. Le
versioni modificate offerte tramite una rete devono rendere disponibile
il proprio codice sorgente ai propri utenti. È esattamente questo il
punto di AGPL rispetto a GPL.

Le integrazioni di provider costruite con gli SDK sono Apache-2.0, quindi
costruire un'integrazione proprietaria di pagamento / spedizione / SMS
sopra gli SDK non attiva AGPL. È intenzionale — vogliamo un ecosistema di
provider fiorente.

<br />

## Privacy e telemetria

Spwig invia un ping anonimo al giorno a `updates.spwig.com/api/v1/telemetry/`:

- UUID di installazione (generato al primo avvio, memorizzato localmente)
- Versione di Spwig
- Edizione (community / pro / enterprise / trial / dev)
- Paese (risolto dall'IP in ingresso; l'IP stesso non viene memorizzato)
- Conteggi aggregati dei feature flag (provider di pagamento configurati,
  temi installati) — mai dati grezzi di clienti o ordini

**Disattiva** con `SPWIG_TELEMETRY=0` nel tuo ambiente. Questo commuta
`settings.SPWIG_TELEMETRY_ENABLED` e il task periodico giornaliero non fa
nulla.

<br />

<p align="center">
  <sub>
    Realizzato con cura a Singapore.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">documentazione</a> — <a href="https://community.spwig.com">comunità</a>
  </sub>
</p>
