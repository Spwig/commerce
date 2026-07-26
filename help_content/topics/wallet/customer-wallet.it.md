---
title: Portafoglio Cliente
---

Il portafoglio cliente è un registro di credito del negozio che traccia un saldo in corso per ogni cliente. Il credito del negozio può essere aggiunto come risultato di rimborsi, premi per referenze, campagne promozionali o aggiustamenti manuali effettuati dal tuo team.

> **I saldi del portafoglio possono essere utilizzati al momento del pagamento.** Un cliente autenticato con credito del negozio lo vede nella fase di pagamento e può applicarlo con un clic. Il credito viene detratto dall'importo finale — dopo le tasse e la consegna — e qualsiasi rimanenza viene addebitata sulla loro carta come di consueto. Se il credito copre l'intero ordine, non è necessaria alcuna carta. Il credito viene riservato quando viene applicato e viene effettivamente detratto solo una volta che il pagamento è confermato, quindi un checkout abbandonato non costa nulla al cliente.

Naviga verso **Clienti > Portafogli Clienti** per visualizzare e gestire i portafogli.

## Comprendere i saldi del portafoglio

Ogni portafoglio cliente mostra quattro figure di saldo:

| Saldos | Descrizione |
|---|---|
| **Saldo Disponibile** | Il credito corrente e utilizzabile del cliente — questo sarà ciò che sarà spendibile al momento del pagamento una volta che questa funzionalità sarà attiva |
| **Saldo in Sospeso** | Crediti che non sono ancora nel saldo disponibile — ad esempio, un rimborso che è ancora all'interno della finestra di conferma |
| **Credito Totale** | L'importo totale mai credito a questo portafoglio, incluso tutti i crediti passati |
| **Utilizzato Totale** | L'importo totale mai addebitato da questo portafoglio |

Il saldo disponibile è la figura che importerà una volta che lo spending al checkout sarà attivo. I crediti in sospeso passano a esso una volta che il periodo di sospeso scade.

## Visualizzare il portafoglio di un cliente

1. Naviga verso **Clienti > Portafogli Clienti**
2. Utilizza il campo di ricerca per trovare il cliente per nome o email
3. Fai clic sull'entry del portafoglio per aprire la vista dettagliata

La vista dettagliata mostra i saldi correnti in alto e una cronologia completa delle transazioni in basso. I timestamp **Ultimo Credito** e **Ultimo Utilizzo** ti dicono quando il portafoglio è stato ultimamente attivo.

### Filtrare l'elenco dei portafogli

Utilizza il filtro **Attivo** per separare i portafogli attivi da quelli congelati. Un portafoglio contrassegnato come inattivo è congelato — non possono essere registrati crediti o addebiti su di esso, anche se mantiene il suo saldo.

## Leggere la cronologia delle transazioni

Ogni modifica al saldo del portafoglio viene registrata come una transazione individuale. La cronologia delle transazioni è un registro completo e permanente — le transazioni non vengono mai modificate o eliminate. Se è necessario correggere un errore, viene aggiunta una nuova transazione compensativa.

Ogni transazione mostra:

| Campo | Descrizione |
|---|---|
| **Tipo** | Credito, Debito, Rimborsa, Regolamento, o Annullamento |
| **Importo** | Il valore di questa transazione (sempre visualizzato come un numero positivo) |
| **Saldo Dopo** | Il saldo del portafoglio immediatamente dopo che questa transazione è stata applicata |
| **Fonte** | Dove il credito o il debito è originato |
| **Stato** | Completato, In Sospeso, o Annullato |
| **Descrizione** | Una breve spiegazione della transazione |
| **ID di Riferimento** | Un link al record originale (ad esempio, un numero di ordine o un ID di premio) |
| **Creato Il** | Quando la transazione è stata registrata |

### Spiegazione dei tipi di transazione

