---
title: Migrazione da Magento
---

Spwig può importare il tuo catalogo, i clienti, gli ordini, i coupon e le pagine CMS direttamente da un negozio Magento 2 o Adobe Commerce in esecuzione, utilizzando l'API REST di Magento. Questa guida illustra come generare le credenziali di integrazione richieste da Magento, eseguire il wizard di migrazione e l'unica significativa lacuna che i commercianti provenienti da Magento devono pianificare: le recensioni dei prodotti.

Solo **Magento 2 e Adobe Commerce** sono supportati. Magento 1 è arrivato al termine della sua vita utile anni fa e non espone l'API REST su cui si basa questa migrazione — se sei ancora su Magento 1, usa invece [Importazione da file CSV](csv-import).

## Prima di iniziare

Consulta [Panoramica della migrazione dei dati](migration-overview) per ottenere un orientamento generale per la pianificazione. Per Magento in particolare:

- **Categorie** — importate mantenendo la gerarchia.
- **Prodotti** — importati, inclusi gli immagini.
- **Clienti e indirizzi** — importati.
- **Ordini** — importati.
- **Coupon** — importati come buoni Spwig, derivati dalle regole di vendita di Magento.
- **Pagine CMS** — importate come pagine Spwig.
- **Recensioni** — di solito **non** importate. Vedere la sezione successiva prima di affidarti a questo.
- Sono supportate le varianti per i prodotti configurabili.

> **Nota:** Le migrazioni da Magento non trasferiscono programmi di affiliazione, commissioni o pagamenti — l'integrazione del ponte degli affiliazioni di Spwig è disponibile solo per i negozi WooCommerce.

### La Limitazione delle Recensioni

Magento Community Edition non espone un endpoint REST per le recensioni dei prodotti — la route `/reviews` semplicemente non esiste in un'installazione standard di Community. Spwig la verifica prima dell'importazione e, se non è presente, registra un messaggio e continua con il resto della migrazione invece di fallire l'intero lavoro. Le tue categorie, prodotti, clienti, ordini, coupon e pagine vengono comunque importate; solo le recensioni vengono saltate.

Le recensioni **verranno** importate se il tuo negozio utilizza **Adobe Commerce** (che espone questo endpoint) o se la tua installazione di Magento ha un modulo personalizzato che aggiunge una route compatibile per le recensioni.

