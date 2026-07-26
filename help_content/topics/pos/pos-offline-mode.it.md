---
title: Modalità offline POS & Installazione App
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA in stato inattivo — vista principale per la selezione login/terminali che mostra il branding Spwig POS
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Screenshot di Add-to-Home-Screen (iPad Safari, Android Chrome) sono specifici del sistema operativo/navigatore.
         Screenshot di riferimento annotate. La sessione che cattura questa schermata dovrebbe utilizzare l'emulazione del dispositivo
         o immagini di riferimento invece di tentare di attivare il prompt di installazione del browser.
-->

Il POS Spwig è un'app Web Progressiva (PWA). Funziona interamente nel browser e può essere installata sullo schermo iniziale del dispositivo come un'app nativa. Poiché l'app, il tuo catalogo dei prodotti e la cronologia degli ordini recenti vengono memorizzati localmente sul dispositivo, il tuo registratore di cassa continua a funzionare anche in caso di brevi interruzioni di rete o connessioni lente.

Questo argomento spiega esattamente cosa funziona quando la connessione si interrompe, come vengono riconciliate le vendite in coda quando la connessione torna, come installare il POS sullo schermo iniziale di un dispositivo e come vengono inviati gli aggiornamenti ai dispositivi installati.

## Funzionamento della modalità offline

Quando apri per la prima volta il POS su un dispositivo, il browser scarica e memorizza localmente l'intera app — l'interfaccia, le immagini e tutto il codice di supporto. Un componente in background chiamato Service Worker gestisce questa cache. Da quel momento in poi, l'app si carica dalla cache locale anche se il server non è raggiungibile.

Oltre alla cache dell'app, il POS mantiene un database locale sul dispositivo (utilizzando lo storage IndexedDB integrato del browser). Questo database contiene:

- **Prodotti e varianti** — sincronizzati dal tuo catalogo e aggiornati ogni cinque minuti quando si è online
- **Categorie** — sincronizzate all'avvio e aggiornate insieme ai prodotti
- **Livelli di inventario** — sincronizzati ogni due minuti quando si è online (utilizzando una strategia di rete-first che si basa sui dati memorizzati localmente se il server non risponde entro tre secondi)
- **Record dei clienti** — fino a 1.000 clienti recenti
- **Cronologia degli ordini** — un numero configurabile di ordini recenti del POS (predefinito: 500 ordini negli ultimi 14 giorni; impostabile per terminale in **POS > POS Terminals**)
- **Immagini dei prodotti** — memorizzate localmente per un massimo di 24 ore

Quando il POS rileva che il dispositivo è offline, compare un banner in alto nello schermo: **"Modalità offline - Le vendite verranno sincronizzate quando la connessione verrà ripristinata."** Il registratore di cassa continua a funzionare utilizzando i dati memorizzati localmente.

## Funzionalità disponibili in modalità offline

| Funzionalità | Disponibilità offline |
|---------|---------------------|
| Ricerca e navigazione dei prodotti | Disponibile — utilizza il catalogo memorizzato localmente |
| Scansione del codice a barre | Disponibile — le scansione cercano i prodotti nella cache locale |
| Aggiunta di articoli al carrello | Disponibile |
| Applicazione di sconti manuali | Disponibile |
| Applicazione di codici voucher | Non disponibile — il controllo del saldo richiede una connessione attiva |
| Pagamenti in contanti | Disponibile — registrati localmente e in coda per la sincronizzazione |
| Pagamenti con carta (inserimento manuale) | Disponibile — il cassiere elabora su un terminale separato e inserisce il riferimento; registrati localmente e in coda per la sincronizzazione |
| Pagamenti con carta (lettore integrato — Stripe Terminal, ecc.) | Non disponibile — i lettori di carta integrati comunicano con la rete di pagamento in tempo reale |
| Pagamenti con carte regalo | Non disponibile — la verifica del saldo richiede una connessione attiva |
| Pagamenti suddivisi combinando contanti e carta manuale | Disponibile |
| Stampa di ricevute su una stampante di rete | Disponibile se la stampante è sulla stessa rete locale del dispositivo — la stampa non richiede l'accesso a Internet, solo la connettività locale |
| Ricevute digitali (email/SMS/WhatsApp) | Non disponibile — l'invio richiede una connessione attiva |
| Navigazione nella cronologia degli ordini | Disponibile — mostra gli ordini memorizzati con un banner che indica che si sta visualizzando dati offline |
| Rimborsi e annullamenti | Non disponibile — richiedono una connessione attiva |
| Verifica dei punti di fedeltà dei clienti | Non disponibile |
| Apertura e chiusura di turni | Disponibile — lo stato del turno viene memorizzato localmente |

