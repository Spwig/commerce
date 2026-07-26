---
title: Mapping dei Campi di Migrazione
---

Ogni piattaforma nomina le cose in modo leggermente diverso — il `regular_price` di WooCommerce non è lo stesso del `price` di Shopify, e una colonna CSV chiamata `barcode` potrebbe essere esattamente la stessa cosa che Spwig aspetta di vedere etichettata come `sku`. La fase 4 del wizard di migrazione, **Configura il Mapping dei Campi**, è dove controlli come i tuoi dati sorgente verranno inseriti in Spwig prima che l'importazione effettivamente venga eseguita. Questo argomento copre ogni blocco su questa pagina e si applica alle migrazioni WooCommerce, Shopify, Magento e CSV, con le differenze di piattaforma indicate dove necessario. Per le credenziali e le fasi precedenti del wizard, vedi [Migrazione da WooCommerce](migrate-from-woocommerce) o la guida equivalente per la tua piattaforma.

## Mapping Automatici

Questo blocco mostra, per ogni tipo di dati selezionato nella fase 3, un elenco di sola lettura dei campi sorgente e del campo Spwig su cui cadauno atterra — ad esempio, il `name` di un prodotto che mappa al titolo del prodotto di Spwig, o l'`email` di un cliente che mappa all'email dell'account. Solo i tipi di dati che stai effettivamente importando appaiono qui; se non hai selezionato Recensioni nella fase 3, non c'è una sezione Recensioni su questa pagina.

Poiché queste righe sono di sola lettura, non c'è nulla da configurare — esistono per permetterti di verificare il mapping prima di procedere con l'importazione. Se un mapping sembra sbagliato per i tuoi dati, non c'è modo di sovrascriverlo da questo schermo; le tue opzioni sono correggere i dati sorgente prima della migrazione, o correggere i record interessati in Spwig dopo che l'importazione è completata.

## Mapping delle Colonne CSV

Questo blocco appare solo per le migrazioni CSV, con una tabella per ogni file caricato. Spwig rileva automaticamente le corrispondenze probabili dai tuoi header di colonna — ad esempio, un `sku` mappa anche header come `barcode`, `part_number` o `item_number` — quindi, nella maggior parte dei casi, non dovrai toccare nulla qui.

Ogni colonna CSV ha un menu a discesa che elenca i campi che Spwig aspetta per quel tipo di file:

- **prodotti** — `id, name, slug, description, price, sku, stock_quantity, category`
- **categorie** — `id, name, slug, description, parent_id`
- **clienti** — `id, email, first_name, last_name, phone`
- **ordini** — `id, customer_email, order_date, status, total, currency`
- **recensioni** — `id, product_id, customer_email, rating, comment, date`

Ogni menu a discesa include anche **— Salta questa colonna —**, che esclude completamente questa colonna dall'importazione. Sovrascrivi il mapping rilevato automaticamente quando il tuo header utilizza una convenzione di denominazione che Spwig non ha riconosciuto, o quando una colonna non corrisponde effettivamente a nulla che Spwig importa (ad esempio, un campo di nota interna) — seleziona Salta invece di forzarla sul campo disponibile più vicino.

## Campi Personalizzati

Questo blocco è specifico di WooCommerce. Spwig preleva 10 prodotti, clienti e ordini dal tuo negozio e elenca eventuali campi meta personalizzati che trova al di là dei campi standard di WooCommerce, insieme al tipo rilevato e a un valore di esempio.

Per ogni campo, scegli dove dovrebbe andare:

- **Mappa a** — Campo Personalizzato 1, 2 o 3 per i prodotti (Campo Personalizzato 1 o 2 per i clienti e gli ordini), o **Meta Dati (JSON)** come soluzione di emergenza se hai più campi personalizzati dei slot numerati, o lascialo come **— Salta questo campo —**.
- **Trasforma** — come il valore dovrebbe essere convertito in entrata: Come Testo, Come Numero (Intero), Come Decimale, Come Vero/Falso (Booleano), Come JSON, Come Data, Come URL, o Come Email.

> **Nota:** I metafield di Shopify non vengono rilevati da questa funzione affatto — le migrazioni Shopify non mostreranno mai un blocco Campi Personalizzati, indipendentemente da quanto dati di metafield il tuo negozio possieda. Se ti affidi ai metafield di Shopify per specifiche dei prodotti, attributi dei clienti o simili, pianifica di reinserire manualmente quei dati in Spwig dopo l'importazione.

Se Spwig non rileva alcun campo personalizzato nei tuoi campioni, vedrai un messaggio di conferma al posto di questo blocco, e non c'è nulla di ulteriore da configurare.

