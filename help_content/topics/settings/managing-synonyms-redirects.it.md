---
title: Gestione di sinonimi e reindirizzamenti
---

I sinonimi e i reindirizzamenti rendono la ricerca più intelligente gestendo termini equivalenti e instradando query specifiche a pagine mirate. I sinonimi espandono le ricerche per includere termini correlati ("laptop" trova anche "notebook"), mentre i reindirizzamenti inviano query come "sale" direttamente alla tua pagina delle vendite. Questa guida spiega come creare e gestire entrambe le funzionalità per migliorare la rilevanza della ricerca e l'esperienza del cliente.

Utilizza i sinonimi per l'equivalenza dei termini e i reindirizzamenti per scorciatoie di navigazione.

![Elenco dei sinonimi](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Comprendere i sinonimi

I sinonimi dicono al sistema di ricerca che certi termini devono essere trattati come equivalenti. Quando un cliente cerca un termine, il sistema include automaticamente i risultati che corrispondono ai termini sinonimi.

**Esempio**: Crea una mappatura dei sinonimi "laptop" → "notebook", "portable computer". Ora, quando qualcuno cerca "laptop", ottiene anche i risultati per i prodotti che contengono "notebook" o "portable computer" nei loro nomi o descrizioni.

I sinonimi sono particolarmente utili per:
- Inglese britannico vs. americano (jumper/sweater, trainers/sneakers)
- Termini di marca vs. termini generici (tissues/Kleenex)
- Errori di ortografia comuni (accommodare/accommodare)
- Gergo specifico del settore vs. linguaggio comune (CPU/processor)

## Creare sinonimi

Naviga verso **Search > Synonyms** e fai clic su **+ Add Synonym**.

![Form per l'aggiunta di un sinonimo](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - Il termine originale di ricerca che attiva l'espansione dei sinonimi

**Sinonimi** - Array JSON di termini equivalenti, ad esempio `['sweater', 'pullover', 'jumper']`

**Bidirezionale** - Predefinito: selezionato. Quando abilitato, le relazioni dei sinonimi funzionano in entrambe le direzioni:
- Ricerca "laptop" trova prodotti "notebook"
- Ricerca "notebook" trova prodotti "laptop"

Deseleziona per mappature unidirezionali (vedi di seguito).

**Lingua** - Opzionale. Limita questo sinonimo alle ricerche in una lingua specifica. Lascia vuoto per applicarlo a tutte le lingue.

**Motore** - Opzionale. Limita questo sinonimo a un motore di ricerca specifico. Lascia vuoto per applicarlo globalmente.

**Attivo** - Se questo sinonimo è attualmente in uso. Deseleziona per disattivarlo temporaneamente senza eliminarlo.

## Esempi bidirezionali

La maggior parte dei sinonimi dovrebbe essere bidirezionale - veri equivalenti che funzionano in entrambe le direzioni:

| Term | Sinonimi | Caso d'uso |
|------|----------|----------|
| laptop | notebook, portable computer | Inglese britannico/americano + termini generici |
| sofa | couch, settee | Variazioni regionali |
| trainers | sneakers, running shoes | Inglese UK/US |
| mobile | cell phone, cellular | Variazioni internazionali |

Con la funzione bidirezionale abilitata, tutti questi termini trovano gli stessi prodotti indipendentemente dal termine utilizzato dal cliente.

## Esempi unidirezionali

Deseleziona "Bidirezionale" per relazioni unidirezionali:

**Casi d'uso comuni**:
- **Errori di ortografia**: Term: "acco
modate" → Sinonimi: `['accommodate']` (unidirezionale in modo che la forma corretta non trovi l'errore)
- **Specifico → Generico**: Term: "MacBook" → Sinonimi: `['laptop']` (i MacBook sono laptop, ma non tutti i laptop sono MacBook)
- **Abbreviazioni**: Term: "CPU" → Sinonimi: `['processor']` (CPU trova prodotti processor, ma le ricerche processor non dovrebbero sempre includere CPU)

## Sinonimi specifici per la lingua

Utilizza il campo Lingua per creare sinonimi adatti alla regione:

**Esempio**: Negozio in inglese britannico
- Term: "jumper", Sinonimi: `['sweater', 'pullover']`, Lingua: Inglese (UK)
- Term: "trainers", Sinonimi: `['sneakers']`, Lingua: Inglese (UK)

**Esempio**: Negozio multilingua
- Term: "ordinateur portable", Sinonimi: `['laptop', 'notebook']`, Lingua: Francese
- Term: "zapatos", Sinonimi: `['shoes']`, Lingua: Spagnolo

I sinonimi specifici per la lingua si applicano solo quando un cliente naviga in quella lingua.

## Sinonimi specifici per il motore

La maggior parte dei sinonimi dovrebbe applicarsi globalmente (lascia il campo Motore vuoto). Utilizza i sinonimi specifici per il motore solo quando diversi contesti di ricerca richiedono mappature di termini diversi:

**Esempio**: Hai motore separati per "shop" e "blog"
- Sinonimo per blog: Term: "tutorial" → Sinonimi: `['guide', 'how-to']`, Motore: blog
- Questo sinonimo si applica solo alle ricerche del blog, non alle ricerche dei prodotti

## Comprendere i reindirizzamenti

I reindirizzamenti di ricerca inviano query specifiche direttamente a pagine designate, bypassando i risultati di ricerca normali. Utilizza i reindirizzamenti quando sai esattamente dove un cliente dovrebbe andare.

**Esempio**: Crea un reindirizzamento per "sale" → "/products/sale/". Ora, quando qualcuno cerca "sale", salta i risultati di ricerca e atterra direttamente sulla tua pagina delle vendite.

I reindirizzamenti sono perfetti per:
- Scorciatoie di navigazione comuni ("returns" → pagina delle politiche di restituzione)
- Promozioni stagionali ("summer sale" → collezione estiva)
- Categorie popolari ("laptops" → pagina della categoria laptop)
- Pagine delle politiche ("shipping" → informazioni sulla spedizione)

![Elenco dei reindirizzamenti](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Tipi di corrispondenza

I reindirizzamenti supportano quattro tipi di corrispondenza che controllano quanto rigorosamente la query di ricerca deve corrispondere:

**Esatto** - Corrispondenza esatta senza distinzione di maiuscole. La query deve corrispondere esattamente al termine (ignorando le maiuscole).
- Term: "sale"
- Corrisponde: "sale", "SALE", "Sale"
- Non corrisponde: "summer sale", "on sale"

**Contiene** - La query contiene il termine in qualsiasi posizione.
- Term: "sizing"
- Corrisponde: "sizing guide", "help with sizing", "what sizing"
- Non corrisponde: "size chart" (parola diversa)

**Inizia con** - La query inizia con il termine.
- Term: "return"
- Corrisponde: "returns", "return policy", "returning items"
- Non corrisponde: "how to return" (non inizia con il termine)

**Regex** - Corrispondenza di pattern utilizzando espressioni regolari. **⚠️ Attenzione alle prestazioni** - i pattern regex complessi rallentano le ricerche. Utilizzali solo quando necessario.
- Pattern: `^(laptop|notebook)s?$`
- Corrisponde: "laptop", "laptops", "notebook", "notebooks"
- Utilizza solo se altri tipi di corrispondenza non funzionano

## Creare reindirizzamenti

Naviga verso **Search > Redirects** e fai clic su **+ Add Redirect**.

![Form per l'aggiunta di un reindirizzamento](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - La query di ricerca da corrispondere

**Tipo di corrispondenza** - Esatto, Contiene, Inizia con, o Regex (vedi sopra)

**URL del reindirizzamento** - Dove inviare il cliente. Può essere relativo (`/products/sale/`) o assoluto (`https://example.com/page/`)

**Tipo di reindirizzamento** - Codice di stato HTTP:
- **302 (Temporaneo)**: Consigliato. Il browser non lo memorizza, puoi cambiare il destinazione in un secondo momento
- **301 (Permanente)**: Il browser e i motori di ricerca lo memorizzano. Utilizzalo solo per reindirizzamenti permanenti

**Motore** - Opzionale. Limita a un motore di ricerca specifico

**Conteggio colpi** - Incrementa automaticamente ogni volta che viene utilizzato questo reindirizzamento. Aiuta a identificare le scorciatoie di navigazione più utilizzate.

**Attivo** - Abilita/disabilita questo reindirizzamento

## Esempi di reindirizzamento

| Term | Tipo di corrispondenza | URL | Caso d'uso |
|------|------------------------|-----|----------|
| sale | Esatto | `/products/sale/` | Reindirizza le ricerche "sale" alla pagina delle vendite |
| clearance | Esatto | `/clearance/` | Salta la ricerca per gli articoli in saldo |
| sizing | Contiene | `/pages/size-guide/` | Ogni query su sizing va alla guida |
| return | Inizia con | `/pages/returns/` | Le query relative al ritorno vanno alla politica |

Tutti utilizzano reindirizzamenti 302 (temporanei) per flessibilità.

## Tipo di reindirizzamento: 302 vs 301

**302 (Temporaneo)** - Consigliato per la maggior parte dei reindirizzamenti
- Il browser effettua una richiesta fresca ogni volta
- Puoi cambiare l'URL di destinazione in qualsiasi momento
- Scelta più sicura se non sei sicuro

**301 (Permanente)** - Utilizzalo con parsimonia
- Il browser memorizza il reindirizzamento
- I motori di ricerca aggiornano i loro indici
- Più difficile cambiarlo in seguito

**Consiglio**: Utilizza 302 a meno che non sia assolutamente certo che il reindirizzamento non cambierà mai.

## Analisi del conteggio colpi

Il campo Conteggio colpi si incrementa automaticamente ogni volta che un reindirizzamento viene attivato. Utilizzalo per:
- Identificare le scorciatoie di navigazione più utilizzate
- Trovare reindirizzamenti mai utilizzati (considera di eliminarli)
- Scoprire pattern di ricerca popolari

Rivedi i conteggi dei colpi mensilmente per ottimizzare la tua strategia di reindirizzamento.

## Trovare opportunità di sinonimi

**Utilizza le query senza risultati**: Naviga verso **Search > Search Analytics** e filtra per query senza risultati. Queste rivelano:
- Termini utilizzati dai clienti che non corrispondono alle descrizioni dei prodotti
- Variazioni regionali non considerate
- Errori di ortografia comuni

**Flusso di lavoro**:
1. Rivedi le query senza risultati settimanalmente
2. Identifica i pattern (stessi termini che appaiono ripetutamente)
3. Aggiungi sinonimi per mappare il linguaggio dei clienti ai nomi dei tuoi prodotti
4. Monitora se le query senza risultati diminuiscono

## Consigli

- **Monitora settimanalmente le query senza risultati per idee sui sinonimi** - Rivelano lacune tra il linguaggio dei clienti e le descrizioni dei tuoi prodotti
- **Inizia con sinonimi comuni, espandi in base ai dati** - Inizia con le variazioni regionali evidenti, quindi aggiungi in base al comportamento effettivo di ricerca
- **Utilizza la bidirezionalità per equivalenti veri** - La maggior parte dei sinonimi dovrebbe funzionare in entrambe le direzioni (laptop ↔ notebook)
- **Evita pattern regex complessi** - La corrispondenza regex è più lenta rispetto ad altri tipi di corrispondenza; utilizzala solo quando necessario
- **Utilizza per default i reindirizzamenti 302 (temporanei)** - Ti dà flessibilità per cambiare le destinazioni in seguito
- **Testa i sinonimi con query reali** - Cerca i termini sinonimi per verificare che restituiscano i risultati previsti
- **Sinonimi specifici per la lingua per negozi multilingua** - Crea mappature di termini adatti alla regione per ogni lingua che supporti