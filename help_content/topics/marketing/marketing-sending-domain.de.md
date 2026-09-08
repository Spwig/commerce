---
title: Marketing-Versanddomain
---

## Marketing-Versanddomain

Ihr Shop sendet zwei sehr verschiedene Arten von E-Mails:

- **Transaktional** — Bestellbestätigungen, Versandupdates, Passwort-Resets. Diese müssen immer den Posteingang erreichen.
- **Marketing** — Newsletter, Promotionen, Warenkorb-Rettung, Lagerbestandsbenachrichtigungen.

Standardmäßig werden beide unter derselben Versandidentität versendet, was bedeutet, dass sie sich **einen Absender-Ruf teilen**. Wenn eine Marketingkampagne Spam-Beschwerden auslöst oder auf veraltete Adressen trifft, sinkt dieser Ruf — und Ihre Bestellbestätigungen und Passwort-Resets können ebenfalls im Spam landen.

Eine **Marketing-Versanddomain** behebt dieses Problem. Sie richten eine zweite Versandidentität ein — auf einer eigenen Subdomain wie `news.yourstore.com` — und kennzeichnen sie für Marketing. Spwig sendet dann jede Kampagne von dieser Identität und behält die transaktionalen E-Mails auf Ihrer Hauptdomain. Eine schlechte Kampagne kann den E-Mail-Verkehr, den Ihre Kunden *benötigen*, nicht mehr negativ beeinflussen.

> Dies gilt für selbst gehostete Shops. Bei Spwig-gehosteten Plänen wird der Versand-Ruf für Sie verwaltet.

## Wie Spwig entscheidet, welche Identität verwendet wird

Sobald ein Marketing-Versandkonto existiert, ist die Routing-Automatik aktiv — Sie müssen nichts kennzeichnen:

- **Marketing-E-Mails** (Kampagnen, Journeys, Newsletter, Warenkorb-Rettung, Lagerbestand) →
  die Marketing-Versanddomain.
- **Transaktionale E-Mails** (Bestellungen, Versand, Passwort-Resets, Verifizierung) → Ihre
  Hauptdomain.

Wenn Sie nie eine Marketing-Domain einrichten, ändert sich nichts: Alles wird weiterhin von Ihrem Standardkonto genau wie zuvor versendet.

## Einrichtung

Sie können von einem der beiden Einstiegspunkte aus starten:

- Der Button **"Marketing-Domain einrichten"** im Banner des Campaign Studio Dashboards, oder
- **E-Mail-Konten → "Marketing-Versanddomain"**.

![Das Campaign Studio Dashboard mit dem Banner "Schützen Sie Ihre transaktionalen E-Mails" und dem Button Marketing-Domain einrichten](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![Der Button Marketing-Versanddomain in der Liste der E-Mail-Konten, neben Anbieter durchsuchen](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Beide öffnen den E-Mail-Einrichtungsassistenten, der bereits für ein Marketing-Konto vorbereitet ist. Dann:

1. **Wählen Sie eine Subdomain.** Verwenden Sie etwas wie `news.yourstore.com` oder
   `mail.yourstore.com`. Dies ist der wichtigste Schritt: Die Marketing-Identität muss eine
   **andere (Sub)domain** sein als die, die Ihre transaktionalen E-Mails verwenden — diese Trennung
   ist genau das, was Ihren transaktionalen Ruf schützt. Marketing von Ihrer
   Hauptdomain zu versenden, bietet keine Isolation.
2. **Geben Sie die Absenderadresse** auf dieser Subdomain ein, z. B. `news@news.yourstore.com`.
3. **Fügen Sie die DNS-Einträge hinzu.** Der Assistent generiert SPF-, DKIM- und DMARC-Einträge für die
   Subdomain — einschließlich eines DKIM-Schlüssels, der einzigartig für diese Marketing-Identität ist. Fügen Sie sie bei
   Ihrem DNS-Anbieter hinzu (der Assistent hat Kopier-Buttons und Tabs pro Anbieter), und führen Sie dann die
   Prüfung durch, bis alle Einträge bestanden sind.
4. **Abschließen.** Das Konto wird erstellt und als **Nur Marketing** markiert. Ab jetzt werden Ihre
   Kampagnen von diesem Konto versendet.

Sie können auf der Liste der **E-Mail-Konten** überprüfen, ob es funktioniert: Sie sehen ein zweites Konto mit
Zweck **Nur Marketing**, und das Banner im Campaign Studio verschwindet.

## Gut zu wissen

- **Sie können transaktionale E-Mails nicht versehentlich beschädigen.** Spwig lässt es nicht zu, dass Sie Ihr einziges
  Konto auf "Nur Marketing" setzen, oder Ihr letztes transaktionalen Konto deaktivieren/löschen — es gibt
  immer ein Ziel für Bestellbestätigungen und Passwort-Resets.
- **Wärmen Sie schrittweise auf.** Eine brandneue Versanddomain hat noch keinen Ruf.

Erhöhen Sie Ihr
  Volumen über ein paar Wochen, anstatt am ersten Tag Ihre gesamte Liste zu bombardieren.
- **Halten Sie die DNS-Einträge der Subdomain gesund.** SPF, DKIM und DMARC auf der Marketing-Subdomain
  müssen gültig bleiben, genau wie bei Ihrer Hauptdomain.

Siehe die [Email Deliverability Runbook](deliverability) für das vollständige Bild.
- **Einwilligung gilt weiterhin.** Marketing-E-Mails werden nur an Abonnenten gesendet, die sich eingewilligt haben,
  und jeder Kampagnen enthält einen Abmeldelink — das Trennen des Domänen-Namens ändert nichts davon.