- **Credito** — fondi aggiunti al portafoglio (da un rimborso, una promozione o un aggiustamento manuale)
- **Debito** — fondi rimossi dal portafoglio. Una volta che lo spending al checkout è attivo, ciò significherà "speso su un ordine" — per ora l'unico modo in cui un debito avviene è un aggiustamento manuale
- **Rimborso** — credito aggiunto specificamente come risultato di un ordine restituito o annullato
- **Regolamento** — un aggiustamento manuale effettuato dal tuo team
- **Annullamento** — una transazione che annulla un'entry precedente

### Spiegazione delle fonti delle transazioni

- **Rimborso Ordine** — credito emesso quando un ordine è stato rimborsato sul portafoglio
- **Premio di Referenza** — credito guadagnato attraverso il programma di referenze
- **Promozione** — credito concesso come parte di una campagna di marketing
- **Regolamento Manuale** — credito aggiunto o rimosso direttamente da un membro dello staff
- **Pagamento Ordine** — fondi spesi al momento del pagamento per pagare un ordine. Non ancora in uso — riservato per quando lo spending del portafoglio al checkout è attivo

## Manual wallet adjustments

Non è possibile aggiungere o rimuovere fondi dal pannello di amministrazione — le transazioni del portafoglio vengono create solo dai processi che le possiedono: rimborso degli ordini, premi della fedeltà e premi per referenze. Questo è intenzionale. Ogni movimento ha un riferimento che indica la causa, e un controllo notturno verifica il saldo di ogni portafoglio rispetto alla sua storia; le righe inserite manualmente sono ciò che rompe questa catena.

Per un credito di cortesia — un reclamo sul servizio, un gesto dopo un problema — emetti invece una **carta regalo** manualmente (vedi l'argomento **Carte regalo** nell'help). Una carta regalo è progettata proprio per questo: tu controlli il valore, il cliente riceve un codice via email e può utilizzarla allo stesso modo del credito in negozio.

## Freezing a wallet

Se devi impedire a un cliente di utilizzare il saldo del suo portafoglio — ad esempio, durante un'indagine su frodi — puoi disattivarlo senza eliminarlo o rimuovere il saldo.

1. Apri la vista dettagliata del portafoglio del cliente
2. Deseleziona l'interruttore **Active**
3. Clicca su **Save**

Il saldo viene conservato e il portafoglio può essere riattivato in qualsiasi momento. Durante l'inattività, non possono essere registrati nuovi crediti o addebiti — manuali o altrimenti — sul portafoglio.

## Viewing all transactions

Per ottenere una visione generale delle attività del portafoglio, vai a **Customers > Wallet Transactions**. Questa lista mostra ogni transazione in tutti i portafogli dei clienti, con filtri per:

- **Transaction Type** — filtra per credito, addebito, aggiustamento, ecc.
- **Source** — filtra per dove sono originate le transazioni
- **Status** — filtra per completate, in sospeso o annullate
- **Date** — utilizza la gerarchia delle date in alto per esplorare un giorno, mese o anno specifico

L'elenco delle transazioni è in sola lettura — non è possibile modificare o eliminare le transazioni da questa vista.

## Tips

- Controlla **Lifetime Credited** versus **Lifetime Used** per comprendere quanto attivamente un cliente utilizza il suo credito in negozio — un grande saldo non utilizzato potrebbe indicare che il cliente ha dimenticato che esiste
- Se un cliente segnala che il suo saldo sembra errato, controlla l'intera cronologia delle transazioni per tracciare esattamente come il saldo è cambiato nel tempo; la colonna **Balance After** in ogni voce rende questo facile
- Un grande saldo non utilizzato vale una spinta — i clienti vedono il loro credito in negozio sul dashboard dell'account e durante il pagamento al momento del checkout, ma un breve'email che lo segnala spesso lo converte in un ordine
- I portafogli congelati mantengono il loro saldo in modo permanente; non c'è scadenza — se disattivi temporaneamente un portafoglio, ricordati di riattivarlo quando il problema è risolto
- L'**Reference ID** su ogni transazione si collega al record originale, rendendo semplice verificare il motivo per cui è stato applicato un credito o un addebito senza dover cercare altrove