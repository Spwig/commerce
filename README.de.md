<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <strong>Deutsch</strong> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
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
  <strong>Selbst gehostetes E-Commerce für Händler, die ihren Shop besitzen möchten.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Website</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Dokumentation</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Community</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/de/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/de/demos">Live-Demos</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Was ist Spwig?

Spwig ist eine vollwertige E-Commerce-Plattform: Katalog, Warenkorb, Kasse,
Bestellungen, Kunden, Zahlungen, Versand, Themes, Page Builder, Admin-API,
POS, Abonnements, Treueprogramme, Blog, SEO – der gesamte Stack. Entwickelt
mit **Django 5**, **PostgreSQL** und **Redis**, ausgeliefert als eine
Sammlung von Docker-Containern, läuft auf einem 5-Dollar-VPS oder auf
Ihrer eigenen Hardware.

Im Gegensatz zu gehosteten Plattformen **gehören Ihnen der Code, die
Datenbank und die Kundendaten.** Keine Transaktionsgebühren. Keine
Herstellerbindung. Wenn Sie das Projekt forken und Ihren eigenen Weg
gehen möchten, erlaubt die Lizenz das ausdrücklich.

<br />

## Editionen

Dieselbe Binärdatei. Eine signierte Lizenzdatei aktiviert Feature-Flags
zur Laufzeit. Included in every edition — no upgrade required.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| Vollständiges E-Commerce, Themes, Page Builder, POS-Oberfläche | ✓ | ✓ | ✓ |
| Eigene Zahlungsanbieter einbinden | ✓ | ✓ | ✓ |
| Eigene Versanddienstleister einbinden | ✓ | ✓ | ✓ |
| Marketplace-Zugang (Premium-Themes + Integrationen) | ✓ | ✓ | ✓ |
| Von Spwig gehostete Adress-Autovervollständigung | Kostenlos · limitiert | Höheres Limit | Höchstes Limit |
| Von Spwig gehostetes GeoIP (Besucherstandort) | Kostenlos · limitiert | Höheres Limit | Höchstes Limit |
| Push-Benachrichtigungen (iOS-Admin-App) | Kostenlos · limitiert | Höheres Limit | Höchstes Limit |
| Point-of-Sale (POS-Terminal-Unterstützung) | ✓ | ✓ | ✓ |
| Gehostetes E-Mail-Gateway mit aufgewärmten IPs + DKIM | – | ✓ | ✓ |
| Priorisierter Support | – | ✓ | ✓ |
| Enterprise SSO (Azure AD, Okta) | – | – | ✓ |

<br />

## Schnellstart

### Option 1 – Ein-Zeilen-Installation (empfohlen)

