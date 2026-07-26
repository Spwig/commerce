---
title: Importazione da file CSV
---

L'importazione da CSV è l'opzione di migrazione di default per qualsiasi negozio a cui Spwig non si connette direttamente. Se provieni da BigCommerce, PrestaShop, Squarespace, Wix, da un foglio di calcolo che hai gestito manualmente, o da un sistema personalizzato senza un API che Spwig comprende, questa è l'opzione in cui atterrerai — esporta i tuoi dati in file CSV e caricali qui invece di connetterti in tempo reale.

Queste linee guida coprono quando utilizzare il CSV, cosa non può portare con sé, i cinque file coinvolti, come prepararli e come funziona la mappatura delle colonne.

## Quando Utilizzare il CSV Invece di una Connessione API

Spwig si connette direttamente a WooCommerce, Shopify e Magento 2/Adobe Commerce — vedi [Panoramica della Migrazione dei Dati](migration-overview) per questi. Per qualsiasi altro piattaforma, il CSV è l'unica opzione; non esiste una connessione diretta per BigCommerce, PrestaShop, Squarespace o Wix. È anche la scelta giusta se stai consolidando i dati da un foglio di calcolo, se stai disattivando un negozio personalizzato, o se desideri controllare esattamente cosa viene importato curando i file da te.

## Cosa il CSV Non Può Fare

Prima di preparare qualsiasi cosa, sappi cosa questa via lascia indietro — questo è il principale motivo di sorpresa per i commercianti che utilizzano l'importazione CSV:

- **Nessuna immagine del prodotto.** I prodotti vengono importati senza immagini allegati; caricali successivamente.
- **Nessuna variante.** Ogni prodotto viene creato come prodotto semplice. Ricostruisci le strutture di dimensioni/colori/stile in Spwig dopo l'importazione.
- **Nessun coupon.** I codici sconto e le promozioni non fanno parte del formato CSV.
- **Nessun contenuto del blog.** Non esiste un file CSV per i post o gli articoli.

Niente di questo blocca l'importazione — significa solo che i prodotti necessiteranno di lavoro successivo una volta che saranno in Spwig. Vedi [Dopo la Tua Migrazione](after-migration-review) per il controllo completo post-importazione.

## I Cinque File

La fase CSV del wizard offre cinque input di file, ciascuno con un pulsante **Scarica Modello**. Inizia da questi modelli invece di creare i file da zero — garantiscono i nomi di colonna corretti e permettono alla rilevazione automatica di fare più lavoro nel passo 4.

| File | Obbligatorio? |
|---|---|
| Prodotti | **Obbligatorio** |
| Categorie | Opzionale |
| Clienti | Opzionale |
| Ordini | Opzionale |
| Recensioni | Opzionale |

Il solo file che Spwig richiede è il prodotti — gli altri possono essere lasciati vuoti se non hai ancora quei dati.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Step 2 with CSV selected, showing the five file inputs and their Download Template buttons
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Prodotti (Obbligatorio)

| Colonna | Descrizione |
|---|---|
| `id` | Identificatore unico nei tuoi dati di origine; non mostrato ai clienti. |
| `name` | Il titolo del prodotto. **Essenziale.** |
| `slug` | Versione amichevole per l'URL del nome; generata automaticamente da `name` se vuota. |
| `description` | La descrizione mostrata sul negozio online. |
| `price` | Il prezzo regolare del prodotto. **Essenziale.** |
| `sku` | Unità di controllo delle scorte — utilizzata per il matching quando **Salta gli elementi esistenti** è abilitato. |
| `stock_quantity` | Unità attualmente in stock. |
| `category` | Nome della categoria a cui appartiene questo prodotto. Deve corrispondere a un `name` nel tuo file delle categorie. |

### Categorie

| Colonna | Descrizione |
|---|---|
| `id` | Identificatore unico nei tuoi dati di origine. |
| `name` | Il nome della categoria. **Essenziale.** |
| `slug` | Versione amichevole per l'URL del nome; generata automaticamente se vuota. |
| `description` | Testo della descrizione della categoria. |
| `parent_id` | L'`id` della categoria genitore di questa categoria. Vuoto significa livello principale. |

### Clienti

| Colonna | Descrizione |
|---|---|
| `id` | Identificatore unico nei tuoi dati di origine. |
| `email` | Indirizzo email del cliente. **Essenziale** — collega gli ordini e le recensioni al cliente giusto. |
| `first_name` | Nome del cliente. |
| `last_name` | Cognome del cliente. |
| `phone` | Numero di telefono del cliente. |

### Ordini


| Colonna | Descrizione |
|---|---|
| `id` | Identificatore univoco nei tuoi dati di origine. |
| `customer_email` | Email del cliente che ha effettuato l'ordine. **Essenziale** — collega l'ordine a un record cliente. |
| `order_date` | La data in cui è stato effettuato l'ordine. |
| `status` | Lo stato dell'ordine (es. completato, in elaborazione). |
| `total` | Totale dell'ordine. **Essenziale.** |
| `currency` | Codice della valuta per il totale dell'ordine. |

### Recensioni (Opzionale)

