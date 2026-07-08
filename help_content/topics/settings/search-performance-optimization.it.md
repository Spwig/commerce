---
title: Ottimizzazione delle Prestazioni di Ricerca
---

Le prestazioni della ricerca influiscono direttamente sull'esperienza dell'utente e sulle conversioni. Le ricerche lente frustrano gli utenti e aumentano il tasso di abbandono. Questa guida completa identifica i collo di bottiglia comuni nel sistema di ricerca nativo del database di Spwig, fornisce strategie di ottimizzazione e stabilisce obiettivi di prestazioni. Utilizza questa guida quando i tempi di risposta della ricerca superano i limiti accettabili o quando stai pianificando una crescita del catalogo.

Tempi di risposta obiettivo: <200ms per l'autocomplete, <500ms per la ricerca completa. Segui la checklist di ottimizzazione di seguito per raggiungere questi obiettivi.

## Comprendere le Metriche delle Prestazioni

Monitora queste metriche in **Search > Search Analytics**:

**Response Time** - Millisecondi necessari per eseguire una query di ricerca (solo lato server, esclude la latenza di rete)

**Cache Hit Rate** - Percentuale di ricerche servite dalla cache rispetto al database

**Query Count** - Numero di query del database per ricerca (meno è meglio)

**Database Query Time** - Tempo trascorso nel database rispetto al codice dell'applicazione

## Obiettivi di Prestazioni

| Tipo di Query | Obiettivo | Accettabile | Richiede Ottimizzazione |
|---------------|----------|-------------|--------------------------|
| Autocomplete | <200ms | 200-300ms | >300ms in modo costante |
| Ricerca Completa | <500ms | 500-800ms | >800ms in modo costante |
| Ricerca Amministrativa | <1000ms | 1000-1500ms | >1500ms in modo costante |

Se i tuoi tempi di risposta medi superano i limiti "Richiede Ottimizzazione", implementa le strategie di seguito.

## Monitoraggio delle Prestazioni

**Media del Tempo di Risposta del Dashboard Analytics**

Naviga in **Search > Search Analytics** per visualizzare il tempo di risposta medio su tutte le ricerche. Questo è il tuo principale indicatore di monitoraggio delle prestazioni.

**Quando investigare**: Tempo di risposta medio >300ms per l'autocomplete o >800ms per la ricerca completa in modo costante su più giorni.

**Monitoraggio Settimanale**: Rivedi le analisi ogni lunedì per individuare prestazioni in calo in anticipo.

## Colli di Bottiglia Noti delle Prestazioni

La ricerca nativa del database di Spwig presenta diversi collo di bottiglia documentati da evitare:

### Calcolo CTR N+1 Query

**Cosa è**: Il calcolo del tasso di clic-through nel AnalyticsService esegue query separate per ogni elemento del risultato aggregato.

**Impatto**: Grave per negozi ad alto traffico con molte query tracciate.

**Posizione del Codice**: `search/services/analytics_service.py` - metodo `get_click_through_rate()`

**Mitigazione**: Evita di chiamare i calcoli CTR in produzione. Questo è principalmente un'analisi amministrativa che dovrebbe essere calcolata in modo asincrono, non durante le richieste rivolte agli utenti.

### Aggregazione del Magazzino

**Cosa è**: `with_stock_totals()` calcola le quantità disponibili su tutti i magazzini per prodotto.

**Impatto**: Costoso per cataloghi >1.000 prodotti. Viene chiamato quando si utilizza il filtro `in_stock` o si visualizza lo stato del magazzino nell'autocomplete.

**Trigger**: **Search Settings > Autocomplete** - opzione "Mostra stato del magazzino"

**Consiglio**: MAI abilitare lo stato del magazzino nell'autocomplete per cataloghi di grandi dimensioni. Aggiunge 200-500ms per richiesta.

### Join delle Varianti

**Cosa è**: Le ricerche SKU attivano JOIN sulla tabella delle varianti per cercare SKU delle varianti.

