---
title: Metodi di spedizione
---

I metodi di spedizione sono le opzioni di consegna rivolte ai clienti, visualizzate al momento del checkout—ogni metodo calcola i costi di spedizione utilizzando diverse strategie di prezzo. Spwig supporta 7 tipi di metodo, che vanno da semplici tariffe fisse a complessi prezzi in tempo reale calcolati dai carrier. I metodi possono essere limitati in base al valore minimo/massimo dell'ordine, al peso e alle zone geografiche. I clienti selezionano il metodo preferito al momento del checkout, e il costo calcolato viene aggiunto al totale dell'ordine.

Utilizza questa guida per configurare metodi di spedizione che si adattino al tuo modello aziendale, dai semplici metodi a tariffa fissa ai complessi metodi basati su zone con tariffe a livelli.

## Tipi di metodi di spedizione

Spwig fornisce 7 tipi di metodi di spedizione, ciascuno con una logica diversa per il calcolo dei costi:

### Spedizione a tariffa fissa

**Cos'è**: Costo fisso, indipendentemente dal contenuto del carrello, dalla destinazione o dal peso.

**Quando utilizzarlo**:
- Negozio semplice con costi di spedizione prevedibili
- Un solo tipo di prodotto (dimensioni/peso simili)
- Spedizione nazionale con tariffe standard dei carrier
- Promozioni di spedizione gratuita (utilizzare con promozioni di spedizione)

