---
title: Regole di spedizione
---

Le regole di spedizione applicano modifiche ai costi di consegna in base al contenuto del carrello, alle caratteristiche del cliente e alle aree di consegna: offri automaticamente la spedizione gratuita sopra i $50, aggiungi sovrapprezzi per aree remote o sconti per i clienti VIP. Le regole utilizzano l'esecuzione basata sulla priorità (priorità maggiore per prima) con flag opzionali per evitare ulteriori elaborazioni. Ogni regola valuta più condizioni (valore del carrello, peso, zone, prodotti, gruppi clienti) ed esegue uno dei 6 tipi di modifica quando tutte le condizioni sono soddisfatte.

Utilizza le regole di spedizione quando hai bisogno di costi di spedizione dinamici che cambiano in base al contesto dell'ordine, non solo tassi fissi dai metodi di spedizione.

## Tipi di regole di spedizione

Le regole di spedizione applicano 6 tipi di modifiche al costo:

### Sconto percentuale

**Cosa fa**: Riduce il costo di spedizione in percentuale (es. 25% di sconto).

**Formula**: `nuovo_costo = costo_base × (1 - percento/100)`

**Esempio**:
```
Costo base: $20
Sconto: 25%
Risultato: $15
```

**Casi d'uso**:
- Sconto per clienti VIP (20% di sconto su tutta la spedizione)
- Promozioni stagionali (15% di sconto sulla spedizione in dicembre)
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
- Bonus per primo ordine ($5 di sconto sulla spedizione per il primo ordine)
- Ricompensa per la registrazione alla newsletter ($3 di sconto sulla spedizione)
- Beneficio del programma fedeltà ($10 di sconto sulla spedizione al mese)

---

### Costo fisso

**Cosa fa**: Sostituisce il costo di spedizione con un importo specifico.

**Formula**: `nuovo_costo = importo_fisso`

**Esempio**:
```
Costo base: $25
Impostare su: $9.99
Risultato: $9.99
```

**Casi d'uso**:
- Vendita a prezzo fisso (spedizione fissa a $5 per tutti gli ordini di oggi)
- Spedizione specifica per categoria (la spedizione per i libri è sempre $3.99)
- Promozioni basate sul tempo (spedizione massima a $9.99 questa settimana)

---

### Spedizione gratuita

**Cosa fa**: Imposta il costo di spedizione a $0.

**Formula**: `nuovo_costo = $0`

**Esempio**:
```
Costo base: $18
La regola si applica
Risultato: $0
```

**Casi d'uso**:
- Spedizione gratuita sopra i $50
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
- Tariffa per consegna in aree remote
- Gestione di articoli di grandi dimensioni
- Sovrapprezzo per consegna di sabato
- Tariffa imballaggio per articoli fragili

---

### Sovrapprezzo (percentuale)

**Cosa fa**: Aumenta il costo di spedizione in percentuale.

**Formula**: `nuovo_costo = costo_base × (1 + percento/100)`

**Esempio**:
```
Costo base: $20
Sovrapprezzo: 15%
Risultato: $23
```

**Casi d'uso**:
- Sovrapprezzo stagionale (20% durante le vacanze)
- Premio per consegna espressa (50% di sovrapprezzo)
- Tariffa carburante (variabile in base ai tassi correnti)

---

## Condizioni della regola

Le regole valutano **tutte le condizioni devono essere soddisfatte** per applicare la regola:

### Validità temporale

- **Data iniziale**: La regola è attiva solo dopo questa data
- **Data finale**: La regola è attiva solo prima di questa data
- **Caso d'uso**: Promozioni stagionali, offerte a tempo

**Esempio**: Spedizione gratuita nel fine settimana del Black Friday solo
```
Inizio: 2026-11-27 00:00
Fine: 2026-11-30 23:59
```

---

### Intervallo valore carrello

- **Valore minimo carrello**: Il totale del carrello deve essere ≥ importo
- **Valore massimo carrello**: Il totale del carrello deve essere ≤ importo
- **Caso d'uso**: Soglie di spedizione gratuita, sconti a scaglie

