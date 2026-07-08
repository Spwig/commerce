---
title: Gestione delle Commissioni
---

La gestione delle commissioni è il processo di revisione e approvazione degli utili degli affiliati per assicurarsi che vengano creditati solo vendite legittime. Questa guida mostra come revisionare le commissioni in sospeso, approvare quelle valide, rifiutare ordini fraudolenti o restituiti e gestire le commissioni in modo efficiente utilizzando azioni di massa.

## Dashboard delle Commissioni

Accedi a **Marketing > Commissioni** per accedere alla dashboard di gestione delle commissioni.

La dashboard fornisce un riepilogo dell'attività delle commissioni in tutti i programmi di affiliazione:

| Statistica | Descrizione |
|-----------|-------------|
| **Commissioni in sospeso** | Numero di commissioni in attesa della tua revisione |
| **Commissioni approvate** | Commissioni confermate e pronte per il pagamento |
| **Commissioni pagate** | Commissioni che sono state pagate agli affiliati |
| **Commissioni rifiutate** | Commissioni rifiutate a causa di frode, restituzioni o violazioni delle policy |
| **Importo in sospeso** | Valore totale delle commissioni approvate ma non pagate |

Queste statistiche ti aiutano a monitorare il tuo carico di lavoro di revisione e a controllare l'impatto finanziario del tuo programma di affiliazione.

![Dashboard delle Commissioni](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Visualizzazione delle Commissioni

L'elenco delle commissioni visualizza tutti i record delle commissioni in ordine cronologico.

### Colonne dell'Elenco

| Colonna | Descrizione |
|--------|-------------|
| **Affiliato** | Nome e codice univoco dell'affiliato |
| **Programma** | Il programma di affiliazione che ha generato questa commissione |
| **Ordine** | Numero dell'ordine (clicca per visualizzare i dettagli completi dell'ordine) |
| **Importo** | Valore della commissione in valuta del tuo negozio |
| **Stato** | In sospeso, Approvato, Rifiutato o Pagato |
| **Creato** | Quando è stata generata la commissione |

### Filtrare le Commissioni

Utilizza il pannello laterale di filtro per restringere le commissioni:

- **Per Stato** — Mostra solo le commissioni in sospeso, approvate, rifiutate o pagate
- **Per Affiliato** — Visualizza le commissioni per un partner specifico
- **Per Programma** — Vedi le commissioni da un programma di affiliazione specifico
- **Per Intervallo di Data** — Filtra per data di creazione

### Ricerca delle Commissioni

Utilizza la barra di ricerca per trovare commissioni specifiche:

- Inserisci un **numero di ordine** per trovare una commissione per una vendita specifica
- Inserisci un **codice affiliato** per visualizzare tutte le commissioni per un unico partner

## Dettagli della Commissione

Fai clic su qualsiasi commissione nell'elenco per visualizzare i suoi dettagli completi.

### Campi dei Dettagli

La vista dettagliata mostra:

- **Informazioni sull'ordine** — Fai clic sul numero dell'ordine per visualizzare l'ordine completo in una nuova scheda, inclusi gli articoli, l'indirizzo di spedizione, lo stato del pagamento e i dettagli del cliente
- **Informazioni sull'affiliato** — Nome, codice, email di pagamento e stato dell'appartenenza al programma dell'affiliato
- **Dettagli del Programma** — Nome del programma, tipo di commissione (percentuale o fisso) e tasso di commissione
- **Timestamp** — Data di creazione, data di approvazione/rifiuto e data di pagamento
- **Sezione delle Note** — Note interne visibili solo ai commercianti (spiegato di seguito)

Queste informazioni ti aiutano a verificare la legittimità della commissione prima di approvarla.

## Approvare le Commissioni

Approvare una commissione conferma che è valida e la aggiunge al saldo disponibile dell'affiliato, rendendola eleggibile per il pagamento.

### Quando Approvare

Approva le commissioni quando:

