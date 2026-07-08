---
title: Referral Program
---

Das Referral-Programm ermöglicht es Ihren bestehenden Kunden, einen eindeutigen Referral-Link mit ihren Freunden und Familie zu teilen. Wenn ein verworbener Freund seine erste qualifizierende Kauf tätigt, können sowohl der Verweisgeber als auch der neue Kunde eine Belohnung erhalten – dadurch wird die Neukundengewinnung durch Mund-zu-Mund-Propaganda gefördert.

## Wie das Referral-Programm funktioniert

1. Ein Kunde teilt seinen eindeutigen Referral-Link (oder Code) mit einem Freund.
2. Der Freund klickt auf den Link und wird über einen Cookie bis zu 30 Tage (konfigurierbar) verfolgt.
3. Der Freund registriert sich und tätigt seinen ersten qualifizierenden Auftrag.
4. Das System erstellt einen Referral-Zuordnungsdatensatz und führt Betrugs- und Berechtigungschecks durch.
5. Wenn die Zuordnung genehmigt wird, erhalten beide Parteien Belohnungen.

Ihr Geschäft hat eine einzige Referral-Programm-Konfiguration. Navigieren Sie zu **Marketing > Referral Program**, um sie einzurichten.

## Einrichtung Ihres Referral-Programms

### Programstatus

Das Programm hat drei Zustände:

- **Entwurf** — Das Programm wird konfiguriert, ist aber noch nicht aktiv. Referral-Links sind inaktiv.
- **Aktiv** — Das Programm ist aktiv. Kunden können Links teilen und Belohnungen verdienen.
- **Pausiert** — Das Programm ist vorübergehend gestoppt. Bestehende Zuordnungen werden weiter verarbeitet, aber keine neuen Referrals werden verfolgt.

Setzen Sie den **Status** auf **Aktiv**, wenn Sie bereit sind, das Programm zu starten. Sie können es jederzeit pausieren.

### Belohnungskonfiguration

Definieren Sie die Belohnungen, die bei einer erfolgreichen Verweisung vergeben werden. Das Programm unterstützt **zweiseitige Belohnungen** – das bedeutet, dass Sie sowohl den Verweisgeber (den Kunden, der den Link geteilt hat) als auch den Verweisenen (den neuen Kunden, der den Link genutzt hat) belohnen können.

Konfigurieren Sie Belohnungen für jeden Empfänger im Feld **Belohnungskonfiguration**. Die verfügbaren Belohnungstypen sind:

| Belohnungstyp | Beschreibung |
|---------------|-------------|
| **Guthaben für den Laden** | Fügt Guthaben in das Kundenkonto hinzu, das bei zukünftigen Bestellungen verwendet werden kann |
| **Gutscheincode** | Erstellt einen eindeutigen Rabatt-Gutschein-Code |
| **Prozentualer Rabatt** | Verleiht einen prozentualen Rabatt, der bei der Kasse verwendet werden kann |
| **Exklusive Vorteile** | Ein benutzerdefinierter Vorteil (z. B. kostenlose Geschenke, Vorrangzugang) – beschrieben im Beschreibungsfeld der Belohnung |

**Beispielkonfiguration** – 10 $ Guthaben für den Verweisgeber und 10 $ Rabatt für den neuen Kunden:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Setzen Sie `"double_sided": false`, wenn Sie nur den Verweisgeber belohnen möchten.

### Berechtigungsregeln

Berechtigungsregeln bestimmen, welche Verweisungen für Belohnungen qualifiziert sind. Konfigurieren Sie diese im Feld **Berechtigungsregeln**:

| Regel | Was es tut |
|------|--------------|
| `new_customer_only` | Wenn `true`, muss der verworbene Freund ein neuer Kunde sein (keine früheren Bestellungen) |
| `min_order_value` | Der minimale Bestellwert (in der Währung Ihres Geschäfts), den der verworbene Freund ausgeben muss |
| `exclude_discounts` | Wenn `true`, werden Bestellungen, bei denen der verworbene Kunde einen Gutschein verwendet hat, nicht berücksichtigt |
| `exclude_staff` | Wenn `true`, können Mitarbeiterkonten nicht als Verweisgeber oder Verweisenen fungieren |

**Beispiel** – nur neue Kunden, minimaler Bestellwert von 40 $, Mitarbeiter ausgeschlossen:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Zeitplanungskonfiguration

Das Feld **Zeitplanungskonfiguration** steuert, wann Belohnungen nach einer qualifizierenden Bestellung vergeben werden:

| Einstellung | Was es tut |
|---------|--------------|
| `issue_on` | Wann die Belohnung vergeben wird: `signup` (sofort bei der Registrierung), `first_purchase` (sofort nach der Bestellung) oder `post_refund` (nach Ablauf der Rückgabefrist) |
| `refund_window_days` | Wie viele Tage gewartet werden sollen, bevor Belohnungen vergeben werden, wenn `post_refund` verwendet wird (Standard: 14 Tage) |

Die Verwendung von `post_refund` ist der vorsichtigste Ansatz – es wartet, bis die Rückgabefrist abgelaufen ist, bevor Belohnungen vergeben werden, was das Risiko verringert, Bestellungen zu belohnen, die später erstattet werden.

