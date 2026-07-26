---
title: Migrazione da WooCommerce
---

Se il tuo negozio attualmente utilizza WooCommerce, lo strumento di migrazione di Spwig può importare i tuoi prodotti, clienti, ordini e contenuti direttamente tramite l'API REST di WooCommerce. Questa guida copre l'ottenimento delle credenziali API, l'esecuzione dell'importazione e due funzionalità specifiche di WooCommerce di cui è utile essere a conoscenza: il plugin opzionale Migration Bridge per i dati degli affiliati e il supporto integrato per diverse estensioni popolari di WooCommerce.

## Prima di iniziare

WooCommerce ha il supporto più ampio tra tutte le piattaforme di origine nello strumento di migrazione. L'importazione pulita include: categorie (con gerarchia), prodotti, immagini e varianti, clienti e indirizzi, ordini, recensioni, coupon e post del blog con le loro categorie, tag e immagini.

I profili degli affiliati, i registri delle commissioni e la cronologia dei pagamenti possono essere importati anche, ma solo se installi prima il plugin Spwig Migration Bridge — vedi di seguito. Senza di esso, quei dati vengono semplicemente ignorati.

Tieni anche presente:

- I prodotti da certe estensioni di WooCommerce (abbonamenti, pacchetti, prenotazioni, biglietti regalo) vengono inseriti nella funzionalità corrispondente di Spwig, ma non tutti i dettagli vengono trasferiti — vedi **Supporto per le estensioni di WooCommerce** di seguito.
- I campi personalizzati sui tuoi prodotti, clienti e ordini vengono rilevati automaticamente e richiedono una mappatura in un passaggio successivo. Vedi [Mapping dei campi di migrazione](migration-field-mapping).
- Le opzioni **Importa imposte** e **Importa zone e metodi di spedizione** del wizard non vengono applicate ai dati importati. Configura le tasse e le spedizioni in Spwig da solo successivamente — vedi [Dopo la migrazione](after-migration-review).
- L'opzione **Regolazione del prezzo** nello stesso passaggio *sì* ha effetto per le importazioni da WooCommerce, modificando il prezzo base di ogni prodotto mentre viene creato. Lasciala impostata su **Nessuna** a meno che non tu voglia deliberatamente spostare ogni prezzo.

Tieni a portata di mano il login amministratore di WordPress e conosci approssimativamente quanti prodotti, clienti e ordini stai importando in modo da poter verificare i conteggi che il wizard ti mostra.

## Ottenimento delle credenziali API REST

Spwig si connette a WooCommerce utilizzando una chiave API REST generata dal tuo amministratore WordPress. Questa chiave ha bisogno solo di **Lettura** — Spwig legge solo dal tuo negozio durante la migrazione, non scrive mai nulla indietro.

1. In WordPress, vai a **WooCommerce > Impostazioni > Avanzate > API REST**
2. Clicca su **Aggiungi chiave**
3. Dà un nome descrittivo (ad esempio, `Spwig Migration`) e imposta **Permessi** su **Lettura**
4. Clicca su **Genera chiave API**
5. Copia la **Chiave del consumatore** (`ck_...`) e il **Segreto del consumatore** (`cs_...`) in un posto sicuro

> **Importante:** WooCommerce mostra il Segreto del Consumatore solo una volta, al momento in cui lo generi. Se ti allontani prima di copiarlo, dovrai generare una nuova chiave.

## Connessione del tuo negozio

Vai a **Importazione e Esportazione dei Dati > Inizia una nuova migrazione** nell'amministratore di Spwig e seleziona **WooCommerce** nel passaggio 1. Nel passaggio 2, inserisci:

- **URL del negozio** — l'indirizzo web completo del tuo negozio, ad esempio `https://mystore.com`
- **Chiave del consumatore** e **Segreto del consumatore** — i valori che hai appena copiato

Lascia selezionata **Testa la connessione prima di procedere** (predefinita come attiva) in modo che Spwig confermi di poter raggiungere il tuo negozio e autenticarsi prima che tu continui — questo cattura immediatamente errori di battitura e problemi di autorizzazione invece che a metà dell'importazione. Clicca su **Avanti** una volta che ha successo.

## Rivedi e seleziona i dati

Il passaggio 3 estrae i conteggi live dal tuo negozio — categorie, prodotti, clienti, ordini, recensioni e coupon — più un campione dei primi cinque prodotti in modo che tu possa confermare che sta leggendo il sito giusto. Ogni casella di controllo per il tipo di dati è automaticamente selezionata quando il conteggio è superiore a zero e disattivata quando è zero.

**Opzioni di importazione**:

- **Salta gli elementi esistenti** (attivo) — confronta i record in arrivo con quelli già presenti in Spwig (SKU per prodotti, email per clienti) e salta i duplicati.

Lascialo attivo a meno che non stia iniziando da uno store vuoto.
- **Importa immagini dei prodotti** (attivo) — più lento, ma vale la pena.
- **Mantieni gli ID originali quando possibile** (disattivo) — il wizard stesso lo etichetta come "non consigliato". Lascialo disattivo a meno che non tu abbia un motivo tecnico specifico per mantenere gli ID numerici di WooCommerce.
- **Dimensione del lotto** — 10, 25 (predefinito), 50 o 100 record alla volta.

I lotti più piccoli si adattano a connessioni instabili; i lotti più grandi terminano più velocemente su una connessione stabile.

## Il Plugin Spwig Migration Bridge

WooCommerce non ha un concetto predefinito di programma di affiliazione, quindi se gestisci uno attraverso un'estensione di affiliazione di WooCommerce, quei dati vivono in tabelle che l'API REST standard non può vedere. Il **Spwig Migration Bridge** è un piccolo plugin complementare che installi sul tuo sito WordPress per esporlo.

