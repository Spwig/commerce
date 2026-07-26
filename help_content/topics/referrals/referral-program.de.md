---
title: Referral Programm
---

Das Referral-Programm ermöglicht es Ihren bestehenden Kunden, einen eindeutigen Referral-Link mit ihren Freunden und Familie zu teilen. Wenn ein verworbener Freund seine erste qualifizierende Kauf tätigt, können sowohl der Verweisgeber als auch der neue Kunde eine Belohnung erhalten – dadurch wird die Neukundengewinnung durch Mund-zu-Mund-Propaganda gefördert.

## Wie das Referral-Programm funktioniert

1. Ein Kunde teilt seinen eindeutigen Referral-Link (oder Code) mit einem Freund.
2. Der Freund klickt auf den Link und wird über einen Cookie bis zu 30 Tage (konfigurierbar) verfolgt.
3. Der Freund registriert sich und tätigt seinen ersten qualifizierenden Auftrag.
4. Das System erstellt einen Referral-Zuordnungsdatensatz und führt Betrugs- und Eignungsprüfungen durch.
5. Wenn die Zuordnung genehmigt wird, werden Belohnungen an beide Parteien ausgeschüttet.

Ihr Geschäft hat eine einzige Referral-Programm-Konfiguration. Navigieren Sie zu **Marketing > Referral Programm**, um es einzurichten.

## Einrichtung Ihres Referral-Programms

### Programmstatus

Das Programm hat drei Zustände:

- **Entwurf** — Das Programm wird konfiguriert, ist aber noch nicht aktiv. Referral-Links sind inaktiv.
- **Aktiv** — Das Programm ist aktiv. Kunden können Links teilen und Belohnungen verdienen.
- **Pausiert** — Das Programm ist vorübergehend gestoppt. Bestehende Zuordnungen werden weiter verarbeitet, aber keine neuen Referrals werden verfolgt.

Setzen Sie den **Status** auf **Aktiv**, wenn Sie bereit sind, das Programm zu starten. Sie können es jederzeit pausieren.

### Belohnungskonfiguration

Definieren Sie die Belohnungen, die bei einer erfolgreichen Verweisung ausgeschüttet werden. Das Programm unterstützt **zweiseitige Belohnungen** – das bedeutet, Sie können sowohl den Verweisgeber (den Kunden, der den Link geteilt hat) als auch den Verweisenen (den neuen Kunden, der den Link genutzt hat) belohnen.

Konfigurieren Sie Belohnungen für jeden Empfänger im Feld **Belohnungskonfiguration**. Die verfügbaren Belohnungstypen sind:

| Belohnungstyp | Beschreibung |
|---------------|-------------|
| **Guthaben für den Laden** | Fügt dem Kundenkonto Guthaben hinzu, das bei zukünftigen Bestellungen verwendet werden kann |
| **Gutscheincode** | Erstellt einen eindeutigen Rabatt-Gutschein-Code |
| **Prozentualer Rabatt** | Erstellt einen prozentualen Rabatt, der am Kasse verwendet werden kann |
| **Exklusive Vorteile** | Ein benutzerdefinierter Vorteil (z. B. kostenlose Geschenke, Vorrangzugang) – beschrieben im Beschreibungsfeld der Belohnung |

Gutscheincode- und Prozentualer Rabatt-Belohnungen sind an den Kunden gebunden, der sie verdient hat – der Gutscheincode funktioniert nur, wenn dieser Kunde angemeldet ist. Wenn ein Verweisgeber seinen Belohnungscode stattdessen mit jemand anderem teilt, anstatt seinen Verweislink, kann der Freund ihn nicht verwenden; nur der Verweislink selbst ist zum Teilen vorgesehen.

**Beispielkonfiguration** – 10 $ Guthaben für den Verweisgeber und 10 $ Rabatt für den neuen Kunden:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Setzen Sie `"double_sided": false`, wenn Sie nur den Verweisgeber belohnen möchten.

### Eignungsregeln

Eignungsregeln bestimmen, welche Verweisungen für Belohnungen qualifiziert sind. Konfigurieren Sie diese im Feld **Eignungsregeln**:

| Regel | Was es tut |
|------|--------------|
| `new_customer_only` | Wenn `true`, muss der verworbene Freund ein neuer Kunde sein (keine früheren Bestellungen) |
| `min_order_value` | Der minimale Bestellwert (in der Währung Ihres Geschäfts), den der verworbene Freund ausgeben muss |
| `exclude_discounts` | Wenn `true`, werden Bestellungen, bei denen der verworbene Kunde einen Gutschein verwendet hat, nicht qualifiziert |
| `exclude_staff` | Wenn `true`, können Mitarbeiterkonten weder als Verweisgeber noch als Verweisenen fungieren |

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

