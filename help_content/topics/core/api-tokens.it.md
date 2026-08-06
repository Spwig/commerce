---
title: API Tokens
---

I token API sono chiavi sicure che consentono a servizi esterni e integrazioni di comunicare con il tuo negozio. Quando un servizio di terze parti o uno strumento ha bisogno di accedere ai dati del tuo negozio o di attivare azioni, invia un token API con ogni richiesta in modo che il tuo negozio possa verificare che la richiesta sia autorizzata. Crei e gestisci tutti i token, incluso esattamente quali parti del tuo negozio possono raggiungere, dalla sezione Token API del tuo amministratore.

## Quando hai bisogno di un token API

Creerai tipicamente un token API quando:

- Connetti un servizio esterno o uno strumento di automazione che ha bisogno di leggere da o scrivere nel tuo negozio
- Configuri un ricevitore di webhook che ha bisogno di autenticare le chiamate in arrivo
- Configuri il sistema di assistenza Spwig per la tua installazione
- Costruisci un'integrazione personalizzata utilizzando l'API di Spwig
- Sincronizzi i dati tra il tuo negozio Spwig e un altro sistema

Ogni integrazione dovrebbe avere il proprio token in modo da poter revocare l'accesso per un servizio senza influenzare gli altri.

## Tipi di token

Quando crei un token, scegli un tipo che descrive il suo scopo. Il tipo è per riferimento tuo e ti aiuta a tenere traccia di ciò che ogni token fa.

| Tipo | Scopo |
|------|---------|
| **Help System** | Utilizzato dal sistema di documentazione di assistenza Spwig |
| **External Integration** | Servizi di terze parti, strumenti di automazione (es. Zapier) o strumenti di sincronizzazione dati |
| **Webhook** | Autenticazione per ricevitori di webhook o endpoint |
| **Custom** | Qualsiasi altro scopo che non rientra nelle categorie sopra elencate |
| **Instance Sync** | Sincronizzazione tra installazioni Spwig o servizi esterni Spwig |

## API scopes: controllare a cosa un token può accedere

Ogni token ha anche una sezione **API Scopes** che decide esattamente quali parti del tuo negozio è autorizzato a chiamare. Invece di un token che abbia un accesso generale a tutto, concedi l'accesso un'area alla volta — e al livello effettivo necessario per l'integrazione.

**Un token senza alcun scope selezionato non può raggiungere alcun API**, anche se è attivo e valido. Questo è il valore predefinito per un nuovo token, quindi un'integrazione non funzionerà fino a quando non gli concederai deliberatamente l'accesso.

Per ogni scope, scegli uno dei tre livelli di accesso:

| Livello di accesso | Cosa permette |
|------------------|------------------|
| **Nessun accesso** | Il token non può chiamare alcun endpoint in questa area |
| **Leggi** | Il token può recuperare dati da questa area, ma non può apportare modifiche |
| **Leggi & Scrivi** | Il token può recuperare dati e anche crearli, aggiornarli o eliminarli |

I scopes sono raggruppati per corrispondere alle aree del tuo amministratore:

| Gruppo | Scope | Disponibile Leggi & Scrivi? | Concede accesso a |
|-------|-------|:---:|-------------------|
| Analytics | **Sales Analytics** | Solo lettura | Dashboard di vendita, KPI, analisi di prodotti/clienti/categorie, confronti ed esportazioni |
| Analytics | **Web Analytics** | Solo lettura | Analisi dei visitatori e del traffico: panoramica, tendenze, pagine più visitate, geografia e referrer |
| Catalog | **Products** | Sì | Prodotti, varianti, immagini, aggiustamenti di stock e assegnazione di attributi |
| Catalog | **Categories** | Sì | Categorie di prodotti, inclusi immagini e banner |
| Catalog | **Brands** | Sì | Marchi di prodotti |
| Catalog | **Attributes** | Sì | Definizioni degli attributi dei prodotti |
| Catalog | **Inventory** | Sì | Dashboard di inventario, velocità di stock, movimenti, suggerimenti di rifornimento e impostazioni dell'inventario |
| Orders | **Orders** | Sì | Ordini, note sugli ordini, aggiornamenti di stato/tracking, annullamenti, rimborsi e documenti degli ordini |
| Customers | **Customer Messages** | Sì | Messaggi dei clienti da moduli di contatto e note sugli ordini, inclusi aggiornamenti di stato e risposte |
| Store & Settings | **Store Settings** | Sì | Impostazioni del negozio, lingue disponibili e branding (nome, colori, logo) |
| Users & Access | **Staff & Roles** | Sì | Account dello staff, inviti, ruoli e catalogo dei permessi |

I due scopes **Analytics** sono sempre solo in lettura — i dati di reporting non hanno un concetto di "scrittura", quindi il selettore offre solo **Nessun accesso** o **Leggi** per loro.

