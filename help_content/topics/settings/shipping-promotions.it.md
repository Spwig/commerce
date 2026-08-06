---
title: Promozioni di spedizione
---

Le regole di spedizione applicano aggiustamenti condizionali ai costi di spedizione in base al contenuto del carrello, agli attributi del cliente e alle aree di consegna - offri automaticamente la spedizione gratuita per ordini superiori a $50, aggiungi sovrapprezzi per aree remote o applica sconti sulla spedizione per clienti VIP. Le regole utilizzano un'esecuzione basata sulla priorità (priorità più alta prima) con flag opzionali per impedire un ulteriore elaborazione. Ogni regola valuta diverse condizioni (valore del carrello, peso, aree, prodotti, gruppi di clienti) ed esegue uno dei 6 tipi di aggiustamento quando tutte le condizioni corrispondono.

Utilizza le promozioni di spedizione quando hai bisogno di costi di spedizione dinamici che cambiano in base al contesto dell'ordine, non solo a tassi fissi definiti nei metodi di spedizione.

## Tipi di promozione di spedizione

Le regole di spedizione applicano 6 tipi di aggiustamenti ai costi:

### Sconto percentuale

**Cosa fa**: Riduce il costo di spedizione in percentuale (es. 25% di sconto).

**Formula**: `nuovo_costo = costo_base × (1 - percentuale/100)`

**Esempio**:
```
Costo base: $20
Sconto: 25%
Risultato: $15
```

**Casi d'uso**:
- Sconto per clienti VIP (20% di sconto su tutte le spedizioni)
- Promozioni stagionali (15% di sconto sulla spedizione a dicembre)
- Sconto per ordini di grandi quantità (10% di sconto sulla spedizione per 5+ articoli)

---

### Sconto fisso

**Cosa fa**: Sottrae un importo fisso dal costo di spedizione.

**Formula**: `nuovo_costo = costo_base - importo` (minimo $0)

**Esempio**:
```
Costo base: $15
Sconto: $5
Risultato: $10
```

**Casi d'uso**:
- Bonus per clienti nuovi ($5 di sconto sulla spedizione del primo ordine)
- Premio per l'iscrizione alla newsletter ($3 di sconto sulla spedizione)
- Beneficio del programma fedeltà ($10 di sconto sulla spedizione al mese)

---

### Sovrascrittura del costo

**Cosa fa**: Sovrascrive il costo di spedizione a un importo specifico.

**Formula**: `nuovo_costo = importo_fisso`

**Esempio**:
```
Costo base: $25
Impostare a: $9.99
Risultato: $9.99
```

**Casi d'uso**:
- Vendita lampo (spedizione a $5 per tutti gli ordini di oggi)
- Spedizione specifica per categoria (libri sempre a $3.99 di spedizione)
- Promozioni basate sul tempo (spedizione limitata a $9.99 questa settimana)

---

### Spedizione gratuita

**Cosa fa**: Imposta il costo di spedizione a $0.

**Formula**: `nuovo_costo = $0`

**Esempio**:
```
Costo base: $18
Regola applicata
Risultato: $0
```

**Casi d'uso**:
- Spedizione gratuita per ordini superiori a $50
- Spedizione gratuita per prodotti specifici (articoli promozionali)
- Spedizione gratuita per clienti VIP
- Spedizione gratuita per ordini con 3+ articoli

---

### Sovrapprezzo (fisso)

**Cosa fa**: Aggiunge un importo fisso al costo di spedizione.

**Formula**: `nuovo_costo = costo_base + importo`

**Esempio**:
```
Costo base: $12
Sovrapprezzo: $5
Risultato: $17
```

**Casi d'uso**:
- Tariffa di consegna per aree remote
- Gestione di articoli di grandi dimensioni
- Sovrapprezzo per consegna di sabato
- Tariffa per imballaggio di articoli fragili

---

### Sovrapprezzo (percentuale)

**Cosa fa**: Aumenta il costo di spedizione in percentuale.

**Formula**: `nuovo_costo = costo_base × (1 + percentuale/100)`

**Esempio**:
```
Costo base: $20
Sovrapprezzo: 15%
Risultato: $23
```

**Casi d'uso**:
- Sovrapprezzo per periodo di alta stagione (20% durante le festività)
- Premio per consegna espressa (sovrapprezzo del 50%)
- Sovrapprezzo per carburante (variabile in base ai tassi correnti)

---

## Condizioni della promozione

Le promozioni valutano **TUTTE le condizioni devono essere soddisfatte** per applicare la regola:

### Validità temporale

- **Data di inizio**: La regola è attiva solo dopo questa data
- **Data di fine**: La regola è attiva solo prima di questa data
- **Caso d'uso**: Promozioni stagionali, offerte a tempo limitato

