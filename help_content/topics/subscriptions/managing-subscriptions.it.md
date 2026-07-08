---
title: Gestione delle iscrizioni dei clienti
---

La sezione delle iscrizioni dei clienti ti dà una visione completa di tutte le iscrizioni ricorrenti attive, sospese e annullate nel tuo negozio. Da qui puoi monitorare la salute del pagamento, visualizzare i dettagli delle singole iscrizioni e prendere provvedimenti quando si verificano problemi.

## Visualizzazione delle iscrizioni dei clienti

Naviga verso **Iscrizioni > Iscrizioni dei clienti** per visualizzare l'elenco completo delle iscrizioni di tutti i clienti.

![Elenco delle iscrizioni dei clienti](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

L'elenco mostra per ogni iscrizione il cliente, il nome del piano, lo stato corrente, la data del prossimo pagamento e il numero di cicli di pagamento completati.

### Filtraggio e ricerca

Utilizza il pannello di filtro a destra per restringere le iscrizioni in base a:

- **Stato** — Filtra per Attivo, Prova, In ritardo, Sospeso, Annullato o Scaduto
- **Piano** — Visualizza le iscrizioni per un piano specifico
- **Modalità del provider** — Nativa (gestita da Stripe/PayPal) o di backup (fatturazione interna)

Utilizza la barra di ricerca per trovare iscrizioni in base all'indirizzo email del cliente.

## Stati delle iscrizioni

Comprendere ogni stato ti aiuta a identificare le iscrizioni che richiedono attenzione:

| Stato | Cosa significa |
|--------|---------------|
| **Prova** | Il cliente è nel periodo di prova gratuito o a prezzo ridotto |
| **Attivo** | L'iscrizione è in salute — i pagamenti sono aggiornati e l'accesso è attivo |
| **In ritardo** | Un tentativo di pagamento è fallito — il sistema sta riprovando. Il cliente mantiene l'accesso durante il periodo di grazia |
| **Sospeso** | L'iscrizione è temporaneamente sospesa — nessun pagamento, nessun accesso |
| **Annullato** | L'annullamento è stato richiesto. Il cliente potrebbe ancora avere accesso fino alla data di fine periodo |
| **Scaduto** | L'iscrizione è completamente terminata — scaduto il periodo di prova, raggiunto il numero massimo di cicli di pagamento o trascorso il periodo di annullamento |

Le iscrizioni che sono **In ritardo** richiedono la maggiore attenzione — se i pagamenti continuano a fallire e il periodo di grazia termina, l'iscrizione verrà sospesa.

## Visualizzazione dei dettagli di un'iscrizione

Fai clic su qualsiasi iscrizione per aprire la vista dettagliata. Questo mostra:

### Periodo di pagamento corrente

- **Inizio / Fine del periodo corrente** — Le date dell'intervallo di pagamento attivo
- **Data del prossimo pagamento** — Quando verrà tentato il prossimo addebito
- **Data dell'ultimo pagamento** e **Stato dell'ultimo pagamento** — Risultato dell'ultimo tentativo di pagamento
- **Conteggio dei cicli di pagamento** — Quanti cicli di pagamento riusciti sono stati completati

### Informazioni sull'iscrizione

- **Piano** e **Livello di prezzo** — Qual è il piano e la frequenza di pagamento del cliente
- **Prodotto / Variante** — Il prodotto del catalogo collegato a questa iscrizione (se applicabile)
- **Quantità** — Numero di posti o unità (per piani basati sulla quantità)
- **Token di pagamento** — Il metodo di pagamento memorizzato utilizzato per il pagamento ricorrente

### Dettagli della prova

Se l'iscrizione è in prova, la **Data di fine prova** mostra quando la prova del cliente scade e inizia il pagamento completo.

### Dettagli sull'annullamento

Per le iscrizioni annullate, puoi vedere:

- **Tipo di annullamento** — Se l'annullamento è stato immediato, alla fine del periodo o programmato
- **Annullato il** — Quando è stata richiesta l'annullamento
- **Motivo dell'annullamento** — Note sul motivo per cui il cliente ha annullato (se registrato)
- **Data di riacquisto** — L'ultima data in cui il cliente può riacquistare senza riascriversi da zero

### Periodo di grazia e impegni

- **Data di fine del periodo di grazia** — Se un pagamento è fallito, mostra la scadenza prima che l'accesso venga sospeso
- **Data di fine dell'impegno minimo** — Per i piani con impegni minimi, la data più precoce per l'annullamento

## Sospensione di un'iscrizione

Una sospensione dell'iscrizione ferma temporaneamente i pagamenti e sospende l'accesso. Questo è utile per i clienti che desiderano prendere una pausa senza annullare completamente.

Per visualizzare le iscrizioni sospese, filtra per **Stato: Sospeso**. La vista dettagliata mostra:

- **Sospeso il** — Quando è iniziata la sospensione
- **Motivo della sospensione** — Note sul motivo per cui è stata sospesa
- **Data di ripresa automatica** — Se impostata, la data in cui l'iscrizione riprenderà automaticamente i pagamenti e l'accesso

Le sottoscrizioni riprendono automaticamente nella data di ripresa automatica o quando il cliente reattiva manualmente la sottoscrizione.

## Registri del ciclo di fatturazione

Ogni tentativo di fatturazione — riuscito o fallito — viene registrato nel registro del ciclo di fatturazione. Passa a **Sottoscrizioni > Registri del ciclo di fatturazione** per visualizzare questa cronologia.

![Elenco dei registri del ciclo di fatturazione](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Lettura di un'entry del registro del ciclo di fatturazione

Ogni entry del registro registra:

- **Sottoscrizione** — A quale sottoscrizione del cliente appartiene questo tentativo di fatturazione
- **Numero del ciclo** — Ciclo di fatturazione sequenziale (Ciclo 1 = primo addebito dopo il periodo di prova)
- **Data di fatturazione** — Quando è stato tentato l'addebito
- **Stato** — In sospeso, In elaborazione, Riuscito, Fallito o In ripetizione
- **Scomposizione dell'importo**:
  - **Importo base** — Il prezzo del piano prima di qualsiasi aggiustamento
  - **Importo per quantità** — Addebito aggiuntivo per la quantità di posti/unità
  - **Importo degli add-on** — Costo totale degli add-on attivi
  - **Importo dello sconto** — Totale degli sconti applicati
  - **Importo totale** — L'importo finale addebitato (o tentato)
- **Metodo di pagamento** — La carta o il metodo di pagamento utilizzato
- **ID transazione del fornitore** — Il numero di riferimento del fornitore di pagamento (utile per le ricerche di rimborso)
- **Motivo del fallimento** — Se la fatturazione è fallita, spiega il motivo (es. carta rifiutata, fondi insufficienti)

### Diagnosi dei fallimenti dei pagamenti

Se un cliente ti contatta riguardo a un problema di fatturazione, trova la sua sottoscrizione e controlla i registri del ciclo di fatturazione. Il campo **Motivo del fallimento** spiega cosa è andato storto. I motivi di fallimento comuni includono:

- **Carta rifiutata** — La carta del cliente è stata rifiutata dalla sua banca
- **Fondi insufficienti** — Il saldo dell'account era troppo basso al momento della fatturazione
- **Carta scaduta** — Il metodo di pagamento salvato è scaduto
- **Errore di rete** — Un problema temporaneo di connessione con il fornitore di pagamento — di solito si risolve con un nuovo tentativo

Per fallimenti persistenti, invia il cliente a aggiornare il proprio metodo di pagamento nelle impostazioni del proprio account.

## Consigli

- Controlla il filtro **In ritardo** settimanalmente per individuare sottoscrizioni a rischio di churn. Un rapido email al cliente spesso risolve i problemi di pagamento prima che scada il periodo di grazia.
- I registri del ciclo di fatturazione sono di sola lettura — vengono creati automaticamente e non possono essere modificati. Questo garantisce un registro di audit affidabile.
- Se una sottoscrizione del cliente mostra **In ritardo** ma il cliente ha già aggiornato il proprio metodo di pagamento, il prossimo tentativo automatico riprenderà la nuova carta. I tentativi seguono la programmazione del periodo di grazia configurata nel piano.
- Le sottoscrizioni **Scadute** non vengono eliminate — rimangono visibili per i report. Utilizza i filtri per data per concentrarti sulle sottoscrizioni attive.
- Per le sottoscrizioni in **Prova**, controlla la **Data di fine prova** per anticipare i prossimi addebiti iniziali e affrontare in modo proattivo eventuali problemi con il metodo di pagamento.