[![Il selettore delle API Scopes, con una nota di accesso sopra i gruppi di scope Analytics e Catalog](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

Sotto il selettore delle scope, una descrizione **'This token can access:'** (Questo token può accedere a:) elenca ogni scope che hai concesso e il relativo livello, in modo da poter verificare rapidamente l'accesso del token senza dover decodificare il selettore.

![La descrizione 'This token can access' che elenca ogni scope concesso e il livello di lettura o lettura/scrittura](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Quali permessi utilizza effettivamente un token

Le scope di un token descrivono il *soffitto* di ciò che può fare — ma il token eredita anche i reali permessi del membro dello staff che lo ha creato:

- Il token non può mai agire con i **permessi superuser**, nemmeno se il membro dello staff che lo ha creato è un superuser.
- Il **Read & Write** su una scope funziona solo se il ruolo del membro dello staff che lo ha creato permette anche l'accesso in scrittura a quell'area. Se il loro ruolo è solo in lettura, ad esempio, per i Prodotti, un token che creano con 'Prodotti: Read & Write' può comunque leggere solo — il ruolo agisce come una seconda porta sopra la scope.
- Se il membro dello staff che ha creato un token viene eliminato o il loro account viene disattivato, il token perde immediatamente l'accesso API, indipendentemente dalle sue scope — non c'è più un utente autorizzato per cui agire.

Questo significa che il modo più sicuro per limitare le scope di un token è crearlo mentre sei loggato come un membro dello staff il cui ruolo corrisponde già all'accesso che desideri che il token abbia.

## Creare un token API

1. Naviga su **Settings > API Tokens** (Impostazioni > Token API)
2. Clicca su **+ Add API Token** (+ Aggiungi Token API)
3. Inserisci un **Name** (Nome) che descriva chiaramente a cosa serve il token (es. `Zapier Product Sync` o `Help System API`)
4. Seleziona il tipo di **Token Type** (Tipo di Token)
5. Opzionalmente aggiungi una **Description** (Descrizione) con ulteriori dettagli sull'integrazione
6. In **API Scopes** (Scope API), seleziona **No access**, **Read**, o **Read & Write** per ogni area necessaria all'integrazione — lascia ogni altra scope su **No access**
7. Configura lo stato **Active** (Attivo), la **Expiry Date** (Data di scadenza) e le **Allowed IPs** (IP consentiti) come necessario (vedi di seguito)
8. Clicca su **Save** (Salva)

Dopo aver salvato, il valore completo del token viene visualizzato sulla pagina dei dettagli. **Copia immediatamente** — il token è mascherato nella vista elenco per motivi di sicurezza e non può essere recuperato nuovamente una volta lasciata questa pagina.

![Dettagli del Token API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Sicurezza del valore del token

Spwig mostra il valore completo del token una sola volta: immediatamente dopo aver salvato un nuovo token. Dopo di che, la vista elenco mostra solo una versione mascherata (es. `spw_••••••••••••••••••••3f8a`).

Se perdi il valore di un token, non puoi recuperarlo. Dovrai eliminare il vecchio token e crearne uno nuovo, quindi aggiornare l'integrazione che lo utilizzava.

**Non condividere mai i valori dei token via email, messaggi di chat o codice sorgente.** Trattali come password.

## Impostare una data di scadenza

Il campo **Expires At** (Scade il) imposta una data e un'ora dopo le quali il token smetterà di funzionare automaticamente. Lascialo vuoto per i token che non dovrebbero scadere.

Le date di scadenza sono utili per:

- Integrazioni temporanee con una data di fine fissata
- Token dati a terzi dove si desidera l'eliminazione automatica dell'accesso
- Aggiungere un ulteriore livello di sicurezza alle integrazioni ad alto privilegio

Quando un token scade, le richieste che lo utilizzano vengono rifiutate. Puoi estendere l'accesso aggiornando la data **Expires At** o creando un token di sostituzione.

## Limitare a specifiche indirizzi IP

Il campo **Allowed IPs** (IP consentiti) accetta un elenco di indirizzi IP. Quando l'elenco non è vuoto, il token funziona solo quando la richiesta proviene da uno di questi indirizzi.

Ad esempio, se il tuo strumento di analisi funziona su un server a `203.0.113.42`, aggiungendo quell'IP significa che il token non può essere utilizzato da altre ubicazioni, nemmeno se venisse compromesso.

Lascia **Allowed IPs** (IP consentiti) vuoto per permettere le richieste da qualsiasi indirizzo IP.

**Le scadenze e le restrizioni IP vengono verificate in modo indipendente dagli ambiti.** Un token scaduto o non presente nell'elenco autorizzato viene rifiutato prima che vengano nemmeno considerati i suoi ambiti, e un token con ambiti generosi viene comunque rifiutato non appena scade o viene richiamato da un IP non elencato.

## Effettuare una chiamata all'API con un token

Le integrazioni si autenticano all'API amministrativa di Spwig inviando il token in un'intestazione `Authorization`:

```
Authorization: Bearer <your-token-value>
```

Ogni endpoint dell'API amministrativa si trova sotto `/api/admin/...`. Lo sviluppatore che crea la tua integrazione decide quali endpoint chiamare — il tuo compito come commerciante è assicurarti che gli **ambiti API** del token coprano quegli endpoint. Se una richiesta viene rifiutata con un errore di autorizzazione, la prima cosa da controllare è se il token ha ricevuto l'ambito corretto al livello di accesso appropriato.

### Esempio: lettura delle analisi del traffico web

Spwig espone un endpoint `GET /api/admin/analytics/traffic/` che restituisce analisi del traffico e dei visitatori del tuo negozio — un riepilogo delle visite e dei visitatori unici, tendenze nel tempo, pagine più popolari, geografia dei visitatori e fonti di riferimento. Per permettere a uno strumento di reporting o a un dashboard di leggere questi dati:

1. Crea un token (o modifica uno esistente) per quell'integrazione
2. In **Ambiti API**, imposta **Analisi Web** su **Lettura**
3. Salva il token e forniscilo all'integrazione

Poiché **Analisi Web** è un ambito di sola lettura, non esiste un'opzione "Lettura & Scrittura" da selezionare — l'integrazione può recuperare solo i dati delle analisi, mai modificare la configurazione del tuo negozio.

## Monitoraggio dell'utilizzo del token

L'elenco dei token mostra:

- **Conteggio utilizzo** — numero totale di volte in cui il token è stato utilizzato
- **Ultimo utilizzo** — quando il token è stato utilizzato per l'ultima volta per effettuare una richiesta

Questi campi ti aiutano a identificare i token non utilizzati (candidati per la revoca) e a notare attività inaspettata. Un improvviso aumento del conteggio di utilizzo potrebbe indicare che un token è in uso da parte di qualcun altro diverso dall'integrazione prevista.

## Revoca di un token

Per fermare immediatamente un token senza eliminarlo:

1. Fai clic sul nome del token
2. Deseleziona **Attivo**
3. Salva

Il token rimane nella tua lista per riferimento ma viene rifiutato in ogni richiesta successiva. Questo è utile quando devi sospendere temporaneamente un'integrazione mentre indagini un problema.

Per rimuovere definitivamente un token:

1. Seleziona la casella accanto al token nell'elenco
2. Scegli **Elimina i token API selezionati** dal menu delle azioni
3. Conferma l'eliminazione

Una volta eliminato, un token non può essere recuperato. Se l'integrazione ha ancora bisogno di accesso, crea un nuovo token e aggiorna la configurazione dell'integrazione.

## Esempio: configurazione di un'integrazione Zapier

**Scenario:** Vuoi collegare il tuo negozio a Zapier per automatizzare le notifiche degli ordini.

| Campo | Valore |
|-------|-------|
| Nome | `Zapier Order Automation` |
| Tipo Token | Integrazione Esterna |
| Descrizione | Utilizzato da Zapier per leggere nuovi ordini e attivare notifiche |
| Ambiti API | **Ordini**: Lettura & Scrittura |
| Attivo | Sì |
| Scade il | *(lascia vuoto)* |
| IPs consentiti | *(lascia vuoto — Zapier utilizza IP dinamici)* |

Viene concesso solo l'ambito **Ordini**, quindi anche se questo token fosse mai esposto, non potrebbe toccare prodotti, messaggi dei clienti, account dello staff o qualsiasi altra parte del tuo negozio. Dopo aver salvato, copia il valore completo del token e incollalo nelle impostazioni dell'integrazione Spwig di Zapier.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Assegna a ogni token un nome chiaro e specifico — `Shopify Sync v2` è molto più utile di `Token 3` quando devi risolvere problemi mesi dopo
- Crea un token per ogni integrazione — se un'integrazione è compromessa, puoi revocare solo quel token senza disturbare gli altri
- **Concedi solo gli ambiti necessari all'integrazione** — uno strumento di reporting ha bisogno solo di accesso in lettura a Sales Analytics o Web Analytics, non di accesso in lettura e scrittura a Prodotti o Staff & Roles
- Controlla la sommario **"This token can access:"** nel modulo di modifica prima di consegnare un token a una terza parte — è il modo più veloce per confermare che non hai concesso più accesso del previsto
- Ricorda che l'accesso in scrittura dipende anche dal ruolo dello stesso membro dello staff che lo ha creato — se un ambito mostra Read & Write ma le scritture continuano a fallire, controlla anche i permessi del ruolo di quell'utente
- Imposta una data di scadenza per i token utilizzati in progetti one-time o integrazioni temporanee — questo riduce il rischio che token dimenticati rimangano attivi indefinitamente
- Rivedi la tua lista dei token ogni paio di mesi e disattiva eventuali token con una data **Last Used** che risulti inaspettatamente vecchia, poiché potrebbero appartenere a integrazioni che non sono più attive
- Se sospetti che un token sia stato esposto, disattivalo immediatamente, crea un sostituto e aggiorna l'integrazione interessata prima di riattivare l'accesso