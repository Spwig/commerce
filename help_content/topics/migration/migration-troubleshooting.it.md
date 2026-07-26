---
title: Risoluzione dei problemi durante la migrazione
---

La maggior parte delle migrazioni si completa senza problemi, ma possono verificarsi errori di connessione, timeout durante gli import, e occasionalmente un processo può fermarsi a metà. Questo argomento tratta la diagnostica di una connessione fallita, la lettura del registro dei progressi durante un import, e - soprattutto - le reali opzioni disponibili una volta che qualcosa va storto, incluso ciò che fanno realmente Retry, Cancel e Rollback.

## Errori di connessione allo step 2

La casella di controllo **Test connection before proceeding** è attiva di default e costituisce il primo strumento diagnostico - verifica le credenziali rispetto alla piattaforma di origine prima di procedere con il resto del wizard. Se fallisce, il messaggio di errore indica di solito uno di questi:

- **WooCommerce** - URL del negozio mancante di `https://` o con un segmento di percorso finale; una chiave/segreto del consumatore sbagliata o rigenerata; o una chiave API REST creata senza il permesso **Read** in **WooCommerce > Settings > Advanced > REST API**.
- **Shopify** - Dominio del negozio non nel formato `yourstore.myshopify.com`; ID/segreto client da un'app errata; o, più comunemente, un'app creata nel Dev Dashboard ma mai effettivamente **installata** - creare una versione dell'app non basta, hai bisogno del link di distribuzione personalizzato e di un clic su **Install**. Spwig emette anche un avviso se `read_products`, `read_customers` o `read_orders` non sono inclusi nei permessi dell'app.
- **Magento 2** - URL del negozio che punta al negozio fisico invece che alla radice dell'API, o un token di integrazione creato ma mai attivato (**Save > Activate > Allow**).
- **Problemi SSL** - un certificato scaduto, auto-firmato o mal configurato fallisce la connessione prima che vengano verificate le credenziali, mostrando un errore generico invece che uno di autenticazione. Se le credenziali sembrano corrette, controlla successivamente il certificato.

Ri-esegui il test di connessione dopo ogni correzione, invece di modificare diverse credenziali contemporaneamente - ciò isola quale fosse errata.

## Lettura del registro live allo step 5

Durante un import, lo step 5 mostra un registro dell'attività mentre avviene. Clicca su **Show Details** per espanderlo in voci individuali - livello e messaggio - invece che solo il riepilogo dello step corrente. Questo è il modo più rapido per vedere cosa sta accadendo se il progresso sembra bloccato: una serie di voci "skipped" per un tipo di dati indica solitamente che "Skip existing items" funziona come previsto, non che qualcosa sia bloccato.

La visualizzazione del registro mostra solo le **ultime 500 voci**, quindi su una migrazione di grandi dimensioni, le voci più vecchie scorreranno fuori dal campo visivo mentre l'import continua. Se hai bisogno del registro completo una volta che un tipo di dati è finito, usa **Download Logs** sulla pagina dei risultati invece - non ha limiti di questo tipo.

## Cosa significa effettivamente una migrazione fallita

Questo è il punto più importante da comprendere se una migrazione fallisce.

Quando una migrazione fallisce, la pagina di completamento ti dice chiaramente cosa è successo: gli elementi importati prima dell'errore sono ancora nel tuo negozio, nulla è stato rimosso automaticamente, e correggere il problema e rieseguire l'import salterà tutto ciò che era già stato importato la prima volta. Prendilo alla lettera. Nessun passaggio dell'import viene eseguito all'interno di una transazione del database che potrebbe essere annullata come unità — qualsiasi cosa sia stata importata con successo prima del punto di fallimento, prodotti, categorie, clienti, ordini, qualunque cosa l'incarico sia riuscito a completare, rimane nel tuo negozio esattamente come creato. Una migrazione fallita è una migrazione **parziale**, non una che è stata annullata.

