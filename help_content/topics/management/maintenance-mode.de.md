---
title: Wartungsmodus
---

Der Wartungsmodus schaltet Ihr Verkaufsportal vorübergehend offline und zeigt Kunden eine Nachricht wie „Wir kommen bald wieder“ an. Während der Wartung bleibt Ihr Admin-Backend weiterhin vollständig zugänglich – Sie können weiterarbeiten, während Kunden auf der Wartungsseite gehalten werden.

Verwenden Sie den Wartungsmodus, bevor Sie Änderungen vornehmen, die zu einem kurzen inkonsistenten Zustand führen könnten, wie beispielsweise das Durchführen eines großen Produkteinimports, das Anwenden einer umfassenden Theme-Umgestaltung oder das Warten, bis eine Wiederherstellung abgeschlossen ist.

![Wartungsmodus-Schalter auf dem System-Dashboard](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Wartungsmodus aktivieren

1. Navigieren Sie zu **Management > System-Metriken**
2. Klicken Sie auf **System-Dashboard** in der Symbolleiste
3. Im Panel **Store Status** klicken Sie auf **Wartungsmodus aktivieren**
4. Geben Sie optional einen **Grund** an – dies dient nur Ihrer Referenz und wird Kunden nicht angezeigt (z. B. `Produktkatalog-Update in Bearbeitung`)
5. Bestätigen Sie, indem Sie auf **Aktivieren** klicken

Ihr Verkaufsportal zeigt sofort die Wartungsseite für alle Besucher an. Das Admin-Backend bleibt davon unbeeinflusst, und Sie können weiterhin normal arbeiten.

## Was Kunden sehen

Wenn der Wartungsmodus aktiv ist, wird auf jeder Seite Ihres Verkaufsportals (Shop, Produktseiten, Kasse und Konto-Seiten) eine markenbasierte Wartungshinweis angezeigt. Die Nachricht teilt Kunden mit, dass der Shop vorübergehend nicht verfügbar ist, und ermutigt sie, bald wiederzukommen.

Kunden, die während der Aktivierung des Wartungsmodus in der Mitte einer Sitzung oder eines Kaufvorgangs sind, sehen ebenfalls die Wartungsseite bei ihrem nächsten Anforderung. Keine laufenden Bestellungen gehen verloren – die Daten sind weiterhin vorhanden, wenn Sie den Wartungsmodus deaktivieren.

## Wartungsmodus deaktivieren

1. Navigieren Sie zu **Management > System-Metriken**
2. Klicken Sie auf **System-Dashboard**
3. Im Panel **Store Status** sehen Sie eine Banner, der bestätigt, dass der Wartungsmodus aktiv ist
4. Klicken Sie auf **Wartungsmodus deaktivieren**
5. Bestätigen Sie, wenn Sie aufgefordert werden

Das Verkaufsportal kommt sofort wieder online. Kunden können weiterhin wie gewohnt stöbern und einkaufen.

## Wann aktiviert Spwig den Wartungsmodus automatisch

Bestimmte Systemvorgänge aktivieren den Wartungsmodus automatisch und schalten das Verkaufsportal wieder ein, sobald sie abgeschlossen sind:

- **Plattform-Upgrades** – der Upgrade-Vorgang aktiviert den Wartungsmodus, bevor Änderungen angewendet werden, und deaktiviert ihn, sobald das Upgrade abgeschlossen ist
- **Wiederherstellungsvorgänge** – das Wiederherstellen aus einer Sicherung schaltet das Verkaufsportal während der Wiederherstellung in den Wartungsmodus

Wenn ein automatisierter Vorgang unerwartet endet, kann der Wartungsmodus weiterhin aktiv bleiben. In diesem Fall folgen Sie den oben genannten Schritten, um ihn manuell zu deaktivieren.

## Tipps

- Informieren Sie immer Ihr Team, bevor Sie den Wartungsmodus aktivieren – er beeinflusst jeden Besucher Ihres Verkaufsportals
- Halten Sie Wartungsfenster so kurz wie möglich; selbst ein paar Minuten Offline-Zeit können den Kundenvertrauen beeinträchtigen
- Verwenden Sie das Feld „Grund“, um sich daran zu erinnern, warum der Wartungsmodus aktiviert wurde – es wird im Systemprotokoll angezeigt
- Wenn Sie feststellen, dass der Wartungsmodus aktiv ist, aber Sie ihn nicht selbst aktiviert haben, prüfen Sie das Systemprotokoll auf automatisierte Vorgänge, die ihn ausgelöst haben könnten
- Planen Sie Wartungsfenster während von geringer Besucherzahl (Abends oder frühen Morgenstunden), um den Einfluss auf den Verkauf zu minimieren