- **Ordine completato con successo** — Prodotto spedito o beni digitali consegnati
- **Nessun ritorno o rimborso** — Il cliente non ha richiesto un ritorno (considera di attendere 14-30 giorni dopo la consegna)
- **Standard di qualità rispettati** — La vendita rispetta i termini del tuo programma (es. non un'autoreferenza, il cliente ha utilizzato un metodo di pagamento autentico)
- **Nessuna frode rilevata** — L'ordine supera il controllo antifrode (verifica IP, discrepanza tra indirizzo di fatturazione/spedizione, modelli di ordine insoliti)

### Come Approvare

**Approvazione di una singola commissione:"

1. Accedi a **Marketing > Commissioni**
2. Fai clic sulla commissione che desideri approvare
3. Fai clic sul pulsante **Approva** in alto nella pagina dei dettagli
4. Opzionalmente aggiungi una nota (es. "Approvata dopo la consegna riuscita")
5. Lo stato cambia in **Approvato** e la commissione viene aggiunta al saldo dell'affiliato

**Approvazione di massa:"

1. Accedi a **Marketing > Commissioni**
2. Seleziona le caselle accanto alle commissioni che desideri approvare
3. Seleziona **Approva selezionati** dal menu a discesa **Azioni**
4. Fai clic su **Vai**
5. Tutte le commissioni selezionate cambiano nello stato **Approvato**

Le commissioni approvate appaiono nel dashboard dell'affiliato come saldo disponibile e possono essere incluse nel prossimo batch di pagamento.

## Rifiutare le Commissioni

Rifiutare una commissione la rimuove dal saldo dell'affiliato e la marca come non eleggibile per il pagamento.

### Quando Rifiutare

Rifiuta le commissioni quando:

- **Ordine fraudolento** — L'ordine mostra segni di frode (metodo di pagamento rubato, discrepanza IP, affiliato che utilizza il proprio link)
- **Cliente ha restituito il prodotto** — Il cliente ha restituito gli articoli per un rimborso completo
- **Problemi di qualità** — La vendita non rispetta i termini del programma (es. l'affiliato ha violato le linee guida di pubblicità)
- **Violazione dei termini** — L'affiliato ha utilizzato metodi di promozione vietati (spam, battaglia di marchi, riempimento dei cookie)
- **Ordine annullato** — Il cliente ha annullato prima della consegna

### Come Rifiutare

**Rifiuto di una singola commissione:"

1. Accedi a **Marketing > Commissioni**
2. Fai clic sulla commissione che desideri rifiutare
3. Fai clic sul pulsante **Rifiuta** in alto nella pagina dei dettagli
4. **Aggiungi una nota** che spiega il motivo (altamente raccomandato per la risoluzione delle dispute)
5. Lo stato cambia in **Rifiutato**

**Rifiuto di massa:"

1. Accedi a **Marketing > Commissioni**
2. Seleziona le caselle accanto alle commissioni che desideri rifiutare
3. Seleziona **Rifiuta selezionati** dal menu a discesa **Azioni**
4. Fai clic su **Vai**
5. Tutte le commissioni selezionate cambiano nello stato **Rifiutato**

Le commissioni rifiutate vengono rimosse dal saldo dell'affiliato e non possono essere pagate. Rimangono visibili nella cronologia delle commissioni per la documentazione.

## Azioni di Massa

Le azioni di massa ti permettono di approvare o rifiutare più commissioni contemporaneamente, risparmiando tempo quando si gestiscono grandi lotti.

### Utilizzo delle Azioni di Massa

1. Accedi a **Marketing > Commissioni**
2. Filtra l'elenco per mostrare solo le commissioni che desideri processare (es. filtra per stato **In sospeso**)
3. Seleziona la casella accanto a ciascuna commissione, o fai clic sulla casella del titolo per selezionare tutte su questa pagina
4. Scegli un'azione dal menu a discesa **Azioni**:
   - **Approva selezionati** — Marchia tutte le commissioni selezionate come approvate
   - **Rifiuta selezionati** — Marchia tutte le commissioni selezionate come rifiutate
5. Fai clic su **Vai**
6. Controlla il messaggio di conferma che mostra quante commissioni sono state aggiornate

### Elaborazione di Massa Efficiente

- **Filtra per programma** — Approva tutte le commissioni da un affiliato di alto rendimento attendibile in una volta
- **Filtra per intervallo di data** — Processa le commissioni più vecchie di 14 giorni (oltre il tuo periodo di restituzione)
- **Rivedi separatamente quelle ad alto valore** — Utilizza le azioni di massa per le commissioni piccole, rivedi manualmente quelle di grandi dimensioni

## Note sulle Commissioni

Il campo delle note ti permette di documentare le tue decisioni e comunicare con il tuo team.

### Aggiungere Note

Le note possono essere aggiunte:

- **Durante l'approvazione** — Fai clic sulla commissione, aggiungi una nota nel campo Note, quindi fai clic su **Approva**
- **Durante il rifiuto** — Aggiungi una nota che spiega il motivo del rifiuto
- **In qualsiasi momento** — Fai clic sulla commissione, aggiungi o modifica la nota nel campo Note e salva

### Quando Utilizzare le Note

- **Commissioni rifiutate** — Documenta sempre il motivo ("Il cliente ha restituito l'ordine #12345 il 2/10/26")
- **Commissioni ad alto valore** — Nota i passaggi di verifica effettuati ("Verificata la consegna tramite tracking #ABC123")
- **Commissioni contestate** — Documenta la comunicazione con l'affiliato
- **Pattern di frode** — Nota attività sospetta per riferimenti futuri

Le note sono **esclusivamente interne** — gli affiliati non possono vederle. Servono come strumento per la tua documentazione.

## Flusso delle Commissioni

Ecco il flusso completo di gestione delle commissioni:

```
Ordine effettuato → Commissione creata (In sospeso)
                      ↓
              Merchant Reviews
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Approvato     Rifiutato
                ↓           ↓
        Pronto per pagamento  Non pagabile
                ↓
        Incluso nel pagamento
                ↓
              Pagato
```

**Esempio del cronogramma:"

- **Giorno 1:** Cliente effettua un ordine di $100 tramite un link affiliato → commissione di $10 creata (In sospeso)
- **Giorno 15:** Ordine completato e passato il periodo di restituzione → merchant approva la commissione
- **Giorno 20:** Merchant elabora il batch di pagamento mensile → lo stato della commissione cambia in Pagato
- **Giorno 21:** Affiliato riceve il pagamento tramite PayPal

## Linee Guida

### Finestra di Revisione

Stabilisci un programma di revisione coerente:

- **Revisioni quotidiane** — Processa le commissioni in sospeso ogni mattina (raccomandato per i programmi ad alto volume)
- **Revisioni settimanali** — Riserva del tempo ogni lunedì per approvare le commissioni della settimana precedente
- **Revisioni bi-settimanali** — Allinea con il tuo programma di pagamento (approva le commissioni a metà mese, elabora i pagamenti alla fine del mese)

### Controlli di Qualità

Prima di approvare le commissioni, verifica:

1. **Ordine completato** — Controlla lo stato dell'ordine nell'amministrazione
2. **Pagamento confermato** — Verifica che il metodo di pagamento sia stato elaborato con successo
3. **Periodo di restituzione scaduto** — Aspetta 14-30 giorni dopo la consegna per considerare le restituzioni
4. **Nessun segnale di frode** — Controlla l'ordine per schemi sospetti (discrepanza tra indirizzi, paesi ad alto rischio, più ordini dallo stesso IP)
5. **Affiliato in buona fede** — Controlla la storia dell'affiliato per precedenti frodi o violazioni

### Prevenzione della Frode

Osserva questi segnali di allarme:

- **Autoreferimenti** — L'affiliato effettua ordini utilizzando il proprio link di tracciamento
- **Inserimento di cookie** — Rapporto di conversione abnormemente alto con valori di ordine bassi
- **Ordini duplicati** — Più ordini dallo stesso cliente/IP tramite lo stesso link affiliato
- **Discrepanza geolocalizzata** — L'affiliato nel Paese A che genera vendite esclusivamente nel Paese B
- **Ricariche** — Tasso elevato di ricariche su ordini riferiti dagli affiliati

Se rilevi frode, **rifiuta le commissioni** e considera la terminazione della membership del programma dell'affiliato.

### Comunicazione con gli Affiliati

- **Stabilisci aspettative** — Documenta chiaramente la tua politica di approvazione delle commissioni nei termini del programma
- **Sii trasparente** — Se rifiuti commissioni, considera l'invio di un'email all'affiliato che spieghi il motivo (usa le note come riferimento)
- **Rispondi alle contestazioni** — Se un affiliato contesta un rifiuto, rivedi le note e i dettagli dell'ordine
- **Pubblica le linee guida** — Crea una pagina "Policy di Approvazione delle Commissioni" nel tuo portale degli affiliati per evitare confusioni

## Consigli

- Approva le commissioni **dopo che il periodo di restituzione è chiuso** (tipicamente 14-30 giorni) per evitare di approvare ordini che i clienti restituiranno in seguito
- Utilizza **azioni di massa con filtri** per elaborare efficientemente le commissioni da affiliati attendibili, mentre rivedi manualmente nuovi o affiliati ad alto rischio
- Documenta i motivi del rifiuto nel **campo note** — questo ti protegge se un affiliato contesta la decisione e ti aiuta a identificare i pattern
- Presta attenzione ai **self-referrals** — è una violazione comune in cui gli affiliati utilizzano i propri link per guadagnare commissioni su acquisti personali
- Imposta un **threshold minimo di approvazione** — ad esempio, approva automaticamente le commissioni inferiori a $10 ma rivedi manualmente quelle superiori a $50 per bilanciare efficienza e rischio
- Crea un **checklist per la frode** — standardizza il tuo processo di revisione con un elenco di segnali di allarme (discrepanza IP, schemi di ordine sospetti, metodi di pagamento ad alto rischio)
- Monitora **i tassi di rifiuto per affiliato** — se un affiliato ha molti rifiuti, potrebbe indicare frode o la necessità di ulteriore formazione sui termini del programma