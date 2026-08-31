---
title: Giri attivati
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

I **Giri** di Campaign Studio sono sequenze email automatizzate e multistep che si avviano da sole ogni volta che un cliente compie un'azione specifica: si registra, effettua un ordine, lascia articoli nel carrello, resta inattivo per un po' di tempo o riceve la consegna di un ordine. Invece di ricordare di inviare manualmente un'email di benvenuto, un promemoria per il recupero del carrello o una richiesta di recensione, crei la sequenza una sola volta e Spwig la esegue per ogni cliente idoneo, finché il giro rimane attivo.

## Tre modi per inviare email

Campaign Studio copre ora tre distinti modelli di invio:

| Tipo | Comportamento |
|------|-----------|
| **Broadcast** | Inviato una sola volta — immediatamente o in un'unica data e ora pianificata. Da usare per un annuncio o una vendita occasionale. |
| **Recurring** | Un modello che viene inviato secondo un programma ripetuto (vedi [Campagne ricorrenti](/help/recurring-campaigns)). |
| **Giro** | Una sequenza multistep che si avvia automaticamente per un singolo cliente quando si verifica un evento del ciclo di vita, per poi distribuire i suoi passaggi nel corso di ore o giorni. |

Un giro non ha un proprio pulsante "invia" né un programma da configurare — reagisce a eventi anziché a un orologio.

## Trigger

Ogni giro monitora esattamente un evento, impostato come **Trigger** del giro:

| Trigger | Si attiva quando |
|---------|-----------|
| **Il cliente si registra** | Viene creato un nuovo account cliente. |
| **Viene effettuato un ordine** | Viene effettuato qualsiasi ordine, da parte di un cliente nuovo o abituale. |
| **Viene effettuato il primo ordine** | Specificamente il primissimo ordine di un cliente. |
| **Carrello abbandonato** | Un acquirente aggiunge qualcosa al carrello, poi resta inattivo senza completare l'acquisto. |
| **Cliente inattivo (win-back)** | Un cliente non ha effettuato un ordine da un po' di tempo. |
| **Ordine consegnato** | Lo stato di un ordine cambia in Consegnato. |
| **Prodotto di nuovo disponibile** | Un prodotto per il quale un cliente ha richiesto di essere avvisato torna disponibile. |

## I trigger di recupero e riattivazione, nel dettaglio

**Ordine consegnato** e **Prodotto di nuovo disponibile** si attivano immediatamente, allo stesso modo di **Viene effettuato un ordine**. **Carrello abbandonato** e **Cliente inattivo (win-back)** funzionano in modo diverso: invece di reagire a un singolo momento, Spwig controlla periodicamente gli acquirenti e i clienti che corrispondono ai criteri, quindi può esserci un breve ritardo tra il momento in cui un carrello diventa inattivo (o un cliente diventa inattivo) e l'iscrizione al giro.

**Carrello abbandonato** — iscrive un acquirente che ha aggiunto qualcosa al carrello e poi è rimasto inattivo senza completare l'acquisto. Di default, ciò avviene dopo circa un'ora di inattività; la finestra esatta di inattività (e quanto indietro Spwig continuerà a guardare) è una soglia che il tuo host può regolare per il tuo negozio. Funziona sia per gli acquirenti registrati che per gli ospiti — per un ospite, Spwig utilizza l'indirizzo email acquisito al momento del checkout. Se l'acquirente torna e completa l'ordine, viene automaticamente rimosso dal giro, in modo che un acquisto completato non riceva mai un'email "hai dimenticato qualcosa?". Aggiungi un blocco di contenuto **Carrello abbandonato** all'email di recupero per mostrare esattamente cosa è stato lasciato indietro, con prezzi aggiornati, immagini e un link di ritorno al carrello — oppure usa un blocco **Prodotto in evidenza** per mettere in risalto un singolo articolo.

**Cliente inattivo (win-back)** — iscrive un cliente che non ha effettuato un ordine da un po' di tempo, per dargli un motivo per tornare.

Di default, ciò corrisponde a 90 giorni senza acquisti (anch'esso una soglia regolabile dall'host).

