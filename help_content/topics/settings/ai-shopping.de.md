---
title: KI-Einkauf
---

KI-Einkauf ermöglicht es KI-Einkaufsassistenzsystemen, Ihre Produkte zu finden und, wenn Sie dies erlauben, im Namen eines Kunden von Ihrem Geschäft zu kaufen. Es ist **standardmäßig deaktiviert** – das Aktivieren ist eine bewusste Entscheidung, und bis Sie dies tun, wird nichts an Ihrem Geschäft für diese Assistenzsysteme sichtbar sein.

## Aktivieren

Öffnen Sie **Einstellungen → KI-Einkauf** und schalten Sie **Agenterbasierter Handel aktiviert** ein. Ab diesem Zeitpunkt können Assistenzsysteme, die das Universal Commerce Protocol unterstützen, Ihr Geschäft entdecken und Ihren Katalog einsehen. An Ihrem normalen Frontend-Geschäft ändert sich nichts.

## Die Bereitschaftsübersicht

Oben auf der KI-Einkauf-Seite beantwortet eine Zeile eine Frage: **Können KI-Assistenten aktuell von Ihrem Geschäft kaufen?**

- **„KI-Assistenten können von Ihrem Geschäft kaufen“** – alles Nötige für einen Kauf ist vorhanden.
- **„KI-Assistenten können Ihr Geschäft durchsuchen, können aber noch nicht kaufen“** – Ihr Geschäft ist erkennbar, aber etwas fehlt, bevor ein Kauf abgeschlossen werden kann (meist ein angeschlossener Zahlungsdienstleister).
- **„Notstopp aktiv“** oder **„Agenterbasierter Handel ist deaktiviert“** – nichts wird an Assistenzsysteme weitergegeben.

Unter dem Ergebnis sehen Sie eine kurze Checkliste – Zahlungsdienstleister angeschlossen, Versandkosten können angezeigt werden, Produkte sind für Assistenzsysteme sichtbar – mit einem Hinweis neben allem, was noch Aufmerksamkeit benötigt. Die Zähler zeigen an, wie viele Produkte Assistenzsysteme verkaufen können, wie viele Sie ihnen verborgen haben, wie viele Assistenzsysteme besucht haben und wie viele Sie blockiert haben.

Die Checkliste spiegelt Ihre **Live-Konfiguration** wider: Schließen Sie einen Zahlungsdienstleister an oder fügen Sie eine Versandmethode hinzu, und das Ergebnis aktualisiert sich beim nächsten Öffnen der Seite.

## Der Notstopp

Der **Notstopp** ist ein separates Schalter vom Hauptschalter. Nutzen Sie ihn, um alle Assistenzaktivitäten sofort zu stoppen – beispielsweise, wenn etwas nicht richtig aussieht – ohne Ihre Konfiguration zu ändern. Deaktivieren Sie ihn, um den Betrieb wieder aufzunehmen. Denken Sie an den Hauptschalter als „Ist diese Funktion konfiguriert?“ und an den Notstopp als „Alles sofort stoppen“.

## Was Assistenzsysteme tun können

Zwei Zugriffsstufen, die separat gesteuert werden können:

- **Lesen** (Entdeckung und Durchsuchen) ist risikoreicher. Ein Assistenzsystem kann Ihr Geschäft finden und Produktinformationen einsehen.
- **Kasse** (tatsächlicher Kauf) ist risikoreicher und bleibt für nicht verifizierte Assistenzsysteme geschlossen, es sei denn, Sie erlauben es.

Ein Geschäft kann entdeckbar sein, ohne käuflich zu sein – eine nützliche Methode, um zu beginnen.

## Spezifische Produkte verbergen

Jedes Produkt hat eine Einstellung **Sichtbar für KI-Einkaufsagenten** (standardmäßig aktiviert). Schalten Sie sie aus, um ein bestimmtes Produkt von Assistenzsystemen zu verbergen, während es weiterhin auf Ihrem Frontend-Geschäft sichtbar bleibt – nützlich für Artikel, die Sie lieber nur über Ihre eigene Website verkaufen möchten.

## Einzelne Assistenzsysteme verwalten

Wenn ein Assistenzsystem zum ersten Mal kauft – oder versucht, dies zu tun –, protokolliert Spwig dies unter **KI-Einkauf → Agentenidentitäten**. Jeder Eintrag zeigt den verifizierten Heimatort des Assistenzsystems (den Ordner, mit dem es sich signiert) und die Anzahl der Anfragen, die es gestellt hat. Der Name und das Logo, das ein Assistenzsystem präsentiert, werden nur als *beantragte* Details angezeigt – behandeln Sie sie als Bezeichnung, nicht als Nachweis der Identität; der verifizierte Heimatort ist der Teil, den man vertrauen kann.

Neue Assistenzsysteme starten **begrenzt**: sie können Transaktionen tätigen, aber innerhalb von Grenzen. Um eines zu blockieren, wählen Sie es aus und wählen Sie **Ausgewählte Assistenzsysteme blockieren** – laufende Käufe enden und das Assistenzsystem kann nicht mehr kaufen, während bereits getätigte Zahlungen unverändert bleiben. **Ausgewählte Assistenzsysteme entblocken** bringt es in den begrenzten Zustand zurück (nie direkt auf unbegrenzt – das Entfernen von Grenzen ist immer ein separates, bewusstes Schritt).

## Aktivitätsprotokoll

**KI-Einkauf → Agentenereignisse** ist ein Protokoll, das Manipulationen erkennen kann, das aufzeichnet, was Assistenzsysteme getan haben – jede verifizierte Anfrage, jeder blockierte Versuch, jede von Ihnen vorgenommene Änderung. Es ist nur zum Lesen und kann nicht bearbeitet oder gelöscht werden, daher dient es als Beweis, wenn ein Kauf, den ein Assistenzsystem getätigt hat, jemals in Streit gerät.

## Hinweis zu den Assistenzsystem-Plattformen

Die Unternehmen, die diese Assistenzsysteme betreiben (und die Regeln, um auf diesen Plattformen erscheinen zu können), sind neu und ändern sich oft.

Einige erfordern, dass Sie sich bewerben oder regionale Bedingungen erfüllen, bevor Ihre Produkte über sie gekauft werden können.


Spwig macht Ihren Store bereit; ob ein bestimmter Assistent Sie auflistet, hängt von diesem Assistenten ab.