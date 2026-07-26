---
title: Rabatte kombinieren
---

Die Plattform bietet vier Arten von Rabatten, die zusammenarbeiten können: Produktverkäufe, Promotionen, Gutschein-Codes und Geschenkkarten. Das Verständnis davon, wie sie sich gegenseitig beeinflussen, hilft Ihnen dabei, effektive Kampagnen zu erstellen, ohne unerwartete Ergebnisse oder unbeabsichtigte Doppelrabatte.

> **Geschenkkarten können noch nicht am Online-Checkout angewendet werden.** Das unten beschriebene Design – Geschenkkarte wird zuletzt angewendet, nach allen anderen Rabatten – ist die Art und Weise, wie es funktionieren wird, sobald diese Funktion bereitgestellt wird. Derzeit kann eine Geschenkkarte nur vor Ort am **Kassensystem** eingelöst werden, daher gelten die unten beschriebenen Interaktionen für den Online-Shop noch nicht explizit für Geschenkkarten. Siehe das **Geschenkkarten**-Hilfethema für den aktuellen Stand.

## Die vier Rabattschichten

Jeder Rabatttyp arbeitet auf einer anderen Ebene und ist dem Kunden auf unterschiedliche Weise sichtbar.

| Schicht | Wo es festgelegt wird | Wie es angewendet wird | Sichtbar für den Kunden |
|-------|---------------|-----------------|-------------------|
| **Produktverkauf** | Produktbearbeitungsformular > Verkaufsabschnitt | Ändert automatisch den angezeigten Preis | Ja – wird als durchgestrichener ursprünglicher Preis angezeigt |
| **Promotion** | Marketing > Verkäufe & Promotionen | Wird automatisch auf passende Produkte angewendet | Ja – wird als Verkaufspreis auf Produktkarten angezeigt |
| **Gutschein-Code** | Marketing > Gutscheine | Der Kunde gibt einen Code am Checkout ein | Nur am Checkout nach Eingabe des Codes |
| **Geschenkkarte** | Wird gegen den Geschenkkartenbestand eingelöst | Reduziert den Gesamtbetrag der Zahlung | Nur vor Ort am Kassensystem (siehe oben erwähnte Notiz) |

## Wie die Priorität funktioniert

Promotionen haben ein **Prioritätsfeld**, das Werte von 0 und höher akzeptiert. Höhere Zahlen bedeuten höhere Priorität.

Wenn mehrere Promotionen dasselbe Produkt treffen, gewinnt die mit der **höchsten Priorität**. Sie überschneiden sich nicht – nur eine Promotion gilt pro Produkt.

**Beispiel:** "Flash Sale 50% Rabatt" (Priorität 10) und "Sommer Sale 20% Rabatt" (Priorität 5) zielen beide auf alle Produkte ab. Ein Kunde sieht den 50% Flash Sale Preis, nicht 70% kombiniert.

Innerhalb derselben Prioritätsebene wählt das System die Promotion aus, die dem Kunden den größten Rabatt gewährt.

## Stapelregeln

Die folgende Tabelle zeigt, welche Rabattkombinationen erlaubt sind und wie Sie sie steuern können.

| Kombination | Erlaubt? | Wie man sie steuert |
|-------------|----------|-------------------|
| Produktverkauf + Promotion | Nur wenn aktiviert | Prüfen Sie **„Mit Produktverkäufen stapeln“** in den erweiterten Einstellungen der Promotion |
| Promotion + Promotion | Nein – die höchste Priorität gewinnt | Setzen Sie Prioritätswerte, um zu steuern, welche angewendet wird |
| Promotion + Gutschein-Code | Ja | Promotion reduziert den Produktpreis, Gutschein reduziert den Warenkorbgesamtbetrag separat |
| Gutschein + Gutschein | Konfigurierbar | Der Gutschein-Flag **„Kann nicht mit anderen Gutscheinen kombiniert werden“** steuert dies (standardmäßig aktiviert) |
| Gutschein + Verkaufsartikel | Konfigurierbar | Der Gutschein-Flag **„Verkaufsartikel ausschließen“** steuert dies |
| Geschenkkarte + Jeder Rabatt | Ja – immer | Geschenkkarten werden zuletzt angewendet, reduzieren den Endzahlungsbetrag nach allen anderen Rabatten. Derzeit nur am Kassensystem möglich – siehe oben erwähnte Notiz |

