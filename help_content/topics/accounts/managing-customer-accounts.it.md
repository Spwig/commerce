---
title: Gestione degli account clienti
---

Gli account clienti permettono ai commercianti di tracciare le informazioni sui clienti, la cronologia degli ordini e le preferenze. Naviga verso **Customers > All Customers** nel sidebar amministrativo per gestire gli account clienti.

![Aggiungi cliente](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Comprendere gli account clienti vs i profili clienti

**Gli account clienti** sono le credenziali di accesso (email/password) archiviate nel modello Utente. **I profili clienti** archiviano informazioni aggiuntive sui clienti come numero di telefono, data di nascita, preferenze e analisi. Ogni account cliente ha un profilo corrispondente che archivia questi dati estesi.

Quando gestisci i clienti nell'amministratore, stai lavorando con i profili clienti che si collegano agli account utente in background.

## Visualizzazione di tutti i clienti

L'elenco dei clienti mostra tutti i clienti registrati con metriche chiave:

| Colonna | Descrizione |
|--------|-------------|
| **Utente** | Nome e indirizzo email del cliente |
| **Stato affiliato** | Se il cliente è anche un partner affiliato |
| **Valore cliente** | Totale importo speso dal cliente (colorato) |
| **Segmento cliente** | Segmento RFM (Campione, Fedele, A rischio, ecc.) |
| **Totale ordini** | Numero di ordini completati |
| **Giorni dall'ultimo ordine** | Recenza dell'ultimo acquisto |
| **Cliente VIP** | Badge se il cliente è contrassegnato come VIP |

### Filtrare i clienti

Utilizza il sidebar dei filtri per restringere l'elenco:

- **Stato affiliato** — È affiliato, Non affiliato, Affiliato in attesa, Attivo, Sospeso, Rifiutato
- **Layout del dashboard** — Layout del dashboard preferito dal cliente
- **Iscrizione alla newsletter** — Se il cliente ha optato per le newsletter
- **Email di marketing** — Se il cliente ha optato per le email promozionali
- **Creato il** — Filtra per data di registrazione

### Ricerca dei clienti

Utilizza la barra di ricerca per trovare clienti per:
- Username
- Indirizzo email
- Nome
- Cognome
- Numero di telefono

## Visualizzazione dei dettagli del cliente

Fai clic sul nome del cliente per visualizzare il loro profilo completo. La pagina dei dettagli del cliente mostra:

![Dettagli cliente](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Sezione Informazioni cliente

Dettagli di contatto di base e stato dell'account:
- **Utente** — Link all'account utente sottostante
- **Telefono** — Numero di telefono del cliente
- **Data di nascita** — Per la verifica d'età e promozioni per compleanni

### Preferenze del dashboard

Come il cliente ha personalizzato il proprio dashboard dell'account:
- **Layout del dashboard** — Vista a griglia, elenco o compatto
- **Mostra cronologia ordini** — Se la cronologia degli ordini appare nel dashboard
- **Mostra lista dei desideri** — Se la lista dei desideri appare nel dashboard
- **Mostra prodotti recenti** — Se i prodotti visualizzati di recente appaiono
- **Mostra raccomandazioni** — Se le raccomandazioni dei prodotti appaiono

### Preferenze di comunicazione

Stato di iscrizione del cliente per varie comunicazioni:
- **Iscrizione newsletter** — Opt-in per le newsletter generali
- **Email di marketing** — Opt-in per le email promozionali
- **Notifiche ordine** — Opt-in per gli aggiornamenti sullo stato dell'ordine

### Analisi cliente

Sintesi in sola lettura del comportamento e del valore del cliente:
- **Sintesi analisi cliente** — Punteggi RFM, segmento, valore vitale
- **Sintesi comportamento acquisti** — Frequenza di acquisto, valore medio dell'ordine, categorie preferite
- **Sintesi engagement** — Ultimo accesso, tasso di apertura email, attività sul sito

Questi campi di analisi vengono calcolati automaticamente e non possono essere modificati manualmente. Per i dettagli, vedi [Comprendere le analisi clienti](customer-analytics.md).

## Creare un account cliente

I commercianti possono creare manualmente gli account clienti per ordini al telefono, prelievi in negozio o per pre-registrare clienti al dettaglio.

1. Fare clic su **+ Aggiungi profilo cliente** in alto a destra
2. Compilare i campi obbligatori e opzionali:

| Campo | Obbligatorio | Descrizione |
|-------|--------------|-------------|
| **Utente** | Sì | Selezionare un account utente esistente o crearne uno nuovo |
| **Telefono** | No | Numero di telefono del cliente |
| **Data di nascita** | No | Per la verifica d'età e campagne per compleanni |
| **Iscrizione newsletter** | No | Opt-in per le newsletter |
| **Email di marketing** | No | Opt-in per le email promozionali |

### Creare un nuovo utente mentre si aggiunge un profilo

Se il cliente non ha ancora un account utente:
1. Fare clic sull'icona **+** accanto al campo Utente
2. Inserire l'**indirizzo email** del cliente (questo diventa il loro nome utente)
3. Inserire opzionalmente il **nome** e il **cognome**
4. Inserire opzionalmente una **password**
5. Selezionare **Invia email di reimpostazione password** se non hai impostato una password
6. Salvare l'account utente
7. Completare i campi del profilo cliente
8. Fare clic su **Salva**

### Email di benvenuto

Dopo aver creato un account cliente:
- Se hai impostato una password, il cliente può accedere immediatamente con quella password
- Se non hai impostato una password, il sistema invia un'email di reimpostazione password in modo che il cliente possa impostare la propria password
- Puoi attivare manualmente un'email di benvenuto attraverso il sistema email a **Marketing > Campagne email**

## Modificare le informazioni del cliente

Per aggiornare le informazioni del cliente:
1. Naviga verso **Customers > All Customers**
2. Fare clic sul nome del cliente
3. Modificare i campi che si desidera aggiornare
4. Fare clic su **Salva**

### Cosa puoi modificare

**Dettagli di contatto:**
- Nome (tramite l'account utente)
- Indirizzo email (tramite l'account utente)
- Numero di telefono
- Data di nascita

**Preferenze:**
- Stato di iscrizione alla newsletter
- Opt-in per email di marketing
- Preferenze per notifiche ordine
- Layout del dashboard e impostazioni di visibilità

### Cosa non puoi modificare

Questi campi vengono calcolati automaticamente in base al comportamento del cliente:
- Totale speso / Valore cliente
- Conteggio ordini
- Segmento cliente (Campione, Fedele, A rischio, ecc.)
- Punteggi RFM
- Previsioni del valore vitale
- Data dell'ultimo ordine
- Sintesi delle analisi

Se questi campi appaiono errati, controlla i dati sottostanti sugli ordini o attiva un ricalcolo manuale a **Customers > Analytics** → **Ricalcola metriche**.

## Note sui clienti

Aggiungi note interne sui clienti per tracciare problemi di supporto, richieste VIP o compiti da seguire.

### Aggiungere una nota

1. Apri il profilo del cliente
2. Scorri fino alla sezione **Note sui clienti** (potrebbe essere una scheda separata)
3. Fare clic su **+ Aggiungi nota**
4. Compilare i dettagli della nota:

| Campo | Descrizione |
|-------|-------------|
| **Tipo di nota** | Generale, Problema di supporto, Lamento, Complimento, Servizio VIP, Richiesta di follow-up, Problema di pagamento, Problema di spedizione |
| **Titolo** | Breve riepilogo della nota |
| **Contenuto** | Contenuto dettagliato della nota |
| **Richiede follow-up** | Selezionare se è necessaria un'azione |
| **Data follow-up** | Data per il follow-up |
| **Completato** | Selezionare quando il follow-up è completato |

### Tipi di note

| Tipo | Caso d'uso |
|------|----------|
| **Nota generale** | Osservazioni generali su un cliente |
| **Problema di supporto** | Registrazione di un ticket di supporto o problema |
| **Lamento** | Lamento del cliente per tracciamento e risoluzione |
| **Complimento** | Feedback positivo sul cliente o sul loro feedback su di te |
| **Servizio VIP** | Richieste di gestione speciale per clienti VIP |
| **Richiesta di follow-up** | Compiti che richiedono un'azione entro una data specifica |
| **Problema di pagamento** | Note su problemi o dispute di pagamento |
| **Problema di spedizione** | Note su problemi di spedizione o richieste di consegna speciali |

### Visualizzazione della cronologia delle note

Tutte le note appaiono in ordine cronologico sul profilo del cliente. Ogni nota mostra:
- Data e ora di creazione
- Creato da (nome del membro dello staff)
- Badge del tipo di nota
- Titolo e contenuto
- Stato del follow-up se applicabile

### Note interne vs note visibili al cliente

Tutte le note sui clienti sono **interne** di default — i clienti non le vedono mai. Sono destinate solo alla comunicazione del team commerciale.

Se devi comunicare con il cliente, utilizza il sistema email a **Marketing > Campagne email** o aggiungi un commento all'ordino specifico.

## Convertire un cliente ospite in un cliente registrato

I clienti ospiti vengono creati automaticamente quando qualcuno completa il checkout senza creare un account. Il loro nome utente segue il modello `guest_10374` dove il numero è un ID unico.

Per convertire un ospite in un cliente registrato:

1. Naviga verso **Customers > All Customers**
2. Cerca l'ospite per l'indirizzo email dell'ordine
3. Fare clic sul profilo del cliente ospite
4. Fare clic sul link **Utente** per modificare l'account utente sottostante
5. Cambia il **username** da `guest_10374` all'indirizzo email reale del cliente
6. Cambia l'**email** per corrispondere
7. Aggiungi opzionalmente il **nome** e il **cognome**
8. Seleziona **Invia email di reimpostazione password** in modo che il cliente possa impostare una password
9. Fare clic su **Salva**

Ora il cliente può accedere con l'indirizzo email e vedrà gli ordini precedenti come cliente ospite nella cronologia degli ordini.

### Perché convertire i clienti ospiti?

- Gli ordini ospite non contano per le analisi o i segmenti dei clienti
- Gli ospiti non possono tracciare gli ordini o accedere alla cronologia degli ordini
- La conversione aumenta il numero di clienti registrati e migliora l'accuratezza delle analisi
- I clienti registrati sono più propensi a effettuare acquisti ripetuti

## Disattivare vs cancellare gli account

### Disattivare un account cliente

La disattivazione impedisce l'accesso ma mantiene tutti i dati:

1. Apri il profilo del cliente
2. Fare clic sul link **Utente** per modificare l'account utente
3. **Deselezionare "Attivo"**
4. Fare clic su **Salva**

**Cosa accade:**
- Il cliente non può accedere
- La cronologia degli ordini è preservata
- Il cliente può essere riattivato in futuro selezionando nuovamente "Attivo"
- Le analisi e le metriche rimangono intatte

**Utilizzare la disattivazione per:**
- Sospensione temporanea di account a causa di dispute sui pagamenti
- Blocco di clienti dannosi
- Clienti che hanno richiesto di smettere di ricevere accesso ma non di cancellare i dati

### Cancellare un account cliente

La cancellazione rimuove l'account e può lasciare orfani la cronologia degli ordini:

1. Apri il profilo del cliente
2. Scorri fino in basso e fare clic su **Cancella**
3. Confermare la cancellazione

**Cosa accade:**
- L'account cliente viene rimosso definitivamente
- Il profilo cliente viene cancellato
- La cronologia degli ordini potrebbe rimanere orfana (gli ordini esistono ma non sono collegati a un cliente)
- Non può essere annullata

**Utilizzare la cancellazione per:**
- Richieste di cancellazione dei dati GDPR/CCPA (esportare i dati prima)
- Account di test che non dovrebbero mai esistere
- Account duplicati creati per errore

### Conformità al GDPR

Prima di cancellare un account cliente in risposta a una richiesta GDPR:

1. Naviga verso **Customers > All Customers**
2. Seleziona il cliente
3. Utilizza l'azione **Esporta dati** per generare un'esportazione completa dei dati
4. Invia l'esportazione al cliente se l'hanno richiesta
5. Poi procedi con la cancellazione

L'esportazione include: profilo cliente, cronologia ordini, indirizzi, note e dati di analisi.

## Consigli

- **Utilizzare i filtri per identificare i clienti ad alto valore** — Filtrare per Valore cliente per trovare i Campioni e i VIP
- **Rivedere regolarmente le note sui clienti** — Controllare i compiti di follow-up aperti almeno una volta a settimana
- **Non modificare manualmente le analisi** — Lasciare che il sistema calcoli automaticamente i punteggi RFM e i segmenti
- **Convertire gli ospiti in modo proattivo** — Dopo che un ospite effettua un secondo acquisto, contattalo e offri di creare un account completo
- **Utilizzare la disattivazione invece della cancellazione** — La disattivazione preserva i dati e può essere annullata se necessario
- **Aggiungere note durante le chiamate di supporto** — Documentare le interazioni di supporto in modo che gli altri membri del team abbiano contesto
- **Impostare date di follow-up** — Utilizzare il sistema di compiti di follow-up nelle note per assicurarsi che niente venga dimenticato
- **Rispettare le preferenze di comunicazione** — Mai inviare email promozionali a clienti che hanno optato per non riceverle

Ricorda: Restituisci SOLO l'oggetto JSON con i campi "title" e "content". Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato sopra.