Das Feld **Zeitplanungskonfiguration** steuert, wann Belohnungen nach einer qualifizierenden Bestellung ausgeschüttet werden:

| Einstellung | Was es tut |
|---------|--------------|
| `issue_on` | Wann die Belohnung ausgeschüttet wird: `signup` (sofort bei der Registrierung), `first_purchase` (sofort nach der Bestellung) oder `post_refund` (nach Ablauf der Rückerstattungszeit) |
| `refund_window_days` | Wie viele Tage gewartet werden sollen, bevor Belohnungen ausgeschüttet werden, wenn `post_refund` verwendet wird (Standard: 14 Tage) |


Die Verwendung von `post_refund` ist der vorsichtigste Ansatz — sie wartet, bis das Rückgabewindow abgelaufen ist, bevor Belohnungen vergeben werden, was das Risiko verringert, Bestellungen zu belohnen, die später erstattet werden.

### Obergrenzen und Limits

Verhindern Sie, dass ein einzelner Verweisgeber unbegrenzte Belohnungen erhält, indem Sie Obergrenzen im Feld **Obergrenzen & Limits** festlegen:

| Einstellung | Was es tut |
|---------|--------------|
| `monthly_per_referrer` | Maximale Anzahl der erfolgreich vermittelten Verweise pro Monat pro Verweisgeber |
| `lifetime_per_referrer` | Gesamte maximale Anzahl der erfolgreich vermittelten Verweise pro Verweisgeber |
| `max_reward_per_order` | Maximale Belohnungssumme (in der Währung Ihres Geschäfts) für einen einzigen Verweis |

**Beispiel** — 20 Verweise pro Monat, 200 im Leben, maximal 50 $ pro Umwandlung:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Tracking-Konfiguration

Konfigurieren Sie, wie Verweislinks verfolgt werden, im Feld **Tracking-Konfiguration**:

| Einstellung | Was es tut |
|---------|--------------|
| `cookie_ttl_days` | Wie viele Tage das Tracking-Cookie aktiv bleibt, nachdem ein Freund auf den Link geklickt hat (Standard: 30) |
| `attribution` | Zuordnungsmodell — derzeit `last_touch` (der letzte Klick auf einen Verweislink wird angerechnet) |

### Betrugsrichtlinie

Das Betrugsdetektionssystem bewertet automatisch jede Verweiszuordnung auf Risiko, bevor sie genehmigt wird. Konfigurieren Sie die Richtlinie im Feld **Betrugsrichtlinie**:

| Einstellung | Was es tut |
|---------|--------------|
| `policy` | Allgemeine Strenge: `strict`, `balanced` oder `lenient` |
| `auto_reject_threshold` | Risikowert (0–100), ab dem Zuordnungen automatisch abgelehnt werden (Standard: 80) |
| `auto_approve_threshold` | Risikowert, unter dem Zuordnungen automatisch genehmigt werden (Standard: 30) |
| `check_ip` | Wenn `true`, wird geprüft, ob Verweisgeber und Verweisnehmer dieselbe IP-Adresse haben |
| `check_device` | Wenn `true`, werden gemeinsame Gerätefingerprints zwischen Verweisgeber und Verweisnehmer geprüft |
| `check_velocity` | Wenn `true`, werden ungewöhnlich hohe Verweisraten von einer Quelle überwacht |
| `velocity_window_hours` | Die Zeitspanne (in Stunden) für die Geschwindigkeitsprüfung |
| `max_referrals_per_window` | Maximale Anzahl an Verweisen, die von einer Quelle innerhalb des Geschwindigkeitsfensters erlaubt sind |

Zuordnungen mit einem Risikowert zwischen den automatischen Ablehnungs- und Genehmigungsschwellen landen im Status **Ausstehend** und benötigen eine manuelle Prüfung.

### Allgemeine Geschäftsbedingungen

Geben Sie hier beliebige rechtliche Geschäftsbedingungen für das Programm im Feld **Allgemeine Geschäftsbedingungen** an. Dieser Text wird Kunden angezeigt, wenn sie das Verweisprogramm ansehen. Markdown-Formatierung wird unterstützt.

## Anzeigen von Verweiszuordnungen

Navigieren Sie zu **Marketing > Verweiszuordnungen**, um alle Verweisfälle anzuzeigen — die Verbindung zwischen einem Verweisgeber und einem Verweisnehmer.

![Liste der Verweiszuordnungen](/static/core/admin/img/help/referral-program/attribution-list.webp)

Jede Zuordnung zeigt den Verweisgeber, den Verweisnehmer, die erste Bestellung, die sie platziert haben, den aktuellen Status und den Risikowert an.

### Zuordnungsstatusse

