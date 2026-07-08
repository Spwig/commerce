---
title: Pesi di Rilevanza e Indicizzazione Approfondita
---

I pesi di rilevanza e l'indicizzazione approfondita controllano come vengono classificati i risultati di ricerca e quali dati del prodotto vengono cercati. I pesi sono moltiplicatori di importanza - un peso 2.0 significa che le corrispondenze in quel campo sono due volte più importanti di un peso 1.0. L'indicizzazione approfondita determina se la ricerca va oltre i nomi dei prodotti di base per includere SKU, attributi, recensioni e anche il contenuto dei documenti. Questa guida spiega entrambi i sistemi, quando modificarli e le implicazioni critiche sulle prestazioni.

I valori predefiniti funzionano bene per la maggior parte dei negozi e-commerce. Modificare solo se si hanno esigenze specifiche di classificazione o indicizzazione.

![Tabella dei Pesi](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Comprendere i Pesi

I pesi sono moltiplicatori (scala 0.0-2.0) applicati quando vengono trovate corrispondenze di testo in diversi campi. Pesi più elevati significano che le corrispondenze in quel campo hanno un punteggio più alto nei risultati.

**Esempio**: Se un prodotto ha "laptop" sia nel nome (peso 1.50) che nella descrizione (peso 0.80):
- La corrispondenza del nome contribuisce 1.50 al punteggio di rilevanza
- La corrispondenza della descrizione contribuisce 0.80
- Il punteggio complessivo determina la classificazione rispetto ad altri prodotti

I pesi consentono di priorizzare alcuni campi rispetto ad altri quando si classificano i risultati della ricerca.

## Categorie di Pesi e Valori Predefiniti

Passa a **Impostazioni di Ricerca > Tabella dei Pesi** per visualizzare tutte le impostazioni dei pesi:

| Campo | Peso Predefinito | Rationale |
|-------|---------------|-----------|
| **weight_name** | 1.50 | I nomi dei prodotti sono i più importanti - i clienti si aspettano corrispondenze esatte nei nomi in cima |
| **weight_sku** | 1.20 | Gli SKU sono identificatori specifici - importanti per i negozi B2B e i clienti che tornano |
| **weight_description** | 0.80 | Le descrizioni forniscono contesto ma sono meno importanti delle corrispondenze esatte nei nomi |
| **weight_categories** | 0.80 | Le corrispondenze di categoria sono utili per la navigazione ma non sono altrettanto specifiche del nome/ISBN |
| **weight_attributes** | 0.70 | Ricerca per colore, dimensione, materiale - utile ma informazione di supporto |
| **weight_brands** | 0.70 | Filtraggio per marca importante ma non criterio principale di ricerca per la maggior parte dei negozi |
| **weight_blog_posts** | 0.60 | Il contenuto del blog è meno importante nella ricerca orientata all'e-commerce (priorità più bassa) |
| **weight_reviews** | 0.50 | Contenuto generato dagli utenti meno controllato - peso più basso |

Questi valori predefiniti presuppongono un negozio e-commerce tipico dove la scoperta dei prodotti è l'obiettivo principale della ricerca.

## Quando Modificare i Pesi

Modificare i pesi quando le priorità del tuo negozio differiscono dai modelli tipici di e-commerce:

**Negozio a SKU Pesanti (B2B, Grossista)** - Aumenta `weight_sku` a 1.8-2.0 in modo che le ricerche per codice prodotto dominino i risultati. I clienti B2B spesso cercano per SKU esatti.

**Negozio Orientato alle Marche** - Aumenta `weight_brands` a 1.2-1.5 quando i clienti acquistano principalmente per marca (abbigliamento di design, prodotti di lusso).

**Negozio a Contenuti Pesanti** - Aumenta `weight_blog_posts` a 0.9-1.2 se sei un editore di contenuti o un rivenditore educativo dove i post del blog sono altrettanto importanti dei prodotti.

**Negozio a Attributi Pesanti (Moda)** - Aumenta `weight_attributes` a 1.0-1.2 quando i clienti cercano frequentemente per attributi di colore, dimensione, stile.

## Esempi di Modifica dei Pesi

| Tipo di Negozio | Modifiche Consigliate |
|-----------|------------------------|
| **B2B Grossista** | weight_sku: 2.0, weight_name: 1.3, weight_description: 0.6 - Priorità ai codici prodotto |
| **Boutique di Moda** | weight_attributes: 1.2, weight_brands: 1.2, weight_name: 1.4 - Colore/stile/marca importanti |
| **Editore di Contenuti** | weight_blog_posts: 1.2, weight_name: 1.3, weight_reviews: 0.7 - Contenuti altrettanto importanti dei prodotti |
| **E-commerce Generale** | Usa i valori predefiniti - Bilanciato per i negozi online tipici |

Modifica un peso alla volta e testa prima di apportare ulteriori modifiche.

## Panoramica dell'Indicizzazione Approfondita

⚠️ **AVVERTENZA SULLE PRESTAZIONI** - Ogni opzione di indicizzazione approfondita aggiunge complessità e sovraccarico alle query.

L'indicizzazione approfondita estende la ricerca al di là del nome/descrizione di base del prodotto in dati aggiuntivi:

![Tabella dell'Indicizzazione Approfondita](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Passa a **Impostazioni di Ricerca > Tabella dell'Indicizzazione Approfondita** per configurare.

## Indicizza SKU

**Predefinito**: ON, **Impatto sulle Prestazioni**: Basso

Includi SKU e varianti SKU nell'indice di ricerca. Triggers JOIN varianti (costo minore).

**Quando mantenerlo attivo**: Essenziale per i negozi B2B dove i clienti conoscono i codici prodotto. Utile anche per i clienti che tornano e ricordano l'SKU da ordini precedenti.

**Quando disattivarlo**: Mai, a meno che non si abbiano letteralmente nessun SKU assegnato. L'impatto sulle prestazioni è trascurabile.

## Indicizza Attributi

**Predefinito**: ON, **Impatto sulle Prestazioni**: Medio

Includi attributi del prodotto (colore, dimensione, materiale, attributi personalizzati) nell'indice di ricerca. JOIN alla tabella degli attributi.

**Quando mantenerlo attivo**: Importante per la moda, prodotti configurabili o qualsiasi negozio dove i clienti cercano per caratteristiche del prodotto ("abito rosso", "maglietta grande").

**Quando disattivarlo**: Cataloghi >20.000 prodotti con molti attributi per prodotto possono vedere un sovraccarico di 50-100ms. Disattivarlo solo se le prestazioni sono critiche e i clienti non cercano per attributi.

## Indicizza Campi Personalizzati

**Predefinito**: ON, **Impatto sulle Prestazioni**: Medio

Includi campi personalizzati definiti dal commerciante da JSONField nell'indice di ricerca. Richiede l'analisi di JSONField.

**Quando mantenerlo attivo**: Se si utilizzano campi personalizzati per dati dei prodotti cercabili (informazioni sulle garanzie, specifiche, dettagli di compatibilità).

**Quando disattivarlo**: Se non si utilizzano campi personalizzati, o i campi personalizzati contengono dati non cercabili (note interne, codici contabili). Disattivarlo risparmia l'overhead del processing JSONField.

## Indicizza Recensioni

**Predefinito**: ON, **Impatto sulle Prestazioni**: Medio-Alto

Includi titoli e commenti delle recensioni approvate nell'indice di ricerca. JOIN alla tabella delle recensioni e aggiunge sovraccarico di ricerca testuale.

**Quando mantenerlo attivo**: Cataloghi con molte recensioni dove i clienti cercano prodotti in base al contenuto delle recensioni ("borsa impermeabile per laptop" potrebbe apparire nel testo delle recensioni).

**Quando disattivarlo**: Cataloghi >20.000 prodotti o negozi con molte recensioni per prodotto. Aggiunge un sovraccarico di 100-200ms su cataloghi di grandi dimensioni.

## Indicizza Documenti

**Predefinito**: OFF, **Impatto sulle Prestazioni**: MOLTO ALTO 🚨

**NON ABILITARE MAI CASUALMENTE** - Funzione di ricerca più costosa.

L'indicizzazione dei documenti estrae il testo da file PDF, DOCX e XLSX allegati ai prodotti digitali, rendendo i contenuti dei file cercabili.

**Dettagli tecnici**:
- Utilizza le librerie PyPDF2, python-docx e openpyxl
- I/O file sincrono ed estrazione del testo durante la ricerca
- Traccia i file tramite checksum MD5 (riindicizza solo quando il file cambia)
- Potenziali timeout su file di grandi dimensioni (>10MB PDF)

**Impatto sulle Prestazioni**:
- Indicizzazione iniziale molto costosa (minuti a ore per grandi biblioteche)
- Sovraccarico significativo delle query (latenza aggiuntiva di 100-500ms)
- Intensivo in termini di memoria per documenti di grandi dimensioni

**Abilitare solo se**:
- Si vendono prodotti digitali con documenti cercabili (ebook, report, manuali)
- Il catalogo è piccolo (<500 prodotti digitali)
- Il server ha risorse sufficienti
- Si è testato l'impatto in modo approfondito

**Per i negozi di prodotti digitali**: Considerare se i clienti realmente necessitano di cercare i contenuti dei documenti, o se la ricerca per nome/descrizione del prodotto è sufficiente.

## Tabella dell'Impatto sulle Prestazioni

| Funzione | Predefinito | Impatto | Utilizzare Quando |
|---------|---------|--------|----------|
| Indicizza SKU | ON | Basso | Sempre (essenziale per B2B) |
| Indicizza Attributi | ON | Medio | Prodotti configurabili |
| Indicizza Campi Personalizzati | ON | Medio | Utilizzo di campi personalizzati |
| Indicizza Recensioni | ON | Medio-Alto | Negozio con molte recensioni |
| Indicizza Documenti | OFF | MOLTO ALTO | Solo prodotti digitali (test prima) |

L'impatto si basa su cataloghi tipici. I cataloghi di grandi dimensioni (>50.000 prodotti) sperimentano un sovraccarico proporzionalmente più alto.

## Test delle Modifiche ai Pesi

Quando si modificano i pesi, seguire questo flusso di lavoro per i test:

1. **Modifica un peso alla volta** - Non modificare più pesi contemporaneamente; non saprai quale cambiamento ha causato i risultati
2. **Incrementi piccoli** - Modifica di ±0.2 alla volta (es. 1.0 → 1.2, non 1.0 → 1.8)
3. **Testa con query reali** - Utilizza termini di ricerca effettivi dei clienti provenienti dall'analisi, non test casuali
4. **Monitora l'analisi** - Confronta la rilevanza dei risultati prima/dopo utilizzando le query principali
5. **Aspetta 1-2 settimane** - Dà ai clienti tempo per interagire con le nuove classificazioni
6. **Misura i tassi di clic** - I clienti stanno cliccando di più o meno rispetto al passato?

## Bilanciamento tra Prestazioni e Precisione

Più indicizzazione = risultati di ricerca migliori ma prestazioni più lente:

**Scenario: Catalogo Piccolo (<1.000 prodotti)**
- Abilita tutte le opzioni di indicizzazione (SKU, attributi, campi personalizzati, recensioni)
- Impatto sulle prestazioni minimo
- Capacità di ricerca complete

**Scenario: Catalogo Medio (1.000-10.000 prodotti)**
- Mantieni SKU, attributi, campi personalizzati attivi
- Considera disattivare le recensioni se la media è >10 recensioni per prodotto
- Monitora i tempi di risposta

**Scenario: Catalogo Grande (>10.000 prodotti)**
- Mantieni SKU attivi (impatto basso)
- Disattiva l'indicizzazione delle recensioni (alto impatto)
- Disattiva i campi personalizzati se non utilizzati
- MAI abilitare l'indicizzazione dei documenti
- Considera Elasticsearch a partire da >50.000 prodotti

Bilancia in base alle dimensioni del catalogo e alle risorse del server.

## Soprascrizioni dei Pesi Specifiche del Motore

Quando si crea un motore di ricerca tramite il wizard (Passo 3), è possibile sovrascrivere i pesi globali per quel motore specifico.

**Caso d'uso**: Motore orientato ai blog
- Crea il motore "blog"
- Sovrascrivi `weight_blog_posts` a 1.5 (vs globale 0.60)
- Il contenuto del blog ora ha un punteggio più alto nelle ricerche del motore blog

La maggior parte dei motori non dovrebbe sovrascrivere i pesi - lascia vuoto per ereditare le impostazioni globali.

## Consigli

- **Mai abilitare l'indicizzazione dei documenti a meno che non sia assolutamente critico** - Costo di prestazioni più alto di qualsiasi altra funzione di ricerca
- **Negozio B2B: Aumenta weight_sku a 2.0** - I codici prodotto sono il metodo principale di ricerca
- **Testa le modifiche ai pesi durante le ore a bassa intensità di traffico** - Osserva l'impatto sulle prestazioni prima delle ore di punta
- **Monitora i tempi di risposta dopo aver abilitato l'indicizzazione** - Controlla il pannello di analisi per eventuali rallentamenti
- **Disattiva l'indicizzazione delle recensioni sui cataloghi >20K prodotti** - Impatto significativo sulle prestazioni
- **Modifica un peso alla volta per i test** - Non è possibile determinare causa/effetto con modifiche simultanee
- **L'estrazione dei documenti richiede PyPDF2/docx/openpyxl** - Verifica che queste librerie siano installate prima di abilitare l'indicizzazione dei documenti

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.