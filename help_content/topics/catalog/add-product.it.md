---
title: Aggiunta di un prodotto
---

Questo documento ti guiderà nella creazione di un nuovo prodotto nel tuo negozio. Il modulo prodotto è organizzato in sezioni che coprono informazioni di base, media, prezzi, inventario, SEO e altro ancora, in modo che tu possa compilare tutto in una volta o tornare a completare le sezioni in un secondo momento.

## Per iniziare

Dalla barra laterale, vai su **Prodotti > Tutti i prodotti** per vedere il tuo elenco prodotti. Fai clic sul pulsante **+ Aggiungi prodotto** nell'angolo in alto a destra per aprire la form di creazione prodotto.

![Pagina elenco prodotti](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informazioni base

La sezione **Informazioni base** è dove definisci l'identità principale del prodotto.

![Modulo per aggiungere un prodotto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campi obbligatori

- **Nome** — Il nome del prodotto visualizzato ai clienti. Fai clic sull'icona del globo per aggiungere le traduzioni per altre lingue.
- **Slug** — Versione adatta all'URL del nome (generato automaticamente). Personalizzalo se necessario.
- **SKU** — Il tuo codice interno per il controllo degli stock.
- **Tipo di prodotto** — Scegli tra: Base, Variabile, Digitale, Pacchetto, Buono regalo, Personalizzabile, Configurabile o Prenotazione.
- **Categoria** — Assegna il prodotto a una categoria per l'organizzazione e la navigazione del negozio.

### Stato e visibilità

Si trova nella sezione **Stato** in fondo alla form:

- **Stato** — Impostalo su **Bozza** mentre lavori, su **Pubblicato** quando sei pronto per vendere, o su **Discontinuato** per i prodotti che non offri più.
- **Segnala come prodotto in evidenza** — Seleziona per evidenziare questo prodotto nel tuo negozio.
- **È un prodotto digitale** — Seleziona se questo prodotto include download digitali (file, licenze). Può essere combinato con qualsiasi tipo di prodotto.
- ** Nascondi dal negozio** — Nasconde il prodotto dagli elenchi del catalogo, mantenendolo comunque disponibile come opzione di configuratore o componente del pacchetto.

### Campi opzionali

- **Marchio** — Associalo a un marchio se applicabile.
- **Tag** — Assegna uno o più tag nella scheda **Tag** più avanti in questa scheda. I tag sono diversi dalle raccolte: sono etichette veloci e non strutturate per organizzare e filtrare i prodotti, invece di un raggruppamento per la vendita. Inserisci il testo per cercare un tag esistente, oppure digita un nuovo nome per crearne uno in tempo reale. Vedere l'argomento **Tag dei prodotti** per creare, rinominare e cancellare in bulk i tag direttamente.

![La scheda Tag nella scheda Informazioni base, con due tag applicati nel selettore di tag](/static/core/admin/img/help/add-product/tags-card.webp)

### Descrizioni del prodotto

- **Descrizione breve** — Appare negli elenchi prodotto e nelle schede. Mantienila breve e coinvolgente.
- **Descrizione completa** — Descrizione dettagliata del prodotto visualizzata nella pagina dettagli prodotto. Usa l'editor di testo per aggiungere formattazione, immagini, video e tabelle.

Entrambi i campi descrizione supportano la funzione di traduzione — fai clic sull'icona del globo per fornire contenuti in altre lingue.

### Funzionalità e specifiche

La sezione **Dettagli prodotto** contiene due campi dati strutturati:

- **Funzionalità** — Coppie chiave-valore per i punti di forza del prodotto (es. "Autonomia batteria: 20 ore").
- **Specifiche** — Dettagli tecnici per la scheda specifiche della pagina prodotto (es. "Processore: Intel i7").

## Media

La sezione **Media** ti permette di gestire le immagini del prodotto utilizzando la libreria media integrata.

![Scheda Media](/static/core/admin/img/help/add-product/media-tab.webp)

1. Fai clic su **+ Aggiungi immagini dalla libreria media** per aprire il selettore media.
2. Seleziona immagini esistenti o carica nuove direttamente.
3. Trascina le immagini per cambiarne l'ordine — la **prima immagine** diventa l'immagine principale del prodotto visualizzata negli elenchi e nelle schede.

Il campo **Tipo di galleria**, nella scheda **Impostazioni galleria** sotto l'elenco immagini, controlla come le immagini vengono visualizzate nel negozio: Galleria standard, Carousel, Layout a griglia, Galleria con zoom o Visualizzazione 360°.

## Prezzi

Imposta il prezzo del prodotto e configura le vendite.

![Scheda Prezzi](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Prezzo normale

- **Prezzo normale** — Il prezzo di vendita al pubblico standard che i clienti vedranno.

La valuta viene impostata insieme all'importo del prezzo.
- **Costo** — Il tuo costo merce, utilizzato per calcolare i profitti.

Questo non viene mai mostrato ai clienti.

### Impostazioni vendita

Configura sconti temporanei:

- **Tipo vendita** — Scegli tra: Nessuna vendita, Prezzo fisso, Importo in meno, o Percentuale in meno.
- **Valore vendita** — L'importo dello sconto o la percentuale.
- **Data inizio vendita / Data fine vendita** — Programmazione quando la vendita attiva e scade. Lasciare vuoto per un avvio immediato o nessuna data di fine.

### Prezzi multi-valuta

Se la multi-valuta è abilitata nel tuo negozio, appare un campo **Strategia prezzi**:

- **Prezzo dinamico** — I prezzi in altre valute vengono calcolati automaticamente utilizzando i tassi di cambio configurati.
- **Prezzo fisso** — Imposta un prezzo specifico per ogni valuta separatamente utilizzando la sezione **Prezzi multi-valuta** che appare qui sotto.

## Magazzino

Gestisci i livelli di scorta, il comportamento della spedizione e le caratteristiche del prodotto fisico.

![Scheda magazzino](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestione scorte

- **Traccia le scorte** — Abilita per tracciare le quantità di scorta (abbinato di default).
- **Soglia scorte basse** — Ricevi alert quando le scorte scendono al di sotto di questo numero (valore predefinito: 5).
- **Consenti ordinazioni in ritardo** — Abilita per accettare gli ordini anche quando non è disponibile a magazzino. I nuovi prodotti iniziano con il valore **Consenti ordinazioni in ritardo di default** da **Impostazioni > Impostazioni negozio > Commercio**, ma puoi sovrascriverlo per prodotto in qualsiasi momento.
- **Azione scorte esaurite** — Sovrascrivi il comportamento a livello del sito o della categoria quando questo prodotto esaurisce: nascondilo, mostralo come non disponibile, mostra un pulsante "Notificami", oppure consenti ordinazioni in ritardo.

Le quantità delle scorte vengono gestite per magazzino. Dopo aver salvato il prodotto, utilizza la sezione **Articoli scorta** in fondo al modulo (oppure naviga su **Prodotti > Articoli scorta**) per impostare le quantità in ciascuna posizione del magazzino.

### Attributi fisici

Inserisci il peso del prodotto (kg) e le dimensioni (lunghezza, larghezza, altezza in cm) per calcoli precisi delle spese di spedizione.

### Spedizione

- **Richiede spedizione** — Se questo prodotto deve essere spedito al cliente. Abilitato di default per i prodotti fisici; il tuo negozio e il checkout lo utilizzano per decidere se raccogliere un indirizzo di spedizione e quotare l'acconto per l'ordine. Spwig disattiva automaticamente questa opzione per i prodotti Digitali, Booking e Gift Card, poiché non vengono mai spediti - non hai bisogno di (e non puoi) riattivarla per questi tipi di prodotti. Lasciala attiva per un prodotto fisico che sembra per caso essere simile a un prodotto digitale, ad esempio un buono regalo stampato che viene spedito in una scatola.
- **Confezione di spedizione preferita** — Seleziona opzionalmente una delle tue confezioni di spedizione configurate. Quando impostata, le dimensioni della confezione vengono utilizzate per il calcolo dei costi di spedizione invece del peso e delle dimensioni del prodotto sopra riportati - utile quando un prodotto viene sempre spedito nella stessa scatola standard o busta. Lasciala vuota per utilizzare le caratteristiche fisiche del prodotto. Gestisci le confezioni disponibili sotto **Spedizione > Confezioni**.

### Ordinazione anticipata

Utilizza la scheda **Ordinazione anticipata** per vendere un prodotto prima che abbia alcuna scorta - utile per rilasci imminenti che si desidera iniziare a prendere gli ordini in anticipo rispetto al lancio:

- **È un ordine anticipato** — Abilita per permettere ai clienti di acquistare questo prodotto anche quando non è disponibile a magazzino.
- **Data di rilascio ordinazione anticipata** — La data prevista di disponibilità, mostrata ai clienti.
- **Messaggio ordinazione anticipata** — Un breve messaggio personalizzato mostrato ai clienti, fino a 200 caratteri (es. "Spedizione marzo 2026").

### Identificatori prodotto

Codici prodotto standard per elenchi di mercato e sistemi di magazzino:

- **GTIN** - Numero globale di articolo commerciale
- **EAN** - European Article Number
- **UPC** - Universal Product Code (US)
- **ISBN** - Per i libri
- **ASIN** - Identificatore Amazon
- **MPN** - Numero parte del produttore

### Spedizione internazionale / dogane

Obbligatorio per le spedizioni internazionali (espandi la sezione **Spedizione internazionale / Dogane**):

- **Codice HS** — Codice di classificazione del sistema armonizzato
- **Nazione di origine** — Dove viene prodotto il prodotto
- **Prezzo unitario per dazio** — Valore dichiarato per unità per i dazi
- **Numero della licenza per l'esportazione** — Richiesto solo per articoli controllati o soggetti a restrizioni
- **Scadenza della licenza per l'esportazione** — Data di scadenza della licenza per l'esportazione

## SEO

Ottimizza la visibilità del prodotto sui motori di ricerca.

![Scheda SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Titolo SEO** — Il titolo visualizzato nei risultati del motore di ricerca. Fare clic sull'icona del globo per tradurre.
- **Descrizione SEO** — Una breve descrizione per i risultati della ricerca (massimo 160 caratteri). Fare clic sull'icona del globo per tradurre.
- **Genera automaticamente SEO** — Selezionare per generare automaticamente il contenuto SEO quando il prodotto viene salvato.

Un'anteprima **Risultato della ricerca** in tempo reale mostra esattamente come apparirà il tuo prodotto nei risultati di ricerca di Google.

## Impostazioni della pagina prodotto

Nella **Scheda Avanzate**, la scheda **Impostazioni della pagina prodotto** ti permette di controllare l'aspetto della pagina del prodotto sul negozio:

- **Modello pagina** — Sostituisci il layout predefinito del sito per questo prodotto: Classico, Larghezza intera, Focus sulla galleria, o Digitale. Lascialo impostato su **Usa il layout predefinito del sito** per ereditare il layout specificato nelle tue impostazioni di progettazione — la maggior parte dei prodotti dovrebbe rimanere sul predefinito in modo che i cambiamenti del modello vengano applicati automaticamente.
- **Mostra prodotti correlati** — Visualizza i prodotti correlati in fondo alla pagina.
- **Mostra recensioni** — Visualizza le recensioni dei clienti.
- **Mostra specifiche** — Visualizza la scheda delle specifiche.

Il campo **Tipo di galleria** — che controlla come vengono visualizzate le immagini del prodotto (Galleria standard, Carousel, Layout a griglia, Galleria con zoom, o Visualizzazione 360°) — è impostato separatamente, nella **Scheda Media**.

![Scheda Avanzate che mostra la scheda Impostazioni della pagina prodotto con un elenco a discesa del Modello pagina, e la scheda Dettagli tecnici qui sotto](/static/core/admin/img/help/add-product/advanced-tab.webp)

## Canale di vendita

Il campo **Canale di vendita** (nella sezione Stato) controlla dove il prodotto può essere venduto:

- **Tutti i canali** — Disponibile online e in negozio (Punto Vendita).
- **Solo online** — Non disponibile tramite terminali Punto Vendita.
- **Solo in negozio** — Non elencato online; disponibile solo nel tuo negozio fisico.

Un campo **Codice a barre** è disponibile anche per il controllo del codice a barre del Punto Vendita.

## Salvataggio del prodotto

Quando sei pronto, usa i pulsanti di salvataggio nell'angolo in alto a destra. Il prodotto sarà visibile sul negozio una volta che lo stato è impostato su **Pubblicato**.

## Suggerimenti

- Inizia con lo stato **Bozza** in modo da poter perfezionare il prodotto prima che i clienti lo vedano.
- Carica più immagini — i prodotti con diverse foto hanno un tasso di conversione migliore.
- Compila i campi **SEO** per migliorare la visibilità nei motori di ricerca.
- Usa **Categorie**, **Marchi** e **Tag** per aiutare i clienti a navigare nel tuo catalogo.
- Per i prodotti variabili (es. dimensioni o colori diversi), scegli il tipo **Prodotto variabile** e aggiungi le varianti dopo aver salvato.
- Usa **Caratteristiche** e **Specifiche** per aggiungere dati strutturati sul prodotto che vengono visualizzati in appositi tab sulla pagina del prodotto.
- Se **Richiede spedizione** non rimane selezionato, controlla **Tipo prodotto** — Spwig disattiva automaticamente la spedizione per i prodotti Digitali, Prenotazioni e Buoni Regalo, poiché nessuno di questi viene effettivamente spedito.
- Imposta un **Impacchettamento preferito per la spedizione** per i prodotti che vengono sempre spediti nello stesso scatolone — ti risparmia di dover tenere sincronizzati peso e dimensioni di quel prodotto con quelle della scatola che effettivamente utilizzi.