Il plugin Bridge sblocca:

- **Profili di affiliazione** — i dettagli dei tuoi affiliati e i codici di riferimento
- **Registri delle commissioni** — storia delle commissioni associata a ciascun affiliato
- **Storico dei pagamenti** — pagamenti effettuati in precedenza agli affiliati

È completamente opzionale — saltalo se non gestisci un programma di affiliazione o non hai bisogno di quel storico in Spwig.

> **Nota:** I dati degli affiliati possono essere importati solo se gli ordini e i clienti vengono importati nello stesso momento, poiché le commissioni e i pagamenti sono legati a ordini e clienti specifici.

Per installarlo:

1. Nella fase 3, se il plugin non è già rilevato sul tuo sito, vedrai un pulsante **Download Bridge Plugin** con le istruzioni di installazione
2. Scarica il file ZIP del plugin
3. In WordPress, vai a **Plugin > Aggiungi Nuovo > Carica Plugin**, seleziona il file ZIP, fai clic su **Installa Ora**, quindi su **Attiva**
4. Torna al wizard di Spwig e aggiorna la pagina — una casella di controllo **Affiliati** e un blocco **Dati del programma di affiliazione** appariranno, mostrando i conteggi trovati

Puoi disattivare e rimuovere il plugin Bridge da WordPress una volta completata la migrazione.

## Supporto per Estensioni WooCommerce

Se il tuo negozio utilizza certe estensioni popolari, i prodotti che creano vengono riconosciuti durante l'importazione e mappati alla funzione corrispondente di Spwig, invece di essere importati come prodotti normali:

| Estensione WooCommerce | Arriva in |
|---|---|
| Subscriptions | Piani di abbonamento di Spwig |
| Product Add-Ons | Aggiunte al prodotto di Spwig |
| Product Bundles | Pacchetti di prodotto di Spwig |
| Gift Cards (WooCommerce, YITH e PW varianti) | Carte regalo di Spwig |
| Composite Products | Prodotti composti di Spwig |
| Bookings and Accommodation Bookings | Prenotazioni di Spwig |

> **Nota:** L'importazione dei dati delle estensioni non blocca mai la creazione del prodotto sottostante. Se i dati specifici dell'estensione di un prodotto non possono essere letti, il prodotto viene comunque importato — semplicemente come un prodotto normale, senza la sua configurazione di abbonamento, pacchetto, prenotazione o carta regalo.

Controlla casualmente i tuoi prodotti di abbonamento, pacchetto, prenotazione e carta regalo dopo l'importazione per confermare che le impostazioni specifiche dell'estensione siano state trasferite, invece di assumere che un'importazione riuscita abbia portato tutti i dettagli.

## Campi Personalizzati

Se hai aggiunto campi meta personalizzati ai tuoi prodotti, clienti o ordini di WooCommerce, Spwig preleva circa dieci record di ciascun tipo per rilevare quali campi esistono. Mappa ciascuno a un slot di campo personalizzato di Spwig o a un campo generale di Meta Data nella fase 4. Vedi [Mapping dei Campi di Migrazione](migration-field-mapping) per la guida completa, inclusi i modi in cui le mappature vengono salvate per future migrazioni.

## Esecuzione dell'Importazione

Una volta aver riveduto la fase 3 e confermato le tue mappature nella fase 4, inizia l'importazione. Si esegue in background — puoi chiudere la finestra del browser e continua comunque. La fase 5 mostra il progresso in tempo reale con una riga per ogni tipo di dati (categorie, prodotti, clienti, ordini, recensioni, coupon, post del blog e affiliati/commissioni/pagamenti se è stato utilizzato il plugin Bridge) più un registro delle attività espandibile.

La fase 6 mostra i tuoi risultati: cosa è stato importato, saltato o fallito, più uno strumento **Riscrittura dei Link** se sono stati trovati link interni al tuo vecchio dominio di WooCommerce nel contenuto importato.

Rivedi attentamente il riepilogo, quindi procedi con la checklist in [Dopo la tua migrazione](after-migration-review) — copre la verifica dei tuoi dati, l'impostazione delle aliquote fiscali e della spedizione (che il wizard non configura per te) e la riscrittura dei collegamenti interni.

## Revoca la tua chiave API

Una volta confermata la migrazione completata con successo, torna a **WooCommerce > Impostazioni > Avanzate > API REST** in WordPress e revoca o elimina la chiave che hai creato per Spwig. Non c'è motivo per lasciare attiva una chiave API sul tuo vecchio negozio una volta che hai finito con essa.

## Consigli

- **Genera la chiave API proprio prima di averne bisogno** — poiché il Consumer Secret viene visualizzato solo una volta, creala immediatamente prima di iniziare il passaggio 2 invece di farlo in anticipo.
- **Solo la lettura è effettivamente sufficiente** — non concedere mai i permessi di Scrittura o Lettura/Scrittura; Spwig legge solo dal tuo negozio WooCommerce.
- **Installa il plugin Bridge prima di iniziare l'importazione** — avrai bisogno di aggiungerlo e di aggiornare il wizard prima di importare, quindi controllalo in anticipo invece di farlo a metà processo.
- **Controlla manualmente i prodotti supportati da estensioni** — le sottoscrizioni, i pacchetti, le prenotazioni e le carte regalo sono i prodotti più probabili che richiederanno un controllo manuale dopo l'importazione.
- **Un importazione parziale non viene pulita automaticamente** — consulta [Risoluzione dei problemi di migrazione](migration-troubleshooting) prima di riprovare un'importazione fallita.
- **Revoca la chiave API una volta che hai finito** — non lasciare attive integrazioni vecchie su un negozio da cui ti sei migrato.