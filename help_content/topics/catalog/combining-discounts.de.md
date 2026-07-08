---
title: Rabatte kombinieren
---

Die Plattform bietet vier Arten von Rabatten an, die zusammenarbeiten können: Produktverkäufe, Promotionen, Gutschein-Codes und Geschenkkarten. Das Verständnis davon, wie sie sich gegenseitig beeinflussen, hilft Ihnen dabei, effektive Kampagnen zu erstellen, ohne unerwartete Ergebnisse oder unbeabsichtigte Doppelrabatte.

## Die vier Rabattschichten

Jeder Rabatttyp funktioniert auf einer anderen Ebene und ist dem Kunden auf unterschiedliche Weise sichtbar.

| Schicht | Wo es festgelegt wird | Wie es angewendet wird | Sichtbar für den Kunden |
|-------|---------------|-----------------|-------------------|
| **Produktverkauf** | Produktbearbeitungsformular > Verkaufsabschnitt | Ändert automatisch den angezeigten Preis | Ja — wird als durchgestrichener ursprünglicher Preis angezeigt |
| **Promotion** | Marketing > Verkäufe & Promotionen | Wird automatisch auf passende Produkte angewendet | Ja — wird als Verkaufspreis auf Produktkarten angezeigt |
| **Gutschein-Code** | Marketing > Gutscheine | Der Kunde gibt einen Code zur Kasse ein | Nur zur Kasse, nachdem der Code eingegeben wurde |
| **Geschenkkarte** | Wird bei der Kasse aus dem Geschenkkarten-Saldo angewendet | Reduziert den Gesamtbetrag der Zahlung | Nur zur Kasse |

## Wie die Priorität funktioniert

Promotionen haben ein **Prioritäts**-Feld, das Werte von 0 und höher akzeptiert. Höhere Zahlen bedeuten höhere Priorität.

Wenn mehrere Promotionen dasselbe Produkt treffen, gewinnt die mit der **höchsten Priorität**. Sie überschneiden sich nicht — nur eine Promotion gilt pro Produkt.

**Beispiel:** "Flash-Verkauf 50% Rabatt" (Priorität 10) und "Sommer-Verkauf 20% Rabatt" (Priorität 5) zielen beide auf alle Produkte ab. Ein Kunde sieht den 50% Flash-Verkaufspreis, nicht 70% kombiniert.

Innerhalb derselben Prioritätsebene wählt das System die Promotion aus, die dem Kunden den größten Rabatt gewährt.

## Stapelregeln

Die folgende Tabelle zeigt, welche Rabattkombinationen erlaubt sind und wie Sie sie steuern können.

| Kombination | Erlaubt? | Wie man sie steuert |
|-------------|----------|-------------------|
| Produktverkauf + Promotion | Nur wenn aktiviert | Prüfen Sie **"Mit Produktverkäufen stapelbar"** in den erweiterten Einstellungen der Promotion |
| Promotion + Promotion | Nein — die höchste Priorität gewinnt | Setzen Sie Prioritätswerte, um zu steuern, welche angewendet wird |
| Promotion + Gutschein-Code | Ja | Promotion reduziert den Produktpreis, Gutschein reduziert den Warenkorb-Gesamtbetrag separat |
| Gutschein + Gutschein | Konfigurierbar | Das Flag **"Kann nicht mit anderen Gutscheinen kombiniert werden"** des Gutscheins steuert dies (standardmäßig aktiviert) |
| Gutschein + Verkaufsartikel | Konfigurierbar | Das Flag **"Verkaufsartikel ausschließen"** des Gutscheins steuert dies |
| Geschenkkarte + beliebiger Rabatt | Ja — immer | Geschenkkarten werden zuletzt angewendet, reduzieren den Endzahlungsbetrag nach allen anderen Rabatten |

## Typische Szenarien

### Szenario A: Sitewide Promotion + Gutschein-Code