**Esempio**: Spedizione gratuita solo nel weekend di Black Friday
```
Inizio: 2026-11-27 00:00
Fine: 2026-11-30 23:59
```

---

### Intervallo del valore del carrello

- **Valore minimo del carrello**: Il sottototale del carrello deve essere ≥ importo
- **Valore massimo del carrello**: Il sottototale del carrello deve essere ≤ importo
- **Caso d'uso**: Soglie per spedizione gratuita, sconti a livelli

**Esempio**: Spedizione gratuita per ordini da $50 a $200
```
Min: $50
Max: $200
```

---

### Intervallo del peso del carrello

- **Peso minimo**: Il peso totale del carrello deve essere ≥ importo
- **Peso massimo**: Il peso totale del carrello deve essere ≤ importo
- **Caso d'uso**: Sconti per spedizioni leggere, sovrapprezzi per articoli pesanti

**Esempio**: Sovrapprezzo di $5 per ordini superiori a 20kg
```
Peso minimo: 20kg
Peso massimo: null (illimitato)
```

---

### Intervallo del numero di articoli


- **Min Item Count**: Il carrello deve contenere ≥ quantità di articoli
- **Max Item Count**: Il carrello deve contenere ≤ quantità di articoli
- **Use Case**: Sconti per ordini di grandi quantità, spese per singolo articolo

**Esempio**: Spedizione gratuita per 5+ articoli
```
Min Items: 5
Max Items: null
```

---

### Shipping Zone

- **Zones**: La regola si applica solo se l'indirizzo del cliente corrisponde a almeno una zona selezionata
- **Empty selection**: La regola si applica a TUTTE le zone
- **Use Case**: Surchi o sconti specifici per zona

**Esempio**: Spedizione gratuita solo per la zona USA domestica
```
Zones: ["Domestic USA"]
```

---

### Shipping Method

- **Methods**: La regola si applica solo a metodi di spedizione specifici
- **Empty selection**: La regola si applica a TUTTI i metodi
- **Use Case**: Promozioni specifiche per metodo

**Esempio**: Sconto del 25% su Spedizione Express
```
Methods: ["Express Delivery"]
```

---

### Product Requirements

**Requires Products**: Il carrello deve contenere almeno uno di questi prodotti

**Requires Categories**: Il carrello deve contenere almeno un prodotto da queste categorie

**Use Case**: Spedizione gratuita specifica per prodotti, pacchetti promozionali

**Esempio**: Spedizione gratuita quando il carrello contiene "Promotion Item A"
```
Requires Products: [Product ID 123]
```

---

### Product Exclusions

**Excludes Products**: La regola non si applica se il carrello contiene uno di questi prodotti

**Excludes Categories**: La regola non si applica se il carrello contiene prodotti da queste categorie

**Use Case**: Escludere articoli pesanti/ingombrati dalla spedizione gratuita

**Esempio**: Spedizione gratuita tranne per la categoria arredamento
```
Excludes Categories: [Furniture]
```

---

### Customer Group

- **Customer Groups**: La regola si applica solo ai clienti nei gruppi selezionati (VIP, Wholesale, ecc.)
- **Empty selection**: La regola si applica a TUTTI i gruppi di clienti
- **Use Case**: Benefici VIP, sconti per clienti wholesale

**Esempio**: Sconto del 15% sulla spedizione per membri VIP
```
Customer Groups: ["VIP"]
```

---

### First-Time Customer

- **First Time Customer**: Toggle per limitare la regola ai clienti senza ordini precedenti
- **Use Case**: Offerte di benvenuto per nuovi clienti

**Esempio**: $5 di sconto sulla spedizione per il primo ordine
```
First Time Customer: Yes
```

---

## Promotion Priority & Execution

Le promozioni vengono eseguite nell'**ordine di priorità** (numero più alto = esecuzione più precoce):

### Priority Mechanics

**Esempio di esecuzione**:
```
Promotion A (Priority 100): Spedizione gratuita se il carrello > $50
Promotion B (Priority 50): Sconto del 10% su tutta la spedizione
Promotion C (Priority 1): Surchi di $2 per zone remote

Carrello: $60, zona remota
Costo di spedizione base: $15

Step 1: Promotion A valuta (Priority 100)
  Carrello > $50? SÌ
  Applica: Imposta costo a $0
  Costo ora: $0

Step 2: Promotion B valuta (Priority 50)
  Applica uno sconto del 10% a $0
  Costo ora: $0 (ancora gratuito)

Step 3: Promotion C valuta (Priority 1)
  Aggiungi un surcharge di $2 a $0
  Costo ora: $2

Costo finale: $2
```

