---
title: Portafoglio Clienti
---

Il portafoglio clienti è un sistema di credito per il negozio che dà ai clienti un saldo che possono utilizzare per futuri ordini. Il credito del negozio può essere aggiunto come risultato di rimborsi, premi per referenze, campagne promozionali o aggiustamenti manuali effettuati dal tuo team. I clienti possono quindi applicare il loro saldo del portafoglio al momento del checkout per ridurre l'importo che pagano.

Naviga verso **Clienti > Portafogli Clienti** per visualizzare e gestire i portafogli.

## Comprendere i saldi del portafoglio

Ogni portafoglio cliente mostra quattro figure di saldo:

| Saldos | Descrizione |
|---|---|
| **Saldo Disponibile** | L'importo che il cliente può spendere immediatamente al momento del checkout |
| **Saldo in Sospeso** | Crediti che non sono ancora spendibili - ad esempio, un rimborso che è ancora all'interno del periodo di conferma |
| **Credito Totale** | L'importo totale mai credito a questo portafoglio, incluso tutti i crediti passati |
| **Totale Utilizzato** | L'importo totale che il cliente ha speso dal loro portafoglio in tutti gli ordini |

Il saldo disponibile è l'unica figura che ha importanza al momento del checkout. I crediti in sospeso diventano disponibili una volta scaduto il periodo di sospeso.

## Visualizzare il portafoglio di un cliente

1. Naviga verso **Clienti > Portafogli Clienti**
2. Utilizza il campo di ricerca per trovare il cliente per nome o email
3. Fai clic sull'ingresso del portafoglio per aprire la vista dettagliata

La vista dettagliata mostra i saldi correnti in alto e una cronologia completa delle transazioni in basso. I timestamp **Ultimo Credito** e **Ultimo Utilizzo** ti dicono quando il portafoglio è stato ultimamente attivo.

### Filtrare l'elenco dei portafogli

Utilizza il filtro **Attivo** per separare i portafogli attivi da quelli congelati. Un portafoglio contrassegnato come inattivo non può essere utilizzato al momento del checkout anche se ha un saldo positivo.

## Leggere la cronologia delle transazioni

Ogni cambiamento nel saldo del portafoglio viene registrato come una transazione individuale. La cronologia delle transazioni è un registro completo e permanente - le transazioni non vengono mai modificate o eliminate. Se è necessario correggere un errore, viene aggiunta una nuova transazione compensativa invece.

Ogni transazione mostra:

| Campo | Descrizione |
|---|---|
| **Tipo** | Credito, Debito, Rimborsa, Aggiustamento o Annullamento |
| **Importo** | Il valore di questa transazione (sempre visualizzato come un numero positivo) |
| **Saldo Dopo** | Il saldo del portafoglio immediatamente dopo che questa transazione è stata applicata |
| **Fonte** | Dove il credito o il debito è originato |
| **Stato** | Completato, In Sospeso o Annullato |
| **Descrizione** | Una breve spiegazione della transazione |
| **ID di Riferimento** | Un collegamento al record originale (es. un numero di ordine o un ID di premio) |
| **Creato Il** | Quando la transazione è stata registrata |

### Spiegazione dei tipi di transazione

- **Credito** - fondi aggiunti al portafoglio (da un rimborso, una promozione o un aggiustamento manuale)
- **Debito** - fondi spesi al momento del checkout
- **Rimborso** - credito aggiunto specificamente come risultato di un ordine restituito o annullato
- **Aggiustamento** - un aggiustamento manuale effettuato dal tuo team
- **Annullamento** - una transazione che annulla un'entrata precedente

### Spiegazione delle fonti delle transazioni

- **Rimborso Ordine** - credito emesso quando un ordine è stato rimborsato al portafoglio
- **Premio di Referenza** - credito guadagnato attraverso il programma di referenze
- **Promozione** - credito concesso come parte di una campagna di marketing
- **Aggiustamento Manuale** - credito aggiunto o rimosso direttamente da un membro dello staff
- **Pagamento Ordine** - fondi spesi al momento del checkout per pagare un ordine

