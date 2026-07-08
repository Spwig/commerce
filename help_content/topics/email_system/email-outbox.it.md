---
title: Posta in uscita
---

La Posta in uscita è un registro completo di ogni email che il tuo negozio ha inviato o ha tentato di inviare — conferme di ordine, aggiornamenti di spedizione, rapporti amministrativi e tutti gli altri messaggi transazionali. Utilizzala per confermare le consegne, investigare i fallimenti e gestire la coda delle email.

Naviga verso **Sistema Email > Posta in uscita** per visualizzare il registro delle email.

![Elenco della posta in uscita con badge di stato](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Leggere la posta in uscita

La barra riassuntiva in alto mostra i conteggi per ogni categoria di stato. L'elenco sottostante mostra singole email con:

- **Oggetto** — la riga dell'oggetto dell'email
- **A** — l'indirizzo email del destinatario
- **Da** — l'indirizzo del mittente utilizzato
- **Stato** — lo stato corrente di consegna
- **In coda da** — quando l'email è entrata in coda
- **Inviata il** — quando l'email è stata inviata al fornitore
- **Conteggio dei tentativi** — quante volte è stato effettuato un tentativo di invio

## Stati delle email

| Stato | Significato |
|-------|------------|
| In coda | L'email è in attesa nella coda per essere inviata |
| In invio | L'email è attualmente in fase di invio al fornitore |
| Inviata | Il fornitore ha accettato l'email |
| In sospeso | L'email è sospesa e non verrà inviata fino a quando non verrà rilasciata |
| Registrata | L'email è stata registrata ma non inviata (modalità di test o configurazione solo per il logging) |
| Fallita | Il fornitore ha rifiutato o non è riuscito a consegnare l'email |
| Rimbalzata | L'email è stata inviata ma è tornata indietro dal server email del destinatario |
| Saltata | L'invio è stato saltato per un motivo del sistema |

## Visualizzare i dettagli delle email

Fai clic su qualsiasi email nell'elenco per visualizzare i dettagli completi:

- Il completo **Corpo HTML** e **Corpo Testo** dell'email
- **ID Messaggio del Fornitore** — il riferimento dal tuo fornitore email (usa questo quando contatti il supporto del fornitore)
- **Messaggio di errore** — l'esatto errore per le email fallite o rimbalzate
- **Conteggio dei tentativi** e **Massimo numero di tentativi** — quante volte è stato effettuato l'invio
- Tutti gli orari: creato, in coda, inviato e fallito

## Filtrare la posta in uscita

Utilizza i filtri a destra per restringere la tua visione:

- **Stato** — mostra email di uno specifico stato di consegna
- **Data** — filtra per quando le email sono state create o inviate
- **Tipo di modello** — mostra solo email di un tipo specifico di notifica (es. solo conferme di ordine)

La casella di ricerca in alto cerca per oggetto, indirizzo del destinatario, indirizzo del mittente o ID messaggio del fornitore.

## Rilasciare email in sospeso

Le email nello stato **In sospeso** sono sospese — non verranno inviate fino a quando non le rilasci. Un'email potrebbe essere in sospeso se il tuo negozio era in modalità manutenzione quando è stata generata, o se un'azione amministrativa l'ha messa in sospeso.

Per rilasciare le email in sospeso:
1. Seleziona le email che desideri rilasciare (spunta le caselle a sinistra)
2. Scegli **Rilascia email in sospeso per la consegna** dal menu a discesa **Azioni**
3. Fai clic su **Vai**

Le email rilasciate passano allo stato **In coda** e vengono inviate nel prossimo ciclo di elaborazione della coda.

## Email pianificate

Alcune email sono pianificate per essere inviate in un momento futuro — ad esempio, i report settimanali sono pianificati per essere inviati in una data e un'ora specifiche. Naviga verso **Sistema Email > Email Pianificate** per visualizzare le prossime inviate pianificate.

L'elenco delle email pianificate mostra:

- **Tipo di modello** — il tipo di email pianificata
- **Email del destinatario** — l'indirizzo a cui verrà inviata
- **Pianificata per** — la data e l'ora in cui è prevista l'invio
- **Stato** — In sospeso (non ancora inviata), Inviata o Fallita

Le email pianificate vengono elaborate automaticamente quando arriva l'ora pianificata — non è necessaria alcuna azione manuale.

## Risoluzione dei problemi di consegna fallita

Se le email mostrano uno stato **Fallita**, fai clic per visualizzare il messaggio di errore e segui questi passaggi:

### Cause comuni e soluzioni

| Symptoma | Probabile causa | Cosa fare |
|---------|-------------|------------|
| "Autenticazione fallita" | Le credenziali del fornitore di email non sono valide | Aggiorna le credenziali in **Email System > Email Accounts** |
| "Connessione rifiutata" / "Timeout" | Il server di email non è raggiungibile | Controlla la pagina di stato del fornitore di email; testa la connessione in **Email Accounts** |
| "Destinatario non valido" | L'indirizzo email del cliente è malformato | Controlla l'account del cliente e correggi il loro indirizzo email |
| Email rimbalzate | Il server di posta del destinatario ha rifiutato l'email | L'indirizzo potrebbe non esistere o la sua casella di posta potrebbe essere piena; non riprova troppo spesso |
| Tasso di fallimento elevato improvviso | Problema del fornitore o credenziali scadute | Controlla lo stato del fornitore; riconfigura la connessione in **Email Accounts** |

### Verifica la connessione del tuo account email

Se molte email stanno fallendo, testa il tuo account email:

1. Vai a **Email System > Email Accounts**
2. Trova il tuo account attivo e controlla lo stato **Connection**
3. Se la connessione mostra un errore, fai clic sull'account e usa l'opzione **Test Connection** per diagnosticare il problema

### Comportamento di riprova

Spwig riprova automaticamente le email fallite fino al limite **Max Retries**. Il conteggio delle riprova mostrato su ogni email ti dice quante volte è stata tentata. Una volta raggiunto il limite di riprova, l'email rimane nello stato **Failed** e non vengono più effettuate riprova automatiche.

## Email rimbalzate

Una email **Bounced** è stata inviata ma restituita dal server di posta del destinatario. Esistono due tipi di rimbalzo:

- **Hard bounce** — l'indirizzo email non esiste o il dominio non accetta email. Non riprova i rimbalzi hard; l'indirizzo non è valido
- **Soft bounce** — un problema temporaneo (casella piena, server temporaneamente non disponibile). Potrebbe riuscire con la riprova

I rimbalzi ripetuti allo stesso indirizzo possono danneggiare la reputazione del mittente con i fornitori di email. Se vedi rimbalzi ripetuti allo stesso indirizzo del cliente, aggiorna o elimina quell'indirizzo dall'account del cliente.

## Consigli

- Controlla la posta in uscita dopo eventi importanti come un flash sale o un lancio di prodotti di grandi dimensioni per confermare che tutte le email di conferma degli ordini siano state inviate con successo
- Se un cliente dice di non aver ricevuto un'email, cerca la posta in uscita per il loro indirizzo email per vedere se è stata inviata, fallita o saltata
- Un aumento improvviso di fallimenti indica di solito un problema di credenziale o account — controlla immediatamente **Email Accounts**
- Lo stato **Held** non è un fallimento — significa solo che l'email è in attesa. Rilascia le email in sospeso quando sei pronto a inviarle
- Usa il filtro **Template Type** per controllare rapidamente tutte le email di un tipo — ad esempio, verifica che tutte le conferme degli ordini degli ultimi 7 giorni abbiano uno stato **Sent**
- La navigazione gerarchica per le date (giorno / mese / anno) in alto nell'elenco è utile per controllare la posta in uscita per un periodo specifico