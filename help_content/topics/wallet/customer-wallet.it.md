---
title: Portafoglio del cliente
---

Il portafoglio del cliente è un registro di credito del negozio che traccia un saldo in corso per ogni cliente. Il credito del negozio può essere aggiunto come risultato di rimborsi, premi per referenze, campagne promozionali o aggiustamenti manuali effettuati dal tuo team.

> **I saldi del portafoglio possono essere utilizzati al momento del pagamento.** Un cliente autenticato con credito del negozio lo vede nella fase di pagamento e può applicarlo con un clic. Il credito viene detratto dall'importo finale — dopo le tasse e la consegna — e qualsiasi rimanenza viene addebitata sulla loro carta come di consueto. Se il credito copre l'intero ordine, non è necessaria alcuna carta. Il credito viene riservato quando viene applicato e viene effettivamente detratto solo una volta che il pagamento è confermato, quindi un checkout abbandonato non costa nulla al cliente.

Naviga verso **Clienti > Portafogli dei clienti** per visualizzare e gestire i portafogli.

## Comprendere i saldi del portafoglio

Ogni portafoglio del cliente mostra quattro figure di saldo:

| Saldos | Descrizione |
|---|---|
| **SALDO DISPONIBILE** | Il credito corrente e utilizzabile del cliente — questo sarà ciò che sarà spendibile al momento del pagamento una volta che questa funzionalità sarà attiva |
| **SALDO IN ATTESA** | Crediti che non sono ancora nel saldo disponibile — ad esempio, un rimborso che è ancora all'interno della finestra di conferma |
| **Credito totale nel corso della vita** | L'importo totale mai credito a questo portafoglio, incluso tutti i crediti passati |
| **Utilizzato nel corso della vita** | L'importo totale mai addebitato da questo portafoglio |

Il saldo disponibile è la figura che importerà una volta che lo spending al checkout sarà attivo. I crediti in sospeso passano a esso una volta che il periodo di sospeso scade.

## Visualizzare il portafoglio di un cliente

1. Naviga verso **Clienti > Portafogli dei clienti**
2. Utilizza il campo di ricerca per trovare il cliente per nome o email
3. Fai clic sull'ingresso del portafoglio per aprire la vista dettagliata

La vista dettagliata mostra i saldi correnti in alto e una cronologia completa delle transazioni in basso. I timestamp **Ultimo credito** e **Ultimo utilizzo** ti dicono quando il portafoglio è stato ultimamente attivo.

### Filtrare l'elenco dei portafogli

Utilizza il filtro **Attivo** per separare i portafogli attivi da quelli congelati. Un portafoglio contrassegnato come inattivo è congelato — non possono essere registrati né crediti né addebiti su di esso, anche se mantiene il suo saldo.

## Leggere la cronologia delle transazioni

Ogni cambiamento nel saldo del portafoglio viene registrato come una transazione individuale. La cronologia delle transazioni è un registro completo e permanente — le transazioni non vengono mai modificate o eliminate. Se è necessario correggere un errore, viene aggiunta una nuova transazione compensativa.

Ogni transazione mostra:

| Campo | Descrizione |
|---|---|
| **Tipo** | Credito, Addebito, Rimborso, Aggiustamento o Annullamento |
| **Importo** | Il valore di questa transazione (sempre visualizzato come un numero positivo) |
| **Saldo Dopo** | Il saldo del portafoglio immediatamente dopo che questa transazione è stata applicata |
| **Fonte** | Dove il credito o l'addebito è originato |
| **Stato** | Completato, In sospeso o Annullato |
| **Descrizione** | Una breve spiegazione della transazione |
| **ID di riferimento** | Un collegamento al record originale (ad esempio, un numero di ordine o un ID di premio) |
| **Creato il** | Quando la transazione è stata registrata |

### Spiegazione dei tipi di transazione

