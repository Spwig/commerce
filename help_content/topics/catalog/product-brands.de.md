---
title: Produktmarken
---

Marken ermöglichen es Ihnen, Produkte mit ihrem Hersteller oder Label zu verknüpfen und den Kunden eine Möglichkeit geben, Ihr Geschäft nach Marken durchzusehen. Jede Marke erhält ihre eigene Seite auf Ihrem Online-Shop, auf der Kunden alle Produkte dieser Marke entdecken, die Marchengeschichte lesen und zu der offiziellen Marke-Website gelangen können.

Navigieren Sie zu **Katalog > Marken**, um Ihre Marken zu verwalten.

## Warum Marken verwenden

Marken haben in Spwig zwei Zwecke:

1. **Organisation** — Produkte werden mit einer Marke versehen, was es Kunden, die einer bestimmten Marke treu sind, leicht macht, das zu finden, was sie suchen
2. **Warenpräsentation** — Markenseiten sind ein dedizierter Raum, um die Marchengeschichte, das Logo und das gesamte Produktportfolio zu präsentieren, was die Umwandlungsrate für markenbewusste Kunden verbessern kann

Marken arbeiten auch mit dem Promotions-System — Sie können einen Verkauf durchführen, der auf alle Produkte einer bestimmten Marke anwendbar ist, ohne jedes Produkt einzeln auswählen zu müssen.

## Eine Marke erstellen

1. Navigieren Sie zu **Katalog > Marken**
2. Klicken Sie auf **+ Marke hinzufügen**
3. Füllen Sie den Abschnitt **Grundlegende Informationen** aus:
   - **Name** — der Marke-Name, wie er auf Ihrem Online-Shop angezeigt wird (muss eindeutig sein)
   - **Slug** — der URL-Pfad für die Markenseite (wird automatisch aus dem Namen befüllt; Sie können ihn anpassen)
   - **Beschreibung** — eine kurze Beschreibung der Marke, die auf der Markenseite angezeigt wird
   - **Website** — die offizielle Website-URL der Marke (optional — wird als Link auf der Markenseite angezeigt)
4. Fügen Sie Markenmaterialien hinzu:
   - **Logo** — das Logo der Marke, das in Markenlisten und auf der Markenseite verwendet wird
   - **Bannerbild** — ein breites Bannerbild, das oben auf der Markenseite angezeigt wird
5. Schreiben Sie die **Markengeschichte** (optional) — ein längeres Editorial über die Geschichte, Werte oder das Besondere der Marke. Dies erscheint auf der Markenseite des Online-Shops und kann eine effektive Möglichkeit sein, die Geschichte der Marke für interessierte Kunden zu erzählen.
6. Konfigurieren Sie die **SEO**-Felder:
   - **Meta-Titel** — der Titel der Seite, der in Suchmaschinenergebnissen angezeigt wird
   - **Meta-Beschreibung** — die kurze Beschreibung, die unter dem Titel in den Suchergebnissen angezeigt wird
7. Legen Sie Anzeigeoptionen fest:
   - **Markenseite anzeigen** — steuert, ob die Marke eine öffentlich zugängliche Seite hat. Deaktivieren Sie dies, um eine Marke aus dem Online-Shop zu verbergen, während sie im System bleibt.
   - **Aktiv** — steuert, ob die Marke für die Zuordnung zu Produkten und sichtbar im Geschäft ist
   - **Als Highlight markieren** — markiert die Marke für eine hervorgehobene Platzierung in Ihrem Theme (z. B. eine Zeile mit Markenlogos auf der Startseite)
8. Klicken Sie auf **Speichern**

## Produkte einer Marke zuweisen

Marken werden auf individuellen Produktverzeichnissen zugewiesen, nicht von der Markenverwaltungsseite aus. Um eine Marke einem Produkt zuzuweisen:

1. Navigieren Sie zu **Katalog > Produkte** und öffnen Sie das Produkt
2. Im Produktformular suchen Sie das Feld **Marke**
3. Suchen Sie nach und wählen Sie die passende Marke aus
4. Speichern Sie das Produkt

Sobald eine Marke zugewiesen ist, wird das Produkt automatisch auf der Markenseite des Online-Shops angezeigt.

## Markenseiten auf Ihrem Online-Shop

Jede Marke mit **Markenseite anzeigen** aktiviert erhält ihre eigene Seite unter `/brand/{slug}/`. Die Seite zeigt an:

- Das Markenlogo und das Bannerbild
- Den Markennamen und die Beschreibung
- Die Markengeschichte (wenn vorhanden)
- Ein Link zur offiziellen Marke-Website (wenn vorhanden)
- Alle aktiven Produkte, die dieser Marke zugewiesen sind

Kunden können zu Markenseiten gelangen, indem sie auf den Markennamen auf einer Produktseite klicken oder über Links, die Sie in Ihrer Navigation oder Ihrem Seitenbuilder erstellen, navigieren.

## SEO für Markenseiten

Das Ausfüllen der Felder **Meta-Titel** und **Meta-Beschreibung** für jede Marke hilft dabei, dass Ihre Markenseiten gut in den Suchergebnissen angezeigt werden. Effektive SEO-Titel für Marken kombinieren in der Regel den Markennamen mit dem, was die Marke verkauft:

| Marke | Guter Meta-Titel |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Wenn Sie die SEO-Felder leer lassen, wird Ihr Theme standardmäßig auf den Markennamen zurückgreifen.

### Automatische SEO-Erstellung

Wenn **SEO automatisch generiert** für eine Marke aktiviert ist, generiert Spwig automatisch Titel- und Beschreibungsinhalte für die Meta-Tags, wenn die Marke gespeichert wird.

Dies ist für Geschäfte mit vielen Marken praktisch, gibt Ihnen aber weniger Kontrolle über die genaue Formulierung.

Sie können den generierten Inhalt immer überschreiben, indem Sie direkt in die Felder tippen und den Schalter zur automatischen Generierung deaktivieren.

## Hervorgehobene Marken

Das **Als hervorgehoben markieren**-Flag wird von Themes verwendet, um eine kurierte Zeile oder ein Raster von Markenlogos anzuzeigen – häufig auf der Startseite. Nur eine kleine Anzahl von Marken sollte gleichzeitig hervorgehoben werden; konsultieren Sie die Dokumentation Ihres Themes, um zu verstehen, wie viele hervorgehobene Marken optimal angezeigt werden.

## Tipps

- Laden Sie ein Markenlogo als PNG oder WebP mit transparentem Hintergrund hoch – es wird auf jeder Hintergrundfarbe in Ihrem Theme sauber angezeigt
- Schreiben Sie eine überzeugende Markengeschichte, auch für weniger bekannte Marken; Kunden, die eine Marke nicht kennen, schätzen den Kontext, der ihnen hilft zu entscheiden, ob die Produkte für sie passen
- Wenn Sie Promotionen für spezifische Marken durchführen, stellen Sie sicher, dass der Markenname in Spwig exakt übereinstimmt – Promotionen verwenden die Beziehung zur Marke auf Produkten, um die Berechtigung zu bestimmen
- Deaktivieren Sie eine Marke, anstatt sie zu löschen, wenn Sie ihre Produkte nicht mehr führen – eine Löschung entfernt die Verweisung auf die Marke von allen zugehörigen Produkten, während die Deaktivierung die Historie beibehält
- Verwenden Sie das **Als hervorgehoben markieren**-Flag sparsam; eine Startseite mit 20 Markenlogos verliert an Wirkung im Vergleich zu 6–8 sorgfältig ausgewählten