Un cliente viene reinserito in un percorso di recupero al massimo una volta per finestra, quindi qualcuno che rimane inattivo non viene reinserito nuovamente subito.

**Ordine consegnato** — iscrive un cliente non appena lo stato del loro ordine cambia in **Consegnato**, un momento naturale per chiedere una recensione alcuni giorni dopo. Viene attivato una volta per ordine, al momento della transizione verso Consegnato - modifiche successive a un ordine già consegnato non lo attivano nuovamente. Si noti che l'azione di massa **Segna gli ordini selezionati come Consegnati** nell'elenco degli ordini aggiorna gli ordini direttamente e non attiva questo trigger (o l'e-mail di conferma della consegna); aggiorna gli ordini uno per uno, oppure tramite l'app mobile Spwig, per attivarlo.

**Prodotto rientrato a magazzino** — quando un prodotto per cui un cliente ha richiesto una notifica torna a magazzino, Spwig controlla se hai un percorso attivo che ascolta questo trigger. Se sì, il cliente viene iscritto in quel percorso invece che nella semplice notifica singola — quindi puoi aggiungere un ritardo, un blocco **Prodotto in evidenza** che mostra l'oggetto rifornito, o un'email di follow-up. Se non esiste un percorso per il rientro a magazzino attivo, i clienti ricevono comunque l'e-mail di notifica singola standard esattamente come prima, quindi attivare un percorso per questo trigger è facoltativo.

## Costruire un percorso

Vai su **Studio Campagne > Percorsi** e clicca su **Aggiungi Percorso**.

1. Dà al percorso un **Nome** — questo è per il tuo riferimento solo; i clienti non lo vedranno mai.
2. Scegli l'evento di **Attivazione**.
3. Imposta in modo opzionale **Solo per segmento** a un **Segmento** — quando impostato, solo i sottoscrittori che appartengono a quel segmento vengono mai iscritti. Lascialo vuoto per iscrivere ogni sottoscrittore idoneo.
4. Imposta **Una volta per sottoscrittore** e **Periodo di raffreddamento per il rientro (giorni)** — vedi [Protezione contro l'iscrizione eccessiva](#protezione-contro-l-iscrizione-eccessiva) qui sotto.
5. Imposta **Stato** su **Attivo** per attivare il percorso. Lascialo come **Bozza** mentre stai ancora progettandolo, oppure imposta su **In sospeso** per fermare nuove iscrizioni senza perdere la tua configurazione.
6. Clicca su **Salva** — Spwig ti porta direttamente nel [Journey Builder](/help/journey-builder), la tela visiva dove progetti la sequenza effettiva: quali email inviare, quanto aspettare tra di esse, e se diversi sottoscrittori debbano seguire percorsi diversi.

Un semplice percorso a tre fasi per i nuovi clienti, una volta progettato sulla tela, potrebbe sembrare così:

| Passo | Aspetta | Invia |
|------|-------|-------|
| 1 | Immediatamente | Email di benvenuto |
| 2 | Dopo 3 giorni | Suggerimenti per iniziare |
| 3 | Dopo 7 giorni | Sconto per il primo ordine |

Le email stesse sono normali Campagne che progetti nello stesso costruttore visivo che useresti per un Broadcast — soggetto, blocchi di contenuto, tutto. Non c'è bisogno di pianificare o inviare personalmente una di esse; lasciala come **Bozza** e basta sceglierla dal menu a tendina del passo nel costruttore. Il percorso lo invierà per te, una volta per sottoscrittore che raggiunge quel passo.

Vedi [Journey Builder](/help/journey-builder) per la guida completa per progettare i passi sulla tela, suddividere un percorso con una condizione **Sì / No**, e partire da un modello pronto invece che da una tela vuota.

## Test A/B di un passo

Ogni passo **Invia email** può essere trasformato in un test A/B, in modo che un percorso scoprira automaticamente — e poi continuerà a utilizzare — l'e-mail che ha ottenuto i migliori risultati. Poiché un percorso funziona in continuo (i sottoscrittori arrivano nel tempo), Spwig non testa un batch fisso e si ferma; invece **suddivide gli iscritti in modo equo tra le varianti man mano che entrano, osserva come ciascuna si comporta, e una volta che una diventa un chiaro vincitore statistico la blocca per ogni iscritto futuro.** I sottoscrittori già in fase di avanzamento mantengono la versione che è stata loro inviata per prima.

Apri un passo **Invia email** nel [Journey Builder](/help/journey-builder) e imposta **Tipo di passo**:

- **Email singolo** — il comportamento normale: tutti ricevono l'unico email che scegli.
- **A/B: email diverse** — scegli **due a quattro** email (design, offerte o layout diversi); ogni iscritto ne riceve una.
- **A/B: righe oggetto diverse** — scegli un'email e inserisci **due a quattro** righe oggetto; ogni iscritto riceve quell'email con un oggetto diverso.

Poi scegli **Scegli il vincitore in base a** — **Tasso di apertura** (di solito il migliore per un test degli oggetti) o **Tasso di clic** — e hai finito. Imposta il percorso su **Attivo** e gli iscritti inizieranno a essere suddivisi tra le varianti.

Il pannello del passaggio mostra una **classifica in tempo reale** man mano che arrivano i dati — i destinatari di ogni variante, il tasso di apertura e il tasso di clic, oltre a quanto Spwig è sicuro del leader ("In vantaggio con il 92% di confidenza"). Un vincitore viene bloccato solo quando Spwig è almeno al **95% di confidenza** *e* ci sono dati sufficienti per fidarsi, in modo che un percorso con poco traffico non tragga conclusioni affrettate. Una volta bloccato, il passaggio mostra **"Vincitore bloccato: Variante B"** e ogni nuovo iscritto riceve quella variante; sulla canvas la card mostra **"A/B · N email"** durante il test, poi **"Vincitore A/B: B"** una volta deciso.

Alcune cose da sapere:

- **Dai traffico.** La confidenza dipende dal volume — un passaggio raggiunto da poche persone potrebbe restare su "Ancora non ci sono dati sufficienti" per un po'. Il test A/B brilla sui percorsi con un'iscrizione costante.
- **Modificare le varianti o la metrica del vincitore avvia un nuovo test** — un vincitore precedentemente bloccato viene cancellato in modo che la nuova configurazione ottenga il proprio risultato.
- Un passaggio A/B con meno di due varianti **impedisce al percorso di diventare Attivo** finché non lo completi (o lo rimetti a un singolo email).

Vedi [Test A/B](ab-testing) per maggiori informazioni su come Spwig legge confidenza e significatività.

## Come funziona l'iscrizione

Quando l'evento di attivazione si verifica per un cliente, Spwig controlla ogni percorso attivo in ascolto di quell'evento e, per ciascuno per cui il cliente è idoneo, lo **iscrive** al punto di partenza del flusso. Da lì, Spwig fa avanzare l'abbonato attraverso ciò che hai progettato sulla canvas — aspettando ogni passaggio **Attesa**, inviando l'email di ogni passaggio **Invia email** e seguendo il percorso corretto **Sì**/**No** a ogni **Ramo** — finché non raggiunge un passaggio **Uscita**, al quale punto il percorso viene marcato come **Completato** per quell'abbonato.

**Il consenso è sempre rispettato.** Un abbonato che non ha optato per le email di marketing, o che si è disiscritto in seguito, viene semplicemente saltato — il percorso non si ferma per gli altri abbonati, e le disiscrizioni a metà percorso interrompono automaticamente le invii rimanenti per quell'abbonato. Non devi mai filtrare i tuoi percorsi in base allo stato del consenso.

## Prevenire le sovrascrizioni

Due impostazioni sul percorso controllano con quale frequenza un abbonato può attraversarlo:

| Impostazione | Cosa fa | Uso tipico |
|---------|--------------|-------------|
| **Una volta per abbonato** *(attivo di default)* | Ogni abbonato viene iscritto al massimo una volta, per sempre, indipendentemente da quante volte l'evento di attivazione si ripresenti per lui. | Una serie di benvenuto — un cliente dovrebbe riceverla solo una volta. |
| **Periodo di raffreddamento per la riiscrizione (giorni)** | Quando **Una volta per abbonato** è disattivato, imposta un numero minimo di giorni che devono trascorrere dall'ultima iscrizione di un abbonato prima che possa essere iscritto di nuovo. Imposta su `0` per nessun periodo di raffreddamento. | Una serie attivata da un ordine che dovrebbe ripetersi per un nuovo ordine, ma non riattivarsi per ogni ordine effettuato nella stessa settimana. |

Disattiva **Una volta per abbonato** per un percorso che vuoi eseguire per ordine (come un ringraziamento post-acquisto) e abbinalo a un periodo di raffreddamento in modo che un cliente che ordina due volte nello stesso giorno venga iscritto solo una volta. Un abbonato già attivamente in un percorso non viene mai iscritto a una seconda esecuzione sovrapposta di quello stesso percorso, indipendentemente da queste impostazioni.

## Monitoraggio dei percorsi


L'elenco **Campaign Studio > Journeys** mostra per ogni percorso il **Trigger**, lo **Stato**, il numero di **Email** inviate e i totali in corso di **Iscritti** / **Completati**, così da poter verificare a colpo d'occhio se un percorso sta effettivamente raggiungendo le persone.

![L'elenco Journeys che mostra due percorsi attivi con i conteggi di iscrizione e completamento](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Per visualizzare i singoli iscritti anziché i totali, apri l'elenco **Journey Enrollments** in `/admin/email_marketing/journeyenrollment/`. Ogni riga mostra i progressi di un iscritto in un percorso: in quale **Journey** si trova, il loro **Current step** (passo attuale), lo **Stato** (Active, Completed o Cancelled) e quando è prevista la loro **Next step** (prossima azione). Usa i filtri per restringere la ricerca a un singolo percorso o a un singolo stato — ad esempio, filtrando per **Active** vengono mostrati tutti coloro che sono attualmente a metà sequenza.

![L'elenco Journey Enrollments che mostra i progressi degli iscritti in due percorsi](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Report del percorso

Ogni percorso ha la propria pagina **Report**, aperta cliccando sul pulsante **Report** sulla scheda del percorso in **Campaign Studio > Journeys**, oppure sulla pagina di impostazioni del percorso stesso. Si tratta di un riepilogo su una singola pagina che mostra quanto gli iscritti avanzano nella sequenza e, se le tue email contengono link tracciati, quanta ricchezza il percorso ha generato.

![La pagina Report del percorso che mostra il funnel di iscrizione, la card del ricavo attribuito e la tabella dei ricavi per passo](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Funnel di iscrizione

Quattro card mostrano la posizione attuale degli iscritti:

| Card | Cosa mostra |
|------|---------------|
| **Enrolled** | Il numero totale di iscritti che sono entrati in questo percorso. |
| **Active now** | Iscritti attualmente a metà sequenza, in attesa o in fase di elaborazione del loro prossimo passo. |
| **Completed** | Iscritti che hanno raggiunto il passo **Exit** (uscita) del percorso. |
| **Exited** | Iscritti rimossi dal percorso prima del completamento — ad esempio, un acquirente che ha completato il checkout a metà di una sequenza di abbandono carrello, o un iscritto che ha disiscritto la newsletter. |

Se il percorso non ha ancora iscrizioni, tutte e quattro le card mostrano zero e una nota ti ricorda che le metriche appariranno una volta che i clienti inizieranno a entrare nel percorso.

### Ricavi attribuiti

La card **Attributed revenue** (Ricavi attribuiti) funziona allo stesso modo di un [report della campagna](campaign-reports) — Spwig traccia gli ordini riconducendoli ai clic sui link nelle email del percorso, con la stessa attribuzione basata sul click-through e soggetta al consenso descritta in [Attributed revenue](campaign-reports#attributed-revenue) in quella pagina. Si applicano le stesse avvertenze: l'attribuzione è solo click-through (una sola apertura non attribuisce mai ricavi), segue il modello di attribuzione attivo del tuo store e la finestra di lookback, rispetta il consenso all'analisi e non è retroattiva — un percorso mostra i ricavi solo dalle email inviate dopo che il tracciamento dell'attribuzione è stato attivato per il tuo store.

La riga secondaria della card scompone il totale in:

- **Orders** — quanti ordini sono attribuiti a questo percorso, sommando le email di tutti i passi.
- **AOV** — il valore medio dell'ordine per quegli ordini.
- **Revenue per enrollee** — ricavi attribuiti divisi per il totale degli **Enrolled**. Un percorso non ha una singola "spesa" come una campagna — funziona in modo continuo anziché avere un costo una tantum — quindi non c'è una figura ROAS qui. **Revenue per enrollee** è l'equivalente più vicino: una misura stabile e confrontabile di quanto efficientemente il percorso converte un'iscrizione in una vendita, che puoi monitorare nel tempo o confrontare con un altro percorso.

### Ricavi per passo

Quando il percorso ha almeno un passo **Send email**, una tabella **Revenue by step** scompone ulteriormente il totale, una riga per passo, così da poter vedere quale email nella sequenza sta effettivamente generando valore:

| Colonna | Cosa mostra |
|--------|---------------|
| **Passo** | La mail del passo, con un **A/B** se il passo sta eseguendo un test [A/B](ab-testing). |
| **Ricavi** | Ricavi attribuiti dagli ordini risalenti a questa mail del passo. |
| **Ordini** | Il numero di ordini che stanno dietro a quel fatturato. |
| **Inviati** | Quante volte questa mail del passo è stata inviata. |
| **Aperture** / **Clic** | Quanti di questi invii sono stati aperti e quanti cliccati. Spwig tiene traccia delle aperture e dei clic per ogni invio di ogni passo, sia in versione normale che A/B. |

Utilizza questa tabella per individuare un collegamento debole in un percorso altrimenti sano — ad esempio, una serie di benvenuto in cui la prima email genera la maggior parte dei ricavi e un passo successivo contribuisce poco potrebbe essere un candidato per un'offerta più forte o una riscrittura, invece di assumere che l'intera sequenza debba essere riesaminata.

## Suggerimenti

- Il modo più veloce per iniziare un percorso di abbandono carrello, recupero clienti, richiesta di recensione post-consegna o notifica di rientro a magazzino è un modello iniziale — quando salvi un nuovo percorso con uno di questi trigger, il selettore **Modelli** di [Journey Builder](/help/journey-builder) offre un flusso già pronto (**Recupero carrello abbandonato**, **Recupero clienti disattivi**, **Richiesta di recensione post-consegna**, o **Notifica di rientro a magazzino**) che puoi modificare invece di costruirlo da zero.
- Inizia ogni percorso come **Bozza** mentre costruisci i passi, quindi cambia **Stato** in **Attivo** una volta che hai verificato le email e i ritardi — nulla viene iscritto finché non è Attivo.
- Mantieni **Una volta per sottoscrittore** attivo per qualsiasi cosa legata a un traguardo unico (iscrizione, primo ordine); disattivalo con un periodo di attenuazione sensato per qualsiasi cosa che dovrebbe ripetersi, come una serie post-ordine.
- Usa **Solo per segmento** per eseguire una diversa serie di benvenuto per un pubblico specifico — ad esempio, un segmento VIP riceverà una sequenza più ricca rispetto agli altri.
- Imposta il tempo di attesa del primo passo su `0` se vuoi che la prima email venga inviata immediatamente dopo che il trigger è scattato, invece di aspettare.
- Controlla l'elenco **Iscrizioni al percorso** dopo aver attivato un nuovo percorso per confermare che i sottoscrittori vengano effettivamente iscritti e avanzino nei loro passi come previsto.
- Mettere in pausa un percorso (**Stato: In pausa**) blocca nuove iscrizioni ma non annulla i sottoscrittori già in fase di avanzamento — essi continueranno a ricevere i loro passi rimanenti.