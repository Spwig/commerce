---
title: Tracking degli affiliati & Link
---

Il sistema di commissioni si basa sul tracking degli affiliati collegando gli acquisti dei clienti agli affiliati che li hanno riferiti. Questa guida spiega come funzionano i link di tracciamento, i dati che Spwig registra quando i clienti cliccano su questi link e come il sistema di attribuzione basato sui cookie determina quale affiliato riceve ogni commissione.

Comprendere i meccanismi di tracciamento vi aiuta a risolvere i problemi di attribuzione, analizzare le prestazioni dei link e istruire gli affiliati su come massimizzare le loro conversioni.

## Cosa è un link di tracciamento?

Un link di tracciamento è un URL unico che reindirizza i clienti al vostro negozio registrando l'identità dell'affiliato in un cookie. Ogni affiliato può creare diversi link di tracciamento che puntano a destinazioni diverse — la homepage, prodotti specifici, pagine di raccolta o pagine di atterraggio.

Formato del link di tracciamento:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Questo link reindirizza alla destinazione impostando un cookie di tracciamento che associa gli acquisti futuri all'affiliato che possiede il codice del link `a2b7f8c4d1e9`.

Gli affiliati generano questi link dal loro pannello di controllo. Copiano l'URL completo e lo condividono in post del blog, social media, email o qualsiasi canale in cui raggiungono potenziali clienti.

## Componenti del link di tracciamento

Ogni link di tracciamento contiene questi elementi:

| Componente | Esempio | Descrizione |
|-----------|---------|-------------|
| **URL base** | `https://yourstore.com` | Il dominio del vostro negozio |
| **Percorso di tracciamento** | `/affiliate/track/` | Endpoint di tracciamento di Spwig |
| **Codice del link** | `a2b7f8c4d1e9` | Identificatore unico automaticamente generato di 12 caratteri |
| **Destinazione** | Impostata quando il link è creato | Dove il cliente atterra dopo il reindirizzamento (homepage, prodotto, ecc.) |

Quando un affiliato crea un link, Spwig genera automaticamente il codice unico di 12 caratteri. L'affiliato non deve mai creare o modificare manualmente questo codice — semplicemente sceglie la destinazione e Spwig gestisce il resto.

### Etichette del link (opzionale)

Gli affiliati possono aggiungere un'etichetta a ciascun link per la propria organizzazione:
- "Link del profilo Instagram"
- "Descrizione di YouTube"
- "Campagna email Black Friday"

Le etichette aiutano gli affiliati a tracciare quali canali promozionali funzionano meglio. Sono visibili solo all'affiliato e a voi — i clienti non vedono mai l'etichetta.

## Come funziona il tracciamento

Il processo di tracciamento e attribuzione segue cinque passaggi dal clic alla commissione:

### 1. Cliente clicca sul link

Un potenziale cliente clicca sul link di tracciamento dell'affiliato da qualsiasi canale promozionale (post sui social media, articolo del blog, newsletter email).

### 2. Clic registrato

L'endpoint di tracciamento di Spwig registra i dettagli del clic:
- Indirizzo IP
- User agent (browser e dispositivo)
- HTTP referrer (da dove è arrivato il clic)
- Timestamp
- Identificatore di sessione

Questi dati appaiono nel pannello amministrativo **Clicchi** a **Affiliati > Clicchi** per l'analisi e la rilevazione dello spam.

### 3. Cookie impostato

Il sistema di tracciamento imposta un cookie nel browser del cliente prima del reindirizzamento. Il cookie contiene:
- ID affiliato (chi dovrebbe ricevere la commissione)
- ID programma (quale struttura di commissione si applica)
- Codice del link (quale link specifico è stato cliccato)

### 4. Cliente effettua l'acquisto

Il cliente naviga nel vostro negozio e completa l'acquisto. Questo può accadere immediatamente o giorni/settimane dopo, purché l'acquisto avvenga entro la finestra di validità del cookie.

### 5. Commissione creata

Al momento del checkout, Spwig controlla la presenza del cookie dell'affiliato. Se trovato e ancora valido (entro la finestra di validità del cookie), il sistema crea un record di commissione con lo stato **In attesa** associato all'affiliato, al programma e all'ordine.

## Attribuzione basata su cookie

Il cookie di tracciamento è il meccanismo centrale che collega gli acquisti agli affiliati. Comprendere come funzionano i cookie vi aiuta a impostare finestre di attribuzione ottimali e a risolvere problemi di tracciamento.

### Struttura del cookie

