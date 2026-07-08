---
title: Regole di spedizione
---

Le regole di spedizione applicano aggiustamenti condizionali ai costi di spedizione in base al contenuto del carrello, agli attributi del cliente e alle aree di consegna - offri automaticamente la spedizione gratuita per ordini superiori a $50, aggiungi sovrapprezzi per aree remote o applica sconti per clienti VIP. Le regole utilizzano un'esecuzione basata sulla priorità (priorità più alta prima) con flag opzionali per fermare ulteriori elaborazioni. Ogni regola valuta diverse condizioni (valore del carrello, peso, aree, prodotti, gruppi di clienti) ed esegue uno dei 6 tipi di aggiustamento quando tutte le condizioni corrispondono.

Utilizza le regole di spedizione quando hai bisogno di costi di spedizione dinamici che cambiano in base al contesto dell'ordine, non solo a tassi fissi definiti nei metodi di spedizione.

## Tipi di regole di spedizione

Le regole di spedizione applicano 6 tipi di aggiustamenti ai costi:

### Sconto percentuale

**Cosa fa**: Riduce il costo di spedizione in percentuale (es. 25% di sconto).

**Formula**: `new_cost = base_cost × (1 - percent/100)`

**Esempio**:
```
Costo base: $20
Sconto: 25%
Risultato: $15
```

**Utilizzo**:
- Sconto per clienti VIP (20% di sconto su tutti i costi di spedizione)
- Promozioni stagionali (15% di sconto su spedizioni in dicembre)
- Sconto per ordini di grandi quantità (10% di sconto su spedizioni per 5+ articoli)

---

### Sconto fisso

**Cosa fa**: Sottrae un importo fisso dal costo di spedizione.

**Formula**: `new_cost = base_cost - amount` (minimo $0)

**Esempio**:
```
Costo base: $15
Sconto: $5
Risultato: $10
```

**Utilizzo**:
- Bonus per clienti nuovi ($5 di sconto sulla spedizione del primo ordine)
- Premio per l'iscrizione alla newsletter ($3 di sconto sulla spedizione)
- Beneficio del programma fedeltà ($10 di sconto sulla spedizione al mese)

---

### Costo fisso

**Cosa fa**: Sovrascrive il costo di spedizione a un importo specifico.

**Formula**: `new_cost = fixed_amount`

**Esempio**:
```
Costo base: $25
Impostare a: $9.99
Risultato: $9.99
```

**Utilizzo**:
- Vendita lampo (spedizione a $5 per tutti gli ordini di oggi)
- Spedizione specifica per categoria (libri sempre a $3.99 di spedizione)
- Promozioni basate sul tempo (spedizione limitata a $9.99 questa settimana)

---

### Spedizione gratuita

**Cosa fa**: Imposta il costo di spedizione a $0.

**Formula**: `new_cost = $0`

**Esempio**:
```
Costo base: $18
Applicazione della regola
Risultato: $0
```

**Utilizzo**:
- Spedizione gratuita per ordini superiori a $50
- Spedizione gratuita per prodotti specifici (articoli promozionali)
- Spedizione gratuita per clienti VIP
- Spedizione gratuita per ordini con 3+ articoli

---

### Sovrapprezzo (fisso)

**Cosa fa**: Aggiunge un importo fisso al costo di spedizione.

**Formula**: `new_cost = base_cost + amount`

**Esempio**:
```
Costo base: $12
Sovrapprezzo: $5
Risultato: $17
```

**Utilizzo**:
- Tariffa di consegna per aree remote
- Gestione di articoli di grandi dimensioni
- Sovrapprezzo per consegna di sabato
- Tariffa per imballaggio di articoli fragili

---

### Sovrapprezzo (percentuale)

**Cosa fa**: Aumenta il costo di spedizione in percentuale.

**Formula**: `new_cost = base_cost × (1 + percent/100)`

**Esempio**:
```
Costo base: $20
Sovrapprezzo: 15%
Risultato: $23
```

**Utilizzo**:
- Sovrapprezzo per periodo di alta stagione (20% durante le festività)
- Premio per consegna espressa (sovrapprezzo del 50%)
- Sovrapprezzo per carburante (variabile in base ai tassi correnti)

---

