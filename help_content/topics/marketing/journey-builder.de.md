---
title: Journey Builder
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

Der **Journey Builder** ist die visuelle Drag-and-Drop-Oberfläche, auf der Sie gestalten, was eine [Journey](/help/triggered-journeys) tatsächlich tut – welche E-Mails versendet werden, wie lange zwischen ihnen gewartet wird und ob verschiedene Abonnenten unterschiedlichen Pfaden folgen sollen. Anstatt ein Formular auszufüllen, erstellen Sie den Ablauf als Flussdiagramm: verbundene Kästen auf einer Leinwand, die Sie auf einen Blick neu anordnen, verzweigen und vorschauen können.

## Den Builder öffnen

Jede Journey hat ihre eigene Builder-Leinwand. Sie können sie auf zwei Wegen erreichen:

- Erstellen einer neuen Journey – füllen Sie auf der Einstellungsseite **Name**, **Trigger** und Zielgruppe aus und klicken Sie auf **Speichern** – Sie gelangen direkt in den Builder und können sofort mit dem Design beginnen.
- Öffnen der Einstellungsseite einer bestehenden Journey und Klicken auf **Journey gestalten** oben.

Der Builder ist ein Vollbild-Arbeitsbereich mit drei Bereichen: eine **Palette** mit Schritttypen links, die **Leinwand** in der Mitte und ein **Schritt-Einstellungen**-Panel rechts, das erscheint, wenn Sie etwas auswählen.

