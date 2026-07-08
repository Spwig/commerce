---
title: Anpassung des Affiliate-Portals
---

Das Spwig Affiliate-Portal ist die öffentlich zugängliche Startseite, an der potenzielle Partner über Ihr Programm erfahren und sich anmelden. Die Anpassung dieses Portals ermöglicht es Ihnen, die Botschaft, das Branding und die Aufforderung zur Aktion mit der einzigartigen Positionierung Ihres Geschäfts abzugleichen. Ein gut gestaltetes Portal zieht hochwertige Partner an und verwandelt Besucher in aktive Partner.

## Was ist das Affiliate-Portal?

Das Affiliate-Portal ist unter `/affiliate/` auf Ihrem Geschäfts-Domain zugänglich. Es dient als:

- **Entdeckungsseite** — An der potenzielle Partner über Ihre Kommissionsstruktur, Vorteile und Anforderungen erfahren
- **Registrierungsstartpunkt** — Registrierungsformular für neue Partner (als Gast oder basierend auf einem Konto)
- **Anmeldeportal** — Bestehende Partner können sich anmelden, um auf ihr Dashboard zuzugreifen
- **Markenpräsentation** — Spiegelt die Identität Ihres Geschäfts und den Wert Ihres Affiliate-Programms wider

Das Portal ist vollständig anpassbar über die Affiliate-Einstellungen im Admin-Bereich, einschließlich Hero-Botschaften, Feature-Highlights, Schritt-für-Schritt-Flüsse und Registrierungsoptionen.