## Condizioni delle regole

Le regole valutano **TUTTE le condizioni devono passare** per applicare la regola:

### Validità temporale

- **Data di inizio**: La regola è attiva solo dopo questa data
- **Data di fine**: La regola è attiva solo prima di questa data
- **Utilizzo**: Promozioni stagionali, offerte a tempo limitato

**Esempio**: Spedizione gratuita solo nel weekend di Black Friday
```
Inizio: 2026-11-27 00:00
Fine: 2026-11-30 23:59
```

---

### Intervallo del valore del carrello

- **Valore minimo del carrello**: Il sottototale del carrello deve essere ≥ importo
- **Valore massimo del carrello**: Il sottototale del carrello deve essere ≤ importo
- **Utilizzo**: Soglie per spedizione gratuita, sconti a scaglioni

**Esempio**: Spedizione gratuita per ordini da $50 a $200
```
Min: $50
Max: $200
```

---

### Intervallo del peso del carrello

- **Peso minimo**: Il peso totale del carrello deve essere ≥ importo
- **Peso massimo**: Il peso totale del carrello deve essere ≤ importo
- **Utilizzo**: Sconti per spedizioni leggere, sovrapprezzi per articoli pesanti

**Esempio**: Sovrapprezzo di $5 per ordini superiori a 20kg
```
Peso minimo: 20kg
Peso massimo: null (illimitato)
```

---

### Intervallo del numero di articoli

- **Minimo numero di articoli**: Il carrello deve contenere ≥ quantità di articoli
- **Massimo numero di articoli**: Il carrello deve contenere ≤ quantità di articoli
- **Utilizzo**: Sconti per ordini di grandi quantità, tariffe per singoli articoli

**Esempio**: Spedizione gratuita per 5+ articoli
```
Minimo articoli: 5
Massimo articoli: null
```

---

### Zona di spedizione

- **Zona**: La regola si applica solo se l'indirizzo del cliente corrisponde a almeno una zona selezionata
- **Selezione vuota**: La regola si applica a TUTTE le zone
- **Utilizzo**: Sconti o sovrapprezzi specifici per zona

**Esempio**: Spedizione gratuita solo per la zona domestica
```
Zona: ["Domestic USA"]
```

---

### Metodo di spedizione

- **Metodi**: La regola si applica solo a metodi di spedizione specifici
- **Selezione vuota**: La regola si applica a TUTTI i metodi
- **Utilizzo**: Promozioni specifiche per metodo

**Esempio**: 25% di sconto su Spedizione Espressa
```
Metodi: ["Express Delivery"]
```

---

### Requisiti del prodotto

**Prodotti richiesti**: Il carrello deve contenere almeno uno di questi prodotti

**Categorie richieste**: Il carrello deve contenere almeno un prodotto da queste categorie

**Utilizzo**: Spedizione gratuita specifica per prodotto, pacchetti promozionali

**Esempio**: Spedizione gratuita quando il carrello contiene "Promotion Item A"
```
Prodotti richiesti: [ID prodotto 123]
```

---

### Esclusioni del prodotto

**Prodotti esclusi**: La regola non si applica se il carrello contiene uno di questi prodotti

**Categorie escluse**: La regola non si applica se il carrello contiene prodotti da queste categorie

**Utilizzo**: Escludere articoli pesanti o di grandi dimensioni dalla spedizione gratuita

**Esempio**: Spedizione gratuita tranne per la categoria arredamento
```
Categorie escluse: [Arredamento]
```

---

### Gruppo di clienti

- **Gruppi di clienti**: La regola si applica solo ai clienti nei gruppi selezionati (VIP, Grossista, ecc.)
- **Selezione vuota**: La regola si applica a TUTTI i gruppi di clienti
- **Utilizzo**: Benefici VIP, sconti per grossisti

**Esempio**: Sconto del 15% sulla spedizione per membri VIP
```
Gruppi di clienti: ["VIP"]
```

---

### Cliente primo ordine

- **Cliente primo ordine**: Toggle per limitare la regola ai clienti senza ordini precedenti
- **Utilizzo**: Offerte di benvenuto per nuovi clienti

**Esempio**: $5 di sconto sulla spedizione per primo ordine
```
Cliente primo ordine: Sì
```