Der [Spwig-Installer](https://github.com/Spwig/spwig) richtet alles mit
einem einzigen Befehl ein: Docker, PostgreSQL, Redis, MinIO, TLS über
Cloudflare oder selbstsigniert, Ersteinrichtungsassistent, Admin-Benutzer.
Signierte Images werden von `registry.spwig.com` bezogen.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Upgrades erfolgen über den Admin-Bereich – siehe [UPGRADING.md](UPGRADING.md).

### Option 2 – Aus dem Quellcode

Sie möchten aus diesem Repository bauen, daran arbeiten oder einen Fork
ausliefern:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Storefront unter `http://localhost`, Admin unter `http://localhost/de/admin/`.
Die Community-Edition aktiviert sich beim ersten Start automatisch – kein
Abgleich mit einem Lizenzserver, kein Schlüssel erforderlich. Später
aktualisieren mit `git pull` und `docker compose build`.

<br />

## Funktionen

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Storefront & Kasse</h3>
      <p>Standardmäßig serverseitig gerendert – schnelle Time-to-First-Byte,
      funktioniert ohne JavaScript, Mobile-First (80 % des Traffics kommt
      von kleinen Bildschirmen). Optionaler Headless-Modus über das
      <a href="https://github.com/Spwig/headless-sdk">Spwig Headless
      SDK</a> und die <a href="https://github.com/Spwig/react">React-
      Komponenten</a>.</p>
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
      <h3>Page Builder</h3>
      <p>Händler erstellen Storefront-Seiten aus wiederverwendbaren Widgets
      – Hero-Bereiche, Produktraster, Testimonials, Embeds – und sehen die
      Vorschau live im Admin-Bereich. Widgets werden aus dem Marketplace
      oder aus dem eigenen Komponenten-Repository installiert.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Bestell- und Kundenverwaltung</h3>
      <p>Jede Bestellung, Rückerstattung, Abo-Verlängerung, digitaler
      Download und jeder Kundenkontakt an einem Ort. Massenoperationen,
      berechtigungsbasierte Mitarbeiterrollen, Export nach CSV/XLSX,
      mobile Admin-App (iOS) mit Push-Benachrichtigungen.</p>
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
      <h3>Themes & Branding</h3>
      <p>Design-Tokens (Farben, Typografie, Abstände) steuern jede
      Oberfläche – Storefront und Admin. Ein Token ändern, alles wird
      aktualisiert. Themes liegen in
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      und werden über den Marketplace installiert; eigene lassen sich mit
      dem <a href="https://github.com/Spwig/theme-sdk">Theme SDK</a>
      schreiben.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Point of Sale</h3>
      <p>Vollwertiges POS-Terminal für stationäre Händler:
      Barcode-Scannen, geteilte Zahlungen, Belegdruck, Kassenschubladen-
      Integration, Kundenanzeige, Offline-Modus. Die Community-Edition
      enthält den Code, im Admin-Bereich erscheint jedoch ein Upgrade-CTA
      – bei einem Fork lässt sich das entfernen, das ist in Ordnung.</p>
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
      <h3>Provider-Ökosystem</h3>
      <p>Alles, was mit einem externen System kommuniziert – Zahlungen,
      Versand, Wechselkurse, Übersetzung, GeoIP, SMS, E-Mail – ist ein
      steckbarer Provider. Bauen Sie mit den
      <a href="https://github.com/Spwig/provider-sdks">Provider SDKs</a>
      Ihre eigenen, veröffentlichen Sie im Marketplace oder betreiben
      Sie eine private Registry selbst.</p>
    </td>
  </tr>
</table>

<br />

## Architektur

- **Single-Tenant.** Jede Installation ist ein Shop, ein Händler, eine
  Django-Site. Händler mit mehreren Shops betreiben je Shop eine eigene
  Spwig-Installation.
- **Modularer Monolith.** Kein Microservice-Geflecht. Ein einziger
  Django-Prozess bedient Storefront + Admin + REST-API + Celery-Worker.
  Einfach zu deployen, zu verstehen und zu forken.
- **Feature-Gates zur Laufzeit.** Community/Pro/Enterprise laufen alle
  auf derselben Binärdatei. Eine signierte Lizenz schaltet Flags um –
  kein Entfernen von Code.

Vollständige Übersicht: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Community & Support

- **Discussions.** Offene Fragen, Ideen, Show-and-Tell:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Community-Forum.** [community.spwig.com](https://community.spwig.com)
  – ausführliche Threads, Best-Practice-Rezepte, Erweiterungs-Showcases.
- **Bug-Reports.** [Issues](https://github.com/Spwig/commerce/issues)
  mit Reproduktionsschritten. Siehe [SECURITY.md](SECURITY.md) für die
  Offenlegung von Sicherheitslücken.
- **Kommerzieller Support.** Verfügbar für Pro- und Enterprise-Lizenzen.

<br />

## Mitwirken

Wir nutzen **DCO** (Developer Certificate of Origin) – jeder Commit wird
mit `git commit -s` signiert. Keine Formalitäten, kein CLA. Vollständige
Anleitung in [CONTRIBUTING.md](CONTRIBUTING.md).

Hinweise für KI-Coding-Assistenten, die am Repository arbeiten, finden
sich in [CLAUDE.md](CLAUDE.md).

<br />

## Ökosystem

Verwandte Open-Source-Projekte unter der [Spwig-Organisation](https://github.com/Spwig):

| Repo | Was es ist |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Dieses Repo – die Kernplattform (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Ein-Zeilen-Installer |
| [Spwig/components](https://github.com/Spwig/components) | Themes, Integrationen und Dienstprogramme (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK zum Erstellen von Themes (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDKs zum Erstellen von Zahlungs-/Versand-/etc.-Providern (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | Headless-/API-Client-SDK (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | React-Komponentenbibliothek (Apache-2.0) |

<br />

## Lizenz

Spwig steht unter [AGPL-3.0-or-later](LICENSE). Sie dürfen es
ausführen, verändern, verteilen und als gehosteten Dienst anbieten –
all das ist erlaubt. Veränderte Versionen, die über ein Netzwerk
angeboten werden, müssen ihren Nutzern den Quellcode zur Verfügung
stellen. Genau darin liegt der Sinn der AGPL gegenüber der GPL.

Provider-Integrationen, die mit den SDKs erstellt werden, stehen unter
Apache-2.0. Der Aufbau einer proprietären Zahlungs-/Versand-/SMS-
Integration auf Basis der SDKs löst daher keine AGPL-Verpflichtung aus.
Das ist beabsichtigt – wir wünschen uns ein florierendes Provider-
Ökosystem.

<br />

## Datenschutz & Telemetrie

Spwig sendet einmal täglich einen anonymen Ping an `updates.spwig.com/api/v1/telemetry/`:

- Installations-UUID (wird beim ersten Start erzeugt und lokal gespeichert)
- Spwig-Version
- Edition (community / pro / enterprise / trial / dev)
- Land (aus der IP beim Eingang aufgelöst; die IP selbst wird nicht gespeichert)
- Bucket-Zähler für Feature-Flags (konfigurierte Zahlungsanbieter,
  installierte Themes) – niemals rohe Kunden- oder Bestelldaten

**Deaktivieren** lässt sich das mit `SPWIG_TELEMETRY=0` in Ihrer
Umgebung. Dadurch wird `settings.SPWIG_TELEMETRY_ENABLED` umgeschaltet
und der tägliche Beat-Task führt keine Aktion mehr aus.

<br />

<p align="center">
  <sub>
    Mit Sorgfalt in Singapur gebaut.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