## Aggiustamenti manuali del portafoglio

Non puoi aggiungere o rimuovere fondi direttamente dalla vista dettagliata del portafoglio - le transazioni del portafoglio vengono create attraverso i processi pertinenti (rimborsi, premi, promozioni). Tuttavia, i membri dello staff con i permessi appropriati possono creare transazioni di aggiustamento manuale attraverso la sezione **Transazioni del Portafoglio**.

Naviga verso **Clienti > Transazioni del Portafoglio** e utilizza **+ Aggiungi Transazione del Portafoglio** se devi applicare un credito che non si adatta ad un'altra fonte - ad esempio, un credito di buona volontà seguendo una lamentela per il servizio.

Quando si crea un aggiustamento manuale:

1.

Seleziona il **Portafoglio** che stai aggiustando (cerca per email del cliente)
2.

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Imposta **Tipo di transazione** su `Adjustment`
3.

Imposta **Fonte** su `Manual Adjustment`
4.

Inserisci l'**Importo** — sempre un numero positivo, indipendentemente dalla direzione
5.

Imposta lo **Stato** su `Completed` per un credito immediato
6.

Aggiungi una descrizione chiara che spieghi il motivo — questa è visibile nella cronologia delle transazioni
7.

Fai clic su **Salva**

> **Nota:** Poiché le transazioni del portafoglio sono immutabili, controlla attentamente l'importo e il portafoglio prima di salvare. Se commetti un errore, dovrai creare una transazione di reverso per correggerla.

## Blocco di un portafoglio

Se devi impedire a un cliente di utilizzare il saldo del portafoglio — ad esempio, durante un'indagine su frodi — puoi disattivarlo senza eliminarlo o rimuovere il saldo.

1. Apri la vista dettagliata del portafoglio del cliente
2. Deseleziona l'interruttore **Attivo**
3. Fai clic su **Salva**

Il saldo viene conservato e il portafoglio può essere riattivato in qualsiasi momento. Durante il blocco, il cliente non può utilizzare il saldo del portafoglio al momento del checkout.

## Visualizzazione di tutte le transazioni

Per ottenere una visione globale dell'attività del portafoglio, vai a **Customers > Wallet Transactions**. Questa lista mostra ogni transazione in tutti i portafogli dei clienti, con filtri per:

- **Tipo di transazione** — filtra per credito, debito, adjustment, ecc.
- **Fonte** — filtra per dove sono originate le transazioni
- **Stato** — filtra per completato, in sospeso o annullato
- **Data** — utilizza la gerarchia delle date in alto per esplorare un giorno, mese o anno specifico

L'elenco delle transazioni è in sola lettura — non è possibile modificare o eliminare le transazioni da questa vista.

## Consigli

- Controlla **Credito totale** versus **Utilizzato totale** per comprendere quanto attivamente un cliente utilizza il credito del negozio — un grande saldo non utilizzato potrebbe indicare che il cliente ha dimenticato che esiste
- Se un cliente segnala che il saldo sembra errato, esamina la cronologia completa delle transazioni per tracciare esattamente come il saldo è cambiato nel tempo; la colonna **Saldo dopo** in ogni voce rende questo facile
- Utilizza i crediti del portafoglio come strumento per la fidelizzazione dei clienti — un credito di buonafede dopo un'esperienza di ordine difficile può costare meno di un rimborso, mantenendo comunque il cliente a spendere nel tuo negozio
- I portafogli bloccati conservano il saldo in modo permanente; non c'è scadenza — se disattivi temporaneamente un portafoglio, ricordati di riattivarlo quando il problema è risolto
- L'**ID di riferimento** su ogni transazione si collega al record originale, rendendo semplice verificare il motivo per cui è stato applicato un credito o un debito senza dover cercare altrove