Quando alcune delle tue categorie di origine non hanno un corrispondente ovvio in Spwig, questo blocco offre tre opzioni: **Crea nuove categorie**, **Assegna alla categoria predefinita** (una categoria 'Non categorizzato' universale), o **Salta gli elementi con categorie non mappate**.

> **Nota:** Indipendentemente dall'opzione che scegli qui, Spwig crea automaticamente una categoria corrispondente per qualsiasi prodotto che abbia dati di categoria di origine, e si rivolge solo a 'Non categorizzato' per i prodotti che non hanno affatto informazioni sulla categoria. Non devi preoccuparti troppo per questa scelta — se finisci per ottenere categorie che non desideri, è più veloce unirle o eliminarle in **Catalogo > Categorie** dopo l'importazione, piuttosto che affidarti a questa impostazione.

## Impostazioni di tasse, spedizione e prezzo

L'ultimo blocco, **Impostazioni sulle tasse e sulla spedizione**, ha tre controlli: **Importa impostazioni sulle tasse**, **Importa zone e metodi di spedizione**, e un tipo e un valore di **Regolazione del prezzo**.

I due checkbox non influiscono attualmente sull'importazione — nessuna tariffa di tassa o zona di spedizione arriva da tuo vecchio piattaforma, indipendentemente da come vengono impostate. Configura entrambi direttamente in Spwig una volta completata l'importazione: le tariffe di tassa sotto **Impostazioni > Tasse e Valuta**, le zone e i metodi di spedizione sotto **Impostazioni > Spedizione**.

**Regolazione del prezzo** si comporta in modo diverso a seconda della tua piattaforma di origine:

- **Migrazioni da WooCommerce, CSV e Shopify** — questo controllo funziona come descritto. Scegli **Percentuale** o **Importo fisso**, inserisci un valore (ad esempio `10` per un aumento del 10%, o `-5` per una riduzione di $5), e il prezzo base di ogni prodotto viene regolato di tale importo durante l'importazione. Si applica solo al prezzo base — i prezzi di vendita/prezzo di confronto vengono importati senza modifiche.
- **Migrazioni da Magento** — lo stesso controllo compare sulla pagina, ma non ha effetto; i prezzi di Magento vengono importati senza modifiche, indipendentemente da ciò che si inserisce. Se hai bisogno di un cambiamento generale dei prezzi durante una migrazione da Magento, applicalo successivamente utilizzando gli strumenti per il prezzo di massa del catalogo di Spwig, invece di questo campo.

> **Avviso:** Se stai migrando da WooCommerce, CSV o Shopify e non desideri modificare i prezzi, lascia **Regolazione del prezzo** impostata su **Nessuna**. È l'unico controllo su questa pagina che modifica veramente i tuoi dati, e è facile assumere erroneamente che si comporti nello stesso modo dei checkbox per le tasse e la spedizione direttamente sopra.

## Le mappature vengono salvate per la prossima volta

Qualsiasi configurazione che effettui su questa pagina viene salvata con il lavoro di migrazione, e Spwig la riutilizza come punto di partenza per future migrazioni dalla stessa piattaforma — utile se esegui una migrazione a fasi (categorie e prodotti prima, ordini in seguito) o se devi rimportare dopo aver corretto un problema dei dati. Puoi anche tornare a visitare e modificare le mappature salvate dopo che una migrazione è completata, utilizzando il pulsante **Mappatura dei campi** sulla dashboard della migrazione, senza dover rieseguire l'intero wizard.

## Consigli

- **Controlla comunque il blocco Mappature automatiche anche se non puoi modificarlo** — catturare una mappatura errata prima di cliccare su Avvia importazione è molto più economico che correggere centinaia di record importati successivamente.
- **Rinomina gli header CSV ambigui prima di caricarli** se la rilevazione automatica non li ha riconosciuti, invece di cercare di forzare un campo non corrispondente attraverso il menu a discesa.
- **Utilizza Meta Data (JSON) come destinazione per i tuoi campi personalizzati extra** — è l'unica destinazione di mappatura che non si esaurisce dopo due o tre campi.
- **Non affidarti a questa pagina per le tasse, la spedizione o (su Magento) i prezzi** — trattale come un compito manuale da eseguire immediatamente dopo l'importazione, non qualcosa che lo wizard gestisce per te.
- **Lascia Regolazione del prezzo su Nessuna durante la tua prima esecuzione di una nuova migrazione**, quindi utilizza un piccolo lotto di test per confermare i calcoli prima di applicarla al tuo catalogo completo.