### Grenzen und Limits

Verhindern Sie, dass ein einzelner Verweisgeber unbegrenzte Belohnungen erhält, indem Sie Grenzen im Feld **Grenzen und Limits** festlegen:

Beispiel — 20 Referrals pro Monat, 200 im Leben, maximal 50 USD pro Vermittlung:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

Konfigurieren Sie, wie Referral-Links verfolgt werden, im Feld **Tracking-Konfiguration**:

Das Betrugsdetektionssystem bewertet automatisch jeden Referral-Zuordnung auf Risiko, bevor sie genehmigt wird. Konfigurieren Sie die Richtlinie im Feld **Betrugsrichtlinie**:

Zuordnungen mit einem Risikowert zwischen den automatischen Ablehnungs- und Genehmigungsschwellen landen im Status **Ausstehend** und benötigen eine manuelle Prüfung.

Geben Sie hier beliebige rechtliche Bedingungen für das Programm im Feld **Nutzungsbedingungen** an. Dieser Text wird Kunden angezeigt, wenn sie das Referral-Programm ansehen. Markdown-Formatierung wird unterstützt.

Navigieren Sie zu **Marketing > Referral-Zuordnungen**, um alle Referral-Fälle anzuzeigen — die Verbindung zwischen einem Vermittler und einem Referenzkunden.

Liste der Referral-Zuordnungen

/static/core/admin/img/help/referral-program/attribution-list.webp

Jede Zuordnung zeigt den Vermittler, den Referenzkunden, den ersten Bestellung, den aktuellen Status und den Risikowert an.

Für Zuordnungen im Status **Ausstehend** können Sie diese manuell genehmigen oder ablehnen, indem Sie das Zuordnungsprotokoll öffnen und die Aktionstasten verwenden. Bei Ablehnung wählen Sie einen **Ablehnungsgrund**:

Sie können auch **Ablehnungsnotizen** für Ihre eigenen Aufzeichnungen hinzufügen.

Verwenden Sie den Filter **Risikostufe** in der Seitenleiste, um sich auf hochriskante Zuordnungen zu konzentrieren, die eine Prüfung benötigen:

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Navigieren Sie zu **Marketing > Ausgestellte Belohnungen**, um alle Belohnungen anzuzeigen, die als Ergebnis genehmigter Zuordnungen ausgestellt wurden.

Jeder Eintrag einer Belohnung zeigt den Kunden, ob er der Empfehler oder der Empfänger ist, die Art und Höhe der Belohnung sowie den aktuellen Gutschriftenstatus an.

### Belohnungsstatus

| Status | Was es bedeutet |
|--------|---------------|
| **Ausstehend** | Die Belohnung wurde erstellt, wurde aber noch nicht an den Kunden ausgestellt |
| **Ausgestellt** | Die Belohnung ist aktiv und steht dem Kunden zur Verwendung zur Verfügung |
| **In Anspruch genommen** | Der Kunde hat die Belohnung bereits genutzt |
| **Abgelaufen** | Die Belohnung ist abgelaufen, ohne dass sie genutzt wurde |
| **Widerrufen** | Die Belohnung wurde manuell storniert (z. B., wenn die ursprüngliche Bestellung nach Ausstellung der Belohnung erstattet wurde) |

### Widerrufen einer Belohnung

Wenn eine Belohnung widerrufen werden muss – beispielsweise, wenn die qualifizierende Bestellung retourniert wurde – öffnen Sie den Belohnungseintrag und verwenden Sie die Aktion **Widerrufen**. Fügen Sie eine Notiz hinzu, die erklärt, warum die Belohnung widerrufen wurde, um Ihre Unterlagen zu dokumentieren.

## Tipps

- Beginnen Sie mit der Einstellung `post_refund`. Das Warten, bis das Retourenfenster abgelaufen ist, bevor Belohnungen ausgestellt werden, verhindert, dass Bestellungen belohnt werden, die am Ende retourniert werden.
- Die `balanced` Betrugsrichtlinie ist eine gute Standardrichtlinie für die meisten Geschäfte. Wechseln Sie zu `strict`, wenn Sie eine ungewöhnliche Steigerung der Empfehlungen von einer geringen Anzahl von Konten bemerken.
- Setzen Sie realistische monatliche und lebenslange Obergrenzen. Wenn der Wert Ihrer Belohnung hoch ist, ist eine Obergrenze von 10–20 pro Monat pro Empfehler angemessen, um Missbrauch zu verhindern.
- Überprüfen Sie **Ausstehende** Zuordnungen wöchentlich. Das Ignorieren von unüberprüften Zuordnungen zu lange kann legitime Empfehler frustrieren, die auf ihre Belohnung warten.
- Verwenden Sie den Filter **Risikostufe**, um Ihre manuelle Prüfungsliste zu priorisieren – beginnen Sie mit den Zuordnungen mit sehr hohem Risiko, bevor Sie zu mittlerem Risiko übergehen.
- Halten Sie Ihre **Allgemeinen Geschäftsbedingungen** kurz und in einfacher Sprache. Kunden sind eher bereit, teilzunehmen, wenn sie die Regeln klar verstehen.