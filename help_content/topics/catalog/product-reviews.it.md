---
title: Recensioni dei prodotti
---

Le recensioni dei prodotti consentono ai clienti di valutare e scrivere del loro esperienza con un prodotto. Le recensioni che approvi appariranno sulla pagina del prodotto nel tuo negozio, dove aiutano altri acquirenti a decidere cosa acquistare. Spwig ti dà pieno controllo su quali recensioni vengano pubblicate: nulla viene pubblicato fino a quando non le approvi.

Le recensioni si trovano sotto **Prodotti > Recensioni** nella barra laterale, che si apre come un gruppo: il collegamento in alto ti porta alla **Dashboard delle recensioni**, e **Moderare le recensioni** ti porta direttamente all'elenco delle recensioni.

## La dashboard delle recensioni

Vai a **Prodotti > Recensioni** per aprire la dashboard - un'anteprima su uno schermo di come le recensioni si stanno comportando in tutto il tuo negozio.

![Dashboard delle recensioni](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

In cima, sei schede KPI riassumono le tue attività di recensione:

| Scheda | Cosa mostra |
|---|---|
| **Totale recensioni** | Tutte le recensioni mai inviate, approvate o meno |
| **Voto medio** | La media dei punteggi delle recensioni |
| **In attesa di moderazione** | Recensioni in attesa del tuo approvazione o rifiuto |
| **Tasso di approvazione** | La percentuale di tutte le recensioni che hai approvato |
| **Acquisti verificati** | La percentuale di recensioni lasciate da clienti con un ordine confermato per quel prodotto |
| **Nuove (30 giorni)** | Recensioni inviate negli ultimi 30 giorni |

Sotto i KPI, tre grafici forniscono dettagli in più:

- **Distribuzione dei voti** - un grafico a barre di quante recensioni cadono in ciascun voto (1-5). Un gruppo di recensioni a 1 stella qui va indagato immediatamente.
- **Volume delle recensioni (12 settimane)** - un grafico a linee dei conteggi delle recensioni settimanali, in modo da poter individuare picchi dopo una promozione o un calo che necessita di attenzione.
- **Canale di acquisto dei recensori** - un grafico a ciambella del canale di marketing (diretto, email, ricerca pagata, social organico, e così via) che ha portato all'**acquisto** dietro ogni recensione. Questo riascolta i tuoi dati di attribuzione e è veramente utile per vedere quali canali portano clienti che poi lasciano recensioni - ma non è un registro di come il cliente abbia trovato la forma delle recensioni stessa. Spwig non ne tiene traccia separatamente; consulta 

Nella scheda **Recensione**, seleziona o deseleziona **Approvato**
3.

Fai clic sul pulsante con il segno di spunta nell'intestazione per salvare

## Pagina modifica recensione

Aprire una recensione ti dà una visualizzazione a dashboard incentrata su quella recensione: un'intestazione con il nome del prodotto, la valutazione a stelle, un badge **Approvato**/**In attesa di approvazione**, un badge **Acquisto verificato** quando è applicabile, chi ha scritto la recensione e quando, e una riga di statistiche (**Valutazione**, **Voti utili**, **Ordini clienti**, **Spesa complessiva**). Qui sotto, i dettagli sono organizzati in quattro schede.

![Pagina modifica recensione - Scheda Recensione con galleria immagini](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Scheda Recensione

Ecco dove moderi la recensione stessa:

- **Immagine della recensione** - se il cliente ha allegato foto, vengono visualizzate qui come galleria di anteprime; fai clic su qualsiasi anteprima per aprire l'immagine a dimensione intera in un'altra scheda. Le recensioni con foto sono un segnale di fiducia forte per gli acquirenti, quindi è bene dare un'occhiata prima di approvare.
- **Valutazione**, **Titolo**, **Commento** - il contenuto inviato dal cliente
- **Approvato** - controlla se la recensione è visibile sul tuo negozio
- **Acquisto verificato** - segnala la recensione come proveniente da un acquirente confermato; Spwig lo imposta automaticamente quando esiste un ordine completato per il prodotto (vedi la **Scheda Acquisto**), ma puoi sovrascriverlo qui se necessario
- **Immagine** - l'elenco sottostante delle URL delle immagini dietro la galleria sopra; di solito non hai bisogno di modificarlo, ma rimane modificabile per casi eccezionali (ad esempio, rimozione di una foto da una recensione con più immagini)

Non puoi modificare la parola della recensione - approvare o rifiutare, e gestire le immagini, è l'estensione di ciò che controlli qui.

### Scheda Cliente e Percorso

![Pagina modifica recensione - Scheda Cliente e Percorso](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Questa scheda ti dà contesto su chi ha lasciato la recensione: ordini totali, quanti recensioni ha scritto, la sua valutazione media data, quanto tempo è stato cliente, e i suoi dati di contatto, con un collegamento per aprire il record completo del cliente.

Sotto vi è il **percorso del traffico** - i canali, le campagne e i riferimenti che hanno portato questo cliente nel tuo negozio, estratti dai dati di attribuzione e visualizzati come un arco temporale.

#### Cosa fa e non fa la "traccia"

Leggi questo arco temporale come il **percorso di arrivo e acquisto** del cliente - come ha trovato inizialmente il tuo negozio e ha proseguito con l'acquisto. Non è un elenco del momento in cui il cliente ha effettuato l'accesso, o quale dispositivo o sessione abbia utilizzato, al momento in cui ha inviato la recensione. Se l'arco temporale mostra "Email > skincare estiva" tre settimane prima della data della recensione, ciò indica che la campagna email ha probabilmente guidato l'acquisto - non dice nulla su se il cliente è tornato da un risultato di ricerca, da un segnalibro o da una email di follow-up per lasciare effettivamente la recensione. Tratta questa scheda come contesto di marketing utile, non come traccia letterale del momento di invio della recensione.

### Scheda Acquisto

![Pagina modifica recensione - Scheda Acquisto](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

Questa scheda elenca ogni ordine in cui il cliente ha acquistato il prodotto recensito - numero d'ordine, data, totale, stato e canale d'acquisto per quell'ordine. Se uno di questi ordini ha raggiunto uno stato completato (spedito o consegnato), vedrai un notifica di conferma che si tratta di un acquisto verificato - lo stesso segnale che imposta automaticamente **Acquisto verificato** nella scheda Recensione.

Se non appare alcun ordine corrispondente qui, il revisore ha acquistato il prodotto prima che il tuo negozio tracciasse gli ordini in Spwig, oppure non ha mai effettivamente acquistato il prodotto - da sapere prima di decidere quanto peso dare alla recensione.

### Scheda Avanzata

Metadati che raramente hai bisogno di modificare: **Conteggio utile** (quanti clienti hanno segnalato la recensione come utile), origine di importazione se la recensione è stata migrata da un altro sito, e le date di creazione/aggiornamento.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi immagini, i blocchi di codice e i termini tecnici.

- Controlla per primo l'elenco **In attesa di moderazione** sulla dashboard — è il modo più veloce per vedere cosa richiede una decisione senza aprire l'elenco completo delle recensioni
- Un insieme di recensioni a 1 punto sullo stesso prodotto nel grafico **Distribuzione dei voti** è un segnale chiaro per indagare sulle confezioni, la qualità del prodotto o la descrizione del listino
- Usa il filtro **Verificato** quando decidi come gestire le recensioni borderline — i feedback dei clienti con un ordine confermato hanno più peso in qualsiasi controversia
- Approva le recensioni tempestivamente, comprese quelle critiche — una recensione negativa visibile senza risposta può sembrare peggiore di un reclamo gestito, e le recensioni che compaiono con ritardo scoraggiano i clienti dal lasciare feedback futuro
- Non leggere troppo il percorso **Fonte del traffico** o il grafico **Canale di acquisto dei recensori** della dashboard — entrambi descrivono come il cliente è arrivato e ha acquistato, non come è arrivato per scrivere la recensione
- Le recensioni con foto meritano un'attenzione maggiore prima dell'approvazione; le foto del prodotto da parte dei clienti veri sono alcuni dei contenuti più persuasivi sul tuo negozio