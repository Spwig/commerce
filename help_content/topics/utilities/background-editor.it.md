---
title: Editor del fondo
---

L'editor del fondo ti dà il pieno controllo sui fondi degli elementi con quattro tipi: colore solido, gradiente, immagine e video. Supporta anche gli stati Normal e Hover separatamente, in modo da poter creare effetti visivi interattivi. Apri la scheda **Style** di qualsiasi elemento e cerca la sezione **Background** per accedere all'editor.

![Editor del fondo](/static/core/admin/img/help/background-editor/background-editor.webp)

## Stati Normal e Hover

In alto nell'editor del fondo, un interruttore passa tra gli stati **Normal** e **Hover**. Ogni stato ha la propria configurazione indipendente del fondo:

- **Normal** — Il fondo predefinito visualizzato quando la pagina viene caricata
- **Hover** — Il fondo applicato quando un visitatore muove il cursore sull'elemento

Due piccoli blocchi di anteprima accanto all'interruttore mostrano i fondi Normal e Hover accanto, in modo da poter vedere il contrasto a colpo d'occhio. Configura lo stato Normal per primo, quindi passa a Hover per aggiungere un effetto interattivo se desiderato.

## Tipi di fondo

Seleziona un tipo di fondo dal riquadro di icone in alto nel pannello dell'editor:

| Tipo | Descrizione |
|------|-------------|
| **Color** | Un riempimento solido utilizzando un singolo valore di colore. Facile da applicare e leggero. |
| **Gradient** | Un'ombra liscia tra due o più colori, lineare o radiale. Include preset predefiniti come Ocean, Sunset, Forest e Berry. Per un editing avanzato dei gradienti, vedi l'argomento [Gradient Creator](gradient-creator). |
| **Image** | Un'immagine caricata o selezionata dalla libreria media. Supporta la posizione, la dimensione e il controllo del ripetizione. |
| **Video** | Un URL di video di fondo con un'immagine poster opzionale che viene visualizzata mentre il video si carica o su dispositivi mobili. |

Solo un tipo può essere attivo alla volta per stato. Cambiare i tipi non elimina la configurazione precedente — puoi tornare indietro e le tue impostazioni saranno preservate.

## Fondi a colori

Quando è selezionato **Color**:

- **Hex Input** — Digita un codice esadecimale direttamente (es. `#1A1A2E`)
- **Color Swatches** — Clicca su un swatch predefinito per una selezione rapida. I swatch sono a tema e riflettono il paletto del tema attivo.
- **Edit Button** — Apri il completo selettore di colori con spettro, cursori e opzioni di formato (vedi l'argomento [Color Picker](color-picker))

I fondi a colori vengono visualizzati immediatamente e non hanno alcun impatto sulle prestazioni, rendendoli ideali per sezioni, card e contenitori.

## Fondi a gradiente

Quando è selezionato **Gradient**:

- **Preset Gradients** — Scegli tra gradienti predefiniti: Ocean, Sunset, Forest, Berry e altri
- **Custom Gradient** — Clicca su **Edit** per aprire il creator di gradienti dove puoi impostare la direzione, il tipo (lineare o radiale) e i punti di colore
- **Angle Slider** — Regola la direzione del gradiente per i gradienti lineari (0-360 gradi)

I gradienti aggiungono profondità visiva senza richiedere asset immagine e si adattano perfettamente a qualsiasi dimensione dello schermo.

## Fondi immagine

Quando è selezionato **Image**:

- **Upload or Media Library** — Clicca sul posto per l'immagine per caricare una nuova immagine o selezionarne una dalla tua libreria media
- **Size** — Scegli **Cover** (riempie l'elemento, potrebbe tagliare), **Contain** (si adatta all'interno dell'elemento) o una dimensione personalizzata
- **Position** — Imposta il punto focale utilizzando una griglia a 9 punti (in alto a sinistra, centro, in basso a destra, ecc.) o inserisci percentuali personalizzate X/Y
- **Repeat** — Attiva o disattiva il ripetizione. Utile per pattern a piastrelle
- **Overlay** — Aggiungi un overlay di colore sopra l'immagine con opacità regolabile, utile per garantire la leggibilità del testo

Ottimizza sempre le immagini prima di caricarle. Le immagini non compresso di grandi dimensioni rallentano i tempi di caricamento della pagina.

## Fondi video

Quando è selezionato **Video**:

- **Video URL** — Inserisci un URL diretto a un file video MP4 o WebM
- **Poster Image** — Carica un'immagine di fallback visualizzata mentre il video si carica e su dispositivi che non riproducono automaticamente il video
- **Autoplay / Loop / Muted** — I fondi video vengono riprodotti automaticamente, in loop e sono muti di default per rispettare le politiche del browser

Mantieni i video di fondo brevi (10-30 secondi), compressi e visivamente sottili.

Dovrebbero migliorare la sezione senza distogliere l'attenzione dal contenuto.

## Dove appare

L'editor del background è disponibile per ogni elemento che supporta i background:

- **Page Builder** — Sezioni, contenitori, colonne e singoli elementi hanno una sezione Background nella scheda Style
- **Header/Footer Builder** — Background delle righe e dei singoli widget
- **Menu Builder** — Background del contenitore del menu e del pannello a discesa

Lo stesso interfaccia editor viene utilizzata ovunque, quindi il tuo flusso di lavoro rimane coerente tra gli editor.

## Consigli

- Utilizza un overlay di colore semitrasparente sui background delle immagini per assicurarti che il testo rimanga leggibile indipendentemente dal contenuto dell'immagine.
- I preset di gradienti sono un modo rapido per aggiungere interesse visivo — applicane uno, quindi personalizza l'angolo o i colori per adattarti al tuo brand.
- Imposta sia lo sfondo Normale che quello su Hover su carte interattive per fornire ai visitatori un feedback visivo chiaro quando esplorano il tuo contenuto.
- Per i background delle immagini, assicurati sempre di impostare un punto focale in modo che la parte più importante dell'immagine rimanga visibile su tutte le dimensioni dello schermo.
- Preferisci sfondi a colori o gradienti rispetto alle immagini per le sezioni in cui la velocità di caricamento è critica, ad esempio per il contenuto sopra la piega.
- Testa gli sfondi video su dispositivi mobili — la maggior parte dei browser mobili mostrerà l'immagine poster invece di riprodurre il video.