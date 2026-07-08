---
title: Modelli di email
---

I modelli di email controllano l'aspetto e il contenuto di ogni email automatica che il tuo negozio invia ai clienti e a te stesso — conferme di ordine, aggiornamenti sulla spedizione, reimpostazioni della password, notifiche di rimborso e molto altro. Modificando un modello, si modificheranno tutte le future email di quel tipo; le email precedenti già nell'outbox non saranno influenzate.

Naviga verso **Email System > Email Templates** per visualizzare e gestire i tuoi modelli.

![Elenco dei modelli di email](/static/core/admin/img/help/email-templates/templates-list.webp)

## Tipi di modello

Il tuo negozio include modelli per una vasta gamma di eventi. Sono raggruppati per categoria:

### Email relative all'ordine del cliente
| Modello | Inviato quando |
|----------|-----------|
| Conferma ordine | Un cliente completa un acquisto |
| Conferma pagamento | Un pagamento viene elaborato con successo |
| Ordine spedito | Un ordine viene contrassegnato come spedito |
| Conferma spedizione | Viene aggiunto un numero di tracciamento della spedizione |
| Conferma consegna | Un ordine viene contrassegnato come consegnato |
| Ordine annullato | Un ordine viene annullato |
| Notifica di ritardo | Viene registrato un ritardo su un ordine |
| Notifica di rimborso | Viene emesso un rimborso |

### Email relative all'account
| Modello | Inviato quando |
|----------|-----------|
| Benvenuto nell'account | Un cliente crea un account |
| Invito all'account | Inviti un cliente a creare un account |
| Verifica email | Un cliente verifica il proprio indirizzo email |
| Reimpostazione password | Un cliente richiede una reimpostazione della password |

### Resi
| Modello | Inviato quando |
|----------|-----------|
| Resi: Richiesta ricevuta | Un cliente invia una richiesta di reso |
| Resi: Approvata | Una richiesta di reso viene approvata |
| Resi: Rifiutata | Una richiesta di reso viene rifiutata |
| Resi: Pacchetto ricevuto | L'articolo restituito arriva al tuo indirizzo |
| Resi: Rimborso processato | Viene emesso il rimborso per il reso |

### Notifiche amministrative (inviate a te)
| Modello | Inviato quando |
|----------|-----------|
| Amministratore: Nuovo ordine | Viene effettuato un nuovo ordine |
| Amministratore: Pagamento fallito | Un tentativo di pagamento fallisce |
| Amministratore: Rapporto giornaliero sulle vendite | Viene generato il riepilogo giornaliero delle vendite |
| Amministratore: Avviso di scorte basse | Un prodotto scende al di sotto del limite di scorte |
| Amministratore: Riepilogo settimanale | Viene generato il riepilogo settimanale del negozio |

Altri modelli coprono i traguardi del tracciamento della spedizione, l'attività del programma affiliato, le conferme di prenotazione (se è abilitata la funzione prenotazioni) e gli eventi del programma fedeltà.

## Modifica di un modello

1. Naviga verso **Email System > Email Templates**
2. Trova il modello che desideri modificare. Puoi filtrare per **Tipo modello**, **Lingua** o **Stato** utilizzando i filtri a destra
3. Fai clic sul modello per aprirlo
4. Modifica la **riga Oggetto** (l'oggetto dell'email visualizzato nella casella di posta del cliente)
5. Modifica il **Contenuto HTML** per la versione a pieno design dell'email
6. Modifica opzionalmente il **Contenuto testo** — una versione testuale semplice per i client email che non supportano HTML
7. Fai clic su **Salva**

> **Email HTML:** Il campo del contenuto HTML accetta HTML standard, incluso CSS inline. Spwig lo rende in un'email formattata correttamente. Se utilizzi il markup MJML, viene compilato automaticamente al salvataggio.

## Anteprima di un modello

Prima di salvare, puoi visualizzare come apparirà il modello in un client email:

