---
title: Analisi dei visitatori
---

L'Analisi dei visitatori ti dà un'immagine chiara su come i clienti si muovono nel tuo negozio. Puoi vedere quali pagine attraggono più visite, come si sviluppa il traffico complessivo nel tempo, quali dispositivi i tuoi clienti utilizzano e come si confrontano i visitatori nuovi rispetto a quelli che tornano — tutto senza dover utilizzare strumenti esterni di analisi.

## Panoramica delle schermate di analisi

Il tuo negozio traccia automaticamente l'attività dei visitatori una volta che il sistema GeoIP è attivo. I dati sono organizzati in tre viste, ciascuna delle quali ti fornisce un livello diverso di dettaglio.

### Riepilogo del traffico giornaliero

Naviga verso **Clienti > Statistiche del traffico giornaliero** per visualizzare il traffico complessivo del tuo negozio per ogni giorno. Ogni riga rappresenta un singolo giorno del calendario e mostra:

| Colonna | Cosa ti dice |
|--------|-------------------|
| **Data** | Il giorno in cui è stato registrato il traffico |
| **Totale visualizzazioni** | Tutte le visualizzazioni delle pagine, incluse quelle dei bot |
| **Visitatori unici** | Visitatori distinti (per sessione) |
| **Visualizzazioni dei bot** | Visualizzazioni provenienti da crawler e strumenti automatizzati |
| **Nuovi visitatori** | Sessioni senza storia precedente |
| **Visitatori tornati** | Sessioni da visitatori già visti |
| **Visualizzazioni da desktop** | Visualizzazioni da browser desktop |
| **Visualizzazioni da mobile** | Visualizzazioni da dispositivi mobili |
| **Visualizzazioni da tablet** | Visualizzazioni da dispositivi tablet |

Utilizza la navigazione gerarchica delle date in alto nell'elenco per saltare rapidamente a un mese o un anno specifico. I totali vengono aggiornati una volta al giorno tramite un processo in background automatizzato, quindi i dati per il giorno corrente appariranno il mattino successivo.

### Statistiche per pagina

Naviga verso **Clienti > Statistiche delle pagine giornaliere** per visualizzare il traffico suddiviso per singola pagina. Ogni riga mostra un percorso URL su un giorno, quindi puoi confrontare le prestazioni di pagine specifiche nel tempo.

| Colonna | Cosa ti dice |
|--------|-------------------|
| **Data** | Il giorno a cui si riferiscono queste statistiche |
| **Percorso URL** | Il percorso della pagina normalizzato (es. `/products/blue-widget`) |
| **Visualizzazioni** | Totale visualizzazioni per quella pagina in quel giorno |
| **Visitatori unici** | Visitatori distinti che hanno visualizzato quella pagina |
| **Visualizzazioni dei bot** | Visualizzazioni provenienti da bot su quella pagina |
| **Entrate** | Quante sessioni sono iniziate su questa pagina (era la loro pagina di atterraggio) |

Utilizza la casella di ricerca **Percorso URL** per trovare le statistiche per una pagina specifica. Ad esempio, cerca `/products/` per visualizzare tutto il traffico delle pagine dei prodotti, o cerca un slug specifico di un prodotto per concentrarti su un singolo elemento.

### Eventi di visualizzazione delle singole pagine

Naviga verso **Clienti > Visualizzazioni delle pagine** per ottenere un registro grezzo di ogni navigazione delle pagine tracciata. Questo è un registro di sola lettura — non puoi aggiungere o modificare gli elementi. Utilizzalo per investigare sessioni specifiche o per verificare che il tracciamento venga registrato correttamente.

Ogni record mostra:
- **Percorso URL** — la pagina visitata
- **Sessione** — un identificativo breve per la sessione del visitatore
- **Fonte** — se la visita proviene dall'interfaccia frontend headless o dal negozio standard
- **È un bot** — se il visitatore è stato identificato come traffico automatizzato
- **È una pagina di entrata** — se questa è stata la prima pagina della loro sessione
- **Timestamp** — l'orario esatto della visita