Se sei su Magento Community e hai bisogno che le recensioni vengano importate in Spwig, esportale separatamente (la maggior parte degli estensioni per le recensioni offre un'esportazione CSV) e importale successivamente utilizzando il file delle recensioni in [Importazione da file CSV](csv-import), collegandole ai tuoi prodotti tramite `product_id`.

## Passo 1: Scegli Magento

Dalla dashboard di migrazione in **Importazione e Esportazione Dati**, fai clic su **Inizia una nuova migrazione** e seleziona **Magento** come piattaforma.

## Passo 2: Connetti al tuo negozio

Hai bisogno dell'URL del tuo negozio Magento e di un token di accesso all'integrazione. L'amministratore di Magento non distribuisce un semplice API key come fanno alcune piattaforme — crei un'**Integrazione**, che è una credenziale a scelta che Magento tratta come un'applicazione connessa.

### Creare un Token di Accesso all'Integrazione

1. Nel tuo amministratore Magento, vai a **Sistema > Integrazioni**.
2. Fai clic su **Aggiungi nuova integrazione**.
3. Imposta il nome su `Spwig Migration` in modo che sia facile da identificare in seguito.
4. Apri la scheda **API** e imposta **Accesso alle risorse** su **Tutto**.
5. Fai clic su **Salva**, quindi fai clic su **Attiva**.
6. Conferma facendo clic su **Consenti** sulla finestra di dialogo che elenca i permessi concessi.
7. Copia il token di accesso visualizzato dopo l'attivazione — Magento lo mostra una sola volta.

> **Nota:** L'accesso alle risorse è impostato su **Tutto** perché l'albero delle risorse di Magento è molto granulare — centinaia di permessi individuali che coprono catalogo, vendite, clienti e CMS — senza un singolo interruttore "leggi tutto" se non si selezionano tutti. La migrazione legge solo dal tuo negozio; non scrive mai indietro, e puoi revocare l'integrazione una volta verificata la migrazione (coperto alla fine di questa guida).

Tornando al wizard di Spwig, inserisci il tuo **URL del negozio** e il **Token di accesso** che hai copiato. Lascia **Testa la connessione prima di procedere** selezionato (predefinito attivo) in modo che Spwig verifichi che possa raggiungere e autenticarsi con il tuo negozio prima di procedere. Se il test fallisce, controlla nuovamente l'URL e assicurati che l'integrazione sia ancora attiva in Magento. Fai clic su **Avanti**.

screenshots-needed

heading

## Passo 3: Rivedi ciò che verrà importato

paragraph

Spwig interroga il tuo negozio Magento e mostra contatori in tempo reale per ogni tipo di dati che ha trovato: categorie, prodotti, clienti, ordini, coupon (provenienti da regole di vendita) e pagine CMS. Ogni tipo ha una casella di controllo, automaticamente selezionata quando Spwig ha trovato elementi da importare e disattivata quando il conteggio è zero.

paragraph

Vedrai anche un campione dei primi cinque prodotti in modo da poter verificare che titoli, prezzi e immagini siano corretti prima di procedere con l'importo completo.

paragraph

Sotto i contatori, **Opzioni di importazione** ti permettono di controllare come si comporterà l'importazione:

list

paragraph

Se devi modificare il modo in cui specifici campi vengono mappati — attributi personalizzati, corrispondenza delle categorie, gestione delle tasse o delle spedizioni — questo avviene nel passo 4, trattato in [Mapping dei campi di migrazione](migration-field-mapping). Clicca **Avanti** per procedere al mapping, quindi **Avvia migrazione** una volta che l'hai riveduto.

heading

## Esecuzione dell'importazione

paragraph

L'importazione viene eseguita in background — puoi chiudere la finestra e l'importazione continuerà comunque. La pagina del progresso mostra lo stato in tempo reale per ogni tipo di dati (categorie, prodotti, clienti, ordini, recensioni, coupon) con un registro che puoi espandere per i dettagli.

paragraph

Una volta completata, arriverai alla pagina della sommario dei risultati. Segui [Dopo la tua migrazione](after-migration-review) per verificare cosa è stato trasferito, gestire eventuali riscritture di link per contenuti che facevano riferimento agli URL del tuo vecchio negozio Magento, e occuparti della configurazione delle tasse e delle spedizioni che lo strumento raccoglie ma non applica automaticamente.

screenshots-needed

heading

## Termine per il rollback

paragraph

Magento è la sola piattaforma in cui il rollback ha un limite di tempo. Una volta completata la tua migrazione, il pulsante **Rollback** appare sulla pagina del riepilogo del lavoro — ma per Magento in particolare, quel pulsante potrebbe smettere di essere offerto dopo un certo periodo successivo al completamento. Altri tipi di migrazione (WooCommerce, Shopify, CSV) non hanno questo termine, ma Magento sì, quindi non rimandare la verifica.

block-quote

paragraph

Verifica i tuoi dati importati in modo tempestivo, mentre il rollback è ancora disponibile, nel caso in cui ne abbia bisogno.

heading

## Revoca dell'integrazione

paragraph

Una volta che hai verificato i tuoi dati in Spwig — prodotti, prezzi, immagini, clienti, ordini, coupon e pagine appaiono tutti corretti — torna a **Sistema > Integrazioni** in Magento, trova `Spwig Migration` e disattivalo o eliminalo.

Il token non è necessario nuovamente a meno che non tu pianifichi di rilanciare la migrazione, e rimuoverlo chiude un credenziale di accesso in lettura che non hai più bisogno di tenere aperto.

## Consigli

- **Le recensioni rappresentano la sorpresa più grande per i commercianti Magento** — pianifica un'esportazione/importazione separata se sei sulla versione Community Edition e le recensioni sono importanti per il tuo negozio.
- **Copia immediatamente il token di accesso** — Magento lo mostra una sola volta quando attivi l'integrazione; se lo perdi, dovrai disattivarla e ricrearla.
- **Non ritardare la verifica** — il pulsante Annulla è disponibile per un periodo limitato per Magento in particolare, a differenza di altre piattaforme.
- **Utilizza l'anteprima di esempio nel passaggio 3** per individuare problemi di mappatura evidenti (prezzi errati, immagini mancanti) prima di eseguire l'importazione completa.
- **I coupon provengono dalle regole di vendita** — se un coupon Magento dipende da condizioni complesse, controllalo in Spwig successivamente, poiché non ogni tipo di regola ha un equivalente diretto.
- **Configura le aliquote fiscali e le aree di spedizione in Spwig dopo l'importazione** — le opzioni fiscali e di spedizione del wizard vengono salvate ma non vengono applicate automaticamente al tuo negozio.