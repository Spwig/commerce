---
title: Clipart e Font per Prodotti Personalizzabili
---

L'editor di design include due tipi di asset creativi che puoi fornire ai clienti: **clipart** (grafiche preconfezionate che possono aggiungere ai loro design) e **font personalizzati** (oltre ai font standard del sistema). Creare una libreria ben curata di asset rende l'editor più utile e aiuta i clienti a creare design migliori più velocemente.\n\n## Libreria di clipart\n\nLa clipart dà ai clienti una libreria di grafiche preconfezionate che possono aggiungere ai loro design con un solo clic. Invece di richiedere ai clienti di trovare e caricare le proprie immagini per elementi comuni come icone, bordi o grafiche decorative, puoi fornirgliene di pronte all'uso.\n\n### Creare categorie di clipart\n\nLa clipart è organizzata in categorie che i clienti possono navigare. Le categorie aiutano i clienti a trovare ciò di cui hanno bisogno rapidamente.\n\n1. Vai a **Prodotti Personalizzabili > Categorie di Clipart**\n2. Clicca su **+ Aggiungi Categoria di Clipart**\n3. Compila:\n   - **Nome della Categoria** — Cosa vedono i clienti (es. \"Sport\", \"Bordi\", \"Festività\")\n   - **Slug** — Generato automaticamente dal nome\n   - **Icona** — Una classe di icona Font Awesome per la scheda della categoria (es. `fas fa-football-ball`)\n   - **Ordine di Sorteggio** — Controlla l'ordine in cui le categorie appaiono nell'editor\n4. Clicca su **Salva**\n\n**Esempi di categorie per un negozio di magliette:**\n\n| Categoria | Icona | Esempio di clipart |\n|----------|------|-----------------|\n| Sport | `fas fa-football-ball` | Logo di squadra, attrezzature sportive, simboli sportivi |\n| Umorismo | `fas fa-laugh` | Meme, citazioni divertenti, personaggi animati |\n| Natura | `fas fa-leaf` | Animali, fiori, paesaggi |\n| Geometrico | `fas fa-shapes` | Pattern, forme astratte, disegni tribali |\n\n**Esempi di categorie per un negozio di stampa/poster:**\n\n| Categoria | Icona | Esempio di clipart |\n|----------|------|-----------------|\n| Bordi | `fas fa-border-all` | Cornici decorative, ornamenti negli angoli |\n| Stagionali | `fas fa-snowflake` | Icone di festività, motivi stagionali |\n| Icone | `fas fa-icons` | Stelle, cuori, frecce, segni di controllo |\n| Sfondi | `fas fa-image` | Texture, gradienti, pattern |\n\n### Aggiungere asset di clipart\n\nOgni asset di clipart è un file immagine (PNG o SVG) che i clienti possono posizionare sul loro canvas.\n\n1. Vai a **Prodotti Personalizzabili > Asset di Clipart**\n2. Clicca su **+ Aggiungi Asset di Clipart**\n3. Compila:\n   - **Nome** — Nome descrittivo (es. \"Stella d'oro\", \"Casco da football\")\n   - **Categoria** — Seleziona da quelle di clipart disponibili\n   - **Asset Immagine** — Clicca per aprire la Libreria Media e selezionare o caricare il file immagine\n   - **Ambito** — Scegli la disponibilità (vedi di seguito)\n   - **Etichette** — Parole chiave cercabili per questa clipart (es. `["stella", "oro", "decorazione"]`)\n   - **Ordine di Sorteggio** — Controlla la posizione all'interno della categoria\n4. Clicca su **Salva**\n\n### Comprendere l'ambito della clipart\n\nOgni asset di clipart ha un ambito che controlla dove è disponibile:\n\n| Ambito | Descrizione | Caso d'uso |\n|-------|-------------|----------|\n| **Disponibile per tutti i prodotti** | Appare nel browser di clipart per ogni prodotto personalizzabile | Grafiche generali come stelle, bordi e icone comuni |\n| **Solo per un prodotto specifico** | Appare solo per un prodotto selezionato | Grafiche specifiche per prodotti come loghi marchiati o artwork tematici del prodotto |\n\nPer la maggior parte degli asset, usa **Disponibile per tutti i prodotti**. Riserva l'ambito specifico per prodotti agli asset che hanno senso solo in contesto di un prodotto specifico — ad esempio, loghi specifici per un prodotto di merchandising di una squadra.\n\n### Linee guida per i file di clipart\n\n- **Formato:** Usa PNG per grafiche raster e SVG per grafiche vettoriali. I file SVG si scalano senza perdita di qualità, rendendoli ideali per clipart che i clienti potrebbero ridimensionare significativamente\n- **Risoluzione:** I file PNG dovrebbero essere almeno 500x500 pixel per una buona qualità di stampa\n- **Fondo:** Usa fondi trasparenti (PNG con canale alfa o SVG) in modo che la clipart si fonda naturalmente con il design\n- **Dimensione del file:** Mantieni i singoli file di clipart sotto i 500KB per un caricamento rapido nell'editor\n\n## Font personalizzati\n\nI font personalizzati estendono il selettore di font nell'editor di design oltre ai font standard del sistema.