## Typische Szenarien

### Szenario A: Sitewide Promotion + Gutschein-Code

- **Einrichtung:** 20% Rabatt auf alles (Promotion) + Kunde hat einen 10$-Gutschein
- **Ergebnis:** Ein 100$-Produkt wird zu 80$ (Promotion), dann wird der 10$-Gutschein auf den Warenkorbgesamtbetrag angewendet. Der Kunde zahlt **70$**.

### Szenario B: Produkt im Verkauf + Sitewide Promotion

- **Einrichtung:** Produkt hat einen 30% Produktverkauf + 20% Sitewide Promotion existiert
- **Ergebnis (Stapelung deaktiviert):** Nur der Produktverkauf gilt. Der Kunde zahlt **70$**.
- **Ergebnis (Stapelung aktiviert):** Beide gelten. 30% Rabatt zuerst = 70$, dann 20% Rabatt = **56$**.

### Szenario C: Zwei Promotionen auf dasselbe Produkt

- **Einrichtung:** "Flash Sale 40% Rabatt" (Priorität 10) + "Sommer Sale 20% Rabatt" (Priorität 5), beide zielen auf alle Produkte ab
- **Ergebnis:** Flash Sale gewinnt, da Priorität höher ist. Der Kunde zahlt **60$** für ein 100$-Produkt.

### Szenario D: Gutschein auf einem Verkaufsprodukt

- **Einrichtung:** Produkt ist im Verkauf für 25% Rabatt.


# Kunden geben einen 10%-Gutscheincode ein, der "Verkaufsartikel ausschließen" aktiviert hat.
- **Ergebnis:** Der Gutschein gilt nicht für dieses Produkt.

Wenn der Warenkorb nicht-Verkaufsartikel enthält, gilt der Gutschein nur für diese.

## Welche Rabattart verwenden

| Ziel | Empfohlener Ansatz | Warum |
|------|---------------------|-----|
| Saisonales Lager bewegen | **Promotion** (Kategorie- oder Sammlungsziel) | Automatisch, keine Kundenhandlung erforderlich, sichtbar auf Produktkarten |
| Einen bestimmten Kunden belohnen | **Gutscheincode** (Einmalig, pro-Kunden-Limit) | Zielgerichtet, nachverfolgbar, fühlt sich persönlich an |
| Schneller Einzelproduktdeal | **Produktverkauf** (auf dem Produktbearbeitungsformular) | Schnellste Einrichtung, kein Promotion-Assistent erforderlich |
| Geschenkkarte oder Geschenk | **Geschenkkarte** | Standortbasiert; derzeit nur am Kassenschalter einlösbar |
| Weit verbreitete Veranstaltung | **Promotion** (alle Produkte als Ziel) | Maximale Reichweite, eine Einrichtung deckt alles ab |
| Wiederkehrende Kampagne | **Gutscheincode** (Einschränkungen für Neukunden oder Rückkehrende) | Kann bestimmte Kundensegmente anvisieren |

## Tipps

- **Mit einem echten Warenkorb testen** — nach der Einrichtung von Promotionen und Gutscheinen, fügen Sie Produkte in einen Warenkorb hinzu und gehen Sie durch den Checkout, um sicherzustellen, dass die Rabatte wie erwartet angewendet werden.
- **Überprüfen Sie die Anzahl der betroffenen Produkte** — im Überprüfungsschritt der Promotion, stellen Sie sicher, dass die Anzahl der betroffenen Produkte Ihrem Ziel entspricht.
- **Verwenden Sie Priorität bewusst** — wenn Sie mehrere Promotionen gleichzeitig laufen lassen, setzen Sie immer unterschiedliche Prioritätswerte, damit Sie steuern können, welche gewinnt.
- **Stapeln Sie standardmäßig deaktiviert lassen** — aktivieren Sie "Mit Produktverkäufen stapeln" nur, wenn Sie bewusst doppelte Rabatte wünschen.
- **Dokumentieren Sie Ihre Strategie** — verwenden Sie das Beschreibungsfeld der Promotion, um zu notieren, warum eine Promotion besteht und wie sie sich zu anderen aktiven Promotionen verhält.