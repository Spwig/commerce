---
title: Configurazione Email
---

La configurazione email controlla come il tuo negozio invia le email transazionali: conferme d'ordine, notifiche di spedizione, reset della password e altro ancora. Spwig include un server SMTP integrato e supporta provider email esterni per una maggiore consegnabilità.

![Account email](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Provider Disponibili

| Provider | Descrizione |
|----------|-------------|
| **SMTP Integrato** | Server email gratuito e self-hosted incluso con Spwig. Firma DKIM automatica. |
| **Gmail API** | Invia tramite il tuo account Gmail o Google Workspace utilizzando l'autenticazione OAuth. |
| **SMTP Generico** | Collega qualsiasi server SMTP (SendGrid, Mailgun, Amazon SES o il tuo server di posta). |

## Configurazione Email

Vai a **Impostazioni > Account Email** e fai clic su **Aggiungi Account Email** per avviare la procedura guidata di configurazione.

### Passaggio 1: Seleziona il Provider

Scegli il tuo provider email. Il server SMTP integrato è l'opzione più semplice per iniziare: non richiede account esterni.

### Passaggio 2: Configura le Credenziali

Inserisci le credenziali per il provider scelto:

- **SMTP Integrato** — Non sono necessarie credenziali. Il server viene eseguito sulla tua installazione di Spwig.
- **Gmail API** — Autenticati tramite Google OAuth. Verrai reindirizzato per accedere con il tuo account Google.
- **SMTP Generico** — Inserisci l'indirizzo del server SMTP, la porta, il nome utente e la password.

### Passaggio 3: Configurazione del Mittente

Imposta l'identità del mittente per le email in uscita:

- **Email del Mittente** — L'indirizzo email che appare nel campo "Da" (es. ordini@tuonnegozio.com)
- **Nome del Mittente** — Il nome visualizzato accanto all'indirizzo email (es. "Nome del Tuo Negozio")
- **Email di Risposta** — Dove vengono indirizzate le risposte dei clienti (può differire dall'indirizzo Da)

### Passaggio 4: Validazione DNS

Verifica i record di autenticazione email del tuo dominio. La procedura guidata controlla tre record DNS:

| Record | Scopo |
|--------|---------|
| **SPF** | Autorizza il tuo server a inviare email a nome del tuo dominio |
| **DKIM** | Firma digitalmente le email per dimostrare che non sono state manomesse |
| **DMARC** | Indica ai server riceventi cosa fare con le email che non superano i controlli SPF/DKIM |

Per ogni record, la procedura guidata mostra:
- **Stato attuale** — Se il record è configurato correttamente
- **Valore richiesto** — Il record DNS esatto da aggiungere presso il tuo registrar di dominio
- **Stato di propagazione** — Se le modifiche recenti sono state applicate (le modifiche DNS possono richiedere fino a 48 ore)

Il server SMTP integrato genera automaticamente le chiavi DKIM per il tuo dominio.

### Passaggio 5: Invia Email di Test

Invia un'email di test per verificare che tutto funzioni:
1. Inserisci un indirizzo email del destinatario
2. Fai clic su **Invia Test**
3. Controlla la tua casella di posta in arrivo per il messaggio di test
4. Verifica che l'email arrivi senza avvisi di spam

### Passaggio 6: Salva e Attiva

Salva la configurazione e imposta l'account come attivo. Segnalalo come **Predefinito** se deve essere l'account email principale.

## Modelli Email

Spwig include oltre 30 modelli email per ogni evento transazionale. Vai a **Impostazioni > Modelli Email** per gestirli.

### Tipi di Modelli

I modelli coprono tutti gli eventi del negozio, tra cui:
- **Ciclo di Vita dell'Ordine** — Conferma, elaborazione, spedito, consegnato, annullato
- **Pagamento** — Ricevuta, conferma di rimborso, pagamento non riuscito
- **Account Cliente** — Benvenuto, reset password, verifica email
- **Biglietti Regalo** — Consegna, notifica di saldo
- **Spedizione** — Aggiornamenti di tracciamento, conferma di consegna
- **Prodotti Digitali** — Link di download, chiavi di licenza
- **Marketing** — Recupero carrello abbandonato, richieste di recensione

### Personalizzazione dei Modelli

1. Vai all'elenco dei modelli
2. Fai clic su un modello per modificarlo
3. Modifica la riga dell'oggetto, l'intestazione, il contenuto del corpo e il piè di pagina
4. Usa le variabili del modello (es. `{{ order.number }}`, `{{ customer.name }}`) per il contenuto dinamico
5. Anteprima l'email prima di salvare

### Supporto Multi-Lingua

I modelli di email supportano più lingue:
- Ogni modello può avere traduzioni per tutte le lingue attive del tuo negozio
- Il sistema invia le email nella lingua preferita del cliente
- **Catena di fallback della lingua** — Se una traduzione non è disponibile, il sistema ricorre alla lingua predefinita del negozio
- Utilizza la funzione **Traduzione AI** per tradurre automaticamente i modelli in altre lingue

### Clonazione dei modelli

Per creare una versione personalizzata di un modello di sistema:
1. Apri il modello che desideri modificare
2. Clicca su **Clona modello**
3. Modifica la versione clonata
4. Il clone ha la priorità rispetto al modello di sistema originale

## Coda delle email

Monitora le email in uscita in **Impostazioni > Coda email**:

- **In coda** — Email in attesa di invio
- **Invio in corso** — Attualmente in trasmissione
- **Inviato** — Consegnato con successo
- **Fallito** — Non è stato possibile consegnare (con dettagli dell'errore)
- **Rimbalzato** — Rifiutato dal server di posta del destinatario

Clicca su qualsiasi email per visualizzarne tutti i dettagli, inclusi destinatario, oggetto, ora di invio e stato di consegna.

## Tracciamento della consegna

Traccia l'interazione con le email:
- **Aperture** — Numero di destinatari che hanno aperto l'email
- **Clic** — Clic sui link all'interno dell'email
- **Rimbalzi** — Tracciamento dei rimbalzi hard e soft
- **Segnalazioni** — Segnalazioni di spam da parte dei destinatari

## Multipli account

Puoi configurare più account email:
- **Account predefinito** — Utilizzato per tutte le email in uscita a meno che non venga sovrascritto
- **Fallback** — Se l'account predefinito fallisce, le email vengono messe in coda per il nuovo tentativo
- Utilizza account diversi per scopi diversi (ad esempio, uno per le email transazionali, un altro per il marketing)

## Modalità di consegna delle email

Vai a **Impostazioni > Impostazioni negozio** per controllare come il tuo negozio gestisce le email in uscita. Queste impostazioni sono utili durante lo sviluppo e i test.

| Modalità | Descrizione |
|------|-------------|
| **Live** | Le email vengono consegnate normalmente ai destinatari reali |
| **In pausa** | Le email vengono trattenute nella coda e non vengono inviate finché non si torna alla modalità Live |
| **Solo log** | Le email vengono registrate nella casella di uscita ma non vengono mai consegnate |

### Email di reindirizzamento di test

Imposta un indirizzo **Email di reindirizzamento di test** per intercettare tutte le email in uscita e reindirizzarle a un unico indirizzo. Quando impostato, ogni email — indipendentemente dal destinatario reale — viene inviata a quell'indirizzo. Questo è utile per testare i modelli di email senza inviare accidentalmente a clienti reali. Lascia vuoto per inviare le email ai destinatari effettivi.

### Whitelist email sandbox

In modalità sandbox o di sviluppo, puoi limitare la consegna delle email a una whitelist di indirizzi approvati. Verranno consegnate solo le email destinate agli indirizzi presenti nella whitelist. Tutte le altre email vengono registrate ma non inviate. L'email di amministrazione è sempre inclusa automaticamente. Puoi aggiungere fino a 10 indirizzi.

## Suggerimenti

- Inizia con il server **SMTP integrato** per una configurazione rapida, quindi passa a un provider esterno se hai bisogno di volumi di invio più elevati o di una migliore consegnabilità.
- Configura sempre i record **SPF, DKIM e DMARC** — senza di essi, le email hanno molte più probabilità di finire nelle cartelle spam.
- Invia un'**email di test** dopo ogni modifica alle impostazioni per verificare che la consegna funzioni.
- Monitora regolarmente la coda delle email per le email **fallite** o **rimbalzate** — queste indicano problemi di consegnabilità.
- Utilizza un **indirizzo mittente professionale** (ad esempio, ordini@tuonegozio.com) anziché un indirizzo email gratuito per una migliore fiducia e consegnabilità.
- Mantieni i tuoi modelli concisi — le email transazionali dovrebbero fornire informazioni rapidamente, non essere newsletter di marketing.