---
title: Piani di abbonamento
---

I piani di abbonamento ti consentono di offrire addebiti ricorrenti per i tuoi prodotti: ideali per prodotti di consumo, servizi, box curate o qualsiasi prodotto che i clienti acquistano ripetutamente. Questa guida spiega come creare e configurare i piani, impostare i livelli di prezzo, aggiungere periodi di prova e collegare accessori opzionali.

## Per iniziare

Passa a **Abbonamenti > Piani di abbonamento** nella barra laterale amministrativa. L'elenco dei piani mostra tutti i tuoi piani con il modello di prezzo, il numero di abbonati attivi e lo stato di visibilità.

Per creare un nuovo piano, fai clic sul pulsante **+ Aggiungi un piano di abbonamento** - questo apre la procedura guidata per la creazione del piano, che ti guida passo dopo passo alla configurazione.

![Elenco dei piani di abbonamento](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Un piano da solo non è acquistabile: è un modello. Una volta che lo hai creato qui, collegalo a uno o più prodotti dal tab **Abbonamenti** del prodotto (esclusivi per prodotti semplici, variabili e digitali), in modo che i clienti possano effettivamente iscriversi. Vedere [Vendere prodotti come abbonamenti](/help/selling-products-as-subscriptions) per questo passaggio.

## Informazioni sul piano

La prima sezione cattura l'identità principale del tuo piano.

- **Nome del piano** - Il nome che i clienti vedono quando si iscrivono. Fai clic sull'icona del globo per aggiungere le traduzioni per le altre lingue del negozio.
- **Slug** - Un identificatore amichevole per le URL generato automaticamente dal nome (es. `piano-premium`). Viene utilizzato internamente e negli integratori.
- **Descrizione** - Testo opzionale che descrive cosa include il piano. Supporta le traduzioni.

## Modello di prezzo

Scegli come strutturare i prezzi per questo piano:

| Modello di prezzo | Ideale per |
|------------------|-------------|
| **Prezzo a livelli** | Offrire opzioni di impegno mensile, trimestrale e annuale con sconti per periodi più lunghi |
| **Prezzo in base alla quantità** | Prezzo per utente o posto dove il totale si adatta alla quantità (es. licenze per team) |
| **Prezzo fisso** | Un unico prezzo fisso senza variazioni |

Per i piani a **Prezzo in base alla quantità**, imposta la **Quantità minima** (posti richiesti minimi) e, opzionalmente, una **Quantità massima** per limitare il numero di posti che un abbonato può acquistare.

## Livelli di prezzo

I livelli di prezzo definiscono la frequenza di addebitamento e le opzioni di sconto disponibili ai clienti su questo piano. Aggiungili nella sezione **Livelli di prezzo** qui sotto il modulo principale.

Ogni livello ha questi campi:

- **Nome del livello** - L'etichetta visualizzata ai clienti (es. `Mensile`, `Annuale - Risparmia 20%`). Supporta le traduzioni.
- **Ciclo di fatturazione** - Quanti spesso il cliente viene addebitato: Giornaliero, Setimanale, Mensile, Trimestrale, Semestrale o Annuale.
- **Intervallo di fatturazione** - Il moltiplicatore per il ciclo di fatturazione. Impostalo a `2` con il Mensile per fatturare ogni 2 mesi.
- **Percentuale di sconto** - Lo sconto applicato al prezzo del prodotto per questo livello. Impostalo a `0` per il prezzo pieno, oppure a `20` per ottenere uno sconto del 20%. Questo sconto si sovrappone a qualsiasi prezzo in saldo sul prodotto stesso.
- **Livello predefinito** - Contrassegna un livello come predefinito per selezionarlo automaticamente per i clienti quando guardano le opzioni di abbonamento.

Lo sconto si applica a partire dal primo ciclo di fatturazione del cliente, non solo sui rinnovi - un livello con uno sconto del 20% addebiterà lo sconto del 20% fin dal primo giorno (o dal primo addebito dopo un periodo di prova, se il piano ne ha uno).

### Esempio: piano a livelli con tre opzioni

Per un piano di abbonamento "Coffee Club":

| Nome del livello | Ciclo di fatturazione | Sconto |
|----------------|----------------------|--------|
| Mensile | Mensile | 0% |
| Trimestrale - Risparmia 10% | Trimestrale | 10% |
| Annuale - Risparmia 20% | Annuale | 20% |

## Periodo di prova

Un periodo di prova permette ai clienti di provare il tuo abbonamento prima del primo addebito completo. Configuralo nella sezione **Periodo di prova**:

- **Periodo di prova (giorni)** - Numero di giorni di prova gratuiti. Imposta a `0` per disabilitare le prove. Il massimo è 365 giorni.
- **Prezzo di prova** - Prezzo ridotto opzionale durante la prova (es. $1 per il primo mese). Lascia vuoto per un periodo di prova completamente gratuito.

## Policy di annullamento

Controlla come i clienti possono annullare il loro abbonamento nella sezione **Policy di annullamento**:

| Policy | Descrizione |
|--------|-------------|
| **Annulla in qualsiasi momento** | I clienti possono annullare immediatamente in qualsiasi momento |
| **Annulla alla fine del periodo** | L'annullamento diventa effettivo alla fine del periodo pagato — i clienti mantengono l'accesso fino alla scadenza |
| **Obbligo minimo richiesto** | I clienti devono completare un numero minimo di cicli di fatturazione prima di annullare |

Ulteriori impostazioni:

- **Obbligo minimo (cicli)** — Quando si utilizza il piano di impegno, impostare il numero richiesto di cicli di fatturazione (es. `3` per un obbligo minimo di 3 mesi).
- **Periodo di tolleranza (giorni)** — Giorni di accesso continuo dopo un fallimento del pagamento prima che la sottoscrizione venga sospesa. Impostare su `0` per la sospensione immediata.
- **Periodo di riacquisto (giorni)** — Giorni dopo l'annullamento durante i quali un cliente può riprendere la propria sottoscrizione senza dover riscrivere da capo.

## Comportamento modifica piano

Quando i clienti passano da un piano all'altro, puoi controllare quando avviene la modifica:

- **Comportamento aggiornamento** — Imposta su **Immediato** (addebita importo proporzionato adesso) o **All'aggiornamento** (cambia alla data di fatturazione successiva).
- **Comportamento riduzione** — Imposta su **Immediato** (applica credito sulla prossima bolletta) o **All'aggiornamento** (cambia alla data di fatturazione successiva).

## Limiti e restrizioni

- **Cicli di fatturazione massimi** — Il numero totale di cicli di fatturazione prima che la sottoscrizione si concluda automaticamente. Lasciare vuoto per una fatturazione ricorrente illimitata. Utile per piani a rate o sottoscrizioni con scadenza temporanea.
- **Fee di attivazione** — Un addebito unico riscosso quando la sottoscrizione viene creata per la prima volta (es. tariffa di accoglienza o attivazione). Impostare su `0.00` per nessuna tariffa di attivazione.

## Aggiunte al piano

Le aggiunte sono opzioni extra che i sottoscrittori possono collegare al loro piano. Aggiungile nella sezione **Aggiunte al piano**:

- **Nome aggiunta** — Il nome visualizzato ai clienti. Supporta le traduzioni.
- **Descrizione** — Cosa fornisce l'aggiunta.
- **Prezzo** — Costo dell'aggiunta.
- **Frequenza di fatturazione** — Se l'aggiunta viene addebitata **Per ciclo di fatturazione** (ricorrente) o **Unica volta** all'inizio della sottoscrizione.
- **Consenti quantità** — Attiva per consentire ai clienti di acquistare più unità dell'aggiunta.
- **Obbligatorio** — Seleziona questa opzione per includere automaticamente l'aggiunta su tutte le nuove sottoscrizioni. Le aggiunte obbligatorie non possono essere rimosse dal cliente.

## Visibilità e stato

- **Attivo** — Deseleziona per disattivare un piano in modo che non possano essere create nuove sottoscrizioni. Le sottoscrizioni esistenti non sono interessate.
- **Pubblico** — Deseleziona per nascondere il piano dalle pagine visibili ai clienti (utile per piani interni o obsoleti che i sottoscrittori esistenti mantengono).
- **Ordine di visualizzazione** — Controlla l'ordine di visualizzazione sulle pagine di selezione delle sottoscrizioni. I numeri più bassi appaiono per primi.

## Suggerimenti

- Usa un **periodo di prova** per ridurre l'esitazione — anche una breve prova gratuita di 7 giorni può migliorare significativamente i tassi di conversione per i prodotti a sottoscrizione.
- Configura **tre livelli di prezzo** (mensile, trimestrale, annuale) con sconti crescenti per incoraggiare gli impegni annuali e migliorare il tuo flusso di cassa.
- Per le sottoscrizioni basate sui servizi, imposta **Policy di annullamento** su **Annulla alla fine del periodo** in modo che i clienti mantengano l'accesso durante il loro periodo pagato — questo sembra equo e riduce i rimborssi.
- Mantieni il **Periodo di tolleranza** tra 3-7 giorni per i fallimenti di pagamento. Questo dà ai clienti il tempo di aggiornare il loro metodo di pagamento prima di perdere l'accesso.
- Usa l'indicatore **Obbligatorio** sugli accessori con moderazione — usalo solo per cose che sono veramente obbligatorie (es. un accordo di servizio), non come modo per aumentare i prezzi.
- Disattiva i piani senza sottoscrittori invece di cancellarli — questo preserva i dati storici per qualsiasi cliente che si è precedentemente sottoscritto.