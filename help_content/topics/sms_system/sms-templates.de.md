---
title: SMS-Vorlagen
---

SMS-Vorlagen steuern den Text jeder Benachrichtigung, die Ihr Geschäft über SMS an Kunden sendet. Jede Vorlage entspricht einem bestimmten Ereignis – wie eine Bestellbestätigung oder eine Versandaktualisierung – und verwendet Platzhaltervariablen, die Spwig mit den tatsächlichen Bestelldetails ersetzt, wenn die Nachricht gesendet wird.

Navigieren Sie zu **SMS-System > SMS-Vorlagen**, um Ihre Vorlagen anzuzeigen und zu bearbeiten.

![Liste der SMS-Vorlagen](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Verfügbare Vorlagenarten

Spwig enthält die folgenden integrierten Vorlagenarten:

| Vorlagenart | Wann gesendet |
|---------------|-----------------|
| Bestellbestätigung | Wenn ein Kunde eine Bestellung aufgibt |
| Versandaktualisierung | Wenn sich der Tracking-Status einer Bestellung ändert |
| Lieferbenachrichtigung | Wenn eine Bestellung als geliefert markiert wird |
| Passwortzurücksetzen | Wenn ein Kunde ein Passwortzurücksetzen anfordert |
| Verifizierungscode | Wenn ein Einmalcode für die Kontoverifizierung benötigt wird |
| POS-Rechnung | Wenn eine Verkaufsabwicklung an einem Kassenterminal erfolgt |
| Marketing | Für Werbekampagnen (erfordert separate Zustimmung) |
| Benutzerdefiniert | Für jede andere Benachrichtigung, die Sie erstellen |

## Vorlage bearbeiten

1. Navigieren Sie zu **SMS-System > SMS-Vorlagen**
2. Klicken Sie auf die Vorlage, die Sie bearbeiten möchten
3. Aktualisieren Sie das Feld **Nachricht** mit Ihrem gewünschten Text
4. Verwenden Sie Platzhalter `{variable}`, um Informationen zu spezifischen Bestellungen einzubeziehen (siehe Variablen unten)
5. Aktivieren Sie **Aktiv**, um die Vorlage zu aktivieren – inaktive Vorlagen werden nicht gesendet
6. Klicken Sie auf **Speichern**

![Bearbeiten einer SMS-Vorlage](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Variablen verwenden

Variablen sind Platzhalter, die in geschweiften Klammern geschrieben werden – zum Beispiel `{name}` oder `{order_number}`. Wenn Spwig die Nachricht sendet, ersetzt es jeden Platzhalter durch den tatsächlichen Wert für diesen Kunden oder diese Bestellung.

### Häufige Variablen

| Variable | Wird ersetzt durch |
|----------|---------------|
| `{name}` | Der Vorname des Kunden |
| `{order_number}` | Die Bestellreferenznummer |
| `{total}` | Der Gesamtbetrag der Bestellung |
| `{tracking_number}` | Die Versand-Tracking-Nummer |
| `{store_name}` | Der Name Ihres Geschäfts |
| `{code}` | Ein Verifizierungs- oder Zurücksetzungscode |

**Beispielnachricht:**

```
Hi {name}, your order #{order_number} has been confirmed. Total: {total}. We'll update you when it ships. - {store_name}
```

Wenn gesendet, wird das zu:

```
Hi Sarah, your order #10045 has been confirmed. Total: $89.00. We'll update you when it ships. - The Garden Shop
```

> Nur Variablen einbeziehen, die für eine bestimmte Vorlagenart verfügbar sind. Zum Beispiel ist `{tracking_number}` in einer Versandaktualisierungsvorlage verfügbar, aber nicht in einer Passwortzurücksetzungsvorlage. Wenn Sie eine nicht verfügbare Variable verwenden, wird sie so wie sie ist (nicht ersetzt) in der Nachricht angezeigt.

## Zeichenbegrenzung und Nachrichtenlänge

Standard-SMS-Nachrichten sind auf **160 Zeichen** für einen Segment begrenzt. Längere Nachrichten werden in mehrere Segmente aufgeteilt und als eine (zusammengesetzte SMS) gesendet, aber die Anbieter zählen jedes Segment einzeln zur Abrechnung.

**Tipps, um die Grenze einzuhalten:**
- Halten Sie Nachrichten kurz – eine Zweck pro Nachricht
- Kürzen Sie gängige Phrasen, wo natürliche (z. B. „Ord“ anstelle von „Order“)
- Vermeiden Sie unnötige Füllwörter

Spwig erzwingt keine harte Zeichenbegrenzung im Editor, also zählen Sie Ihre Zeichen (einschließlich Variablenwerte) vor dem Speichern.

## Aktivieren und Deaktivieren von Vorlagen

Der **Aktiv**-Schalter auf jeder Vorlage steuert, ob dieser Benachrichtigungstyp gesendet wird. Wenn eine Vorlage inaktiv ist, überspringt Spwig das Senden dieser Benachrichtigung vollständig – die Nachricht wird als **Übersprungen** im SMS-Ausgangsordner angezeigt, mit dem Grund `template_inactive`.

Um eine Vorlage zu aktivieren:
1. Öffnen Sie die Vorlage
2. Aktivieren Sie das **Aktiv**-Kästchen
3. Speichern Sie

Um eine Vorlage zu deaktivieren (Senden einer Benachrichtigungstyp ohne die Vorlage zu löschen):
1. Öffnen Sie die Vorlage
2. Deaktivieren Sie **Aktiv**
3. Speichern Sie

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Verwenden Sie eine Stimme, die mit Ihrer Marke übereinstimmt – SMS ist ein direkter, persönlicher Kommunikationskanal, daher eignet sich ein freundlicher Ton gut
- Fügen Sie immer den Namen Ihres Geschäfts in die Nachricht ein, damit Kunden wissen, wer sie anruft
- Halten Sie Bestätigungs-Nachrichten kurz: Die Bestellnummer, der Gesamtbetrag und eine Anmerkung zu den nächsten Schritten reichen aus
- Testen Sie Nachrichten, indem Sie eine Testbestellung auf Ihrem eigenen Geschäft tätigen (mit einer Telefonnummer, die Sie kontrollieren), um zu sehen, was Kunden tatsächlich erhalten
- Deaktivieren Sie eine Vorlage und überarbeiten Sie sie, wenn eine Benachrichtigung Verwirrung oder Beschwerden auslöst, anstatt sie zu löschen – so können Sie sie nach der Aktualisierung wieder aktivieren
- Marketing-Vorlagen dürfen nur an Kunden gesendet werden, die explizit in das SMS-Marketing eingewilligt haben, wie es in den Telekommunikationsvorschriften der meisten Länder erforderlich ist