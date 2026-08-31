---
title: Zielgruppen
---

Ein **Segment** ist eine gespeicherte Zielgruppe, die Sie auf eine Kampagne, einen Weg oder einen A/B-Test ausrichten können – die eigene Segmentliste von Campaign Studio nennt sie "Zielgruppen", und dieser Leitfaden verwendet beide Begriffe für dasselbe. Jedes Segment ist entweder **dynamisch**, d. h. durch Regeln definiert, die Spwig jedes Mal neu berechnet, wenn es verwendet wird, oder **statistisch**, eine explizite Liste von Abonnenten, die Sie manuell auswählen.

Dieser Leitfaden beschreibt das Erstellen der Regeln für ein dynamisches Segment – einschließlich neuerer Felder, die Ihre eigene Kundenwertebucket, Treueprogramm und Partner abzielen – und die Schaltfläche **Zielgruppen hinzufügen** mit einem Klick, die eine Reihe von vorgefertigten Segmenten aus dem Datenbestand Ihres Stores erstellt.

## Dynamische vs. statische Segmente

| Art | Funktionsweise | Empfohlen für |
|---|---|---|
| **Dynamisch (Regeln)** | Sie definieren Bedingungen – z. B. "Gesamtausgaben betragen mindestens 500 $". Spwig berechnet erneut, wer übereinstimmt, jedes Mal, wenn das Segment verwendet wird, sodass sich die Mitgliedschaft automatisch ändert, je nachdem, wie sich Ihre Abonnenten verändern. | Dauerhafte Zielgruppen, die stets aktuell sein sollten, wie "VIP-Kunden" oder "hat in den letzten 90 Tagen keinen Kauf getätigt".
| **Statisch (festgelegte Liste)** | Eine explizte Liste von Abonnenten, die Sie manuell hinzufügen oder entfernen. Die Mitgliedschaft ändert sich nie, es sei denn, Sie ändern sie. | Eine Einzelveranstaltung – alle aus einer bestimmten Veranstaltung oder eine manuell ausgewählte Gruppe für einen Einzelversand.

Wählen Sie bei der Erstellung eines Segments die **Art** aus. Der Rest dieses Leitfadens befasst sich mit dynamischen Segmenten – statische sind einfach nur eine Mitgliederliste ohne Konfigurationsregeln.

## Erstellen eines dynamischen Segments

Öffnen Sie **Campaign Studio > Segmente**, und klicken Sie auf **+ Neues Segment** (oder öffnen Sie ein vorhandenes dynamisches Segment), um den **Zielgruppen-Regel-Editor** zu erreichen. Klicken Sie auf **+ Bedingung hinzufügen**, um eine Regel hinzuzufügen, wählen Sie, was geprüft werden soll, und wie, und legen Sie fest, ob ein Abonnent **alle** oder **eine** Ihrer Bedingungen erfüllen muss. Ein Echtzeit-Zähler in der rechten oberen Ecke – z. B. "8 übereinstimmende Abonnenten" – aktualisiert sich einen Moment nach jeder Änderung, sodass Sie genau sehen können, wer sich vor dem Speichern qualifiziert.