**Stop Further Promotions Flag**:

Se Promotion A ha `stop_further_promotions = True`:
```
Promotion A (Priority 100, stop_further_promotions=True): Spedizione gratuita se il carrello > $50
Promotion B (Priority 50): Sconto del 10%
Promotion C (Priority 1): Surchi di $2 per zone remote

Carrello: $60
Base: $15

Step 1: Promotion A applica, imposta costo a $0
        stop_further_promotions = True → STOP

Costo finale: $0 (Le regole B e C mai eseguite)
```

---

## Creating Shipping Promotions

**Step-by-Step Workflow**:

1. **Navigate to Rules**
   - Settings > Shipping > Shipping Promotions
   - Click "Add Shipping Promotion"

2. **Basic Configuration**
   - **Name**: Identificatore interno (es. "Spedizione gratuita per ordini superiori a $50")
   - **Description**: Note opzionali (non mostrate ai clienti)
   - **Active**: Toggle per abilitare/disabilitare
   - **Priority**: Imposta l'ordine di esecuzione (100 per alta priorità, 1 per bassa)

3. **Choose Promotion Type**
   - Seleziona il tipo di regolazione (sconto %, sconto fisso, imposta costo, gratuito, surcharge %, surcharge fisso)
   - Inserisci l'importo o la percentuale


4. **Imposta Flag di Arresto** (Opzionale)
   - Seleziona "Arresta ulteriori promozioni" se questa regola deve impedire l'esecuzione di promozioni a priorità inferiore
   - Utilizzare per regole finali/assolute (es. la spedizione gratuita non dovrebbe avere sovrapprezzi aggiunti dopo)

5. **Definisci Condizioni** (Opzionale - lasciare vuoto per "applica sempre")
   - Validità temporale: date di inizio/fine
   - Valore del carrello: min/max
   - Peso del carrello: min/max
   - Numero di articoli: min/max
   - Zone: seleziona le zone applicabili
   - Metodi: seleziona i metodi applicabili
   - Prodotti: richiesti o esclusi
   - Cliente: gruppi o solo primi tempi

