---
title: Comprendere le Impostazioni di Ricerca
---

L'interfaccia SearchSettings controlla tutti i comportamenti di ricerca globali nel tuo negozio Spwig. Questa singola pagina di configurazione utilizza un'interfaccia a 8 schede per organizzare le opzioni di ricerca, dalle semplici abilitazioni alle avanzate regolazioni delle prestazioni. I cambiamenti effettuati qui si applicano a tutti i motori di ricerca, salvo che siano sovrascritti a livello di motore.

Questo documento spiega ogni scheda, spiegando cosa fa ogni impostazione e quando modificarla.

![Scheda Generale delle Impostazioni di Ricerca](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## L'Interfaccia a 8 Schede

SearchSettings è un modello singleton - esiste un'unica registrazione di configurazione (pk=1) per tutto il tuo negozio. L'interfaccia è divisa in otto schede:

| Scheda | Scopo |
|--------|-------|
| **Generale** | Abilitare/disabilitare la ricerca, impostare parametri di base |
| **Autocomplete** | Configurare il comportamento del menu a discesa di ricerca predittiva |
| **Tipi di Contenuti** | Scegliere quali tipi di contenuti sono ricercabili |
| **Indicizzazione Approfondita** | Controllare quali dati dei prodotti vengono indicizzati (impatto sulle prestazioni) |
| **Corrispondenza Approssimativa** | Tolleranza agli errori di digitazione e soglie di similarità |
| **Pesi** | Moltiplicatori di rilevanza per il ranking dei risultati |
| **Caching** | Bilanciamento tra tempo di risposta e freschezza dei dati |
| **Analisi** | Tracciamento delle query e impostazioni sulla privacy |

Ogni scheda si concentra su un aspetto specifico della configurazione della ricerca.

## Scheda Generale

La scheda Generale contiene le impostazioni principali che influenzano tutte le ricerche:

**Abilita Ricerca** - Interruttore principale per il sistema di ricerca. Quando disabilitato, tutte le funzionalità di ricerca sono inattive in tutto il tuo negozio, incluso l'autocomplete e la pagina dei risultati della ricerca.

**Lunghezza Minima della Query** - Default: 2 caratteri. Le ricerche più brevi di questo valore vengono rifiutate. Impostare questo valore a 1 permette ricerche con un singolo carattere (es. "A") ma aumenta il carico del server.

**Risultati per Pagina** - Default: 20 elementi. Controlla la paginazione per le pagine dei risultati della ricerca. Valori più alti (30-50) riducono i clic di paginazione ma aumentano il tempo di caricamento della pagina.

## Scheda Tipi di Contenuti

![Impostazioni dei Tipi di Contenuti](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Attiva/Disattiva i tipi di contenuti che appaiono nei risultati della ricerca:

- **Prodotti** - Prodotti fisici, digitali e di abbonamento
- **Categorie** - Categorie di prodotti
- **Marchi** - Marchi di prodotti
- **Post del Blog** - Contenuti del blog

**Nota sulle Prestazioni**: Meno tipi di contenuti = ricerche più veloci. Ogni tipo abilitato aggiunge ulteriori query al database. Se non hai un blog, disattiva i Post del Blog per migliorare i tempi di risposta.

## Scheda Indicizzazione Approfondita

⚠️ **AVVERTENZA SULLE PRESTAZIONI** - Queste impostazioni hanno un impatto significativo sulle prestazioni.

![Impostazioni di Indicizzazione Approfondita](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

L'indicizzazione approfondita controlla quali dati relativi ai prodotti vengono inclusi nelle ricerche:

**Indicizza SKU** - Default: ATTIVO, Impatto basso. Includere SKU di prodotti e varianti nella ricerca. Essenziale per i negozi B2B dove i clienti cercano per codici prodotto.

**Indicizza Attributi** - Default: ATTIVO, Impatto medio. Includere attributi dei prodotti (colore, dimensione, materiale) nella ricerca. Aggiunge un JOIN alla tabella degli attributi. Importante per i prodotti di moda e configurabili.

**Indicizza Campi Personalizzati** - Default: ATTIVO, Impatto medio. Includere campi personalizzati definiti dal commerciante nei risultati della ricerca. Richiede l'accesso ai campi JSONField.

**Indicizza Recensioni** - Default: ATTIVO, Impatto medio-alto. Includere titoli e commenti delle recensioni approvate nella ricerca. Aggiunge un JOIN alla tabella delle recensioni e introduce un sovraccarico di ricerca testuale. Utile per cataloghi con molte recensioni.

**Indicizza Documenti** - Default: DISATTIVO, **IMPATTO MOLTO ALTO** ⚠️

L'indicizzazione dei documenti estrae il testo da file PDF, DOCX e XLSX allegati ai prodotti digitali. Questa funzione:

- Richiede un'indicizzazione iniziale molto costosa
- Aggiunge un sovraccarico significativo alle query su ogni ricerca
- Può causare tempi di attesa su file di grandi dimensioni
- **Deve essere abilitata SOLO per i negozi di prodotti digitali con documenti ricercabili**
- **Mai abilitare casualmente** - testa attentamente l'impatto sulle prestazioni

## Scheda Corrispondenza Approssimativa

![Impostazioni di Corrispondenza Approssimativa](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

La corrispondenza approssimativa utilizza la distanza di Levenshtein per gestire gli errori di digitazione:

**Abilita Corrispondenza Approssimativa** - Permette alle ricerche di corrispondere a termini simili (es. "laptop" corrisponde a "labtop")

**Soglia di Similarità** - Default: 0,80 (80% di similarità). Intervallo: 0,0-1,0. Valori più alti richiedono corrispondenze più precise e funzionano più velocemente. Valori più bassi catturano più errori di digitazione ma possono restituire risultati irrilevanti.

**Massima Distanza di Modifica** - Default: 2 cambiamenti di caratteri. Numero massimo di inserimenti, cancellazioni o sostituzioni consentiti. Valori più bassi (1) migliorano le prestazioni ma catturano meno errori di digitazione.

## Scheda Pesi

I pesi controllano il punteggio di rilevanza - come vengono ordinati i risultati. La scheda Pesi mostra i moltiplicatori predefiniti per ogni campo ricercabile:

- weight_name: 1,50 (i nomi dei prodotti sono i più importanti)
- weight_sku: 1,20
- weight_description: 0,80
- weight_categories: 0,80
- weight_attributes: 0,70
- weight_brands: 0,70
- weight_blog_posts: 0,60
- weight_reviews: 0,50

Questi valori predefiniti funzionano bene per la maggior parte dei negozi e-commerce. Per informazioni dettagliate su come modificare i pesi e comprendere il loro impatto, vedi l'argomento [Pesi di Rilevanza e Indicizzazione Approfondita](/en/admin/help/relevance-weights-deep-indexing/).

## Scheda Caching

![Impostazioni di Caching](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Il caching migliora drasticamente le prestazioni della ricerca memorizzando i risultati recenti:

**TTL del Caching Autocomplete** - Default: 60 secondi. Per quanto tempo i risultati dell'autocomplete vengono memorizzati. Un TTL più breve (30-45s) = risultati più recenti ma più query al database. Un TTL più lungo (90-120s) = risultati più veloci ma potenzialmente obsoleti.

**TTL del Caching Risultati** - Default: 300 secondi (5 minuti). Durata del cache della pagina completa dei risultati della ricerca. Un TTL più lungo migliora significativamente le prestazioni ma ritarda la visibilità dei nuovi prodotti.

**Compromessi**: Il caching è l'ottimizzazione più efficace per le prestazioni. Se le ricerche sono lente, aumenta questi valori prima di disabilitare funzionalità.

## Scheda Analisi

![Impostazioni di Analisi](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Traccia le Query di Ricerca** - Abilita il pannello di controllo per l'analisi delle ricerche. Registra il testo della query, il numero di risultati, il tempo di risposta e il timestamp.

**Traccia le Informazioni Utente** - Associa le ricerche agli utenti autenticati. Disabilita per la conformità alla privacy (GDPR, CCPA).

**Traccia le Informazioni della Sessione** - Utilizza gli ID di sessione per tracciare le ricerche degli utenti anonimi. Utile per identificare i pattern di ricerca senza dati personali.

## Modello Singleton

SearchSettings utilizza un modello singleton - esiste un'unica registrazione di impostazioni nel tuo database (pk=1). Quando navighi verso Impostazioni di Ricerca nell'amministrazione, stai sempre modificando la stessa registrazione.

Non esiste un'opzione "Aggiungi" o "Elimina" - solo "Modifica". Tutti i motori di ricerca ereditano queste impostazioni a meno che non specificano sovrascritture per motore (raro).

## Consigli

- **Mantieni i valori predefiniti a meno che non tu abbia un bisogno specifico** - Le impostazioni predefinite sono ottimizzate per i negozi e-commerce tipici
- **Mai abilitare l'indicizzazione dei documenti casualmente** - Solo per i negozi di prodotti digitali con documenti ricercabili, e testa prima l'impatto sulle prestazioni
- **Monitora i tempi di risposta nell'analisi** - Obiettivo: <200ms per l'autocomplete, <500ms per la ricerca completa
- **Aumenta il TTL del caching se le prestazioni sono lente** - Il caching è la vittoria più facile sulle prestazioni
- **Rivedi le query senza risultati settimanalmente** - Reveal prodotti mancanti o sinonimi necessari
- **Disattiva i tipi di contenuti non utilizzati** - Se non hai un blog, disattiva i Post del Blog per accelerare le ricerche

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.