- **Einrichtung:** 20% Rabatt auf alles (Promotion) + Kunde hat einen 10$-Gutschein
- **Ergebnis:** Ein Produkt im Wert von 100$ wird auf 80$ reduziert (Promotion), dann wird der 10$-Gutschein auf den Warenkorb-Gesamtbetrag angewendet. Der Kunde zahlt **70$**.

### Szenario B: Produkt im Verkauf + Sitewide Promotion

- **Einrichtung:** Produkt hat einen 30% Produkt-Rabatt + es gibt eine 20% Sitewide-Promotion
- **Ergebnis (Stapelung deaktiviert):** Nur der Produkt-Rabatt gilt. Der Kunde zahlt **70$**.
- **Ergebnis (Stapelung aktiviert):** Beide gelten. 30% Rabatt zuerst = 70$, dann 20% Rabatt = **56$**.

### Szenario C: Zwei Promotionen auf dasselbe Produkt

- **Einrichtung:** "Flash-Verkauf 40% Rabatt" (Priorität 10) + "Sommer-Verkauf 20% Rabatt" (Priorität 5), beide zielen auf alle Produkte ab
- **Ergebnis:** Flash-Verkauf gewinnt, da er eine höhere Priorität hat. Der Kunde zahlt **60$** für ein 100$-Produkt.

### Szenario D: Gutschein auf einem Produkt im Verkauf

- **Einrichtung:** Produkt ist im Verkauf mit 25% Rabatt. Kunde gibt einen 10% Gutschein-Code ein, bei dem das Flag **"Verkaufsartikel ausschließen"** aktiviert ist.
- **Ergebnis:** Der Gutschein gilt nicht für dieses Produkt. Wenn der Warenkorb nicht-Verkaufsartikel enthält, gilt der Gutschein nur für diese.

## Welche Rabattart zu verwenden

| Ziel | Empfohlener Ansatz | Warum |
|------|---------------------|-----|
| Saisonale Lagerbewegung | **Promotion** (Kategorie- oder Sammlungsziel) | Automatisch, keine Kundenhandlung erforderlich, sichtbar auf Produktkarten |
| Belohnung eines bestimmten Kunden | **Gutschein-Code** (Einmalig, pro-Kunden-Limit) | Zielgenau, nachverfolgbar, fühlt sich persönlich an |
| Schneller Einzelprodukt-Deal | **Produktverkauf** (auf dem Produktbearbeitungsformular) | Schnellste Einrichtung, kein Promotion-Assistent erforderlich |
| Lagerkredit oder Geschenk | **Geschenkkarte** | Saldo-basiert, Kunde verwaltet seinen eigenen Kredit |
| Sitewide-Event | **Promotion** (alle Produkte als Ziel) | Maximale Reichweite, eine Einrichtung deckt alles ab |
| Wiederherstellungskampagne | **Gutschein-Code** (Einschränkungen für Neukunden oder Rückkehrende) | Kann bestimmte Kundensegmente anvisieren |

## Tipps

- **Testen Sie mit einem echten Warenkorb** — nachdem Sie Promotionen und Gutscheine eingerichtet haben, fügen Sie Produkte in einen Warenkorb hinzu und durchlaufen Sie den Checkout, um sicherzustellen, dass die Rabatte wie erwartet angewendet werden.
- **Überprüfen Sie die Anzahl der betroffenen Produkte** — in der Promotion-Überprüfungsschritt, stellen Sie sicher, dass die Anzahl der betroffenen Produkte Ihrem Ziel entspricht.
- **Verwenden Sie Prioritäten bewusst** — wenn Sie mehrere Promotionen gleichzeitig laufen lassen, legen Sie immer unterschiedliche Prioritätswerte fest, damit Sie steuern können, welche gewinnt.
- **Deaktivieren Sie Stapelung standardmäßig** — aktivieren Sie "Mit Produktverkäufen stapelbar" nur, wenn Sie bewusst Doppelrabatte wünschen.
- **Dokumentieren Sie Ihre Strategie** — verwenden Sie das Beschreibungsfeld der Promotion, um zu notieren, warum eine Promotion existiert und wie sie sich zu anderen aktiven Promotionen verhält.