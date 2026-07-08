---
title: Fornitori di Spedizione
---

I fornitori di spedizione collegano il tuo negozio alle API dei corrieri per ottenere tariffe di spedizione in tempo reale, generazione di etichette e tracciamento dei pacchi. Spwig supporta i principali corrieri in tutto il mondo e consente anche di configurare tabelle di tariffe manuali per i corrieri che non dispongono di integrazioni API.

![Fornitori di spedizione](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Fornitori Disponibili

| Fornitore | Regioni | Funzionalità principali |
|-----------|---------|------------------------|
| **FedEx** | Globale | Tariffe in tempo reale, stampa etichette, tracciamento, multi-pacco |
| **UPS** | Globale | Tariffe in tempo reale, stampa etichette, tracciamento, validazione indirizzo |
| **USPS** | Stati Uniti | Tariffe nazionali e internazionali, tracciamento |
| **NinjaVan** | Sud-est asiatico | Consegna ultima miglia, supporto pagamento in contanti |
| **Canada Post** | Canada | Nazionale e internazionale, tariffe per pacchi e lettere |
| **Australia Post** | Australia | Nazionale e internazionale, pacchi e espressi |

## Connessione a un Fornitore

Accedi a **Impostazioni > Fornitori di spedizione** e clicca su **Connetti Fornitore** per avviare il wizard di configurazione.

### Passo 1: Seleziona Fornitore

Scegli tra i fornitori di spedizione disponibili. Ogni scheda mostra le regioni e le funzionalità supportate dal fornitore.

### Passo 2: Istruzioni di Configurazione

Consulta la guida specifica per la configurazione del fornitore:
- Come creare un account per sviluppatori/aziende con il fornitore
- Dove trovare le credenziali API
- Impostazioni account necessarie (es. numero mittente, numero metro)

### Passo 3: Inserisci Credenziali

Inserisci le credenziali API per il tuo account corriere. I campi richiesti variano in base al fornitore:

- **Chiave API / Segreto** — Credenziali di autenticazione
- **Numero Account** — Il tuo numero di account corriere o mittente
- **Numero Metro** — Richiesto da alcuni fornitori (es. FedEx)
- **Modalità Sandbox** — Abilita per testare con l'API sandbox del fornitore prima di andare live

### Passo 4: Test Connessione

Clicca su **Test Connessione** per verificare le tue credenziali. Il wizard conferma:
- L'autenticazione API ha successo
- Le autorizzazioni dell'account sono valide
- Le query di tariffe restituiscono i risultati previsti

### Passo 5: Configura e Salva

Finalizza le impostazioni:
- **Attivo** — Abilita o disabilita il fornitore
- **Nome Visualizzato** — Il nome mostrato ai clienti al momento del checkout
- **Indirizzo di Origine** — L'indirizzo del magazzino o del centro di smistamento per i calcoli delle tariffe

## Zona di Spedizione

Le zone di spedizione definiscono aree geografiche per i calcoli delle tariffe. Accedi a **Impostazioni > Zone di spedizione** per gestirle.

### Creare una Zona

1. Clicca su **+ Aggiungi Zona**
2. Assegna un nome alla zona (es. "Domestico", "Europa", "Asia-Pacifico")
3. Definisci la copertura della zona utilizzando uno o più di:
   - **Paesi** — Seleziona paesi specifici
   - **Stati/Province** — Ristretto a regioni specifiche all'interno di un paese
   - **Pattern dei codici postali** — Abbinare i codici postali/ZIP utilizzando pattern (es. "90*" per l'area di Los Angeles)
4. Imposta la **Priorità** — Quando le zone si sovrappongono, viene utilizzata la zona con la priorità più alta

### Abbinamento delle Zone

Quando un cliente inserisce il suo indirizzo di spedizione al momento del checkout, il sistema:
1. Verifica i pattern dei codici postali per primi (più specifici)
2. Poi i match di stato/provincia
3. Poi i match di paese
4. Utilizza la zona con la priorità più alta che corrisponde

## Regole di Spedizione

Le regole di spedizione applicano modificatori condizionali alle tariffe di spedizione. Accedi a **Impostazioni > Regole di spedizione** per configurarle.

### Tipi di Regola

| Tipo di Regola | Descrizione |
|----------------|-------------|
| **Sconto %** | Riduci la tariffa di spedizione di una percentuale |
| **Sconto Fisso** | Riduci la tariffa di spedizione di un importo fisso |
| **Imposta Costo** | Sovrascrivi la tariffa con un importo specifico |
| **Spedizione Gratuita** | Imposta la tariffa di spedizione a zero |
| **Sovrapprezzo %** | Aggiungi una percentuale di sovrapprezzo alla tariffa |
| **Sovrapprezzo Fisso** | Aggiungi un sovrapprezzo fisso alla tariffa |

### Condizioni

Ogni regola può avere una o più condizioni che devono essere soddisfatte:

| Condizione | Esempio |
|------------|---------|
| **Valore del Carrello** | Spedizione gratuita per ordini superiori a $100 |
| **Peso Totale** | Sovrapprezzo per ordini superiori a 30 kg |
| **Quantità di Articoli** | Sconto per ordini con 5+ articoli |
| **Zona di Spedizione** | Applica la regola solo alle spedizioni nazionali |
| **Metodo di Spedizione** | Applica a specifici metodi di spedizione del fornitore |
| **Prodotti** | Tariffe speciali per prodotti specifici |
| **Gruppo di Clienti** | I clienti VIP ottengono la spedizione gratuita |
| **Intervallo di Date** | Promozioni di spedizione per le festività |

### Priorità delle Regole

- Le regole vengono valutate in ordine di priorità (da numero più basso a numero più alto)
- **Arresta ulteriori regole** — Quando abilitato, se questa regola corrisponde, non vengono verificate ulteriori regole
- Più regole possono sovrapporsi (es. una regola di sconto del 10% più una regola di soglia per spedizione gratuita)

## Tabelle di Tariffe

Le tabelle di tariffe forniscono prezzi a livelli basati su attributi dell'ordine. Accedi a **Impostazioni > Tabelle di tariffe di spedizione** per configurarle.

### Tipi di Tabelle

Crea livelli di tariffa basati su:
- **Peso** — Livelli di prezzo in base al peso totale dell'ordine (es. 0-1 kg = $5, 1-5 kg = $10)
- **Valore dell'Ordine** — Livelli di prezzo in base al sottototale del carrello
- **Quantità** — Livelli di prezzo in base al numero di articoli

### Creare una Tabella di Tariffe

1. Clicca su **+ Aggiungi Tabella di Tariffe**
2. Assegna un nome alla tabella e seleziona il tipo di livello
3. Aggiungi livelli con intervalli min/max e prezzi
4. Assegna la tabella di tariffa a una zona di spedizione

Le tabelle di tariffe sono utili quando non si utilizzano le tariffe API dei fornitori e si desidera definire una propria struttura di prezzo.

## Pacchetti di Spedizione

Definisci dimensioni standard dei pacchetti per calcoli accurati delle tariffe di spedizione. Accedi a **Impostazioni > Pacchetti di spedizione**.

Per ogni tipo di pacchetto, imposta:
- **Nome** — Descrizione (es. "Scatola Piccola", "Grande Tariffa Flattata")
- **Dimensioni** — Lunghezza, larghezza, altezza
- **Peso Massimo** — Peso massimo che il pacchetto può sostenere
- **Predefinito** — Usa questo pacchetto quando non è assegnato un imballaggio specifico

I fornitori utilizzano le dimensioni del pacchetto per calcolare il peso dimensionale, che può influenzare le tariffe di spedizione.

## Fornitori Manuali (Preimpostazioni Fornitore)

Per i fornitori senza integrazione API, crea preimpostazioni manuali dei fornitori:

1. Accedi a **Impostazioni > Preimpostazioni Fornitore**
2. Clicca su **+ Aggiungi Preimpostazione**
3. Configura:
   - **Nome Fornitore** — Nome visualizzato al momento del checkout
   - **Modello URL di tracciamento** — Modello di URL con un placeholder {tracking_number} (es. `https://track.carrier.com/?id={tracking_number}`)
   - **Consegna stimata** — Intervallo di tempo di consegna da mostrare ai clienti
4. Assegna una tabella di tariffa per la tariffazione

I fornitori manuali forniscono link di tracciamento e stimative di consegna senza integrazione API in tempo reale.

## Spedizione da Multi-Magazzino

Se hai più magazzini, la spedizione può essere calcolata da origini diverse:

- **Magazzino specifico per paese** — Assegna magazzini a paesi specifici per distanze di spedizione più brevi
- **Catena di backup** — Definisci quale magazzino effettua la spedizione quando il magazzino principale è esaurito
- **Assegnamento per prodotto** — Alcuni prodotti potrebbero spedire solo da magazzini specifici

Il sistema seleziona automaticamente il miglior magazzino in base alla posizione del cliente e alla disponibilità del prodotto.

## Consigli

- Connetti le API dei fornitori di spedizione per **tariffe in tempo reale** quando possibile — sono più accurate delle tabelle a tariffa fissa e si adattano a peso, dimensioni e destinazione.
- Crea una **zona di spedizione 'Resto del Mondo'** come opzione di default per i paesi non coperti da zone specifiche.
- Usa il tipo di regola **Spedizione Gratuita** con una condizione sul valore del carrello come incentivo per le vendite (es. "Spedizione gratuita per ordini superiori a $75").
- Testa i calcoli delle tariffe di spedizione con diversi indirizzi e contenuti del carrello prima di andare live.
- Configura **Preimpostazioni Fornitore** con modelli di URL di tracciamento per qualsiasi fornitore locale che non abbia integrazioni API — i clienti ricevono comunque i link di tracciamento.
- Usa **Pacchetti di Spedizione** per ottenere un prezzo preciso del peso dimensionale da fornitori come FedEx e UPS.