## Vendite in coda e sincronizzazione quando la connessione torna

Le vendite in modalità offline non vengono perse.

Quando il POS non riesce a raggiungere il server, ogni vendita completata viene scritta in una coda locale (il magazzino `pendingTransactions` nel database locale del dispositivo).

La vendita include tutti gli elementi del carrello, le quantità, i prezzi, il metodo di pagamento e l'orario in cui è stata completata.

Quando l'accesso a Internet viene ripristinato, il POS esegue automaticamente le seguenti azioni:

1. Rileva il riconnessione tramite l'evento `online` del browser
2. Mostra un banner: **"Sincronizzazione di N transazioni in sospeso..."**
3. Invia le vendite in coda al backend nell'ordine, utilizzando un piano di ripetizione con back-off esponenziale se il primo tentativo fallisce (fino a 10 ripetizioni in un intervallo massimo di cinque minuti per tentativo)
4. Marca ogni vendita come sincronizzata una volta che il backend la conferma

**Protezione contro le vendite duplicate** — ogni vendita in coda viene assegnata un ID unico locale prima di lasciare il dispositivo. Il backend controlla questo ID prima di creare un ordine. Se la stessa vendita viene inviata due volte (ad esempio, perché un tentativo di ripetizione si è sovrapposto a un primo tentativo riuscito), il backend ignora la duplicata. Mai finire con vendite duplicate.

**Rilevamento dei conflitti** — in rari casi, il backend potrebbe segnalare una vendita in coda come conflittuale (ad esempio, se un prodotto è stato eliminato sul server mentre il dispositivo era offline). Le vendite conflittuali appaiono in **POS > Impostazioni > Transazioni in sospeso** in modo da poterle rivedere e risolverle manualmente.

**Gestione degli aggiustamenti dell'inventario offline** — vengono gestiti nello stesso modo: i cambiamenti all'inventario effettuati in modalità offline vengono messi in coda e riprodotti quando la connessione torna. I numeri dell'inventario locali sul dispositivo vengono aggiornati immediatamente in modo che il cassiere veda un conteggio accurato (stimato).

## Installazione del POS sullo schermo iniziale del dispositivo

Installare il POS sullo schermo iniziale del dispositivo ti dà un'esperienza a schermo intero senza barra degli indirizzi del browser, un'icona di accesso rapido sul dispositivo e tempi di avvio più veloci.

### iPad (Safari)

1. Apri Safari e vai all'URL del POS del tuo negozio: `https://yourstore.com/pos/`
2. Accedi e completa il primo abbinamento se si tratta di un nuovo dispositivo.
3. Tocca il pulsante **Condividi** (il quadrato con una freccia verso l'alto) nella barra degli strumenti di Safari.
4. Scorri verso il basso nella scheda Condividi e tocca **Aggiungi allo schermo iniziale**.
5. Modifica il nome se desideri (di default è "Spwig POS") e tocca **Aggiungi**.

L'icona del POS ora appare sullo schermo iniziale dell'iPad. Toccarla apre l'app a schermo intero senza la barra del browser di Safari.

> **Nota:** Safari su iPad è richiesto per l'opzione Aggiungi allo schermo iniziale. I browser di terze parti su iOS (Chrome, Firefox) non supportano l'installazione di PWA a partire da metà 2025.

### Android (Chrome)

1. Apri Chrome e vai all'URL del POS del tuo negozio: `https://yourstore.com/pos/`
2. Accedi e completa l'abbinamento se necessario.
3. Tocca il **menu a tre punti** (in alto a destra) e tocca **Installa app** (o **Aggiungi allo schermo iniziale** su versioni più vecchie di Chrome).
4. Conferma toccando **Installa**.

L'icona del POS appare sullo schermo iniziale e nell'elenco delle app. Avviandola dall'icona apre l'app in modalità standalone.

### Desktop (Chrome o Edge)

1. Vai all'URL del POS del tuo negozio in Chrome o Edge.
2. Cerca l'**icona di installazione** nella barra degli indirizzi del browser (un monitor con una freccia verso il basso, o un'icona '+' a seconda della versione).
3. Oppure apri il **menu a tre punti** e seleziona **Installa Spwig POS** (Chrome) o **Apps > Installa questo sito come app** (Edge).
4. Conferma l'installazione.