| Proprietà | Valore |
|----------|-------|
| **Nome** | `aff_{program_id}` (es. `aff_7` per l'ID programma 7) |
| **Valore** | JSON contenente l'ID affiliato, codice del link, timestamp |
| **Dominio** | Il dominio del vostro negozio |
| **Percorso** | `/` (accesso sito-wide) |
| **Durata** | Durata del cookie del programma (1–365 giorni) |
| **HttpOnly** | `true` (impedisce l'accesso tramite JavaScript per motivi di sicurezza) |
| **SameSite** | `Lax` (consente il tracciamento da referrer esterni) |
| **Secure** | `true` su siti HTTPS (consigliato) |

### Finestra di validità del cookie

La durata del cookie determina quanto tempo i clienti hanno per effettuare un acquisto dopo aver cliccato su un link di un affiliato. Questa finestra è impostata per programma a **Marketing > Programmi di affiliati** quando si crea o modifica un programma.

Durate standard del cookie per settore:
- **7 giorni**: Prodotti con decisione rapida (prodotti alimentari, biglietti per eventi)
- **30 giorni**: E-commerce standard (impostazione più comune)
- **60–90 giorni**: Acquisti considerati (arredamento, elettronica, prodotti B2B)
- **365 giorni**: Cicli di vendita lunghi (prodotti di lusso, servizi ad alto prezzo)

Se un cliente clicca su un link di un affiliato il 1 gennaio e la durata del cookie è di 30 giorni, qualsiasi acquisto effettuato entro il 30 gennaio attribuisce la commissione a quell'affiliato. Gli acquisti del 31 gennaio o successivi non generano una commissione perché il cookie è scaduto.

### Modello di attribuzione per ultimo clic

Spwig utilizza il modello di attribuzione **per ultimo clic**: l'ultimo clic dell'affiliato vince. Ecco come funziona:

**Scenario**: Un cliente clicca sul link dell'affiliato A il lunedì, poi clicca sul link dell'affiliato B il mercoledì e infine effettua l'acquisto il venerdì.

**Risultato**: L'affiliato B riceve la commissione perché il suo link è stato l'ultimo clic.

Il cookie dell'ultimo clic sovrascrive i cookie degli affiliati precedenti. Questo modello è semplice da comprendere e impedisce le commissioni doppie, anche se significa che solo un affiliato riceve il credito per ordine (l'ultimo prima dell'acquisto).

## Registrazione dei clic

Spwig registra ogni clic su ogni link di affiliato per fornire analisi sia a voi che agli affiliati. I dati dei clic aiutano a misurare le prestazioni dei link, rilevare lo spam e ottimizzare le strategie promozionali.

### Dati registrati per ogni clic

Navigare a **Affiliati > Clicchi** per visualizzare tutti i clic registrati. Ogni voce contiene:

| Campo | Descrizione |
|-------|-------------|
| **Link** | Quale link di tracciamento è stato cliccato |
| **Affiliato** | Chi ha creato il link |
| **Indirizzo IP** | Indirizzo IP del cliente (per la rilevazione dello spam) |
| **User Agent** | Informazioni sul browser e dispositivo |
| **Referrer** | Pagina da cui il cliente ha cliccato sul link (es. "https://instagram.com") |
| **ID sessione** | Identificatore unico per questa sessione di navigazione |
| **Timestamp** | Data e ora esatte del clic |

### Limitazione del tasso di clic

Per prevenire lo spam di clic e l'abuso da parte di bot, Spwig limita i clic a **100 al minuto per indirizzo IP**. Se lo stesso IP supera questo limite, i clic aggiuntivi vengono ignorati e non incrementano i conteggi dei clic.

Questo protegge da attori malintenzionati che cercano di gonfiare i dati dei clic senza bloccare il traffico legittimo. I clienti reali quasi mai superano i 100 clic al minuto.

### Considerazioni sulla privacy

I dati dei clic contengono indirizzi IP e user agent per scopi di rilevazione dello spam. Assicuratevi che la vostra policy sulla privacy rivelare che tracciate le referenze degli affiliati e condividete dati sulle prestazioni anonimizzati con gli affiliati.

## Visualizzazione dei link degli affiliati

Tutti i link di tracciamento generati dagli affiliati appaiono nel vostro pannello amministrativo per il monitoraggio e la gestione.

### Accesso all'elenco dei link

Navigare a **Affiliati > Link** per visualizzare tutti i link di tracciamento per tutti gli affiliati e i programmi. La vista in elenco mostra:

- **Codice del link**: L'identificatore unico di 12 caratteri
- **Affiliato**: Chi ha creato il link
- **Programma**: Quale struttura di commissione si applica
- **Etichetta**: Descrizione opzionale fornita dall'affiliato
- **Destinazione**: Dove il link reindirizza i clienti
- **Totale clicchi**: Conteggio totale dei clic
- **Stato attivo**: Se il link è attualmente in tracciamento

### Filtrare i link

Utilizzare i filtri amministrativi per restringere l'elenco:
- **Per affiliato**: Vedere tutti i link per un partner specifico
- **Per programma**: Visualizzare i link che promuovono una specifica struttura di commissione
- **Per stato attivo**: Trovare i link disattivati

Questo filtraggio vi aiuta ad analizzare la distribuzione dei link nella vostra rete di affiliati e a identificare i link con le migliori prestazioni.

## Statistiche dei link

Ogni link di tracciamento accumula metriche sulle prestazioni che aiutano gli affiliati a ottimizzare le loro strategie promozionali e vi aiutano a identificare i vostri partner con le migliori prestazioni.

### Clicca su un record del link per visualizzare le statistiche dettagliate:

| Metrica | Descrizione | Calcolo |
|--------|-------------|-------------|
| **Totale clicchi** | Tutti i clic registrati da quando è stato creato il link | Conteggio dei record dei clic |
| **Clicchi (7 giorni)** | Indicatore di attività recente | Clicchi negli ultimi 7 giorni |
| **Conversioni** | Ordini attribuiti a questo link | Conteggio delle commissioni da questo codice del link |
| **Tasso di conversione** | Percentuale di clic che hanno portato a un acquisto | (Conversioni ÷ Totale clicchi) × 100 |
| **Totale ricavi** | Somma di tutti i valori degli ordini da questo link | Somma dei totali degli ordini per i clic convertiti |

### Utilizzare le statistiche per l'ottimizzazione

**Per gli affiliati**: Questi numeri mostrano quali canali promozionali funzionano meglio. Se un link del profilo Instagram ha un tasso di conversione del 5% ma un link di un articolo del blog ha il 15%, l'affiliato dovrebbe concentrarsi di più sul contenuto del blog.

**Per i commercianti**: Le statistiche dei link rivelano quali affiliati generano traffico di qualità. Un alto numero di clic con un basso tasso di conversione suggerisce che l'audience dell'affiliato non è adatto ai vostri prodotti.

## Gestione dei link

Puoi gestire i link degli affiliati dal pannello amministrativo per scopi di manutenzione e risoluzione dei problemi.

### Disattivare i link

Per impedire a un link specifico di tracciare nuovi clic mantenendo i dati storici:

1. Navigare a **Affiliati > Link**
2. Cliccare sul link che si desidera disattivare
3. Deselezionare **Attivo**
4. Cliccare su **Salva**

I link disattivati reindirizzano comunque i clienti alla destinazione, ma non impostano cookie di tracciamento né registrano clic. Questo è utile quando un affiliato sta conducendo una campagna temporanea o quando è necessario disattivare un canale promozionale specifico.

### Modificare i dettagli del link

È possibile modificare:
- **Etichetta**: Aggiornare la descrizione fornita dall'affiliato
- **Destinazione**: Cambiare dove il link reindirizza (utile se si sposta una pagina del prodotto)
- **Stato attivo**: Abilitare o disabilitare il tracciamento

Non è possibile modificare il codice del link — è permanente e legato a tutti i dati storici di clic e commissioni.

### Eliminare i link inattivi

Eliminate i link non utilizzati che non hanno clic o conversioni storiche. Questo mantiene la lista dei link pulita senza perdere dati analitici importanti.

**Attenzione**: Eliminare un link rimuove tutti i record dei clic associati. Eliminate i link solo se non hanno clic o se siete assolutamente sicuri di non averne bisogno per i dati storici.

## Modello di attribuzione

Comprendere la logica di attribuzione di Spwig vi aiuta a stabilire aspettative con gli affiliati e a risolvere le dispute sulle commissioni.

### Attribuzione per ultimo clic

Come menzionato in precedenza, Spwig utilizza l'attribuzione per ultimo clic: se un cliente clicca su diversi link di affiliati prima dell'acquisto, solo l'ultimo affiliato riceve la commissione.

**Vantaggi**:
- Semplice da comprendere e spiegare
- Impedisce le commissioni doppie
- Riconosce gli affiliati che chiudono l'affare

**Svantaggi**:
- Gli affiliati che hanno introdotto il cliente non ricevono alcun credito
- Non riflette i percorsi di acquisto multi-touch
- Potrebbe incentivare il "hijacking" dei link (affiliati che mirano a clienti ad alto intento già riferiti da qualcun altro)

### La durata del cookie determina l'attribuzione

Solo gli acquisti all'interno della finestra di validità del cookie generano commissioni. Se il cookie scade prima del checkout, non viene creata alcuna commissione anche se il cliente ritorna tramite un bookmark.

**Esempio**: Durata del cookie di 30 giorni
- Cliente clicca sul link il 1 gennaio → Cookie impostato, scade il 31 gennaio
- Cliente effettua l'acquisto il 25 gennaio → Commissione creata
- Cliente effettua l'acquisto il 5 febbraio → Nessuna commissione (cookie scaduto)

### Tracciamento della sessione

Oltre al cookie, Spwig traccia l'ID della sessione per ogni clic. Questo consente l'attribuzione su più visite all'interno della stessa sessione anche se i cookie sono bloccati o cancellati.

Se un cliente clicca su un link, naviga nel vostro negozio e carica più pagine, quindi effettua l'acquisto — tutto nella stessa sessione — l'affiliato riceve il credito anche senza un cookie persistente.

## Risoluzione dei problemi

Problemi comuni di tracciamento e come risolverli:

### Link non traccia i clic

**Sintomi**: Il conteggio dei clic rimane a zero nonostante gli affiliati riferiscano di aver condiviso il link.

**Causa e soluzione**:
1. **Link disattivato**: Controllare lo stato **Attivo** nella pagina dettagli del link
2. **Programma disattivato**: Navigare a **Affiliati > Programmi** e verificare che lo stato del programma sia **Attivo**
3. **Account affiliato disattivato**: Controllare lo stato dell'account affiliato a **Affiliati > Affiliati**
4. **Limitazione del tasso**: Controllare se lo stesso IP genera troppi clic (traffico bot)

### Basso tasso di conversione

**Sintomi**: Alti conteggi di clic ma pochi ordini attribuiti.

**Causa e soluzione**:
1. **Durata del cookie troppo breve**: Aumentare la durata del cookie del programma se i vostri prodotti richiedono ricerca e considerazione
2. **Qualità della pagina di destinazione**: Controllare la pagina di atterraggio — è mobile-friendly? Carica velocemente? Il prodotto è disponibile in magazzino?
3. **Mismatch dell'audience**: L'audience dell'affiliato potrebbe non essere adatto ai vostri prodotti
4. **Browser che blocca i cookie**: Alcuni strumenti di privacy bloccano i cookie di terze parti, anche se Spwig utilizza cookie di prima parte che sono meno probabili di essere bloccati

### Registri di clic duplicati

**Sintomi**: Lo stesso cliente genera diversi registri di clic in rapida successione.

**Causa**: Questo è un comportamento normale. Ogni caricamento di pagina del link di tracciamento genera un registro di clic. Se un cliente clicca, la pagina si carica lentamente e clicca di nuovo, vedrete diversi registri.

**Soluzione**: Nessun'azione necessaria. Il limitatore di tasso impedisce l'abuso (100 clic/minuto/IP), e i clic duplicati dalla stessa sessione non influiscono sull'attribuzione — viene impostato un solo cookie.

## Consigli

- **Testare il tracciamento prima del lancio** — Creare un account affiliato di test, generare un link di tracciamento, cliccarlo in un browser in incognito e completare un acquisto di test. Verificare che la commissione appaia con l'attribuzione corretta all'affiliato.
- **Istruire gli affiliati sulla durata del cookie** — Assicurarsi che gli affiliati comprendano che ricevono commissioni solo per gli acquisti effettuati entro la finestra del cookie. Questo li aiuta a stabilire aspettative realiste e a concentrarsi sul traffico ad alto intento.
- **Monitorare i pattern dei clic per rilevare lo spam** — Un numero insolitamente alto di clic da un singolo IP o clic senza stringa user agent potrebbe indicare traffico bot. Esaminare attentamente questi affiliati prima di approvare le commissioni.
- **Utilizzare le etichette dei link in modo coerente** — Incoraggiare gli affiliati a etichettare i loro link per canale (Instagram, Blog, Email) in modo da poter entrambi analizzare quali canali promozionali generano le conversioni migliori.
- **Considerare una durata del cookie più lunga per prodotti ad alto prezzo** — Se il valore medio degli ordini è alto e i clienti tipicamente effettuano ricerche prima di acquistare, estendere la durata del cookie a 60–90 giorni per catturare quelle conversioni ritardate.
- **Controllare i dati del referrer per ottenere informazioni sui canali** — Il campo referrer mostra da dove provengono i clic. Se vedete molti clic da "instagram.com" o "youtube.com", sapete quali piattaforme social i vostri affiliati utilizzano in modo più efficace.