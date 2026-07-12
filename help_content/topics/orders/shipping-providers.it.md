---
title: Fornitori di spedizione
---

I fornitori di spedizione collegano il tuo negozio agli API dei corrieri per ottenere tariffe di spedizione in tempo reale, la generazione di etichette e il tracciamento dei pacchi. Spwig supporta i principali corrieri in tutto il mondo e ti permette anche di impostare tabelle di tariffe manuali per i corrieri che non dispongono di un'integrazione API.

![Fornitori di spedizione](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Fornitori disponibili

| Fornitore | Regioni | Funzionalità principali |
|---------|---------|-------------|
| **FedEx** | Globale | Tariffe in tempo reale, stampa etichette, tracciamento, multi-pacco |
| **UPS** | Globale | Tariffe in tempo reale, stampa etichette, tracciamento, validazione indirizzo |
| **USPS** | Stati Uniti | Tariffe nazionali e internazionali, tracciamento |
| **NinjaVan** | Sud-est asiatico | Consegna ultima miglia, supporto pagamento in contanti |
| **Canada Post** | Canada | Nazionale e internazionale, tariffe per pacchi e lettere |
| **Australia Post** | Australia | Nazionale e internazionale, pacchi e espressi |

## Connessione a un Fornitore

Vai a **Impostazioni > Fornitori di spedizione** e fai clic su **Connetti Fornitore** per avviare il wizard di configurazione.

### Passo 1: Seleziona Fornitore

Scegli tra i fornitori di spedizione disponibili. Ogni scheda mostra le regioni e le funzionalità supportate dal fornitore.

### Passo 2: Istruzioni di configurazione

Consulta la guida specifica per il fornitore:
- Come creare un account per sviluppatori/aziende con il fornitore
- Dove trovare le tue credenziali API
- Impostazioni dell'account necessarie (es. numero spedizioniatore, numero metro)

### Passo 3: Inserisci le credenziali

Inserisci le credenziali API per il tuo account del fornitore. I campi richiesti variano in base al fornitore:

- **Chiave API / Segreto** — Credenziali di autenticazione
- **Numero account** — Il tuo numero di account o spedizioniatore del fornitore
- **Numero metro** — Richiesto da alcuni fornitori (es. FedEx)
- **Modalità sandbox** — Abilita per testare con l'API sandbox del fornitore prima di andare in produzione

### Passo 4: Test della connessione

Fai clic su **Test Connessione** per verificare le tue credenziali. Il wizard conferma:
- L'autenticazione API ha successo
- Le autorizzazioni dell'account sono valide
- Le query di tariffe restituiscono i risultati previsti

### Passo 5: Configura e salva

Finalizza le impostazioni:
- **Attivo** — Abilita o disabilita il fornitore
- **Nome visualizzato** — Il nome mostrato ai clienti durante il checkout
- **Indirizzo di origine** — L'indirizzo del magazzino o di spedizione utilizzato per il calcolo delle tariffe

## Zone di spedizione

Le zone di spedizione definiscono aree geografiche per il calcolo delle tariffe. Vai a **Impostazioni > Zone di spedizione** per gestirle.

### Creare una zona

1. Fai clic su **+ Aggiungi zona**
2. Assegna un nome alla zona (es. "Domestico", "Europa", "Asia-Pacifico")
3. Definisci l'area di copertura utilizzando uno o più dei seguenti:
   - **Paesi** — Seleziona paesi specifici
   - **Stati/Province** — Ristretto a regioni specifiche all'interno di un paese
   - **Pattern dei codici postali** — Corrispondenza dei codici postali/ZIP utilizzando pattern (es. "90*" per l'area di Los Angeles)
4. Imposta la **Priorità** — Quando le zone si sovrappongono, viene utilizzata la zona con la priorità più alta

### Corrispondenza delle zone

Quando un cliente inserisce l'indirizzo di spedizione durante il checkout, il sistema:
1. Controlla i pattern dei codici postali per primi (più specifici)
2. Poi le corrispondenze di stato/provincia
3. Poi le corrispondenze di paese
4. Utilizza la zona con la priorità più alta corrispondente

## Promozioni di spedizione

Le promozioni di spedizione applicano modificatori condizionali alle tariffe di spedizione. Vai a **Impostazioni > Promozioni di spedizione** per configurarle.

### Tipi di promozione

| Tipo di promozione | Descrizione |
|-----------|-------------|
| **Sconto %** | Riduci la tariffa di spedizione di una percentuale |
| **Sconto fisso** | Riduci la tariffa di spedizione di un importo fisso |
| **Sovrascrivi costo** | Sovrascrivi la tariffa con un importo specifico |
| **Spedizione gratuita** | Imposta il costo di spedizione a zero |
| **Sovrapprezzo %** | Aggiungi una percentuale di sovrapprezzo alla tariffa |
| **Sovrapprezzo fisso** | Aggiungi un sovrapprezzo fisso alla tariffa |

### Condizioni

Ogni promozione può avere una o più condizioni che devono essere soddisfatte:

| Condizione | Esempio |
|-----------|---------|
| **Valore del Carrello** | Spedizione gratuita per ordini superiori a $100 |
| **Peso Totale** | Extra per ordini superiori a 30 kg |
| **Numero di Articoli** | Sconto per ordini con 5+ articoli |
| **Zona di Spedizione** | Applica la promozione solo per spedizioni nazionali |
| **Metodo di Spedizione** | Applica a metodi specifici di carrier |
| **Prodotti** | Tariffe speciali per prodotti specifici |
| **Gruppo di Clienti** | I clienti VIP hanno la spedizione gratuita |
| **Intervallo di Date** | Promozioni di spedizione per festività |

### Priorità delle Promozioni

- Le promozioni vengono valutate nell'ordine di priorità (da numero più basso a numero più alto)
- **Interrompi ulteriori promozioni** — Quando abilitato, se questa promozione corrisponde, non vengono verificate altre promozioni
- Più promozioni possono sovrapporsi (es. una promozione di sconto del 10% più una promozione di spedizione gratuita con un limite di valore)

## Tabelle di Tariffa

Le tabelle di tariffa forniscono prezzi a scaglioni in base agli attributi dell'ordine. Passa a **Impostazioni > Tabelle di Tariffa di Spedizione** per configurarle.

### Tipi di Tabelle

Crea scaglioni di tariffa in base a:
- **Peso** — Scaglioni di prezzo in base al peso totale dell'ordine (es. 0-1 kg = $5, 1-5 kg = $10)
- **Valore dell'Ordine** — Scaglioni di prezzo in base al sottototale del carrello
- **Quantità** — Scaglioni di prezzo in base al numero di articoli

### Creare una Tabella di Tariffa

1. Clicca su **+ Aggiungi Tabella di Tariffa**
2. Assegna un nome alla tabella e seleziona il tipo di scaglione
3. Aggiungi scaglioni con intervalli min/max e prezzi
4. Assegna la tabella di tariffa a una zona di spedizione

Le tabelle di tariffa sono utili quando non si utilizzano le tariffe API dei carrier e si desidera definire una propria struttura di prezzo.

## Pacchetti di Spedizione

Definisci dimensioni standard di imballaggio per calcoli di tariffa accurati. Passa a **Impostazioni > Pacchetti di Spedizione**.

Per ogni tipo di pacchetto, imposta:
- **Nome** — Descrizione (es. "Scatola Piccola", "Grande a Tariffa Fissa")
- **Dimensioni** — Lunghezza, larghezza, altezza
- **Peso Massimo** — Peso massimo che il pacchetto può contenere
- **Predefinito** — Usa questo pacchetto quando non è assegnato un imballaggio specifico

I carrier utilizzano le dimensioni del pacchetto per calcolare il peso dimensionale, che può influenzare le tariffe di spedizione.

## Carrier Manuali (Preimpostazioni Carrier)

Per carrier senza integrazione API, crea preimpostazioni manuali per carrier:

1. Passa a **Impostazioni > Preimpostazioni Carrier**
2. Clicca su **+ Aggiungi Preimpostazione**
3. Configura:
   - **Nome del Carrier** — Nome visualizzato durante il checkout
   - **Modello dell'URL di Tracciamento** — Modello URL con un segnaposto {tracking_number} (es. `https://track.carrier.com/?id={tracking_number}`)
   - **Consegna Stimata** — Intervallo di tempo di consegna da visualizzare ai clienti
4. Associa una tabella di tariffa per i prezzi

I carrier manuali forniscono link di tracciamento e stimative di consegna senza integrazione API in tempo reale.

## Spedizione da Multi-Deposito

Se hai più depositi, la spedizione può essere calcolata da origini diverse:

- **Deposito Specifico per Paese** — Assegna depositi a paesi specifici per distanze di spedizione più brevi
- **Catena di Riserva** — Definisci quale deposito effettua la spedizione quando il deposito principale è esaurito
- **Assegnamento per Prodotto** — Alcuni prodotti possono spedire solo da depositi specifici

Il sistema seleziona automaticamente il miglior deposito in base alla posizione del cliente e alla disponibilità del prodotto.

## Consigli

- Connetti le API dei carrier per **tariffe in tempo reale** quando possibile — sono più accurate delle tabelle a tariffa fissa e si adattano al peso, alle dimensioni e alla destinazione.
- Crea una **zona di spedizione "Resto del Mondo"** come opzione di default per i paesi non coperti da zone specifiche.
- Usa il tipo di promozione **Spedizione Gratuita** con una condizione di valore del carrello come incentivo per le vendite (es. "Spedizione gratuita per ordini superiori a $75").
- Testa i calcoli delle tariffe di spedizione con indirizzi e contenuti del carrello diversi prima di andare online.
- Configura **Preimpostazioni Carrier** con modelli URL di tracciamento per qualsiasi carrier locale che non abbia integrazioni API — i clienti ricevono comunque i link di tracciamento.
- Usa **Pacchetti di Spedizione** per ottenere prezzi accurati per il peso dimensionale da carrier come FedEx e UPS.