---
title: Elaborazione dei pagamenti
---

L'elaborazione dei pagamenti ti permette di pagare agli affiliati le loro commissioni approvate. Questa guida ti mostra come creare, gestire ed elaborare i pagamenti tramite PayPal o fornitori di trasferimenti bancari.

![Elenco dei pagamenti](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Panoramica dei pagamenti

Un pagamento è un batch di pagamenti che raggruppa diverse commissioni approvate per un unico affiliato. Immaginalo come un assegno per tutti i guadagni pendenti.

Caratteristiche principali:
- **Include diverse commissioni** — Un pagamento può coprire decine di commissioni approvate
- **Richiede un limite minimo** — La maggior parte dei programmi ha importi minimi di pagamento ($50-$100 tipici)
- **Elaborato tramite fornitori** — PayPal o Airwallex gestiscono effettivamente il trasferimento dei fondi
- **Ha un ciclo di vita** — In sospeso → In elaborazione → Completato (o Fallito)

## Flusso di lavoro dei pagamenti

Il processo completo di pagamento segue sei passaggi:

1. **L'affiliato guadagna commissioni** — Vendite attribuite a link di tracciamento degli affiliati
2. **Il merchant approva le commissioni** — Rivedi e approva le commissioni pendenti
3. **Il saldo raggiunge il minimo** — Il saldo approvato dell'affiliato soddisfa il limite del programma
4. **L'affiliato richiede il pagamento** — L'affiliato invia la richiesta di pagamento nel proprio dashboard
5. **Il merchant elabora il pagamento** — Crei e elabori il pagamento
6. **Pagamento completato** — Il fornitore invia i fondi, le commissioni vengono contrassegnate come pagate

## Visualizzazione dei pagamenti

Naviga verso **Programma degli affiliati > Pagamenti** per accedere al dashboard di gestione dei pagamenti.

Il pannello delle statistiche mostra:
- **In sospeso** — Pagamenti creati ma non ancora elaborati
- **In elaborazione** — Attualmente inviati al fornitore di pagamento
- **Completati** — Pagati con successo
- **Falliti** — Pagamento fallito (richiede attenzione)

La visualizzazione in elenco mostra:
- Nome e codice dell'affiliato
- Importo del pagamento
- Metodo di pagamento (PayPal o Trasferimento bancario)
- Etichetta di stato
- Date di creazione e completamento
- Pulsanti di azione

Utilizza i filtri per restringere per:
- Affiliato
- Metodo di pagamento
- Stato
- Intervallo di date

## Creazione di un pagamento

Segui questi passaggi per creare un nuovo pagamento:

1. **Naviga** verso **Programma degli affiliati > Pagamenti**
2. **Clicca** sul pulsante **+ Aggiungi pagamento**
3. **Seleziona l'affiliato** dal menu a discesa
4. **Rivedi le commissioni approvate** — Il sistema visualizza tutte le commissioni non pagate e approvate per questo affiliato
5. **Seleziona le commissioni da includere** — Seleziona le caselle per le commissioni da pagare (di solito tutte)
6. **Verifica l'importo totale** — Il sistema calcola automaticamente la somma
7. **Scegli il metodo di pagamento** — PayPal o Trasferimento bancario (in base alle preferenze dell'affiliato)
8. **Seleziona l'account del fornitore** — Scegli quale account PayPal/Airwallex utilizzare
9. **Aggiungi note** (opzionale) — Note interne per la documentazione
10. **Clicca Salva** — Il pagamento viene creato con lo stato "In sospeso"

Il pagamento è ora pronto per l'elaborazione.

## Elaborazione dei pagamenti

Hai due opzioni per l'elaborazione dei pagamenti: manuale o basata sul fornitore.

### Elaborazione manuale

Utilizza l'elaborazione manuale quando gestisci i pagamenti al di fuori del sistema (assegni, trasferimenti bancari, ecc.):

1. Seleziona il pagamento nell'elenco
2. Clicca sull'azione **Contrassegna come in elaborazione**
3. Completa il pagamento attraverso il tuo metodo esterno
4. Torna al pagamento
5. Clicca sull'azione **Contrassegna come completato**
6. Le commissioni vengono automaticamente aggiornate allo stato "Pagato"

L'elaborazione manuale offre flessibilità ma richiede più lavoro amministrativo.

### Elaborazione tramite fornitore (consigliata)

L'elaborazione tramite fornitore automatizza i pagamenti tramite PayPal o Airwallex:

1. **Seleziona pagamento(i)** nell'elenco (puoi elaborare più di uno)
2. **Clicca** sull'azione **Elabora con fornitore**
3. **Conferma** nel dialogo
4. **Il sistema inserisce in coda il compito** — Il worker Celery gestisce la chiamata API
5. **Il fornitore elabora il pagamento**:
   - **PayPal**: Batch fino a 15.000 pagamenti per richiesta
   - **Airwallex**: Trasferimenti bancari individuali
6. **Webhook aggiorna lo stato** — Il fornitore conferma il completamento
7. **Commissioni contrassegnate come pagate** — Il sistema aggiorna tutte le commissioni incluse

L'elaborazione tramite fornitore è più veloce, più affidabile e crea un registro di audit automatico.

## Metodi di pagamento

Spwig supporta due metodi di pagamento con requisiti diversi:

| Metodo | Fornitore | Requisiti | Tempo di elaborazione | Costi | Migliore per |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Payouts | L'affiliato deve avere un valido `payment_email` | 1-2 giorni lavorativi | ~2% o $0,25-$1,00 per pagamento | La maggior parte degli affiliati, portata globale |
| **Trasferimento bancario** | Airwallex | Dettagli dell'account bancario (numero di conto, routing, SWIFT) | 2-5 giorni lavorativi | Varia in base al paese | Affiliati internazionali, importi elevati |

Gli affiliati configurano il loro metodo di pagamento e i dettagli nel loro dashboard. Il sistema seleziona automaticamente il fornitore appropriato in base alle loro preferenze.

### Logica di selezione del metodo di pagamento

Quando si elabora un pagamento, Spwig seleziona il fornitore come segue:

1. Controlla il metodo di pagamento preferito dall'affiliato (PayPal o Trasferimento bancario)
2. Abbinalo all'account del fornitore configurato (PayPal → PayPal, Banca → Airwallex)
3. Ricadi su un fornitore disponibile se la preferenza non è disponibile
4. Mostra un errore se non sono configurati fornitori

## Flusso degli stati dei pagamenti

Comprendere gli stati dei pagamenti ti aiuta a monitorare lo stato dei pagamenti:

| Stato | Significato | Azione successiva |
|--------|---------|-------------|
| **In sospeso** | Creato ma non ancora inviato al fornitore | Elabora con il fornitore o contrassegna come in elaborazione |
| **In elaborazione** | Inviato al fornitore di pagamento, in attesa di conferma | Aspetta il webhook o controlla il dashboard del fornitore |
| **Completato** | Pagamento riuscito, fondi inviati | Nessuna — le commissioni sono contrassegnate come pagate |
| **Fallito** | Pagamento fallito (vedi dettagli dell'errore) | Rivedi l'errore, risolvi il problema, riprova o annulla |
| **Annullato** | Annullato manualmente prima del completamento | Nessuna — le commissioni rimangono non pagate |

### Percorso di successo

In sospeso → In elaborazione → Completato

Questo è il percorso ideale. I webhook del fornitore aggiornano automaticamente lo stato man mano che il pagamento procede.

### Percorso di fallimento

In sospeso → In elaborazione → Fallito

Quando un pagamento fallisce, lo stato del pagamento cambia in Fallito e devi investigare.

## Gestione dei pagamenti falliti

I pagamenti falliti richiedono un intervento manuale. Causa comuni di fallimento:

| Causa | Errore del fornitore | Soluzione |
|-------|----------------------------------|----------|
| Account non valido | "Account del destinatario non trovato" | Verifica l'e-mail di pagamento o i dettagli bancari dell'affiliato |
| Saldo insufficiente | "Fondi insufficienti" | Aggiungi fondi al tuo account del fornitore |
| Errore nei dettagli bancari | "Numero di routing non valido" | Chiedi all'affiliato di aggiornare le informazioni bancarie |
| Restrizione dell'account | "Il destinatario non può ricevere pagamenti" | Contatta l'affiliato per risolvere lo stato del loro account |
| Problema del fornitore | "Servizio temporaneamente non disponibile" | Aspetta e riprova dopo alcune ore |

### Come riprovare un pagamento fallito

1. **Visualizza il pagamento fallito** — Clicca su di esso nell'elenco
2. **Leggi il messaggio di errore** — Controlla il campo **Risposta del fornitore** per i dettagli
3. **Risolvi il problema sottostante** — Aggiorna i dettagli dell'affiliato, aggiungi fondi al fornitore, ecc.
4. **Reimposta lo stato** — Cambia lo stato di nuovo in In sospeso (modulo di modifica)
5. **Elabora nuovamente** — Utilizza l'azione **Elabora con fornitore**

### Come annullare e ricreare

Se il riprovare non funziona:

1. **Apri il pagamento fallito**
2. **Cambia lo stato in Annullato**
3. **Salva il pagamento**
4. **Crea un nuovo pagamento** — Segui nuovamente i passaggi di creazione
5. **Elabora il nuovo pagamento**

I pagamenti annullati non contrassegnano le commissioni come pagate, quindi rimangono eleggibili per nuovi pagamenti.

## Integrazione con i fornitori di pagamento

L'elaborazione dei pagamenti richiede un account del fornitore di pagamento configurato. Spwig si integra con:

- **API PayPal Payouts** — Per i pagamenti PayPal
- **Airwallex** — Per i trasferimenti bancari internazionali

### Requisiti di configurazione

Prima di elaborare i pagamenti:
1. Configura almeno un fornitore in **Impostazioni > Fornitori di pagamento**
2. Aggiungi le credenziali API (ID client, segreto, chiave API)
3. Imposta la modalità di produzione (sandbox per i test)
4. Configura l'URL del webhook nel dashboard del fornitore
5. Verifica la connettività con un pagamento di test

Vedi la guida [Configurazione del fornitore di pagamento](#) per le istruzioni dettagliate di configurazione.

### Selezione del fornitore da parte dell'affiliato

Gli affiliati scelgono il loro metodo di pagamento preferito nel loro dashboard:
- PayPal: Inserisci `payment_email`
- Trasferimento bancario: Inserisci i dettagli dell'account bancario

Il sistema instrada automaticamente i pagamenti al fornitore corrispondente.

## Linee guida per l'orario dei pagamenti

Stabilisci un orario regolare per i pagamenti per costruire la fiducia con gli affiliati:

| Orario | Frequenza | Carico di lavoro | Soddisfazione degli affiliati | Consigliato per |
|----------|-----------|----------|------------------------|-----------------|
| Settimanale | Ogni venerdì | Elevato | Eccellente | Nuovi programmi, alto volume |
| Bimensile | 1° e 15° del mese | Medio | Buono | Programmi a volume medio |
| Mensile | 1° del mese | Basso | Accettabile | Programmi consolidati |
| Trimestrale | Ogni 3 mesi | Molto basso | Scarsa | Non consigliato |

Considera la dimensione del tuo programma e la capacità amministrativa quando scegli un orario.

## Linee guida per l'elaborazione

Segui queste linee guida per operazioni di pagamento fluide:

- **Elabora i pagamenti in base all'orario** — Elabora tutti i pagamenti idonei nello stesso giorno ogni settimana/mese
- **Verifica i dettagli prima dell'elaborazione** — Controlla nuovamente le informazioni di pagamento degli affiliati, soprattutto per importi elevati
- **Monitora il saldo del fornitore** — Assicurati che ci siano fondi sufficienti nel tuo account PayPal/Airwallex
- **Imposta i limiti minimi chiari** — Comunica i minimi di pagamento nei termini del programma ($50-$100 tipici)
- **Documenta il tuo orario** — Aggiungi l'orario dei pagamenti ai termini degli affiliati e alle impostazioni del portale
- **Utilizza l'elaborazione tramite fornitore** — Evita l'elaborazione manuale a meno che non sia assolutamente necessario
- **Rivedi immediatamente i pagamenti falliti** — Risolvi i fallimenti entro 24 ore
- **Mantieni configurati i webhook del fornitore** — I webhook abilitano gli aggiornamenti automatici dello stato
- **Esporta regolarmente i report dei pagamenti** — Scarica i report mensili per la contabilità

## Registri dei pagamenti e reporting

Ogni pagamento crea un registro immutabile con:
- Informazioni sull'affiliato
- ID delle commissioni incluse
- Importo totale
- Metodo e fornitore di pagamento
- Timestamp di creazione e completamento
- ID della transazione del fornitore (dopo l'elaborazione)
- Dati della risposta del fornitore (per il debug)
- Note interne

Accedi a questi dati cliccando su qualsiasi pagamento nell'elenco. Utilizza il funzionalità di esportazione dell'interfaccia amministrativa per scaricare i report dei pagamenti per scopi contabili o fiscali.

## Consigli

- Elabora i pagamenti su un orario fisso (ad esempio, ogni venerdì alle 14:00) in modo che gli affiliati sappiano quando aspettarsi il pagamento.
- Utilizza sempre l'elaborazione tramite fornitore invece di quella manuale — è più veloce, più affidabile e crea un registro di audit migliore.
- Imposta i limiti minimi dei pagamenti nei tuoi programmi per ridurre l'overhead amministrativo — $50 o $100 è standard.
- Monitora il saldo del tuo account del fornitore prima di elaborare grandi lotti per evitare fallimenti.
- Testa l'integrazione dei pagamenti in modalità sandbox prima di passare a pagamenti reali.
- Aggiungi una nota a ogni pagamento che spieghi il periodo che copre (es. "Commissioni per gennaio 2026").
- Controlla immediatamente i pagamenti falliti — i ritardi frustrano gli affiliati e danneggiano la fiducia.
- Comunica proattivamente i ritardi — se non puoi elaborare in orario, notifica in anticipo gli affiliati interessati.

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.