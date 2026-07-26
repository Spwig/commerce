---
title: Panoramica della migrazione dei dati
---

Se i tuoi prodotti, clienti e ordini si trovano attualmente in WooCommerce, Shopify o Magento, o semplicemente in un paio di file CSV, lo strumento di migrazione porterà quei dati nel tuo nuovo negozio Spwig, in modo che non debba reinserirli manualmente. Gestisce categorie, prodotti, clienti, ordini, recensioni e coupon, e per WooCommerce può anche trasferire il contenuto del blog e, con un plugin di collegamento, il tuo programma di affiliazione.

Trovalo nel menu laterale dell'amministratore sotto **Pannello di sistema > Importazione/Esportazione dati** (visibile agli utenti superuser nelle installazioni self-hosted; se non lo vedi, chiedi a chi gestisce l'installazione). La pagina, intitolata **Importazione e Esportazione dati**, elenca ogni migrazione avviata con schede statistiche per Totale migrazioni, Completate, In corso e Fallite, più i pulsanti **Avvia nuova migrazione**, **Visualizza log** e **Mapping dei campi**. Le migrazioni possono essere create solo tramite la procedura guidata.

## Piattaforme supportate

Spwig si connette direttamente a tre piattaforme, più semplici file CSV:

- **WooCommerce** — il percorso più completo; i dati estesi (abbonamenti, pacchetti, carte regalo, prenotazioni) e il tuo programma di affiliazione possono essere trasferiti anche loro.
- **Shopify** — si connette tramite un'app personalizzata che crei nel tuo pannello di sviluppo Shopify.
- **Magento 2** — si connette tramite un token di integrazione dal tuo amministratore Magento.
- **File CSV** — cinque file separati (prodotti, categorie, clienti, ordini, recensioni), per altre piattaforme o dati preparati a mano.

> **Nota:** BigCommerce, PrestaShop, Squarespace e Wix non sono supportati come connessioni dirette. Se stai migrando da uno di questi, esporta il tuo catalogo e i dati dei clienti in CSV e usa invece l'opzione CSV — vedi [Importazione da file CSV](csv-import).

## Cosa viene trasferito, per piattaforma

La copertura varia per piattaforma — controlla questa tabella rispetto al tuo negozio prima di impegnarti con una data di lancio.

| Dati | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Categorie | Sì, con gerarchia | Sì, come Collezioni (piatta) | Sì | Sì |
| Prodotti | Sì | Sì | Sì | Sì (file obbligatorio) |
| Immagini dei prodotti | Sì | Sì | Sì | No |
| Varianti | Sì | Sì | Sì | No |
| Clienti + indirizzi | Sì | Sì | Sì | Sì |
| Ordini | Sì | Sì, solo gli ultimi 60 giorni a meno che non venga aggiunto lo scope `read_all_orders` | Sì | Sì |
| Recensioni | Sì | Non supportate affatto | Di solito non disponibili — Magento Community non ha un endpoint REST per le recensioni | Sì |
| Coupon / sconti | Sì | Sì | Sì | No |
| Blog / contenuti CMS | Sì (post, categorie, tag, immagini) | Sì (articoli) | Sì (pagine CMS) | No |
| Affiliazioni, commissioni, pagamenti | Sì, richiede il plugin Spwig Migration Bridge | No | No | No |
| Rilevamento di campi personalizzati | Sì | No — i metafield di Shopify non vengono letti | No | n/a |

I commercianti Shopify dovrebbero pianificare di reinserire manualmente qualsiasi dato dei metafield (specifiche personalizzate dei prodotti, campi aggiuntivi dei clienti) dopo l'importazione, poiché non vengono rilevati o trasferiti. Per tutto il resto, vedi [Mapping dei campi di migrazione](migration-field-mapping) per sapere come i campi di origine vengono mappati sui campi Spwig.

## Pianificare la migrazione

- **Migra prima di andare online**, su un'installazione Spwig che non gestisce ancora il traffico reale, prima di puntare il DNS del tuo dominio su di essa — in questo modo puoi rivedere e correggere le cose senza che i clienti vedano un catalogo incompleto.
- **Mantieni il vecchio negozio in esecuzione in sola lettura**, finché non hai verificato che la copia Spwig sia corretta.
- **Pianifica del tempo per la configurazione delle tasse e della spedizione successivamente** — le impostazioni del wizard per questo sembrano importare le tue tariffe e zone, ma non vengono applicate (vedi [Mapping dei campi di migrazione](migration-field-mapping)). Configura da solo **Impostazioni > Tasse e Valuta** e **Impostazioni > Spedizione**.
- **Fai un controllo spot invece di scorrere** — le importazioni dei dati estesi avvengono su base di buona fede; un prodotto i cui dati estesi non possono essere letti verrà comunque creato, ma senza di essi. Vedi [Dopo la migrazione](after-migration-review) prima di annunciare qualcosa ai clienti.

- **Accesso amministrativo alla tua piattaforma di origine** per creare le credenziali API — una chiave API REST in WooCommerce, un'app personalizzata in Shopify o un token di integrazione in Magento.

Non necessario per CSV.
- **Ambiti di sola lettura** ovunque la piattaforma di origine li offra — Spwig legge solo dal tuo vecchio negozio, mai di nuovo su di esso.
- **Un budget di tempo** — ogni esecuzione ha un limite massimo di 4 ore.