![Affiliate-Portal-Startseite](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Zugriff auf Einstellungen

Navigieren Sie zu **Marketing > Affiliate-Programm > Portal-Einstellungen**, um das Portal anzupassen.

Das Affiliate-Einstellungen-Modell ist ein **Singleton** — Sie haben genau ein Einstellungsprotokoll für Ihr gesamtes Geschäft. Alle Felder sind **übersetzbar** mithilfe des Spwig-Übersetzungssystems, sodass Sie die Botschaften für jede Sprache, die Ihr Geschäft unterstützt, anpassen können.

## Hero-Bereich

Der Hero-Bereich ist das erste, was potenzielle Partner sehen. Er enthält:

- **Titel** — Hauptüberschrift (z. B. "Join Our Affiliate Program")
- **Untertitel** — Unterstützender Text, der den Programmwert erklärt (z. B. "Earn commissions by promoting premium products to your audience")
- **Statistiken** — Automatisch angezeigte Metriken:
  - Gesamt aktive Programme
  - Gesamt aktive Partner
  - Durchschnittliche Kommissionsrate (berechnet über alle aktiven Programme)
- **CTA-Schaltflächen** — Automatisch generiert:
  - **Anmelden** — Für bestehende Partner
  - **Partner werden** — Lässt die Registrierung starten

### Anpassen der Hero-Botschaft

| Feld | Beispielwert | Zweck |
|------|--------------|-------|
| **Hero-Titel** | "Partner mit uns und verdienen" | Aufmerksamkeit erregen mit einer fokusierten Nutzenüberschrift |
| **Hero-Untertitel** | "Treten Sie 500+ Partnern bei, die bei jedem von Ihnen vermittelten Verkauf wettbewerbsfähige Kommissionen verdienen" | Sozialen Beweis liefern und das Angebot klären |

Die Statistiken werden **automatisch berechnet** und in Echtzeit basierend auf Ihren aktiven Programmen und Partnern aktualisiert. Sie können diese Werte nicht manuell bearbeiten.

## Features-Bereich

Der Features-Bereich hebt **6 anpassbare Vorteilskarten** hervor, die erklären, warum Partner Ihr Programm beitreten sollten. Jede Vorteilskarte enthält:

- **Icon** — FontAwesome-Icon-Klasse (z. B. `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Titel** — Vorteilsüberschrift (z. B. "Wettbewerbsfähige Kommissionen")
- **Beschreibung** — 1-2 Satz Erklärung (z. B. "Erwirken Sie bis zu 15 % auf jeden von Ihnen vermittelten Verkauf")

### Standard-Features

Spwig bietet Standard-Features an, wenn Sie das Affiliate-App zum ersten Mal installieren:

| Icon | Titel | Beschreibung |
|------|-------|-------------|
| `fa-dollar-sign` | Wettbewerbsfähige Kommissionen | Erwirken Sie großzügige Kommissionen auf jeden von Ihnen vermittelten Verkauf |
| `fa-link` | Einfache Tracking-Links | Erhalten Sie eindeutige Tracking-Links, die überall funktionieren |
| `fa-chart-line` | Echtzeit-Analytik | Verfolgen Sie Klicks, Konversionen und Einnahmen in Ihrem Dashboard |
| `fa-calendar-check` | Zuverlässige Auszahlungen | Erhalten Sie pünktlich Auszahlungen über PayPal oder Banküberweisung |
| `fa-headset` | Dedierte Unterstützung | Unser Team ist hier, um Ihnen zu helfen, Erfolg zu haben |
| `fa-gift` | Marketing-Materialien | Zugang zu Bannern, Bildern und Werbematerialien |

### Anpassen der Features

Features werden als **JSON-Array** in der Datenbank gespeichert. Bearbeiten Sie sie direkt im Admin-Formular:

```json
[
  {
    "icon": "fa-percent",
    "title": "Up to 20% Commission",
    "description": "Earn industry-leading commissions on premium product sales"
  },
  {
    "icon": "fa-rocket",
    "title": "Fast Approval",
    "description": "Get approved in 24 hours and start promoting immediately"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Mobile Dashboard",
    "description": "Manage your links and track earnings from any device"
  }
]
```

**Icon-Referenz:** Verwenden Sie jede FontAwesome 5 Free Icon-Klasse. Durchsuchen Sie Icons auf [fontawesome.com/icons](https://fontawesome.com/icons) und verwenden Sie die Klassenname (z. B. `fa-trophy`, `fa-users`, `fa-star`).

## Abschnitt "Wie es funktioniert"

Der Abschnitt "Wie es funktioniert" zeigt eine **4-Schritt-Visuelle Fluss** an, die den Partner-Journey erklärt. Jeder Schritt enthält:

- **Titel** — Schrittname (z. B. "Anmelden")
- **Beschreibung** — 1-2 Satz Erklärung, was passiert

### Standard-Schritte

| Schritt | Titel | Beschreibung |
|--------|-------|-------------|
| 1 | Anmelden | Erstellen Sie Ihr kostenloses Affiliate-Konto in Minuten |
| 2 | Links erhalten | Generieren Sie eindeutige Tracking-Links für jedes Produkt oder jede Seite |
| 3 | Werben | Teilen Sie Ihre Links mit Ihrem Publikum über Inhalt, soziale Medien oder E-Mail |
| 4 | Kommissionen verdienen | Erhalten Sie Zahlungen, wenn Kunden mit Ihren Verweis-Links einkaufen |

### Anpassen der Schritte

Schritte werden als **JSON-Array** gespeichert. Sie können sie im Admin bearbeiten:

```json
[
  {
    "title": "Aufnahme beantragen",
    "description": "Reichen Sie Ihre Bewerbung ein und erzählen Sie uns über Ihre Plattform"
  },
  {
    "title": "Genehmigung erhalten",
    "description": "Unser Team prüft Ihre Bewerbung innerhalb von 24 Stunden"
  },
  {
    "title": "Links erstellen",
    "description": "Greifen Sie auf Ihr Dashboard zu und generieren Sie Tracking-Links sofort"
  },
  {
    "title": "Loslegen und verdienen",
    "description": "Erwirken Sie Kommissionen auf jeden von Ihnen vermittelten Verkauf — monatlich über PayPal ausgezahlt"
  }
]
```

Der visuelle Fluss nummeriert automatisch jeden Schritt (1, 2, 3, 4) auf der Startseite.

## CTA-Bereich

Der letzte Abschnitt vor dem Registrierungsformular ist der **Call-to-Action (CTA)-Bereich**. Er bietet eine letzte Push, um Registrierungen zu fördern.

| Feld | Beispielwert | Zweck |
|------|--------------|-------|
| **CTA-Titel** | "Bereit, um zu verdienen?" | Direkte Frage erzeugt Dringlichkeit |
| **CTA-Beschreibung** | "Treten Sie heute unserem Affiliate-Programm bei und beginnen Sie, Kommissionen für Produkte zu verdienen, die Sie bereits lieben und empfehlen." | Vorteile stärken und Reibung reduzieren |

Der CTA-Bereich zeigt automatisch die Schaltfläche **Partner werden** unter dem Text an.

## Registrierungseinstellungen

Steuern Sie, wie neue Partner sich registrieren und welche Informationen sie bereitstellen.

### Anpassbares Registrierungsformular

**Feld:** `custom_form` (ForeignKey zu FormBuilder-Formular)

Wenn Sie ein benutzerdefiniertes Registrierungsformular mit dem Spwig Form Builder erstellt haben, wählen Sie es hier aus. Dies ermöglicht es Ihnen, zusätzliche Informationen während der Registrierung zu sammeln (z. B. Website-URL, Zielgruppengröße, Promotion-Kanäle).

**Leer lassen** um das Standard-Registrierungsformular für Affiliate (E-Mail, Passwort, Zahlungsdetails) zu verwenden.

### Gastregistrierung erlauben

**Feld:** `allow_guest_registration` (Boolesch)

- **Markiert** — Besucher können sich ohne erstellen Spwig-Konto anmelden
- **Nicht markiert** — Besucher müssen sich anmelden oder ein Kundenkonto erstellen, bevor sie sich anmelden

**Empfehlung:** Aktivieren Sie die Gastregistrierung, um Reibung zu reduzieren. Sie können immer die Genehmigung erfordern, um Partner vor der Aktivierung zu prüfen.

### Genehmigung erforderlich

**Feld:** `require_approval` (Boolesch)

- **Markiert** — Neue Partner müssen auf manuelle Genehmigung warten, bevor sie auf ihr Dashboard zugreifen können
- **Nicht markiert** — Neue Partner werden automatisch genehmigt und können Links sofort erstellen

**Empfehlung:** Aktivieren Sie manuelle Genehmigung, wenn Sie Partner für Markenpassform, Betrugsschutz oder exklusive Programme prüfen möchten.

### Geschäftsbedingungen-URL

**Feld:** `terms_url` (URL)

Optionaler Link zu den Geschäftsbedingungen Ihres Affiliate-Programms. Wenn bereitgestellt, wird im Registrierungsformular ein Häkchenfeld angezeigt, das Partner dazu verpflichtet, Ihre Geschäftsbedingungen zu akzeptieren, bevor sie sich registrieren.

**Beispiel:** `/pages/affiliate-terms/`

### Willkommensnachricht

**Feld:** `welcome_message` (Text)

Nachricht, die Partner sofort nach einer erfolgreichen Registrierung angezeigt wird. Verwenden Sie dies, um:

- Sie für die Teilnahme zu danken
- Die nächsten Schritte zu erklären (z. B. "Wir werden Ihre Bewerbung innerhalb von 24 Stunden prüfen")
- Links zu Startressourcen bereitzustellen

**Beispiel:"
```
Willkommen in unserem Affiliate-Programm! Wir haben Ihre Bewerbung erhalten und werden sie innerhalb von 24 Stunden prüfen. Prüfen Sie Ihre E-Mail für die Genehmigung und Anmeldeanweisungen.
```

## Mehrsprachige Unterstützung

Alle Textfelder in Affiliate-Einstellungen sind **übersetzbar** mithilfe des Spwig-Übersetzungssystems:

- Hero-Titel
- Hero-Untertitel
- Features (JSON pro Sprache übersetzt)
- Wie es funktioniert Schritte (JSON pro Sprache übersetzt)
- CTA-Titel
- CTA-Beschreibung
- Willkommensnachricht

### Wie Übersetzung funktioniert

Wenn Sie ein übersetzbares Feld bearbeiten, sehen Sie ein Übersetzungstool, das es Ihnen ermöglicht, Inhalt für jede aktiviert Sprache bereitzustellen. Für JSON-Felder (Features, Schritte) geben Sie separate JSON-Objekte pro Sprache an:

**Englisch:"
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**Spanisch:"
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

Das Portal zeigt automatisch die richtige Sprachversion basierend auf der Sprachpräferenz des Besuchers.

## Änderungen Vorschau

Nachdem Sie das Portal-Einstellungen angepasst haben:

1. **Speichern** Sie Ihre Änderungen im Admin
2. Besuchen Sie `/affiliate/` auf der Frontend Ihres Geschäfts (öffnen Sie in einem neuen Tab)
3. **Testen Sie den Registrierungsfluss** durch Klicken auf "Partner werden"
4. **Überprüfen Sie die Markenkonsistenz** — stimmt das Portal mit dem Design und der Botschaft Ihres Geschäfts überein?

Sie können iterative Änderungen vornehmen und die Seite aktualisieren, um sofortige Updates zu sehen.

## Beispielanpassungen

### Szenario 1: E-Commerce Modegeschäft

**Ziel:** Rekrutieren Sie Mode-Influencer und Blogger.

| Einstellung | Wert |
|-------------|-------|
| Hero-Titel | "Promote Styles You Love & Earn" |
| Hero-Untertitel | "Join 1,200+ influencers earning 12% commissions on every sale" |
| Feature 1 | Icon: `fa-tshirt`, Titel: "Curated Fashion Collections", Beschreibung: "Promote premium apparel and accessories" |
| Feature 2 | Icon: `fa-percentage`, Titel: "12% Commission", Beschreibung: "Industry-leading rates on all products" |
| Feature 3 | Icon: `fa-camera`, Titel: "Exklusiver Inhalt", Beschreibung: "Access product photos, videos, and campaign assets" |
| Gastregistrierung erlauben | Markiert |
| Genehmigung erforderlich | Markiert (manuelle Prüfung für Markenpassform) |

### Szenario 2: B2B SaaS Partnerprogramm

**Ziel:** Rekrutieren Sie Berater und Agenturen für Unternehmenssoftware-Verweisungen.

| Einstellung | Wert |
|-------------|-------|
| Hero-Titel | "Partner With Us to Grow Revenue" |
| Hero-Untertitel | "Earn $500 per enterprise referral through our B2B partner program" |
| Feature 1 | Icon: `fa-handshake`, Titel: "$500 Pro Referral", Beschreibung: "Festgelegte Kommission für qualifizierte Unternehmensleads" |
| Feature 2 | Icon: `fa-clock`, Titel: "180-Day Cookie", Beschreibung: "Lange Attributionsfenster für komplexe Verkaufszyklen" |
| Feature 3 | Icon: `fa-user-tie`, Titel: "Dedicated Partner Manager", Beschreibung: "White-glove Support für Ihre Kunden" |
| Gastregistrierung erlauben | Nicht markiert (B2B erfordert Konto) |
| Genehmigung erforderlich | Markiert (einladungsbasiertes Programm) |
| Geschäftsbedingungen-URL | `/pages/partner-programm-terms/` |

## Tipps

- Anpassen Sie Ihren **Hero-Titel**, um sich auf Vorteile, nicht auf Features zu konzentrieren — "Earn While You Sleep" ist überzeugender als "Affiliate Program Sign-Up"
- Verwenden Sie **sozialen Beweis** im Untertitel (z. B. "Join 500+ affiliates") um Vertrauen und Glaubwürdigkeit aufzubauen
- Wählen Sie **FontAwesome-Icons**, die den jeweiligen Vorteil visuell unterstreichen — das Icon sollte den Wert sofort kommunizieren
- Halten Sie die Feature-Beschreibungen auf **1-2 Sätze** — das Portal ist für Konversionen, nicht für umfassende Erklärungen
- Testen Sie den **Registrierungsfluss** selbst, bevor Sie das Portal bewerben — erkennen Sie Reibungspunkte wie verwirrende Formularfelder oder defekte Links
- Aktivieren Sie **Gastregistrierung**, um die Registrierungsreibung zu reduzieren, und verwenden Sie **Genehmigung erforderlich**, um Partner nach der Einreichung zu prüfen
- Verwenden Sie die **Willkommensnachricht**, um Erwartungen zu setzen (Genehmigungstermin, nächste Schritte, Support-Kontakt) und Support-Anfragen zu reduzieren
- Aktualisieren Sie das Portal **saisonal**, um mit Kampagnen abzugleichen — betonen Sie besondere Kommissionspromotionen oder Produktstarts

Erinnern Sie sich: Bewahren Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe genau wie in den Erhaltungsvorschriften gezeigt.