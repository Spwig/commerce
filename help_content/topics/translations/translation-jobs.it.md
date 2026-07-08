---
title: Lavori di traduzione
---

I lavori di traduzione automatizzano la traduzione di grandi quantità di contenuti. Invece di tradurre manualmente i prodotti uno per uno, crea un lavoro che traduca l'intero catalogo o sottocategorie specifiche in background. I lavori vengono eseguiti in modo asincrono, quindi puoi continuare a lavorare mentre centinaia o migliaia di campi vengono tradotti automaticamente.

Utilizza i lavori di traduzione quando attivi nuove lingue, importi nuovi prodotti o recuperi contenuti non tradotti.

## Cosa sono i lavori di traduzione?

Un lavoro di traduzione è un compito in background che:

1. **Scansiona il contenuto** per i campi traducibili (prodotti, pagine, post di blog, ecc.)
2. **Identifica i campi non tradotti o obsoleti** in base all'ambito del lavoro
3. **Invia i campi al motore di traduzione** (modello AI locale o fornitore esterno)
4. **Salva le traduzioni** nel tuo contenuto
5. **Riporta il completamento** con statistiche sui campi tradotti

I lavori vengono eseguiti tramite la coda di compiti Celery, quindi non bloccano l'interfaccia di amministrazione.

## Quando utilizzare i lavori di traduzione

**Lancio di una nuova lingua**:
- Attiva il tedesco come nuova lingua
- Crea lavoro: traduci tutti i prodotti dall'inglese al tedesco
- Risultato: l'intero catalogo disponibile in tedesco entro minuti/ore (a seconda della dimensione)

**Import di nuovi prodotti**:
- Importa 500 nuovi prodotti in inglese
- Crea lavoro: traduci i nuovi prodotti in tutte le lingue attive
- Risultato: l'inventario nuovo immediatamente disponibile in tutti i mercati

**Recupero di lacune**:
- Il rapporto di copertura mostra che i prodotti sono solo il 60% tradotti in francese
- Crea lavoro: traduci solo i campi mancanti dei prodotti in francese
- Risultato: la copertura in francese aumenta fino a ~100%

**Aggiornamento di traduzioni obsolete**:
- Il modello di traduzione è migliorato o è disponibile un nuovo fornitore
- Crea lavoro: ristraduci tutti i prodotti in spagnolo
- Risultato: traduzioni in spagnolo di alta qualità in tutto il catalogo

## Creare un lavoro di traduzione

Naviga in **Impostazioni > Lavori di traduzione** e fai clic su **+ Crea lavoro**.

### Configurazione del lavoro

**Nome del lavoro** - Etichetta descrittiva (es. "Traduci i prodotti in tedesco", "Nuovi post di blog - tutte le lingue")

**Tipo di contenuto** - Cosa tradurre:
- Prodotti
- Categorie di prodotti
- Pagine
- Post di blog
- Metadati SEO
- Modelli di email
- Tutti i tipi di contenuti

**Lingua di origine** - La lingua da cui si sta traducendo (di solito la lingua predefinita)

**Lingua/e di destinazione** - Una o più lingue in cui tradurre (seleziona più lingue per la traduzione parallela)

**Ambito** - Quale sottocategoria di contenuti:
- **Tutti gli elementi** - Traduci tutto, indipendentemente dalle traduzioni esistenti
- **Solo non tradotti** - Salta i campi che già hanno traduzioni
- **Creati/modificati da una data** - Solo contenuti nuovi o recentemente modificati
- **Elementi specifici** - Seleziona prodotti/pagine individuali (filtraggio avanzato)

**Motore di traduzione** - Quale servizio utilizzare:
- Modello AI locale (predefinito, nessun costo API)
- Fornitore esterno specifico (DeepL, Google, Azure, AWS)
- Auto-seleziona (usa la preferenza configurata)

**Blocca traduzioni** - Se bloccare i campi tradotti contro l'overwriting automatico futuro (utile per traduzioni revisionate)

### Opzioni avanzate

**Salta campi bloccati** - Se abilitato, rispetta le traduzioni bloccate esistenti (consigliato)

**Sovrascrivi esistenti** - Ristraduci anche se esistono traduzioni (usa per miglioramenti di qualità)

**Filtri dei campi** - Traduci solo campi specifici (es. nomi e descrizioni dei prodotti, salta gli attributi)

**Dimensione del lotto** - Quanti elementi elaborare alla volta (predefinito: 50, aumenta per un elaborazione più rapida se il server lo permette)

**Priorità** - I lavori ad alta priorità vengono eseguiti prima di quelli a priorità normale (usa con moderazione)

## Ciclo di vita e stato del lavoro

I lavori passano attraverso questi stati:

**In coda** - Lavoro creato, in attesa che un worker lo prenda

**In elaborazione** - Worker che traduce attivamente il contenuto

**Completato** - Tutte le traduzioni sono finite con successo

**Fallito** - Il lavoro ha incontrato errori (controlla il registro degli errori)

**Annullato** - Fermato manualmente dall'amministratore

**Pausa** - Sospeso temporaneamente (può essere ripreso)

## Monitoraggio del progresso del lavoro

