---
title: Media Library
---

La Libreria Media è il centro di gestione per tutte le immagini, video, modelli 3D e file utilizzati nel tuo negozio. Carica i file trascinandoli, organizza con cartelle e tag e lascia che il sistema ottimizzi automaticamente le immagini per un caricamento rapido.

![Media Gallery](/static/core/admin/img/help/media-library/media-gallery.webp)

## Interfaccia della Galleria

Accedi a **Libreria Media** nel menu laterale per aprire la galleria. L'interfaccia ha tre aree:

| Area | Posizione | Scopo |
|------|----------|---------|
| **Zona Caricamento** | Barra laterale sinistra, in alto | Trascina e rilascia i file per caricarli (immagini, video, modelli 3D fino a 100 MB) |
| **Cartelle & Tag** | Barra laterale sinistra, sotto | Esplora le cartelle, filtra per tag, accedi al Cestino |
| **Griglia Media** | Area principale | Cerca, filtra, esplora e gestisci tutti i tuoi asset |

### Controlli della Barra degli Strumenti

La barra degli strumenti sopra la griglia media fornisce:

- **Cerca** — trova asset per titolo, testo alternativo, descrizione o nome del tag
- **Filtro per tipo** — mostra solo Immagini, Video o Modelli 3D
- **Filtro per dimensioni** — filtra per dimensione del file (Piccola, Media, Grande)
- **Azioni di massa** — Seleziona Elementi, Modifica Dettagli, Elimina Selezionati
- **Modalità di visualizzazione** — Griglia (grande), Griglia Piccola, o Visualizzazione Elenco (persistente tra le sessioni)

## Caricamento dei File

Trascina uno o più file sulla **Zona Caricamento** nella barra laterale sinistra, o fai clic sulla zona per aprire un selettore di file.

### Formati Supportati

| Tipo | Formati |
|------|---------|
| **Immagini** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Video** | MP4, WebM, MOV, MKV, AVI |
| **Modelli 3D** | GLB, glTF |

### Coda di Caricamento

Quando si caricano più file, compare un gestore della coda che mostra:

- Il nome di ogni file e la barra di avanzamento del caricamento
- Caricamenti paralleli (fino a 2 alla volta per prestazioni)
- Lo stato di elaborazione mentre i file vengono ottimizzati dopo il caricamento
- Opzione per annullare singoli caricamenti o eliminare gli elementi completi

La coda è trascinabile e può essere ridotta in modo da poter continuare a lavorare mentre i caricamenti vengono completati.

## Ottimizzazione Automatica delle Immagini

Ogni immagine che carichi viene ottimizzata automaticamente:

- **Conversione in WebP** — una versione WebP viene generata insieme all'originale (qualità 85%) per un caricamento più rapido
- **Generazione di miniature** — vengono create diverse dimensioni in base ai tuoi preset di immagine
- **Orientamento EXIF** — le immagini vengono ruotate automaticamente nell'orientamento corretto

### Preset di Immagini del Sistema

La piattaforma include 21 preset predefiniti che coprono casi d'uso comuni:

| Preset | Dimensioni | Taglio | Utilizzato Per |
|--------|-----------|------|---------|
| **Miniatura** | 150 x 150 | Copertura | Liste amministrative, anteprime rapide |
| **Piccola** | 300 x 300 | Copertura | Cartelle di prodotti piccole |
| **Media** | 600 x 600 | Contenuto | Cartelle di prodotti, miniature del blog |
| **Grande** | 1200 x 1200 | Contenuto | Pagine di dettaglio del prodotto |
| **Galleria** | 800 x 800 | Contenuto | Gallerie di immagini |
| **Hero** | 1920 x 1080 | Copertura | Sezioni hero, banner delle pagine |
| **Banner** | 1200 x 400 | Copertura | Banner promozionali |
| **Cartella** | 400 x 300 | Copertura | Cartelle di funzionalità, cartelle di contenuti |
| **Avatar** | 200 x 200 | Taglio | Avatar dei clienti e del personale |
| **Elenco Prodotti** | 400 x 400 | Copertura | Cartelle della griglia dei prodotti |
| **Dettaglio Prodotto** | 1200 x 1200 | Copertura | Immagini complete dei prodotti |
| **Miniatura Prodotto** | 100 x 100 | Copertura | Selettori di varianti, mini carrelli |
| **Banner Categoria** | 1920 x 480 | Copertura | Intestazioni delle pagine delle categorie |
| **Miniatura Categoria** | 300 x 200 | Copertura | Cartelle delle categorie |
| **Logo Intestazione** | 300 x 80 | Allungamento | Logo dell'intestazione del sito |
| **Logo Footer** | 200 x 60 | Allungamento | Logo del piè di pagina del sito |
| **Logo Email** | 400 x 100 | Allungamento | Loghi dei modelli di email |
| **Logo Quadrato** | 160 x 160 | Allungamento | Posizioni per loghi quadrati |
| **Logo Brand** | 200 x 100 | Allungamento | Loghi di brand/partners |
| **Banner Annuncio** | 800 x 300 | Copertura | Immagini di annuncio |
| **Fondo Annuncio** | 1200 x 800 | Copertura | Fondi di annuncio |

I preset del sistema non possono essere rinominati o eliminati. Puoi creare preset personalizzati aggiuntivi sotto **Libreria Media > Preset di Dimensioni Immagine** se hai bisogno di dimensioni non coperte dai preset predefiniti.

### Modalità di Taglio

| Modalità | Comportamento |
|------|----------|
| **Copertura** | Riempie l'intera area, tagliando gli bordi se necessario — ideale per cartelle e banner |
| **Contenuto** | Adatta l'immagine intera all'area, aggiungendo spazio trasparente se necessario — ideale per immagini di prodotti |
| **Taglio** | Taglia al centro per le dimensioni esatte |
| **Allungamento** | Adatta l'immagine e aggiungi un bordo (trasparente, bianco o nero) — ideale per loghi |

## Organizzazione dei File

### Cartelle

Crea cartelle per organizzare i tuoi media in gruppi logici. Le cartelle possono essere annidate a qualsiasi profondità. Fai clic su una cartella nella barra laterale sinistra per mostrare solo gli asset al suo interno. Il collegamento **Tutti i File** mostra tutto.

### Tag

Aggiungi tag agli asset per un'organizzazione flessibile tra le cartelle. I tag appaiono in una nuvola nella barra laterale sinistra. Fai clic su un tag per filtrare gli asset per quel tag. Gli asset possono avere più tag.

### Ricerca

La barra di ricerca trova asset per titolo, testo alternativo, descrizione o nome del tag. Combina la ricerca con i filtri per tipo e dimensioni per ottenere risultati precisi.

## Dettagli dell'Asset

Fai clic su un asset per aprire la sua vista dettagliata con un'anteprima grande e i metadati completi.

