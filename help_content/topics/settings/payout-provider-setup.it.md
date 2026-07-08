---
title: Configurazione del Fornitore di Pagamenti
---

La configurazione del fornitore di pagamenti ti permette di configurare PayPal e Airwallex per i pagamenti automatici agli affiliati. Questa guida ti mostra come collegare i tuoi account dei fornitori di pagamento, configurare i webhooks e testare l'integrazione.

## Fornitori di Pagamenti Supportati

Spwig si integra con due fornitori di pagamenti per automatizzare i pagamenti agli affiliati:

| Fornitore | Metodo di Pagamento | Elaborazione | Supporto Batch | Migliore Per |
|----------|----------------|------------|---------------|----------|
| **PayPal** | Trasferimenti tramite account PayPal | Basato sull'API | Sì (fino a 15.000) | La maggior parte degli affiliati, portata globale |
| **Airwallex** | Trasferimenti bancari internazionali | Basato sull'API | No (singoli) | Trasferimenti bancari, pagamenti internazionali |

### Differenze Principali

**Pagamenti PayPal**:
- Richiede che gli affiliati abbiano un account PayPal (indirizzo email di pagamento)
- Elabora batch di fino a 15.000 pagamenti alla volta
- Elaborazione più rapida (1-2 giorni lavorativi)
- Complessità di configurazione inferiore
- Costi: ~2% o $0,25-$1,00 per pagamento
- Un singolo webhook per l'intero batch

**Airwallex**:
- Supporta trasferimenti bancari diretti
- Elabora singoli pagamenti uno alla volta
- Elaborazione più lunga (2-5 giorni lavorativi)
- Supporta diverse valute e paesi
- I costi variano in base al paese di destinazione
- Webhook individuale per ogni pagamento

Puoi configurare entrambi i fornitori e permettere agli affiliati di scegliere il metodo di pagamento preferito.

## Perché Usare Fornitori di Pagamenti?

L'integrazione dei fornitori di pagamento offre vantaggi significativi rispetto ai pagamenti manuali:

- **Elaborazione automatica** — Nessuna digitazione manuale o esecuzione dei pagamenti
- **Efficienza batch** — Elabora decine o centinaia di pagamenti con un clic
- **Conferme tramite webhook** — Aggiornamenti automatici dello stato quando i pagamenti vengono completati
- **Meno errori** — Il sistema verifica i dettagli dell'account prima dell'elaborazione
- **Tracciamento delle operazioni** — Registri completi delle transazioni e delle risposte del fornitore
- **Pagamenti più veloci** — Gli affiliati ricevono i fondi più rapidamente
- **Scalabilità** — Gestisci programmi di affiliati in crescita senza un lavoro amministrativo proporzionale

Senza l'integrazione del fornitore, devi elaborare ogni pagamento manualmente tramite il tuo banco o il pannello di controllo PayPal, quindi tornare a Spwig per contrassegnare i pagamenti come completati.

## Configurazione di PayPal

Segui questi passaggi per configurare i pagamenti automatici tramite PayPal.

### Requisiti Preparatori

