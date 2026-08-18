---
title: Piani di sottoscrizione
---

I piani di sottoscrizione ti consentono di offrire addebiti ricorrenti per i tuoi prodotti: ideali per prodotti di consumo, servizi, box curate o qualsiasi prodotto che i clienti acquistano ripetutamente. Questa guida spiega come creare e configurare i piani, impostare i livelli di prezzo, aggiungere periodi di prova e collegare accessori opzionali.

## Per iniziare

Vai a **Sottoscrizioni > Piani di sottoscrizione** nella barra laterale amministrativa. L'elenco dei piani mostra tutti i tuoi piani con il modello di prezzo, il numero di sottoscrittori attivi e lo stato di visibilità.

![Elenco dei piani di sottoscrizione](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Per creare un nuovo piano, fai clic sul pulsante **Crea con l'assistente** - questo apre l'assistente per la creazione del piano, che ti guida passo dopo passo. Il pulsante **+ Aggiungi piano** accanto ad esso apre un modulo vuoto per i commercianti che preferiscono configurare tutto manualmente.

Un piano da solo non è acquistabile - è un modello. Una volta costruito qui, collegalo a uno o più prodotti dal tab **Sottoscrizioni** del prodotto (esclusivi per prodotti semplici, variabili e digitali), in modo che i clienti possano effettivamente sottoscriversi. Vedere [Vendere prodotti come sottoscrizioni](/help/selling-products-as-subscriptions) per questo passaggio.

## L'editor del piano

Aprire un piano esistente (cliccando sul nome o sull'icona della matita, dall'elenco) ti porta nell'editor del piano. L'intestazione mostra il nome del piano, il modello di prezzo, i badge **Attivo**/**Non attivo** e **Pubblico**/**Privato**, e la data di creazione. I due pulsanti nell'angolo in alto a destra dell'intestazione salvano le modifiche - l'icona del cerchio verde salva e torna all'elenco, l'icona del cerchio semplice salva e ti tiene sulla pagina in modo che tu possa continuare a modificare.

Sotto l'intestazione, una striscia di statistiche riassume il piano in un colpo d'occhio: **Sottoscrizioni attive**, **Livelli di prezzo**, **Accessori**, e **Reddito totale**.

Il resto del modulo è organizzato in cinque schede:

| Scheda | Cosa contiene |
|-----|-------------------|
| **Generale** | Informazioni sul piano (nome, slug, descrizione) e Stato (attivo/pubblico) |
| **Prezzo** | Configurazione del prezzo, Periodo di prova e Limiti & restrizioni |
| **Livelli e accessori** | Editor dei livelli di prezzo e accessori |
| **Ciclo vitale** | Politica di annullamento e comportamento del piano |
| **Avanzate** | Integrazione del provider e statistiche |

Le sezioni seguenti illustrano le impostazioni di ciascuna scheda. Quando crei un nuovo piano direttamente da **+ Aggiungi piano** (anziché dall'assistente), gli stessi campi appaiono in un unico modulo scorrevole invece di schede - salva il piano una volta e riapri il piano per ottenere l'editor con le schede complete.

## Informazioni sul piano (scheda Generale)

La scheda **Informazioni sul piano** cattura l'identità principale del piano.

- **Nome del piano** - Il nome che i clienti vedono quando si sottoscrivono. Fai clic sull'icona del globo per aggiungere le traduzioni per le altre lingue del negozio.
- **Slug** - Un identificatore amichevole per le URL generato automaticamente dal nome (es. `premium-plan`). Viene utilizzato internamente e negli integratori.
- **Descrizione** - Testo opzionale che descrive cosa include il piano. Supporta le traduzioni.

La scheda **Stato** sulla stessa scheda controlla i comandi **Attivo** e **Pubblico** - vedi [Visibilità e stato](#visibility-and-status) qui sotto.

![Scheda Generale dell'editor del piano](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modello di prezzo (scheda Prezzo)

La scheda **Configurazione del prezzo** controlla come è strutturato il prezzo per questo piano:

| Modello di prezzo | Migliore per |
|---------------|----------|
| **Prezzo a livelli** | Offrire opzioni di impegno mensile, trimestrale e annuale con sconti per periodi più lunghi |
| **Prezzo in base alla quantità** | Prezzo per utente o per sede dove il totale si adatta alla quantità (es. licenze per team) |
| **Tariffa fissa** | Un unico prezzo fisso senza variazioni |

Per i piani **Prezzo in base alla quantità**, seleziona **Consenti quantità** e imposta la **Quantità minima** (sedie richieste minime) e, eventualmente, una **Quantità massima** per limitare il numero di sedie che un sottoscrittore può acquistare.

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

[![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-prricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Costi di base (scheda Tier & Add-ons)

I costi di base definiscono la frequenza di fatturazione e le opzioni di sconto disponibili per i clienti su questo piano. Aggiungili nella scheda **Costi di base** sulla scheda **Tier & Add-ons**, insieme all'editor per gli accessori.

Ogni livello ha questi campi:

- **Nome del livello** — L'etichetta visualizzata ai clienti (es. `Mensile`, `Annuale - Risparmia 20%`). Supporta le traduzioni.
- **Ciclo di fatturazione** — Quanto spesso il cliente viene addebitato: Giornaliero, Setimanale, Mensile, Quadrimestrale, Semestrale o Annuale.
- **Intervallo di fatturazione** — Il moltiplicatore per il ciclo di fatturazione. Impostare a `2` con il Mensile per fatturare ogni 2 mesi.
- **Percentuale di sconto** — Lo sconto applicato al prezzo del prodotto per questo livello. Impostare a `0` per il prezzo pieno, oppure a `20` per ottenere uno sconto del 20%. Questo sconto si sovrappone a qualsiasi prezzo in saldo sul prodotto stesso.
- **Livello predefinito** — Contrassegna un livello come predefinito per selezionarlo automaticamente per i clienti quando guardano le opzioni di sottoscrizione.

Lo sconto si applica a partire dal primo ciclo di fatturazione del cliente, non solo sui rinnovi — un livello con uno sconto del 20% addebiterà lo sconto del 20% fin dal primo giorno (o dal primo addebito dopo un periodo di prova, se il piano ne ha uno).

### Esempio: piano a livelli con tre opzioni

Per un piano di sottoscrizione "Coffee Club":

| Nome del livello | Ciclo di fatturazione | Sconto |
|-----------|---------------|----------|
| Mensile | Mensile | 0% |
| Quadrimestrale - Risparmia 10% | Quadrimestrale | 10% |
| Annuale - Risparmia 20% | Annuale | 20% |

## Accessori del piano (scheda Tier & Add-ons)

Gli accessori sono extra opzionali che i sottoscrittori possono aggiungere al loro piano. Aggiungili nella scheda **Accessori**, direttamente sotto i Costi di base sulla stessa scheda:

- **Nome dell'accessorio** — Il nome visualizzato ai clienti. Supporta le traduzioni.
- **Descrizione** — Cosa fornisce l'accessorio.
- **Prezzo** — Costo dell'accessorio.
- **Frequenza di fatturazione** — Se l'accessorio viene addebitato **Per ciclo di fatturazione** (ricorrente) o **Una tantum** all'inizio della sottoscrizione.
- **Consenti quantità** — Attiva per consentire ai clienti di acquistare più unità dell'accessorio.
- **Obbligatorio** — Seleziona questa opzione per includere automaticamente l'accessorio su tutte le nuove sottoscrizioni. Gli accessori obbligatori non possono essere rimossi dal cliente.

[![Scheda Tier & Add-ons del piano editor](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Periodo di prova (scheda Pricing)

Un periodo di prova permette ai clienti di provare la sottoscrizione prima del primo addebito completo. Configuralo nella scheda **Periodo di prova**, sotto la Configurazione dei prezzi:

- **Periodo di prova (giorni)** — Numero di giorni di prova gratuiti. Impostare a `0` per disabilitare i periodi di prova. Il massimo è 365 giorni.
- **Prezzo di prova** — Prezzo ridotto opzionale durante la prova (es. $1 per il primo mese). Lasciare vuoto per un periodo di prova completamente gratuito.

## Limiti e restrizioni (scheda Pricing)

La scheda **Limiti & Restrizioni**, presente anch'essa sulla scheda Pricing, include:

- **Massimo cicli di fatturazione** — Il numero totale di cicli di fatturazione prima che la sottoscrizione si concluda automaticamente. Lasciare vuoto per una fatturazione ricorrente illimitata. Utile per piani a rate o sottoscrizioni con scadenza temporanea.

**Fatto di attivazione** e **Ordine di visualizzazione** non fanno parte di questa scheda — vengono impostati una volta, quando si crea per la prima volta il piano attraverso la procedura **Crea con l'assistente**, e non possono essere modificati successivamente dalla schermata di modifica. Se necessiti di modificare uno di questi valori, disattiva il piano e rigeneralo con l'assistente invece di modificare quello esistente. Nota che i costi di attivazione non vengono ancora addebitati automaticamente al checkout in questa versione — considera il campo come riservato per un aggiornamento futuro invece che un addebito funzionante.

## Policy di annullamento (scheda Lifecycle)

Controlla come i clienti possono annullare la loro sottoscrizione nella scheda **Policy di annullamento**:

{"| Policy | Description |\n|--------|-------------|\n| **Cancel Anytime** | I clienti possono annullare immediatamente in qualsiasi momento |\n| **Cancel at Period End** | L'annullamento diventa effettivo alla fine del periodo pagato — i clienti mantengono l'accesso fino alla scadenza |\n| **Minimum Commitment Required** | I clienti devono completare un numero minimo di cicli di fatturazione prima di annullare |\n\nAdditional settings: |\n\n- **Minimum Commitment (Cycles)** — Quando si utilizza la policy di impegno, impostare il numero richiesto di cicli di fatturazione (es. `3` per un minimo di 3 mesi). |\n- **Grace Period (Days)** — Giorni di accesso continuato dopo un fallimento di pagamento prima che la sottoscrizione venga sospesa. Impostare su `0` per la sospensione immediata. |\n- **Reactivation Period (Days)** | Giorni dopo l'annullamento durante i quali un cliente può riaccedere alla propria sottoscrizione senza dover riscrivere da zero. |\n\n## Plan change behavior (Lifecycle tab) |\n\nLa scheda **Plan Change Behavior**, sotto la politica di annullamento, controlla cosa accade quando i clienti passano da un piano all'altro: |\n\n- **Upgrade Behavior** — Impostare su **Immediate** (addebitare l'importo proporzionato adesso) o **At Renewal** (cambiare alla data di rinnovo successiva). |\n- **Downgrade Behavior** — Impostare su **Immediate** (applicare un credito alla prossima fattura) o **At Renewal** (cambiare alla data di rinnovo successiva). |\n\n![Lifecycle tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp) |\n\n## Advanced tab |\n\nLa scheda **Advanced** contiene impostazioni che non userai spesso nella vita quotidiana: |\n\n- **Provider Integration** — Collegare questo piano a ID piani/ prezzi dai tuoi fornitori di pagamento (es. `"stripe": "price_xxx", "paypal": "P-xxx"`), per negozi che gestiscono le sottoscrizioni in modo autonomo tramite il fornitore invece del motore di fatturazione di Spwig. |\n- **Statistics** — Dati leggibili solo: **Active Subscriptions**, **Total Revenue**, e le date di creazione/aggiornamento del piano. Questi riflettono le statistiche nella parte superiore della pagina. |\n\n![Advanced tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp) |\n\n## Visibility and status (General tab) |\n\n- **Active** — Deselezionare per disattivare un piano in modo che non possano essere create nuove sottoscrizioni. Le sottoscrizioni esistenti non vengono interessate. |\n- **Public** — Deselezionare per nascondere il piano dalle pagine visibili ai clienti (utile per piani interni o obsoleti a cui i sottoscrittori esistenti rimangono). |\n\n## Tips |\n\n- Usa un periodo di prova per ridurre l'esitazione — anche una prova gratuita di 7 giorni può migliorare significativamente i tassi di conversione per i prodotti a sottoscrizione. |\n- Configura tre livelli di prezzo (mensile, trimestrale, annuale) con sconti crescenti per incoraggiare gli impegni annuali e migliorare il tuo flusso di cassa. |\n- Per sottoscrizioni basate su servizi, imposta la **Cancellazione Policy** su **Cancel at Period End** in modo che i clienti mantengano l'accesso durante il loro periodo pagato — questo sembra equo e riduce i rimborssi. |\n- Mantieni il **Grace Period** tra 3-7 giorni per i fallimenti di pagamento. Questo dà ai clienti il tempo di aggiornare il loro metodo di pagamento prima di perdere l'accesso. |\n- Usa l'indicatore **Required** sugli accessori con moderazione — usalo solo per cose che sono veramente obbligatorie (es. un accordo di servizio), non come modo per aumentare i prezzi. |\n- Disattiva i piani senza sottoscrittori invece di cancellarli — questo preserva i dati storici per qualsiasi cliente che si è precedentemente sottoscritto."}