**Esempio**: Spedizione gratuita per ordini tra $50 e $200
```
Min: $50
Max: $200
```

---

### Intervallo peso carrello

- **Peso minimo**: Il peso totale del carrello deve essere ≥ importo
- **Peso massimo**: Il peso totale del carrello deve essere ≤ importo
- **Caso d'uso**: Sconti per spedizioni leggere, sovrapprezzi per articoli pesanti

**Esempio**: Sovrapprezzo di $5 per ordini superiori a 20kg
```
Peso minimo: 20kg
Peso massimo: null (illimitato)
```

---

### Intervallo numero articoli


- **Min Item Count**: Il carrello deve contenere ≥ quantità di articoli
- **Max Item Count**: Il carrello deve contenere ≤ quantità di articoli
- **Use Case**: Sconti per ordini multipli, tariffe per singolo articolo

**Esempio**: Spedizione gratuita per 5+ articoli
```
Min Items: 5
Max Items: null
```


### Zona di Spedizione

- **Zone**: La regola si applica solo se l'indirizzo del cliente corrisponde a almeno una zona selezionata
- **Selezione vuota**: La regola si applica a TUTTE le zone
- **Use Case**: Ritenute o sconti specifici per zona

**Esempio**: Spedizione gratuita solo per la zona Interna
```
Zone: ["Interni USA"]
```


### Metodo di Spedizione

- **Metodi**: La regola si applica solo a metodi specifici di spedizione
- **Selezione vuota**: La regola si applica a TUTTI i metodi
- **Use Case**: Promozioni specifiche per metodo

**Esempio**: Sconto del 25% per la spedizione espressa
```
Metodi: ["Consegna Espressa"]
```


### Requisiti dei Prodotti

**Richiede Prodotti**: Il carrello deve contenere almeno uno di questi prodotti

**Richiede Categorie**: Il carrello deve contenere almeno un prodotto da queste categorie

**Use Case**: Spedizione gratuita specifica per prodotto, pacchetti promozionali

**Esempio**: Spedizione gratuita quando il carrello include "Prodotto Promozionale A"
```
Richiede Prodotti: [ID Prodotto 123]
```


### Esclusioni dei Prodotti

**Esclude Prodotti**: La regola non si applica se il carrello include uno di questi prodotti

**Esclude Categorie**: La regola non si applica se il carrello include prodotti da queste categorie

**Use Case**: Escludere articoli pesanti/o di grandi dimensioni dalla spedizione gratuita

**Esempio**: Spedizione gratuita tranne per la categoria Mobili
```
Escludi Categorie: [Mobili]
```


### Gruppo Cliente

- **Gruppi Cliente**: La regola si applica solo ai clienti appartenenti ai gruppi selezionati (VIP, Fornitori, ecc.)
- **Selezione vuota**: La regola si applica a TUTTI i gruppi clienti
- **Use Case**: Benefici per i clienti VIP, sconti per fornitori

**Esempio**: Sconto del 15% per la spedizione per i membri VIP
```
Gruppi Cliente: ["VIP"]
```


### Cliente per la Prima Volta

- **Cliente per la Prima Volta**: Attiva per limitare la regola ai clienti senza ordini precedenti
- **Use Case**: Offerte di benvenuto per nuovi clienti

**Esempio**: Sconto di $5 per la spedizione per il primo ordine
```
Cliente per la Prima Volta: Sì
```


## Priorità e Esecuzione delle Regole

Le regole vengono eseguite in **ordine di priorità** (numero maggiore = esecuzione più precoce):

### Meccanica della Priorità

