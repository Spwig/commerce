---
title: Configurazione dei pagamenti
---

I fornitori di pagamento collegano il tuo negozio a passerelle di pagamento in modo da poter accettare carte di credito, portafogli digitali e altri metodi di pagamento al momento del checkout. Spwig supporta diversi fornitori contemporaneamente, offrendo ai tuoi clienti opzioni di pagamento flessibili.

![Fornitori di pagamento](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Fornitori disponibili

| Fornitore | Descrizione |
|----------|-------------|
| **Stripe** | Carte di credito, Apple Pay, Google Pay e 135+ valute |
| **PayPal** | Saldo PayPal, carte di credito/debito e opzioni di pagamento successivo |
| **Airwallex** | Pagamenti multi-valuta ottimizzati per il commercio transfrontaliero |
| **Adyen** | Pagamenti a livello aziendale con 250+ metodi di pagamento in tutto il mondo |
| **Square** | Pagamenti in persona e online con supporto POS integrato |
| **Revolut** | Pagamenti europei veloci con tassi di cambio competitivi |

## Connessione a un Fornitore

Naviga verso **Impostazioni > Fornitori di pagamento** e fai clic su **Connect Provider** per avviare il wizard di configurazione.

### Passo 1: Seleziona Fornitore

Scegli tra i fornitori di pagamento disponibili. Ogni carta mostra le funzionalità e le regioni supportate dal fornitore.

### Passo 2: Istruzioni di configurazione

Rivedi la guida specifica per il fornitore. Questo include:
- Come creare un account con il fornitore (se non ne hai uno)
- Dove trovare le tue credenziali API nel dashboard del fornitore
- Requisiti preliminari (ad esempio, verifica aziendale)

### Passo 3: Inserisci le credenziali

Inserisci le tue credenziali API:
- **Chiave API / Chiave segreta** — Le tue credenziali di autenticazione ottenute dal dashboard del fornitore
- **Modalità di checkout** — Scegli come i clienti interagiscono con il modulo di pagamento:

| Modalità | Descrizione |
|------|-------------|
| **Ospitato** | I clienti vengono reindirizzati alla pagina di pagamento del fornitore (es. Stripe Checkout). Configurazione più semplice, la conformità PCI è gestita dal fornitore. |
| **Integrato** | Il modulo di pagamento è incorporato direttamente nella tua pagina di checkout. Esperienza fluida, ma richiede l'SDK JavaScript del fornitore. |

- **Modalità sandbox / live** — Inizia in modalità sandbox per i test, quindi passa a live quando sei pronto

### Passo 4: Test Connection

Fai clic su **Test Connection** per verificare che le tue credenziali siano valide. Il wizard controlla:
- Autenticazione della chiave API
- Permessi dell'account
- Accessibilità del punto di terminazione delle webhook

### Passo 5: Configura e salva

Finalizza le impostazioni del fornitore:
- **Attivo** — Abilita o disabilita il fornitore
- **Fornitore predefinito** — Imposta come metodo di pagamento principale al momento del checkout
- **Nome visualizzato** — Il nome visualizzato ai clienti durante il checkout
- **Ordine di ordinamento** — Controlla l'ordine in cui vengono visualizzati i fornitori al momento del checkout (i numeri più bassi appaiono per primi)

## Dashboard dei pagamenti

Naviga verso **Impostazioni > Dashboard dei pagamenti** per un riepilogo delle tue attività di pagamento:

### Azioni richieste

Le schede di avviso in alto evidenziano problemi che richiedono attenzione:
- **Transazioni fallite** — Pagamenti che non sono potuti essere elaborati
- **Catture in sospeso** — Pagamenti autorizzati in attesa di cattura
- **Errori di connessione** — Fornitori con problemi di connettività

### Analisi dei ricavi

- **Grafico dei ricavi** — Riepilogo visivo del volume dei pagamenti nel tempo, raggruppato per giorno, settimana o mese
- **Metriche di prestazioni** — Totale dei ricavi, tasso di successo, valore medio delle transazioni e tasso di rimborso
- **Confronto dei fornitori** — Schede di prestazioni a confronto per ciascun fornitore connesso

### Analisi delle transazioni

- **Distribuzione dello stato** — Conteggio delle transazioni completate, in sospeso, fallite e rimborsate
- **Mischi di metodi di pagamento** — I metodi di pagamento utilizzati di più dai clienti (carte di credito, PayPal, portafogli digitali)

## Gestione dei metodi di pagamento

Ogni fornitore supporta diversi metodi di pagamento. Puoi abilitare o disabilitare metodi specifici per paese:

1. Naviga verso la pagina di configurazione di un fornitore
2. Scorri fino alla sezione **Metodi di pagamento**
3. Attiva o disattiva i metodi individuali
4. Utilizza i controlli a livello di paese per limitare i metodi a specifici mercati

Questo è utile quando un metodo di pagamento è popolare in una regione ma non in un'altra (es. iDEAL nei Paesi Bassi, Bancontact in Belgio).

## Webhook

I webhook mantengono il tuo negozio sincronizzato con il fornitore di pagamento in tempo reale. Gestiscono eventi come:
- Pagamento completato o fallito
- Rimborso processato
- Dispute e chargeback aperti
- Rinnovi delle sottoscrizioni

### Configurazione automatica

Quando colleghi un fornitore, Spwig registra automaticamente un endpoint webhook con il fornitore. L'URL del webhook è visualizzato sulla pagina di configurazione del fornitore per riferimento.

### Monitoraggio dei webhook

Ogni webhook in arrivo viene registrato con:
- **Tipo di evento** (es. payment_intent.succeeded)
- **Timestamp** e stato di elaborazione
- **Payload** per il debug

Se un webhook non riesce nell'elaborazione, viene registrato come errore in modo da poter investigare.

## Utilizzo di più fornitori

Puoi collegare più fornitori di pagamento contemporaneamente:

- **Fornitore predefinito** — Il fornitore selezionato di default al momento del checkout. Marca un fornitore come predefinito nella sua configurazione.
- **Ordine di ordinamento** — Controlla l'ordine di visualizzazione al momento del checkout. I clienti vedono tutti i fornitori attivi e possono scegliere il loro preferito.
- **Failover** — Se un fornitore ha un'interruzione, i clienti possono comunque pagare utilizzando un altro fornitore.

## Consigli

- Inizia con **Stripe** o **PayPal** — coprono la gamma più ampia di metodi di pagamento e regioni.
- Utilizza la **modalità sandbox/test** per elaborare transazioni di test prima di andare in produzione. Ogni fornitore ha numeri di carta di test nella loro documentazione.
- Abilita **più fornitori** in modo che i clienti abbiano un'opzione di pagamento di backup se un fornitore ha problemi.
- Imposta un **ordine di ordinamento basso** per il tuo fornitore preferito in modo che appaia per primo al momento del checkout.
- Monitora la Dashboard dei pagamenti settimanalmente per individuare tempestivamente transazioni fallite e problemi di connessione.
- Mantieni le tue credenziali API sicure — sono memorizzate crittografate nel database ma non dovrebbero mai essere condivise.