Puoi filtrare per **È un bot**, **Fonte** e **È una pagina di entrata** utilizzando i filtri laterali, e navigare per data utilizzando la gerarchia delle date in alto.

## Lettura delle tendenze del traffico

Il riepilogo del traffico giornaliero è lo strumento migliore per individuare tendenze. Cerca schemi come:

- **Picchi di traffico** dopo aver lanciato una promozione o inviato un'email di marketing
- **Crescita graduale** settimanale e mensile man mano che il tuo negozio guadagna visibilità organica
- **Pattern di fine settimana vs. giorni feriali** per comprendere quando i tuoi clienti sono più attivi
- **Suddivisione tra mobile e desktop** per decidere se prioritizzare modifiche al design ottimizzato per dispositivi mobili

Le colonne **Nuovi visitatori** e **Visitatori tornati** insieme ti dicono quanto bene stai mantenendo i clienti. Un negozio sano vede generalmente una miscela di entrambi — una proporzione elevata di nuovi visitatori suggerisce un'acquisizione forte, mentre una quota più elevata di visitatori tornati suggerisce che la fedeltà dei clienti sta crescendo.

La vista delle statistiche per pagina, ordinata per visualizzazioni in ordine decrescente (il valore predefinito), mostra immediatamente quali pagine generano il maggior traffico in un determinato giorno.

Cerca di:

- **Pagine con alto ingresso e basso numero di visualizzazioni** — pagine che attraggono visitatori da ricerca o annunci ma potrebbero non mantenere l'attenzione
- **Pagine con alto numero di visualizzazioni e molti visitatori unici** — pagine popolari che vale la pena mantenere aggiornate
- **Pagine prodotto con un aumento del numero di visualizzazioni** — prodotti che potrebbero guadagnare visibilità nei risultati di ricerca

### Esempio: trovare il traffico di un prodotto

Per controllare quanto traffico ha ricevuto il tuo prodotto più venduto la scorsa settimana:

1. Vai a **Customers > Daily Page Stats**
2. Usa la gerarchia delle date per selezionare la settimana rilevante
3. Nella casella di ricerca, inserisci lo slug dell'URL del prodotto (es. `/blue-widget`)
4. Esamina le colonne **Views**, **Unique Visitors** e **Entries** per i giorni visualizzati

## Dati sulla posizione dei visitatori

Vai a **Customers > Visitor Locations** per visualizzare a livello di sessione dove si trovano i tuoi visitatori. Ogni record rappresenta una sessione di un visitatore e include:

- Paese e città (risolti automaticamente dal sistema GeoIP)
- Tipo di dispositivo (desktop, mobile, tablet)
- Preferenze di valuta e lingua selezionate dal visitatore
- Attribuzione della campagna UTM (fonte, mezzo, nome della campagna)
- Indicatori per traffico da bot e traffico amministrativo

Puoi filtrare i visitatori per paese, tipo di dispositivo, fonte UTM e se erano bot o personale amministrativo. Usa il filtro **Is Bot** impostato su false per concentrarti sul traffico reale dei clienti, e il filtro **Is Admin Traffic** per escludere le tue sessioni di test dall'analisi.

## Consigli

- Le visualizzazioni dei bot vengono registrate separatamente ed escluse automaticamente dal conteggio dei visitatori unici — i tuoi dati sul traffico riflettono l'attività reale dei clienti
- La colonna **Entries** nelle statistiche per pagina ti dice quali pagine agiscono come porta d'ingresso del tuo negozio da ricerca e annunci; ottimizzare quelle pagine ha l'impatto maggiore
- Filtra le posizioni dei visitatori per **UTM Source** per misurare quanto traffico un canale di marketing specifico (es. una newsletter via email o un annuncio di Google) sta realmente inviando
- Le statistiche giornaliere vengono aggregate di notte — se devi controllare il traffico dello stesso giorno, usa direttamente il registro delle visualizzazioni delle pagine
- La suddivisione per dispositivi nel riepilogo giornaliero ti aiuta a priorizzare i lavori di progettazione; se più della metà delle tue visite proviene da dispositivi mobili, assicurati che le tue pagine prodotto e il checkout siano ottimizzati per schermi piccoli