La pagina dei dettagli del lavoro mostra:

**Barra di progresso** - Percentuale completata

**Statistiche**:
- Totale elementi da tradurre
- Elementi completati
- Elementi rimanenti
- Tempo stimato rimanente

**Registro in tempo reale** - Flusso di attività di traduzione (utile per risolvere problemi)

**Conteggio errori** - Quanti campi non sono riusciti a tradurre (con motivi)

## Risultati e statistiche del lavoro

Quando un lavoro è completato, la pagina dei risultati mostra:

**Riepilogo**:
- Totale campi elaborati
- Tradotti con successo
- Traduzioni fallite
- Saltati (già tradotti, bloccati o esclusi dai filtri)

**Analisi per elemento**:
- Quali prodotti/pagine sono state tradotte
- Quanti campi per elemento
- Qualsiasi errore riscontrato

**Metriche di prestazioni**:
- Tempo totale trascorso
- Media delle traduzioni al secondo
- Motore di traduzione utilizzato

## Gestione delle traduzioni fallite

Se alcune traduzioni falliscono:

**Rivedi il registro degli errori** - Identifica quali campi sono falliti e il motivo

**Causa comune di fallimento**:
- Limite di velocità API raggiunto (fornitore esterno)
- Timeout del motore di traduzione (testo molto lungo)
- Formato campo non valido (errore di analisi JSON)
- Modello non supporta la coppia di lingue

**Opzioni di riprovare**:
- Risolvi il problema sottostante
- Crea un nuovo lavoro solo per gli elementi falliti
- Usa un diverso motore di traduzione

## Annullare e sospendere i lavori

**Annulla** - Ferma immediatamente il lavoro, elimina eventuali traduzioni in corso (le traduzioni completate vengono salvate)

**Pausa** - Ferma temporaneamente il lavoro, puoi riprendere in un secondo momento da dove era rimasto

**Riprendi** - Continua un lavoro sospeso

Utilizza pausa/riprendi quando devi liberare temporaneamente le risorse del server.

## Strategie per lavori in batch

**Strategia 1: Lingua per lingua**:
- Crea lavori separati per ogni lingua di destinazione
- Più facile monitorare il progresso per lingua
- Puoi priorizzare le lingue importanti
- Distribuisce il carico nel tempo

**Strategia 2: Tutte insieme**:
- Un singolo lavoro che traduce in tutte le lingue attive
- Completamento più rapido complessivo
- Maggiore carico sul server durante l'elaborazione
- Gestione più semplice del lavoro

**Strategia 3: Tipo di contenuto per tipo di contenuto**:
- Traduci prima i prodotti (priorità più alta)
- Poi categorie, pagine, post di blog
- Permette un rilascio progressivo
- Più facile testare e verificare le traduzioni

Scegli in base alla capacità del server, all'urgenza e alla dimensione del catalogo.

## Programmazione dei lavori

Programma lavori ricorrenti per gestire automaticamente il nuovo contenuto:

**Lavori giornalieri** - Traduci qualsiasi prodotto creato/modificato nell'ultimo 24 ore

**Lavori settimanali** - Recupera eventuali lacune di traduzione settimanalmente

**Dopo l'import** - Attiva automaticamente il lavoro dopo l'import di massa di prodotti

**All'attivazione della lingua** - Crea automaticamente un lavoro quando attivi una nuova lingua

I lavori programmati mantengono le traduzioni aggiornate senza intervento manuale.

## Considerazioni sulle prestazioni

**Modello AI locale**:
- ~100-500 traduzioni al secondo (dipende dal server)
- Intensivo in termini di CPU durante l'elaborazione
- Nessun limite di velocità API
- Gratuito (nessun costo per traduzione)

**Fornitori esterni**:
- I limiti di velocità variano (DeepL: 500k caratteri/mese sulla versione gratuita)
- Latenza API aggiunge overhead
- Maggiore qualità ma a costo
- Limiti di richieste concorrenti

**Lavori di grandi dimensioni** (>10.000 campi):
- Esegui durante le ore di bassa intensità
- Monitora le risorse del server
- Considera la suddivisione in lotti più piccoli
- Testa prima con un subset

## Consigli

- **Inizia piccolo** - Testa i lavori su un subset (es. 10 prodotti) prima di eseguire la traduzione del catalogo completo
- **Utilizza l'ambito "Solo non tradotti"** - Più veloce e evita di ristradurre contenuti già buoni
- **Monitora attentamente il primo lavoro** - Osserva errori o problemi di qualità prima di lanciare lavori più grandi
- **Programma i lavori durante i periodi di bassa intensità** - La traduzione è intensiva in termini di CPU/API
- **Blocca le traduzioni revisionate** - Impedisce ai lavori di massa di sovrascrivere le tue modifiche manuali
- **Mantieni i lavori focalizzati** - I lavori più piccoli e mirati sono più facili da risolvere rispetto ai lavori massicci "traduci tutto"
- **Rivedi i campioni dopo il completamento** - Controlla traduzioni casuali per la qualità prima di considerare il lavoro completato
- **Esporta/backup prima di lavori importanti** - In caso di bisogno di annullare modifiche di massa

Ricorda: preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.