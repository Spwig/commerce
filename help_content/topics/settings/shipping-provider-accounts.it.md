---
title: Shipping Provider Accounts
---

Le account dei fornitori di spedizione collegano il tuo negozio agli API dei corrieri (FedEx, UPS, DHL) per il calcolo in tempo reale delle tariffe e l'acquisto automatico delle etichette. Ogni account memorizza le credenziali API crittografate, monitora lo stato della connessione e si collega ai metodi di spedizione in tempo reale. I fornitori recuperano le tariffe in tempo reale al momento del checkout in base alle dimensioni del pacco, al peso, all'origine e alla destinazione - eliminando la manutenzione manuale delle tabelle delle tariffe e assicurando un prezzo corretto del corriere.

Utilizza gli account dei fornitori quando hai bisogno di tariffe di spedizione calcolate dal corriere o di generazione automatica delle etichette invece della creazione manuale delle spedizioni.

## Fornitori di spedizione supportati

Spwig supporta i principali corrieri tramite componenti installabili dei fornitori:

### FedEx

**Servizi**: Ground, Express, Internazionale
**API**: FedEx Web Services
**Funzionalità**: Tariffe in tempo reale, acquisto etichette, tracciamento, documenti doganali internazionali

### UPS

**Servizi**: Ground, Air, Worldwide
**API**: UPS Developer API
**Funzionalità**: Tariffe in tempo reale, generazione etichette, tracciamento, validazione indirizzi

### DHL

**Servizi**: Express, eCommerce, Internazionale
**API**: DHL Express API
**Funzionalità**: Tariffe internazionali, documenti doganali, tracciamento

### Altri fornitori

Installa dal marketplace dei componenti quando necessario (USPS, Canada Post, Australia Post, ecc.)

---

## Configurazione dell'account del fornitore

Ogni account del fornitore richiede:

### Informazioni di base

- **Nome visualizzato**: Come appare l'account nell'amministrazione (es. "FedEx Production Account")
- **Fornitore**: Seleziona il componente del fornitore installato dal menu a discesa
- **Attivo**: Toggle per abilitare/disabilitare senza eliminare le credenziali
- **Predefinito**: Imposta come account predefinito per questo fornitore (solo un account predefinito per fornitore)

### Credenziali API (Crittografate)

**Variano in base al fornitore**, tipicamente includono:

**FedEx**:
- Numero account
- Numero metro
- Chiave API
- Segreto API

**UPS**:
- Numero di licenza di accesso
- ID utente
- Password
- Numero account

**DHL**:
- ID sito
- Password
- Numero account

**Tutte le credenziali sono crittografate a riposo** e vengono decrittografate solo quando si effettuano chiamate API.

### Indirizzo di origine

- **Indirizzo di spedizione predefinito**: Indirizzo del magazzino/origine per il calcolo delle tariffe
- Alcuni fornitori richiedono una configurazione specifica dell'origine nel loro dashboard

### Impostazioni

Opzioni specifiche del fornitore (variano in base al corriere):

- **Modalità di test**: Utilizza gli endpoint API di sandbox/test del corriere
- **Tariffe negoziate**: Utilizza le tariffe negoziate con il corriere (se disponibili)
- **Includi assicurazione**: Offri automaticamente l'assicurazione nelle tariffe
- **Sovrapprezzo residenziale**: Applica le spese di consegna residenziale
- **Firma richiesta**: Requisiti di firma predefiniti

---

## Creazione di un account del fornitore

**Processo di configurazione a 6 passaggi**:

**Passaggio 1: Ottenere l'accesso all'API del corriere**
1. Crea un account con il corriere (FedEx.com, UPS.com, DHL.com)
2. Richiedi l'accesso API/Developer
3. Completa l'onboarding API del corriere (potrebbe richiedere 1-3 giorni lavorativi)
4. Ricevi le credenziali API via email o portale dello sviluppatore

**Passaggio 2: Installa il componente del fornitore** (se non preinstallato)
1. Vai a Impostazioni > Componenti > Marketplace
2. Cerca il nome del corriere (es. "FedEx")
3. Installa il componente del fornitore di spedizione
4. Attendere il completamento dell'installazione

**Passaggio 3: Crea un account del fornitore in Spwig**
1. Naviga su Impostazioni > Spedizione > Account Fornitori
2. Clicca su "Aggiungi account fornitore"
3. Seleziona il fornitore dal menu a discesa
4. Inserisci il nome visualizzato

**Passaggio 4: Inserisci le credenziali API**
1. Compila i campi delle credenziali (variano in base al fornitore)
2. Le credenziali vengono crittografate automaticamente al salvataggio
3. Opzionale: Abilita la modalità di test per i test iniziali

**Passaggio 5: Testa la connessione**
1. Clicca sul pulsante "Test Connection"
2. Il sistema tenta di effettuare una chiamata API al corriere
3. Verifica che lo stato "Connected" appaia
4. Controlla il timestamp last_tested_at

**Passaggio 6: Collega a un metodo di spedizione**
1. Crea o modifica un metodo di spedizione (Impostazioni > Carrello > Metodi di spedizione)
2. Imposta method_type = "Real-Time"
3. Seleziona l'account del fornitore dal menu a discesa
4. Salva il metodo

---

## Monitoraggio dello stato della connessione

Gli account dei fornitori monitorano lo stato della connessione:

### Valori di stato

**Sconosciuto** (grigio): Mai testato o non ancora connesso

**Connesso** (verde): Ultima chiamata API riuscita, credenziali valide

