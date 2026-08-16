---
title: Azioni di stock di massa
---

Oltre alle modifiche singole, Spwig ti offre tre azioni di massa sulla lista **Articoli in magazzino** per i lavori di gestione degli stock che avvengono su molti prodotti contemporaneamente: spostare lo stock tra i magazzini, registrare unità danneggiate o perse, e rilevare lo stock dopo un conteggio fisico. Tutte e tre le azioni vengono eseguite dallo stesso menu a tendina **Azioni**, applicano la stessa quantità a ogni articolo in magazzino che selezioni e vengono registrate pienamente nel registro delle registrazioni degli spostamenti di stock.

Vai a **Prodotti > Articoli in magazzino** per utilizzarle.

## Esecuzione di un'azione di stock di massa

1. Nella lista **Articoli in magazzino**, usa i filtri o la ricerca per trovare gli articoli che desideri aggiornare
2. Seleziona la casella accanto a ciascun articolo in magazzino per includerlo (oppure usa la casella di spunta dell'intestazione per selezionare tutti gli articoli della pagina)
3. Scegli una delle tre azioni dal menu a tendina **Azioni**:
   - **Sposta lo stock nel magazzino**
   - **Registra stock danneggiato/perso**
   - **Ricalcola lo stock (conteggio fisico)**
4. Clicca su **Vai**
5. Controlla la pagina di conferma — elenca ogni articolo in magazzino selezionato con le sue quantità **in magazzino**, **assegnate** e **disponibili**, in modo da poter verificare di aver selezionato gli articoli giusti
6. Compila i campi dell'azione (vedi sotto) e fai clic sul pulsante invia per applicarla

![La lista degli articoli in magazzino con il menu a tendina Azioni aperto, che mostra Sposta lo stock nel magazzino, Registra stock danneggiato/perso e Ricalcola lo stock (conteggio fisico) insieme ad altre azioni](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

La stessa quantità che hai immessoto viene applicata a **ogni** articolo selezionato — questa funzione è progettata per spostare, registrare o ricalcolare lo stesso numero di unità su molti SKU contemporaneamente (ad esempio, spostare 10 unità di diversi prodotti in una nuova posizione del negozio). Per un singolo articolo con una quantità diversa, esegui nuovamente l'azione con solo quell'articolo selezionato, oppure usa **Regola i livelli dello stock** invece.

## Sposta lo stock nel magazzino

Usalo per spostare lo stock disponibile da ciascun articolo selezionato dal proprio magazzino a un altro magazzino — ad esempio, rifornire un nuovo punto vendita dal tuo magazzino principale, o riequilibrare l'inventario tra centri di evasione regionali.

Nella pagina di conferma, compila:

| Campo | Descrizione |
|-------|-------------|
| **Magazzino di destinazione** | Dove lo stock dovrebbe spostarsi. Vengono visualizzati solo i magazzini attivi in questa lista. |
| **Quantità per articolo** | Unità da spostare da ciascun articolo selezionato dal proprio magazzino attuale. |
| **Motivo** | Nota opzionale, ad esempio "Rifornimento nuovo negozio di Auckland". |

Clicca su **Sposta lo stock** per applicare.

![La pagina di conferma Sposta lo stock: un riquadro degli articoli selezionati che elenca tre articoli con i loro valori in magazzino/assegnati/disponibili, e un modulo Dettagli dello spostamento con un magazzino di destinazione, quantità e motivo compilati](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Solo lo stock non riservato può essere spostato.** Spwig effettua lo spostamento dallo stock *disponibile* (in magazzino meno le unità assegnate agli ordini aperti) — le unità già promesse per un ordine del cliente rimangono nel magazzino di origine in modo che l'ordine possa comunque essere evaso. Se un articolo selezionato non ha abbastanza stock disponibile per coprire la quantità immessa, quell'articolo verrà saltato e un messaggio d'errore spiegherà il motivo; la restante selezione verrà comunque spostata.

Se un articolo selezionato è già presente nel magazzino di destinazione scelto, verrà automaticamente saltato (non c'è niente da spostare verso se stesso), e vedrai un messaggio che ti indica quanti articoli sono stati saltati per questo motivo.

Ogni trasferimento scrive un insieme di movimenti abbinati nel registro delle registrazioni — un ingresso negativo **Trasferimento magazzino** alla fonte e uno positivo corrispondente alla destinazione — in modo che l'intero registro mostri esattamente da dove proviene lo stock e dove va.

## Registra stock danneggiato/perso

Usalo per registrare unità che sono rotte, guaste o mancanti — ad esempio, dopo aver trovato prodotti danneggiati in una consegna o investigando una discrepanza.

Nella pagina di conferma, compila:

| Campo | Descrizione |
|-------|-------------|
| **Quantità da scartare (per articolo)** | Unità da rimuovere dal magazzino disponibile per ciascun articolo selezionato. |
| **Motivo** | Nota opzionale, ad esempio "Danno causato dall'acqua durante lo stoccaggio". |

Fai clic su **Registra Scarto** per applicare.

**Lo stock riservato non può essere scartato.** Lo stock disponibile non può mai scendere al di sotto della quantità attualmente allocata agli ordini aperti — Spwig blocca lo scarto per qualsiasi articolo in cui la quantità immessa potrebbe ridurre lo stock riservato, quindi non è possibile accidentalmente lasciare un ordine pagato senza lo stock necessario per soddisfarlo. Se ciò accade per un articolo, vedrai un messaggio d'errore che indica l'articolo e quanti unità non riservate effettivamente disponibili per lo scarto.

Ogni scarto viene registrato come movimento **Danneggiato/Perso** per quell'articolo, con una quantità negativa.

## Ricalcolo dello stock (conteggio fisico)

Usalo dopo un conteggio fisico dello stock per correggere le quantità disponibili in modo che corrispondano a quelle che hai effettivamente contato — il modo più veloce per riconciliare molti articoli dopo un'ispezione del magazzino o un conteggio ciclico.

Nella pagina di conferma, compila:

| Campo | Descrizione |
|-------|-------------|
| **Quantità disponibile conteggiata (per articolo)** | La quantità che hai contato fisicamente. Lo stock disponibile viene impostato su questo numero esatto per ogni articolo selezionato — non aggiunto né sottratto. |
| **Motivo** | Nota opzionale, ad esempio "Conteggio dello stock del magazzino del terzo trimestre". |

Fai clic su **Applica Ricalcolo** per applicare.

![La pagina di conferma Ricalcolo dello stock: il riquadro degli articoli selezionati e un modulo Dettagli Ricalcolo con la quantità disponibile conteggiata e un motivo compilati](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

A differenza delle altre due azioni, il ricalcolo può spostare lo stock in entrambe le direzioni — in alto se hai contato di più di quanto il sistema si aspettasse, in basso se hai contato di meno. Se il conteggio che immetti è inferiore alla quantità attualmente allocata agli ordini aperti, Spwig comunque lo applica (un conteggio è un fatto, non qualcosa con cui dibattere), ma la figura **Disponibile** di quell'articolo mostrerà `0` nella lista degli stock e l'icona di stato si trasformerà in "Esaurito" — trattalo come un segnale per controllare se gli ordini interessati possono ancora essere soddisfatti.

Ogni ricalcolo viene registrato come movimento **Conteggio Fisico**, con la quantità che mostra la correzione (positiva o negativa) tra le vecchie e le nuove quantità disponibili.

## Verifica di ciò che è cambiato

Ogni trasferimento, scarto e ricalcolo viene registrato nello stesso modo di qualsiasi altra modifica allo stock:

- Apri un articolo e scorri verso il basso verso la sezione **Movimenti dello stock** per vedere la sua intera cronologia
- Oppure naviga su **Prodotti > Movimenti dello stock** per esaminare i movimenti su tutti gli articoli, filtrabili per tipo

Ogni voce registra il tipo di movimento, la variazione della quantità, il vecchio e il nuovo importo disponibile, chi ha effettuato la modifica e il motivo che hai immessoo (se presente) — quindi un trasferimento di massa o uno scarto è altrettanto tracciabile di un'aggiustamento manuale singolo.

## Suggerimenti

- Esegui **Ricalcola lo stock** subito dopo un conteggio fisico mentre i numeri conteggiati sono freschi — è più facile individuare un errore di battitura nella pagina di conferma che cercare di risolverlo in seguito nella cronologia dei movimenti.
- Compila sempre **Motivo** per gli scarti e i ricalcoli. Fra sei mesi, "Danno causato dall'acqua durante lo stoccaggio" è molto più utile nel percorso di audit rispetto a un campo vuoto.
- Prima di trasferire lo stock, controlla la colonna **Disponibile** nella pagina di conferma — già tiene conto delle unità allocate, quindi saprai immediatamente se una quantità è troppo alta per uno degli articoli selezionati.
- Queste azioni applicano la stessa quantità a ogni articolo selezionato. Raggruppa la selezione per articoli che necessitano veramente della stessa quantità spostata, scartata o ricalcolata, e gestisci le eccezioni uno per uno.
- Se usi il POS in un punto vendita al dettaglio, ricorda che il buffer dello stock del magazzino non è incluso nella "disponibilità" per gli ordini online — ma i trasferimenti di massa e gli scarti funzionano comunque rispetto al totale reale dello stock disponibile del magazzino.