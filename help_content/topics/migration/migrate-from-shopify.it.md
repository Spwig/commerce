---
title: Migrazione da Shopify
---

Se il tuo negozio attualmente funziona su Shopify, lo strumento di migrazione di Spwig può importare i tuoi prodotti, clienti, ordini e contenuti collegandosi a un piccolo app personalizzato che crei nel pannello Shopify Partners. La piattaforma Shopify è più limitata rispetto alla maggior parte, quindi gran parte di questa guida è dedicata alla creazione di quell'app in modo corretto — la connessione stessa è un passo di cinque minuti una volta che l'app esiste.

## Prima di iniziare

Due limiti specifici di Shopify sono abbastanza importanti da menzionarli qui, non solo più avanti in una tabella:

> **Importante:** Shopify non ha un'API per le recensioni, quindi **le recensioni dei clienti non vengono migrate affatto**, indipendentemente dagli ambiti dell'app che concedi. Se hai bisogno delle tue recensioni, esportale separatamente dall'app per le recensioni che stai utilizzando (Judge.me, Yotpo, Loox, ecc.) e importale tu stesso in Spwig.

> **Importante:** Di default, Spwig può leggere **solo gli ordini degli ultimi 60 giorni**. Per trasferire l'intera cronologia degli ordini, devi aggiungere l'ambito `read_all_orders` quando crei l'app — vedi l'elenco degli ambiti di seguito. Questo è facile da perdere, poiché l'app si collega e importa comunque con successo senza di esso; semplicemente limita silenziosamente quanto indietro va la cronologia degli ordini.

Tutto il resto si trasferisce bene: le categorie (come Collezioni — vedi di seguito), i prodotti, le immagini, le varianti, i clienti e gli indirizzi, gli sconti e il contenuto del blog. I campi personalizzati rappresentano l'altro gap significativo — vedi **Metafields di Shopify** verso la fine di questa guida.

Tieni anche presente:

- Le opzioni **Importa impostazioni fiscali** e **Importa zone e metodi di spedizione** del wizard non vengono applicate ai dati importati. Configura tu stesso le aliquote fiscali e le spedizioni in Spwig successivamente — vedi [Dopo la migrazione](after-migration-review).
- L'opzione **Regolazione del prezzo** nello stesso passo *sì* ha effetto per le importazioni da Shopify, modificando il prezzo base di ogni prodotto mentre viene creato. Lasciala impostata su **Nessuna** a meno che non tu voglia deliberatamente spostare ogni prezzo.
-avrai bisogno di un accesso a un account Shopify Partners per creare l'app. Se non ne hai già uno, Shopify ti permette di crearne uno gratuitamente a [partners.shopify.com](https://partners.shopify.com).

## Creare l'app Shopify

Spwig si collega a Shopify tramite un'app personalizzata che crei e installi sul tuo negozio. Questo specchio la guida **Shopify API Setup Guide** in prodotto (aperta tramite **Open Setup Guide** nel passo 2 del wizard), quindi i passaggi seguenti corrispondono esattamente a quanto vedrai lì — puoi seguire entrambi.

### Passo 1: Creare l'app