**Esempio di Esecuzione**:
```
Regola A (Priorità 100): Spedizione gratuita se il carrello > $50
Regola B (Priorità 50): Sconto del 10% su tutta la spedizione
Regola C (Priorità 1): Aggiungi un sovrapprezzo di $2 per le zone remote

Carrello: $60, Zona remota
Costo base della spedizione: $15

Passo 1: Valuta la Regola A (Priorità 100)
  Il carrello > $50? SÌ
  Applica: Imposta il costo a $0
  Costo ora: $0

Passo 2: Valuta la Regola B (Priorità 50)
  Applica lo sconto del 10% su $0
  Costo ora: $0 (sempre gratuito)

Passo 3: Valuta la Regola C (Priorità 1)
  Aggiungi un sovrapprezzo di $2 a $0
  Costo ora: $2

Costo finale: $2
```

**Flag per Fermare le Ulteriori Regole**:

Se la Regola A ha `stop_further_rules = True`:
```
Regola A (Priorità 100, stop_further_rules=True): Spedizione gratuita se il carrello > $50
Regola B (Priorità 50): Sconto del 10% su tutta la spedizione
Regola C (Priorità 1): Aggiungi un sovrapprezzo di $2 per le zone remote

Carrello: $60
Base: $15

Passo 1: La Regola A si applica, imposta il costo a $0
        stop_further_rules = True → FERMA

Costo finale: $0 (Le regole B e C non vengono mai eseguite)
```


## Creazione di Regole di Spedizione

**Workflow Passo Passo**:

1. **Vai alle Regole**
   - Impostazioni > Spedizione > Regole di Spedizione
   - Clicca "Aggiungi Regola di Spedizione"

2. **Configurazione Base**
   - **Nome**: Identificativo interno (es. "Spedizione Gratuita Oltre $50")
   - **Descrizione**: Note opzionali (non visibili ai clienti)
   - **Attivo**: Attiva/disattiva
   - **Priorità**: Imposta l'ordine di esecuzione (100 per alta priorità, 1 per bassa)

3. **Scegli il Tipo di Regola**
   - Seleziona il tipo di modifica (sconto %, sconto fisso, costo fisso, gratuito, sovrapprezzo %, sovrapprezzo fisso)
   - Inserisci importo o percentuale

4. **Imposta il Flag per Fermare** (Opzionale)
   - Seleziona "Ferma Ulteriori Regole" se questa regola deve impedire l'esecuzione di regole a bassa priorità
   - Utilizza per regole finali/assolute (es. la spedizione gratuita non dovrebbe avere sovrapprezzi aggiunti dopo)

5. **Definisci le condizioni** (Opzionale - lasciare vuoto per "applica sempre")
  - Validità nel tempo: Date di inizio/fine
  - Valore del carrello: Minimo/Massimo
  - Peso del carrello: Minimo/Massimo
  - Numero di articoli: Minimo/Massimo
  - Zone: Seleziona le zone applicabili
  - Metodi: Seleziona i metodi applicabili
  - Prodotti: Richiesti o esclusi
  - Clienti: Gruppi o solo per i nuovi