1. Apri il modello che desideri anteprimare
2. Fai clic sul pulsante **Anteprima** (visibile nell'elenco dei modelli o sulla pagina dettagliata del modello)
3. L'anteprima si apre in una nuova scheda del browser, mostrando l'email renderizzata

Questo ti permette di controllare layout, formattazione e aspetto delle variabili di testo prima che il modello venga reso attivo.

## Variabili del modello

Le variabili sono segnaposti nel tuo modello che Spwig sostituisce con dati reali quando invia l'email. Vengono scritte come `{{ variable_name }}`.

Variabili comuni disponibili nella maggior parte dei modelli:

| Variabile | Sostituito con |
|----------|---------------|
| `{{ customer_name }}` | Il nome completo del cliente |
| `{{ order_number }}` | Il numero di riferimento dell'ordine |
| `{{ order_total }}` | L'importo totale dell'ordine |
| `{{ store_name }}` | Il nome del tuo negozio |
| `{{ store_url }}` | L'indirizzo web del tuo negozio |
| `{{ tracking_number }}` | Il numero di tracciamento del pacco |
| `{{ tracking_url }}` | Un collegamento cliccabile per tracciare il pacco |

Le variabili esatte disponibili dipendono dal tipo di modello. Le variabili rilevanti per un modello relativo a un ordine (come `{{ order_number }}`) non sono disponibili in un modello per l'account (come il Reset della Password). Se includi una variabile che non si applica, apparirà vuota o non sostituita.

## Supporto per le lingue

Ogni tipo di modello può avere una versione per ciascuna lingua supportata dal tuo negozio. Il campo **Lingua** in ogni modello controlla quale versione della lingua è attiva.

Spwig seleziona automaticamente la versione corretta della lingua in base alle preferenze linguistiche del cliente durante l'invio. Se non esiste un modello per la lingua del cliente, Spwig ricorre alla versione in inglese.

Per aggiungere un modello per una nuova lingua:
1. Apri un modello esistente
2. Fai clic su **Clona Modello** dal menu **Azioni**
3. Imposta il **Codice della Lingua** sulla copia per la nuova lingua
4. Traduci il contenuto
5. Attiva il modello clonato

## Clonare, attivare e disattivare i modelli

### Clonare un modello

La clonazione crea una copia esatta di un modello — utile per creare varianti linguistiche o testare versioni diverse senza influenzare il modello attivo.

1. Seleziona uno o più modelli nell'elenco
2. Scegli **Clona i modelli selezionati** dal menu a discesa **Azioni**
3. La copia viene creata come inattiva — modificala e attivala quando sei pronto

### Attivare e disattivare i modelli

Un modello deve essere **Attivo** per essere utilizzato per l'invio. Viene utilizzato un solo modello attivo per tipo e combinazione di lingua alla volta.

Per attivare o disattivare in blocco:
1. Seleziona i modelli
2. Scegli **Attiva i modelli selezionati** o **Disattiva i modelli selezionati** dal menu a discesa **Azioni**

Oppure apri un modello singolo e attiva/disattiva il checkbox **Attivo**.

## Modelli del sistema

I modelli contrassegnati con un badge **Sistema** sono i modelli predefiniti forniti da Spwig. Non possono essere eliminati. Puoi modificarli direttamente o clonarli per creare una versione personalizzata.

## Consigli

- Anteprima sempre un modello dopo averlo modificato per individuare eventuali problemi di formattazione prima che i clienti li vedano
- Mantieni gli oggetti delle email brevi e specifici — `Il tuo ordine #10045 è stato spedito` ha un rendimento migliore rispetto agli oggetti generici come `Aggiornamento dal nostro negozio`
- Modifica anche il contenuto in testo semplice — alcuni client di posta elettronica mostrano solo la versione in testo semplice, e alcuni clienti preferiscono questa opzione
- Clona la versione in inglese di un modello come punto di partenza prima di creare una versione tradotta
- Se desideri testare un cambiamento senza influenzare le email attive, clona il modello, modifica la copia e lascia entrambe attive per un breve periodo mentre verifichi l'anteprima — quindi disattiva l'originale
- I modelli per le notifiche degli amministratori (come **Amministratore: Nuovo Ordine**) vengono inviati all'indirizzo email dell'amministratore del tuo negozio — assicurati che quell'indirizzo email sia corretto nelle impostazioni del tuo negozio