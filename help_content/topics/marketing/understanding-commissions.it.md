---
title: Comprendere le Commissioni
---

Le commissioni sono registri di guadagni creati quando un affiliato riesce a generare un acquisto nel tuo negozio. Ogni commissione è legata a un ordine specifico, a un affiliato e a un programma, e passa attraverso un ciclo di vita da in sospeso a pagato. Questa guida spiega come funzionano le commissioni, come vengono calcolate e come gestirle efficacemente.

## Cosa è una Commissione?

Una commissione rappresenta l'importo dovuto a un affiliato per aver riferito un cliente che ha completato un acquisto. Quando un cliente clicca su un link di riferimento di un affiliato e effettua un ordine entro la finestra di tempo di validità del cookie, Spwig crea automaticamente un registro della commissione.

Ogni commissione contiene:
- **Affiliato** — Il partner che ha riferito il cliente
- **Programma** — Il programma degli affiliati che definisce le regole delle commissioni
- **Ordine** — L'ordine che ha generato la commissione
- **Importo** — Il valore della commissione calcolato
- **Stato** — La fase corrente nel ciclo di vita della commissione
- **Date** — Data di creazione, data di approvazione/rifiuto e data di pagamento

## Calcolo delle Commissioni

Le commissioni vengono calcolate automaticamente in base al tipo di commissione e al tasso del programma.

| Tipo di Commissione | Calcolo | Esempio |
|---------------------|---------|---------|
| **Percentuale** | Totale Ordine × Percentuale di Commissione ÷ 100 | Ordine: $200, Tasso: 10% → **Commissione di $20** |
| **Fissa** | Importo fisso per ordine | Tasso: $15 → **Commissione di $15** (indipendentemente dal valore dell'ordine) |

### Esempi di Calcolo

**Commissione Percentuale (10%)**:
- Cliente effettua un ordine di $50 → $5 di commissione
- Cliente effettua un ordine di $150 → $15 di commissione
- Cliente effettua un ordine di $300 → $30 di commissione

**Commissione Fissa ($20)**:
- Cliente effettua un ordine di $50 → $20 di commissione
- Cliente effettua un ordine di $150 → $20 di commissione
- Cliente effettua un ordine di $300 → $20 di commissione

La commissione viene calcolata sul **sottototale dell'ordine** (prima delle spese di spedizione e delle tasse) e viene creata immediatamente quando l'ordine viene effettuato.

## Ciclo di Vita delle Commissioni

Ogni commissione passa attraverso una serie di stati dal momento della creazione al pagamento:

```
In sospeso → Approvato → Pagato
   ↓
Rifiutato
```

### Definizioni degli Stati

| Stato | Descrizione | Cosa accade |
|--------|-------------|--------------|
| **In sospeso** | Ordine effettuato, commissione in attesa di revisione | La commissione è creata ma non è ancora confermata. L'affiliato può vederla ma non può ritirare i fondi. |
| **Approvato** | Mercante conferma che l'acquisto è valido | La commissione è verificata e aggiunta al saldo disponibile dell'affiliato. E' eleggibile per il pagamento. |
| **Rifiutato** | Mercante rifiuta la commissione | La commissione è negata (es. ordine rimborsato, frode o violazione dei termini). Non è eleggibile per il pagamento. |
| **Pagato** | La commissione è inclusa in un pagamento completato | L'affiliato è stato pagato. La commissione è finalizzata e non può essere modificata. |

![Elenco delle Commissioni](/static/core/admin/img/help/commission-management/commission-list.webp)

## Quando Vengono Create le Commissioni

Le commissioni vengono create automaticamente seguendo questa sequenza:

1. **Cliente clicca sul link dell'affiliato** — L'URL di riferimento contiene il codice di tracciamento unico dell'affiliato (es. `?ref=JOHNSMITH`)
2. **Viene impostato un cookie** — Un cookie di tracciamento viene memorizzato nel browser del cliente con il codice dell'affiliato
3. **Acquisto entro la validità del cookie** — Il cliente completa un ordine prima che il cookie scada (predefinito: 30 giorni)
4. **Il sistema attribuisce l'ordine** — Spwig controlla la presenza di un cookie di tracciamento attivo e identifica l'affiliato che ha riferito il cliente
5. **Creazione automatica della commissione** — Viene generato un registro della commissione con lo stato **In sospeso**

La commissione viene creata **immediatamente** quando l'ordine viene effettuato, anche prima che venga confermato il pagamento. Questo permette ai commercianti di revisionare le commissioni mentre gli ordini vengono elaborati.

## Tracciamento e Attribuzione

Spwig utilizza il modello **last-click** per determinare a quale affiliato attribuire un acquisto.

### Funzionamento dell'Attribuzione

- **Modello last-click** — L'ultimo link cliccato dall'affiliato riceve il credito (anche se più affiliati hanno riferito il cliente)
- **Tracciamento basato su cookie** — Un cookie memorizza il codice dell'affiliato nel browser del cliente
- **Durata del cookie** — Determina la finestra di tempo durante la quale un acquisto può essere attribuito (configurabile per programma, tipicamente 30 giorni)
- **Tracciamento IP e sessione** — Dati aggiuntivi aiutano a identificare schemi fraudolenti

### Esempio di Attribuzione

- Giorno 1: Il cliente clicca sul link dell'affiliato A → Cookie impostato per l'affiliato A
- Giorno 5: Il cliente clicca sul link dell'affiliato B → Cookie **aggiornato** all'affiliato B (vince il last-click)
- Giorno 7: Il cliente effettua un ordine → La commissione va a **l'affiliato B**

Se il cliente torna il Giorno 35 (dopo che il cookie è scaduto) e effettua un ordine, **nessuna commissione** viene creata perché la finestra di tracciamento è chiusa.

## Dettagli delle Commissioni

Naviga a **Marketing > Commissioni** per visualizzare tutti i registri delle commissioni.

### Campi delle Commissioni

Ogni commissione visualizza:

| Campo | Descrizione |
|-------|-------------|
| **Affiliato** | Nome e codice dell'affiliato |
| **Programma** | Nome del programma degli affiliati |
| **Ordine** | Numero dell'ordine (collegamento cliccabile per visualizzare i dettagli completi dell'ordine) |
| **Importo** | Valore della commissione calcolato |
| **Stato** | Fase corrente (In sospeso, Approvato, Rifiutato, Pagato) |
| **Creato** | Quando è stata generata la commissione |
| **Data di Approvazione/Rifiuto** | Quando lo stato è stato aggiornato |
| **Data di Pagamento** | Quando è stato processato il pagamento |
| **Note** | Note interne sulla commissione |

