---
title: Gestione di Spostamenti POS e Cassa
---

I turni POS tracciano i periodi di lavoro del cassiere e assicurano un conto corretto della cassa. Ogni turno rappresenta il tempo in cui un singolo cassiere opera su un terminale, dall'apertura del cassetto con un conteggio iniziale del denaro all'uscita del turno con un conteggio finale e una conciliazione. Il sistema calcola automaticamente il denaro previsto in base alle vendite effettive e lo confronta con il conteggio fisico, evidenziando le discrepanze per un'indagine. I movimenti di denaro durante i turni (aggiunte di float, prelievi di cassa piccola) vengono tracciati con motivazioni per un completo registro delle operazioni.

Naviga in **POS > Turni** per visualizzare tutti i turni, monitorare i turni attivi, rivedere i report di conciliazione della cassa e verificare l'attività storica.

![Elenco dei turni](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Comprendere i turni POS

Un turno è un periodo di lavoro durante il quale un singolo cassiere opera su un terminale. I turni garantiscono la responsabilità del denaro: ogni cassiere è responsabile del denaro nel cassetto durante il suo turno.

**Ciclo di vita del turno**:
1. **Apertura** - Il cassiere inizia il turno, conta il denaro iniziale, registra l'importo
2. **Durante il turno** - Elabora vendite, accetta pagamenti, emette rimborshi
3. **Chiusura** - Il cassiere conta il denaro, registra l'importo finale, il sistema calcola la discrepanza
4. **Conciliato** - Il turno è finalizzato e bloccato per scopi di audit

**Metriche principali tracciate**:
- **Denaro iniziale** - Importo iniziale nel cassetto all'inizio del turno
- **Denaro finale** - Denaro fisico nel cassetto alla fine del turno
- **Denaro previsto** - Calcolato: Denaro iniziale + vendite in contanti - rimborshi in contanti + movimenti di denaro
- **Discrepanza del denaro** - Discrepanza: Denaro finale - denaro previsto (positivo = eccesso, negativo = mancanza)
- **Totale vendite** - Somma di tutte le transazioni di vendita durante il turno
- **Totale rimborshi** - Somma di tutte le transazioni di rimborso durante il turno
- **Conteggio delle transazioni** - Numero di ordini elaborati

## Visualizzazione dell'elenco dei turni

L'elenco dei turni visualizza tutti i turni con informazioni chiave:

**Stato del turno**:
- **Aperto** (badge verde) - turno attivo
- **Chiuso** (badge grigio) - turno completato
- **Conciliato** (badge blu) - finalizzato e bloccato per l'audit

**Terminale** - Quale terminale POS era utilizzato per il turno

**Cassiere** - Membro dello staff che ha lavorato il turno

**Denaro iniziale** - Importo iniziale

**Denaro finale** - Importo finale (vuoto se il turno è ancora aperto)

**Denaro previsto** - Importo previsto calcolato dal sistema in base alle transazioni

**Discrepanza del denaro** - Discrepanza (evidenziata in rosso se negativa, verde se positiva, nera se zero)

**Durata** - Lunghezza del turno (ora di inizio all'ora di fine)

**Totale vendite** - Ricavi generati durante il turno

Utilizza i filtri per visualizzare:
- Solo i turni aperti (monitorare i terminali attivi)
- I turni con discrepanze (discrepanza del denaro ≠ 0)
- I turni per intervallo di date (report di conciliazione giornaliera)
- I turni per cassiere (audit delle prestazioni)

## Apertura di un turno

I cassieri aprono i turni direttamente dal terminale POS (non possono essere aperti dall'amministrazione). Il flusso di lavoro sul terminale:

1. **Staff si autentica** - Inserisce le credenziali per accedere al terminale

2. **Conta il denaro iniziale** - Conta fisicamente tutto il denaro nel cassetto (banconote e monete)

3. **Inserisci l'importo iniziale** - Registra l'importo contato nell'app POS

4. **Inizia il turno** - Il terminale è pronto per elaborare le vendite

**Linee guida per il denaro iniziale**:
- Il denaro iniziale standard (float) è tipicamente $100-$300 a seconda della dimensione del negozio
- Conta due volte per garantire l'accuratezza - gli errori all'apertura si propagano alle discrepanze alla chiusura
- Se il cassetto è vuoto, il denaro iniziale è $0.00 (float aggiunto tramite movimento di denaro)
- Documenta le banconote di grandi tagli (>$50) separatamente per tracciare i loro movimenti

![Form per l'aggiunta di un turno](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Durante il turno

Mentre il turno è aperto, il sistema traccia automaticamente:

**Vendite in contanti** - Qualsiasi transazione in cui il cliente paga con denaro fisico (aggiunge al denaro previsto)

**Rimborsi in contanti** - Qualsiasi rimborso emesso in contanti (sottrae dal denaro previsto)

**Vendite con carta** - Transazioni con carta di credito/debito (nessun impatto sul denaro)

**Pagamento misto** - Parte in contanti + parte con carta (solo la parte in contanti influisce sul denaro previsto)

**Carte regalo e buoni** - Metodi di pagamento non in contanti (nessun impatto sul denaro)

I cassieri continuano a elaborare le vendite normalmente. Il sistema mantiene un calcolo in corso del denaro previsto in background.

## Movimenti del denaro

I movimenti del denaro sono aggiustamenti al cassetto durante un turno:

**Aggiunta di float** - Aggiunta di denaro al cassetto:
- Motivo: "Aggiunta di resto per banconote di grandi tagli"
- Importo: +$100.00
- Denaro previsto aumenta di $100.00

**Prelievi di cassa piccola** - Rimozione di denaro per spese:
- Motivo: "Acquisto di materiali per ufficio"
- Importo: -$25.00
- Denaro previsto diminuisce di $25.00

**Depositi bancari** - Rimozione di denaro in eccesso per motivi di sicurezza:
- Motivo: "Deposito in cassaforte - più di $500 nel cassetto"
- Importo: -$300.00
- Denaro previsto diminuisce di $300.00

**Registrazione dei movimenti del denaro sul terminale**:
1. Tocca **Menu** > **Movimento del denaro**
2. Seleziona il tipo: Aggiungi o Rimuovi
3. Inserisci l'importo
4. Inserisci il motivo (richiesto per il registro delle operazioni)
5. Conferma

Tutti i movimenti del denaro appaiono nel rapporto dettagliato del turno con orari, importi e motivi.

## Chiusura di un turno

Quando un cassiere termina il periodo di lavoro, chiude il turno:

1. **Tocca Chiudi turno** - Nel menu del terminale

2. **Elabora le transazioni rimanenti** - Completare eventuali carrelli parcheggiati o vendite in sospeso

3. **Conta il denaro finale** - Conta fisicamente tutto il denaro nel cassetto
   - Conta le banconote per denominazione ($100s, $50s, $20s, $10s, $5s, $1s)
   - Conta le monete per tipo (quarti, decimi, nichel, centesimi)
   - Totale = importo finale del denaro

4. **Inserisci l'importo finale** - Registra il totale contato

5. **Il sistema calcola la discrepanza**:
   - Denaro previsto = Denaro iniziale + vendite in contanti - rimborshi in contanti + movimenti di denaro
   - Discrepanza del denaro = Denaro finale - denaro previsto
   - Esempio: Denaro finale $485.00 - Denaro previsto $480.00 = +$5.00 eccesso

6. **Rivedi la discrepanza** - Il terminale visualizza la differenza:
   - **Esatto ($0.00)** - Conciliazione perfetta
   - **Eccesso piccolo (+$1 a +$5)** - Arrotondamento accettabile o mancia del cliente
   - **Mancanza piccola (-$1 a -$5)** - Errore di conteggio minore, accettabile
   - **Discrepanza grande (>$5)** - Richiesta di riconteggio

7. **Riconteggio se necessario** - Se la discrepanza è grande (>$10), il cassiere deve riconteggiare il denaro finale prima di finalizzare

8. **Finalizza il turno** - Conferma l'importo finale, lo stato del turno cambia in "Chiuso"

9. **Stampa il rapporto del turno** - Il terminale stampa un ricevuta di conciliazione del denaro per i registri del cassiere

![Dettaglio del turno](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Formula di conciliazione del denaro

Il sistema calcola il denaro previsto utilizzando questa formula:

```
Denaro previsto = Denaro iniziale
                + Vendite in contanti
                - Rimborshi in contanti
                + Aggiunte di denaro (movimenti)
                - Rimozioni di denaro (movimenti)
```

**Esempio**:
- Denaro iniziale: $200.00
- Vendite in contanti: $450.00 (da 15 transazioni)
- Rimborshi in contanti: -$30.00 (1 rimborso)
- Aggiunta di denaro: +$100.00 (float aggiunto durante il turno)
- Rimozione di denaro: -$50.00 (prelievo di cassa piccola)
- **Denaro previsto: $200 + $450 - $30 + $100 - $50 = $670.00**

Se il cassiere conta $675.00 alla chiusura:
- Discrepanza del denaro: $675.00 - $670.00 = **+$5.00 eccesso**

## Rapporti e audit dei turni

I rapporti dei turni forniscono informazioni dettagliate sulla conciliazione:

**Sezione riassuntiva**:
- Denaro iniziale e finale
- Calcolo del denaro previsto
- Discrepanza del denaro (eccesso/mancanza)
- Totale vendite e rimborshi
- Conteggio delle transazioni
- Durata del turno

**Dettaglio delle transazioni**:
- Tutte le vendite durante il turno (ID ordine, importi, metodi di pagamento)
- Tutti i rimborshi emessi
- Orario di ogni transazione

**Registro dei movimenti del denaro**:
- Tutte le aggiunte e rimozioni
- Motivi forniti
- Orari

**Utilizzo**:
- **Conciliazione giornaliera** - Rivedere tutti i turni alla fine del giorno di lavoro
- **Prestazioni del cassiere** - Identificare modelli di discrepanze per membro dello staff
- **Rilevamento di furti** - Mancanze grandi e costanti possono indicare furti
- **Necessità di formazione** - Discrepanze frequenti piccole suggeriscono problemi di accuratezza nel conteggio
- **Registro delle operazioni** - Registri completi per scopi contabili e fiscali

## Gestione della cassa con più terminali

Per i negozi con più terminali che eseguono turni contemporanei:

**Cassetti separati**: Ogni terminale ha il proprio cassetto di cassa - i turni sono indipendenti. Il cassiere A sul Terminale 1 e il cassiere B sul Terminale 2 eseguono turni separati con conciliazione separata.

**Cassetto condiviso**: Alcuni negozi condividono un unico cassetto tra più terminali (non raccomandato). Se si fa così:
- Solo un turno può essere aperto per cassetto condiviso alla volta
- I cassieri devono chiudere il turno quando passano a un altro cassiere
- I movimenti del denaro registrano tutte le aggiunte/rimozioni durante i passaggi
- Le discrepanze sono più difficili da attribuire a cassieri specifici

**Pratica consigliata**: Un cassetto per terminale, un turno per cassiere per sessione. Questo garantisce una responsabilità chiara e una conciliazione semplificata.

## Gestione delle discrepanze

Quando il denaro chiuso non corrisponde al denaro previsto:

**Discrepanze piccole (<$5)**:
- Accettabili a causa di arrotondamenti, errori di conteggio o mancie dei clienti
- Documenta nel registro del turno
- Nessun'azione ulteriore necessaria a meno che non emerga un modello

**Discrepanze medie ($5-$20)**:
- Riconteggio del denaro prima di finalizzare il turno
- Rivedi il registro delle transazioni per errori (cambio errato, transazione annullata non elaborata)
- Documenta le circostanze nel registro del turno
- Consigliato un controllo da parte del manager

**Discrepanze grandi (>$20)**:
- Riconteggio obbligatorio
- Approvazione del manager richiesta per chiudere il turno
- Rivedi tutte le transazioni e i movimenti del denaro
- Indaga le possibili cause (furto, accesso al cassetto, importo iniziale errato)
- Potrebbe essere necessaria un'azione disciplinare a seconda delle circostanze

**Mancanze costanti**:
- Modello di discrepanze negative dallo stesso cassiere = problema di formazione o furto
- Implementa un controllo aggiuntivo (controllo casuale del manager durante il turno)
- Rivedi le procedure di formazione POS
- Considera aggiornamenti delle politiche di gestione del denaro

## Consigli

- **Conta il denaro iniziale due volte** - Gli errori all'apertura si propagano alle discrepanze alla chiusura; l'accuratezza all'inizio previene i problemi alla fine
- **Registra i movimenti del denaro immediatamente** - Non aspettare la chiusura per documentare le aggiunte di float o prelievi di cassa piccola
- **Fornisci sempre motivi per i movimenti** - "Aggiunto $100" è inutile per l'audit; "Aggiunto $100 per resto (pochi $5)") è un'azione utile
- **Riconteggio se la discrepanza è >$10** - Non finalizzare il turno con una grande discrepanza senza riconteggio
- **Stampa i rapporti dei turni quotidianamente** - Allegate ai documenti di conciliazione giornaliera per i conti
- **Rivedi i modelli, non le discrepanze individuali** - Un mancato $3.00 è normale; cinque mancanze consecutive di $3.00 sono un problema
- **Chiudi i turni alla fine della giornata** - Non lasciare i turni aperti durante la notte; le discrepanze sono più facili da investigare quando sono recenti
- **Forma i cassieri al conteggio per denominazione** - La maggior parte degli errori proviene da un conteggio errato delle banconote (pensare che una $5 sia una $10)
- **Utilizza buste per monete** - Le monete pre-confezionate riducono gli errori di conteggio e accelerano la conciliazione

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.