1. Vai al [dashboard di sviluppo Shopify Partners](https://dev.shopify.com/dashboard) e apri **Apps**
2. Clicca su **Create app**
3. Scegli **Start from Dev Dashboard**
4. Inserisci il nome dell'app: `Spwig Migration`
5. Clicca su **Create**

![Creare l'app Spwig Migration nel dashboard di sviluppo Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Passo 2: Impostare l'URL dell'app e gli ambiti

Nella pagina di configurazione dell'app nuova, sotto **Versions**, imposta:

- **App URL**: `https://shopify.dev/apps/default-app-home`
- **Scopes**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Impostare l'URL dell'app e gli ambiti necessari](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Scope | Concede a Spwig l'accesso a |
|---|---|
| `read_products` | Prodotti, varianti, immagini, collezioni |
| `read_customers` | Nomi clienti, email, indirizzi |
| `read_orders` | Ordini degli ultimi 60 giorni |
| `read_content` | Post del blog e pagine |
| `read_discounts` | Codici sconto e regole |
| `read_files` | File multimediali caricati |

> **Nota:** Vuoi la cronologia completa degli ordini invece di solo gli ultimi 60 giorni? Aggiungi `read_all_orders` all'elenco degli ambiti sopra.

### Passo 3: Copiare il tuo Client ID e Secret

Vai a **Settings > Credentials** e copia il **Client ID** e **Secret** visualizzati lì — li incollerai nel wizard di Spwig tra un momento.

![Copiare il Client ID e Secret dalla pagina Settings dell'app](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Passo 4: Generare un link di distribuzione personalizzato

1.

Vai a **Distribuzione** e seleziona **Distribuzione personalizzata**
2.

Inserisci il dominio del tuo negozio (ad esempio, `yourstore.myshopify.com`)
3.

Fai clic su **Genera link**, quindi **Copia** il link di installazione che genera

![Copiando il link di installazione per la distribuzione personalizzata](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Passaggio 5: Installa l'app sul tuo negozio

Apri il link di installazione che hai appena copiato nel tuo browser (assicurati di essere connesso all'amministrazione del tuo negozio Shopify), esamina le autorizzazioni che richiede e fai clic su **Installa**.

![Installazione dell'app sul negozio Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Importante:** Questo ultimo passaggio è facile da dimenticare. La generazione del link di installazione non installa l'app — devi effettivamente aprire il link e fare clic su Installa, altrimenti Spwig non sarà in grado di connettersi. Se il test di connessione fallisce nella sezione successiva, questo è il primo elemento da controllare.

## Copia delle tue credenziali in Spwig

Nell'amministrazione di Spwig, vai a **Importa e esporta dati > Avvia nuova migrazione**, scegli **Shopify** nel passaggio 1, e nel passaggio 2 inserisci:

- **Dominio del negozio** — `yourstore.myshopify.com`
- **Client ID** — da Impostazioni > Credenziali
- **Client Secret** — da Impostazioni > Credenziali

Se preferisci seguire la procedura guidata all'interno del prodotto invece di questa guida, fai clic su **Apri guida di configurazione** in questo passaggio — copre gli stessi cinque passaggi elencati sopra con le stesse immagini e richiede circa 10 minuti in totale.

Lascia selezionato **Testa la connessione prima di procedere**. Se `read_products`, `read_customers` o `read_orders` manca dalle autorizzazioni dell'app, Spwig ti avvisa prima che tu continui — torna alla pagina delle versioni dell'app nel pannello di amministrazione Shopify, aggiungi l'autorizzazione mancante, salva una nuova versione e riprova.

## Rivedi e seleziona i dati

Il passaggio 3 estrae i conteggi in tempo reale dal tuo negozio e mostra un campione dei primi cinque prodotti. Alcune cose appaiono diverse rispetto ad altre piattaforme:

- **Collezioni, non categorie** — Shopify organizza i prodotti in Collezioni invece che in categorie, e le Collezioni non supportano l'annidamento, quindi l'importazione mantiene una struttura piatta. Se il tuo negozio Shopify utilizzava le collezioni per rappresentare un albero di categorie, pianifica di ricostruire quella struttura nel gestore delle categorie di Spwig dopo l'importazione.
- **Sconti, non coupon** — I codici sconto e le regole di sconto di Shopify vengono importati come sconti di Spwig.
- **Nessuna riga Recensioni** — poiché Shopify non ha un'API per le recensioni, questo tipo di dati non appare affatto in questo passaggio, a differenza di WooCommerce o importazioni CSV.

Le **Opzioni di importazione** funzionano allo stesso modo di altre piattaforme: **Ignora gli elementi esistenti** (attivo) si basa su SKU e email per evitare duplicati; **Importa immagini dei prodotti** (attivo) è più lento ma consigliato; **Mantieni gli ID originali quando possibile** (disattivo) dovrebbe rimanere disattivo a meno che non tu abbia un motivo specifico per cambiarlo; **Dimensione del lotto** predefinita a 25.

## Metafields di Shopify

Se utilizzi i metafields di Shopify per archiviare dati aggiuntivi sui prodotti, clienti o ordini, tieni presente che Spwig non li rileva né li legge — a differenza di WooCommerce, non esiste un passaggio di mappatura dei campi personalizzati per le importazioni di Shopify. Qualsiasi dato che hai archiviato nei metafields dovrà essere riassegnato manualmente in Spwig utilizzando [campi personalizzati](migration-field-mapping) dopo la migrazione, quindi è utile esportare un elenco dei tuoi metafields e dei loro valori da Shopify prima di iniziare.

## Esecuzione dell'importazione

Una volta aver riveduto il passaggio 3, avvia l'importazione. Si esegue in background — puoi chiudere la finestra del browser e continua comunque. Il passaggio 5 mostra lo stato in tempo reale con una riga per ogni tipo di dati e un registro delle attività espandibile.

Il passaggio 6 mostra i risultati: cosa è stato importato, saltato o fallito, più uno strumento per **Riscrittura dei collegamenti** se sono stati trovati collegamenti interni al tuo vecchio dominio `myshopify.com` nel contenuto importato.

Rivedi attentamente il riepilogo, quindi procedi con la checklist in [Dopo la migrazione](after-migration-review) — copre la verifica dei tuoi dati, la ricostruzione di qualsiasi gerarchia di raccolte, l'impostazione delle aliquote fiscali e della spedizione (che il wizard non configura per te), e la reimmissione di qualsiasi elemento che era memorizzato nei metafield.

## Elimina l'app da Shopify

Una volta confermata la migrazione completata con successo, torna alla pagina **Apps** dell'amministrazione Shopify, o al dashboard dei Partner, e elimina l'app Spwig Migration (o al minimo disinstallala dal tuo negozio). Non c'è motivo per lasciare attiva l'accesso in lettura ai dati del tuo negozio una volta completata la migrazione.

## Consigli

- **L'archivio degli ordini è limitato di default** — se hai bisogno di più di 60 giorni di ordini, aggiungi `read_all_orders` all'elenco degli ambiti prima di generare il link di installazione, non dopo.
- **Le recensioni richiedono un'esportazione separata** — pianifica questo prima della migrazione, poiché non esiste alcun modo per trasferire le recensioni tramite il wizard.
- **Generare il link non è lo stesso che installare l'app** — completa sempre il passaggio 5 e fai clic su Installa, altrimenti il test di connessione in Spwig fallirà.
- **Le raccolte arrivano in formato piatto** — se la struttura delle tue categorie aveva importanza per la navigazione o per l'ottimizzazione dei motori di ricerca, prevedi del tempo per ricostruire la gerarchia in Spwig dopo l'importazione.
- **Esporta i metafield prima** — Spwig non può leggerli, quindi cattura quei dati da Shopify prima di iniziare, se ne avrai bisogno in seguito.
- **Elimina l'app una volta verificato** — non lasciare un'integrazione attiva puntata al tuo vecchio negozio dopo che ti sei spostato.