- **Credito** — fondi aggiunti al portafoglio (da un rimborso, una promozione o un aggiustamento manuale)
- **Addebito** — fondi rimossi dal portafoglio. Una volta che lo spending al checkout è attivo, ciò significherà "speso su un ordine" — per ora l'unico modo in cui un addebito avviene è un aggiustamento manuale
- **Rimborso** — credito aggiunto specificamente come risultato di un ordine restituito o annullato
- **Aggiustamento** — un aggiustamento manuale effettuato dal tuo team
- **Annullamento** — una transazione che annulla un'entrata precedente

### Spiegazione delle fonti delle transazioni

- **Rimborso dell'ordine** — credito emesso quando un ordine è stato rimborsato sul portafoglio
- **Premio per referenza** — credito guadagnato attraverso il programma di referenze
- **Promozione** — credito concesso come parte di una campagna di marketing
- **Aggiustamento manuale** — credito aggiunto o rimosso direttamente da un membro dello staff
- **Pagamento dell'ordine** — fondi spesi al momento del pagamento per pagare un ordine. Non è ancora in uso — riservato per quando lo spending del portafoglio al checkout è attivo

## Regolamenti manuali del portafoglio

Non è possibile aggiungere o rimuovere fondi dal pannello di amministrazione — le transazioni del portafoglio vengono create solo dai processi che le possiedono: rimborso degli ordini, premi della fedeltà e premi per referenze. Questo è intenzionale. Ogni movimento ha un riferimento che indica la causa, e un controllo notturno verifica il saldo di ogni portafoglio rispetto alla sua storia; le righe inserite manualmente sono ciò che rompe questa catena.

Per un credito di cortesia — un reclamo sul servizio, un gesto dopo un problema — emetti invece una **carta regalo** manualmente (vedi l'argomento **Carte regalo**). Una carta regalo è progettata proprio per questo: tu controlli il valore, il cliente riceve un codice via email e può utilizzarla allo stesso modo del credito del negozio durante il checkout.

## Blocco del portafoglio

Se devi impedire a un cliente di utilizzare il saldo del suo portafoglio — ad esempio, durante un'indagine su frodi — puoi disattivarlo senza eliminarlo o rimuovere il saldo.

1. Apri la vista dettagliata del portafoglio del cliente
2. Deseleziona l'interruttore **Attivo**
3. Clicca su **Salva**

Il saldo viene conservato e il portafoglio può essere riattivato in qualsiasi momento. Durante il blocco, non possono essere registrati nuovi crediti o addebiti — manuali o altrimenti — sul portafoglio.

## Visualizzazione di tutte le transazioni

Per una visione generale delle attività del portafoglio, vai a **Clienti > Transazioni del portafoglio**. Questa lista mostra ogni transazione in tutti i portafogli dei clienti, con filtri per:

- **Tipo di transazione** — filtra per credito, addebito, regolamento, ecc.
- **Fonte** — filtra per dove sono originate le transazioni
- **Stato** — filtra per completato, in sospeso o annullato
- **Data** — utilizza la gerarchia delle date in alto per esplorare un giorno, mese o anno specifico

L'elenco delle transazioni è in sola lettura — non è possibile modificare o eliminare le transazioni da questa vista.

## Consigli

- Controlla **Credito totale** rispetto a **Utilizzato totale** per comprendere quanto attivamente un cliente utilizza il credito del negozio — un grande saldo non utilizzato potrebbe indicare che il cliente ha dimenticato che esiste
- Se un cliente segnala che il suo saldo sembra errato, controlla l'intera cronologia delle transazioni per tracciare esattamente come il saldo è cambiato nel tempo; la colonna **Saldo dopo** in ogni voce rende questo facile
- Un grande saldo non utilizzato vale un promemoria — i clienti vedono il loro credito del negozio sul dashboard del profilo e durante il pagamento al checkout, ma un breve email che lo segnala spesso lo converte in un ordine
- I portafogli bloccati conservano il loro saldo in modo permanente; non c'è scadenza — se disattivi temporaneamente un portafoglio, ricordati di riattivarlo quando il problema è risolto
- L'**ID di riferimento** su ogni transazione si collega al record originale, rendendo semplice verificare il motivo per cui è stato applicato un credito o un addebito senza dover cercare altrove