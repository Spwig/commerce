---
title: Parken und Fortsetzen von POS-Transaktionen
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Parked cart list view (may be empty on fresh install — capture anyway)
  save-to: core/static/core/admin/img/help/pos/
-->

Parkierte Warenkörbe ermöglichen es Ihren Kassierern, eine Transaktion zu pausieren und sofort mit dem nächsten Kunden zu beginnen – ohne ein einziges Produkt oder Rabatt zu verlieren. Wenn Sie bereit sind, wird der ursprüngliche Warenkorb exakt so wie zuvor wiederhergestellt und der Verkauf kann von dem Punkt fortgesetzt werden, an dem er unterbrochen wurde.

## Was das Parken eines Warenkorbs bewirkt

Wenn ein Kassierer auf **Park** im POS-Registrierkasse tippt, speichert Spwig einen vollständigen Snapshot des aktuellen Warenkorbs auf dem Server. Das Registrierkasse wird geleert, damit eine neue Transaktion sofort begonnen werden kann. Der geparkte Warenkorb wird gespeichert und mit dem Terminal verknüpft, auf dem er erstellt wurde.

Nichts geht verloren. Der geparkte Warenkorb bewahrt:

- Jedes Produkt und dessen Menge
- Jeden Kunden, der dem Verkauf zugeordnet war
- Alle manuell auf den Warenkorb oder einzelne Produkte angewendeten Rabatte

Der geparkte Warenkorb ist auf demselben Terminal bis zu **24 Stunden** verfügbar. Danach entfernt Spwig ihn automatisch. Warenkörbe, die bereits wiederhergestellt wurden, werden sofort nach der Wiederherstellung entfernt und zählen nicht zur 24-Stunden-Fenster.

## Wie man eine Transaktion parkt

Sie müssen mindestens ein Produkt im Warenkorb haben, bevor Sie ihn parken können. Ein leerer Warenkorb kann nicht geparkt werden.

1. Während eines laufenden Verkaufs tippen Sie auf die Schaltfläche **Park** auf der POS-Registrierkasse.
2. Spwig speichert den Warenkorb und leert das Registrierkasse. Sie sehen eine Bestätigung und die Anzahl der geparkten Warenkörbe im Bereich **geparkte Warenkörbe** wird aktualisiert.
3. Starten Sie die Transaktion des nächsten Kunden auf dem nun leeren Registrierkasse.

Wenn der Kunde bereits vor dem Parken dem Verkauf zugeordnet war, wird sein Name in der Liste der geparkten Warenkörbe angezeigt, um eine einfache Identifizierung zu ermöglichen.

## Wie man eine geparkte Transaktion fortsetzt

1. Tippen Sie auf den Bereich **geparkte Warenkörbe** oder das Symbol auf der POS-Registrierkasse. Sie sehen eine Liste aller derzeit geparkten Warenkörbe auf diesem Terminal, die den Kundenname (falls vorhanden), die Anzahl der Artikel, den Gesamtbetrag, den Kassierer, der den Warenkorb geparkt hat, und die Zeit, zu der der Warenkorb geparkt wurde, anzeigt.
2. Tippen Sie auf den Warenkorb, den Sie fortsetzen möchten.
3. Wenn Ihr aktuelles Registrierkasse Artikel enthält, wird das Registrierkasse diese Artikel löschen, bevor der geparkte Warenkorb wiederhergestellt wird. Stellen Sie sicher, dass Sie die aktuelle Transaktion entweder abgeschlossen oder geparkt haben, bevor Sie eine andere fortsetzen.
4. Die Artikel des geparkten Warenkorbs, die Kundenbeziehung und die manuellen Rabatte werden alle wiederhergestellt. Der Verkauf wird wie gewohnt fortgesetzt.

## Sichtbarkeit von geparkten Warenkörben

Geparkte Warenkörbe sind **mit dem Terminal verknüpft**, auf dem sie erstellt wurden. Jeder Kassierer, der sich auf demselben Terminal anmeldet, kann alle geparkten Warenkörbe auf diesem Terminal sehen und fortsetzen – es gibt keine Einschränkung pro Kassierer, wer einen geparkten Warenkorb abholen kann.

Warenkörbe, die auf einem anderen Terminal geparkt wurden, selbst im selben Geschäftstandort, sind auf Ihrem aktuellen Terminal nicht sichtbar.

## Löschen eines geparkten Warenkorbs über die POS

Ein Kassierer kann einen geparkten Warenkorb direkt aus der Liste der geparkten Warenkörbe auf dem Terminal löschen – tippen Sie auf den Warenkorb und verwenden Sie die Löschen- oder Entsorgen-Option. Gelöschte geparkte Warenkörbe werden dauerhaft entfernt und können nicht wiederhergestellt werden.

## Automatische Ablaufzeit und Bereinigung

Jeder geparkte Warenkorb läuft **24 Stunden nach dem Parken** ab. Spwig führt eine Hintergrundaufgabe durch, die abgelaufene Warenkörbe entfernt, die nie wiederhergestellt wurden. Es ist nichts, das Sie tun müssen – die Bereinigung erfolgt automatisch.

Wenn Sie geparkte Warenkörbe vor dem Ablauf der 24-Stunden-Fenster löschen müssen, kann ein Kassierer sie nacheinander aus der Liste der geparkten Warenkörbe auf dem Terminal löschen.

## Schichtwechsel und geparkte Warenkörbe

Es besteht keine feste Verknüpfung zwischen einem geparkten Warenkorb und der Schicht, die aktiv war, als er geparkt wurde. Das Schließen einer Schicht führt **nicht** automatisch zur Löschung oder zum Abbrechen von geparkten Warenkörben auf diesem Terminal. Geparkte Warenkörbe überstehen Schichtwechsel und bleiben für die volle 24-Stunden-Fenster verfügbar.

Das bedeutet:

- Ein Warenkorb, der am Ende einer Morgen-Schicht geparkt wurde, kann von einem Kassierer in einer späteren Schicht fortgesetzt werden.
- Wenn Sie nicht möchten, dass geparkte Warenkörbe zwischen Schichten übertragen werden, bitten Sie die Kassierer, die Liste der geparkten Warenkörbe vor dem Schließen ihrer Schicht zu löschen.

## Tipps

Erhalten Sie alle Markdown-Formatierung, Bildpfade, Codeblöcke und technischen Begriffe beibehalten.

- Halte einen Warenkorb an, sobald ein Kunde sagt: „Ich muss nur noch eine Sache holen“. Das ist schneller, als ihn zu bitten, erneut in die Schlange zu warten oder die Artikel manuell hinzuzufügen.
- Wenn die Liste der angehaltenen Warenkörbe sehr lang wird, prüfe, ob ein früherer Kassier Transaktionen am Ende seiner Schicht nicht abgeschlossen hat, und entferne alle veralteten Warenkörbe.
- Verknüpfe den Kunden mit dem Verkauf, sobald es möglich ist – sein Name erscheint in der Liste, was es viel einfacher macht, den richtigen Warenkorb zu finden, wenn er zurückkehrt.
- Angehaltene Warenkörbe verfallen nach 24 Stunden, daher eignen sie sich nicht zum Speichern von Transaktionen über mehrere Geschäftstage hinweg.
- Beachte, dass das Wiederherstellen eines angehaltenen Warenkorbs den aktuellen Inhalt des Kassenregisters löscht.

Schließe den aktiven Vorgang ab oder halte ihn an, bevor du einen anderen angehaltenen Warenkorb übernimmst.