![Der Audience-Regel-Editor mit dem Kunden-Segment, Treue-Stufe, Lebenszeit-Wert und Partner-Bedingungen, und einem Echtzeit-Zähler für übereinstimmende Abonnenten](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Eine Bedingung mit einer festen **ist wahr**-Prüfung – **Hat bestellt**, **In Marketing eingewilligt**, **Treue-Mitglied**, **Partner** – benötigt nichts weiter als die Auswahl des Feldes selbst; es gibt keinen Operator oder Wert, den Sie einstellen müssen.

## Was Sie ansprechen können

| Feld | Was prüft es |
|---|---|
| **Gesamtausgaben** | Gesamtausgaben der Bestellungen. |
| **Anzahl der Bestellungen** | Anzahl der abgeschlossenen Bestellungen. |
| **Lebenszeit-Wert** | Der berechnete Lebenszeit-Wert des Kunden. |
| **Durchschnittswert pro Bestellung** | Durchschnittlicher Betrag pro abgeschlossene Bestellung. |
| **Tage seit letzter Bestellung** | Wie lange seit der letzten Bestellung des Kunden – Zielgruppe für Wiedererlangung mit 90+ Tagen. |
| **Hat bestellt** | Ob der Kunde mindestens eine abgeschlossene Bestellung hat. |
| **In Marketing eingewilligt** | Ob der Abonnent der E-Mail-Marketing-Zielgruppe zugestimmt hat. |
| **Sprache** | Die gespeicherte Sprache des Abonnenten. |
| **Quelle** | Wie der Abonnent beigetreten ist – Storefront-Anmeldung, Import, Bestellung, manuell hinzugefügt oder API. |
| **Beigetreten nach** | Abonnenten, die am oder nach einem ausgewählten Datum beigetreten sind. |
| **Hat Tag** | Ob der Abonnent einen [Tag](/help/subscriber-tags) trägt, den Sie erstellt haben. |
| **Kunden-Segment** | Ob der Kunde zu einem der eigenen Namen [Kunden-Segmente](/help/customer-segments) Ihres Stores gehört – Gastkunde, Neukunde, Regelmäßiger Kunde, Häufiger Käufer, Hochwertiger Kunde, VIP-Kunde, Schnäppchenjäger, Risikokunde oder Inaktiver Kunde. |
| **Treue-Mitglied** | Ob der Kunde Mitglied eines aktiven Treueprogramms ist. |
| **Treuepunkte** | Das aktuelle verfügbare Punktekonto des Mitglieds. |
| **Treue-Stufe** | Welche Treue-Stufe das Mitglied derzeit hat. |
| **Partner** | Ob der Kunde einer Ihrer aktiven Partner ist.

**Kundensegment**, die beiden **Loyalitäts**-Werte, **Loyalitätstufe** und **Affiliate** sind neuere Ergänzungen und erscheinen erst im Bedingungs-Selector, sobald Ihr Geschäft tatsächlich über diese Art von Daten verfügt: Die Loyalitätsfelder erscheinen, sobald Ihr Loyalitätsprogramm Mitglieder und mindestens eine aktive Stufe hat, **Affiliate** erscheint, sobald Sie mindestens ein Affiliate haben, und **Kundensegment** erscheint, sobald Sie mindestens ein aktives Kundensegment konfiguriert haben.

Sie werden bei einem frischen Geschäft keine Option sehen, die niemanden treffen könnte.

Eine aktuelle Einschränkung, die man kennen sollte: Bei jeder Bedingung mit einer Dropdown-Auswahl — **Sprache**, **Quelle**, **Hat Tag**, **Kundensegment**, **Loyalitätstufe** — ermöglicht der **ist einer von**-Operator weiterhin nur die Auswahl eines Werts pro Zeit. Wenn Sie mehrere abgleichen möchten (z. B. Kunden, die entweder in Ihrem VIP- oder Hochwert-Segment sind), fügen Sie pro Wert eine Bedingung hinzu und setzen Sie **Match** auf **any**.

## Startsegnungen hinzufügen

Es ist mühsam, für jedes offensichtliche Publikum eine Regel von Grund auf zu erstellen — Ihre VIPs, Ihre Loyalitätsmitglieder, alle, die stillgelegt haben —, wenn Spwig bereits sehen kann, wer qualifiziert ist. Klicken Sie auf der **Segments**-Liste auf **Startsegnungen hinzufügen**, und Spwig erstellt eine Reihe von fertigen, editierbaren dynamischen Segmente aus dem, was Ihr Geschäft bereits an Kundendaten, Loyalitäts- und Affiliate-Daten hat.

![Die Segmente-Liste mit den Schaltflächen **Neues Segment** und **Startsegnungen hinzufügen**](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Starter | Ziele | Benötigungen |
|---|---|---|
| **VIP-Kunden** | Ihr VIP-Kundensegment | Ein aktives VIP-Kundensegment |
| **Hochwertige Kunden** | Ihre VIP- und Hochwert-Kundensegmente | Ein aktives VIP- oder Hochwert-Kundensegment |
| **Wiederholungskäufer** | Ihre häufigen Käufer- und Regelmäßige-Kundensegmente | Ein aktives häufiges Käufer- oder Regelmäßiges-Kunden-Segment |
| **Neue Kunden** | Ihr Neukunden-Segment | Ein aktives Neukunden-Segment |
| **Eingeschlafene Kunden** | Kunden, die bereits bestellt haben, aber nicht in den letzten 90 Tagen | Jede Kundenbestellhistorie |
| **Loyalitätsmitglieder** | Alle, die in Ihrem Loyalitätsprogramm aktiv sind | Ein aktives Loyalitätsprogramm mit Mitgliedern |
| **Top-Loyalitätstufe** | Mitglieder in Ihrer höchstrangigen Loyalitätstufe | Mindestens eine aktive Loyalitätstufe |
| **Affiliate** | Ihre aktiven Affiliate-Partner | Mindestens ein Affiliate |

Spwig erstellt nur die Starter, für die es tatsächlich Daten gibt — ein Geschäft ohne Loyalitätsprogramm erhält einfach kein **Loyalitätsmitglied**, sondern kein leeres, das niemanden treffen könnte. Spwig bestätigt genau, was es hinzugefügt hat, z. B. "Hinzugefügt 7 Startsegnungen: Hochwertige Kunden, Wiederholungskäufer, Neue Kunden, Eingeschlafene Kunden, Loyalitätsmitglieder, Top-Loyalitätstufe, Affiliate."

![Erfolgsmeldung, die bestätigt, welche Startsegnungen gerade hinzugefügt wurden](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

Es ist sicher, auf **Startsegnungen hinzufügen** mehr als einmal zu klicken. Spwig erstellt niemals eine Duplikat-Startsegnung, die bereits existiert, sodass das Klicken erneut nach dem Einrichten (z. B. Ihres Loyalitätsprogramms zum ersten Mal) nur das hinzufügt, was neu verfügbar ist — wenn alles bereits eingerichtet ist, sagt es einfach so.

![Info-Meldung, die angezeigt wird, wenn jede Startsegnung bereits vorhanden ist](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Wenn Sie eine Startsegnung löschen, die Sie nicht möchten, bringt das erneute Klicken auf **Startsegnungen hinzufügen** sie nicht zurück — Spwig behandelt sie als ein Segment, das Sie absichtlich gelöscht haben, nicht eines, das erneut erstellt werden soll.

Sobald ein Starter vorhanden ist, ist es ein gewöhnliches dynamisches Segment: Öffnen Sie es aus der Liste, um seine Regeln zu überprüfen oder zu bearbeiten, es zu benennen oder zu löschen, genau so, wie Sie es mit jedem Segment tun würden, das Sie selbst erstellt haben.

## Wer diese Publikum tatsächlich erreicht

Die oben genannten Kunden-, Treue- und Affiliate-Bedingungen passen sich nur auf Abonnenten, deren E-Mail mit einem Kundenkonto verknüpft ist - eine anonyme Newsletter-Anmeldung passt nicht auf eine **Treue-Mitgliedschaft** oder **VIP**-Bedingung, selbst wenn dies korrekt ist, da Spwig kein Bestell- oder Treue-Verlauf hat, um sie darauf zu prüfen.

Wenn viele Ihrer Kunden Konten haben, aber noch nicht abonniert haben, sollten Sie denjenigen fragen, der Ihre Spwig-Installation verwaltet, um eine Abonnentensynchronisierung durchzuführen - sie erstellt für jedes bestehende Kundenkonto in einem Schritt einen Abonnenteneintrag, damit diese Zielgruppen echte Personen haben, mit denen sie übereinstimmen können.

Unabhängig davon, wie viele Abonnenten eine Zielgruppe zählt, beschreibt diese Zahl, wer *empfangen* könnte, nicht, wer es auch tatsächlich tut. Jeder Versand prüft zuerst die eigene Einwilligung in den Werbeempfang eines Abonnenten, sodass eine Zielgruppe niemals eine Möglichkeit ist, dies zu umgehen.

## Tipps

- Beginnen Sie mit einer Startzielgruppe und passen Sie sie an, anstatt die gleiche Regel von Hand zu erstellen - sobald eine Startzielgruppe erstellt wurde, ist sie mit jeder von Ihnen selbst erstellten Zielgruppe identisch.
- Boolesche Bedingungen wie **Treue-Mitglied**, **Affiliate** und **Hat bestellt** benötigen keinen Operator oder Wert - einfach das Hinzufügen der Bedingung und Sie sind fertig.
- Kombinieren Sie die neueren Felder mit den ursprünglichen für eine präzisere Zielgruppenansprache, z. B. **Treue-Mitglied** plus **Werbung zugestimmt**, anstatt sich allein auf eine Bedingung zu verlassen.
- Wenn die Regeln einer Zielgruppe etwas beziehen, das seither gelöscht wurde - eine gelöschte Kundenzielgruppe, ein leeres Etikett usw. - behandelt Spwig dies als Übereinstimmung mit niemandem, anstatt sich auf Ihre gesamte Abonnentenliste zu verlassen. Fehlerhafte Zielgruppen senden weniger; es wird niemand versehentlich versandt.
- Wenn die Mitgliederanzahl einer Zielgruppe veraltet erscheint, öffnen Sie sie erneut und speichern Sie sie, oder verwenden Sie die Aktion **Mitgliederanzahl neu berechnen** aus der Liste der Zielgruppen, um sie sofort neu zu berechnen.
- Beobachten Sie den Echtzeit-„Abonnenten-Übereinstimmungszähler“, während Sie eine Regel erstellen - das ist der schnellste Weg, um eine Bedingung zu erkennen, die enger (oder breiter) ist, als Sie es beabsichtigt haben, bevor Sie speichern.