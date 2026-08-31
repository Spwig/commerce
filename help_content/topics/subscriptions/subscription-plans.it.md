---
title: Piani di abbonamento
---

I piani di abbonamento ti consentono di offrire fatturazione ricorrente per i tuoi prodotti — ideali per consumabili, servizi, box curati o qualsiasi prodotto che i clienti acquistano ripetutamente. Questa guida spiega come creare e configurare i piani, impostare le fasce di prezzo, aggiungere periodi di prova e allegare add-on opzionali.

## Per iniziare

Vai a **Abbonamenti > Piani di abbonamento** nella barra laterale di amministrazione. L'elenco dei piani mostra tutti i tuoi piani con il loro modello di prezzo, il numero di abbonati attivi e lo stato di visibilità.

![Elenco dei piani di abbonamento](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Per creare un nuovo piano, fai clic sul pulsante **Crea con Assistente** — questo apre l'assistente di creazione del piano, che ti guida passo dopo passo nella configurazione. Il pulsante **+ Aggiungi Piano** accanto ad esso apre un modulo vuoto per i commercianti che preferiscono configurare tutto manualmente.

Un piano da solo non è acquistabile — è un modello. Una volta che l'hai creato qui, allegalo a uno o più prodotti dalla scheda **Abbonamenti** del prodotto (solo prodotti Semplici, Variabili e Digitali) in modo che i clienti possano effettivamente abbonarsi. Consulta [Vendita di prodotti come abbonamenti](/help/selling-products-as-subscriptions) per quel passaggio.

## L'editor del piano

L'apertura di un piano esistente (fai clic sul suo nome, o sull'icona della matita, dall'elenco) ti porta all'editor del piano. L'intestazione mostra il nome del piano, il suo modello di prezzo, le etichette di stato **Attivo**/**Inattivo** e **Pubblico**/**Privato**, e la data di creazione. I due pulsanti nell'angolo in alto a destra dell'intestazione salvano le tue modifiche — l'icona del cerchio con il segno di spunta salva e torna all'elenco, l'icona di spunta semplice salva e ti mantiene sulla pagina in modo da poter continuare a modificare.

Sotto l'intestazione, una striscia di statistiche riassume il piano a colpo d'occhio: **Abbonamenti Attivi**, **Fasce di Prezzo**, **Add-on** e **Ricavi Totali**.

Il resto del modulo è organizzato in cinque schede:

| Scheda | Contenuto |
|-----|-------------------|
| **Generale** | Informazioni sul piano (nome, slug, descrizione) e Stato (attivo/pubblico) |
| **Prezzi** | Configurazione dei prezzi, Periodo di prova e Limiti e restrizioni |
| **Fasce e Add-on** | Editor delle Fasce di prezzo e degli Add-on |
| **Ciclo di vita** | Politica di cancellazione e Comportamento di modifica del piano |
| **Avanzate** | Integrazione del provider e Statistiche |

Le sezioni sottostanti illustrano le impostazioni di ciascuna scheda. Quando crei un piano completamente nuovo direttamente da **+ Aggiungi Piano** (anziché dall'assistente), gli stessi campi appaiono in un unico modulo scorrevole invece che in schede — salva il piano una volta e riaprilo per ottenere l'editor completo con schede.

## Informazioni sul piano (scheda Generale)

La card **Informazioni sul piano** cattura l'identità principale del tuo piano.

- **Nome del piano** — Il nome che i clienti vedono quando si abbonano. Fai clic sull'icona del globo per aggiungere traduzioni per altre lingue dello store.
- **Slug** — Un identificatore compatibile con URL generato automaticamente dal nome (ad es., `premium-plan`). Viene utilizzato internamente e nelle integrazioni.
- **Descrizione** — Testo facoltativo che descrive cosa include il piano. Supporta le traduzioni.

La card **Stato** nella stessa scheda controlla le interruttori **Attivo** e **Pubblico** — consulta [Visibilità e stato](#visibility-and-status) di seguito.

![Scheda Generale dell'editor del piano](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modello di prezzo (scheda Prezzi)

La card **Configurazione dei prezzi** controlla come è strutturata la tariffa per questo piano:

| Modello di prezzo | Ideale per |
|---------------|----------|
| **Prezzi a fasce** | Offrire opzioni di impegno mensili, trimestrali e annuali con sconti per termini più lunghi |
| **Basato sulla quantità** | Prezzi per posto o per utente in cui il totale scala con la quantità (ad es., licenze di team) |
| **Tariffa fissa** | Un singolo prezzo fisso senza variazioni |

Per i piani **Basati sulla quantità**, seleziona **Consenti Quantità** e imposta la **Quantità Minima** (numero minimo di posti richiesti) e facoltativamente una **Quantità Massima** per limitare il numero di posti che un abbonato può acquistare.

![Scheda Prezzi dell'editor dei piani](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Livelli di prezzo (Scheda Livelli & Add-on)

I livelli di prezzo definiscono la frequenza di fatturazione e le opzioni di sconto disponibili per i clienti su questo piano. Aggiungili nella card **Livelli di prezzo** nella scheda **Livelli & Add-on**, accanto all'editor degli Add-on.

Ogni livello ha questi campi:

- **Nome del livello** — L'etichetta mostrata ai clienti (es. `Mensile`, `Annuale — Risparmia 20%`). Supporta le traduzioni.
- **Ciclo di fatturazione** — Con quale frequenza il cliente viene addebitato: Giornaliero, Settimanale, Mensile, Trimestrale, Semestrale o Annuale.
- **Intervallo di fatturazione** — Il moltiplicatore per il ciclo di fatturazione. Imposta su `2` con Mensile per fatturare ogni 2 mesi.
- **Percentuale di sconto** — Lo sconto applicato al prezzo del prodotto per questo livello. Imposta su `0` per il prezzo pieno, oppure su `20` per concedere il 20% di sconto. Questo sconto si somma a qualsiasi prezzo in offerta sul prodotto stesso.
- **Livello predefinito** — Segna un livello come predefinito per pre-selezionarlo per i clienti quando visualizzano le opzioni di abbonamento.

Lo sconto si applica a partire dal primo ciclo di fatturazione del cliente, non solo ai rinnovi — un livello con uno sconto del 20% addebita il 20% di sconto fin dal primo giorno (o dal primo addebito dopo un periodo di prova, se il piano ne ha uno).

### Esempio: piano a livelli con tre opzioni

Per un piano di abbonamento "Coffee Club":

| Nome del livello | Ciclo di fatturazione | Sconto |
|-----------|---------------|----------|
| Mensile | Mensile | 0% |
| Trimestrale — Risparmia 10% | Trimestrale | 10% |
| Annuale — Risparmia 20% | Annuale | 20% |

## Add-on del piano (Scheda Livelli & Add-on)

Gli add-on sono extra opzionali che gli abbonati possono allegare al loro piano. Aggiungili nella card **Add-on**, direttamente sotto Livelli di prezzo nella stessa scheda:

- **Nome dell'add-on** — Il nome mostrato ai clienti. Supporta le traduzioni.
- **Descrizione** — Cosa fornisce l'add-on.
- **Prezzo** — Costo dell'add-on.
- **Frequenza di fatturazione** — Se l'add-on viene addebitato **Per ciclo di fatturazione** (ricorrente) o **Una tantum** all'inizio dell'abbonamento.
- **Consenti quantità** — Attiva per consentire ai clienti di acquistare più unità dell'add-on.
- **Obbligatorio** — Spunta questa opzione per includere automaticamente l'add-on in tutti i nuovi abbonamenti. Gli add-on obbligatori non possono essere rimossi dal cliente.

![Scheda Livelli & Add-on dell'editor dei piani](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Periodo di prova (Scheda Prezzi)

Un periodo di prova consente ai clienti di provare il tuo abbonamento prima del primo addebito completo. Configura questo nella card **Periodo di prova**, sotto Configurazione prezzi:

- **Periodo di prova (Giorni)** — Numero di giorni di prova gratuiti. Imposta su `0` per disabilitare le prove. Il massimo è 365 giorni.
- **Prezzo di prova** — Prezzo ridotto opzionale durante la prova (es. $1 per il primo mese). Lascia vuoto per una prova completamente gratuita.

## Limiti e restrizioni (Scheda Prezzi)

La card **Limiti & Restrizioni**, anch'essa nella scheda Prezzi, contiene:

- **Cicli di fatturazione massimi** — Il numero totale di cicli di fatturazione prima che l'abbonamento termini automaticamente. Lascia vuoto per una fatturazione ricorrente illimitata. Utile per piani a rate o abbonamenti a tempo limitato.

**Commissione di attivazione** e **Ordine di ordinamento** non fanno parte di questa card — vengono impostati una sola volta, quando crei per la prima volta il piano tramite il flusso **Crea con Wizard**, e non possono essere modificati dalla schermata di modifica successivamente. Se hai bisogno di regolare uno di questi valori, disattiva il piano e ricrealo con il wizard invece di modificare quello esistente. Tieni presente che le commissioni di attivazione non vengono ancora addebitate automaticamente al checkout in questa release — considera il campo come riservato per un aggiornamento futuro piuttosto che come un addebito funzionante.

## Politica di cancellazione (Scheda Ciclo di vita)

Controlla come i clienti possono annullare il loro abbonamento nella card **Politica di cancellazione**:


{"| Policy | Description |\n|--------|-------------|\n| **Cancel Anytime** | I clienti possono annullare immediatamente in qualsiasi momento |\n| **Cancel at Period End** | L'annullamento ha effetto alla fine del periodo pagato — i clienti mantengono l'accesso fino alla scadenza |\n| **Minimum Commitment Required** | I clienti devono completare un numero minimo di cicli di fatturazione prima di annullare |\n\nAdditional settings: |\n\n- **Minimum Commitment (Cycles)** — Quando si utilizza la policy di impegno, impostare il numero richiesto di cicli di fatturazione (es. `3` per un minimo di 3 mesi). |\n- **Grace Period (Days)** — Giorni di accesso continuato dopo un fallimento di pagamento prima che la sottoscrizione venga sospesa. Impostare su `0` per la sospensione immediata. |\n- **Reactivation Period (Days)** | Giorni dopo l'annullamento durante i quali un cliente può riaccedere alla propria sottoscrizione senza dover riscriverne da capo. |\n\n## Plan change behavior (Lifecycle tab) |\n\nLa scheda **Plan Change Behavior**, sotto la politica di annullamento, controlla cosa accade quando i clienti passano da un piano all'altro: |\n\n- **Upgrade Behavior** — Impostare su **Immediate** (addebitare l'importo proporzionato adesso) o **At Renewal** (cambiare alla data di rinnovo successiva). |\n- **Downgrade Behavior** — Impostare su **Immediate** (applicare un credito alla prossima fattura) o **At Renewal** (cambiare alla data di rinnovo successiva). |\n\n![Lifecycle tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp) |\n\n## Advanced tab |\n\nLa scheda **Advanced** contiene impostazioni che non userai spesso nella vita quotidiana: |\n\n- **Provider Integration** — Collegare questo piano a ID piani/ prezzi dai tuoi fornitori di pagamento (es. `"stripe": "price_xxx", "paypal": "P-xxx"`), per negozi che gestiscono le sottoscrizioni in modo autonomo tramite il fornitore invece del motore di fatturazione di Spwig. |\n- **Statistics** — Dati leggibili solo: **Active Subscriptions**, **Total Revenue**, e le date di creazione/aggiornamento del piano. Questi riflettono le statistiche nella parte superiore della pagina. |\n\n![Advanced tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp) |\n\n## Visibility and status (General tab) |\n\n- **Active** — Deselezionare per disattivare un piano in modo che non possano essere create nuove sottoscrizioni. Le sottoscrizioni esistenti non vengono interessate. |\n- **Public** — Deselezionare per nascondere il piano dalle pagine visibili ai clienti (utile per piani interni o obsoleti a cui i sottoscrittori esistenti rimangono). |\n\n## Tips |\n\n- Usa un periodo di prova per ridurre l'esitazione — anche una prova gratuita di 7 giorni può migliorare significativamente i tassi di conversione per i prodotti a sottoscrizione. |\n- Configura tre livelli di prezzo (mensile, trimestrale, annuale) con sconti crescenti per incoraggiare gli impegni annuali e migliorare il tuo flusso di cassa. |\n- Per sottoscrizioni basate su servizi, imposta la **Cancellazione Policy** su **Cancel at Period End** in modo che i clienti mantengano l'accesso durante il loro periodo pagato — questo sembra equo e riduce i rimborssi. |\n- Mantieni il **Grace Period** tra 3-7 giorni per i fallimenti di pagamento. Questo dà ai clienti il tempo di aggiornare il loro metodo di pagamento prima di perdere l'accesso. |\n- Usa l'indicatore **Required** sugli accessori con moderazione — usalo solo per cose che sono veramente obbligatorie (es. un accordo di servizio), non come modo per aumentare i prezzi. |\n- Disattiva i piani senza sottoscrittori invece di cancellarli — questo preserva i dati storici per qualsiasi cliente che si era precedentemente sottoscritto."}