### Visualizzazione dei Dettagli dell'Ordine

Clicca sul **numero dell'ordine** nel registro della commissione per visualizzare l'ordine originale. Questo ti permette di verificare:
- Totale dell'ordine e articoli acquistati
- Informazioni sul cliente
- Stato del pagamento
- Stato della spedizione
- Rimborsi o resi

Questo contesto ti aiuta a decidere se approvare o rifiutare la commissione.

## Gestione delle Commissioni

Sebbene questa guida si concentri su comprendere le commissioni, i passaggi pratici per approvare, rifiutare e pagare le commissioni vengono trattati in dettaglio nell'argomento di aiuto **Gestione delle Commissioni**.

### Panoramica Rapida

- **Approvare** — Verifica che l'ordine sia legittimo e conferma che la commissione sia valida
- **Rifiutare** — Rifiuta le commissioni per ordini fraudolenti, rimborsi o violazioni delle politiche
- **Aggiungere note** — Documenta le ragioni per l'approvazione o il rifiuto per riferimento futuro
- **Elaborare i pagamenti** — Raggruppa le commissioni approvate in pagamenti di batch

Consulta gli argomenti di aiuto correlati per le istruzioni passo-passo su ogni compito di gestione.

## Consigli

- Rivedi le commissioni in sospeso **ogni giorno** durante il primo mese per stabilire un ritmo e individuare eventuali problemi di tracciamento fin dall'inizio
- Configura **notifiche via email** per essere avvisato quando vengono create nuove commissioni in modo da poterle rivedere mentre i dettagli dell'ordine sono freschi
- Approva le commissioni **dopo la consegna dell'ordine** (non immediatamente all'effettuazione dell'ordine) per considerare le annullamenti e i resi
- Utilizza il **campo note** per documentare le decisioni, specialmente per le commissioni rifiutate, in modo da avere un registro se gli affiliati fanno domande
- Cerca **pattern di rifiuto** — se un affiliato ha molte commissioni rifiutate, potrebbe indicare frode o malinteso sui termini del programma
- Considera la creazione di una **policy di approvazione delle commissioni** (es. "approvate dopo la finestra di restituzione di 14 giorni") e comunicala agli affiliati per stabilire aspettative chiare