6. **Salva la regola**
  - Clicca Salva
  - La regola diventa attiva immediatamente (se l'interruttore Attiva è su Sì)


## Scenari comuni per le regole di spedizione

### Scenario 1: Spedizione gratuita sopra i $50

**Obiettivo**: Offrire spedizione gratuita quando il totale del carrello ≥ $50.

**Configurazione**:
```
Nome: Spedizione gratuita sopra i $50
Tipo: Spedizione gratuita
Priorità: 100
Condizioni:
  Valore minimo del carrello: $50
Ferma ulteriori regole: Sì
```


### Scenario 2: Aggiunta di un sovrapprezzo per le aree remote

**Obiettivo**: Aggiungere un sovrapprezzo di $10 per le consegne nelle aree remote.

**Configurazione**:
```
Nome: Aggiunta di un sovrapprezzo per le aree remote
Tipo: Sovrapprezzo (Fisso)
Importo: $10
Priorità: 50
Condizioni:
  Zone: ["Aree remote"]
Ferma ulteriori regole: No
```


### Scenario 3: Sconto del 20% per i clienti VIP

**Obiettivo**: I clienti VIP ricevono uno sconto del 20% su tutte le spedizioni.

**Configurazione**:
```
Nome: Sconto per la spedizione VIP
Tipo: Sconto (Percentuale)
Percentuale: 20
Priorità: 75
Condizioni:
  Gruppi clienti: ["VIP"]
Ferma ulteriori regole: No
```


### Scenario 4: Tariffa fissa per le vacanze

**Obiettivo**: Tutte le spedizioni sono limitate a $9.99 durante dicembre.

**Configurazione**:
```
Nome: Promozione tariffa fissa dicembre
Tipo: Costo fisso
Importo: $9.99
Priorità: 100
Condizioni:
  Data di inizio: 2026-12-01
  Data di fine: 2026-12-31
Ferma ulteriori regole: Sì
```


### Scenario 5: Aggiunta di un sovrapprezzo per articoli pesanti

**Obiettivo**: Aggiungere un costo aggiuntivo di $15 per gli ordini superiori a 25kg.

**Configurazione**:
```
Nome: Aggiunta di un sovrapprezzo per ordini pesanti
Tipo: Sovrapprezzo (Fisso)
Importo: $15
Priorità: 50
Condizioni:
  Peso minimo: 25kg
Ferma ulteriori regole: No
```


### Scenario 6: Spedizione gratuita per il primo ordine

**Obiettivo**: I clienti nuovi ricevono la spedizione gratuita sul primo ordine.

**Configurazione**:
```
Nome: Spedizione gratuita per il primo ordine
Tipo: Spedizione gratuita
Priorità: 100
Condizioni:
  Cliente nuovo: Sì
Ferma ulteriori regole: Sì
```


### Scenario 7: Spedizione gratuita per categorie specifiche

**Obiettivo**: Spedizione gratuita per gli ordini che includono articoli di categoria promozionale.

**Configurazione**:
```
Nome: Spedizione gratuita per le categorie promozionali
Tipo: Spedizione gratuita
Priorità: 90
Condizioni:
  Categorie richieste: ["Promozioni"]
Ferma ulteriori regole: Sì
```


### Scenario 8: Escludere i mobili dalla spedizione gratuita

**Obiettivo**: Spedizione gratuita sopra i $50, tranne se il carrello include mobili.

Soluzione: Due regole

**Regola 1**:
```
Nome: Spedizione gratuita generale
Tipo: Spedizione gratuita
Priorità: 50
Condizioni:
  Valore minimo del carrello: $50
  Categorie escluse: ["Mobili"]
Ferma ulteriori regole: No
```

**Regola 2**:
```
Nome: Sconto di $5 per gli ordini di mobili
Tipo: Sconto (Fisso)
Importo: $5
Priorità: 40
Condizioni:
  Categorie richieste: ["Mobili"]
  Valore minimo del carrello: $50
Ferma ulteriori regole: No
```


## Strategie per il combinare le regole

### Strategia 1: Sconti sovrapposti

**Consenti a più sconti di sovrapporsi**:
```
Regola A (Priorità 100): 10% di sconto per i VIP → stop_further_rules=No
Regola B (Priorità 50): 15% di sconto sugli ordini >$100 → stop_further_rules=No

Cliente VIP con ordine di $120:
Base: $15
Dopo la Regola A: $13.50 (10% di sconto)
Dopo la Regola B: $11.48 (15% di sconto su $13.50)
```


### Strategia 2: Regole esclusive

**Solo una regola si applica** (priorità più alta):
```
Regola A (Priorità 100): Spedizione gratuita >$50 → stop_further_rules=Sì
Regola B (Priorità 50): 20% di sconto su tutte le spedizioni → stop_further_rules=Sì

Carrello > $50:
La Regola A si applica → Spedizione gratuita → FERMA
La Regola B non viene mai eseguita
```


### Strategia 3: Sovrapprezzi condizionati

**Sconti per primi, sovrapprezzi per ultimi**:
```
Regola A (Priorità 100): Spedizione gratuita >$75
Regola B (Priorità 75): Sconto del 15% per i clienti VIP
Regola C (Priorità 50): Sconto del 10% generale
Regola D (Priorità 25): Sovrapprezzo di $5 per le aree remote
Regola E (Priorità 1): Sovrapprezzo del 10% per il carburante

Ordine: $80, zona remota, cliente VIP
Base: $20
A: $80 > $75 → Gratuita ($0)
B: VIP → 15% di sconto su $0 = $0
C: 10% di sconto su $0 = $0
D: Remota +$5 = $5
E: Carburante +10% di $5 = $5.50
```


Oggetto: 5,50 $ (non gratuito a causa di sovrapprezzi)
```

**Per prevenire ciò, utilizzare stop_further_rules=Si**:
```
Regola A (Priorità 100, stop=Si): Spedizione gratuita >75$

Stessa ordinazione:
A: 80 $ > 75 $ → Gratuita ($0) → FERMA
Oggetto: 0 $ (veramente gratuito)
```

---

## Verifica delle regole di spedizione

**Prima di andare in produzione**:

1. **Crea carrelli di prova**
   - Carrello A: 25 $ (sotto soglia)
   - Carrello B: 55 $ (sopra soglia)
   - Carrello C: 200 $ + zona remota
   - Carrello D: Cliente VIP

2. **Test di ogni regola**
   - Procedi all'acquisto
   - Verifica che venga visualizzato l'importo corretto per la spedizione
   - Controlla l'ordine di esecuzione delle regole

3. **Test della risoluzione della priorità**
   - Più regole che si applicano
   - Verifica che venga eseguita per prima la priorità più alta
   - Controlla il comportamento di stop_further_rules

4. **Test dei casi limite**
   - Valore del carrello esattamente alla soglia
   - Più condizioni che si applicano
   - Regole in conflitto

---

## Risoluzione dei problemi

**Problema 1: La regola non viene applicata**

**Cause**:
- La regola è disattivata
- Una o più condizioni non soddisfatte
- Una regola con priorità più alta ha impostato stop_further_rules=Si
- La validità del tempo è al di fuori della data corrente

**Soluzione**: Verifica tutte le condizioni, controlla la priorità, verifica lo stato attivo.

---

**Problema 2: Importo scontato non previsto**

**Cause**:
- Più regole che si sovrappongono
- Percentuale applicata a un costo già scontato
- Priorità della regola errata

**Soluzione**: Controlla l'ordine delle priorità, verifica i flag stop_further_rules, esegui manualmente il tracciamento dell'esecuzione.

---

**Problema 3: La spedizione gratuita non funziona**

**Cause**:
- Una regola con priorità inferiore che aggiunge costi dopo la regola della spedizione gratuita
- Il carrello non soddisfa il valore minimo richiesto
- Prodotti esclusi nel carrello

**Soluzione**: Utilizza stop_further_rules=Si sulla regola della spedizione gratuita, verifica le condizioni, controlla le esclusioni.

---

## Suggerimenti

- **Utilizza una priorità elevata per la spedizione gratuita** - Priorità 100 assicura che venga eseguita prima di altri aggiustamenti
- **Imposta stop_further_rules per regole assolute** - La spedizione gratuita dovrebbe fermare ulteriori elaborazioni
- **Testa le combinazioni di regole** - Più regole possono interagire in modo imprevisto
- **Usa nomi descrittivi** - "Sconto VIP 20% (Priorità 75)" è meglio di "Regola 3"
- **Documenta la logica complessa** - Aggiungi note nel campo descrizione
- **Inizia con regole semplici** - Aggiungi complessità gradualmente
- **Monitora le prestazioni delle regole** - Controlla se le regole vengono utilizzate o causano confusione
- **Evita troppe regole** - Troppi regole rallentano l'acquisto, usa massimo 5-10
- **Usa le aree per la geografia** - Meglio di molte regole simili per paese
- **Combina con metodi** - Le regole + I metodi funzionano insieme per prezzi complessi
- **Imposta finestre temporali chiare** - Includi sempre le date di fine per le promozioni
- **Testa i casi limite** - Esattamente 50 $, esattamente 5 articoli, ecc.