6. **Salva Regola**
   - Clicca su Salva
   - La regola diventa attiva immediatamente (se l'interruttore Attivo è su Sì)

---

## Scenario Comuni di Promozione di Spedizione

### Scenario 1: Spedizione Gratuita per Ordini di $50 o Più

**Obiettivo**: Offrire una spedizione gratuita quando il sottototale del carrello è ≥ $50.

**Configurazione**:
```
Nome: Spedizione Gratuita per $50
Tipo: Spedizione Gratuita
Priorità: 100
Condizioni:
  Valore Minimo del Carrello: $50
Arresta Ulteriori Promozioni: Sì
```

---

### Scenario 2: Soprapprezzo per Zone Remote

**Obiettivo**: Aggiungi un soprapprezzo di $10 per consegne in zone remote.

**Configurazione**:
```
Nome: Soprapprezzo per Zone Remote
Tipo: Soprapprezzo (Fisso)
Importo: $10
Priorità: 50
Condizioni:
  Zone: ["Zone Remote"]
Arresta Ulteriori Promozioni: No
```

---

### Scenario 3: Sconto del 20% per Clienti VIP

**Obiettivo**: I clienti VIP ottengono uno sconto del 20% su tutta la spedizione.

**Configurazione**:
```
Nome: Sconto di Spedizione VIP
Tipo: Sconto (Percentuale)
Percentuale: 20
Priorità: 75
Condizioni:
  Gruppi di Clienti: ["VIP"]
Arresta Ulteriori Promozioni: No
```

---

### Scenario 4: Tariffa Fissa per le Feste

**Obiettivo**: Limitare la spedizione a $9.99 durante il mese di dicembre.

**Configurazione**:
```
Nome: Promozione Tariffa Fissa di Dicembre
Tipo: Sovrascrivi Costo
Importo: $9.99
Priorità: 100
Condizioni:
  Data di Inizio: 2026-12-01
  Data di Fine: 2026-12-31
Arresta Ulteriori Promozioni: Sì
```

---

### Scenario 5: Soprapprezzo per Ordini Pesanti

**Obiettivo**: Aggiungi un costo di $15 per ordini superiori a 25kg.

**Configurazione**:
```
Nome: Soprapprezzo per Ordini Pesanti
Tipo: Soprapprezzo (Fisso)
Importo: $15
Priorità: 50
Condizioni:
  Peso Minimo: 25kg
Arresta Ulteriori Promozioni: No
```

---

### Scenario 6: Spedizione Gratuita per Primo Ordine

**Obiettivo**: I nuovi clienti ottengono una spedizione gratuita per il primo ordine.

**Configurazione**:
```
Nome: Spedizione Gratuita per Primo Ordine
Tipo: Spedizione Gratuita
Priorità: 100
Condizioni:
  Cliente Prima Volta: Sì
Arresta Ulteriori Promozioni: Sì
```

---

### Scenario 7: Spedizione Gratuita per Categorie Specifiche

**Obiettivo**: Spedizione gratuita per ordini che contengono articoli di categorie promozionali.

**Configurazione**:
```
Nome: Spedizione Gratuita per Categorie Promozionali
Tipo: Spedizione Gratuita
Priorità: 90
Condizioni:
  Richiede Categorie: ["Promozioni"]
Arresta Ulteriori Promozioni: Sì
```

---

### Scenario 8: Escludi Mobili dalla Spedizione Gratuita

**Obiettivo**: Spedizione gratuita per ordini di $50 o più, tranne se il carrello contiene mobili.

**Soluzione**: Due regole

**Promozione 1**:
```
Nome: Spedizione Gratuita Generale
Tipo: Spedizione Gratuita
Priorità: 50
Condizioni:
  Valore Minimo del Carrello: $50
  Esclude Categorie: ["Mobili"]
Arresta Ulteriori Promozioni: No
```

**Promozione 2**:
```
Nome: Sconto di $5 per Ordini di Mobili
Tipo: Sconto (Fisso)
Importo: $5
Priorità: 40
Condizioni:
  Richiede Categorie: ["Mobili"]
  Valore Minimo del Carrello: $50
Arresta Ulteriori Promozioni: No
```

---

## Strategie di Combinazione delle Promozioni

### Strategia 1: Sovrapposizione di Sconti

**Consenti a più sconti di sovrapporsi**:
```
Promozione A (Priorità 100): 10% di sconto per VIP → stop_further_promotions=No
Promozione B (Priorità 50): 15% di sconto per ordini >$100 → stop_further_promotions=No

Cliente VIP con un ordine di $120:
Base: $15
Dopo Promozione A: $13.50 (10% di sconto)
Dopo Promozione B: $11.48 (15% di sconto su $13.50)
```

### Strategia 2: Regole Esclusive

**Solo una regola si applica** (priorità più alta):
```
Promozione A (Priorità 100): Spedizione gratuita >$50 → stop_further_promotions=Yes
Promozione B (Priorità 50): 20% di sconto su tutta la spedizione → stop_further_promotions=Yes

Carrello > $50:
Promozione A si applica → Spedizione gratuita → STOP
Promozione B non viene mai eseguita
```

### Strategia 3: Soprapprezzi Condizionali


**Sconti prima, sovrapprezzi dopo**:
```
Promotion A (Priority 100): Free shipping >$75
Promotion B (Priority 75): 15% VIP discount
Promotion C (Priority 50): 10% general discount
Promotion D (Priority 25): $5 remote area surcharge
Promotion E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (not free due to surcharges)
```

**Per prevenire questo, usa stop_further_promotions=Yes**:
```
Promotion A (Priority 100, stop=Yes): Free shipping >$75

Same order:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (truly free)
```

---

## Testing Shipping Promotions

**Before going live**:

1. **Create Test Carts**
   - Cart A: $25 (below threshold)
   - Cart B: $55 (above threshold)
   - Cart C: $200 + Remote zone
   - Cart D: VIP customer

2. **Test Each Rule**
   - Proceed to checkout
   - Verify correct shipping cost displayed
   - Check rule execution order

3. **Test Priority Resolution**
   - Multiple matching rules
   - Verify highest priority executes first
   - Check stop_further_promotions behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Promotion not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_promotions=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple promotions stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_promotions flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping promotion
- Cart doesn't meet min value threshold
- Excluded products in cart

**Solution**: Use stop_further_promotions=Yes on free shipping promotion, verify conditions, check exclusions.

---

## Tips

- **Use high priority for free shipping** - Priority 100 ensures it executes before other adjustments
- **Set stop_further_promotions for absolute rules** - Free shipping should stop further processing
- **Test rule combinations** - Multiple promotions can interact unexpectedly
- **Use descriptive names** - "VIP 20% Discount (Priority 75)" better than "Promotion 3"
- **Document complex logic** - Add notes in description field
- **Start with simple promotions** - Add complexity gradually
- **Monitor rule performance** - Check if rules are being used or causing confusion
- **Avoid excessive promotions** - Too many promotions slow checkout, use 5-10 max
- **Use zones for geography** - Better than multiple similar rules per country
- **Combine with methods** - Rules + Methods work together for sophisticated pricing
- **Set clear time windows** - Always include end dates for promotions
- **Test edge cases** - Exactly $50, exactly 5 items, etc.