**Impatto**: 2-3 volte più lente sui prodotti con molte varianti (10+ varianti per prodotto).

**Mitigazione**: Utilizza `.distinct()` per evitare duplicati, che aggiunge un overhead. Necessario per la funzionalità SKU - non disattivarlo a meno che non vengano utilizzati SKU.

### Conteggio dei Prodotti nell'Autocomplete

**Cosa è**: I risultati dell'autocomplete per categoria/marca mostrano i contatori dei prodotti ("Elettronica (234)")

**Impatto**: Ogni tipo di contenuto con i contatori abilitati aggiunge 2 query extra. Le query includono join e aggregazioni.

**Trigger**: **Search Settings > Autocomplete** - "Mostra Conteggio Prodotti" per categorie/marchi

**Consiglio**: Disattiva i contatori dei prodotti. Risparmia 2-4 query per richiesta di autocomplete. Il miglior ottimizzazione dell'autocomplete.

### Indicizzazione dei Documenti

**Cosa è**: Estrazione del testo da file PDF/DOCX/XLSX durante le query di ricerca.

**Impatto**: Estremamente costoso (I/O del file + estrazione del testo). Operazioni bloccanti sincrone.

**Trigger**: **Search Settings > Indicizzazione Approfondita** - "Indicizza Documenti"

**Consiglio**: Raramente giustificabile il costo delle prestazioni. ABILITA SOLO per piccoli cataloghi di prodotti digitali (<500 prodotti) dopo test approfonditi.

## Configurazione della Cache

La cache è l'ottimizzazione di prestazioni più efficace.

**Cache dell'Autocomplete** - Default: 60s
- **Intervallo Consigliato**: 45-90s
- **TTL più alto (90-120s)**: Migliore prestazione se le modifiche all'inventario avvengono raramente
- **TTL più basso (30-45s)**: Risultati più aggiornati se si aggiungono prodotti ogni ora

**Cache dei Risultati** - Default: 300s (5 minuti)
- **Intervallo Consigliato**: 180-600s
- **TTL più alto (600s/10min)**: Miglioramento significativo delle prestazioni per cataloghi statici
- **TTL più basso (180s)**: Risultati più aggiornati se si aggiornano frequentemente i dati del prodotto

**Strategia di Ottimizzazione**: Se le ricerche sono lente, raddoppia il TTL della cache prima di disattivare le funzionalità. Passare da 60s a 120s per la cache dell'autocomplete riduce il carico del database a metà.

## Checklist di Ottimizzazione dell'Autocomplete

Applica questi cambiamenti alle impostazioni dell'autocomplete per ottenere le prestazioni massime:

**1. Aumenta il Debounce a 300-400ms**
- Posizione: **Search Settings > Autocomplete** - "Debounce Delay"
- Impatto: Riduce le chiamate API attendendo più a lungo tra i tasti premuti
- Compromesso: Leggermente meno reattivo (impercettibile per la maggior parte degli utenti)

**2. Riduci il Max Results da 8 a 5-6**
- Posizione: **Search Settings > Autocomplete** - "Max Results Per Type"
- Impatto: Insiemi di risultati più piccoli = query più veloci e payload JSON più piccoli
- Compromesso: Meno opzioni mostrate (di solito sufficiente)

**3. Disattiva i Contatori dei Prodotti (MAGGIOR VANTAGGIO)**
- Posizione: **Search Settings > Autocomplete** - Disattiva "Mostra Conteggio Prodotti" per categorie/marchi
- Impatto: Risparmia 2-4 query per richiesta di autocomplete
- Compromesso: Nessun contatore dei prodotti nel menu a discesa (raramente necessario)

