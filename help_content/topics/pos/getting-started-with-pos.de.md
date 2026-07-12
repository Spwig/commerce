---
title: Einstieg in den POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Spwig POS verwandelt jedes Tablet oder Browserfenster in einen vollwertigen Kassenterminal – verbunden mit Ihrem Produktkatalog, Lagerbestand und Bestellhistorie. Dieser Leitfaden führt Sie von der frischen Installation bis zum ersten Verkauf. Jeder Schritt verlinkt zu einem separaten Thema, falls Sie die vollständigen Details benötigen.

![POS Dashboard](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Schritt 1: POS für einen Store-Location aktivieren

POS-Terminals sind an eine physische Store-Location gebunden. In Spwig sind Store-Location Lager, die als Verkaufsstandorte markiert sind.

1. Navigieren Sie zu **Katalog > Lager** in Ihrer Admin-Linkleiste.
2. Öffnen Sie das Lager, das Sie als Store verwenden möchten, oder erstellen Sie ein neues.
3. Aktivieren Sie das **Verkaufsstandort**-Toggle und geben Sie einen **POS-Anzeigenamen** ein (z. B. "High Street Store"). Dieser Name erscheint auf Rechnungen und im Terminal-Selektor.
4. Speichern Sie das Lager.

Wenn Sie mehrere Stores haben oder sie für regionale Berichte gruppieren möchten, erstellen Sie zunächst eine **Store-Gruppe** unter **POS > Store-Gruppen**, und weisen Sie dann jedes Lager dieser Gruppe zu. Store-Gruppen ermöglichen es Ihnen, eine gemeinsame Währung, Zeitzoneneinstellung und Rechnungsvorlage festzulegen, die alle Standorte in der Gruppe erben.

## Schritt 2: Erstellen oder überprüfen Sie mindestens ein Mitarbeiterkonto mit POS-Zugriff

Ihr Personal meldet sich mit denselben Anmeldeinformationen bei POS an, die sie für die Spwig-Admin-Plattform verwenden. Jedes Mitarbeiterkonto mit **Aktiv**-Status und mindestens der Berechtigung `pos_admin` kann auf POS zugreifen.

Um den Zugriff zu überprüfen oder zu gewähren, gehen Sie zu **Einstellungen > Mitarbeiterverwaltung**, öffnen Sie das Konto des Mitarbeiters und bestätigen Sie, dass der entsprechende POS-Rolle zugewiesen ist. Ein separates POS-Konto ist nicht erforderlich.

## Schritt 3: Registrieren Sie Ihr erstes POS-Terminal

Ein Terminal stellt einen einzelnen Kassentisch oder Gerät dar. Sie registrieren es im Admin-Bereich und verbinden es anschließend mit einem physischen Gerät mithilfe eines Einmal-Paarkodes.

1. Navigieren Sie zu **POS > POS-Terminals** und klicken Sie auf **+ POS-Terminal hinzufügen**.
2. Geben Sie dem Terminal einen Namen (z. B. "Vorderer Kassentisch") und weisen Sie es dem Store-Location zu, den Sie in Schritt 1 aktiviert haben.
3. Speichern Sie das Terminal. Spwig generiert einen **8-stelligen Paarkode** – Sie sehen ihn auf der Detailseite des Terminals.
4. Auf dem Gerät, das Sie als Kassentisch verwenden möchten, öffnen Sie einen Browser und navigieren Sie zu `/pos/`.
5. Geben Sie den Paarkode ein, wenn Sie aufgefordert werden. Das Gerät ist jetzt mit diesem Terminal verbunden.

Der Paarkode ist nur einmal verwendbar. Wenn Sie ein Gerät erneut verbinden müssen, öffnen Sie das Terminal im Admin-Bereich und klicken Sie auf **Paarkode erneuern**.

Für Hardware-Konfigurationsoptionen (Rechnungsdrucker, Barcode-Scanner, Kassenschublade) siehe [POS-Terminal-Setup](pos-terminal-setup).

## Schritt 4: Konfigurieren Sie einen Zahlungsdienstleister

Der Zahlungsdienstleister verbindet Ihre Kartenleser mit einem Zahlungsnetzwerk wie Stripe Terminal oder Square. Verwenden Sie den 5-Schritte-Setup-Assistenten, um Ihre Anmeldeinformationen einzugeben.

1. Navigieren Sie zu **POS > Zahlungsdienstleister** und klicken Sie auf **Dienstleister konfigurieren**.
2. Der Assistent öffnet sich unter `/admin/pos/terminal-provider/wizard/step1/`.

![Zahlungsdienstleister-Assistent](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Wählen Sie Ihren Dienstleister (z. B. **Stripe Terminal**) und folgen Sie den Anweisungen auf dem Bildschirm durch alle fünf Schritte: Dienstleister auswählen → Einrichtungsanweisungen → Anmeldeinformationen eingeben → Verbindung testen → Standort konfigurieren.
4. Ein grüner **Verbunden**-Stempel bestätigt, dass die Integration aktiv ist.

Wenn Sie nur Bargeld und manuelle Karten-Eingabe benötigen, wählen Sie **Manuell** als Anbieter – keine Zugangsdaten erforderlich.

Für detaillierte Felder für Zugangsdaten jedes unterstützten Anbieters siehe [POS-Zahlungsanbieter-Setup](pos-payment-provider-setup).

## Schritt 5: Kartenleser verbinden

Mit einem verbundenen Zahlungsanbieter können Sie einen physischen Kartenleser mithilfe des 3-Schritte-Assistenten einem Ihrer Terminals zuweisen.

1. Navigieren Sie zu **POS > Kartenleser** und klicken Sie auf **Leser hinzufügen**.
2. Der Leser-Assistent startet unter `/admin/pos/reader/wizard/step1/`.
3. Wählen Sie Ihren Anbieter und dann **Neues Gerät registrieren** (geben Sie den Code ein, der auf dem Bildschirm des Lesers angezeigt wird) oder **Bestehendes Gerät entdecken** (Spwig holt bereits registrierte Leser vom Anbieter).
4. Im letzten Schritt weisen Sie den Leser dem Terminal zu, das Sie im Schritt 3 erstellt haben.

Jedes Terminal unterstützt einen zugewiesenen Kartenleser. Sie können Leser jederzeit von der Liste der Kartenleser neu zuweisen.

## Schritt 6: Rechnungsvorlage gestalten (optional für Tag 1)

Spwig erstellt automatisch eine Standardrechnungsvorlage. Sie können sofort mit dem Verkaufen beginnen, ohne sie anzufassen – die Standardvorlage druckt den Namen Ihres Geschäfts, die Adresse, die detaillierten Verkaufspositionen, die Zahlungsmethode und einen Fußbereich mit der Aufschrift „Vielen Dank für Ihren Kauf!“.

Wenn Sie bereit sind, die Vorlage anzupassen, gehen Sie zu **POS > Rechnungsvorlagen**. Zu den Optionen gehören Ihr Logo, Ihre Steuernummer, eine QR-Code-Werbung, eine Rückgabepolitik und die Papierbreite (58 mm oder 80 mm für thermische Drucker). Sie können separate Vorlagen pro Geschäft oder pro Geschäftsguppe erstellen.

## Schritt 7: Ihren ersten Schichtbeginn öffnen

Schichten verfolgen, wer Verkäufe abgewickelt hat und wie viel Bargeld in der Kasse sein sollte. Kassierer öffnen und schließen Schichten direkt am POS.

1. Auf dem verbundenen Gerät navigieren Sie zu `/pos/` und melden Sie sich mit Ihren Mitarbeiterdaten an.
2. Wählen Sie das Terminal und den Geschäftsort aus.
3. Spwig fragt Sie nach der **Anfangskasse** – geben Sie den Bargeldbetrag ein, der bereits in der Kasse ist (geben Sie `0` ein, wenn die Kasse leer ist).
4. Tippen Sie auf **Schicht öffnen**. Die Kasse ist jetzt bereit, um zu verkaufen.

Für eine vollständige Erklärung zu Schichten, Bargeldbewegungen und Abstimmungsberichten siehe [POS-Schichten verwalten](pos-shifts).

## Schritt 8: Ihren ersten Verkauf abschließen

Sobald eine Schicht geöffnet ist, ist der Verkauf einfach:

1. Suchen Sie nach Produkten nach Namen, scannen Sie eine Barcodes oder durchsuchen Sie Kategorien, um Artikel in den Warenkorb zu legen.
2. Wenden Sie bei Bedarf einen Rabatt oder einen Gutscheincode an.
3. Tippen Sie auf **Bezahlen**, um den Zahlungsvorgang zu starten. Wählen Sie die Zahlungsmethode (Bargeld, Karte über Leser oder geteilte Zahlung).
4. Bei Kartenzahlungen fordert der Leser den Kunden auf, seine Karte zu tippen oder einzustecken.
5. Die Rechnung wird automatisch gedruckt (oder eine Option für eine digitale Rechnung wird angezeigt). Die Bestellung wird in Echtzeit in Ihre Bestellhistorie gespeichert.

## Schritt 9: Schicht am Ende des Tages schließen

Das Schließen einer Schicht sperrt die Kasse und erzeugt eine Zusammenfassung der Abstimmung.

1. Im POS-Menü tippen Sie auf **Schicht schließen**.
2. Zählen Sie das Bargeld in der Kasse und geben Sie den Gesamtbetrag ein, wenn Sie aufgefordert werden.
3. Spwig berechnet den erwarteten Bargeldbetrag basierend auf der Anfangskasse, den Bargeldverkäufen und allen Bargeldbewegungen während der Schicht und zeigt Ihnen den Unterschied an.
4. Bestätigen Sie, um die Schicht zu schließen. Der Schichtbericht wird gespeichert und ist unter **POS > Schichten** in Ihrem Admin-Bereich sichtbar.

Notieren Sie alle Bargeldbewegungen, die während des Tages aus der Kasse entfernt oder hinzugefügt wurden, als **Bargeldbewegungen** (über das Schichtmenü) anstatt den Schließungsbetrag anzupassen – dies hält Ihre Abstimmung präzise.

## Tipps

- Führen Sie Schritte 1 bis 5 vor Ihrem ersten Tag des Handels durch.

Schritte 6 bis 9 können am Tag des Handels durchgeführt werden.
- Verwenden Sie ein starkes, aber merkbares Mitarbeiterpasswort – Mitarbeiter geben ihre Zugangsdaten direkt an der Kasse ein, daher verlangsamen übermäßig komplexe Passwörter sie.
- Wenn der Kartenleser nicht online erscheint, klicken Sie auf **Leser synchronisieren** auf der Seite Kartenleser, um den neuesten Status von Ihrem Anbieter abzurufen.
- Testen Sie den gesamten Ablauf (Schicht öffnen → Verkauf → Rechnung → Schicht schließen) mit einer Testtransaktion von 0,01 $, bevor Sie in einer beschäftigten Handelsphase sind.
- Der POS funktioniert offline für einfache Bargeldverkäufe.

Karten-Endgerätezahlungen benötigen eine Internetverbindung zur Autorisierung.
- Sie können an einem Store-Standort mehrere Endgeräte haben — fügen Sie in der Verwaltung eine neue Endgeräte-Bezeichnung hinzu und verknüpfen Sie sie mit einem anderen Gerät.