| Colonna | Descrizione |
|---|---|
| `id` | Identificatore univoco nei tuoi dati di origine. |
| `product_id` | L'`id` del prodotto che viene recensito, corrispondente al tuo file dei prodotti. **Essenziale** — collega la recensione al prodotto giusto. |
| `customer_email` | Indirizzo email del recensore. |
| `rating` | La valutazione a stelle assegnata. |
| `comment` | Il testo della recensione. |
| `date` | La data in cui è stata pubblicata la recensione. |

## Preparazione dei File

- **Salva come UTF-8** per evitare caratteri accentati corrotti, specialmente da un diverso encoding di origine.
- **Includi virgolette per i campi che contengono virgole** — racchiudi una descrizione o un nome che contiene una virgola tra virgolette doppie in modo che non venga interpretato come un'interruzione di colonna.
- **Includi una riga di intestazione.** La prima riga deve contenere i nomi delle tue colonne — un file senza una riga di intestazione viene rifiutato.
- **Costruisci la gerarchia delle categorie con `parent_id`.** Assegna a ogni categoria un `id` univoco, quindi imposta il `parent_id` di una sottocategoria all'`id` della sua categoria principale. Lascia vuoto per indicare un livello principale.
- **Collega gli ordini ai clienti con `customer_email`**, corrispondente alla colonna `email` nel tuo file dei clienti (o verrà creato un record ospite), invece di affidarsi a numeri ID interni, che raramente corrispondono tra i diversi piattaforme.
- **Collega le recensioni ai prodotti con `product_id`**, corrispondente a un valore nella colonna `id` del tuo file dei prodotti, altrimenti la recensione verrà ignorata.

## Mappatura delle Colonne nel Passo 4

Il passo 4 mostra un pannello di mappatura delle colonne CSV. Spwig scansiona gli header e rileva automaticamente le corrispondenze probabili rispetto a una lista di alias comuni — ad esempio, un campo `sku` corrisponde anche a `barcode`, `part_number` o `item_number`. Gli header esportati direttamente da un'altra piattaforma si mappano spesso correttamente senza alcun lavoro manuale.

Per ogni colonna, puoi accettare la supposizione rilevata automaticamente, sovrascriverla selezionando un diverso campo di destinazione, o scegliere "— Salta questa colonna —" per escluderla. Le mappature vengono salvate e riutilizzate per le future migrazioni CSV. Vedere [Mapping dei Campi di Migrazione](migration-field-mapping) per una visione completa del passo 4, inclusi i mapping automatici dei campi, il mapping delle categorie e le opzioni di tasse/spedizione.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Pannello di mappatura delle colonne CSV del passo 4 che mostra le mappature rilevate automaticamente con i menu a discesa per sovrascrivere
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Errori Comuni e Cosa Significano

| Errore | Significato |
|---|---|
| `Products CSV is required.` | Hai provato a procedere senza caricare un file dei prodotti. È l'unico file che Spwig richiede — carica uno per continuare. |
| `{Type} CSV has no headers.` | La prima riga del file specificato è vuota o mancante. Aggiungi una riga di intestazione con i nomi delle colonne e ricaricalo. |
| `{Type} CSV could not be read: ...` | Spwig non è riuscito a leggere il file specificato — di solito un file danneggiato, un encoding errato o un file che non è effettivamente CSV nonostante l'estensione. Re-esportalo e conferma che si apra correttamente prima di caricarlo nuovamente. |

## Esecuzione dell'Importazione

Una volta confermata la mappatura, avvia la migrazione dal passo 5. Si esegue in background, quindi puoi chiudere la finestra — lo stato di avanzamento e un log in tempo reale sono disponibili se torni a controllare prima che finisca. Vedere [Dopo la Migrazione](after-migration-review) per verificare i risultati.

Ricorda che l'importazione CSV lascia specificamente **immagini dei prodotti** e **varianti** per te da completare manualmente — né vengono trasferite automaticamente, indipendentemente da quanto siano completi i tuoi file.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- **Inizia dal pulsante Download Template per ogni file** — ti evita di correggere gli errori di battitura nei nomi delle colonne che altrimenti passerebbero inosservati fino al mapping manuale.
- **Risolvi le discrepanze di `product_id` prima di caricare le recensioni** — una recensione il cui `product_id` non corrisponde a nessun `id` del prodotto non ha nulla a cui collegarsi e viene saltata.
- **Non rinomina gli header provenienti da un'export di un'altra piattaforma** — la rilevazione automatica li riconosce spesso così com'è tramite alias, quindi potrebbe non essere necessun lavoro manuale.
- **Riserva del tempo per le immagini e le varianti subito dopo l'import** — queste sono le due cose che il CSV non porta mai con sé, e sono facili da dimenticare fino a quando un cliente non noterà una pagina del prodotto vuota.
- **Utilizza `parent_id` per modellare categorie a più livelli** — fai puntare il `parent_id` di una sottocategoria all'`id` della sua categoria principale per annidarla; lascialo vuoto per le categorie di primo livello.
- **Re-esporta e ricontrolla in caso di errore "could not be read"** — è quasi sempre un problema di codifica o di corruzione nel file sorgente, non qualcosa da correggere in Spwig.