| Status | Was es bedeutet |
|--------|---------------|
| **Ausstehend** | Warte auf Prüfung — der Risikowert liegt im manuellen Prüfbereich |
| **Genehmigt** | Verweis ist gültig — Belohnungen wurden oder werden vergeben |
| **Abgelehnt** | Verweis war nicht qualifiziert oder wurde als betrügerisch markiert |
| **Abgelaufen** | Der Verweis wurde nicht innerhalb des Trackingfensters umgewandelt |

### Manuelle Genehmigung oder Ablehnung von Zuordnungen

Für Zuordnungen im Status **Ausstehend** können Sie diese manuell genehmigen oder ablehnen, indem Sie das Zuordnungsprotokoll öffnen und die Aktionstasten verwenden. Bei der Ablehnung wählen Sie einen **Ablehnungsgrund**:

- Selbstverweis
- Nicht neuer Kunde
- Unter dem Mindestbestellwert
- Abwerbeweitere-Mail
- Obergrenze überschritten
- Betrugsrisiko
- Bestellung erstattet oder storniert
- Manuelle Ablehnung

Sie können auch **Ablehnungsnotizen** für Ihre eigenen Aufzeichnungen hinzufügen.

### Nach Risikostufe filtern

Verwenden Sie den Filter **Risikostufe** in der Seitenleiste, um sich auf hochriskante Zuordnungen zu konzentrieren, die eine Prüfung benötigen:

- Niedriges Risiko (Bewertung 0–30) — Automatisch genehmigt
- Mittleres Risiko (Bewertung 31–70) — Manuelle Prüfung
- Hoches Risiko (Bewertung 71–89) — Manuelle Prüfung, vorsichtig behandeln
- Sehr hohes Risiko (Bewertung 90+) — Automatisch abgelehnt

## Anzeigen von vergebenen Belohnungen

Navigieren Sie zu **Marketing > Vergebene Belohnungen**, um alle Belohnungen anzuzeigen, die als Ergebnis genehmigter Zuordnungen vergeben wurden.

Jeder Eintrag einer Belohnung zeigt den Kunden, ob er der Empfehler oder der Empfänger ist, die Art und Höhe der Belohnung sowie den aktuellen Gutschriftenstatus an.

### Belohnungsstatus

| Status | Was es bedeutet |
|--------|---------------|
| **Ausstehend** | Die Belohnung wurde erstellt, wurde aber noch nicht an den Kunden übermittelt |
| **Vergeben** | Die Belohnung ist aktiv und kann vom Kunden verwendet werden |
| **In Anspruch genommen** | Der Kunde hat die Belohnung bereits verwendet |
| **Abgelaufen** | Die Belohnung ist abgelaufen, ohne dass sie genutzt wurde |
| **Widerrufen** | Die Belohnung wurde manuell storniert (z. B., wenn die ursprüngliche Bestellung nach Vergabe der Belohnung erstattet wurde) |

### Widerrufen einer Belohnung

Wenn eine Belohnung widerrufen werden muss — beispielsweise, wenn die qualifizierende Bestellung retourniert wurde — öffnen Sie den Eintrag der Belohnung und verwenden Sie die Aktion **Widerrufen**. Fügen Sie eine Notiz hinzu, die erklärt, warum die Belohnung widerrufen wurde, um Ihre Unterlagen zu dokumentieren.

## Tipps

- Beginnen Sie mit der Einstellung `post_refund`. Das Warten, bis das Retourenfenster abgelaufen ist, bevor Belohnungen vergeben werden, verhindert, dass Bestellungen, die letztendlich retourniert werden, belohnt werden.
- Die `balanced` Betrugsrichtlinie ist eine gute Standardrichtlinie für die meisten Geschäfte. Wechseln Sie zu `strict`, wenn Sie eine ungewöhnliche Steigerung der Empfehlungen von einer geringen Anzahl von Konten bemerken.
- Legen Sie realistische monatliche und lebenslange Obergrenzen fest. Wenn der Wert der Belohnung hoch ist, ist eine Obergrenze von 10–20 pro Monat pro Empfehler angemessen, um Missbrauch zu verhindern.
- Prüfen Sie **Ausstehende** Zuordnungen wöchentlich. Das Ignorieren von Zuordnungen zu lange kann legitime Empfehler frustrieren, die auf ihre Belohnung warten.
- Verwenden Sie den **Risikostufe**-Filter, um Ihre manuelle Prüfungswarteschlange zu priorisieren — beginnen Sie mit den sehr hohen Risikozuordnungen, bevor Sie zu mittlerem Risiko übergehen.
- Halten Sie Ihre **Allgemeinen Geschäftsbedingungen** kurz und in einfacher Sprache. Kunden sind eher bereit, teilzunehmen, wenn sie die Regeln klar verstehen.