---
title: Log di consegna dei webhook
---

Ogni volta che il tuo negozio tenta di inviare un webhook, viene creato un entry nei log di consegna. Questi log ti permettono di vedere esattamente cosa è stato inviato, se è riuscito o meno, e cosa è successo durante i tentativi di riconsegna. Questa guida spiega come leggere i log di consegna e risolvere i problemi quando le consegne falliscono.

## Visualizzazione dei log di consegna

Naviga verso **Integrations > Webhook Deliveries** per visualizzare l'intera storia di tutti i tentativi di consegna dei webhook su tutti i tuoi endpoint.

![Webhook delivery logs](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

L'elenco mostra il nome dell'endpoint, il tipo di evento, lo stato, il codice di risposta HTTP, il tempo di risposta e il numero di tentativi effettuati per ogni consegna.

I log di consegna sono di sola lettura — vengono creati automaticamente quando vengono generati gli eventi e non possono essere modificati.

## Stati di consegna

Ogni consegna ha uno di questi stati:

| Stato | Cosa significa |
|--------|---------------|
| **In attesa** | La consegna è in coda e non è ancora stata tentata |
| **Successo** | Il server ricevente ha risposto con un codice di stato HTTP 2xx — consegna confermata |
| **Fallita** | Tutti i tentativi di consegna sono stati esauriti — la consegna non verrà più riprovata |
| **Riprova** | L'ultimo tentativo è fallito, ma il sistema proverà di nuovo al tempo di riprova programmato |
| **Bloccato in sandbox** | La consegna è stata bloccata perché l'URL dell'endpoint non è accessibile nell'ambiente corrente |

Una consegna è considerata riuscita quando il server ricevente restituisce qualsiasi codice di risposta HTTP 2xx (200, 201, 202, ecc.). Qualsiasi altra risposta — incluso 3xx redirect o errori 4xx/5xx — viene trattata come un fallimento.

## Filtro delle consegne

Utilizza il pannello di filtro a destra per restringere l'elenco:

- **Stato** — Visualizza solo consegne fallite, in riprova o riuscite
- **Tipo di evento** — Visualizza tutte le consegne per un evento specifico (es. tutte le consegne `order.created`)
- **Endpoint** — Visualizza le consegne per un endpoint specifico
- **Creato il** — Filtra per intervallo di date

Utilizza la barra di ricerca per cercare per tipo di evento o nome dell'endpoint, o per trovare una consegna specifica tramite il suo ID.

## Visualizzazione dei dettagli di una consegna

Fai clic su qualsiasi consegna per visualizzare i suoi dettagli completi. I record di consegna sono di sola lettura.

### Riepilogo

- **ID** — L'identificatore univoco per questo tentativo di consegna
- **Endpoint** — A quale endpoint webhook è stata inviata questa consegna (collegamento al record dell'endpoint)
- **Tipo di evento** — L'evento che ha scatenato questa consegna (es. `order.paid`)
- **Stato** — Lo stato corrente della consegna

### Payload

La sezione **Payload** mostra i dati JSON esatti che sono stati inviati al tuo endpoint. Questi includono il tipo di evento, un timestamp e i dati completi dell'evento. Utilizza questa sezione per verificare che il tuo server ricevente riceva la struttura dati corretta.

### Risposta

La sezione **Risposta** mostra cosa ha risposto il tuo server:

- **Codice di risposta** — Il codice di stato HTTP restituito dal tuo server. Codificato in colori: verde per 2xx (successo), giallo per 4xx (errore del client), rosso per 5xx (errore del server).
- **Tempo di risposta** — Quanto tempo ha impiegato il tuo server per rispondere in millisecondi. Codificato in colori: verde sotto i 500 ms, giallo fino a 2 secondi, rosso sopra i 2 secondi.
- **Corpo della risposta** — Il corpo della risposta del tuo server (troncato a 1.000 caratteri). Questo può aiutare a identificare il motivo per cui il tuo server ha rifiutato il webhook.
- **Intestazioni della risposta** — Le intestazioni restituite dal tuo server.

### Dettagli dell'errore

Se la consegna è fallita, la sezione **Dettagli dell'errore** mostra il messaggio di errore — ad esempio, `Connection refused`, `Timeout after 30s`, o l'errore HTTP dal tuo server.

### Informazioni sulle riprovate

- **Conteggio tentativi** — Quanti tentativi di consegna sono stati effettuati (incluso il primo tentativo)
- **Prossima riprova a** — Quando verrà effettuata la prossima riprova (mostrata solo per le consegne nello stato **Riprova**)

Le riprovate seguono un programma di back-off esponenziale — l'intervallo tra le riprovate aumenta con ogni tentativo per evitare di sovraccaricare un server temporaneamente non disponibile. Con un massimo di 5 riprovate (predefinito), il programma di riprova si estende su diverse ore.

## Riprovare manualmente le consegne fallite

Se si desidera riprovare immediatamente una consegna senza attendere lo schedule automatico:

1. Selezionare le caselle di controllo accanto alle consegne che si desidera riprovare
2. Dal menu a discesa **Azioni**, scegliere **Riprovare le consegne selezionate**
3. Fare clic su **Vai**

Vengono messi in coda solo le consegne che non sono già nello stato **Success**. Le consegne riuscite vengono ignorate.

Questo è utile quando si è risolto un problema con il proprio server ricevente e si desidera rielaborare gli eventi falliti senza attendere.

## Diagnosi dei fallimenti comuni

### Codici di risposta HTTP 4xx

Una risposta 4xx dal vostro server indica di solito che c'è un problema con la richiesta — l'autenticazione è fallita, l'URL dell'estremità è cambiato o il vostro server ha rifiutato il formato del payload. Controllare:

- L'URL dell'estremità è corretto?
- Il vostro server verifica correttamente la firma HMAC? Una discrepanza causa spesso che molti server restituiscano 401 o 403.
- È cambiata la struttura del payload? Controllare il payload nel registro delle consegne rispetto a quanto il vostro server aspetta.

### Codici di risposta HTTP 5xx

Una risposta 5xx indica che il vostro server ha incontrato un errore interno durante il processamento del webhook. Controllare i propri log degli errori del server per diagnosticare il problema.

### Connessione rifiutata / Timeout

Questi errori significano che Spwig non è riuscito a raggiungere il vostro server affatto:

- Il server è in esecuzione e accessibile pubblicamente?
- L'URL è corretto (incluso il protocollo corretto — http o https)?
- Un firewall blocca le richieste in arrivo?
- Il tempo di risposta del server supera il timeout configurato? Se sì, aumentare l'impostazione **Timeout** sull'estremità o ottimizzare il gestore webhook del server per rispondere rapidamente (ideale entro 5 secondi).

### Sandbox Bloccata

Le consegne sono bloccate per URL localhost o indirizzi di rete interna. Gli endpoint webhook devono essere accessibili pubblicamente. Utilizzare uno strumento come ngrok durante lo sviluppo per esporre pubblicamente un server locale.

## Consigli

- Risolvere immediatamente le consegne **Fallite** — i dati dell'evento sono ancora nel payload, e si può riprovare manualmente una volta risolto il problema.
- Se si vedono molte consegne **Riprovando** per un singolo endpoint, aprire il record dell'estremità e controllare la sezione **Salute** — l'estremità potrebbe essere presto disattivata automaticamente.
- Il tempo di risposta è importante: configurare il gestore webhook per rispondere rapidamente (entro alcuni secondi) e elaborare il payload in modo asincrono in background. Un gestore lento causa fallimenti per timeout anche se la logica è corretta.
- Utilizzare il filtro **Tipo di evento** per controllare l'history delle consegne per un tipo specifico di evento quando si indaga se l'integrazione riceve gli eventi corretti.
- I log delle consegne si accumulano nel tempo. Utilizzare il filtro per la data per concentrarsi sulle consegne recenti e evitare di navigare attraverso l'history vecchia.