Il fallimento marca anche l'incarico come non annullabile, quindi il pulsante **Rollback** non sarà disponibile su un **import** fallito - appare solo una volta che una migrazione è completata, o se un rollback di una migrazione completata è fallito a metà, in tal caso Spwig offre nuovamente il pulsante in modo da poter riprovare. L'unica situazione in cui vorresti un annullamento automatico - un import fallito - è esattamente la situazione in cui il pulsante non è disponibile.

Quindi, quando una migrazione fallisce:

1. **Rivedi cosa è effettivamente stato importato**, utilizzando i conteggi Importati/Skipped/Failed e i log scaricati per costruire un'immagine di ciò che è presente nel tuo negozio rispetto a ciò che non è riuscito.

2. **Decidi come pulire.** Per una piccola quantità di dati parziali, rivedi manualmente i dati e cancella ciò che non desideri tramite le normali visualizzazioni della lista dell'amministratore.

Per un'importazione parziale più grande o disordinata, spesso è più veloce cancellare i dati importati da soli prima di iniziare da capo, piuttosto che riconciliarli uno per uno.

3. **Ri-esegui con Skip existing items abilitato**, indipendentemente dal percorso di pulizia scelto — è ciò che impedisce ai dati che hanno superato l'importazione di essere duplicati nel prossimo tentativo.

## Riprova

**Riprova** riavvia completamente l'importazione dall'inizio. Cancella i contatori e i log precedenti del lavoro e riimporta tutto da zero — **non** continua da dove l'ultimo tentativo è fallito. Mantieni **Skip existing items** abilitato in modo che gli elementi già importati nel primo tentativo non vengano duplicati nel secondo passaggio.

Se una migrazione si ferma perché ha raggiunto il **limite di 4 ore**, il messaggio che vedrai è accurato: eseguire nuovamente l'importazione inizia dall'inizio e salta gli elementi già importati, non è un riprendere da dove si era fermati. Per un negozio abbastanza grande da raggiungere il limite di tempo, riprovare l'intero processo ripetutamente raramente termina; invece, riduci l'ambito di ogni esecuzione selezionando meno tipi di dati nel passaggio 3 (prodotti in un'esecuzione, ordini in un'altra) e fai diversi passaggi più piccoli.

## Annulla

**Annulla** è disponibile su una migrazione in corso, e segna immediatamente il lavoro come fallito nel dashboard. **Non** ferma il compito di importazione in background, che continua a eseguirsi e a scrivere i dati fino a raggiungere un punto di arresto naturale. Prevedi che i conteggi importati continueranno a salire per un po' dopo aver annullato — lascia che si stabilizzino prima di decidere cosa pulire, invece di agire sui conteggi catturati nel momento in cui hai cliccato Annulla.

## Non esiste una pausa o un riprendere

Spwig non supporta l'interruzione di una migrazione in corso e il riprendere più tardi. Il pulsante **Riprendi** nel dashboard è per un caso diverso: una migrazione configurata tramite il wizard ma mai avviata. Reapre il wizard da dove ti eri fermato nella configurazione — non è correlato a un'esecuzione già in corso.

## Rollback

> **Avviso:** Il rollback è un'azione permanente e distruttiva. Leggi interamente questa sezione prima di utilizzarla.

Il rollback è disponibile su una **migrazione completata**, e nuovamente su una in cui il rollback precedente ha fallito parzialmente (stato **Rollback Failed**), quindi un rollback bloccato può essere riprovato. Rimuove solo ciò che l'importazione stessa ha creato, e mantiene qualsiasi cosa su cui il tuo negozio ora dipende:

- Un cliente migrato che ha effettuato un ordine reale dopo l'importazione è **mantenuto** — il loro account, gli indirizzi, la storia della fedeltà e il credito del negozio rimangono con loro, e quell'ordine reale rimane intatto. Solo gli ordini creati dall'importazione vengono rimossi.
- Un prodotto migrato che è ancora riferito da qualsiasi ordine, bundle, carta regalo o slot di configurazione è **mantenuto**. Gli ordini appartenenti ad altri clienti non vengono mai modificati — il rollback non può più rimuovere gli elementi di un ordine non correlato o lasciarlo con un totale errato.
- Quello che viene mantenuto ti viene riferito con il nome e il conteggio, con la ragione — ad esempio "1 Prodotto mantenuto, ancora riferito da un elemento dell'ordine" — in modo da sapere esattamente cosa è ancora presente e il motivo.
- Affiliati, commissioni e pagamenti creati dall'importazione **vengono rimossi**, insieme a qualsiasi account affiliato creato dall'importazione. Un affiliato collegato a un cliente che esisteva già mantiene il loro account; solo il record dell'affiliato viene rimosso.
- La storia della fedeltà e il credito del negozio seguono il cliente: vengono rimossi se il cliente viene rimosso, mantenuti se il cliente viene mantenuto.

