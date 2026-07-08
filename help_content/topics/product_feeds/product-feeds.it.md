---
title: Feed dei prodotti
---

I feed dei prodotti ti permettono di esportare il tuo catalogo su piattaforme di acquisto come Google Shopping e Facebook Catalog. Una volta collegati, i dati dei tuoi prodotti vengono sincronizzati automaticamente in base a un programma, in modo che gli annunci riflettano sempre i prezzi, lo stock e i dettagli dei prodotti correnti.

La tua negozio utilizza un sistema di componenti provider per i feed. Ogni provider di feed (Google, Facebook o altri) viene installato come componente e successivamente collegato tramite un account provider. Puoi eseguire più provider di feed contemporaneamente - ad esempio, un feed per Google Shopping e uno separato per Facebook.

## Collegamento di un provider di feed

Prima di poter sincronizzare il tuo catalogo, devi installare e collegare almeno un componente provider di feed.

### Installazione di un componente provider

I componenti provider sono disponibili nel mercato dei componenti Spwig. L'amministratore del tuo negozio li installa attraverso il sistema di aggiornamento dei componenti. Una volta installato un componente provider, appare come opzione quando si crea un account provider di feed.

### Creazione di un account provider di feed

1. Vai a **Marketing > Provider di Feed**
2. Clicca su **+ Aggiungi account provider di feed**
3. Compila il modulo:

**Sezione Informazioni sul provider:**
- **Sito** — seleziona il tuo negozio (esiste solo uno)
- **Componente provider** — scegli il provider di feed installato (es. Google Shopping, Facebook Catalog)
- **Nome account** — un nome descrittivo come `Google Shopping — Main` o `Facebook Catalog — US`

**Sezione Configurazione:**
- **Attivo** — spunta per abilitare la generazione e la sincronizzazione del feed
- **Principale** — spunta se questo è il tuo provider di feed principale per questo tipo di piattaforma
- **Priorità** — controlla l'ordine di ordinamento nell'elenco (i numeri più bassi appaiono per primi)
- **Config** — impostazioni specifiche del provider (vedi di seguito)

4. Clicca su **Salva**

## Opzioni di configurazione del feed

Il campo **Config** accetta un oggetto JSON con le seguenti opzioni:

| Opzione | Valori | Descrizione |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Frequenza con cui il feed viene rigenerato automaticamente |
| `format_preference` | `xml`, `csv`, `json` | Formato di output (la maggior parte delle piattaforme preferisce XML) |
| `include_variants` | `true` / `false` | Includi le varianti del prodotto come voci di feed separate |
| `target_country` | Codice del paese ad es. `"US"` | Paese di destinazione del feed |
| `content_language` | Codice della lingua ad es. `"en"` | Lingua dei dati del prodotto |

#### Esempio di configurazione per un feed XML giornaliero mirato agli Stati Uniti:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtrare quali prodotti appaiono nel feed

Puoi controllare esattamente quali prodotti vengono inclusi aggiungendo una sezione `product_filter` alla configurazione:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Opzione di filtro | Descrizione |
|---------------|-------------|
| `status` | Includi solo prodotti con questi stati. Usa `["published"]` per includere solo prodotti attivi. |
| `in_stock_only` | Imposta su `true` per escludere i prodotti fuori stock |
| `categories` | Limita a specifici ID di categoria |
| `brands` | Limita a specifici ID di marca |

Puoi anche escludere prodotti specifici utilizzando i loro ID con `exclude_products`:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Monitoraggio dello stato di sincronizzazione

L'elenco degli account provider di feed mostra lo stato di sincronizzazione di ciascun feed collegato a colpo d'occhio:

- **PENDING** — nessuna sincronizzazione è stata eseguita ancora, o il feed è in attesa di essere generato
- **SYNCING** — una sincronizzazione è in corso
- **SUCCESS** — l'ultima sincronizzazione è completata senza errori
- **ERROR** — l'ultima sincronizzazione è fallita; il messaggio di errore viene visualizzato sulla pagina dei dettagli dell'account

L'elenco mostra anche il numero di prodotti nel feed corrente e quando è stata eseguita l'ultima sincronizzazione.

## Visualizzazione dei feed generati

Vai a **Marketing > Feed dei prodotti** per visualizzare i file dei feed generati. Ogni voce rappresenta una snapshot di un feed generato e mostra:

- **Provider Account** — a cui appartiene questo feed
- **Format** — XML, CSV o JSON
- **Product Count** — numero di prodotti inclusi
- **Size** — dimensione del file del feed generato
- **Generated At** — quando è stato creato
- **Expires At** — quando questa versione memorizzata scade
- **Status** — se il feed è ancora valido o è scaduto
- **Download Count** — quante volte è stato scaricato questo feed

I feed sono in sola lettura nell'amministrazione — vengono generati automaticamente dal processo di sincronizzazione.

## Visualizzazione del log della sincronizzazione

Passa a **Marketing > Feed Sync Logs** per visualizzare una cronologia completa di ogni tentativo di sincronizzazione per tutti i tuoi account feed. Ogni voce del log registra:

- L'account provider che è stato sincronizzato
- Il tipo di sincronizzazione (Completo, Incrementale, Manuale o Programmato)
- Stato (Successo, Parziale, Fallito, ecc.)
- Prodotti sincronizzati, falliti e saltati
- Durata della sincronizzazione
- Qualsiasi messaggio di errore

Il pannello del log di sincronizzazione in alto nella pagina mostra statistiche generali: totale sincronizzazioni, tasso di successo e durata media della sincronizzazione. Usa i filtri **Account** e **Sync Type** per restringere la visualizzazione a un feed specifico.

### Cosa fare quando una sincronizzazione fallisce

1. Passa a **Marketing > Feed Sync Logs** e trova l'entry fallita
2. Fai clic sulla voce del log per visualizzare il completo **Messaggio di errore** e **Dettagli dell'errore**
3. Le cause comuni includono:
   - Campi obbligatori dei prodotti mancanti (titolo, prezzo, immagine)
   - Credenziali API non valide o scadute — reinstalla il componente provider per aggiornare le credenziali
   - Errori di rete durante la connessione all'API del provider
4. Una volta risolto il problema, la prossima sincronizzazione programmata verrà eseguita automaticamente, oppure puoi attivare una sincronizzazione manuale dall'account provider

## Consigli

- Imposta `"sync_interval": "daily"` per la maggior parte dei casi d'uso — Google e Facebook non richiedono aggiornamenti più frequenti a meno che non tu abbia una forte volatilità dei prezzi
- Includi sempre `"in_stock_only": true` nei tuoi filtri dei prodotti per evitare di pubblicare prodotti che i clienti non possono acquistare
- Usa un nome descrittivo per l'account che includa la piattaforma e il mercato di destinazione (es. `Google Shopping — UK`) per rendere facile la gestione di diversi feed
- Il conteggio **Prodotti nel feed** nell'account provider ti dice immediatamente se un numero inferiore di prodotti rispetto al previsto è incluso — verifica le impostazioni del filtro dei prodotti se il conteggio sembra basso
- Contrassegna un account come **Feed Primario** per ogni tipo di provider; alcuni strumenti di reporting lo utilizzano per identificare il tuo feed principale
- Controlla il log della sincronizzazione dopo qualsiasi modifica di massa al tuo catalogo prodotti per confermare che i dati aggiornati siano stati correttamente acquisiti