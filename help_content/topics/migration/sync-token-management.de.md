---
title: Sync Token Management
---

Sync tokens sind sichere Anmeldeinformationen, die zwei Spwig-Installationen miteinander kommunizieren lassen. Bevor Sie Einstellungen synchronisieren oder Daten zwischen Stores migrieren können, müssen Sie auf dem **Ziel-**Store einen Token generieren und ihn dem **Quell-**Store bereitstellen.

## Wie Sync Tokens funktionieren

Ein Sync Token ist ein einmal sichtbarer API-Schlüssel, der Anfragen zwischen zwei Spwig-Installationen authentifiziert. Wenn Sie eine Verbindung einrichten, verwendet der entfernte Store diesen Token, um zu beweisen, dass er Berechtigung hat, von Ihrem Store zu lesen oder darauf zu schreiben.

- Tokens werden auf dem Store generiert, der **verbunden werden soll** (das Ziel)
- Jeder Token kann nur einmal angezeigt werden, unmittelbar nach der Generierung
- Tokens können jederzeit widerrufen werden, um den Zugriff sofort zu unterbrechen
- Ein Store kann mehrere aktive Tokens für verschiedene Verbindungen haben

## Token generieren

1. Navigieren Sie zu **Data Migration > Spwig-to-Spwig Sync** in der Admin-Seitenleiste
2. Klicken Sie auf **Manage Tokens** auf dem Sync-Dashboard
3. Geben Sie einen beschreibenden Namen für den Token ein (z. B. "Staging Server" oder "Production Sync")
4. Klicken Sie auf **Generate Token**
5. **Kopieren Sie den Token sofort** -- er wird nicht erneut angezeigt

> **Wichtig:** Speichern Sie den Token sicher. Falls Sie ihn verlieren, müssen Sie einen neuen generieren.

## Token verwenden

Sobald Sie einen Token vom Ziel-Store haben:

1. Gehen Sie zum **Spwig-to-Spwig Sync**-Dashboard auf dem Store, der die Verbindung initiieren wird
2. Starten Sie eine neue **Settings Sync** oder **Full Migration**
3. Im Schritt "Connection", geben Sie die URL des Ziel-Stores ein und fügen Sie den Token ein
4. Klicken Sie auf **Test Connection**, um sicherzustellen, dass es funktioniert
5. Die Verbindung wird für zukünftige Verwendung gespeichert

## Token widerrufen

Wenn ein Token kompromittiert ist oder nicht mehr benötigt wird:

1. Gehen Sie zu **Manage Tokens** auf dem Sync-Dashboard
2. Finden Sie den Token, den Sie widerrufen möchten
3. Klicken Sie auf die Schaltfläche **Revoke**
4. Bestätigen Sie den Widerruf

Der Widerruf eines Tokens wirkt sich sofort aus. Alle aktiven Verbindungen, die diesen Token verwenden, werden nicht mehr funktionieren und müssen mit einem neuen Token neu konfiguriert werden.

## Best Practices

- **Benennen Sie Tokens beschreibend**, damit Sie wissen, zu welcher Verbindung jeder Token gehört
- **Widerrufen Sie ungenutzte Tokens**, um die Sicherheit zu minimieren
- **Generieren Sie separate Tokens** für jeden verbindenden Store, anstatt einen Token über mehrere Stores hinweg zu teilen
- **Erstellen Sie Tokens regelmäßig neu**, als Teil Ihrer Sicherheitsroutine, insbesondere nach Änderungen im Personal