![Die Journey Builder-Leinwand zeigt eine Willkommensserie mit einer Ja/Nein-Verzweigung](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

Oben auf der Leinwand wiederholt der Header den **Trigger** und die **Zielgruppe** der Journey (oder "Alle Abonnenten", wenn kein Segment festgelegt ist), damit Sie immer wissen, für wen Sie gestalten, ohne den Builder zu verlassen. Verwenden Sie die **Zurück**-Schaltfläche, um zur Einstellungsseite der Journey zurückzukehren.

## Die Schritttypen

Ziehen Sie einen Schritt aus der linken Palette auf die Leinwand oder klicken Sie auf ein Palette-Element, um es automatisch abzulegen. Vier Schritttypen sind verfügbar:

| Schritt | Was er tut |
|------|--------------|
| **E-Mail senden** | Sendet eine Ihrer Kampagnen an den Abonnenten. |
| **Warten** | Pausiert für eine festgelegte Anzahl von Stunden oder Tagen, bevor es weitergeht. |
| **Verzweigung** | Teilt den Pfad in zwei – **Ja** oder **Nein** – basierend darauf, ob der Abonnent zu einem von Ihnen gewählten Segment gehört. |
| **Beenden** | Beendet die Journey für den Abonnenten. |

Jede Journey beginnt mit einem einzelnen **Eingang**-Schritt, der automatisch erstellt wird, wenn Sie den Builder zum ersten Mal öffnen. Er zeigt den Trigger der Journey an und kann nicht gelöscht werden – er ist einfach der Punkt, an dem Abonnenten in den Ablauf eintreten.

## Schritte verbinden

Jeder Schritt hat einen kleinen kreisförmigen **Port**: einen oben (Eingang) und einen oder mehrere unten (Ausgang). Um zwei Schritte zu verbinden, ziehen Sie vom unteren Port eines Schritts zum oberen Port eines anderen Schritts – eine geschwungene Linie erscheint, die sie verbindet.

Ein **Verzweigung**-Schritt hat zwei Ausgangs-Ports statt eines: ein grünes **Ja** und ein rotes **Nein**. Verbinden Sie jeden mit dem Ort, an den dieser Pfad führen soll – sie können später am selben Schritt wieder zusammenlaufen (wie im obigen Beispiel, wo beide Pfade zum selben **Beenden**-Schritt zurückführen) oder völlig getrennte Wege gehen.

Um das Layout neu anzuordnen, ziehen Sie einen Schritt an seinem Körper, um ihn zu verschieben – verbundene Linien folgen automatisch. Ziehen Sie einen leeren Teil des Leinwandhintergrunds, um sich zu bewegen, und verwenden Sie Ihr Mausrad, um herein- oder herauszuzoomen. Wenn Sie den Ablauf aus den Augen verlieren, klicken Sie auf **Anpassen** in der Werkzeugleiste, um alles zentriert und passend auf dem Bildschirm anzuzeigen.

## Einen Schritt konfigurieren

Klicken Sie auf einen beliebigen Schritt, um seine Einstellungen im rechten Panel zu öffnen:


{
  "Step": "Einstellung",
  "------": "---------",
  "**Send email**": "Wählen Sie die **Zu sendende E-Mail** aus einer Liste Ihrer Kampagnen aus.",
  "**Wait**": "Geben Sie **Wartezeit** an — eine Zahl plus **Stunden** oder **Tage**.",
  "**Branch**": "Wählen Sie **Wenn Abonnent in Segment ist** — das Segment, das Ja vs. Nein entscheidet.",
  "**Exit**": "Keine Einstellungen — es handelt sich einfach um einen Endpunkt."
}

![Der rechte Bereich zur Konfiguration eines Verzweigungsschritts mit dem Canvas, der dahinter abgedunkelt ist](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Änderungen werden automatisch gespeichert, sobald Sie einen Wert auswählen — es gibt auf dem Canvas keinen separaten **Speichern**-Button. Jeder Schritt außer **Eintrag** hat einen **Löschen-Button** am unteren Rand seines Einstellungspanels.

Die E-Mails, die Sie für **E-Mail senden**-Schritte auswählen, sind gewöhnliche Kampagnen, die Sie in der regulären visuellen Builder-Oberfläche von Campaign Studio entwerfen — Betreffzeile, Inhaltsschichten, alles. Lassen Sie sie als **Entwurf** und wählen Sie sie einfach aus der Dropdown-Liste aus; der Weg sendet sie für Sie, Sie klicken nie auf **Senden**.

## Von einem Vorlage starten

Es ist nicht immer notwendig, einen Fluss von einem leeren Canvas aus zu bauen — klicken Sie auf **Vorlagen** in der Symbolleiste (oder **Vorlagen durchsuchen** auf einem leeren Canvas), um einen Picker mit acht vorgefertigten Startvorlagen zu öffnen:

| Vorlage | Was es baut |
|----------|-----------------|
| **Willkommensreihe** | Begrüßen Sie neue Abonnenten, teilen Sie mit, was Sie sind, und geben Sie einen ersten Bestellhinweis.
| **Erster Kauf Onboarding** | Verwandeln Sie einen Neuling in einen Wiederholungs-Kunden mit einer sanften Onboarding-Sequenz.
| **Nach Bestellung und Bewertung** | Danken Sie nach jeder Bestellung, und bitten Sie um eine Bewertung, sobald sie eingetroffen ist.
| **VIP vs. Standardangebot** | Verzweigen Sie sich nach Ihrem VIP-Segment, um dem jeweiligen Team das richtige Folgeangebot zu senden.
| **Abandoned Cart Recovery** | Erinnern Sie einen Shop-Besucher, der Artikel zurückgelassen hat, und geben Sie einen Follow-up-Hinweis am nächsten Tag.
| **Win-back lapsed customers** | Reaktivieren Sie einen Kunden, der lange nicht gekauft hat, mit einem Grund, zurückzukommen.
| **Post-Delivery Bewertungsanfrage** | Bitte um eine Bewertung ein paar Tage nachdem eine Bestellung als **Geliefert** markiert wurde.
| **Back-in-stock Alert** | Teilen Sie einem wartenden Kunden mit, sobald ein Produkt, das er wollte, erneut verfügbar ist.

Jede Vorlage ist bereits mit dem passenden Auslöser verdrahtet — zum Beispiel erwartet das Anwenden von **Win-back lapsed customers** auf einen neuen Weg, dass der **Auslöser** des Weges **Kunde hat aufgehört (Win-back)** ist. Siehe [Ausgelöste Wege](/help/triggered-journeys), um zu sehen, was jeden dieser Auslöseereignisse auslöst und wie die auf Erholung ausgerichteten Arten funktionieren (idle windows, Gast-Kauf, einmal pro Bestellung Bewertungsanfragen und wie ein Back-in-stock-Weg sich von dem einfachen Einzelalert absetzt).

![Der Vorlagen-Picker zeigt die vorgefertigten Start-Wege an](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Das Anwenden einer Vorlage ersetzt den aktuellen Fluss auf dem Canvas, also verwenden Sie es am Anfang des Entwurfs eines Weges, nicht in der Mitte. Spwig verknüpft jeden Schritt mit einer echten E-Mail oder einem Segment, wo der Name mit etwas übereinstimmt, was Sie bereits haben; wo es keine Übereinstimmung gibt, meldet der Header, wie viele Schritte immer noch eine E-Mail oder ein Segment auswählen müssen, damit Sie genau wissen, was Sie beenden müssen, bevor Sie live gehen.

## Wege teilen

Zwei Symbolleisten-Buttons ermöglichen es Ihnen, den Entwurf eines Weges zwischen Schritten oder zwischen Stores zu verschieben:

- **Exportieren** lädt den Weg als `.journey.json`-Datei herunter — eine tragbare Beschreibung der Flussform (seine Schritte, Wartezeiten, Verzweigungen und Ja/Nein-Pfade) plus die *Namen* der E-Mails und Segmente, die jeder Schritt verwendet. Es enthält nicht die E-Mail-Entwürfe selbst oder irgendeine Abonnentendaten.
- **Importieren** lädt eine `.journey.json`-Datei in den aktuellen Weg, wodurch das auf dem Canvas vorhandene ersetzt wird.

Dies ist nützlich, um einen Fluss zu sichern, den Sie stolz sind, eine bewährte Willkommensreihe an einen anderen Spwig-Store zu übergeben, oder einen Weg nach dem Klonen Ihres Stores in eine neue Installation neu zu erstellen.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Im Gegensatz zu Vorlagen verknüpft Spwig E-Mails und Segmente anhand des Namens, sofern eine Übereinstimmung auf dem Ziel-Store besteht, und markiert alles, was nicht übereinstimmen könnte, damit Sie die Einrichtung abschließen können.

## Aktivieren Sie Ihre Reise

Wenn der Fluss bereit ist, verwenden Sie den Status-Steuerungspunkt oben rechts im Builder. Ein Rechteck zeigt den aktuellen Status der Reise an – **Entwurf**, **Aktiv** oder **Pause** – neben einem **Aktivieren**-Knopf.

Klicken Sie auf **Aktivieren**, **prüft zuerst den Fluss**. Wenn etwas den Fluss blockieren würde, wird die Aktivierung blockiert und eine Banner-Liste listet die Probleme auf – z. B. ein **E-Mail senden**-Schritt mit keiner ausgewählten E-Mail, ein **Zweig**, bei dem kein Segment oder kein Ja/Nein-Pfad vorhanden ist, eine E-Mail oder ein Segment, das danach gelöscht wurde, oder eine Schleife, die ewig läuft. Jedes Problem ist klickbar: Wenn Sie es auswählen, springt es zum betreffenden Schritt, der bis zu Ihrer Behebung in Rot umrandet ist. Warnungen (z. B. ein nicht erreichbarer Schritt oder ein **Warte**-Schritt ohne festgelegte Verzögerung) werden ebenfalls gelistet, blockieren die Aktivierung aber nicht.

![Aktivierung blockiert, mit dem Problem in einer Leiste und dem betreffenden Schritt in rot umrandet](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Sobald der Fluss funktioniert, wechselt das Rechteck zu **Aktiv** und die Reise beginnt, Abonnenten zu registrieren, sobald ihr Auslöser feuert. Der Knopf wird zu **Pause**, der neue Registrierungen stoppt – Abonnenten, die bereits auf halbem Weg sind, erhalten ihre verbleibenden Schritte weiterhin. Siehe [Ausgelöste Reisen](/help/triggered-journeys), wie sich Registrierung, Wartezeiten und Status gegenseitig beeinflussen.

## Wer ist in der Reise?

Sobald die Reise aktiv ist, zeigt jeder Schritt ein kleines **Zählungs-Symbol** in seiner Ecke an: die Anzahl der Abonnenten, die sich gerade an diesem Schritt befinden. Es ist eine schnelle Möglichkeit zu sehen, wo die Leute fließen und wo sie sich ansammeln – eine große Zahl bei einem **Warte**-Schritt ist zu erwarten, während eine Ansammlung kurz vor einer bestimmten E-Mail möglicherweise einen Blick wert ist. Die Zahlen aktualisieren sich, sobald Sie zum Builder-Reiter zurückkehren.

![Die Leinwand mit live Zählungs-Symbolen auf den Schritten und dem Aktivieren-Knopf in der Symbolleiste](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Tipps

- Entwerfen Sie den Fluss, während er noch **Entwurf** ist – niemand wird registriert, bis Sie **Aktivieren**. Die Aktivierung vom Builder aus führt zuerst eine schnelle Prüfung durch und lässt keinen defekten Fluss live, sodass es kein Risiko für eine halbfertige Reise gibt, die Abonnenten registriert.
- Starten Sie von einem **Vorlage**-Schritt aus, auch wenn Sie beabsichtigen, sie stark anzupassen – es ist schneller, eine vorhandene Reise zu bearbeiten, als eine Reise Schritt für Schritt zu bauen, und sie zeigt das Verzweigungsmuster, falls Sie es noch nicht verwendet haben.
- Nachdem Sie eine Vorlage angewandt oder eine Datei importiert haben, prüfen Sie den Header auf eine Notiz zu nicht übereinstimmenden Schritten und füllen Sie alle **E-Mail senden**- oder **Verzweigung**-Schritte aus, die nicht übereinstimmen, bevor Sie aktivieren.
- Klicken Sie auf **Anpassen**, sobald ein Fluss breit wird (vor allem Verzweigungen) – es ist der schnellste Weg, das gesamte Aussehen erneut zu sehen, nachdem Sie vergrößert oder verschoben haben.
- Halten Sie Schrittbezeichnungen leicht zu scannen, indem Sie jeden **Warte**-Schritt unmittelbar vor der E-Mail platzieren, die er verzögert, anstatt mehrere Warte-Schritte zusammenzubündeln.
- **Exportieren** Sie eine funktionierende Reise, bevor Sie größere Änderungen daran vornehmen – es ist eine schnelle Möglichkeit, eine Rückfallversion zu behalten, die Sie erneut importieren können, falls Sie das Ergebnis nicht mögen.