Il POS si apre come finestra autonoma senza schede del browser o la barra degli indirizzi. Appare nell'elenco delle app del sistema e può essere fissata alla barra delle applicazioni.

## Come l'app viene aggiornata

Il POS gestisce gli aggiornamenti autonomamente tramite il Service Worker. Non è necessario visitare un negozio di app o scaricare manualmente nulla.

**Ciclo di aggiornamento:**

1.

Ogni volta che apri il POS (o la scheda diventa attiva dopo essere stata in background), il Service Worker controlla il server alla ricerca di una nuova versione.
2.

Se una nuova versione è disponibile, il Service Worker la scarica in background mentre continui a lavorare — la tua sessione corrente non viene interrotta.
3.

L'aggiornamento entra in vigore la prossima volta che apri il POS.

Se l'app è già aperta e una sincronizzazione è in sospeso, il POS attende che la coda venga svuotata prima di segnalare che un riavvio è pronto, per evitare di interrompere un turno attivo con vendite non sincronizzate.

**Cosa significa "riavvio" quando ci sono vendite in sospeso** — se vedi un prompt per il riavvio per un aggiornamento e hai vendite offline in sospeso, chiudi il turno corrente in modo pulito (o aspetta che il banner di sincronizzazione si elimini) prima di riavviare. Riavviare mentre ci sono vendite in coda non le elimina — rimangono nel database locale — ma è più sicuro sincronizzarle prima per confermare che siano state ricevute.

**Verifica la versione installata** — apri il POS, tocca l'icona **menu** (tre linee orizzontali), e vai a **Impostazioni**. La versione corrente del build è mostrata in fondo al pannello delle impostazioni.

## Archiviazione e cancellazione dell'installazione

Il POS archivia diversi tipi di dati in locale:

| Cosa | Dimensione tipica |
|------|-------------|
| App shell (HTML, CSS, JS, icone) | ~3–5 MB |
| Catalogo dei prodotti (testo e metadati) | 1–10 MB a seconda della dimensione del catalogo |
| Immagini dei prodotti (cachate) | 5–50 MB a seconda della dimensione del catalogo |
| Storico degli ordini | 1–5 MB (500 ordini) |
| Registri dei clienti | 1–3 MB (1.000 clienti) |
| Coda delle transazioni in sospeso | Minima; cancellata durante la sincronizzazione |

**Se il dispositivo ha poco spazio di archiviazione** — i browser applicano pressione alla memoria cache quando il dispositivo è pieno. Il POS imposta le sue cache come persistenti dove il browser lo permette, ma su dispositivi molto pieni il browser potrebbe eliminare prima le immagini dei prodotti. Se le immagini smettono di caricarsi, il POS le ricacherà durante la prossima sincronizzazione. Le vendite sincronizzate e la shell dell'app non sono interessate.

**Reinstallazione dell'app** — se il POS si comporta in modo inaspettato (bloccato su una vecchia versione, catalogo non aggiornato, sincronizzazione bloccata definitivamente), puoi eseguire un reset pulito:

