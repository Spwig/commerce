---
title: Page Builder
---

Il Page Builder è un editor visivo a trascinamento per la creazione di pagine ricche e responsive senza scrivere codice. Aggiungi elementi da una libreria di 39 componenti, stili con potenti utilità, configura animazioni e regole di visibilità, e pubblica con l'intero storico delle versioni.

![Page Builder](/static/core/admin/img/help/page-builder/builder-overview.webp)

## L'Interfaccia del Builder

Il builder ha quattro aree principali:

| Area | Posizione | Scopo |
|------|----------|---------|
| **Barra degli Strumenti** | Barra superiore | Anteprima del dispositivo (desktop/tablet/mobile), annulla/ripristina, impostazioni della pagina, salva bozza, pubblica |
| **Libreria degli Elementi** | Barra laterale sinistra | Esplora e trascina 39 elementi organizzati in 9 categorie |
| **Canvas** | Centro | Area di editing WYSIWYG in tempo reale — vedi i cambiamenti mentre li fai |
| **Pannello delle Proprietà** | Barra laterale destra | Modifica il contenuto, lo stile, le animazioni e le impostazioni avanzate dell'elemento selezionato |

## Libreria degli Elementi

Gli elementi sono organizzati in categorie. Trascina qualsiasi elemento dalla libreria sul canvas per aggiungerlo alla tua pagina.

| Categoria | Elementi |
|----------|----------|
| **Layout** | Container, Divider, Hero Section, Modal Popup, Navigation Menu, Spacer |
| **Basic** | Heading, Text, Button, Icon |
| **Content** | Blog Post Carousel, Blog Post Grid, FAQ Accordion, Related Posts, Testimonials |
| **Media** | Image, Image Gallery, Image Accordion, Video Embed |
| **Forms** | Contact Form, Form, Newsletter Signup |
| **Marketing** | Countdown Timer, CTA Banner, Featured Blog Banner, Loyalty Banner, Promotion Banner, Trust Badges, Voucher Code Display |
| **E-commerce** | Category Showcase, Gift Card Promo, Product Carousel, Product Grid, Product List, Reviews Display, Sale Products, Store Locator |
| **Social** | Social Links |
| **Navigation** | Search Bar |

### Container e Annidamento

L'elemento **Container** è la base per i layout complessi. I container possono contenere altri elementi — incluso altri container — permettendoti di costruire griglie a più colonne e strutture annidate. Utilizza i preset di layout del container per impostare rapidamente disposizioni di colonne comuni (50/50, 33/33/33, 25/75, ecc.).

## Aggiunta di Elementi

1. Trova l'elemento che desideri nella barra laterale sinistra
2. **Trascinalo** sul canvas e rilascialo dove lo desideri
3. Gli elementi possono essere rilasciati tra elementi esistenti o all'interno di container
4. La linea di inserimento blu mostra dove l'elemento verrà posizionato
5. Dopo il rilascio, l'elemento è automaticamente selezionato e il pannello delle proprietà si apre

Puoi anche riordinare gli elementi trascinandoli su o giù sul canvas.

## Modifica del Contenuto

Seleziona qualsiasi elemento sul canvas per aprire le sue proprietà nel pannello di destra. La scheda **Contenuto** mostra i campi specifici per quel tipo di elemento.

![Pannello delle Proprietà](/static/core/admin/img/help/page-builder/properties-panel.webp)

Per esempio:
- **Heading** — testo, tag HTML (H1–H6), allineamento, ID ancore
- **Image** — origine immagine (libreria media), testo alternativo, link, dimensioni
- **Button** — etichetta, URL, variante di stile, icona
- **Product Grid** — origine dati, numero di colonne, prodotti per pagina, ordine di ordinamento
- **Hero Section** — titolo, sottotitolo, descrizione, background, pulsanti di chiamata all'azione

I campi del contenuto traducibili mostrano un'icona di traduzione — clicca per aggiungere traduzioni per negozi multilingua.

## Stilizzazione degli Elementi

La scheda **Stile** fornisce controlli visivi per ogni elemento. Ogni sezione apre un editor dedicato per le utilità.

![Scheda Stile](/static/core/admin/img/help/page-builder/style-tab.webp)

| Sezione | Cosa Controlla | Utilità |
|---------|-----------------|---------|
| **Tipografia** | Famiglia del font, dimensione, peso, altezza del rigo, spaziatura tra lettere, stile del testo | Editor della Tipografia |
| **Colori** | Colore del testo con input esadecimale/RGB/HSL e token del tema | Selettore di Colore |
| **Background** | Colore solido, gradienti, immagini o video di background con stati di hover | Editor del Background |
| **Bordo** | Larghezza, stile, colore e raggio del bordo per lato | Editor del Bordo |
| **Spaziatura** | Margine e padding con editor del modello a scatola visivo | Editor della Spaziatura |
| **Effetti** | Ombra della scatola con preset e supporto per più strati, cursore di opacità | Editor dell'Ombra |

Ogni utilità è documentata in un proprio argomento di aiuto — cerca "color picker", "background editor", ecc. per ulteriori informazioni.

## Animazioni

La scheda **Animazioni** ti permette di aggiungere movimento agli elementi.

### Animazioni di Ingresso

Vengono attivate quando l'elemento scorre in vista:

| Animazione | Descrizione |
|-----------|-------------|
| Fade In | Appare gradualmente |
| Slide In (Up/Down/Left/Right) | Scivola da una direzione |
| Zoom In | Si ingrandisce da piccolo a dimensione completa |
| Bounce In | Si muove in posizione con un balzo |
| Pulse / Shake / Bounce / Flash / Spin | Effetti che richiamano l'attenzione |

Configura **durata** (0,3s–1,5s), **ritardo** (0–1s), **funzione di timing** (ease, ease-in, ease-out, lineare), e **ripetizione** (una volta o infinita).

### Animazioni su Hover

Vengono attivate quando un visitatore passa il mouse sull'elemento:

| Effetto | Descrizione |
|--------|-------------|
| Scale Up / Scale Down | Si ingrandisce o si riduce |
| Lift | Si solleva verso l'alto |
| Rotate (CW / CCW) | Ruota in senso orario o antiorario |
| Brighten / Fade | Modifica la luminosità o l'opacità |
| Shadow Grow | L'ombra si espande |
| Lift with Shadow | Si solleva con un'ombra crescente |
| Pulse Scale / Skew / Border Glow | Effetti speciali |

Configura **durata**, **timing** e **intensità** (sottile, normale, forte).

## Impostazioni Avanzate

La scheda **Avanzate** fornisce un controllo fine-grained:

### Regole di Visibilità

Controlla quando un elemento è mostrato o nascosto in base a condizioni:

- **Stato dell'utente** — autenticato, non autenticato, nuovo cliente, cliente ritornato
- **Dispositivo** — desktop, tablet, mobile
- **Ora** — intervallo di date, orario del giorno, giorno della settimana
- **Gruppo di clienti** — VIP, wholesale, ecc.
- **Valore del carrello** — totale minimo o massimo del carrello
- **Geografia** — paese, regione
- E 20+ tipi di regole aggiuntive

Le regole possono essere combinate con logica AND/OR per un targeting complesso.

### CSS Personalizzato

| Campo | Scopo |
|-------|---------|
| **ID Elemento** | ID unico per collegamenti di ancore o targeting CSS |
| **Classi CSS Personalizzate** | Classi aggiuntive da applicare |
| **Stili CSS Personalizzati** | CSS inline per sovrascrivere singolarmente |
| **Attributi Dati** | Attributi personalizzati data-* come coppie chiave-valore |
| **Z-Index** | Ordine di sovrapposizione per elementi sovrapposti |

## Flusso di Pubblicazione

Le pagine utilizzano un sistema di bozza/pubblicazione con l'intero storico delle versioni:

| Stato | Significato |
|--------|---------|
| **Bozza** | Lavoro in corso — non visibile ai visitatori |
| **Pubblicata** | Attiva sul tuo negozio |
| **Archiviata** | Rimossa dal sito ma conservata |

### Funzionamento

1. Apporta modifiche nel builder — vengono salvate come **bozza**
2. Clicca su **Salva Bozza** per salvare senza pubblicare
3. Clicca su **Pubblica** per rendere la bozza corrente attiva
4. Ogni pubblicazione crea una **istantanea della versione**
5. Puoi **ripristinare** qualsiasi versione precedente dall'history delle versioni (icona dell'orologio nella barra degli strumenti)

Questo significa che puoi sperimentare liberamente — la tua pagina attiva rimane invariata finché non pubblichi esplicitamente.

## Template delle Pagine

Risparmia tempo lavorando con template:

- **Salva come Template** — salva il design di qualsiasi pagina come un template riutilizzabile
- **Crea da Template** — inizia una nuova pagina da un template esistente
- **Categorie dei Template** — organizza i template per scopo (pagina di atterraggio, informazioni, showcase dei prodotti, ecc.)

I template catturano l'intera struttura della pagina inclusi tutti gli elementi, il contenuto e lo stile.

## Design Risponsivo

Utilizza i pulsanti di anteprima del dispositivo nella barra degli strumenti per vedere come la tua pagina appare su diverse dimensioni di schermo:

- **Desktop** — layout a piena larghezza
- **Tablet** — viewport medio
- **Mobile** — viewport stretto

Gli elementi si riassegnano automaticamente in base alle impostazioni del loro container. Puoi anche utilizzare le regole di visibilità per mostrare o nascondere elementi specifici su determinati dispositivi.

## Consigli

- **Inizia con un Container** — la maggior parte dei layout inizia con un container per creare colonne e struttura. Utilizza i preset di layout per disposizioni comuni.
- **Utilizza le sezioni Hero per gli header delle pagine** — l'elemento Hero fornisce titolo, sottotitolo, immagine di background e pulsanti di chiamata all'azione in un unico componente.
- **Anteprima prima di pubblicare** — clicca su Anteprima per vedere esattamente cosa vedranno i visitatori, quindi pubblica quando sei soddisfatto.
- **Utilizza le regole di visibilità per la personalizzazione** — mostra contenuti diversi agli utenti autenticati rispetto a quelli non autenticati, o mira a gruppi specifici di clienti.
- **Mantieni le animazioni sottili** — una o due animazioni di ingresso per sezione di pagina appaiono professionali. Troppa animazione può sembrare sopraffacente.
- **Nomina i tuoi container** — utilizza il campo ID Elemento per etichettare i container (es. "hero-section", "features") in modo che siano facili da trovare in pagine complesse.
- **Testa su tutti i dispositivi** — utilizza l'anteprima del dispositivo per verificare il tuo layout su desktop, tablet e mobile prima di pubblicare.
- **Sfrutta i template** — salva i tuoi migliori disegni di pagina come template per velocizzare la creazione futura delle pagine.