Prima di iniziare, hai bisogno di:
- Un account PayPal Business (gli account personali non possono utilizzare l'API dei pagamenti)
- Accesso al [Pannello di Controllo dello Sviluppatore di PayPal](https://developer.paypal.com/dashboard/)
- Approvazione per l'API dei pagamenti (dopo i test in ambiente sandbox)

### Passaggio 1: Creare un App PayPal

1. **Naviga** verso [Pannello di Controllo dello Sviluppatore di PayPal](https://developer.paypal.com/dashboard/)
2. **Accedi** con il tuo account PayPal Business
3. **Clicca** su **Le mie App e Credenziali** nel menu laterale
4. **Seleziona** la scheda **Live** (o Sandbox per i test)
5. **Clicca** su **Crea App**
6. **Inserisci il nome dell'app** (es. "Pagamenti Affiliati Spwig")
7. **Seleziona il tipo di app**: Merchant
8. **Clicca** su **Crea App**

PayPal genera le tue credenziali.

### Passaggio 2: Ottenere le Credenziali API

Dopo aver creato l'app:

1. **Copia l'ID Client** — Una lunga stringa alfanumerica
2. **Clicca** su **Mostra** sotto Segreto
3. **Copia il Client Secret** — Mantienilo riservato
4. **Nota la modalità** — Sandbox o Live

### Passaggio 3: Abilitare la Funzione di Pagamenti

Le app PayPal richiedono un'autorizzazione esplicita per utilizzare i pagamenti:

1. **Scorri** fino alla sezione **Funzionalità** della tua app
2. **Cerca** la funzione **Pagamenti**
3. **Clicca** su **Aggiungi** se non è già abilitata
4. **Invia per l'approvazione** se stai utilizzando la modalità Live (l'approvazione richiede 1-2 giorni lavorativi)

### Passaggio 4: Aggiungere il Fornitore in Spwig

Ora aggiungi l'account PayPal a Spwig:

1. **Naviga** verso **Impostazioni > Fornitori di Pagamenti**
2. **Clicca** su **+ Aggiungi account PayPal**
3. **Compila il modulo**:
   - **Nome account**: Etichetta descrittiva (es. "Account PayPal Principale")
   - **ID Client**: Incolla dal pannello di controllo dello sviluppatore di PayPal
   - **Client Secret**: Incolla dal pannello di controllo dello sviluppatore di PayPal
   - **Modalità**: Seleziona Sandbox (test) o Produzione (live)
   - **Attivo**: Spunta per abilitare
4. **Clicca Salva**

Spwig verifica le credenziali richiedendo un token di accesso. Se la verifica fallisce, controlla nuovamente l'ID Client e il Secret.

### Passaggio 5: Testare la Connessione

Verifica l'integrazione di PayPal:

1. Crea un pagamento di test in **Programma di Affiliazione > Pagamenti**
2. Usa il tuo proprio indirizzo email PayPal come destinatario
3. Imposta l'importo a $0,01 (se in Produzione) o qualsiasi importo (se Sandbox)
4. Elabora con il fornitore
5. Controlla l'account PayPal per i pagamenti ricevuti
6. Verifica che il webhook aggiorni lo stato del pagamento in Spwig

Se utilizzi la modalità Sandbox, crea un account PayPal di test a [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) per ricevere i pagamenti di test.

## Configurazione di Airwallex

Airwallex supporta i trasferimenti bancari internazionali per gli affiliati che preferiscono il deposito diretto.

### Requisiti Preparatori

Prima di iniziare, hai bisogno di:
- Un account Airwallex (crea a [airwallex.com](https://www.airwallex.com))
- Lo stato dell'account aziendale verificato
- L'accesso all'API abilitato (contatta il supporto di Airwallex se necessario)
- Saldo sufficiente nell'account Airwallex

### Passaggio 1: Generare le Credenziali API

1. **Accedi** al [Pannello di Controllo di Airwallex](https://www.airwallex.com/app/)
2. **Naviga** verso **Impostazioni > Chiavi API**
3. **Clicca** su **Crea Chiave API**
4. **Inserisci una descrizione**: "Pagamenti Affiliati Spwig"
5. **Seleziona i permessi**: Abilita **Pagamenti** (lettura e scrittura)
6. **Clicca** su **Genera**
7. **Copia la Chiave API** — Mostrata una sola volta
8. **Copia l'ID Client** — Visualizzato con la chiave

### Passaggio 2: Notare il Tuo Ambiente

Airwallex fornisce due ambienti:

- **Demo**: Per test con transazioni finte
- **Produzione**: Per trasferimenti con denaro reale

Assicurati di sapere a quale ambiente appartiene la tua chiave API.

### Passaggio 3: Aggiungere il Fornitore in Spwig

Aggiungi l'account Airwallex a Spwig:

1. **Naviga** verso **Impostazioni > Fornitori di Pagamenti**
2. **Clicca** su **+ Aggiungi account Airwallex**
3. **Compila il modulo**:
   - **Nome account**: Etichetta descrittiva (es. "Account Airwallex EUR")
   - **Chiave API**: Incolla dal pannello di controllo di Airwallex
   - **ID Client**: Incolla dal pannello di controllo di Airwallex
   - **Ambiente**: Seleziona Demo o Produzione
   - **Attivo**: Spunta per abilitare
4. **Clicca Salva**

Spwig verifica le credenziali interrogando il saldo del tuo account.

### Passaggio 4: Verificare i Paesi Supportati

Airwallex supporta i trasferimenti a molti paesi ma non a tutti. Controlla la pagina [Copertura di Airwallex](https://www.airwallex.com/global-business-account/global-transfers) per confermare che i paesi dei tuoi affiliati siano supportati.

I paesi comuni supportati includono:
- Stati Uniti
- Regno Unito
- Paesi dell'Unione Europea
- Australia
- Canada
- Singapore
- Hong Kong

### Passaggio 5: Testare il Trasferimento Bancario

Testa l'integrazione di Airwallex:

1. Crea un pagamento di test per un affiliato con i dettagli bancari
2. Usa un importo piccolo ($1-$5) se in modalità Produzione
3. Elabora con il fornitore
4. Controlla il pannello di controllo di Airwallex per la transazione
5. Aspetta la conferma del webhook
6. Verifica che il pagamento venga completato in Spwig

La modalità Demo elabora immediatamente. La modalità Produzione richiede 2-5 giorni lavorativi.

## Logica di Selezione del Fornitore

Quando elabori un pagamento, Spwig seleziona automaticamente il fornitore appropriato in base al metodo di pagamento dell'affiliato.

### Flusso di Selezione

1. **Verifica il metodo di pagamento dell'affiliato**:
   - Se `payment_email` è impostato → L'affiliato preferisce PayPal
   - Se sono impostati i dettagli bancari → L'affiliato preferisce il trasferimento bancario
2. **Abbinamento al fornitore**:
   - Email PayPal → Utilizza l'account attivo di PayPal
   - Dettagli bancari → Utilizza l'account attivo di Airwallex
3. **Ricaduta al primo disponibile** se il fornitore preferito non è configurato
4. **Mostra un errore** se non esiste alcun fornitore corrispondente

### Account di Fornitore Multipli

Puoi configurare più account per lo stesso fornitore (es. due account PayPal per diverse regioni). Spwig seleziona il primo account attivo che corrisponde al metodo di pagamento. Per controllare quale account viene utilizzato, riordina gli account nell'elenco amministrativo o imposta solo uno come attivo.

## Test dell'Integrazione dei Pagamenti

Testa sempre l'integrazione del fornitore prima di elaborare pagamenti reali agli affiliati.

### Test in Modalità Sandbox/Demo

1. **Imposta il fornitore in modalità sandbox** (PayPal Sandbox o Airwallex Demo)
2. **Crea un affiliato di test** con dettagli di pagamento di test
3. **Crea commissioni di test** e approvalele
4. **Crea un pagamento di test** che includa quelle commissioni
5. **Elabora con il fornitore** utilizzando il menu delle azioni
6. **Monitora i log di Celery** per le richieste API
7. **Controlla il pannello del fornitore** per la transazione
8. **Aspetta il webhook** per aggiornare lo stato del pagamento
9. **Verifica che le commissioni siano contrassegnate come pagate**

### Test in Produzione

Prima di passare in produzione:

1. **Passa alla modalità produzione** nelle impostazioni del fornitore
2. **Crea un piccolo pagamento di test** a te stesso ($0,01-$1,00)
3. **Elabora** e attendi il completamento
4. **Verifica che i fondi siano ricevuti** nel tuo account
5. **Controlla che il webhook sia stato attivato** e che lo stato sia aggiornato
6. **Rivedi le commissioni del fornitore**

### Problemi Comuni durante i Test

| Problema | Causa | Soluzione |
|-------|-------|----------|
| "Credenziali non valide" | Chiave API errata o mismatch di modalità | Ricontrolla le credenziali, verifica sandbox vs produzione |
| Webhook mai attivato | URL non configurato nel fornitore | Aggiungi l'URL del webhook nel pannello del fornitore |
| Pagamento rimane in Elaborazione | Firma del webhook fallita | Controlla che il segreto del webhook corrisponda |
| Nessun fornitore disponibile | Nessun fornitore attivo per il metodo di pagamento | Abilita almeno un account del fornitore |

## Elaborazione in Batch (PayPal)

PayPal supporta l'elaborazione in batch per efficienza e risparmio di costi.

### Funzionamento del Batch

Quando selezioni diversi pagamenti e clicchi su **Elabora con Fornitore**:

1. Spwig raggruppa tutti i pagamenti PayPal in un singolo batch
2. Il sistema invia una singola richiesta API con tutti i dettagli dei pagamenti (fino a 15.000)
3. PayPal elabora l'intero batch come una singola transazione
4. Il webhook restituisce i risultati del batch
5. Spwig aggiorna tutti i pagamenti in base alla risposta del batch

### Vantaggi del Batch

- **Meno richieste API** — Una richiesta per centinaia di pagamenti
- **Costi inferiori** — Alcune strutture dei costi di PayPal favoriscono l'elaborazione in batch
- **Elaborazione più rapida** — Esecuzione parallela per l'intero batch
- **Un singolo webhook** — Più facile monitoraggio e log

### Limiti del Batch

PayPal impone questi limiti:
- Massimo 15.000 destinatari per batch
- Massimo $100.000 totali per batch
- L'elaborazione si completa tipicamente in pochi minuti

Se superi i 15.000 pagamenti, Spwig divide automaticamente in diversi batch.

## Elaborazione Individuale (Airwallex)

Airwallex elabora i pagamenti uno alla volta, che offre diversi compromessi.

### Funzionamento dell'Elaborazione Individuale

Quando elabori i pagamenti Airwallex:

1. Il sistema invia una richiesta API separata per ogni pagamento
2. Airwallex inserisce i trasferimenti in coda individualmente
3. Ogni trasferimento si completa in modo indipendente (2-5 giorni)
4. Un webhook individuale viene attivato quando ogni trasferimento si completa
5. Spwig aggiorna i pagamenti quando arrivano i webhook

### Vantaggi dell'Elaborazione Individuale

- **Migliore isolamento degli errori** — Un fallimento non blocca gli altri
- **Tracciamento per pagamento** — ID transazione individuale
- **Maggiori dettagli del pagamento** — Informazioni specifiche per ogni trasferimento bancario
- **Orario flessibile** — I trasferimenti si completano a velocità diverse

### Tempo di Elaborazione

A differenza dell'elaborazione batch istantanea di PayPal, i trasferimenti Airwallex richiedono più tempo:
- Trasferimenti nazionali: 1-2 giorni lavorativi
- Trasferimenti internazionali: 3-5 giorni lavorativi
- Alcuni paesi: Fino a 7 giorni lavorativi

Imposta le aspettative degli affiliati di conseguenza nei termini del tuo programma.

## Configurazione dei Webhook

I webhook permettono agli aggiornamenti automatici dello stato dei pagamenti quando i fornitori completano le transazioni.

### Formato dell'URL del Webhook

Configura questo URL nel pannello del fornitore:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Sostituisci `{provider}` con:
- `paypal` per i webhook di PayPal
- `airwallex` per i webhook di Airwallex

Esempi:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### Configurazione del Webhook di PayPal

1. **Naviga** verso [Pannello di Controllo dello Sviluppatore di PayPal](https://developer.paypal.com/dashboard/)
2. **Clicca** sul nome della tua app
3. **Scorri** fino alla sezione **Webhook**
4. **Clicca** su **Aggiungi Webhook**
5. **Inserisci l'URL del webhook** (formato sopra)
6. **Seleziona gli eventi**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Clicca Salva**

PayPal fornisce una chiave di firma del webhook. Spwig utilizza questa per verificare l'autenticità del webhook.

### Configurazione del Webhook di Airwallex

1. **Naviga** verso [Pannello di Controllo di Airwallex](https://www.airwallex.com/app/)
2. **Vai a** **Impostazioni > Webhook**
3. **Clicca** su **Crea Webhook**
4. **Inserisci l'URL del webhook** (formato sopra)
5. **Seleziona gli eventi**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Clicca Crea**

Airwallex firma i webhook con il tuo segreto API.

### Sicurezza dei Webhook

I webhook vengono verificati utilizzando questi meccanismi:

- **Verifica della firma** — Il fornitore firma il payload del webhook con una chiave segreta
- **Controllo del timestamp** — Rifiuta i webhook vecchi (prevenzione degli attacchi di replay)
- **Elenco IP consentiti** (opzionale) — Limita ai range IP del fornitore
- **Richiesto HTTPS** — I webhook funzionano solo su SSL

Mai disabilitare la verifica della firma in produzione.

### Test dei Webhook

La maggior parte dei fornitori offre strumenti per testare i webhook:

**PayPal**: Utilizza il "Simulatore" nel pannello di controllo dello sviluppatore per attivare webhook di test

**Airwallex**: Crea un trasferimento di test in modalità Demo e osserva il webhook

Puoi anche controllare i log dei webhook in Spwig a **Impostazioni > Log del Sistema** (se i log sono abilitati).

## Risoluzione dei Problemi

### Errore di Credenziali Non Valide

**Sintomo**: "Autenticazione fallita" quando si salva l'account del fornitore

**Causa**:
- ID Client o Secret errati
- Credenziali di sandbox utilizzate in modalità produzione (o viceversa)
- Chiave API scaduta o revocata
- Account non verificato

**Soluzioni**:
- Ri-copia le credenziali dal pannello del fornitore
- Verifica che la modalità corrisponda (sandbox vs produzione)
- Rigenera le chiavi API
- Contatta il supporto del fornitore per verificare lo stato dell'account

### Webhook Non Ricevuti

**Sintomo**: Pagamento bloccato nello stato "Elaborazione" indefinitamente

**Causa**:
- URL del webhook non configurato nel pannello del fornitore
- Certificato SSL non valido
- Firewall che blocca gli IP del fornitore
- Verifica della firma del webhook fallita

**Soluzioni**:
- Controlla nuovamente l'URL del webhook nelle impostazioni del fornitore
- Verifica che il certificato SSL sia valido
- Whitelista gli IP del fornitore nel firewall
- Controlla i log di Celery per errori di firma
- Testa il webhook con lo strumento di simulazione del fornitore

### Pagamento Fallito

**Sintomo**: Lo stato del pagamento cambia in "Fallito" con un messaggio di errore

**Causa**:
- Dettagli di pagamento non validi dell'affiliato (email o account bancario errati)
- Saldo insufficiente nell'account del fornitore
- Account del destinatario non può ricevere pagamenti
- Paese non supportato (Airwallex)
- Pagamento supera i limiti del fornitore

**Soluzioni**:
- Controlla l'errore nel campo **Risposta del Fornitore**
- Verifica che i dettagli di pagamento dell'affiliato siano corretti
- Aggiungi fondi all'account del fornitore
- Chiedi all'affiliato di controllare lo stato del loro account
- Controlla il supporto per paese e valuta del fornitore
- Dividi i pagamenti di grandi dimensioni se superano i limiti

### Mismatch di Modalità

**Sintomo**: I pagamenti di test funzionano ma i pagamenti in produzione falliscono

**Causa**:
- Fornitore impostato in modalità Sandbox ma utilizzato con account di affiliati in produzione
- Chiavi API da un ambiente errato

**Soluzioni**:
- Passa la modalità del fornitore a Produzione
- Rigenera le chiavi API per la produzione
- Verifica che l'URL del webhook punti al dominio di produzione

## Pratiche di Sicurezza Consigliate

Proteggi l'integrazione dei pagamenti con queste misure di sicurezza:

### Archiviazione delle Credenziali

- **Non committa mai le credenziali nel controllo delle versioni** — Utilizza variabili d'ambiente o archiviazione sicura
- **Ruota le chiavi API ogni trimestre** — Genera nuove chiavi ogni 3 mesi
- **Utilizza chiavi separate per sandbox e produzione** — Mai mescolare gli ambienti
- **Limita i permessi API** — Concedi solo l'accesso ai pagamenti, non il controllo completo dell'account

Spwig archivia le credenziali del fornitore crittografate nel database. Mantieni i backup del database sicuri.

### Sicurezza dei Webhook

- **Verifica sempre le firme** — Mai saltare la verifica della firma
- **Utilizza esclusivamente HTTPS** — I webhook HTTP non sono supportati
- **Implementa l'elenco IP consentiti** — Limita i webhook ai range IP del fornitore
- **Logga tutti i webhook** — Monitora per attività sospette
- **Limita la frequenza degli endpoint dei webhook** — Previene l'abuso

### Controllo degli Accessi

- **Limita l'accesso del personale** — Solo il personale attendibile deve elaborare i pagamenti
- **Utilizza l'autenticazione a due fattori** — Richiedi la 2FA per gli account del personale
- **Revisa le azioni di pagamento** — Controlla chi ha elaborato quali pagamenti
- **Separa i compiti** — Personale diverso per l'approvazione vs l'elaborazione

### Monitoraggio

- **Controlla i pagamenti falliti quotidianamente** — Risolvi i problemi in modo tempestivo
- **Monitora i saldi degli account dei fornitori** — Assicurati che siano sufficienti
- **Rivedi i log delle transazioni settimanalmente** — Cattura anomalie precocemente
- **Imposta alert** — Notifiche email per pagamenti di grandi dimensioni o falliti

## Consigli

- Testa sempre l'integrazione in modalità sandbox prima di passare alla produzione — cattura problemi con denaro finto.
- Configura entrambi PayPal e Airwallex per dare agli affiliati la scelta del metodo di pagamento — diversi affiliati preferiscono diversi metodi.
- Imposta gli URL dei webhook durante la configurazione iniziale e verifica che vengano attivati correttamente — i webhook sono fondamentali per l'automazione.
- Mantieni i saldi degli account dei fornitori aggiornati per evitare pagamenti falliti durante l'elaborazione in batch.
- Utilizza nomi descrittivi per gli account se configuri più fornitori (es. "Account PayPal USD", "Account PayPal EUR").
- Ruota le credenziali API ogni trimestre come pratica di sicurezza.
- Documenta gli URL dei webhook e le credenziali in un gestore di password sicuro condiviso con il tuo team.
- Monitora immediatamente i pagamenti falliti — i ritardi frustrano gli affiliati e danneggiano la reputazione del programma.
- Utilizza sempre HTTPS per l'installazione di Spwig — i webhook richiedono certificati SSL.
- Contatta il supporto del fornitore se incontri errori persistenti — possono verificare lo stato del tuo account e i permessi.