1. **Disinstalla l'app** — su mobile, premi e tieni premuto l'icona del POS e scegli **Rimuovi** o **Disinstalla**. Su desktop, fai clic con il tasto destro sulla barra del titolo della finestra dell'app e scegli **Disinstalla**.
2. Apri direttamente l'URL del POS nel browser e accedi nuovamente.
3. Il dispositivo ti chiederà nuovamente il codice di accoppiamento di 8 caratteri del terminale. Puoi trovare o rigenerare questo codice nell'amministratore a **POS > POS Terminals** — apri il terminale e fai clic su **Rigenera codice di accoppiamento**.
4. Un nuovo accoppiamento forza una completa ricarica di tutti i dati in cache.

> **Dopo il reset**: qualsiasi vendita offline che era in coda ma non sincronizzata prima del reset sarà persa, poiché il database locale viene cancellato. Assicurati sempre che la connessione venga ripristinata e che il banner di sincronizzazione si elimini prima di resettare un'installazione.

## Risoluzione dei problemi

### Il POS è bloccato su una vecchia versione

Il Service Worker potrebbe non aver attivato ancora la nuova versione. Prova a chiudere tutti i tab del browser aperti con il POS e poi riaprirlo. Se il problema persiste, esegui il reset dell'installazione come descritto sopra.

### Il banner "Nessuna connessione" non si elimina

Verifica che il dispositivo abbia accesso a Internet al di fuori del POS (prova a caricare un altro sito). Se il dispositivo è online ma il banner persiste:

- Il server del POS potrebbe essere temporaneamente irraggiungibile — attendi un minuto e il POS riproverà automaticamente.
- Se sei su una rete che richiede una pagina di accesso (captive portal), apri una nuova scheda del browser, completa l'accesso e poi torna al POS.

### Un prodotto manca nel POS anche se esiste nell'amministratore

Il POS sincronizza i prodotti ogni cinque minuti quando è online. Se hai aggiunto un prodotto nell'amministratore molto recentemente, tocca l'icona **menu** e vai a **Impostazioni > Sincronizza Ora** per attivare una sincronizzazione immediata. Se il prodotto non appare comunque, conferma che sia contrassegnato come **Attivo** e non escludere la disponibilità nel POS nelle impostazioni del prodotto.

### Le transazioni in sospeso sono bloccate nello stato "Conflitto"

Vai a **POS > Impostazioni** (all'interno dell'app POS stessa) e controlla il pannello **Transazioni in sospeso**.

Le transazioni in conflitto sono generalmente causate da un prodotto o un prezzo che è cambiato tra il momento in cui la vendita è stata fatta offline e quando è stata sincronizzata.

Puoi visualizzare i dettagli dello sconto e, se lo sconto è stato ricevuto correttamente, contrassegnarlo come revisionato.

## Consigli

- Esegui il POS su un dispositivo dedicato che rimanga connesso alla tua rete Wi-Fi locale. I brevi interruzioni di Wi-Fi vengono gestite automaticamente, ma un dispositivo che rimane offline per lunghi periodi avrà bisogno di più tempo per risincronizzarsi quando ristabilisce la connessione.
- Gli intervalli di sincronizzazione sono per dispositivo. Se hai più terminali, ciascuno sincronizza in modo indipendente. Uno sconto su un terminale appare immediatamente nell'amministrazione durante la sincronizzazione, ma il cache degli ordini locali dell'altro terminale si aggiorna solo durante il proprio ciclo di sincronizzazione.
- Prima di un'interruzione pianificata di Internet (ad esempio, spostandoti a un evento senza Wi-Fi), apri il POS mentre sei ancora connesso in modo che i dati del catalogo e dell'inventario siano aggiornati. Le vendite in contanti saranno in coda in modo affidabile; evita semplicemente i pagamenti con carta integrati fino a quando non sei nuovamente online.
- Se hai bisogno solo di vendite in contanti a un evento, il metodo di pagamento con carta manuale (il cassiere elabora sul terminale autonomo e inserisce un riferimento) funziona anche offline per le transazioni con carta.
- Mantieni il dispositivo collegato durante un turno lungo — il database locale e il processo di sincronizzazione non influiscono significativamente sulla batteria rispetto allo schermo, ma un dispositivo carico è sempre più sicuro per le transazioni.