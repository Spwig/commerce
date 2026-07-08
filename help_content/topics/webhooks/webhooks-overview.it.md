---
title: Panoramica dei Webhook
---

I webhook permettono al tuo negozio di notificare automaticamente sistemi esterni — come strumenti di gestione dell'inventario, ERP, servizi di spedizione o applicazioni personalizzate — ogni volta che accade qualcosa nel tuo negozio. Invece di far ripetere a questi sistemi la domanda "è cambiato qualcosa?", il tuo negozio invia una notifica non appena si verifica un evento.

## Cosa fanno i webhook

Quando si verifica un evento nel tuo negozio (un ordine viene effettuato, un pagamento viene ricevuto, un prodotto va fuori stock), Spwig invia una richiesta HTTP POST con i dati dell'evento a un URL che configuri. Il sistema ricevente può quindi agire immediatamente su quei dati — ad esempio, aggiornare l'inventario, attivare un'etichetta di spedizione o inviare una notifica personalizzata.

Usi comuni dei webhook includono:

- Sincronizzare gli ordini in tempo reale con un partner di spedizione
- Aggiornare l'inventario in un ERP quando cambia lo stock
- Attivare SMS o notifiche push per i cambiamenti nello stato degli ordini
- Registrare gli eventi in un data warehouse per la reporting
- Connettersi a strumenti di automazione come Zapier o Make

## Visualizzazione e gestione degli endpoint

Naviga verso **Integrations > Webhooks** per visualizzare tutti gli endpoint dei webhook configurati.