**4. Disattiva lo Stato del Magazzino**
- Posizione: **Search Settings > Autocomplete** - Disattiva "Mostra Stato del Magazzino"
- Impatto: Elimina l'aggregazione costosa del magazzino
- Compromesso: Nessun badge di magazzino (non critico nel contesto dell'autocomplete)

**5. Disattiva le Descrizioni dei Prodotti**
- Posizione: **Search Settings > Autocomplete** - Disattiva "Mostra Descrizione"
- Impatto: Riduce il processamento del testo e la dimensione del payload
- Compromesso: Meno testo di anteprima (il nome del prodotto è di solito sufficiente)

**6. Aumenta il TTL della Cache a 90s**
- Posizione: **Search Settings > Caching** - "Autocomplete Cache TTL"
- Impatto: Più richieste servite dalla cache
- Compromesso: Risultati fino a 90 secondi obsoleti (accettabile per la maggior parte dei negozi)

**Miglioramento Previsto**: Applicando tutte e 6 le ottimizzazioni, il tempo di risposta dell'autocomplete viene ridotto del 50-70%.

## Ottimizzazione dell'Indicizzazione Approfondita

Ogni opzione di indicizzazione approfondita aggiunge un overhead. Disattivala in base alle dimensioni del catalogo:

| Dimensione del Catalogo | Indicizzazione Approfondita Consigliata |
|-------------------------|----------------------------------------|
| **<1.000 prodotti** | Tutte ABILITATE (impatto minimo) |
| **1.000-10.000** | Mantieni SKUs, Attributi, Campi Personalizzati ABILITATI; Disattiva Recensioni |
| **10.000-20.000** | Mantieni SKUs, Attributi ABILITATI; Disattiva Campi Personalizzati, Recensioni |
| **20.000-50.000** | Mantieni solo SKUs ABILITATI; Disattiva tutto il resto |
| **>50.000** | Mantieni SKUs ABILITATI; Considera la migrazione a Elasticsearch |

**Indicizzazione dei Documenti**: SEMPRE DISABILITATA a meno che non sia critica (prodotti digitali con documenti cercabili E <500 prodotti totali).

## Ottimizzazione dei Tipi di Contenuto

Disattiva i tipi di contenuto non utilizzati in **Search Settings > Content Types**:

- **Nessun blog?** Disattiva "Blog Posts" - risparmia query
- **Nessun filtro per marca?** Disattiva "Brands" - risparmia query
- **Negozio solo per acquisti?** Disattiva "Categories" e "Blog Posts"

Ogni tipo di contenuto disattivato elimina query del database da ogni ricerca.

## Ottimizzazione del Database

Spwig crea gli indici necessari tramite migrazioni. Fidati di loro - non creare indici aggiuntivi senza profilare.

**Manutenzione PostgreSQL** (se si utilizza PostgreSQL):
- Esegui `VACUUM ANALYZE` settimanalmente per aggiornare le statistiche del pianificatore delle query
- I cataloghi di grandi dimensioni beneficiano di un `VACUUM FULL` mensile (richiede tempo di inattività)

**Monitora il Tempo di Query del Database**: Durante lo sviluppo, identifica le query lente utilizzando strumenti di profilatura. La maggior parte dell'ottimizzazione delle query è già implementata:
- `.select_related('brand', 'category')` sui prodotti
- `.prefetch_related('images')` per le miniature
- `.distinct()` per le ricerche di varianti

## Prestazioni del Matching Fuzzy

La distanza di Levenshtein è computazionalmente costosa (complessità O(m*n)):

**Ottimizzazione del Threshold**:
- **Threshold più alto (0,85 vs 0,80)**: Più veloce ma cattura meno errori di battitura
- **Threshold più basso (0,75 vs 0,80)**: Più lento ma più tollerante

**Ottimizzazione del Max Edits**:
- **Max edits più basso (1 vs 2)**: Più veloce ma perde più errori di battitura
- **Max edits più alto (2 vs 3)**: Più lento ma cattura più errori di battitura

**Prestazioni della Libreria**: Spwig utilizza `rapidfuzz` se disponibile (10 volte più veloce del puro Python). Assicurati che sia installato: `pip install rapidfuzz`

## Prestazioni dei Sinonimi e dei Redirect

**Espansione delle Query dei Sinonimi**: Ogni sinonimo aggiunge clausole OR alla query di ricerca. Limita a un massimo di 10-20 sinonimi per termine.

**Tipo di Match Regex**: I redirect regex sono più lenti rispetto a exact/contains/starts_with. Evita pattern complessi.

**Consiglio**: Utilizza tipi di match semplici quando possibile. Riserva regex ai casi in cui non funzionano altri tipi di match.

## Ottimizzazione per Cataloghi Grandi (>10.000 prodotti)

Strategie specifiche per cataloghi grandi:

**1. Caching Aggressivo**
- Autocomplete: TTL 90-120s
- Risultati: TTL 600s (10 min) 
- Accetta l'obsolescenza per le prestazioni

**2. Indicizzazione Approfondita Minimale**
- Solo SKUs (disattiva attributi, campi personalizzati, recensioni)
- Testa le prestazioni con e senza attributi

**3. Risultati Ridotti dell'Autocomplete**
- Massimo 5 risultati per tipo (da 8)
- Riduce l'overhead delle query

**4. Disattiva lo Stato del Magazzino ovunque**
- Nell'autocomplete
- Nei risultati della ricerca se visualizzato

**5. Considera Elasticsearch a partire da 50K prodotti**
- La ricerca nativa del database è adatta fino a circa 50.000 prodotti
- Oltre a questo, Elasticsearch è consigliato per:
  - Ricerca faceta complessa
  - Carico di ricerca elevato (concorrente >100 ricerche/sec)
  - Tempi di risposta costantemente >500ms nonostante l'ottimizzazione

## Prestazioni Multilingua

L'indicizzazione JSONField JSONB (PostgreSQL) rende la multilingua efficiente:

- **1-3 lingue**: Overhead minimo (5-10ms)
- **5+ lingue**: Aumento minore nella complessità delle query (20-40ms)
- **10+ lingue**: Overhead notevole (50-100ms)

L'overhead aumenta linearmente con il numero di lingue.

## Correzioni di Prestazioni di Emergenza

Se le ricerche sono criticamente lente (>2s di tempo di risposta), applica queste correzioni immediate nell'ordine seguente:

**Immediato** (applica ora):
1. Disattiva l'indicizzazione dei documenti
2. Disattiva i contatori dei prodotti nell'autocomplete
3. Aumenta i TTL della cache a 120s autocomplete / 600s risultati

**Rapido** (applica entro 24 ore):
4. Disattiva lo stato del magazzino nell'autocomplete
5. Riduci il numero massimo di risultati dell'autocomplete a 5
6. Disattiva le descrizioni dei prodotti nell'autocomplete

**Medio** (applica entro una settimana):
7. Disattiva l'indicizzazione delle recensioni se >20K prodotti
8. Rivedi e disattiva i tipi di contenuto non utilizzati
9. Aumenta il debounce a 400ms

**Miglioramento Previsto**: Queste 9 correzioni riducono in genere i tempi di risposta del 60-80% sui cataloghi di grandi dimensioni.

## Consigli

- **Monitora i tempi di risposta settimanalmente** - Individua prestazioni in calo in anticipo
- **Le aumenti della cache sono la prima ottimizzazione** - Raddoppiare il TTL della cache è il miglior guadagno facile
- **Conteggio dei prodotti nell'autocomplete = costoso** - Il principale killer delle prestazioni dell'autocomplete
- **L'indicizzazione dei documenti è quasi mai giustificabile** - Il costo delle prestazioni raramente giustifica il beneficio
- **Testa un cambiamento alla volta** - Non puoi identificare causa/effetto con cambiamenti simultanei
- **Benchmarka con volumi di dati realistici** - Testa con cataloghi di dimensioni di produzione
- **L'aggregazione del magazzino distrugge le prestazioni nei cataloghi grandi** - Evita di visualizzare lo stato del magazzino nell'autocomplete
- **Considera Elasticsearch a partire da 50K+ prodotti** - La ricerca nativa del database ha limiti

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.