---

## Priorità e esecuzione delle regole

Le regole vengono eseguite in **ordine di priorità** (numero più alto = esecuzione più precoce):

### Meccanica delle priorità

**Esempio di esecuzione**:
```
Regola A (Priorità 100): Spedizione gratuita se carrello > $50
Regola B (Priorità 50): Sconto del 10% su tutti i costi di spedizione
Regola C (Priorità 1): Sovrapprezzo di $2 per aree remote

Carrello: $60, zona remota
Costo base di spedizione: $15

Passo 1: Valutazione della Regola A (Priorità 100)
  Carrello > $50? SÌ
  Applicare: Impostare costo a $0
  Costo ora: $0

Passo 2: Valutazione della Regola B (Priorità 50)
  Applicare sconto del 10% a $0
  Costo ora: $0 (ancora gratuito)

Passo 3: Valutazione della Regola C (Priorità 1)
  Aggiungere $2 di sovrapprezzo a $0
  Costo ora: $2

Costo finale: $2
```

**Flag per fermare ulteriori regole**:

Se la Regola A ha `stop_further_rules = True`:
```
Regola A (Priorità 100, stop_further_rules=True): Spedizione gratuita se carrello > $50
Regola B (Priorità 50): Sconto del 10%
Regola C (Priorità 1): Sovrapprezzo di $2 per aree remote

Carrello: $60
Costo base: $15

Passo 1: Applicazione della Regola A, imposta costo a $0
        stop_further_rules = True → FERMA

Costo finale: $0 (Le regole B e C non vengono mai eseguite)
```

---

## Creazione di regole di spedizione

**Flusso di lavoro passo-passo**:

1. **Navigare alle regole**
   - Impostazioni > Spedizione > Regole di spedizione
   - Fare clic su "Aggiungi regola di spedizione"

2. **Configurazione di base**
   - **Nome**: Identificatore interno (es. "Spedizione gratuita per ordini superiori a $50")
   - **Descrizione**: Note opzionali (non mostrate ai clienti)
   - **Attiva**: Toggle per abilitare/disabilitare
   - **Priorità**: Impostare l'ordine di esecuzione (100 per alta priorità, 1 per bassa)

3. **Scegliere il tipo di regola**
   - Selezionare il tipo di aggiustamento (sconto %, sconto fisso, costo fisso, gratuito, sovrapprezzo %, sovrapprezzo fisso)
   - Inserire l'importo o la percentuale

4. **Impostare il flag di arresto** (Opzionale)
   - Selezionare "Ferma ulteriori regole" se questa regola deve impedire l'esecuzione di regole a priorità inferiore
   - Utilizzare per regole finali/assolute (es. la spedizione gratuita non dovrebbe avere sovrapprezzi aggiunti dopo)

5. **Definire le condizioni** (Opzionale - lasciare vuoto per "applica sempre")
   - Validità temporale: date di inizio/fine
   - Valore del carrello: min/max
   - Peso del carrello: min/max
   - Numero di articoli: min/max
   - Zone: selezionare le zone applicabili
   - Metodi: selezionare i metodi applicabili
   - Prodotti: richiesti o esclusi
   - Cliente: gruppi o solo primo ordine