Non rimuove comunque i piani di abbonamento, i livelli di prezzo o le risorse di prenotazione creati dalle estensioni del negozio — questi sopravvivono a un rollback e devono essere puliti manualmente se non li desideri.

Prima di confermare, la pagina di conferma mostra un'anteprima di esattamente cosa verrà rimosso e cosa verrà mantenuto, calcolato rispetto ai tuoi dati live — leggila prima di cliccare **Yes, Rollback Migration**.

Il rollback viene poi eseguito in background invece che nel tuo browser, quindi è sicuro chiudere la scheda; controlla lo stato della migrazione per il rapporto su ciò che è effettivamente stato rimosso e mantenuto una volta completato.

Poiché il rollback non va oltre ciò che l'import ha creato, non è più uno strumento disponibile solo per lo stesso giorno — gli ordini reali di un cliente migrato e le vendite reali di un prodotto migrato sono protetti indipendentemente dal tempo trascorso dalla migrazione. È comunque un'azione permanente e distruttiva per le righe che rimuove, quindi utilizzalo con attenzione e non in modo casuale, e pulisci manualmente qualsiasi elemento che Spwig mantiene ma non desideri realmente.

Per la disponibilità: il pulsante Rollback rimane visibile nella panoramica di una migrazione completata fintanto che il record del lavoro esiste — per la maggior parte delle piattaforme non c'è un termine fissato. Magento è l'eccezione e perde la disponibilità di rollback dopo una finestra predefinita, quindi decidi rapidamente se stai utilizzando Magento. I record dei lavori non vengono rimossi in base a un programma, quindi una migrazione rimane annullabile indefinitamente a meno che non elimini tu stesso il suo record.

## Strategia per grandi negozi e import lenti

Per un negozio abbastanza grande che rischia il limite di 4 ore in un'unica esecuzione:

- **Aumenta la dimensione del lotto** nel passo 3 (fino a 100) — i lotti più grandi significano in genere meno viaggi di andata e ritorno e un throughput più veloce.
- **Dividi la migrazione in più esecuzioni per tipo di dati** — categorie e prodotti in un'esecuzione, clienti e ordini in un'esecuzione successiva, invece di tutto insieme.
- **Mantieni attivo Skip existing items** per ogni esecuzione successiva alla prima, in modo che le esecuzioni ripetute non duplichino ciò che è già stato completato con successo.
- **Disattiva Importa immagini dei prodotti.** Il download e l'elaborazione di ogni immagine è di solito il fattore più grande che influisce su un'esecuzione lenta. Puoi aggiungere le immagini ai prodotti singolarmente, o tramite un import CSV separato, una volta che il resto dei dati è stato inserito.

## Consigli

- **Testa la connessione dopo ogni modifica delle credenziali**, non una volta sola alla fine — isola il valore errato.
- **Non assumere mai che un lavoro fallito abbia pulito da solo** — controlla esattamente cosa è presente nel tuo negozio prima di decidere una pulizia o un nuovo tentativo.
- **Mantieni attivo Skip existing items per ogni ripetizione** — è l'unica cosa che impedisce i duplicati in un secondo passaggio.
- **Non combatti il limite di 4 ore con più ripetizioni** — dividi per tipo di dati invece.
- **Leggi l'anteprima del rollback prima di confermare** — indica esattamente cosa verrà rimosso e cosa verrà mantenuto, calcolato rispetto ai tuoi dati live, quindi non ci saranno sorprese.