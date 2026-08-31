---
title: Journey Builder
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

Il **Journey Builder** è la tela visiva drag-and-drop in cui si progetta ciò che una [Journey](/help/triggered-journeys) fa effettivamente: quali email vengono inviate, quanto tempo attendere tra di esse e se diversi abbonati dovrebbero seguire percorsi diversi. Invece di compilare un modulo, si costruisce il flusso come un diagramma di flusso: caselle connesse su una tela che è possibile riorganizzare, ramificare e visualizzare d'occhio.

## Apertura del builder

Ogni journey ha la propria tela builder. È possibile accedervi in due modi:

- Creazione di una nuova journey — compila i campi **Nome**, **Trigger** e pubblico nella pagina delle impostazioni e fai clic su **Salva** — verrai portato direttamente nel builder per iniziare a progettare immediatamente.
- Apertura della pagina delle impostazioni di una journey esistente e cliccando su **Progetta journey** in alto.

Il builder è un'area di lavoro a schermo intero con tre sezioni: una **paletta** di tipi di passaggio a sinistra, la **tela** al centro e un pannello **impostazioni passaggio** a destra che appare quando selezioni un elemento.

![La tela del Journey Builder che mostra una serie di benvenuto con una ramifica Sì/No](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

In alto sulla tela, un'intestazione ripete il **Trigger** e il **pubblico** della journey (o "Tutti gli abbonati" se non è stato impostato un segmento) in modo da sapere sempre per chi si sta progettando senza uscire dal builder. Usa il pulsante **Indietro** per tornare alla pagina delle impostazioni della journey.

## I tipi di passaggio

Trascina un passaggio dalla paletta a sinistra sulla tela, oppure fai clic su un elemento della paletta per inserirlo automaticamente. Sono disponibili quattro tipi di passaggio:

| Passaggio | Cosa fa |
|------|--------------|
| **Invia email** | Invia una delle tue campagne all'abbonato. |
| **Attendi** | Sospende per un numero impostato di ore o giorni prima di continuare. |
| **Ramifica** | Divide il percorso in due — **Sì** o **No** — in base a se l'abbonato appartiene a un segmento scelto da te. |
| **Esci** | Termina la journey per l'abbonato. |

Ogni journey inizia con un singolo passaggio **Ingresso**, creato automaticamente la prima volta che apri il builder. Mostra il trigger della journey e non può essere eliminato: è semplicemente il punto in cui gli abbonati entrano nel flusso.

## Connessione dei passaggi

Ogni passaggio ha un piccolo **porto** circolare: uno in alto (input) e uno o più in basso (output). Per connettere due passaggi, trascina dal porto inferiore di un passaggio al porto superiore di un altro passaggio — appare una linea curva che li collega.

Un passaggio **Ramifica** ha due porte di output invece di una: una verde **Sì** e una rossa **No**. Collega ciascuna al punto in cui quel percorso dovrebbe portare — possono ricongiungersi successivamente allo stesso passaggio (come nell'esempio sopra, dove entrambi i percorsi tornano allo stesso **Esci**) o procedere per vie completamente separate.

Per riorganizzare il layout, trascina un passaggio per il corpo per riposizionarlo — le linee connesse seguono automaticamente. Trascina una parte vuota dello sfondo della tela per scorrere, e usa la rotella del mouse per zoomare in avanti o indietro. Se perdi il filo del flusso, fai clic su **Adatta** nella barra degli strumenti per ricentrare e zoomare per adattarlo tutto allo schermo.

## Configurazione di un passaggio

Fai clic su qualsiasi passaggio per aprire le sue impostazioni nel pannello a destra:


| Passaggio | Impostazione |
|------|---------|
| **Invia email** | Seleziona l'**Email da inviare** dall'elenco a discesa delle tue campagne. |
| **Attesa** | Imposta **Attendi per** — un numero più **ore** o **giorni**. |
| **Ramo** | Scegli **Se l'abbonato è nel segmento** — il segmento che decide Sì o No. |
| **Uscita** | Nessuna impostazione — è solo un punto finale. |

![Pannello a destra che configura un passaggio Ramo, con la tela attenuata sullo sfondo](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Le modifiche vengono salvate automaticamente non appena selezioni un valore — non c'è un pulsante **Salva** separato sulla tela. Ogni passaggio, tranne **Ingresso**, ha un pulsante **Elimina passaggio** in fondo al suo pannello di impostazioni.

Le email che selezioni per i passaggi **Invia email** sono campagne ordinarie che progetti nel normale builder visivo di Campaign Studio — riga dell'oggetto, blocchi di contenuto, tutto. Lasciale come **Bozza** e scegli semplicemente dall'elenco a discesa qui; il percorso le invia per te, non devi mai cliccare Invia tu stesso.

## Partire da un modello

Costruire un flusso da una tela vuota non è sempre necessario — clicca su **Modelli** nella barra degli strumenti (o **Sfoglia modelli** su una tela vuota) per aprire un selettore con otto starter pronti all'uso:

| Modello | Cosa costruisce |
|----------|-----------------|
| **Serie di benvenuto** | Saluta i nuovi abbonati, condividi di cosa ti occupi, poi un promemoria per il primo ordine. |
| **Onboarding primo ordine** | Trasforma un acquirente alla prima volta in un cliente abituale con una sequenza di onboarding delicata. |
| **Post-acquisto e recensione** | Ringrazia dopo qualsiasi ordine, poi chiedi una recensione una volta che è arrivato. |
| **Offerta VIP vs. standard** | Dopo un ordine, si ramifica sul tuo segmento VIP per inviare l'offerta di follow-up giusta a ciascun gruppo. |
| **Recupero carrello abbandonato** | Promemoria a un acquirente che ha lasciato articoli indietro, poi un promemoria di follow-up un giorno dopo. |
| **Recupero clienti inattivi** | Riaggancia un cliente che non ha acquistato da un po' con un motivo per tornare. |
| **Richiesta recensione post-consegna** | Chiedi una recensione pochi giorni dopo che un ordine è stato contrassegnato come Consegnato. |
| **Avviso di disponibilità** | Avvisa un acquirente in attesa nel momento in cui un prodotto che desiderava è di nuovo disponibile. |

Ogni modello è preconfigurato per il trigger corrispondente — ad esempio, applicare **Recupero clienti inattivi** a un nuovo percorso prevede anche che il **Trigger** di quel percorso sia **Cliente inattivo (recupero)**. Vedi [Percorsi attivati](/help/triggered-journeys) per cosa attiva ciascuno di questi eventi di trigger e come si comportano quelli focalizzati sul recupero (finestre di inattività, checkout come ospite, richieste di recensione una volta per ordine e come un percorso di disponibilità sostituisce l'avviso una tantum semplice).

![Selettore di modelli che mostra i percorsi starter pronti all'uso](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Applicare un modello **sostituisce il flusso attuale** sulla tela, quindi usalo all'inizio della progettazione di un percorso piuttosto che a metà. Spwig ricollega ogni passaggio a una vera email o segmento ovunque i nomi corrispondano a qualcosa che hai già; ovunque non riesca a trovare una corrispondenza, l'intestazione riporta quanti passaggi hanno ancora bisogno di una scelta di email o segmento, così sai esattamente cosa completare prima di andare online.

## Condivisione dei percorsi

Due pulsanti nella barra degli strumenti ti permettono di spostare la progettazione di un percorso tra passaggi o tra negozi:

- **Esporta** scarica il percorso come file `.journey.json` — una descrizione portante della forma del flusso (i suoi passaggi, attese, rami e percorsi Sì/No) più i *nomi* delle email e dei segmenti che ogni passaggio utilizza. Non include i design delle email stesse né alcun dato degli abbonati.
- **Importa** carica un file `.journey.json` nel percorso attuale, sostituendo ciò che è sulla tela.

Questo è utile per fare il backup di un flusso di cui sei orgoglioso, passare una serie di benvenuto collaudata a un altro negozio Spwig, o ricostruire un percorso dopo aver clonato il tuo negozio in una nuova installazione.

Come per i modelli, Spwig ricollega e-mail e segmenti in base al nome, dove esiste una corrispondenza sul negozio di destinazione, e segnala qualsiasi elemento che non riesce a trovare in modo che tu possa completare la configurazione.

## Attivazione del tuo percorso

Quando il flusso è pronto, utilizza il controllo dello stato nell'angolo in alto a destra del costruttore. Un'etichetta mostra lo stato corrente del percorso - **Bozza**, **Attivo** o **In pausa** - accanto al pulsante **Attiva**.

Fare clic su **Attiva** **verifica innanzitutto il flusso**. Se qualcosa potrebbe bloccare il funzionamento, l'attivazione viene bloccata e un banner elenca i problemi: ad esempio un passo **Invia e-mail** senza e-mail selezionata, un **Ramo** senza segmento o senza percorso Sì / No, un'e-mail o un segmento che è stato eliminato, o un ciclo che potrebbe eseguirsi all'infinito. Ogni problema è cliccabile: selezionandolo si passa al passo corrispondente, che viene evidenziato in rosso finché non lo si risolve. Vengono inoltre elencati gli avvisi (ad esempio un passo non raggiungibile o un **Attesa** senza ritardo impostato), ma non bloccano l'attivazione.

![Attivazione bloccata, con il problema elencato in un banner e il passo corrispondente evidenziato in rosso](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Una volta che il flusso è passato, l'etichetta diventa **Attivo** e il percorso inizia a iscrivere gli iscritti ogni volta che viene attivato il suo trigger. Il pulsante diventa **Pausa**, che blocca le nuove iscrizioni - gli iscritti già in fase di esecuzione ricevono comunque i loro passaggi rimanenti. Vedere [Percorsi scatenati](/help/triggered-journeys) per come interagiscono iscrizione, periodi di raffreddamento e stato.

## Vedere chi è nel percorso

Una volta che il percorso è attivo, ogni passo mostra un piccolo **badge del conteggio** nell'angolo: il numero di iscritti che si trovano in quel passo in quel momento. È un modo veloce per vedere dove si sta verificando il flusso e dove si sta accumulando il traffico - un numero elevato su un passo **Attesa** è normale, mentre un accumulo prima di una particolare e-mail potrebbe valere la pena di controllare. I conteggi vengono aggiornati ogni volta che torni nella scheda del costruttore.

![Il piano con i badge del conteggio attivi sui passi e la funzione Attiva nel riquadro degli strumenti](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Suggerimenti

- Progetta il flusso mentre è ancora in **Bozza** - nessuno verrà iscritto finché non lo **Attivi**. Attivare dal costruttore esegue un controllo veloce e non permetterà a un flusso difettoso di essere attivo, quindi non c'è il rischio che un percorso non completato iscriva degli iscritti.
- Parti da un **Modello** anche se hai intenzione di personalizzarlo molto - è più veloce modificare un flusso esistente che costruirne uno da zero, inoltre dimostra il modello di ramo se non l'hai mai utilizzato prima.
- Dopo aver applicato un modello o aver importato un file, controlla l'intestazione per un avviso sui passi non corrispondenti e completa eventuali passi **Invia e-mail** o **Branca** che non riesce a trovare prima di attivarlo.
- Fai clic su **Adatta** ogni volta che il flusso diventa troppo ampio (specialmente i rami) - è il modo più veloce per vedere di nuovo l'intera forma dopo aver ingrandito o spostato.
- Mantieni i nomi dei passi facilmente individuabili tenendo ciascun passo **Attesa** immediatamente prima dell'e-mail che ritarda, invece di raggruppare diversi passi **Attesa** insieme.
- **Esporta** un percorso funzionante prima di apportare modifiche importanti - è un modo veloce per tenere presente una copia di backup che puoi rimportare se non ti piace il risultato.