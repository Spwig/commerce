---
title: Aggiunta di un prodotto
---

Questo documento illustra come creare un nuovo prodotto nel tuo negozio. Il modulo prodotto è organizzato in sezioni che coprono informazioni base, media, prezzi, inventario, SEO e altro ancora: puoi compilare tutto in una volta o tornare in seguito per completare le sezioni.

## Inizio

Dalla barra laterale, vai su **Prodotti > Tutti i prodotti** per visualizzare il tuo catalogo prodotti. Fai clic sul pulsante **+ Aggiungi prodotto** nell'angolo in alto a destra per aprire la form di creazione prodotti.

![Pagina elenco prodotti](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informazioni base

La sezione **Informazioni base** è dove definisci l'identità principale del prodotto.

![Modulo per l'aggiunta di un prodotto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campi obbligatori

- **Nome** — Il nome del prodotto visualizzato ai clienti. Fai clic sull'icona del globo per aggiungere le traduzioni per le altre lingue.
- **Slug** — Versione adatta alle URL del nome (generata automaticamente). Personalizzalo se necessario.
- **SKU** — Il tuo codice interno per il controllo del magazzino.
- **Tipo di prodotto** — Scegli tra: Base, Variabile, Digitale, Pacchetto, Buono regalo, Personalizzabile, Configurabile o Prenotazione.
- **Categoria** — Assegna il prodotto a una categoria per l'organizzazione e la navigazione del negozio.

### Stato e visibilità

Si trova nella sezione **Stato** in fondo al modulo:

- **Stato** — Impostalo su **Bozza** mentre lavori, **Pubblicato** quando sei pronto per la vendita, o **Discontinuato** per i prodotti che non offri più.
- **Segnala come prodotto in evidenza** — Seleziona per evidenziare questo prodotto nel tuo negozio.
- **È un prodotto digitale** — Seleziona se questo prodotto include download digitali (file, licenze). Può essere combinato con qualsiasi tipo di prodotto.
- ** Nascondi dal negozio** — Nasconde il prodotto dagli elenchi del catalogo, mantenendolo comunque disponibile come opzione di configurazione o componente del pacchetto.

### Campi opzionali

- **Marchio** — Associa un marchio se applicabile.
- **Tag** — Assegna uno o più tag nella scheda **Tag** più avanti in questa scheda. I tag sono diversi dalle raccolte: sono etichette veloci e non strutturate per organizzare e filtrare i prodotti, invece di un raggruppamento per la vendita. Inserisci il testo per cercare un tag esistente, oppure digita un nuovo nome per crearne uno in tempo reale. Vedere l'argomento **Tag dei prodotti** per creare, rinominare e cancellare in bulk i tag direttamente.

### Descrizioni del prodotto

- **Descrizione breve** — Appare negli elenchi prodotto e nelle schede. Mantienila breve e accattivante.
- **Descrizione completa** — Descrizione dettagliata del prodotto visualizzata nella pagina dettagli prodotto. Usa l'editor di testo per aggiungere formattazione, immagini, video e tabelle.

Entrambi i campi descrizione supportano la funzione di traduzione — fai clic sull'icona del globo per fornire contenuti in altre lingue.

### Funzionalità e specifiche

Mantieni tutti i formati markdown, i percorsi immagine, i blocchi di codice e i termini tecnici.

La sezione **Dettagli prodotto** contiene due campi dati strutturati:

- **Caratteristiche** — Coppie chiave-valore per le caratteristiche del prodotto (es. "Autonomia batteria: 20 ore").
- **Specifiche** — Dettagli tecnici per la scheda delle specifiche nella pagina del prodotto (es. "Processore: Intel i7").

## Media

La sezione **Media** ti permette di gestire le immagini del prodotto utilizzando la libreria media integrata.

![Scheda Media](/static/core/admin/img/help/add-product/media-tab.webp)

1. Clicca su **+ Aggiungi immagini dalla libreria media** per aprire il selettore media.
2. Seleziona immagini esistenti o carica nuove direttamente.
3. Trascina le immagini per cambiarne l'ordine — la **prima immagine** diventa l'immagine principale del prodotto visualizzata nelle liste e nei modelli.

Il campo **Tipo di galleria**, nella scheda **Impostazioni galleria** sotto l'elenco immagini, controlla come le immagini vengono visualizzate nel negozio: Galleria standard, Carousel, Layout a griglia, Galleria con zoom, o Visualizzazione 360°.

## Prezzi

Imposta il prezzo del prodotto e configura le vendite.

![Scheda Prezzi](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Prezzo regolare

- **Prezzo regolare** — Il prezzo di vendita al pubblico standard che i clienti vedranno. La valuta è impostata insieme al valore del prezzo.
- **Costo** — Il tuo costo del bene, utilizzato per calcolare i profitti. Questo non viene mai visualizzato ai clienti.

### Impostazioni scontate

Configura sconti temporanei:

- **Tipo di vendita** — Scegli tra: Nessuna vendita, Prezzo fisso in vendita, Importo scontato, o Percentuale scontata.
- **Valore della vendita** — L'importo dello sconto o la percentuale.
- **Data inizio vendita / Data fine vendita** — Programmazione quando la vendita attiva e scade. Lasciare vuoto per un avvio immediato o nessuna data di fine.

### Prezzi multivaluta

Se la multivaluta è abilitata nel tuo negozio, appare un campo **Strategia prezzi**:

- **Prezzo dinamico** — I prezzi in altre valute vengono calcolati automaticamente utilizzando i tassi di cambio configurati.
- **Prezzo fisso** — Imposta un prezzo specifico per ogni valuta separatamente utilizzando la sezione **Prezzi multivaluta** che appare sotto.

## Magazzino

Gestisci i livelli di scorta, il comportamento della spedizione e le caratteristiche fisiche del prodotto.

![Scheda Magazzino](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestione scorte

- **Traccia le scorte** — Abilita per tracciare le quantità di scorta (abilitato di default).
- **Soglia scorte basse** — Ricevi alert quando le scorte scendono sotto questo numero (default: 5).
- **Consenti ordinazioni in ritardo** — Abilita per accettare gli ordini anche quando non è disponibile.
- **Azione quando esaurito** — Sovrascrivi il comportamento del sito o della categoria quando il prodotto esaurisce: nascondilo, mostralo come non disponibile, mostra un pulsante "Notificami", o consenti ordinazioni in ritardo.

Le quantità delle scorte vengono gestite per magazzino. Dopo aver salvato il prodotto, utilizza la sezione **Articoli scorta** in fondo al modulo (oppure naviga su **Prodotti > Articoli scorta**) per impostare le quantità in ciascuna posizione del magazzino.

### Attributi fisici

Inserisci il peso del prodotto (kg) e le dimensioni (lunghezza, larghezza, altezza in cm) per calcoli precisi delle spese di spedizione.

### Spedizione

- **Richiede spedizione** — Se questo prodotto deve essere spedito al cliente. Abilitato di default per i prodotti fisici; il tuo negozio e il checkout lo utilizzano per decidere se raccogliere un indirizzo di spedizione e quotare l'acconto per l'ordine. Spwig attiva automaticamente la disattivazione per i prodotti Digitali, Prenotazioni e Gift Card, poiché non vengono mai spediti — non hai bisogno (e non puoi) di attivarlo nuovamente per quei tipi di prodotti. Lascialo selezionato per un prodotto fisico che sembra adatto a prodotti digitali, ad esempio un biglietto d'auguri stampato che viene spedito in una scatola.
- **Confezione di spedizione preferita** — Seleziona opzionalmente una delle tue confezioni di spedizione configurate. Quando impostato, le dimensioni della confezione vengono utilizzate per il calcolo dei costi di spedizione invece del peso e delle dimensioni del prodotto sopra — utile quando un prodotto viene sempre spedito nella stessa scatola standard o busta. Lascialo vuoto per utilizzare le caratteristiche fisiche del prodotto. Gestisci le confezioni disponibili sotto **Spedizione > Confezioni**.

### Ordine anticipato

Preserva tutti i formati markdown, i percorsi immagini, i blocchi di codice e i termini tecnici.

Utilizza la scheda **Pre-ordine** per vendere un prodotto prima che abbia scorte — utile per rilasci imminenti che desideri iniziare a prendere ordinazioni in anticipo rispetto al lancio:

- **È un pre-ordine** — Abilita per consentire ai clienti di acquistare questo prodotto anche quando non è disponibile.
- **Data di rilascio pre-ordine** — La data prevista di disponibilità, visualizzata ai clienti.
- **Messaggio pre-ordine** — Un breve messaggio personalizzato visualizzato ai clienti, fino a 200 caratteri (es. "Spedizione marzo 2026").

### Identificatori del prodotto

Codici standard per elenchi del mercato e sistemi di magazzino:

- **GTIN** — Numero di articolo globale
- **EAN** — European Article Number
- **UPC** — Codice prodotto universale (US)
- **ISBN** — Per libri
- **ASIN** — Identificativo Amazon
- **MPN** — Numero parte del produttore

### Spedizione internazionale / dogane

Obbligatorio per spedizioni internazionali (espandi la sezione **Spedizione internazionale / Dogane**):

- **Codice HS** — Codice di classificazione del sistema armonizzato
- **Nazione di origine** — Dove viene prodotto il prodotto
- **Prezzo unitario doganale** — Valore dichiarato per unità per le dogane
- **Numero autorizzazione all'esportazione** — Richiesto solo per articoli controllati o limitati
- **Scadenza autorizzazione all'esportazione** — Data di scadenza dell'autorizzazione all'esportazione

## SEO

Ottimizza la visibilità del prodotto nei motori di ricerca.

![Scheda SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Titolo meta** — Il titolo visualizzato nei risultati del motore di ricerca. Fare clic sull'icona del globo per tradurre.
- **Descrizione meta** — Una breve descrizione per i risultati della ricerca (max 160 caratteri). Fare clic sull'icona del globo per tradurre.
- **Genera automaticamente SEO** — Seleziona per generare automaticamente il contenuto SEO quando il prodotto viene salvato.

Un'anteprima **Anteprima risultato ricerca** mostra esattamente come apparirà il tuo prodotto nei risultati di ricerca di Google.

## Impostazioni pagina prodotto

Nella scheda **Avanzate**, la scheda **Impostazioni pagina prodotto** ti permette di controllare come appare la pagina del negozio di questo prodotto:

- **Modello pagina** — Sostituisci il layout predefinito del sito per questo prodotto: Classico, Larghezza intera, Focus galleria, o Digitale. Lascialo impostato su **Usa layout predefinito del sito** per ereditare il layout specificato nelle tue impostazioni di progettazione — la maggior parte dei prodotti dovrebbe rimanere sulle impostazioni predefinite in modo che i cambiamenti del modello vengano applicati automaticamente.
- **Mostra prodotti correlati** — Visualizza prodotti correlati in fondo alla pagina.
- **Mostra recensioni** — Visualizza le recensioni dei clienti.
- **Mostra specifiche** — Visualizza la scheda delle specifiche.

Il campo **Tipo galleria** — che controlla come vengono visualizzate le immagini del prodotto (Galleria standard, Carousel, Layout griglia, Galleria zoom, o Visualizzazione 360°) — è impostato separatamente, nella scheda **Media**.

## Canale di vendita

Il campo **Canale di vendita** (nella sezione Stato) controlla dove può essere venduto il prodotto:

- **Tutti i canali** — Disponibile online e in negozio (POS).
- **Solo online** — Non disponibile tramite terminali POS.
- **Solo in negozio** — Non elencato online; disponibile solo nel tuo negozio fisico.

Un campo **Barcode** è disponibile anche per la scansione del codice a barre del POS.

## Salvataggio del prodotto

Quando sei pronto, usa i pulsanti di salvataggio nell'angolo in alto a destra. Il prodotto sarà visibile nel negozio una volta che lo stato è impostato su **Pubblicato**.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi immagini, i blocchi di codice e i termini tecnici.

- Inizia con lo stato **Bozza** in modo da poter perfezionare il prodotto prima che i clienti lo vedano.
- Carica più immagini: i prodotti con diverse foto hanno un tasso di conversione più alto.
- Compila i campi **SEO** per migliorare la visibilità nei motori di ricerca.
- Usa **Categorie**, **Marchi** e **Tag** per aiutare i clienti a navigare nel tuo catalogo.
- Per i prodotti variabili (ad esempio, dimensioni o colori diversi), scegli il tipo **Prodotto variabile** e aggiungi le varianti dopo aver salvato.
- Usa **Caratteristiche** e **Specifiche** per aggiungere dati strutturati sui prodotti che vengono visualizzati in schede dedicate sulla pagina del prodotto.
- Se **Richiede Spedizione** non rimane selezionato, controlla **Tipo di prodotto** - Spwig disattiva automaticamente la spedizione per i prodotti Digitali, Prenotazioni e Buoni Regalo, poiché nessuno di questi viene effettivamente spedito.
- Imposta un **Confezione di spedizione preferita** per i prodotti che vengono sempre spediti nello stesso imballaggio: ti risparmia il lavoro di tenere aggiornati peso e dimensioni del prodotto rispetto all"imballaggio effettivo utilizzato.