Per un negozio grande, pianifica un approccio a fasi (categorie e prodotti prima, ordini in seguito) anziché un'unica passata.

> **Importante:** Spwig non crittografa le credenziali API che inserisci nel wizard. Una volta verificata la migrazione completa, revoca o elimina la credenziale sulla piattaforma di origine.

## Il wizard di migrazione, passo per passo

Il wizard ha sei passaggi, con il progresso salvato tra di essi:

1. **Piattaforma** — scegli WooCommerce, Shopify, Magento o Import CSV.
2. **Connessione** — inserisci le credenziali, con un'opzione (abilitata di default) per testare la connessione prima. Le guide specifiche per la piattaforma coprono esattamente cosa generare.
3. **Anteprima** — conteggi in tempo reale dal tuo negozio di origine, un campione dei primi 5 prodotti, e caselle di controllo per i tipi di dati da includere, più opzioni come la dimensione del lotto.
4. **Mapping** — come i campi della fonte vengono mappati sui campi di Spwig, eventuali campi personalizzati di WooCommerce e categorie senza un corrispondente ovvio. Dettagli completi in [Migration Field Mapping](migration-field-mapping).
5. **Import** — eseguito in background; puoi chiudere la scheda e continua comunque, con un log in tempo reale.
6. **Completato** — un riepilogo dei risultati, uno strumento per il riscrittura dei collegamenti per il contenuto che fa riferimento al tuo vecchio dominio, e download di report PDF/CSV.

## Dopo la tua migrazione

Un importo riuscito non è la linea di arrivo — vedi [After Your Migration](after-migration-review) per un elenco completo di verifiche che copre la verifica dei dati, la correzione dei collegamenti interni che puntano ancora al tuo vecchio dominio, e la configurazione delle tasse e della spedizione che il wizard non gestisce per te.

## Il rollback non è una rete di sicurezza

Capiscilo prima di iniziare, non dopo che qualcosa va storto. Il rollback esiste, ma non è il pulsante annulla che potrebbe sembrare:

- Non esiste un rollback automatico se un import fallisce a metà. Quello che è stato importato prima del fallimento rimane nel tuo negozio, e un import fallito non può essere annullato dall'amministrazione — dovrai revisionare e pulire i dati parziali manualmente.
- Una migrazione completata può essere annullata, e il rollback rimuove solo ciò che l'import stesso ha creato — mai di più. Un cliente migrato che ha effettuato un ordine reale dopo l'import mantiene il proprio account, gli indirizzi, la cronologia fedeltà e il credito negozio, e quell'ordine reale resta intatto; vengono rimossi solo gli ordini creati dall'import. Anche un prodotto migrato ancora referenziato da un ordine, un pacchetto, una carta regalo o uno slot del configuratore viene mantenuto, e gli ordini appartenenti ad altri clienti non vengono mai modificati.
- Gli affiliati, le commissioni e i pagamenti creati dall'import vengono rimossi, insieme a qualsiasi account affiliato creato dall'import — un affiliato collegato a un cliente già esistente mantiene il proprio account, e viene rimosso solo il record dell'affiliato. I piani di abbonamento, i livelli di prezzo e le risorse di prenotazione creati dalle estensioni del negozio continuano a non essere rimossi — puliscili manualmente.
- Prima di confermare, Spwig mostra un'anteprima di esattamente ciò che verrà rimosso e ciò che verrà mantenuto, per nome e conteggio, con la motivazione — calcolata rispetto ai tuoi dati reali. Leggila prima di confermare. Il rollback viene poi eseguito in background, quindi è sicuro chiudere la scheda; controlla il riepilogo della migrazione per il rapporto una volta terminato.
- Il rollback resta comunque un'azione permanente e distruttiva sui record che rimuove, quindi usalo con consapevolezza — e pulisci manualmente tutto ciò che Spwig mantiene e che in realtà non desideri. Ma poiché non va più oltre ciò che l'import ha creato, non è più uno strumento utilizzabile solo lo stesso giorno come una volta.
- Il pulsante Rollback rimane disponibile sul riepilogo di una migrazione completata fintanto che il record del lavoro esiste, e viene riproposto se un tentativo di rollback fallisce a sua volta a metà, così puoi riprovarlo. I record non vengono rimossi secondo alcuna pianificazione, quindi questo non scade da solo.

Se incontri una migrazione fallita o bloccata, [Migration Troubleshooting](migration-troubleshooting) copre il riprovare, il cancellare e la lettura dei log.

## Tips

- **Inizia con un test su una piccola scala** — categorie più una manciata di prodotti conferma che la mappatura dei campi sembra corretta prima del catalogo completo.
- **Leggi prima la guida specifica della piattaforma** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify), e [Migrating from Magento](migrate-from-magento) coprono esattamente le credenziali e gli ambiti di cui hai bisogno.
- **Non saltare la matrice delle funzionalità sopra** — sapere che le recensioni di Shopify o le varianti CSV non verranno trasferite ti risparmia una sorpresa dopo aver cambiato il DNS.
- **Mantieni aperto l'amministratore della tua piattaforma di origine in un'altra scheda** per generare o copiare le credenziali mentre procedi.
- **Tratta i checkbox del wizard letteralmente** — se un'impostazione non è descritta come funzionante qui, configurala direttamente in Spwig invece di fidarti del wizard.