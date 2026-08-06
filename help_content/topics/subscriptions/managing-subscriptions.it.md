---
title: Gestione delle sottoscrizioni dei clienti
---

La sezione delle sottoscrizioni dei clienti ti dà una visione completa di tutte le sottoscrizioni ricorrenti attive, in sospeso e annullate nel tuo negozio. Da qui puoi monitorare la salute del pagamento, visualizzare i dettagli di ciascuna sottoscrizione e intervenire quando si verificano problemi.

## Visualizzazione delle sottoscrizioni dei clienti

Vai a **Sottoscrizioni > Sottoscrizioni dei clienti** per vedere l'elenco completo delle sottoscrizioni di tutti i clienti.

![Elenco delle sottoscrizioni dei clienti](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

L'elenco mostra il cliente, il nome del piano, lo stato corrente, la data del prossimo pagamento e il numero di cicli di fatturazione completati per ciascuna sottoscrizione.

### Filtraggio e ricerca

Utilizza il pannello dei filtri a destra per restringere le sottoscrizioni per:

- **Stato** — Filtra tra Attivo, Prova, Scaduto, Sospeso, Annullato o Scaduto
- **Piano** — Visualizza le sottoscrizioni per un piano specifico
- **Modalità del provider** — Nativo (gestito da Stripe/PayPal) o Backup (fatturazione interna)

Utilizza la barra di ricerca per trovare le sottoscrizioni per indirizzo email del cliente.

## Stati delle sottoscrizioni

Capire ciascuno stato ti aiuta a identificare le sottoscrizioni che necessitano di attenzione:

| Stato | Cosa significa |
|--------|----------------|
| **Prova** | Il cliente si trova in un periodo di prova gratuito o a prezzo ridotto |
| **Attivo** | La sottoscrizione è in salute — il pagamento è attuale e l'accesso è attivo |
| **Scaduto** | Un tentativo di pagamento è fallito — il sistema sta riprovando. Il cliente mantiene l'accesso durante il periodo di tolleranza |
| **Sospeso** | La sottoscrizione è sospesa temporaneamente — nessuna fatturazione, nessun accesso |
| **Annullato** | È stata richiesta l'annullamento. Il cliente potrebbe ancora avere accesso fino alla data di fine periodo |
| **Scaduto** | La sottoscrizione è terminata completamente — la prova è scaduta, i cicli di fatturazione massimi sono stati raggiunti o il periodo di annullamento è trascorso |

Le sottoscrizioni che sono **Scadute** richiedono la massima attenzione — se i pagamenti continuano a fallire e il periodo di tolleranza si esaurisce, la sottoscrizione verrà sospesa.

## Visualizzazione dei dettagli di una sottoscrizione

Fai clic su qualsiasi sottoscrizione per aprire la visualizzazione dettagliata. Questo mostra:

### Periodo di fatturazione corrente

- **Inizio / Fine del periodo corrente** — Le date della finestra di fatturazione attiva
- **Data del prossimo pagamento** — Quando verrà eseguito il prossimo tentativo di addebito
- **Data dell'ultimo pagamento** e **Stato dell'ultimo pagamento** — Risultato del tentativo di fatturazione più recente
- **Conteggio del ciclo di fatturazione** — Quanti cicli di fatturazione riusciti sono stati completati

### Informazioni sulla sottoscrizione

- **Piano** e **Livello di prezzo** — Quale piano e frequenza di fatturazione sta utilizzando il cliente
- **Prodotto / Variante** — Il prodotto del catalogo collegato a questa sottoscrizione (se applicabile)
- **Quantità** — Numero di posti o unità (per piani basati sulla quantità)
- **Token di pagamento** — Il metodo di pagamento memorizzato utilizzato per la fatturazione ricorrente

### Dettagli della prova

Se la sottoscrizione è in fase di prova, **Data di fine prova** indica quando scade la prova del cliente e inizia la piena fatturazione.

### Dettagli di annullamento

Per le sottoscrizioni annullate, puoi vedere:

- **Tipo di annullamento** — Se l'annullamento è stato immediato, alla fine del periodo o programmato
- **Annullato il** — Quando è stata richiesta l'annullamento
- **Motivo dell'annullamento** — Note su perché il cliente ha annullato (se registrato)
- **Data limite per il riacquisto** — Ultima data in cui il cliente può riprendere l'accesso senza riscrivere la sottoscrizione da capo

### Periodo di tolleranza e impegni

- **Data di fine periodo di tolleranza** — Se un pagamento è fallito, indica la scadenza prima che l'accesso venga sospeso
- **Data di fine impegno minimo** — Per i piani con impegni minimi, la data di annullamento più precoce

## Sospendere una sottoscrizione

Una sottoscrizione sospesa sospende temporaneamente la fatturazione e l'accesso. Questo è utile per i clienti che vogliono prendersi una pausa senza annullare completamente.

Per visualizzare le sottoscrizioni sospese, filtra per **Stato: Sospeso**. La visualizzazione dettagliata mostra:

- **Sospeso il** — Quando è iniziata la sospensione
- **Motivo della sospensione** — Note su perché è stata sospesa
- **Data di ripresa automatica** — Se impostata, la data in cui la sottoscrizione riprenderà automaticamente la fatturazione e l'accesso

I sospesi riprendono o sulla data di riattivazione automatica o quando il cliente attiva nuovamente manualmente il servizio.

## registri del ciclo di fatturazione

Ogni tentativo di fatturazione - riuscito o fallito - viene registrato nel registro del ciclo di fatturazione. Passa a **Abbonamenti > Registri del ciclo di fatturazione** per visualizzare questa cronologia.

![Elenchi dei registri del ciclo di fatturazione](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Lettura di un elemento del registro del ciclo di fatturazione

Ogni voce del registro registra:

- **Abbonamento** - Quale abbonamento del cliente appartiene a questo tentativo di fatturazione
- **Numero del ciclo** - Ciclo di fatturazione sequenziale (Ciclo 1 = primo addebito dopo la prova)
- **Data di fatturazione** - Quando è stato effettuato l'addebito
- **Stato** - In sospeso, in elaborazione, Riuscito, Fallito o Riprova
- **Scomposizione dell'importo**:
  - **Importo base** - Il prezzo del piano prima di eventuali modifiche
  - **Importo quantità** - Costo aggiuntivo per la quantità di posti/unità
  - **Importo accessori** - Costo totale degli accessori attivi
  - **Importo sconto** - Sconti applicati complessivi
  - **Importo totale** - L'importo finale addebitato (o tentato)
- **Metodo di pagamento** - La carta o il metodo di pagamento utilizzato
- **ID transazione del provider** - Il numero di riferimento del provider di pagamento (utile per le ricerche di rimborso)
- **Motivo del fallimento** - Se la fatturazione è fallita, perché è andata in fallo (es. carta rifiutata, fondi insufficienti)

### Diagnosi degli errori di pagamento

Se un cliente ti contatta per un problema di fatturazione, trova il suo abbonamento e controlla i registri del ciclo di fatturazione. Il campo **Motivo del fallimento** spiega cosa è andato storto. I motivi comuni di fallimento includono:

- **Carta rifiutata** - La carta del cliente è stata rifiutata dalla banca
- **Fondi insufficienti** - Il saldo del conto era troppo basso al momento della fatturazione
- **Carta scaduta** - Il metodo di pagamento salvato è scaduto
- **Errore di rete** - Un problema temporaneo di connessione con il fornitore di pagamento - di solito si risolve al tentativo successivo

Per i fallimenti persistenti, invia il cliente a modificare il metodo di pagamento nelle sue impostazioni del conto.

## Come vengono eseguiti i rinnovi

Ogni addebito di rinnovo riuscito crea un nuovo ordine pagato per quel ciclo di fatturazione - non è solo un record di pagamento. Questo ordine scorre attraverso il tuo normale processo di evasione esattamente come un ordine effettuato al checkout:

- **Prodotti fisici** - L'ordine di rinnovo entra nella tua normale coda di evasione per la scelta, imballaggio e spedizione. Non viene allocato automaticamente in scorta non appena la carta viene addebitata, quindi un calo temporaneo di scorte non blocca mai un addebito che è già riuscito - vedrai comunque l'ordine e puoi evaderlo man mano che le scorte lo permettono.
- **Prodotti digitali** - L'accesso (link per il download, chiavi per le licenze) viene nuovamente concesso automaticamente non appena viene creato l'ordine di rinnovo, esattamente come accadrebbe per un acquisto iniziale.

Gli ordini di rinnovo copiano i dettagli di consegna e fatturazione dall'ordine che ha avviato l'abbonamento, quindi non devi rientrare nulla. Non hanno un marchio speciale nella lista **Ordini**, ma puoi sempre tracciare un ciclo specifico al suo ordine: apri **Abbonamenti > Registri del ciclo di fatturazione**, fai clic sulla voce del registro per quel ciclo e il campo **Ordine** ti porterà direttamente ad esso.

## Email per gli abbonamenti automatici

Spwig invia automaticamente le email del ciclo vitale degli abbonamenti - non hai bisogno di attivarle manualmente. Quelle che i commercianti chiedono di più:

| Email | Quando viene inviata |
|-------|------------------|
| **Promemoria per il rinnovo** | Prima di un rinnovo imminente |
| **Fine della prova** | Prima che una prova gratuita o a prezzo ridotto si trasformi in fatturazione completa |
| **Pagamento fallito** | Immediatamente dopo che un rinnovo non è riuscito, e nuovamente come notifica finale se il periodo di tolleranza sta per scadere (dunning) |
| **Conferma di annullamento** | Quando un abbonamento viene annullato |

Spwig invia anche email di benvenuto, di successo del pagamento, di sospensione/riattivazione, di scadenza, di riattivazione, di modifica del piano e di scadenza del metodo di pagamento nei punti rilevanti del ciclo vitale di un abbonamento.

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Tutti questi sono modelli di email normali — consulta [Modelli di email](/help/email-templates) per revisionarne o personalizzarne il contenuto e verificare che siano attivi.

## Accesso self-service per i clienti

I clienti non devono contattarti per modifiche di sottoscrizione quotidiane — possono gestire le proprie sottoscrizioni dal proprio account: visualizzare dettagli e cronologia dei pagamenti, sospendere, riprendere, annullare e aggiornare il metodo di pagamento in archivio. Questo copre la maggior parte delle richieste che altrimenti finirebbero nella tua coda di supporto, quindi quando un cliente contatta per la sottoscrizione, è opportuno verificare per primo se abbia già provato la pagina del loro account prima di apportare la modifica per loro nell'amministrazione.

## Suggerimenti

- Controlla il filtro **Scadenza** ogni settimana per individuare le sottoscrizioni a rischio di abbandono. Un'email veloce al cliente spesso risolve i problemi di pagamento prima che scada il periodo di tolleranza.
- I registri del ciclo di fatturazione sono di sola lettura — vengono creati automaticamente e non possono essere modificati. Questo garantisce una tracciabilità affidabile.
- Se la sottoscrizione di un cliente mostra **Scadenza** ma ha già aggiornato il metodo di pagamento, il prossimo tentativo automatico prenderà in carico la nuova carta. I tentativi seguono la pianificazione del periodo di tolleranza configurata nel piano.
- Le sottoscrizioni **Scadute** non vengono eliminate — rimangono visibili per i report. Usa i filtri delle date per concentrarti sulle sottoscrizioni attualmente attive.
- Per le sottoscrizioni in **Prova**, controlla la **Data di fine prova** per prevedere le prime fatturazioni imminenti e affrontare in modo proattivo eventuali problemi con il metodo di pagamento.
- Se un cliente dice che un rinnovo fisico "non è stato spedito", controlla la tua normale coda di evasione invece della registrazione della sottoscrizione — gli ordini di rinnovo vengono evasi nello stesso modo di qualsiasi altro ordine e non saltano la coda.