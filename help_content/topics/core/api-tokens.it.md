---
title: API Tokens
---

I token API sono chiavi sicure che consentono a servizi esterni e integrazioni di comunicare con il tuo negozio. Quando un servizio di terze parti o uno strumento ha bisogno di accedere ai dati del tuo negozio o di attivare azioni, invia un token API con ogni richiesta in modo che il tuo negozio possa verificare che la richiesta sia autorizzata. Crei e gestisci tutti i token dalla sezione Token API del tuo pannello di amministrazione.

## Quando hai bisogno di un token API

Di solito avrai bisogno di creare un token API quando:

- Connetti un servizio esterno o uno strumento di automazione che deve leggere da o scrivere nel tuo negozio
- Configuri un ricevitore webhook che deve autenticare le chiamate in arrivo
- Configuri il sistema di assistenza Spwig per la tua installazione
- Costruisci un'integrazione personalizzata utilizzando l'API di Spwig
- Sincronizzi i dati tra il tuo negozio Spwig e un altro sistema

Ogni integrazione dovrebbe avere il proprio token in modo da poter revocare l'accesso per un servizio senza influenzare gli altri.

## Tipi di token

Quando crei un token, puoi scegliere un tipo che descrive il suo scopo. Il tipo è per riferimento tuo e ti aiuta a tenere traccia di ciò che ogni token fa.

| Tipo | Scopo |
|------|---------|
| **Help System** | Utilizzato dal sistema di documentazione di assistenza Spwig |
| **External Integration** | Servizi di terze parti, strumenti di automazione (es. Zapier) o strumenti di sincronizzazione dati |
| **Webhook** | Autenticazione per ricevitori webhook o endpoint |
| **Custom** | Qualsiasi altro scopo che non rientra nelle categorie sopra elencate |
| **Instance Sync** | Sincronizzazione tra installazioni Spwig o servizi esterni Spwig |

## Creare un token API

1. Naviga su **Impostazioni > Token API**
2. Fai clic su **+ Aggiungi token API**
3. Inserisci un **Nome** che descriva chiaramente a cosa serve il token (es. `Sincronizzazione prodotti Zapier` o `API Help System`)
4. Seleziona il tipo di token appropriato
5. Aggiungi opzionalmente una **Descrizione** con ulteriori dettagli sull'integrazione
6. Configura lo stato **Attivo**, la **Data di scadenza** e le **IP consentite** come necessario (vedi di seguito)
7. Fai clic su **Salva**

Dopo aver salvato, il valore completo del token viene visualizzato sulla pagina dei dettagli. **Copialo immediatamente** — il token è mascherato nella vista elenco per motivi di sicurezza e non può essere recuperato nuovamente una volta lasciata questa pagina.

![Dettaglio token API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Sicurezza del valore del token

Spwig mostra il valore completo del token una sola volta: immediatamente dopo aver salvato un nuovo token. Dopo di che, la vista elenco mostra solo una versione mascherata (es. `spw_••••••••••••••••••••3f8a`).

Se perdi il valore di un token, non puoi recuperarlo. Dovrai eliminare il vecchio token e crearne uno nuovo, quindi aggiornare l'integrazione che lo utilizzava.

**Mai condividere i valori dei token via email, messaggi di chat o codice sorgente.** Trattali come password.

## Impostare una data di scadenza

Il campo **Scade il** imposta una data e un'ora dopo le quali il token smetterà di funzionare automaticamente. Lascialo vuoto per i token che non dovrebbero scadere.

Le date di scadenza sono utili per:

- Integrazioni temporanee con una data di fine fissata
- Token dati a terze parti in cui si desidera la rimozione automatica dell'accesso
- Aggiungere un ulteriore livello di sicurezza per integrazioni ad alto privilegio

Quando un token scade, le richieste che lo utilizzano vengono rifiutate. Puoi estendere l'accesso aggiornando la data **Scade il** o creando un token di sostituzione.

## Limitare a specifiche indirizzi IP

Il campo **IP consentiti** accetta un elenco di indirizzi IP. Quando l'elenco non è vuoto, il token funziona solo quando la richiesta proviene da uno di questi indirizzi.

Ad esempio, se lo strumento di analisi funziona su un server a `203.0.113.42`, aggiungendo quell'IP si evita che il token venga utilizzato in modo non autorizzato da qualsiasi altro luogo, anche se dovesse essere divulgato.

Lascia **IP consentiti** vuoto per permettere le richieste da qualsiasi indirizzo IP.

## Monitorare l'utilizzo del token

L'elenco dei token mostra:

- **Conteggio utilizzo** — numero totale di volte in cui il token è stato utilizzato
- **Ultimo utilizzo** — quando il token è stato utilizzato per l'ultima volta per effettuare una richiesta

Questi campi ti aiutano a identificare i token non utilizzati (candidati per la revoca) e a rilevare attività inaspettata.

Un improvviso aumento del conteggio dell'utilizzo potrebbe indicare che un token è in uso da parte di qualcun altro diverso dall'integrazione prevista.

## Revoca di un token

Per fermare immediatamente un token senza eliminarlo:

1. Fare clic sul nome del token
2. Deselezionare **Active**
3. Salvare

Il token rimane nella tua lista per riferimento, ma viene rifiutato in ogni richiesta successiva. Questo è utile quando è necessario sospendere temporaneamente un'integrazione durante un'indagine su un problema.

Per rimuovere definitivamente un token:

1. Selezionare la casella di controllo nella lista
2. Scegliere **Delete selected API tokens** dal menu delle azioni
3. Confermare l'eliminazione

Una volta eliminato, un token non può essere recuperato. Se l'integrazione ha ancora bisogno di accesso, creare un nuovo token e aggiornare la configurazione dell'integrazione.

## Esempio: configurazione di un'integrazione Zapier

**Scenario:** Si desidera collegare il proprio negozio a Zapier per automatizzare le notifiche degli ordini.

| Campo | Valore |
|-------|-------|
| Nome | `Zapier Order Automation` |
| Tipo di token | External Integration |
| Descrizione | Utilizzato da Zapier per leggere nuovi ordini e attivare notifiche |
| Active | Sì |
| Scade il | *(lasciare vuoto)* |
| IPs consentiti | *(lasciare vuoto — Zapier utilizza IP dinamici)* |

Dopo aver salvato, copiare il valore completo del token e incollarlo nelle impostazioni dell'integrazione Spwig di Zapier.

## Consigli

- Assegnare a ogni token un nome chiaro e specifico — `Shopify Sync v2` è molto più utile di `Token 3` quando si effettua il debug mesi più tardi
- Creare un token per ogni integrazione — se un'integrazione è compromessa, è possibile revocare solo quel token senza disturbare gli altri
- Impostare una data di scadenza per i token utilizzati in progetti a breve termine o integrazioni temporanee — ciò riduce il rischio che i token dimenticati rimangano attivi indefinitamente
- Rivedere la lista dei token ogni paio di mesi e disattivare eventuali token con una data **Last Used** inaspettatamente vecchia, poiché potrebbero appartenere a integrazioni che non sono più attive
- Se si sospetta che un token sia stato esposto, disattivarlo immediatamente, crearne un sostituto e aggiornare l'integrazione interessata prima di riattivare l'accesso