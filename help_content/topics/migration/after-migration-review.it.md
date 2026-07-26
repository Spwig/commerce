---
title: Dopo la migrazione
---

Una migrazione completata è l'inizio della tua revisione, non la fine. La fase 6 del wizard ti fornisce un riepilogo di ciò che è stato trasferito, uno strumento per correggere i collegamenti che puntano ancora al tuo vecchio sito e un rapporto che puoi scaricare per i tuoi archivi. Questo argomento ti guiderà su ciò che devi controllare prima di considerare il trasferimento completato, incluso il lavoro relativo alle tasse, alle spedizioni e all'avvio del sito che il wizard stesso non esegue per te.

## Lettura dei risultati

In alto nella pagina di completamento vedrai una riga di schede statistiche — una per ogni tipo di dati (Prodotti, Categorie, Clienti, Ordini, ecc.) — seguita da una tabella **Import Summary** con le colonne Imported, Skipped, Failed e Total per ogni passaggio eseguito.

- **Imported** — elementi creati con successo in Spwig.
- **Skipped** — elementi che la tua piattaforma di origine aveva, ma Spwig non ha creato. Questo è quasi sempre previsto: con **Skip existing items** attivo nella fase 3, qualsiasi elemento che corrisponde a un elemento già esistente in Spwig (per SKU, email, ecc.) viene lasciato com'è invece di essere duplicato. Un alto numero di elementi saltati dopo un tentativo di ripristino indica spesso che il primo tentativo aveva già creato quei record.
- **Failed** — elementi che Spwig ha provato a creare, ma non è riuscito, a causa di un problema dei dati, di una dipendenza mancante o di un errore sul lato della fonte. Un conteggio di fallimenti diverso da zero è degno di essere investigato; vedi [Migration Troubleshooting](migration-troubleshooting) per sapere come leggere i log e quali sono le tue opzioni di pulizia.

> **Nota:** Se qualsiasi passaggio mostra fallimenti, non assumere che il negozio abbia annullato qualcosa per compensare — non lo fa. Qualsiasi elemento importato prima del fallimento è presente nel tuo negozio insieme a tutto ciò che è riuscito. Controllalo nello stesso modo in cui lo faresti per un risultato parziale normale.

## Riscrittura dei collegamenti

Prodotti, pagine e post del blog importati dalla tua vecchia piattaforma spesso contengono collegamenti al loro dominio originale — un URL di un'immagine, un collegamento a un "prodotto correlato", un riferimento incrociato interno. Se Spwig rileva uno di questi nel contenuto appena importato, un pannello **Link Rewriting** appare sulla pagina di completamento.

Ogni collegamento rilevato è raggruppato per la pagina o il prodotto da cui proviene e mostrato con:

- **Original URL** — il collegamento esattamente come è apparso nel contenuto importato.
- **Suggested URL** — il miglior tentativo di Spwig per trovare la pagina equivalente nel tuo nuovo negozio, se è stata trovata.
- **Match** — una percentuale di confidenza per questa proposta. I collegamenti senza un match ragionevole vengono visualizzati come **None** e non hanno alcun URL proposto da approvare.

Per ogni collegamento puoi **Approve** la proposta o **Skip** esso, uno alla volta. **Auto-approve high confidence** approva ogni proposta con un livello di confidenza del 85% o superiore con un clic — un risparmio di tempo, ma comunque degno di un controllo casuale successivo. Le proposte al di sotto di quel limite sono quelle che vale la pena aprire manualmente: un match del 50-70% potrebbe essere il prodotto giusto con il nome sbagliato, o potrebbe non essere nemmeno vicino, e solo uno sguardo umano può dirlo.

Approvare o saltare un collegamento segna solo il collegamento — nulla nel tuo contenuto cambia finché non clicchi su **Apply Approved Links**, che riscrive ogni collegamento approvato in una volta sola. Questo significa che è sicuro lavorare attraverso l'elenco in più di una sessione prima di confermare.

> **Consiglio:** Lascia qualsiasi collegamento di cui non sei sicuro come **Skip** invece di approvare un'ipotesi. Puoi sempre correggere manualmente un collegamento a un vecchio dominio in un secondo momento; un riscrittura errata applicata a decine di prodotti richiederà più lavoro per annullarla.

## Verifica dei dati

Tratta le schede statistiche come un punto di partenza, non come prova che tutto sia corretto. Dedica alcuni minuti a controllare casualmente:

- **Prodotti** — Apri un paio di prodotti, specialmente quelli con varianti (taglia, colore, ecc.), e conferma che le opzioni delle varianti e i prezzi siano arrivati correttamente, e che le immagini siano attaccate e visibili sullo store, non solo nell'amministrazione.
- **Categorie** — Conferma che la gerarchia delle categorie appaia corretta, in particolare se hai migrato da Shopify, dove le raccolte vengono importate come un elenco piatto invece che come un albero annidato.
- **Account clienti** — Controlla casualmente gli indirizzi email e gli indirizzi su alcuni record.

I clienti migrati non portano con sé la vecchia password — Spwig non ha modo di leggerla dalla piattaforma di origine — quindi **i clienti dovranno reimpostare la password** la prima volta che si accedono.

Considera un'email di avviso una volta che vai live.
- **Ordini** — Verifica che i totali, gli stati e gli elementi dell'ordine di un campione di ordini corrispondano a quanto hai visto sulla vecchia piattaforma.
- **Prodotti derivati da estensioni** — Se hai migrato da WooCommerce con estensioni come Subscriptions, Bundles, Gift Cards, Composite Products o Bookings, controlla alcuni prodotti che le utilizzavano.