**Errore** (rosso): Ultima chiamata API fallita, credenziali potrebbero non essere valide

### Ultimo test effettuato

- **Timestamp**: Quando è stata verificata l'ultima connessione
- **Aggiornamento automatico**: Ogni volta che si utilizza il fornitore (recupero tariffe, acquisto etichette)
- **Test manuale**: Clicca sul pulsante "Test Connection" in qualsiasi momento

### Risoluzione dei problemi con connessioni fallite

**Causa comune**:
- Credenziali API errate (errore di battitura, copiate con spazio extra)
- Chiave API del corriere scaduta o revocata
- Modalità di test abilitata ma si utilizzano credenziali di produzione (o viceversa)
- Indirizzo IP non elencato nel white list del corriere
- Interruzione del servizio API del corriere

**Passaggi per la soluzione**:
1. Verifica che le credenziali corrispondano esattamente al dashboard del corriere
2. Controlla che l'impostazione della modalità di test corrisponda al tipo di credenziali
3. Controlla la pagina di stato dell'API del corriere per eventuali interruzioni
4. Contatta il supporto del corriere per la verifica dell'account

---

## Flusso di lavoro per la ricerca delle tariffe

Come funzionano le tariffe in tempo reale al momento del checkout:

**1. Il cliente inserisce l'indirizzo**
- Inserito l'indirizzo di spedizione
- Il carrello calcola il peso totale + dimensioni

**2. Il sistema prepara la richiesta per le tariffe**
- Recupera le credenziali dell'account del fornitore (decriptate)
- Calcola le dimensioni del pacco dagli elementi del carrello (usa i pacchi di spedizione se definiti)
- Prepara la richiesta API con origine, destinazione, pacchi

**3. API del fornitore chiamata**
- Richiesta inviata all'API del corriere con le credenziali di autenticazione
- Il corriere calcola la tariffa in base alla zona, al peso e alle dimensioni
- La risposta include le opzioni di servizio (Ground, Express, ecc.)

**4. Tariffe visualizzate**
- Il sistema analizza la risposta del corriere
- Normalizza al formato standard
- Applica un markup opzionale (se configurato)
- Tariffe mostrate al cliente al momento del checkout

**5. Cliente seleziona il servizio**
- Il cliente sceglie l'opzione preferita
- La tariffa selezionata viene salvata nell'ordine

**Esempio di flusso API**:
```
Richiesta all'API di FedEx:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // grammi
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

Risposta di FedEx:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Acquisto dell'etichetta (opzionale)

Se il fornitore supporta la generazione delle etichette:

**Flusso di lavoro**:
1. Il cliente completa l'ordine
2. Il commerciante crea la spedizione (Ordini > Dettagli ordine > Crea spedizione)
3. Seleziona l'account del fornitore + servizio
4. Il sistema chiama l'API delle etichette del fornitore
5. Genera il PDF dell'etichetta e lo allega alla spedizione
6. Il numero di tracciamento viene automaticamente compilato
7. L'etichetta è pronta per la stampa

**Vantaggi**:
- Nessun login manuale al sito del corriere
- Tracciamento automatico sincronizzato
- Documenti doganali automatici generati (internazionali)
- Generazione di etichette in batch possibile

---

## Markup delle tariffe

Aggiungi un markup del commerciante alle tariffe dei corrieri:

**Configurazione** (nella metodologia di spedizione, non nell'account del fornitore):
- **Tipo di markup**: Percentuale o Fissa
- **Importo markup**: es. 15% o $2,50

**Esempio**:
```
Tariffa del corriere: $12,50
Markup: 15%
Cliente paga: $14,38

O

Tariffa del corriere: $12,50
Markup: $2,50 (fissa)
Cliente paga: $15,00
```

**Casi d'uso**:
- Coprire costi di imballaggio/maneggio
- Aggiungere un margine di profitto alla spedizione
- Compensare le commissioni di carta di credito sulla spedizione

---

## Più account del fornitore

Puoi creare più account per lo stesso fornitore:

**Casi d'uso**:
1. **Test vs Produzione**
   - Account di test: Credenziali del sandbox del corriere
   - Account di produzione: Credenziali live

2. **Più magazzini**
   - Account del magazzino A: Origine = Los Angeles
   - Account del magazzino B: Origine = New York

3. **Diverse tariffe negoziate**
   - Account A: Tariffe standard
   - Account B: Tariffe scontate per volume

**Ogni account può collegarsi a diversi metodi di spedizione** per una configurazione flessibile.

---

## Consigli

- **Testa nel sandbox prima** - Utilizza le credenziali di test del corriere prima di andare in produzione
- **Monitora lo stato della connessione** - Controlla il dashboard per gli errori regolarmente
- **Definisci i pacchi di spedizione** - Le dimensioni accurate migliorano le quotazioni delle tariffe
- **Utilizza le tariffe negoziate** - Abilita se hai sconti per volume con il corriere
- **Imposta un'origine realistica** - Utilizza l'indirizzo effettivo di spedizione per le zone accurate
- **Mantieni le credenziali sicure** - Non condividere mai le chiavi API, ruotale periodicamente
- **Mantieni un metodo di backup** - Mantieni attivo un metodo a tariffa fissa se l'API del corriere fallisce
- **Monitora i limiti dell'API del corriere** - Alcuni corrieri limitano le chiamate API al giorno
- **Aggiorna le credenziali tempestivamente** - Quando il corriere ruota le chiavi, aggiornale immediatamente
- **Utilizza nomi descrittivi** - "FedEx LA Warehouse" è meglio di "FedEx 1"