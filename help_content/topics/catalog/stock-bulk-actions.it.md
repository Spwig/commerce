---
title: Azioni di stock di massa
---

Oltre alle modifiche singole, Spwig ti offre tre azioni di massa sulla lista **Articoli di magazzino** per i lavori di gestione del magazzino che avvengono su molti prodotti contemporaneamente: spostare lo stock tra i magazzini, registrare unità danneggiate o perse, e rilevare lo stock dopo un conteggio fisico. Tutte e tre le azioni vengono eseguite dallo stesso menu a tendina **Azioni**, applicano la stessa quantità a ogni articolo di magazzino selezionato e vengono registrate completamente nel registro delle registrazioni di movimento dello stock.

Vai a **Prodotti > Articoli di magazzino** per utilizzarle.

## Esecuzione di un'azione di stock di massa

1. Nella lista **Articoli di magazzino**, usa i filtri o la ricerca per trovare gli articoli che desideri aggiornare
2. Seleziona la casella accanto a ciascun articolo di magazzino per includerlo (oppure usa la casella di spunta dell'intestazione per selezionare tutti gli articoli della pagina)
3. Scegli una delle tre azioni dal menu a tendina **Azioni**:
   - **Sposta lo stock nel magazzino**
   - **Registra lo stock danneggiato/perso**
   - **Ricalcola lo stock (conteggio fisico)**
4. Fai clic su **Vai**
5. Controlla la pagina di conferma — elenca ogni articolo di magazzino selezionato con le sue quantità **sul banco**, **allocate** e **disponibili**, in modo da poter verificare di aver selezionato gli articoli giusti
6. Compila i campi dell'azione (vedi sotto) e fai clic sul pulsante invia per applicarla

![La lista degli articoli di magazzino con il menu a tendina Azioni aperto, che mostra Sposta lo stock nel magazzino, Registra lo stock danneggiato/perso e Ricalcola lo stock (conteggio fisico) insieme ad altre azioni](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

La stessa quantità che hai immessoto viene applicata a **ogni** articolo selezionato — questa funzione è progettata per spostare, registrare o ricalcolare lo stesso numero di unità su molti SKU contemporaneamente (ad esempio, spostare 10 unità di diversi prodotti in una nuova posizione del negozio). Per un singolo articolo con una quantità diversa, esegui nuovamente l'azione con solo quell'articolo selezionato, oppure usa **Regola i livelli dello stock** invece.

## Sposta lo stock nel magazzino

Usa questa funzione per spostare lo stock disponibile da ciascun articolo selezionato nel proprio magazzino in un altro magazzino — ad esempio, rifornire un nuovo punto vendita dal tuo magazzino principale, o riequilibrare l'inventario tra i centri di evasione regionali.

Nella pagina di conferma, compila:

| Campo | Descrizione |
|-------|-------------|
| **Magazzino di destinazione** | Dove lo stock dovrebbe spostarsi. Vengono visualizzati solo i magazzini attivi in questa lista. |
| **Quantità per articolo** | Unità da spostare da ciascun articolo selezionato dal proprio magazzino attuale. |
| **Motivo** | Nota opzionale, ad esempio "Rifornimento del nuovo negozio di Auckland". |

Fai clic su **Sposta lo stock** per applicare.

![La pagina di conferma Sposta lo stock: un riquadro degli articoli selezionati che elenca tre articoli con i loro valori sul banco/allocati/disponibili, e un modulo Dettagli dello spostamento con un magazzino di destinazione, quantità e motivo compilati](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Solo lo stock non riservato può essere spostato.** Spwig effettua lo spostamento dallo stock *disponibile* (sul banco meno le unità allocate per gli ordini aperti) — le unità già promesse per un ordine del cliente rimangono nel magazzino di origine in modo che l'ordine possa comunque essere evaso. Se un articolo selezionato non ha abbastanza stock disponibile per coprire la quantità immessa, quell'articolo viene saltato e un messaggio d'errore spiega il motivo; la restante selezione viene comunque spostata.

Se un articolo selezionato è già presente nel magazzino di destinazione scelto, viene automaticamente saltato (non c'è niente da spostare verso se stesso), e vedrai un messaggio che ti indica quanti articoli sono stati saltati per questo motivo.

Ogni trasferimento scrive un insieme di movimenti abbinati nel registro delle registrazioni — un ingresso negativo **Trasferimento magazzino** alla fonte e uno positivo corrispondente alla destinazione — in modo che l'intero registro mostri esattamente da dove proviene lo stock e dove va.

## Registra lo stock danneggiato/perso

Usa questa funzione per registrare unità che sono rotte, guaste o mancanti — ad esempio, dopo aver trovato merci danneggiate in una consegna o investigando una discrepanza.

Nella pagina di conferma, compila:

| Campo | Descrizione |
|-------|-------------|
| **Quantità da scorporare (per articolo)** | Unità da rimuovere dal magazzino disponibile per ciascun articolo selezionato. |
| **Motivo** | Nota opzionale, ad esempio "danni da acqua durante lo stoccaggio". |

Fare clic su **Registra Scorporo** per applicare.

**Lo stock riservato non può essere scorporato.** Lo stock disponibile non può mai scendere al di sotto della quantità attualmente allocata agli ordini aperti — Spwig blocca lo scorporo per qualsiasi articolo in cui la quantità immessa potrebbe ridurre lo stock riservato, quindi non è possibile accidentalmente lasciare un ordine pagato senza lo stock necessario per soddisfarlo. Se ciò accade per un articolo, vedrai un messaggio d'errore che nomina l'articolo e indica quanti unità non riservate effettivamente disponibili per scorporare.

Ogni scorporo viene registrato come movimento **Danni/Persi** per quell'articolo, con una quantità negativa.

## Ricalcolo dello stock (conteggio fisico)

Utilizzalo dopo un conteggio fisico dello stock per correggere le quantità disponibili in modo che corrispondano a quelle che hai effettivamente contato — il modo più veloce per riconciliare molti articoli dopo un'ispezione del magazzino o un conteggio ciclico.

Nella pagina di conferma, compilare:

| Campo | Descrizione |
|-------|-------------|
| **Quantità disponibile conteggiata (per articolo)** | La quantità che hai contato fisicamente. Lo stock disponibile viene impostato su questo numero esatto per ogni articolo selezionato — non aggiunto né sottratto. |
| **Motivo** | Nota opzionale, ad esempio "conteggio dello stock del terzo trimestre". |

Fare clic su **Applica Ricalcolo** per applicare.

![La pagina di conferma Ricalcolo Stock: il riquadro degli Articoli selezionati e un modulo Dettagli Ricalcolo con la quantità disponibile conteggiata e un motivo compilati](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

A differenza delle altre due azioni, il ricalcolo può spostare lo stock in entrambe le direzioni — in alto se hai contato di più di quanto il sistema si aspettasse, in basso se hai contato di meno. Se il conteggio che immetti è inferiore alla quantità attualmente allocata agli ordini aperti, Spwig comunque lo applicherbbe (un conteggio è un fatto, non qualcosa con cui dibattere), ma la figura **Disponibile** di quell'articolo mostrerebbe `0` nella lista stock e il suo icona di stato si capovolgerà in Esaurito — trattalo come un segnale per verificare se gli ordini interessati possono ancora essere soddisfatti.

Ogni ricalcolo viene registrato come movimento **Conteggio Fisico**, con la quantità che mostra la correzione (positiva o negativa) tra le vecchie e le nuove quantità disponibili.

## Verifica di ciò che è cambiato

Ogni trasferimento, scorporo e ricalcolo viene registrato nello stesso modo di qualsiasi altra modifica allo stock:

- Apri un articolo e scorri verso il basso verso la sezione **Movimenti Stock** per vedere la sua cronologia completa
- Oppure naviga su **Prodotti > Movimenti Stock** per esaminare i movimenti su tutti gli articoli, filtrabili per tipo

Ogni voce registra il tipo di movimento, la variazione della quantità, il vecchio e il nuovo importo disponibile, chi ha effettuato la modifica e il motivo che hai immesso (se presente) — quindi un trasferimento di massa o uno scorporo è altrettanto tracciabile di un'aggiustamento manuale singolo.

## Suggerimenti

- Esegui **Ricalcolo Stock** subito dopo un conteggio fisico mentre i numeri conteggiati sono freschi — è più facile individuare un errore di battitura nella pagina di conferma che cercare di risolverlo in seguito nella cronologia dei movimenti.
- Compila sempre **Motivo** per gli scorpori e i ricalcoli. Fra sei mesi, "danni da acqua durante lo stoccaggio" è molto più utile nel percorso di controllo rispetto a un campo vuoto.
- Prima di trasferire lo stock, controlla la colonna **Disponibile** nella pagina di conferma — già tiene conto delle unità allocate, quindi saprai immediatamente se una quantità è troppo alta per uno degli articoli selezionati.
- Queste azioni applicano la stessa quantità a ogni articolo selezionato. Raggruppa la selezione per articoli che necessitano veramente della stessa quantità spostata, scorporata o ricalcolata, e gestisci le eccezioni uno per volta.
- Se utilizzi un punto vendita al dettaglio, ricorda che il buffer dello stock del magazzino non è incluso nella "disponibilità" per gli ordini online — ma i trasferimenti di massa e gli scorpori funzionano comunque rispetto al totale reale disponibile del magazzino.