---
title: Configuring Autocomplete
---

Autocomplete, anche chiamato ricerca prevedibile o ricerca mentre si digita, mostra i risultati mentre i clienti digitano le loro query. Questo migliora drasticamente l'esperienza utente aiutando i clienti a trovare i prodotti più velocemente e riducendo le ricerche senza risultati. Questa guida spiega come configurare il comportamento dell'autocomplete, le impostazioni di visualizzazione e i compromessi di prestazioni.

L'autocomplete è abilitato di default con impostazioni ragionevoli. Modificate queste solo se avete preoccupazioni specifiche sulle prestazioni o preferenze di visualizzazione.

![Autocomplete Settings](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Abilitare l'Autocomplete

Navigare verso **Search > Search Settings** e cliccare sulla scheda **Autocomplete**.

**Enable Autocomplete** - Interruttore principale per la ricerca prevedibile. Quando abilitato, gli input di ricerca mostrano un menu a discesa dei risultati mentre i clienti digitano.

**Max Results Per Type** - Default: 8 elementi. Quanti risultati mostrare per ogni tipo di contenuto (prodotti, categorie, marche, post del blog). Valori più bassi (5-6) riducono la dimensione del payload API e rendono più veloce il rendering. Valori più alti (10-12) danno ai clienti più opzioni ma rallentano la risposta.

## Timing di Debounce

⚠️ **AVVISO SULLE PRESTAZIONI** - Il timing di debounce influisce significativamente sul carico del server.

**Debounce Delay** - Default: 300ms. Quanto attendere dopo l'ultimo tasto premuto prima di attivare una richiesta di autocomplete.

Questo'impostazione bilancia la risponsività con il carico del server:

| Delay | User Experience | Server Impact |
|-------|----------------|---------------|
| **100ms** | Molto reattivo | 3x più chiamate API rispetto a 300ms - alto carico |
| **200ms** | Reattivo | 1.5x più chiamate API rispetto a 300ms |
| **300ms** | Buon equilibrio (consigliato) | Linea di base |
| **400ms** | Leggermente lento | Meno chiamate API - carico ridotto |
| **500ms** | Ritardo notevole | 50% meno chiamate ma sembra lento |

**Consiglio**: Mantenere tra 250-350ms. Aumentare solo sopra 350ms se il vostro server ha difficoltà con il carico di autocomplete. Mai andare sotto 200ms a meno che non si abbia un server molto veloce e un catalogo piccolo.

## Impostazioni di Visualizzazione per i Prodotti

Questi interruttori controllano che informazioni appaiono nei risultati dell'autocomplete per i prodotti:

**Show Thumbnail** - Default: ON. Mostra l'immagine del prodotto accanto al risultato. **Impatto sulle prestazioni**: Aggiunge una query sull'immagine e aumenta la dimensione del payload JSON. Disattivarlo per un autocomplete più veloce su connessioni lente.

**Show Description** - Default: OFF. Mostra la descrizione breve del prodotto. **Impatto sulle prestazioni**: Aggiunge un elaborazione del testo e aumenta significativamente la dimensione del payload. Mantenere disattivato a meno che le descrizioni non siano critiche per la selezione del prodotto.

**Show Price** - Default: ON. Mostra il prezzo del prodotto. **Impatto sulle prestazioni**: Basso - i dati del prezzo sono già caricati con il prodotto. Sicuro da lasciare abilitato.

**Show SKU** - Default: ON. Mostra lo SKU del prodotto. **Impatto sulle prestazioni**: Basso - lo SKU è già indicizzato. Essenziale per i negozi B2B.

**Show Stock Status** - Default: OFF. **⚠️ AVVISO SULLE PRESTAZIONI IMPORTANTE**

Mostra i badge 'In Stock', 'Low Stock' o 'Out of Stock'. **Mai abilitare questo su cataloghi grandi**.

Lo stato del stock richiede l'aggregazione `with_stock_totals()` - calcolando le quantità disponibili in tutti i magazzini per ogni prodotto nei risultati dell'autocomplete. Questo aggiunge:
- Un carico significativo sul database (query di aggregazione)
- 200-500ms di latenza aggiuntiva su cataloghi >1.000 prodotti
- Potenziali timeout su cataloghi >10.000 prodotti

Abilitare solo se assolutamente necessario e se avete <500 prodotti.

## Impostazioni di Visualizzazione per i Post del Blog

**Show Featured Image** - Default: ON. Miniatura del post del blog nei risultati dell'autocomplete.

**Show Excerpt** - Default: ON. Testo breve di anteprima dal contenuto del post.

**Excerpt Length** - Default: 60 caratteri. Quanto testo di anteprima mostrare.

Queste impostazioni hanno un impatto minimo sulle prestazioni poiché i post del blog sono tipicamente pochi rispetto ai prodotti.

## Impostazioni di Visualizzazione per Categorie e Marche

**Show Thumbnail/Logo** - Default: ON. Immagine della categoria o del marchio nei risultati.

**Show Product Count** - Default: OFF. **⚠️ AVVISO SULLE PRESTAZIONI**

Mostra quanti prodotti sono in ogni categoria o marchio (es. 'Elettronica (234)').

**Mai abilitare questo su cataloghi grandi**. I conteggi dei prodotti vengono ricalcolati su ogni richiesta di autocomplete:
- Ogni tipo di contenuto con i conteggi abilitati aggiunge 2 query extra
- Le query includono join e aggregazioni
- Latenza aggiuntiva tipica di 100-300ms
- Aumenta linearmente con il numero di categorie/marche

Abilitare solo se avete <50 categorie/marche E <1.000 prodotti totali.

## Caching

**Autocomplete Cache TTL** - Default: 60 secondi (impostato nella scheda Caching).

I risultati dell'autocomplete vengono memorizzati in cache per migliorare le prestazioni. Il TTL di 60 secondi significa:
- Il primo cliente che cerca 'laptop' attiva una query sul database
- Per i successivi 59 secondi, tutte le ricerche 'laptop' restituiscono i risultati memorizzati in cache
- Dopo 60 secondi, la cache scade e la prossima ricerca aggiorna i dati

**Consiglio per il TTL**:
- **45-60s**: Buon equilibrio per la maggior parte dei negozi (predefinito)
- **90-120s**: Migliore prestazione se l'inventario dei prodotti cambia raramente
- **30s**: Risultati più recenti se aggiungete spesso prodotti nuovi

Aumentare il TTL della cache è il modo più semplice per migliorare le prestazioni dell'autocomplete.

## Autocomplete Multilingua

Se avete configurato più lingue, l'autocomplete cerca automaticamente il contenuto tradotto memorizzato nei campi JSONField.

**Come funziona**:
- Il cliente cerca in spagnolo: 'zapatos'
- Il sistema cerca le traduzioni dei nomi dei prodotti in spagnolo
- I risultati mostrano i nomi dei prodotti in spagnolo dati da JSONField
- Si passa alla lingua base se la traduzione in spagnolo non è disponibile

**Prestazioni**: Overhead minimo per 1-3 lingue. Con 5+ lingue, un leggero aumento nella complessità delle query.

## Test dell'Autocomplete

Dopo aver configurato le impostazioni, testare l'esperienza dell'autocomplete:

1. **Aprire la homepage del vostro negozio** in una finestra incognito
2. **Cliccare sulla casella di ricerca** per metterla a fuoco
3. **Digitare lentamente il nome di un prodotto comune** (es. 'laptop')
4. **Osservare**:
   - Quanto velocemente appaiono i risultati dopo che smettete di digitare (il debounce funziona?)
   - Che informazioni vengono mostrate (immagini, prezzi, SKU come configurato)
   - Se i risultati sono rilevanti (verificare i pesi di rilevanza se non lo sono)
5. **Testare su mobile** - Assicurarsi che il menu a discesa sia amichevole al tocco e leggibile

## Consigli

- **Disabilitare le descrizioni dei prodotti per velocità** - Le descrizioni aumentano significativamente la dimensione del payload con un valore minimo nel contesto dell'autocomplete
- **Mai abilitare lo stato del stock su cataloghi grandi** - L'aggregazione del stock distrugge le prestazioni dell'autocomplete
- **Testare su mobile con target di tocco** - I risultati dell'autocomplete devono essere facilmente toccabili sui telefoni
- **Monitorare i tempi di risposta settimanalmente** - Obiettivo <200ms per le richieste di autocomplete
- **Aumentare il TTL della cache se lento** - Ottimizzazione più semplice per le prestazioni
- **I conteggi dei prodotti sono costosi - disabilitarli a meno che non siano critici** - Ogni conteggio di categoria/marchio aggiunge 2 query a ogni richiesta di autocomplete