I dati delle estensioni che non possono essere letti non bloccano l'importazione del prodotto — arriva comunque, ma senza quella configurazione aggiuntiva — quindi questi prodotti sono i più probabili a richiedere un intervento manuale.

## Configurazione delle tasse e della spedizione

Le opzioni del passo 4 del wizard per l'importazione delle impostazioni fiscali e delle zone di spedizione registrano le tue preferenze, ma non vengono applicate all'importazione — non vengono create tasse o zone di spedizione da esse. Questo è previsto: **la configurazione delle tasse e della spedizione è un passo normale e separato che completi direttamente in Spwig** dopo che l'importazione dei dati è finita, esattamente come faresti quando configuri un nuovo negozio.

Il controllo **Price adjustment** nello stesso passo è l'eccezione — ha effetto per le importazioni da WooCommerce, CSV e Shopify, spostando il prezzo base di ogni prodotto mentre viene creato. Se ne imposti uno e i prezzi sembrano sbagliati, è da lì che proviene il cambiamento. Vedi [Migration Field Mapping](migration-field-mapping) per i dettagli.

Prima di andare live, configura:

- Le tue aliquote fiscali — vedi [Tax Configuration](tax-configuration) per impostare le aliquote per paese, stato o regione, incluso eventuali esenzioni necessarie per i tuoi prodotti.
- Le tue zone e metodi di spedizione — vedi [Setting Up Shipping](setup-shipping) per riprodurre le opzioni di spedizione che i tuoi clienti avevano sulla vecchia piattaforma.

Fallo prima di testare il checkout, in modo che l'ordine di test rifletta i totali reali.

## Scaricare il tuo rapporto

La pagina di completamento offre tre download:

- **Download PDF** — un riepilogo formattato con i metadati del lavoro, i conteggi per passo e un elenco degli errori, limitato ai **primi 20 errori**.
- **Download CSV** — lo stesso riepilogo in formato foglio di calcolo, limitato ai **primi 50 errori**.
- **Download Logs** — ogni voce del registro per il lavoro, senza limiti.

Se il numero di errori falliti è piccolo, il PDF o il CSV è sufficiente. Per una migrazione con un gran numero di fallimenti, scarica i log invece — l'unico dei tre con il registro completo invece di un campione troncato.

> **Consiglio:** I record dei lavori di migrazione — inclusi i loro log e rapporti — rimangono in Spwig indefinitamente; nulla li elimina in base a un programma. Scaricali comunque se desideri conservarli per registri offline o condividere con qualcuno che non ha accesso amministrativo, ma non c'è un countdown che ti costringa a farlo oggi.

## Andare live

Una volta che sei soddisfatto della tua configurazione dei dati, delle tasse e della spedizione:

1. **Testa il checkout da capo a fondo.** Aggiungi un prodotto al carrello, completa il checkout e conferma che le tasse, la spedizione e il pagamento vengano calcolati e processati correttamente, idealmente con un metodo di pagamento reale in modalità test.
2. **Aggiorna il tuo DNS** per puntare il tuo dominio a Spwig solo dopo che quel test ha successo. Non passare al DNS prima e debuggare dopo — i clienti potrebbero imbattersi in un checkout rotto nel frattempo.
3. **Mantieni il tuo vecchio negozio disponibile, in uno stato di sola lettura o "chiuso"**, finché non sei sicuro che il nuovo gestisca correttamente gli ordini. Questo ti dà un fallback senza rischiare che vengano effettuati ordini sul vecchio negozio dopo il passaggio.

## Revoca le credenziali della piattaforma di origine

Una volta che hai verificato che la migrazione è completa e non ti aspetti di eseguirla di nuovo, torna sulla tua piattaforma di origine e revoca o elimina la chiave API, l'app o l'integrazione che hai creato per essa (vedi [Migrating from WooCommerce](migrate-from-woocommerce) o la guida equivalente per la piattaforma per sapere dove si trova questa credenziale).

Spwig non ha bisogno di un accesso permanente al tuo vecchio negozio dopo che l'importazione è completata, quindi rimuoverlo chiude un credenziale che non utilizzi più.

## Tips

- **Skipped è generalmente accettabile, failed non lo è** — un numero elevato di elementi saltati dopo un tentativo di ripristino con Skip existing items abilitato è previsto; un numero non nullo di elementi falliti richiede un'ispezione dei log.
- **Non premere subito su Apply Approved Links** — le approvazioni e i salti possono essere modificati liberamente fino a quando non clicchi su Apply, quindi prendi il tuo tempo con quelli a bassa confidenza.
- **Configura le tasse e la spedizione prima del primo vendita live**, non dopo — l'importazione non lo fa per te, e un tasso di tassa non configurato è facile da ignorare fino a quando un cliente non si lamenta.
- **Avvisa i clienti riguardo ai reset delle password** se stai inviando un'email alla tua lista clienti riguardo al trasferimento, in modo che il primo login non sia una sorpresa.
- **Scarica il tuo rapporto prima della scadenza dei 90 giorni** se hai bisogno per registri contabili o di conformità.
- **Mantieni il vecchio negozio attivo, in sola lettura, per un po'** — costa poco e ti dà una rete di sicurezza durante i primi giorni di utilizzo su Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Pagina di completamento della migrazione che mostra le schede statistiche e la tabella di riepilogo Imported/Skipped/Failed/Total
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Pannello di riscrittura dei collegamenti con suggerimenti raggruppati, percentuali di confidenza e i controlli Approve/Skip/Apply Approved Links
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->