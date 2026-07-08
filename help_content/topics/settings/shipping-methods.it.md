---
title: Metodi di spedizione
---

I metodi di spedizione sono le opzioni di consegna rivolte ai clienti che vengono visualizzate al momento del checkout - ogni metodo calcola i costi di spedizione utilizzando diverse strategie di prezzo. Spwig supporta 7 tipi di metodi, che vanno da semplici tariffe fisse a complessi calcoli in tempo reale effettuati dai carrier. I metodi possono essere limitati in base al valore minimo/massimo dell'ordine, al peso e alle zone geografiche. I clienti selezionano il metodo preferito al momento del checkout, e il costo calcolato viene aggiunto al totale dell'ordine.

Utilizza questa guida per configurare metodi di spedizione che si adattano al tuo modello aziendale, da una semplice spedizione a tariffa fissa a una complessa tariffa a livelli basata su zone.

## Tipi di metodi di spedizione

Spwig fornisce 7 tipi di metodi di spedizione, ciascuno con una logica diversa per il calcolo dei costi:

### Spedizione a tariffa fissa

**Cos'è**: Costo fisso, indipendentemente dal contenuto del carrello, dalla destinazione o dal peso.

**Quando utilizzarlo**:
- Negozio semplice con costi di spedizione prevedibili
- Un solo tipo di prodotto (dimensioni/peso simili)
- Spedizione nazionale con tariffe standard dei carrier
- Promozioni di spedizione gratuita (utilizzare con le regole di spedizione)

**Configurazione**:
- Imposta **Tipo di metodo** = Tariffa fissa
- Inserisci **Costo fisso** (es. $9.99)
- Opzionale: Imposta le restrizioni sul valore minimo/massimo dell'ordine

**Esempio**: "Spedizione standard - $9.99" per tutti gli ordini nazionali.

---

### Spedizione gratuita

**Cos'è**: Opzione di spedizione a costo zero (nessun costo per il cliente).