6. **Salvare la regola**
   - Fare clic su Salva
   - La regola diventa attiva immediatamente (se l'opzione attiva è Yes)

---

## Scenario comuni per regole di spedizione

### Scenario 1: Spedizione gratuita per ordini superiori a $50

**Obiettivo**: Offrire spedizione gratuita quando il sottototale del carrello ≥ $50.

**Configurazione**:
```
Nome: Spedizione gratuita per ordini superiori a $50
Tipo: Spedizione gratuita
Priorità: 100
Condizioni:
  Valore minimo del carrello: $50
Ferma ulteriori regole: Sì
```

---

### Scenario 2: Sovrapprezzo per aree remote

**Obiettivo**: Aggiungere un sovrapprezzo di $10 per consegne in aree remote.

**Configurazione**:
```
Nome: Sovrapprezzo per aree remote
Tipo: Sovrapprezzo (fisso)
Importo: $10
Priorità: 50
Condizioni:
  Zone: ["Aree remote"]
Ferma ulteriori regole: No
```

---

### Scenario 3: Sconto del 20% per clienti VIP

**Obiettivo**: I clienti VIP ottengono il 20% di sconto su tutti i costi di spedizione.

**Configurazione**:
```
Nome: Sconto sulla spedizione per clienti VIP
Tipo: Sconto (percentuale)
Percentuale: 20
Priorità: 75
Condizioni:
  Gruppi di clienti: ["VIP"]
Ferma ulteriori regole: No
```

---

### Scenario 4: Tariffa fissa per dicembre

**Obiettivo**: Limitare tutti i costi di spedizione a $9.99 durante il mese di dicembre.

**Configurazione**:
```
Nome: Promozione tariffa fissa per dicembre
Tipo: Costo fisso
Importo: $9.99
Priorità: 100
Condizioni:
  Data di inizio: 2026-12-01
  Data di fine: 2026-12-31
Ferma ulteriori regole: Sì
```

---

### Scenario 5: Sovrapprezzo per articoli pesanti

**Obiettivo**: Aggiungere una tariffa di $15 per ordini superiori a 25kg.

**Configurazione**:
```
Nome: Sovrapprezzo per ordini pesanti
Tipo: Sovrapprezzo (fisso)
Importo: $15
Priorità: 50
Condizioni:
  Peso minimo: 25kg
Ferma ulteriori regole: No
```

---

### Scenario 6: Spedizione gratuita per primo ordine

**Obiettivo**: I nuovi clienti ottengono spedizione gratuita per il primo ordine.

**Configurazione**:
```
Nome: Spedizione gratuita per primo ordine
Tipo: Spedizione gratuita
Priorità: 100
Condizioni:
  Cliente primo ordine: Sì
Ferma ulteriori regole: Sì
```

---

### Scenario 7: Spedizione gratuita per categoria promozionale

**Obiettivo**: Spedizione gratuita per ordini che contengono articoli della categoria promozionale.

**Configurazione**:
```
Nome: Spedizione gratuita per categoria promozionale
Tipo: Spedizione gratuita
Priorità: 90
Condizioni:
  Categorie richieste: ["Promozioni"]
Ferma ulteriori regole: Sì
```

---

### Scenario 8: Escludere l'arredamento dalla spedizione gratuita

**Obiettivo**: Spedizione gratuita per ordini superiori a $50, tranne se il carrello contiene arredamento.

**Soluzione**: Due regole

**Regola 1**:
```
Nome: Spedizione gratuita generale
Tipo: Spedizione gratuita
Priorità: 50
Condizioni:
  Valore minimo del carrello: $50
  Categorie escluse: ["Arredamento"]
Ferma ulteriori regole: No
```

**Regola 2**:
```
Nome: Sconto di $5 per ordini di arredamento
Tipo: Sconto (fisso)
Importo: $5
Priorità: 40
Condizioni:
  Categorie richieste: ["Arredamento"]
  Valore minimo del carrello: $50
Ferma ulteriori regole: No
```

---

## Strategie per la combinazione delle regole

### Strategia 1: Sovrapposizione degli sconti

**Permettere a più sconti di sovrapporsi**:
```
Regola A (Priorità 100): 10% di sconto per VIP → stop_further_rules=No
Regola B (Priorità 50): 15% di sconto per ordini >$100 → stop_further_rules=No

Cliente VIP con ordine di $120:
Costo base: $15
Dopo la Regola A: $13.50 (10% di sconto)
Dopo la Regola B: $11.48 (15% di sconto su $13.50)
```

### Strategia 2: Regole esclusive

**Solo una regola si applica** (priorità più alta):
```
Regola A (Priorità 100): Spedizione gratuita >$50 → stop_further_rules=Yes
Regola B (Priorità 50): 20% di sconto su tutti i costi di spedizione → stop_further_rules=Yes

Carrello > $50:
Regola A si applica → Spedizione gratuita → FERMA
Regola B mai eseguita
```

### Strategia 3: Sovrapprezzi condizionali

**Sconti prima, sovrapprezzi dopo**:
```
Regola A (Priorità 100): Spedizione gratuita >$75
Regola B (Priorità 75): Sconto del 15% per clienti VIP
Regola C (Priorità 50): Sconto del 10% generale
Regola D (Priorità 25): Sovrapprezzo di $5 per aree remote
Regola E (Priorità 1): Sovrapprezzo del 10% per carburante

Ordine: $80, zona remota, cliente VIP
Costo base: $20
A: $80 > $75 → Spedizione gratuita ($0)
B: VIP → 15% di sconto su $0 = $0
C: 10% di sconto su $0 = $0
D: Zona remota +$5 = $5
E: Carburante +10% di $5 = $5.50

Risultato finale: $5.50 (non gratuito a causa dei sovrapprezzi)
```

**Per prevenire questo, utilizzare stop_further_rules=Yes**:
```
Regola A (Priorità 100, stop=Yes): Spedizione gratuita >$75

Stesso ordine:
A: $80 > $75 → Spedizione gratuita ($0) → FERMA
Risultato finale: $0 (veramente gratuito)
```

---

## Test delle regole di spedizione

**Prima di andare online**:

1. **Creare carrelli di test**
   - Carrello A: $25 (sotto soglia)
   - Carrello B: $55 (sopra soglia)
   - Carrello C: $200 + zona remota
   - Carrello D: cliente VIP

2. **Testare ogni regola**
   - Procedere al checkout
   - Verificare che venga visualizzato il costo di spedizione corretto
   - Controllare l'ordine di esecuzione delle regole

3. **Testare la risoluzione delle priorità**
   - Più regole che corrispondono
   - Verificare che venga eseguita prima la priorità più alta
   - Controllare il comportamento di stop_further_rules

4. **Testare i casi limite**
   - Valore del carrello esattamente alla soglia
   - Più condizioni che corrispondono
   - Regole conflittuali

---

## Risoluzione dei problemi

**Problema 1: Regola non applicabile**

**Causa**:
- La regola non è attiva
- Una o più condizioni non sono soddisfatte
- Una regola a priorità più alta ha impostato stop_further_rules=Yes
- Validità temporale fuori dalla data corrente

**Soluzione**: Rivedere tutte le condizioni, controllare la priorità, verificare lo stato attivo.

---

**Problema 2: Importo di sconto inaspettato**

**Causa**:
- Più regole che si sovrappongono
- Percentuale applicata a un costo già scontato
- Priorità della regola errata

**Soluzione**: Controllare l'ordine di priorità, rivedere i flag stop_further_rules, tracciare manualmente l'esecuzione.

---

**Problema 3: Spedizione gratuita non funzionante**

**Causa**:
- Una regola a priorità inferiore aggiunge un costo dopo la regola di spedizione gratuita
- Il carrello non soddisfa il valore minimo della soglia
- Prodotti esclusi nel carrello

**Soluzione**: Utilizzare stop_further_rules=Yes sulla regola di spedizione gratuita, verificare le condizioni, controllare le esclusioni.

---

## Consigli

- **Utilizzare una priorità alta per la spedizione gratuita** - Priorità 100 assicura che venga eseguita prima di altri aggiustamenti
- **Impostare stop_further_rules per le regole assolute** - La spedizione gratuita dovrebbe fermare ulteriori elaborazioni
- **Testare le combinazioni di regole** - Più regole possono interagire in modo inaspettato
- **Utilizzare nomi descrittivi** - "Sconto del 20% per VIP (Priorità 75)" è meglio di "Regola 3"
- **Documentare la logica complessa** - Aggiungere note nel campo descrizione
- **Iniziare con regole semplici** - Aggiungere complessità gradualmente
- **Monitorare le prestazioni delle regole** - Controllare se le regole vengono utilizzate o causano confusione
- **Evitare troppe regole** - Troppa regole rallentano il checkout, utilizzare un massimo di 5-10
- **Utilizzare le zone per la geografia** - Meglio di molte regole simili per paese
- **Combinare con i metodi** - Le regole + metodi funzionano insieme per prezzi sofisticati
- **Impostare finestre temporali chiare** - Includere sempre la data di fine per le promozioni
- **Testare i casi limite** - Esattamente $50, esattamente 5 articoli, ecc.

Ricorda: Preservare tutto il formattazione markdown, percorsi delle immagini, blocchi di codice e termini tecnici esattamente come mostrato nelle regole di conservazione.