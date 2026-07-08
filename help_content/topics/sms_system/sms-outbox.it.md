---
title: Cassa di uscita SMS
---

La cassa di uscita SMS è un registro completo di ogni messaggio di testo che il tuo negozio ha tentato di inviare. Utilizzala per confermare che le notifiche siano arrivate ai clienti, investigare i fallimenti di consegna e comprendere l'attività complessiva di messaggistica.

Naviga verso **Sistema SMS > Cassa di uscita SMS** per visualizzare il registro dei messaggi.

![Elenco della cassa di uscita SMS con badge di stato](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Leggere la cassa di uscita

Ogni riga nella cassa di uscita rappresenta un tentativo di messaggio e mostra:

- **Telefono** — il numero di telefono del destinatario
- **Tipo di messaggio** — SMS o WhatsApp
- **Stato** — lo stato corrente di consegna (vedi di seguito)
- **Creato** — quando è stato creato il messaggio
- **Inviato il** — quando il messaggio è stato inviato al provider

La barra riassuntiva in alto mostra i conteggi aggregati per gli stati più importanti a colpo d'occhio.

## Stati dei messaggi

| Stato | Significato |
|--------|---------|
| In attesa | Il messaggio è in attesa di essere preso in carico dalla coda di invio |
| In coda | Il messaggio è stato messo in coda e verrà inviato presto |
| Inviato | Il provider ha accettato il messaggio per la consegna |
| Consegnato | Il provider ha confermato che il messaggio è arrivato al dispositivo del destinatario |
| Fallito | Il provider ha rifiutato o non è riuscito a consegnare il messaggio |
| Saltato | L'invio è stato saltato intenzionalmente (vedi le ragioni del salto di seguito) |
| Registrato in sandbox | Il messaggio è stato registrato solo (il negozio è in modalità test/sandbox) |

> **Inviato vs Consegnato:** Uno stato **Inviato** significa che il messaggio è uscito dal tuo negozio e è stato accettato dal provider. Uno stato **Consegnato** significa che il provider ha ricevuto un ricevuto di consegna dal carrier. Non tutti i provider supportano i ricevuti di consegna — se il tuo provider non lo fa, i messaggi potrebbero mostrare **Inviato** ma mai progredire a **Consegnato**, che è normale.

## Visualizzare i dettagli del messaggio

Fai clic su qualsiasi riga nella cassa di uscita per visualizzare i dettagli completi di quel messaggio:

- Il testo completo del **Messaggio** inviato
- L'**ID del messaggio del provider** — il numero di riferimento dal provider SMS (utile quando si contatta il supporto del provider)
- Il **Messaggio di errore** (per i messaggi falliti) — l'esatto errore restituito dal provider
- Il **Conteggio dei tentativi** — quante volte Spwig ha tentato di inviare il messaggio
- Tutti gli orari (creato, in coda, inviato, consegnato)

## Filtrare la cassa di uscita

Utilizza i filtri a destra per restringere l'elenco:

- **Stato** — mostra solo i messaggi con uno stato specifico
- **Tipo di messaggio** — mostra solo SMS o solo messaggi WhatsApp
- **Data** — filtra per il giorno in cui è stato creato il messaggio

La casella di ricerca in alto ti permette di cercare per numero di telefono, contenuto del messaggio o ID del messaggio del provider.

## Comprendere le ragioni del salto

I messaggi saltati non sono stati inviati perché Spwig ha determinato che l'invio non era appropriato o necessario. Le ragioni comuni del salto:

| Ragione del salto | Cosa significa |
|-------------|---------------|
| `user_preference_disabled` | Il cliente ha disattivato le notifiche SMS nelle impostazioni del proprio account |
| `unsubscribed` | Il cliente si è disiscritto dalle notifiche SMS |
| `no_provider` | Non è configurato alcun account predefinito attivo per il provider SMS |
| `template_inactive` | Il modello per questo tipo di notifica è inattivo |

Un messaggio saltato non è un fallimento — significa che il sistema ha funzionato come previsto. Tuttavia, un alto numero di salti `no_provider` indica che devi configurare e attivare un account del provider SMS.

## Risoluzione dei problemi di consegna fallita

Se i messaggi mostrano uno stato **Fallito**, segui questi passaggi:

1. Fai clic sul messaggio fallito per visualizzare il suo **Messaggio di errore**
2. Cause comuni di errore:

   | Errore | Probabile causa |
   |-------|-------------|
   | Numero di telefono non valido | Il numero di telefono del cliente è mancante o non è nel formato E.164 |
   | Autenticazione fallita | Le credenziali del provider sono invalido o scadute — aggiornale in **SMS Provider Accounts** |
   | Account sospeso | Il tuo account del provider è stato sospeso — accedi al dashboard del provider |
   | Fondi insufficienti | Il saldo del tuo account del provider è troppo basso — riforniscilo |
   | Rifiuto del carrier | Il carrier di destinazione ha bloccato il messaggio (spesso a causa del filtraggio del contenuto) |

3. Dopo aver risolto il problema sottostante, i futuri messaggi verranno inviati normalmente — l'outbox è un log di sola lettura e i singoli messaggi non possono essere inviati manualmente

## L'outbox è di sola lettura

L'Outbox SMS è un registro solo. Non puoi aggiungere messaggi all'outbox manualmente, né puoi rinviare singoli messaggi da qui. I messaggi vengono inviati automaticamente da Spwig quando si verificano gli eventi rilevanti (es. un ordine è stato effettuato).

## Consigli

- Controlla l'outbox dopo un periodo di alta attività per confermare che tutti i messaggi di conferma degli ordini siano stati consegnati con successo
- Se un cliente dice di non aver ricevuto un SMS, cerca nell'outbox per il loro numero di telefono per verificare se il messaggio è stato inviato, fallito o saltato
- Un aumento improvviso di messaggi **Falliti** indica generalmente un problema con le credenziali del provider o con il saldo dell'account — controlla immediatamente questi aspetti
- Se vedi molti messaggi **Saltati** con motivo `no_provider`, vai a **SMS System > SMS Provider Accounts** e assicurati che un account predefinito attivo sia configurato
- La gerarchia delle date in alto nell'elenco ti permette di navigare rapidamente per giorno, mese o anno per esaminare i messaggi storici