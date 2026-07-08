---
title: Transazioni di pagamento
---

Le transazioni di pagamento rappresentano il registro completo di ogni evento di pagamento elaborato dal tuo negozio — addebiti, rimborsi, autorizzazioni e altro. Questa sezione include anche i log dei webhook dai tuoi fornitori di pagamento e le intenzioni di pagamento create durante il checkout.

## Transazioni di pagamento

Vai a **Pagamenti > Transazioni di pagamento** per visualizzare ogni transazione elaborata dal tuo negozio.

### Tipi di transazione

| Tipo | Cosa significa |
|------|--------------|
| **Addebito** | Un pagamento immediato — i fondi vengono raccolti al momento della transazione |
| **Autorizzazione** | I fondi vengono bloccati sulla carta del cliente ma non sono ancora raccolti |
| **Cattura** | Raccoglie i fondi da un'autorizzazione precedente |
| **Annulla** | Annulla un'autorizzazione prima che venga catturata |
| **Rimborso** | Restituisce il pagamento al cliente |

### Stati delle transazioni

| Stato | Cosa significa |
|--------|--------------|
| **In sospeso** | La transazione è stata iniziata ma non è ancora stata elaborata |
| **In elaborazione** | È in corso di elaborazione dal fornitore di pagamento |
| **Autorizzato** | I fondi sono bloccati — in attesa di cattura |
| **Completato** | Il pagamento è stato riuscito |
| **Fallito** | Il pagamento è stato rifiutato o è verificato un errore |
| **Annullato** | L'autorizzazione è stata annullata prima della cattura |
| **Rimborsato** | È stato emesso un rimborso completo |
| **Rimborsato parzialmente** | Parte del pagamento è stata restituita |

### Cosa puoi vedere in un registro di transazione

Ogni transazione mostra:
- **ID transazione** — riferimento interno di Spwig
- **ID transazione del fornitore** — il riferimento dal tuo fornitore di pagamento (es. ID addebito di Stripe)
- **Importo** — l'importo della transazione e la valuta
- **Stato** e **Tipo**
- **Email del cliente** e **Nome del cliente**
- **Metodo di pagamento** — tipo (carta di credito, bonifico bancario, ecc.) e ultime 4 cifre
- **Ordine** — l'ordine a cui appartiene questa transazione
- **Account del fornitore** — quale fornitore di pagamento l'ha elaborata
- **Risposta del fornitore** — la risposta tecnica grezza dal fornitore di pagamento
- **Messaggio di errore** — se la transazione è fallita, il motivo fornito dal fornitore
- Timestamp per la creazione, l'ultima modifica e il completamento

### Filtro delle transazioni

Utilizza i filtri dell'amministratore per restringere le transazioni per:
- Stato (es. mostra solo le transazioni fallite)
- Tipo (es. mostra solo i rimborsi)
- Account del fornitore
- Intervallo di date

Questo è utile per la conciliazione alla fine della giornata o per investigare la cronologia dei pagamenti di un cliente specifico.

### Quando una transazione può essere rimborsata?

Una transazione può essere rimborsata quando:
- Il suo stato è **Completato**
- Il suo tipo è **Addebito** o **Cattura**

Per emettere un rimborso, utilizza l'azione **Rimborso** dalla pagina dei dettagli dell'ordine. I rimborsi elaborati tramite l'ordine creano un nuovo registro di transazione del tipo **Rimborso**.

### Flusso di autorizzazione e cattura

Alcuni metodi di pagamento (e alcuni fornitori di pagamento) supportano autorizzazione e cattura separate. Questo è utile se desideri verificare il pagamento prima di spedire:

1. **Autorizza** — I fondi vengono bloccati sulla carta del cliente (stato: `Autorizzato`)
2. **Cattura** — Attivata quando l'ordine viene spedito o completato
3. Se non catturata entro la finestra di autorizzazione, il blocco **scade** automaticamente

Il campo **Scade a** nella transazione mostra quando un'autorizzazione scadrà.

## Webhook dei pagamenti

I fornitori di pagamento inviano eventi webhook per notificare al tuo negozio i cambiamenti nello stato dei pagamenti — ad esempio, quando un pagamento ha successo, fallisce o viene sollevata una controversia. Spwig registra tutti i webhook in arrivo.

Vai a **Pagamenti > Webhook dei pagamenti** per visualizzare il registro.

### Cosa mostrano i registri dei webhook