![Dettagli dell'Asset](/static/core/admin/img/help/media-library/media-detail.webp)

La vista dettagliata mostra:

- **Anteprima** — anteprima dell'immagine grande con le dimensioni originali
- **Informazioni sul file** — tipo, dimensioni, dimensione del file, data di caricamento
- **Schede** per l'editing:

| Scheda | Campi |
|-----|--------|
| **Generale** | Titolo, Testo Alternativo, Descrizione (tutti traducibili per negozi multilingua) |
| **Tecnica** | Tipo MIME, hash del file, nome del file originale, stato della versione WebP |
| **Organizzazione** | Assegnazione cartella, tag, commutatore pubblico/privato |
| **Avanzato** | Coordinate del punto focale, ID esterno, JSON dei metadati |

### Campi Traducibili

Titolo, testo alternativo e descrizione supportano le traduzioni. Fai clic sull'icona di traduzione accanto a ciascun campo per aggiungere traduzioni per le tue lingue abilitate. Questo assicura che le immagini abbiano un testo alternativo e descrizioni localizzate correttamente per SEO e accessibilità.

### Tracciamento dell'Utilizzo

Il sistema traccia dove ogni asset viene utilizzato in tutta la piattaforma. La sezione **Utilizzo dei Media** in basso mostra ogni modello e campo che fa riferimento a questo asset, aiutandoti a comprendere l'impatto prima di apportare modifiche o eliminare.

## Supporto per Video

I video caricati nella libreria media vengono analizzati automaticamente:

- **Estrazione dei metadati** — durata, risoluzione, frequenza di fotogrammi, bitrate e codec vengono catturati
- **Immagine poster** — una miniature viene generata dal video per l'anteprima
- **Streaming** — i video supportano le richieste di intervallo per cercare senza scaricare l'intero file
- **Conversione opzionale** — i video possono essere convertiti in formato WebM/AV1 ottimizzato per una consegna più rapida

## Cestino

Cancellare un asset lo sposta nel **Cestino** invece di eliminarlo definitivamente. Questo protegge da cancellazioni accidentali.

| Azione | Cosa Fa |
|--------|-------------|
| **Cancella** | Sposta l'asset nel Cestino (cancellazione morbida) |
| **Ripristina** | Restituisce un asset cancellato al suo luogo originale |
| **Cancellazione Permanente** | Rimuove l'asset e tutte le sue miniature dallo storage in modo permanente |
| **Vuota Cestino** | Elimina definitivamente tutti gli elementi nel Cestino |

Fai clic su **Cestino** nella barra laterale sinistra per visualizzare e gestire gli asset cancellati.

## Dove Viene Utilizzata la Libreria Media

La libreria media è integrata in tutto il piattaforma:

| Funzionalità | Come Utilizza i Media |
|---------|------------------|
| **Catalogo dei Prodotti** | Immagini dei prodotti, immagini delle varianti, banner delle categorie |
| **Blog** | Immagini principali, immagini all'interno del contenuto tramite CKEditor |
| **Costruttore di Pagine** | Elementi immagine, background hero, componenti galleria |
| **Costruttore di Intestazione/Piede di Pagina** | Immagini del logo, immagini di background |
| **Impostazioni del Sito** | Logo del sito e favicon |
| **Annunci** | Immagini di annuncio e fondi di annuncio |
| **CKEditor** | Tutti i caricamenti di immagini in testo ricco passano attraverso la libreria media |
| **Programma di Fidelizzazione** | Immagini di premi e livelli |

Quando selezioni un'immagine in una di queste funzionalità, la galleria della libreria media si apre come finestra modale per un facile navigazione e selezione.

## Consigli

- **Utilizza titoli e testi alternativi descrittivi** — una buona metadati migliora SEO e accessibilità. Il sistema utilizza il testo alternativo nei tag immagine in tutto il negozio online.
- **Organizza con cartelle fin dall'inizio** — crea una struttura di cartelle (es. Prodotti, Blog, Banner, Loghi) prima di caricare molti file. È molto più facile organizzare man mano che vai che riassemblare più tardi.
- **Utilizza tag per categorie trasversali** — tag come 'stagionali', 'vendita' o 'stile di vita' ti aiutano a trovare asset che coprono più cartelle.
- **Controlla l'utilizzo prima di cancellare** — la sezione di tracciamento dell'utilizzo mostra dove un asset è riferito. Cancellare un asset utilizzato potrebbe lasciare immagini rotte nel tuo negozio online.
- **Lascia che WebP faccia il lavoro** — la conversione automatica in WebP riduce tipicamente le dimensioni dei file del 25-35% rispetto al JPEG senza perdita visibile di qualità. Non è necessario convertire manualmente le immagini prima del caricamento.
- **Crea preset personalizzati** — se hai un layout unico che richiede una dimensione specifica dell'immagine, crea un preset personalizzato invece di ridimensionare manualmente le immagini.