**Configurazione**:
- Imposta **Tipo di metodo** = Tariffa fissa
- Inserisci **Costo fisso** (es. $9.99)
- Opzionale: Imposta i limiti di valore minimo/massimo dell'ordine

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
- Funziona bene con le promozioni di spedizione per la spedizione gratuita condizionata

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
2. Crea **Tabella delle tariffe di spedizione** con basis_type = "weight"
3. Aggiungi **Livelli di tariffe di spedizione** (es. 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
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

**Cos'è**: Il costo viene calcolato da una tabella a livelli basata sul sottototale del carrello.

**Quando utilizzarlo**:
- I costi di spedizione sono correlati al valore dell'ordine
- Incentivare un valore del carrello più alto (tariffa più bassa per dollaro a livelli più alti)
- Alternativa semplice alla spedizione basata sul peso per prodotti con prezzo simile

**Configurazione**:
1. Imposta **Tipo di metodo** = Basato sul prezzo
2. Crea **Tabella delle tariffe di spedizione** con basis_type = "price"
3. Aggiungi **Livelli di tariffe di spedizione** (es. $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Esempio**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Gratuita
```

**Come funziona**: Il carrello calcola il sottototale → trova il livello corrispondente → restituisce la tariffa del livello.

---

### Tariffe di spedizione in tempo reale

**Cos'è**: Tariffe in tempo reale ottenute da API dei carrier (FedEx, UPS, DHL) al momento del checkout.

**Quando utilizzarlo**:
- Costi di spedizione variabili in base alla destinazione
- Opzioni di diversi carrier per i clienti
- Prezzi dei carrier precisi senza tabelle di tariffe manuali
- Spedizione internazionale con prezzi complessi

**Configurazione**:
1. Imposta **Tipo di metodo** = In tempo reale
2. Crea **Account del provider** (Impostazioni > Spedizione > Account dei provider)
3. Inserisci le credenziali API del carrier (numero di account, chiave API, segreto)
4. Collega l'account del provider al metodo di spedizione
5. Opzionale: Aggiungi un margine percentuale o un margine fisso

**Requisiti**:
- Account attivo del carrier (FedEx, UPS, DHL, ecc.)
- Credenziali API del carrier
- Pacchetti di spedizione definiti (per il calcolo del peso dimensionale)

**Esempio**: Il metodo "FedEx Ground" recupera le tariffe live di FedEx in base al peso del carrello, alle dimensioni e alla destinazione al momento del checkout.

**Come Funziona**:
1. Il cliente inserisce l'indirizzo al momento del checkout
2. Il sistema chiama l'API del carrier con origine, destinazione, dimensioni del pacco e peso
3. Il carrier restituisce l'offerta di prezzo
4. Applicazione opzionale di markup
5. La tariffa viene visualizzata al cliente

---

### Ritiro in Locale

**Cos'è**: Il cliente ritira l'ordine in un'ubicazione fisica (nessun costo di spedizione).

**Quando Usarlo**:
- Negozio al dettaglio che offre il ritiro
- Opzioni di ritiro presso il magazzino
- Eventi o bancarelle
- Eliminare i costi di spedizione per i clienti locali

**Configurazione**:
1. Imposta **Tipo di Metodo** = Ritiro in Locale
2. Crea **Ubicazione** (Impostazioni > Spedizione > Ubicazioni)
   - Imposta indirizzo, orari di apertura, capacità di ritiro
3. Collega l'ubicazione (o le ubicazioni) al metodo
4. Opzionale: Imposta il tempo di preparazione del ritiro (es. "Pronto in 2 ore")

**Esperienza del Cliente**:
- Seleziona "Ritiro in Locale" al momento del checkout
- Scegli l'ubicazione di ritiro (se ce ne sono più di una)
- Scegli la data/ora di ritiro in base alla disponibilità
- Riceve una notifica quando l'ordine è pronto

**Esempio**: "Ritiro in Negozio - Gratuito" con 3 ubicazioni retail, pronti entro 24 ore.

---

### Spedizione a Tabelle

**Cos'è**: Prezzo flessibile a livelli basato su peso, prezzo o quantità con targeting avanzato per zone.

**Quando Usarlo**:
- Prezzi complessi (diverse tariffe per zona E PESO)
- Bisogno di un controllo maggiore rispetto a solo peso o prezzo
- Più fattori di prezzo (es. peso + destinazione + quantità)

**Configurazione**:
1. Imposta **Tipo di Metodo** = Spedizione a Tabelle
2. Crea **Tabella di Tariffa di Spedizione**
3. Definisci **basis_type**: peso, prezzo o quantità
4. Aggiungi **Livelli di Tariffa di Spedizione** con valori minimi/massimi
5. Opzionale: Limita i livelli a specifiche zone o paesi

**Differenza rispetto a Peso/Prezzo**: La tariffa a tabella supporta le restrizioni geografiche per livello, permettendo tariffe diverse per lo stesso peso/prezzo in diverse zone.

**Esempio**:
```
Zona A (Domestica):
  0-5kg: $10
  5-10kg: $15

Zona B (Rimota):
  0-5kg: $18
  5-10kg: $25
```

**Come Funziona**: Il carrello calcola il valore di base (peso/prezzo/quantità) → trova il livello corrispondente per la zona del cliente → restituisce la tariffa del livello.

---

## Configurazione del Metodo di Spedizione

Tutti i metodi di spedizione condividono queste impostazioni comuni:

### Impostazioni di Base

- **Nome**: Identificatore interno (non mostrato ai clienti)
- **Nome Visualizzato**: Nome rivolto al cliente al momento del checkout (es. "Spedizione Standard", "Spedizione Espressa")
- **Descrizione**: Testo di aiuto opzionale mostrato al momento del checkout (es. "Consegna in 3-5 giorni lavorativi")
- **Tipo di Metodo**: Uno dei 7 tipi sopra
- **Attivo**: Interruttore per abilitare/disabilitare il metodo senza eliminarlo

### Impostazioni di Costo

- **Costo Fisso**: Solo per i metodi a tariffa fissa
- **Tabella di Tariffa**: Per i metodi basati su peso, prezzo o tariffa a tabella
- **Account Fornitore**: Per i metodi di spedizione in tempo reale con carrier
- **Classe di Imposta**: Applica l'IVA al costo di spedizione (se applicabile)

### Restrizioni

**Restrizioni sul Valore dell'Ordine**:
- **Valore Minimo dell'Ordine**: Il metodo è disponibile solo se il totale del carrello è ≥ importo (es. spedizione gratuita per ordini superiori a $50)
- **Valore Massimo dell'Ordine**: Il metodo è nascosto se il totale del carrello > importo (es. tariffa fissa solo per ordini inferiori a $100)

**Restrizioni sul Peso**:
- **Peso Minimo**: Il metodo è disponibile solo se il peso del carrello ≥ importo
- **Peso Massimo**: Il metodo è nascosto se il peso del carrello > importo (comune per opzioni di spedizione per oggetti leggeri)

**Restrizioni Geografiche**:
- **Zone di Spedizione**: Collega il metodo a specifiche zone (domestiche, internazionali, regionali)
- Zone vuote = disponibile per tutti gli indirizzi
- Più zone = disponibile per qualsiasi zona corrispondente

### Impostazioni Avanzate

- **Priorità**: Ordine di visualizzazione al momento del checkout (numero più basso = più alto nella lista)
- **Tariffa di Gestione**: Tariffa aggiuntiva fissa aggiunta al costo calcolato
- **Limite per Spedizione Gratuita**: Imposta automaticamente il costo a $0 se il totale del carrello ≥ limite (alternativa al min_order_value)

---

## Creare un Metodo di Spedizione

**Flusso di Lavoro Passo Passo**:

1. **Naviga verso i Metodi di Spedizione**
   - Vai a Impostazioni > Carrello > Metodi di Spedizione
   - Clicca su "Aggiungi Metodo di Spedizione"

2. **Scegliere il Tipo di Metodo**
   - Selezionare il tipo appropriato in base alla strategia di prezzo
   - Il tipo determina i campi disponibili per la configurazione dei costi

3. **Configurare le Informazioni di Base**
   - Nome: Riferimento interno (es. "domestic_ground")
   - Nome Visualizzato: Orientato al cliente (es. "Spedizione Standard")
   - Descrizione: Intervallo di consegna (es. "5-7 giorni lavorativi")

4. **Impostare il Calcolo dei Costi**
   - **Tariffa Fissa**: Inserire un costo fisso
   - **Peso/Prezzo/Tabella di Tariffa**: Creare una tabella di tariffa (vedi di seguito)
   - **In Tempo Reale**: Collegare l'account del fornitore
   - **Gratuito/Ritiro in Locale**: Nessuna configurazione dei costi necessaria

5. **Aggiungere Restrizioni (Opzionale)**
   - Valore minimo/massimo dell'ordine
   - Peso minimo/massimo
   - Zone di spedizione

6. **Impostare la Priorità**
   - I numeri più bassi appaiono per primi durante il checkout
   - Ordine consigliato: Gratuito (1), Ritiro in Locale (2), Standard (3), Espresso (4)

7. **Attivare il Metodo**
   - Attiva il toggle "Attivo" = Sì
   - Salva

---

## Creare Tabelle di Tariffa

Per i metodi basati sul peso, sul prezzo e sulle tabelle di tariffa:

**Passo 1: Creare una Tabella di Tariffa**
- Vai a Impostazioni > Spedizione > Tabelle di Tariffa
- Fare clic su "Aggiungi Tabella di Tariffa"
- Impostare **Nome** (es. "Domestic Weight Tiers")
- Impostare **Tipo di Base**: peso, prezzo o quantità

**Passo 2: Aggiungere Livelli**
- Fare clic su "Aggiungi Livello"
- Impostare **Valore Minimo** e **Valore Massimo** (intervallo per il matching)
- Impostare **Tariffa** (costo per questo livello)
- Opzionale: Limitare a specifiche zone o paesi
- Salva il livello

**Passo 3: Ripetere per Tutti i Livelli**
- Coprire l'intero intervallo (da 0 al valore massimo previsto)
- Assicurarsi che non ci siano lacune (es. 0-5, 5-10, 10-20, 20+)
- Usare `null` per il valore massimo nell'ultimo livello (illimitato)

**Passo 4: Collegare al Metodo di Spedizione**
- Modificare il metodo di spedizione
- Selezionare la tabella di tariffa dal menu a discesa
- Salva

**Esempio di Tabella basata sul Peso**:
```
Nome: Domestic Weight Tiers
Base: Peso

Livelli:
1. Min: 0g, Max: 2000g, Tariffa: $8
2. Min: 2000g, Max: 5000g, Tariffa: $12
3. Min: 5000g, Max: 10000g, Tariffa: $18
4. Min: 10000g, Max: null, Tariffa: $25
```

---

## Scenario di Spedizione Comuni

### Scenario 1: Spedizione Domestica di Base

**Obiettivo**: Tariffa fissa di $9.99 per tutti gli ordini domestici.

**Soluzione**:
- Tipo di Metodo: Tariffa Fissa
- Costo Fisso: $9.99
- Zona di Spedizione: "Domestico" (solo il tuo paese)

---

### Scenario 2: Spedizione Gratuita per Ordini di $50

**Obiettivo**: Incentivare valori del carrello più elevati con un limite per la spedizione gratuita.

**Opzione di Soluzione A** (Raccomandata):
- Tipo di Metodo: Spedizione Gratuita
- Valore Minimo dell'Ordine: $50
- Nome Visualizzato: "Spedizione Gratuita (Ordini $50+)")

**Opzione di Soluzione B** (Utilizzando le Regole):
- Tipo di Metodo: Tariffa Fissa
- Costo Fisso: $9.99
- Creare una Promozione di Spedizione:
  - Condizione: Valore del carrello ≥ $50
  - Azione: Impostare il costo a $0

---

### Scenario 3: Spedizione basata sul Peso per Domestico + Internazionale

**Obiettivo**: Diverse tariffe per domestico rispetto all'internazionale basate sul peso.

**Soluzione**:
1. Creare 2 zone: "Domestico", "Internazionale"
2. Creare 2 tabelle di tariffa: "Domestic Weight", "International Weight"
3. Creare 2 metodi:
   - "Spedizione Domestica" → collegato alla zona Domestica + tabella di tariffa Domestica
   - "Spedizione Internazionale" → collegato alla zona Internazionale + tabella di tariffa Internazionale

---

### Scenario 4: Opzioni di Più Fornitori

**Obiettivo**: Consentire ai clienti di scegliere tra FedEx Ground, FedEx Express, UPS Ground.

**Soluzione**:
1. Creare un Account Fornitore per l'API di FedEx
2. Creare un Account Fornitore per l'API di UPS
3. Creare 3 metodi in tempo reale:
   - "FedEx Ground" → Fornitore FedEx, codice servizio = "FEDEX_GROUND"
   - "FedEx Express" → Fornitore FedEx, codice servizio = "FEDEX_EXPRESS"
   - "UPS Ground" → Fornitore UPS, codice servizio = "UPS_GROUND"
4. Tutti e 3 i metodi interrogano le API dei fornitori durante il checkout e mostrano le tariffe in tempo reale

---

### Scenario 5: Ritiro in Locale + Spedizione

**Obiettivo**: Il negozio al dettaglio offre sia l'opzione di ritiro in loco che di spedizione.

**Soluzione**:
1. Creare una Posizione: "Main Store" con indirizzo, orari e tempo di preparazione
2. Creare 2 metodi:
   - "Ritiro in Locale" → Tipo Ritiro in Locale, collegato alla posizione Main Store
   - "Spedizione Standard" → Tariffa Fissa $9.99
3. I clienti vedranno entrambe le opzioni durante il checkout

---

## Testare i Metodi di Spedizione

Prima di andare online, testare tutti i metodi:

1. **Crea Carrello di Test**
   - Aggiungi prodotti con diversi pesi/prezzi
   - Procedi al checkout

2. **Testa Ogni Metodo**
   - Inserisci indirizzi in diverse zone
   - Verifica che i metodi corretti appaiano
   - Controlla che i costi calcolati corrispondano alle aspettative

3. **Testa le Restrizioni**
   - Aggiungi articoli fino a raggiungere il valore minimo dell'ordine → verifica che la spedizione gratuita appaia
   - Aggiungi articoli pesanti → verifica che i livelli basati sul peso funzionino
   - Testa le restrizioni per le zone → verifica che i metodi siano nascosti per le zone escluse

4. **Testa i Metodi in Tempo Reale** (se applicabile)
   - Usa le credenziali di test del carrier
   - Verifica che i tassi siano restituiti con successo
   - Controlla l'accuratezza dei tassi rispetto al sito web del carrier

---

## Risoluzione dei Problemi

**Problema 1: Metodo non visualizzato al checkout**

**Causa**:
- Il metodo non è attivo
- Il carrello non soddisfa il valore minimo/massimo dell'ordine
- Il carrello non soddisfa il peso minimo/massimo
- L'indirizzo del cliente non corrisponde a nessuna zona collegata
- Non ci sono livelli della tabella dei tassi che coprono il peso/prezzo del carrello

**Soluzione**: Controlla le restrizioni, verifica lo stato attivo, assicurati che le zone/livelli coprano la situazione del cliente.

---

**Problema 2: Tassi in tempo reale non funzionanti**

**Causa**:
- Credenziali API non valide
- Account del provider non attivo
- Nessun pacchetto di spedizione definito (il carrier necessita delle dimensioni)
- Indirizzo di origine non impostato
- API del carrier non disponibile

**Soluzione**: Testa la connessione al provider, verifica le credenziali, assicurati che i pacchetti siano configurati, controlla l'indirizzo di origine nelle impostazioni.

---

**Problema 3: Costo calcolato errato**

**Causa**:
- I livelli della tabella dei tassi hanno lacune o sovrapposizioni
- I valori minimo/massimo dei livelli sono in unità errate (grammi vs kg)
- Una tariffa aggiuntiva è stata aggiunta inaspettatamente
- Una regola di spedizione sta modificando il costo

**Soluzione**: Rivedi i livelli della tabella dei tassi, verifica le unità, controlla la priorità delle promozioni di spedizione.

---

## Consigli

- **Inizia semplice** - Usa un tasso fisso per il primo metodo, aggiungi complessità quando necessario
- **Testa accuratamente** - Verifica che tutti i metodi funzionino in ambiente di staging prima di abilitarli in produzione
- **Usa nomi descrittivi** - "Spedizione Standard (5-7 giorni)" è meglio di "Metodo 1"
- **Imposta tempi di consegna realistici** - Sotto-prometti e supera per la soddisfazione del cliente
- **Offri la ritirata se possibile** - Riduce i costi di spedizione e migliora la convenienza per il cliente
- **Monitora l'affidabilità dell'API del carrier** - Usa un'opzione a tasso fisso come fallback se i tassi in tempo reale falliscono
- **Usa le zone per l'internazionale** - Diverse tariffe per regione evitano perdite su destinazioni costose
- **Combina con promozioni di spedizione** - Le regole aggiungono logica condizionale (promozioni di spedizione gratuite, sovrapprezzi per aree remote)
- **Mantieni i metodi limitati** - 2-4 opzioni al checkout evitano la paralisi decisionale
- **Aggiorna le tabelle dei tassi stagionalmente** - I tassi dei carrier cambiano, rivedi annualmente
- **Usa la priorità con saggezza** - Metti le opzioni gratuite/cheap in alto, le opzioni costose in fondo