**Quando utilizzarlo**:
- Promozioni di spedizione gratuita
- Ordini ad alto valore (combinare con valore minimo dell'ordine)
- Alternativa per il ritiro locale
- Benefici del programma fedeltà

**Configurazione**:
- Imposta **Tipo di metodo** = Spedizione gratuita
- Opzionale: Imposta **Valore minimo dell'ordine** (es. gratuita per ordini superiori a $50)
- Funziona bene con le regole di spedizione per la spedizione gratuita condizionata

**Esempio**: "Spedizione gratuita per ordini superiori a $50" con min_order_value = $50.

---

### Spedizione basata sul peso

**Cos'è**: Il costo viene calcolato da una tabella a livelli basata sul peso totale del carrello.

**Quando utilizzarlo**:
- Prodotti con pesi variabili (libri, hardware, alimentari)
- Modelli di prezzo dei carrier basati sul peso
- Rapporto prevedibile tra peso e costo

**Configurazione**:
1. Imposta **Tipo di metodo** = Basato sul peso
2. Crea **Tabella tariffa di spedizione** con basis_type = "weight"
3. Aggiungi **Livelli di tariffa di spedizione** (es. 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opzionale: Limitare a specifiche zone

**Esempio**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Come funziona**: Il carrello calcola il peso totale → trova il livello corrispondente → restituisce la tariffa del livello.

---

### Spedizione basata sul prezzo

**Cos'è**: Il costo viene calcolato da una tabella a livelli basata sul totale del carrello.

**Quando utilizzarlo**:
- I costi di spedizione sono correlati al valore dell'ordine
- Incentivare un valore del carrello più alto (ridurre la tariffa per dollaro a livelli più alti)
- Alternativa semplice alla spedizione basata sul peso per prodotti con prezzo simile

**Configurazione**:
1. Imposta **Tipo di metodo** = Basato sul prezzo
2. Crea **Tabella tariffa di spedizione** con basis_type = "price"
3. Aggiungi **Livelli di tariffa di spedizione** (es. $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Esempio**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Gratuita
```

**Come funziona**: Il carrello calcola il totale → trova il livello corrispondente → restituisce la tariffa del livello.

---

### Tariffe in tempo reale dei carrier

**Cos'è**: Tariffe in tempo reale ottenute da API dei carrier (FedEx, UPS, DHL) al momento del checkout.

**Quando utilizzarlo**:
- Costi di spedizione variabili in base alla destinazione
- Opzioni multiple di carrier per i clienti
- Prezzi dei carrier precisi senza tabelle di tariffe manuali
- Spedizione internazionale con prezzi complessi

**Configurazione**:
1. Imposta **Tipo di metodo** = Reale in tempo reale
2. Crea **Account fornitore** (Impostazioni > Spedizione > Account fornitori)
3. Inserisci le credenziali API del carrier (numero di account, chiave API, segreto)
4. Collega l'account fornitore al metodo di spedizione
5. Opzionale: Aggiungi un percentuale di markup o un markup fisso

**Requisiti**:
- Account attivo del carrier (FedEx, UPS, DHL, ecc.)
- Credenziali API ottenute dal carrier
- Pacchetti di spedizione definiti (per il calcolo del peso dimensionale)

**Esempio**: Il metodo "FedEx Ground" recupera le tariffe live di FedEx in base al peso del carrello, alle dimensioni e alla destinazione al momento del checkout.

**Come funziona**:
1. Il cliente inserisce l'indirizzo al momento del checkout
2. Il sistema chiama l'API del carrier con origine, destinazione, dimensioni del pacchetto e peso
3. Il carrier restituisce l'offerta di prezzo
4. Eventuale markup applicato
5. La tariffa viene visualizzata al cliente

---

### Ritiro in loco

**Cos'è**: Il cliente ritira l'ordine in un'ubicazione fisica (nessun costo di consegna).

**Quando utilizzarlo**:
- Negozio al dettaglio che offre il ritiro
- Opzioni di ritiro presso il magazzino
- Eventi o bancarelle di mercato
- Eliminare i costi di spedizione per i clienti locali

**Configurazione**:
1. Imposta **Tipo di metodo** = Ritiro in loco
2. Crea **Ubicazione** (Impostazioni > Spedizione > Ubicazioni)
   - Imposta l'indirizzo, gli orari di apertura, la capacità di ritiro
3. Collega l'ubicazione (o le ubicazioni) al metodo
4. Opzionale: Imposta il tempo di preparazione del ritiro (es. "Pronto in 2 ore")

**Esperienza del cliente**:
- Seleziona "Ritiro in loco" al momento del checkout
- Scegli l'ubicazione di ritiro (se ce ne sono più di una)
- Scegli la data/ora di ritiro in base alla disponibilità
- Riceve una notifica quando l'ordine è pronto

**Esempio**: "Ritiro in negozio - Gratuito" con 3 ubicazioni retail, pronti entro 24 ore.

---

### Spedizione a tariffa tabellare

**Cos'è**: Tariffa a livelli flessibile basata su peso, prezzo o quantità con mira avanzata sulle zone.

**Quando utilizzarlo**:
- Prezzi complessi (diverse tariffe per zona E peso)
- Bisogno di un controllo maggiore rispetto alla spedizione basata su peso o prezzo
- Più fattori di prezzo (es. peso + destinazione + quantità)

**Configurazione**:
1. Imposta **Tipo di metodo** = Tariffa tabellare
2. Crea **Tabella tariffa di spedizione**
3. Definisci **basis_type**: peso, prezzo o quantità
4. Aggiungi **Livelli di tariffa di spedizione** con valori min/max
5. Opzionale: Limitare i livelli a specifiche zone o paesi

**Differenza rispetto a peso/prezzo basato**: La tariffa tabellare supporta le restrizioni geografiche per livello, permettendo tariffe diverse per lo stesso peso/prezzo in diverse zone.

**Esempio**:
```
Zona A (Nazionale):
  0-5kg: $10
  5-10kg: $15

Zona B (Rimota):
  0-5kg: $18
  5-10kg: $25
```

**Come funziona**: Il carrello calcola il valore di base (peso/prezzo/quantità) → trova il livello corrispondente per la zona del cliente → restituisce la tariffa del livello.

---

## Configurazione del metodo di spedizione

Tutti i metodi di spedizione condividono queste impostazioni comuni:

### Impostazioni di base

- **Nome**: Identificatore interno (non mostrato ai clienti)
- **Nome visualizzato**: Nome rivolto ai clienti al momento del checkout (es. "Spedizione standard", "Spedizione espressa")
- **Descrizione**: Testo di aiuto opzionale mostrato al momento del checkout (es. "Consegna in 3-5 giorni lavorativi")
- **Tipo di metodo**: Uno dei 7 tipi sopra
- **Attivo**: Interruttore per abilitare/disabilitare il metodo senza eliminarlo

### Impostazioni dei costi

- **Costo fisso**: Solo per i metodi a tariffa fissa
- **Tabella tariffa**: Per i metodi basati su peso, prezzo, tariffa tabellare
- **Account fornitore**: Per i metodi in tempo reale dei carrier
- **Classe fiscale**: Applica l'imposta al costo di spedizione (se applicabile)

### Restrizioni

**Restrizioni sul valore dell'ordine**:
- **Valore minimo dell'ordine**: Il metodo è disponibile solo se il totale del carrello ≥ importo (es. spedizione gratuita per ordini superiori a $50)
- **Valore massimo dell'ordine**: Il metodo è nascosto se il totale del carrello > importo (es. tariffa fissa solo per ordini inferiori a $100)

**Restrizioni sul peso**:
- **Peso minimo**: Il metodo è disponibile solo se il peso del carrello ≥ importo
- **Peso massimo**: Il metodo è nascosto se il peso del carrello > importo (comune per opzioni di spedizione leggere)

**Restrizioni geografiche**:
- **Zone di spedizione**: Collega il metodo a specifiche zone (nazionali, internazionali, regionali)
- Zone vuote = disponibile per tutti gli indirizzi
- Multiple zone = disponibile per qualsiasi zona corrispondente

### Impostazioni avanzate

- **Priorità**: Ordine di visualizzazione al momento del checkout (numero più basso = più alto nell'elenco)
- **Tariffa di gestione**: Tariffa aggiuntiva fissa aggiunta al costo calcolato
- **Limite per spedizione gratuita**: Imposta automaticamente il costo a $0 se il totale del carrello ≥ limite (alternativa al min_order_value)

---

## Creare un metodo di spedizione

**Flusso di lavoro passo-passo**:

1. **Naviga ai metodi di spedizione**
   - Vai a Impostazioni > Carrello > Metodi di spedizione
   - Clicca su "Aggiungi metodo di spedizione"

2. **Scegli il tipo di metodo**
   - Seleziona il tipo appropriato in base alla tua strategia di prezzo
   - Il tipo determina i campi disponibili per la configurazione dei costi

3. **Configura le informazioni di base**
   - Nome: Riferimento interno (es. "domestic_ground")
   - Nome visualizzato: Rivolto ai clienti (es. "Spedizione terrestre")
   - Descrizione: Intervallo di consegna (es. "5-7 giorni lavorativi")

4. **Imposta il calcolo dei costi**
   - **Tariffa fissa**: Inserisci il costo fisso
   - **Peso/Prezzo/Tariffa tabellare**: Crea una tabella tariffa (vedi di seguito)
   - **Reale in tempo reale**: Collega l'account fornitore
   - **Gratuito/Ritiro**: Nessuna configurazione di costo necessaria

5. **Aggiungi restrizioni (opzionale)**
   - Valore minimo/massimo dell'ordine
   - Peso minimo/massimo
   - Zone di spedizione

6. **Imposta la priorità**
   - I numeri più bassi appaiono prima al momento del checkout
   - Ordine consigliato: Gratuito (1), Ritiro in loco (2), Standard (3), Espresso (4)

7. **Attiva il metodo**
   - Imposta "Attivo" = Sì
   - Salva

---

## Creare tabelle tariffarie

Per i metodi basati su peso, prezzo e tariffa tabellare:

**Passo 1: Creare una tabella tariffa**
- Vai a Impostazioni > Spedizione > Tabelle tariffarie
- Clicca su "Aggiungi tabella tariffa"
- Imposta **Nome** (es. "Livelli di peso nazionali")
- Imposta **Tipo di base**: peso, prezzo o quantità

**Passo 2: Aggiungere livelli**
- Clicca su "Aggiungi livello"
- Imposta **Valore minimo** e **Valore massimo** (intervallo per il matching)
- Imposta **Tariffa** (costo per questo livello)
- Opzionale: Limitare a specifiche zone o paesi
- Salva il livello

**Passo 3: Ripetere per tutti i livelli**
- Coprire l'intervallo completo (da 0 al valore massimo previsto)
- Assicurarsi che non ci siano lacune (es. 0-5, 5-10, 10-20, 20+)
- Utilizzare `null` per il valore massimo nel livello finale (illimitato)

**Passo 4: Collegare alla tabella di spedizione**
- Modifica il metodo di spedizione
- Seleziona la tabella tariffa dal menu a discesa
- Salva

**Esempio di tabella basata su peso**:
```
Nome: Livelli di peso nazionali
Base: Peso

Livelli:
1. Min: 0g, Max: 2000g, Tariffa: $8
2. Min: 2000g, Max: 5000g, Tariffa: $12
3. Min: 5000g, Max: 10000g, Tariffa: $18
4. Min: 10000g, Max: null, Tariffa: $25
```

---

## Scenario di spedizione comuni

### Scenario 1: Spedizione nazionale di base

**Obiettivo**: Tariffa fissa di $9.99 per tutti gli ordini nazionali.

**Soluzione**:
- Tipo di metodo: Tariffa fissa
- Costo fisso: $9.99
- Zona di spedizione: "Nazionale" (solo il tuo paese)

---

### Scenario 2: Spedizione gratuita per ordini superiori a $50

**Obiettivo**: Incentivare un valore del carrello più alto con un limite per la spedizione gratuita.

**Opzione di soluzione A** (consigliata):
- Tipo di metodo: Spedizione gratuita
- Valore minimo dell'ordine: $50
- Nome visualizzato: "Spedizione gratuita (Ordini $50+)")

**Opzione di soluzione B** (Utilizzando le regole):
- Tipo di metodo: Tariffa fissa
- Costo fisso: $9.99
- Crea regola di spedizione:
  - Condizione: Valore del carrello ≥ $50
  - Azione: Imposta il costo a $0

---

### Scenario 3: Spedizione basata su peso nazionale + internazionale

**Obiettivo**: Diverse tariffe per nazionale rispetto all'internazionale basate sul peso.

**Soluzione**:
1. Crea 2 zone: "Nazionale", "Internazionale"
2. Crea 2 tabelle tariffarie: "Tariffe di peso nazionali", "Tariffe di peso internazionali"
3. Crea 2 metodi:
   - "Spedizione nazionale" → collega alla zona nazionale + tabella tariffa nazionale
   - "Spedizione internazionale" → collega alla zona internazionale + tabella tariffa internazionale

---

### Scenario 4: Opzioni multiple di carrier

**Obiettivo**: Consentire ai clienti di scegliere tra FedEx Ground, FedEx Express, UPS Ground.

**Soluzione**:
1. Crea account fornitore per l'API FedEx
2. Crea account fornitore per l'API UPS
3. Crea 3 metodi in tempo reale:
   - "FedEx Ground" → fornitore FedEx, codice servizio = "FEDEX_GROUND"
   - "FedEx Express" → fornitore FedEx, codice servizio = "FEDEX_EXPRESS"
   - "UPS Ground" → fornitore UPS, codice servizio = "UPS_GROUND"
4. Tutti e 3 i metodi interrogano le API dei carrier al momento del checkout e visualizzano le tariffe in tempo reale

---

### Scenario 5: Ritiro in loco + consegna

**Obiettivo**: Il negozio al dettaglio offre sia opzioni di ritiro che di consegna.

**Soluzione**:
1. Crea ubicazione: "Negozio principale" con indirizzo, orari, tempo di preparazione
2. Crea 2 metodi:
   - "Ritiro in loco" → tipo Ritiro in loco, collega all'ubicazione principale
   - "Consegna standard" → tariffa fissa $9.99
3. I clienti vedono entrambe le opzioni al momento del checkout

---

## Test dei metodi di spedizione

Prima di andare online, testa tutti i metodi:

1. **Crea un carrello di test**
   - Aggiungi prodotti con diversi pesi/prezzi
   - Procedi al checkout

2. **Testa ogni metodo**
   - Inserisci indirizzi in diverse zone
   - Verifica che i metodi corretti appaiano
   - Controlla che i costi calcolati corrispondano alle aspettative

3. **Testa le restrizioni**
   - Aggiungi articoli fino a raggiungere il valore minimo dell'ordine → verifica che la spedizione gratuita appaia
   - Aggiungi articoli pesanti → verifica che i livelli basati sul peso funzionino
   - Testa le restrizioni delle zone → verifica che i metodi siano nascosti per le zone escluse

4. **Testa i metodi in tempo reale** (se applicabile)
   - Utilizza credenziali di test del fornitore
   - Verifica che le tariffe siano restituite correttamente
   - Controlla l'accuratezza delle tariffe rispetto al sito web del fornitore

---

## Risoluzione dei problemi

**Problema 1: Il metodo non appare al momento del checkout**

**Causa**:
- Il metodo non è attivo
- Il carrello non soddisfa il valore minimo/massimo dell'ordine
- Il carrello non soddisfa il peso minimo/massimo
- L'indirizzo del cliente non corrisponde a nessuna zona collegata
- Nessun livello della tabella tariffa copre il peso/prezzo del carrello

**Soluzione**: Controlla le restrizioni, verifica lo stato attivo, assicurati che le zone/livelli coprano la situazione del cliente.

---

**Problema 2: Le tariffe in tempo reale non funzionano**

**Causa**:
- Credenziali API non valide
- Account fornitore non attivo
- Nessun pacchetto di spedizione definito (il carrier necessita delle dimensioni)
- Indirizzo di origine non impostato
- API del carrier non disponibile

**Soluzione**: Testa la connessione del fornitore, verifica le credenziali, assicurati che i pacchetti siano configurati, controlla l'indirizzo di origine nelle impostazioni.

---

**Problema 3: Costo calcolato errato**

**Causa**:
- Livelli della tabella tariffa con lacune o sovrapposizioni
- Valori min/max dei livelli in unità errate (grammi vs kg)
- Tariffa di gestione aggiunta inaspettatamente
- Regola di spedizione che modifica il costo

**Soluzione**: Rivedi i livelli della tabella tariffa, verifica le unità, controlla la priorità delle regole di spedizione.

---

## Consigli

- **Inizia semplice** - Utilizza una tariffa fissa per il primo metodo, aggiungi complessità quando necessario
- **Testa accuratamente** - Verifica che tutti i metodi funzionino in ambiente di staging prima di abilitarli in produzione
- **Utilizza nomi descrittivi** - "Spedizione standard (5-7 giorni)" è meglio di "Metodo 1"
- **Imposta tempi di consegna realistici** - Sotto-prometti, sopra-consegna per la soddisfazione del cliente
- **Offri il ritiro se possibile** - Riduce i costi di spedizione, migliora la convenienza per i clienti
- **Monitora l'affidabilità delle API dei carrier** - Hai un'alternativa a tariffa fissa se le tariffe in tempo reale falliscono
- **Utilizza le zone per la spedizione internazionale** - Diverse tariffe per regione evitano perdite su destinazioni costose
- **Combina con le regole di spedizione** - Le regole aggiungono logica condizionale (promozioni di spedizione gratuita, sovrapprezzi per aree remote)
- **Mantieni i metodi limitati** - 2-4 opzioni al momento del checkout evitano la paralisi decisionale
- **Aggiorna le tabelle tariffarie stagionalmente** - Le tariffe dei carrier cambiano, rivedi annualmente
- **Utilizza la priorità con saggezza** - Metti le opzioni gratuite/cheap in alto, le opzioni costose in fondo