Questo ti permette di offrire una tipografia curata che si adatta al tuo brand o allo stile del prodotto.

### Aggiunta di una font personalizzata

1. Vai a **Prodotti Personalizzabili > Font Personalizzati**
2. Clicca su **+ Aggiungi Font Personalizzato**
3. Compila i seguenti campi:
   - **Nome Font** — Nome visualizzato nel selettore del font (es. "Playfair Display")
   - **Famiglia Font** — Nome della famiglia font CSS utilizzato internamente (es. `PlayfairDisplay`)
   - **Normale** — Clicca per caricare il file del font in peso normale tramite la Libreria Media
   - **Grassetto** — Variante opzionale in peso grassetto
   - **Corsivo** — Variante opzionale in corsivo
   - **Grassetto Corsivo** — Variante opzionale in grassetto e corsivo
4. Clicca su **Salva**

Il peso **Normale** è obbligatorio per i font personalizzati. Le varianti grassetto, corsivo e grassetto corsivo sono opzionali — se non vengono fornite, il browser cercherà di sintetizzare questi stili a partire dal font normale, anche se i risultati potrebbero non apparire altrettanto raffinati rispetto a file font dedicati.

### Font del sistema vs font personalizzati

Puoi anche registrare font del sistema preinstallati su quasi tutti i dispositivi:

1. Aggiungi un nuovo entry di font personalizzato
2. Seleziona **Font del sistema**
3. Inserisci il nome della famiglia font esattamente come appare in CSS (es. `Georgia`, `Courier New`)
4. Non è necessario caricare alcun file per i font del sistema

I font del sistema si caricano immediatamente poiché sono già presenti sul dispositivo del cliente. I font caricati personalmente richiedono un download iniziale, il che aggiunge un piccolo ritardo quando il font viene selezionato per la prima volta.

### Consigli per i font per tipo di prodotto

**Per magliette e abbigliamento:**
- I font grassetto e impattanti funzionano meglio: Impact, Anton, Bebas Neue, Oswald
- Le lettere bloccate e i font sans-serif sono più leggibili su tessuti
- Evita font sottili o delicati che potrebbero non stampare bene su superfici testurate

**Per poster e prodotti da stampa:**
- Font serif eleganti per progetti formali: Playfair Display, Merriweather, Lora
- Font script per inviti e biglietti: Great Vibes, Dancing Script, Pacifico
- Font sans-serif puliti per progetti moderni: Montserrat, Raleway, Open Sans

### Formati dei file dei font

| Formato | Estensione | Consiglio |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Preferito — dimensione del file più piccola, caricamento più veloce |
| TrueType | `.ttf` | Buona alternativa — ampiamente compatibile |

I file WOFF2 sono generalmente del 30-50% più piccoli rispetto ai file TTF, quindi si caricano più velocemente nell'editor del cliente. Utilizza WOFF2 quando disponibile.

## Gestione della tua libreria di asset

### Organizzazione per i clienti

L'ordine in cui gli asset appaiono nell'editor è controllato dal campo **Ordine di Sort** su entrambe le categorie e gli asset singoli. I numeri più bassi appaiono per primi. Utilizza questo per:

- Posizionare le categorie di clipart più popolari in cima
- Posizionare le clipart più utili e versatili in cima a ogni categoria
- Ordinare i font con le opzioni più utilizzate in cima

### Mantieni la libreria aggiornata

- Aggiungi clipart stagionali prima delle festività (Halloween, Natale, San Valentino) e disattivali dopo
- Utilizza la casella **Attivo** per nascondere temporaneamente gli asset senza eliminarli
- Monitora quali clipart e font vengono utilizzati di più dai clienti e espandi quelle categorie

## Consigli

- Inizia con il piede giusto — 20-30 clipart di alta qualità distribuite su 3-4 categorie è meglio che centinaia di opzioni mediocri. Puoi sempre aggiungere di più man mano che impari cosa desiderano i clienti.
- Utilizza il formato SVG per le clipart quando possibile. I file SVG sono più piccoli, si adattano perfettamente a qualsiasi dimensione e producono stampe più nitide rispetto alle immagini raster.
- Testa ogni font caricato nell'editor di progettazione per assicurarti che tutti i caratteri vengano visualizzati correttamente, specialmente i caratteri speciali e gli accenti se i clienti utilizzano più lingue.
- Etichetta le clipart in modo dettagliato — i clienti cercano per parola chiave, quindi etichette descrittive come "oro", "stella", "a 5 punte", "decorazione" aiutano a trovare l'asset giusto velocemente.
- Raggruppa le clipart correlate nello stesso categoria. Se vendi merchandising per squadre, crea una categoria per ogni sport invece di una singola categoria "Sport" molto grande.
- Rivedi regolarmente la tua libreria di clipart dal punto di vista del cliente visitando l'editor di progettazione sullo store.