![Elenco degli endpoint dei webhook](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

L'elenco mostra il nome di ogni endpoint, l'URL, lo stato attivo, il numero di eventi a cui si iscrive, lo stato di salute e l'ultima ricezione di consegna.

### Indicatori di salute

La colonna **Salute** mostra a colpo d'occhio come ogni endpoint sta performando:

- **Sano** — Tutte le consegne recenti sono state riuscite
- **Degrado** — Alcuni fallimenti recenti, ma l'endpoint è comunque attivo
- **Non sano / Disattivato** — L'endpoint è stato disattivato automaticamente dopo troppi fallimenti consecutivi (di default 10). Devi attivarlo manualmente una volta risolto il problema sottostante.

## Creazione di un endpoint dei webhook

Fai clic su **+ Aggiungi endpoint dei webhook** per aprire il wizard di configurazione. Il wizard ti guida attraverso quattro passaggi.

### Passaggio 1: Informazioni di base

- **Nome** — Un'etichetta amichevole per identificare questo endpoint (es. `Servizio di spedizione degli ordini` o `Sincronizzazione dell'inventario`).
- **URL** — L'URL completo del server che riceverà le richieste POST dei webhook. Questo deve essere raggiungibile pubblicamente (non un URL localhost).
- **Descrizione** — Note opzionali su a cosa serve questo endpoint.
- **Attivo** — Se questo endpoint deve ricevere le consegne. Deseleziona per sospendere temporaneamente senza eliminare l'endpoint.

### Passaggio 2: Sottoscrizioni agli eventi

Scegli quali eventi devono attivare una consegna a questo endpoint. Gli eventi sono raggruppati per categoria:

#### Eventi degli ordini

| Evento | Quando si verifica |
|-------|---------------|
| `order.created` | Viene effettuato un nuovo ordine |
| `order.paid` | Il pagamento per un ordine è confermato |
| `order.cancelled` | Un ordine viene annullato |
| `order.fulfilled` | Tutti gli articoli in un ordine vengono spediti |
| `order.partially_fulfilled` | Alcuni articoli in un ordine vengono spediti |
| `order.status_changed` | Lo stato dell'ordine cambia |
| `order.note_added` | Viene aggiunta una nota a un ordine |

#### Eventi dei pagamenti

| Evento | Quando si verifica |
|-------|---------------|
| `payment.received` | Viene ricevuto un pagamento |
| `payment.failed` | Un tentativo di pagamento fallisce |
| `payment.pending` | Un pagamento è in attesa di conferma |

#### Eventi delle spedizioni

| Evento | Quando si verifica |
|-------|---------------|
| `shipment.created` | Viene creata una spedizione |
| `shipment.shipped` | Una spedizione viene inviata |
| `shipment.delivered` | Una spedizione viene consegnata |
| `shipment.returned` | Una spedizione viene restituita |
| `shipment.tracking_updated` | Le informazioni di tracciamento vengono aggiornate |

#### Eventi dell'inventario

| Evento | Quando si verifica |
|-------|---------------|
| `inventory.low_stock` | Lo stock scende al di sotto del limite |
| `inventory.out_of_stock` | Un prodotto va fuori stock |
| `inventory.restocked` | Un prodotto viene rifornito |
| `inventory.adjusted` | L'inventario viene aggiustato manualmente |

#### Eventi dei prodotti

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

#### Eventi dei clienti

`customer.created`, `customer.updated`, `customer.deleted`

#### Eventi di abbonamento

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Altri eventi

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

Per ricevere tutti gli eventi, iscriviti a `*` (wildcard). Questo è utile per endpoint di logging generici, ma genera più traffico — iscriviti solo agli eventi che effettivamente necessiti per le integrazioni in produzione.

### Passaggio 3: Configurazione

- **Max Retries** — Quante volte Spwig dovrebbe riprovare a consegnare un messaggio fallito prima di abbandonare (predefinito: 5). Ogni riprova utilizza un intervallo di back-off esponenziale.
- **Timeout (Secondi)** — Quanto tempo attendere che il server ricevente risponda prima di contrassegnare la consegna come fallita (predefinito: 30 secondi). Aumenta questo valore solo se il tuo server è noto per essere lento.

### Passaggio 4: Sicurezza

Ogni endpoint webhook riceve un **segreto di firma** generato automaticamente — una chiave casuale di 64 caratteri. Spwig utilizza questo segreto per firmare ogni payload del webhook con una firma HMAC-SHA256.

La firma è inclusa nell'intestazione della richiesta `X-Webhook-Signature`. Il tuo server ricevente dovrebbe verificare questa firma per confermare che la richiesta provenga effettivamente dal tuo negozio e non sia stata manipolata.

Il segreto viene visualizzato mascherato nell'amministrazione. Per visualizzarlo o ruotarlo, utilizza l'API di Spwig. Ruota immediatamente il segreto se sospetti che sia stato compromesso.

## Abilitare e disabilitare gli endpoint

Per abilitare o disabilitare rapidamente uno o più endpoint senza aprire ciascuno:

1. Seleziona le caselle di controllo accanto agli endpoint che desideri modificare
2. Utilizza il menu a discesa **Action** per scegliere **Enable selected endpoints** o **Disable selected endpoints**
3. Clicca su **Go**

Per riabilitare un endpoint che è stato disabilitato automaticamente a causa di errori, selezionalo e utilizza l'azione **Reset failure count**, quindi riabilitalo. Risolvi prima il problema che ha causato gli errori, altrimenti verrà disabilitato nuovamente rapidamente.

## Consigli

- Iscriviti solo agli eventi che effettivamente necessiti — gli eventi non necessari generano rumore nei tuoi log e aumentano il carico di consegna.
- Verifica sempre la firma del webhook nel tuo server ricevente prima di elaborare il payload. Questo ti protegge contro le richieste contraffatte.
- Utilizza il campo **Description** per registrare a quale sistema o integrazione questo endpoint è collegato. Questo è utile quando si risolvono problemi mesi dopo.
- Imposta un **Timeout** leggermente superiore al tempo di risposta tipico del tuo server. Un timeout di 10–15 secondi è sufficiente per la maggior parte delle integrazioni.
- Se un endpoint diventa **Unhealthy**, controlla prima i log di consegna (vedi **Webhook Deliveries**) per comprendere il modello di errore prima di riabilitarlo.
- Per test, indirizza i webhook a uno strumento come [webhook.site](https://webhook.site) per ispezionare i payload grezzi senza necessitare di un server live.