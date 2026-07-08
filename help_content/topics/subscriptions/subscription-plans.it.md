---
title: Piani di Abbonamento
---

I piani di abbonamento ti permettono di offrire un fatturazione ricorrente per i tuoi prodotti — ideale per prodotti consumabili, servizi, scatole curate o qualsiasi prodotto che i clienti acquistano ripetutamente. Questa guida spiega come creare e configurare i piani, impostare le fasce di prezzo, aggiungere periodi di prova e collegare opzioni aggiuntive.

## Getting started

Naviga verso **Subscriptions > Subscription Plans** nel sidebar dell'amministratore. L'elenco dei piani mostra tutti i tuoi piani con il loro modello di prezzo, il numero di abbonati attivi e lo stato di visibilità.

Per creare un nuovo piano, fai clic sul pulsante **+ Add Subscription Plan** — questo apre il wizard per la creazione del piano, che ti guida passo dopo passo nell'impostazione.

![Subscription plans list](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Plan information

La prima sezione cattura l'identità principale del tuo piano.

- **Plan Name** — Il nome che i clienti vedranno quando si iscrivono. Fai clic sull'icona della Terra per aggiungere traduzioni per altre lingue del negozio.
- **Slug** — Un identificatore amico degli URL generato automaticamente dal nome (es. `premium-plan`). Viene utilizzato internamente e nelle integrazioni.
- **Description** — Testo opzionale che descrive cosa include il piano. Supporta le traduzioni.

## Pricing model

Scegli come è strutturato il prezzo per questo piano:

| Pricing Model | Best For |
|---------------|----------|
| **Tiered Pricing** | Offrire opzioni di impegno mensile, trimestrale e annuale con sconti per termini più lunghi |
| **Quantity-Based** | Prezzo per postazione o per utente dove il totale si scala in base alla quantità (es. licenze per team) |
| **Flat Rate** | Un prezzo fisso unico senza variazioni |

Per i piani **Quantity-Based**, imposta la **Minimum Quantity** (quantità minima richiesta) e opzionalmente una **Maximum Quantity** per limitare il numero di postazioni che un abbonato può acquistare.

## Pricing tiers

Le fasce di prezzo definiscono la frequenza di fatturazione e le opzioni di sconto disponibili per i clienti su questo piano. Aggiungile nella sezione **Pricing Tiers** sotto il modulo principale.

Ogni fascia ha questi campi:

- **Tier Name** — L'etichetta mostrata ai clienti (es. `Monthly`, `Annual — Save 20%`). Supporta le traduzioni.
- **Billing Cycle** — Con quale frequenza il cliente viene addebitato: Giornaliera, Settimanale, Mensile, Trimestrale, Semestrale o Annuale.
- **Billing Interval** — Il moltiplicatore del ciclo di fatturazione. Imposta su `2` con Mensile per fatturare ogni 2 mesi.
- **Discount Percentage** — Lo sconto applicato al prezzo del prodotto per questa fascia. Imposta su `0` per il prezzo completo, o `20` per un sconto del 20%. Questo sconto si sovrappone a qualsiasi prezzo promozionale sul prodotto stesso.
- **Default Tier** — Contrassegna una fascia come predefinita per selezionarla automaticamente per i clienti quando visualizzano le opzioni di abbonamento.

### Esempio: piano a fasce con tre opzioni

Per un piano di abbonamento "Coffee Club":

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Trial period

Un periodo di prova permette ai clienti di provare l'abbonamento prima del primo addebito completo. Configuralo nella sezione **Trial Period**:

- **Trial Period (Days)** — Numero di giorni di prova gratuiti. Imposta su `0` per disattivare i periodi di prova. Massimo 365 giorni.
- **Trial Price** — Prezzo ridotto opzionale durante il periodo di prova (es. $1 per il primo mese). Lascia vuoto per un periodo di prova completamente gratuito.

## Cancellation policy

Controlla come i clienti possono cancellare l'abbonamento nella sezione **Cancellation Policy**:

| Policy | Description |
|--------|-------------|
| **Cancel Anytime** | I clienti possono cancellare immediatamente in qualsiasi momento |
| **Cancel at Period End** | La cancellazione entra in vigore alla fine del periodo pagato — i clienti mantengono l'accesso fino all'expiry |
| **Minimum Commitment Required** | I clienti devono completare un numero minimo di cicli di fatturazione prima di poter cancellare |

Additional settings:

- **Minimo impegno (Cicli)** — Quando si utilizza la politica di impegno, impostare il numero richiesto di cicli di fatturazione (es. `3` per un minimo di 3 mesi).
- **Periodo di grazia (Giorni)** — Giorni di accesso continuo dopo un fallimento del pagamento prima che l'abbonamento venga sospeso.

Impostare su `0` per la sospensione immediata.
- **Periodo di riacquisto (Giorni)** — Giorni dopo la cancellazione durante i quali un cliente può riacquistare l'abbonamento senza doverlo riascrivere da zero.

## Comportamento del cambio piano

Quando i clienti aggiornano o riducono il piano, è possibile controllare quando il cambiamento entra in vigore:

- **Comportamento di aggiornamento** — Impostare su **Immediato** (addebito proporzionato ora) o **Al Rinnovo** (cambiare al prossimo data di fatturazione).
- **Comportamento di riduzione** — Impostare su **Immediato** (applicare il credito alla prossima fattura) o **Al Rinnovo** (cambiare al prossimo data di fatturazione).

## Limiti e restrizioni

- **Numero massimo di cicli di fatturazione** — Il numero totale di cicli di fatturazione prima che l'abbonamento termini automaticamente. Lasciare vuoto per un'abbonamento ricorrente illimitato. Utile per piani a rate o abbonamenti con scadenza.
- **Tariffa di configurazione** — Un addebito unico raccolto quando l'abbonamento viene creato per la prima volta (es. tariffa di onboarding o di attivazione). Impostare su `0.00` per non avere una tariffa di configurazione.

## Add-on del piano

Gli add-on sono extra opzionali che i sottoscrittori possono aggiungere al loro piano. Aggiungerli nella sezione **Add-on del piano**:

- **Nome dell'add-on** — Il nome visualizzato ai clienti. Supporta le traduzioni.
- **Descrizione** — Cosa offre l'add-on.
- **Prezzo** — Costo dell'add-on.
- **Frequenza di fatturazione** — Se l'add-on viene addebitato **Per ciclo di fatturazione** (ricorrente) o **Una volta** all'inizio dell'abbonamento.
- **Consenti quantità** — Abilitare per permettere ai clienti di acquistare più unità dell'add-on.
- **Obbligatorio** — Selezionare per includere automaticamente l'add-on in tutti i nuovi abbonamenti. Gli add-on obbligatori non possono essere rimossi dal cliente.

## Visibilità e stato

- **Attivo** — Deselezionare per disattivare un piano in modo che non possano essere creati nuovi abbonamenti. Gli abbonamenti esistenti non sono influenzati.
- **Pubblico** — Deselezionare per nascondere il piano dalle pagine rivolte ai clienti (utile per piani interni o obsoleti su cui i sottoscrittori esistenti rimangono).
- **Ordine di ordinamento** — Controlla l'ordine di visualizzazione sulle pagine di selezione degli abbonamenti. I numeri più bassi appaiono per primi.

## Consigli

- Utilizzare un **periodo di prova** per ridurre l'esitazione — anche un breve periodo di prova gratuito di 7 giorni può migliorare significativamente il tasso di conversione per i prodotti a abbonamento.
- Configurare **tre livelli di prezzo** (mensile, trimestrale, annuale) con sconti crescenti per incoraggiare gli impegni annuali e migliorare il flusso di cassa.
- Per gli abbonamenti basati su servizi, impostare **Politica di cancellazione** su **Cancella alla fine del periodo** in modo che i clienti mantengano l'accesso durante il periodo pagato — questo sembra giusto e riduce i rimborshi.
- Mantenere il **Periodo di grazia** tra 3–7 giorni per i fallimenti di pagamento. Questo dà ai clienti tempo per aggiornare il loro metodo di pagamento prima di perdere l'accesso.
- Utilizzare raramente il flag **Obbligatorio** sugli add-on — utilizzarlo solo per cose che sono veramente obbligatori (es. un accordo di servizio), non come modo per gonfiare i prezzi.
- Disattivare i piani senza sottoscrittori invece di eliminarli — questo preserva i dati storici per eventuali clienti che hanno precedentemente sottoscritto.