| Campo | Descrizione |
|-------|-------------|
| **Provider** | Quale fornitore di pagamento ha inviato il webhook |
| **ID evento** | L'identificatore unico dell'evento fornito dal fornitore |
| **Tipo evento** | Il tipo di evento (es. `payment_intent.succeeded`, `charge.refunded`) |
| **Elaborato** | Se Spwig ha agito su questo webhook |
| **Firma verificata** | Se la firma di sicurezza del webhook era valida |
| **Carico utile** | I dati completi inviati dal fornitore |
| **Risultato dell'elaborazione** | Cosa ha fatto Spwig in risposta |
| **Errore di elaborazione** | Qualsiasi errore verificatosi durante l'elaborazione |
| **Ricevuto il** | Quando è arrivato il webhook |

### Utilizzo dei log dei webhook per il troubleshooting

Se un pagamento sembra bloccato o lo stato dell'ordine non è aggiornato dopo il pagamento:

1. Vai a **Pagamenti > Webhook dei pagamenti**
2. Filtra per il fornitore e cerca eventi recenti
3. Controlla la colonna **Elaborato** — un webhook non elaborato potrebbe indicare un problema di consegna
4. Controlla **Firma verificata** — una firma non verificata potrebbe significare che il segreto del webhook è configurato in modo errato
5. Rivedi **Errore di elaborazione** per eventuali messaggi di errore

Gli eventi duplicati vengono gestiti automaticamente — la combinazione di `ID evento` e fornitore è unica, quindi lo stesso webhook non può essere elaborato due volte.

## Intenti di pagamento

Un intento di pagamento traccia il ciclo di vita di un pagamento al checkout dal momento in cui un cliente inizia il processo di pagamento al risultato finale. Gli intenti di pagamento vengono creati automaticamente quando un cliente raggiunge la fase di pagamento al checkout.

Vai a **Pagamenti > Intenti di pagamento** per visualizzare l'elenco.

### Stati degli intenti di pagamento

| Stato | Significato |
|--------|---------|
| **Creato** | L'intento è stato creato, in attesa del metodo di pagamento |
| **Richiesto metodo di pagamento** | In attesa che il cliente inserisca i dettagli della carta |
| **Richiesto conferma** | Dettagli del pagamento inseriti, in attesa di conferma |
| **Richiesto azione** | Il cliente deve completare un'azione (es. autenticazione 3D Secure) |
| **In elaborazione** | Il pagamento sta venendo elaborato |
| **Completato** | Il pagamento è stato completato con successo |
| **Annullato** | Il pagamento è stato abbandonato o annullato |
| **Fallito** | L'attempto di pagamento è fallito |

### Flusso da intento di pagamento a ordine

1. Il cliente raggiunge la fase di pagamento al checkout → Spwig crea un **Intento di pagamento** e un **Ordine** in bozza (non pagato)
2. Il cliente inserisce i dettagli del pagamento e conferma
3. Il fornitore di pagamento elabora il pagamento
4. In caso di successo, l'Ordine viene aggiornato a **Pagato** e l'Intento di pagamento passa a **Completato**
5. Viene creato un **Record di transazione di pagamento** con i dettagli finali della transazione

L'intento di pagamento collega la sessione di checkout, l'account del fornitore e l'ordine — ti dà una visione completa del percorso di checkout del cliente.

### Utilizzo degli intenti di pagamento per il supporto

Se un cliente segnala di aver pagato ma l'ordine mostra come non pagato:

1. Trova l'ordine del cliente in **Ordini**
2. Vai a **Pagamenti > Intenti di pagamento** e cerca gli intenti collegati a quell'ordine
3. Controlla lo stato dell'intento — se è **Completato**, controlla la transazione collegata
4. Se l'intento è **Richiesto azione**, il cliente potrebbe non aver completato l'autenticazione 3D Secure
5. Se l'intento è **Fallito**, i dettagli dell'errore spiegano il motivo per cui il pagamento è stato rifiutato

## Consigli

- Rivedi le transazioni fallite quotidianamente — i pattern di fallimenti (es. un metodo di pagamento specifico o un paese) potrebbero indicare un problema di configurazione o un tentativo di frode.
- I log dei webhook sono fondamentali quando si indaga su discrepanze dei pagamenti.

Se un ordine è stato pagato ma non confermato, i log dei webhook ti diranno di solito cosa è andato storto.
- Le prenotazioni di autorizzazione scadono automaticamente — se utilizzi l'autorizzazione seguita dal prelievo, assicurati che il tuo processo di spedizione prelevi i fondi prima che la finestra di scadenza si chiuda (di solito 7 giorni per la maggior parte dei fornitori).
- Il campo **Risposta del fornitore** sulle transazioni contiene i dati grezzi provenienti dal fornitore di pagamento.

Condividi questo con il team di supporto del tuo fornitore se hai bisogno di aiuto per risolvere un problema specifico relativo a una transazione.
- I fallimenti nella verifica della firma sui webhooks devono essere indagati immediatamente — potrebbero indicare un segreto del webhook non configurato correttamente o un tentativo di inviare eventi webhook fraudolenti al tuo negozio.