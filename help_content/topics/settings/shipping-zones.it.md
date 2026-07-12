---
title: Zone di spedizione
---

Le zone di spedizione definiscono aree geografiche per tariffe di spedizione mirate: raggruppa paesi, stati o codici postali in zone, quindi collega i metodi di spedizione a zone specifiche per un controllo preciso delle tariffe. Le zone utilizzano un abbinamento basato sulla priorità quando gli indirizzi corrispondono a più zone (vince la priorità più alta). Questo sistema consente strategie di prezzo sofisticate: addebitare di più per aree remote, offrire la spedizione gratuita all'interno del paese o fornire tariffe scontate per aree specifiche.

Utilizza le zone quando hai bisogno di costi di spedizione diversi per aree geografiche diverse, da semplici divisioni tra nazionale e internazionale a complessi prezzi a livelli multi-regione.

## Comprensione delle zone di spedizione

**Cosa sono le zone**: Aree geografiche denominate definite da paesi, stati/province e pattern dei codici postali.

**Come funzionano le zone**:
1. Il cliente inserisce l'indirizzo di spedizione al checkout
2. Il sistema valuta tutte le zone attive
3. Le zone che corrispondono all'indirizzo del cliente sono candidate
4. Se più zone corrispondono, la zona con priorità più alta vince
5. I metodi di spedizione collegati alla zona vincente vengono visualizzati
6. I metodi non collegati a nessuna zona (o collegati a una zona corrispondente) vengono mostrati

**Componenti della zona**:
- **Nome**: Identificatore della zona (es. "Domestico", "UE", "Aree Remote")
- **Paesi**: Elenco dei codici dei paesi inclusi (vuoto = tutti i paesi)
- **Stati/Province**: Restrizioni per stato per paese specifico (opzionale)
- **Pattern dei codici postali**: Pattern regex per l'abbinamento dei codici postali (opzionale)
- **Priorità**: Numero più alto = priorità più alta quando corrispondono più zone

---

## Logica di abbinamento delle zone

Le zone utilizzano **restringimento progressivo** per abbinare gli indirizzi:

### Livello 1: Abbinamento per paese

**Elenco dei paesi vuoto** → La zona corrisponde a TUTTI i paesi

**Elenco dei paesi fornito** → Il paese dell'indirizzo deve essere nell'elenco

Esempio:
```
Zona: "Domestico"
Paesi: ["US"]
→ Corrisponde: Qualsiasi indirizzo USA
→ Non corrisponde: Canada, UK, ecc.
```

### Livello 2: Abbinamento per stato/provincia

**Nessun stato definito** → La zona corrisponde a TUTTI gli stati nei paesi consentiti

**Stati definiti per paesi specifici** → Lo stato dell'indirizzo deve corrispondere

Esempio:
```
Zona: "West Coast"
Paesi: ["US"]
Stati: {"US": ["CA", "OR", "WA"]}
→ Corrisponde: Indirizzi della California, Oregon, Washington
→ Non corrisponde: New York, Texas, ecc.
```

### Livello 3: Abbinamento per codice postale

**Nessun pattern definito** → La zona corrisponde a TUTTI i codici postali nei paesi/stati consentiti

**Pattern definiti** → Il codice postale dell'indirizzo deve corrispondere a almeno un pattern

Esempio:
```
Zona: "Los Angeles Metro"
Paesi: ["US"]
Stati: {"US": ["CA"]}
Pattern dei codici postali: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Corrisponde: 90001, 91210, 90245
→ Non corrisponde: 94102 (San Francisco)
```

**Esempi di pattern regex**:
- `^90[0-9]{3}$` - Area di Los Angeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Formato del codice postale canadese (K1A 0B1)
- `^SW[0-9]{1,2}` - Codici postali di Londra, UK che iniziano con SW

---

## Selezione delle zone basata sulla priorità

Quando più zone corrispondono a un indirizzo, la **priorità** determina quale zona si applica:

**Come funziona la priorità**:
- Numero più alto = priorità più alta
- Se l'indirizzo corrisponde a zone con priorità 100 e 50, la priorità 100 vince
- Solo i metodi di spedizione della zona vincente sono disponibili

**Casi d'uso**:

**Scenario 1: Specifico sovrasta generale**
```
Zona A: "Remote Alaska"
  Paesi: ["US"]
  Stati: {"US": ["AK"]}
  Priorità: 100

Zona B: "Domestico USA"
  Paesi: ["US"]
  Priorità: 50

Indirizzo: Anchorage, AK
→ Corrisponde a entrambe le zone
→ Priorità 100 vince
→ Si applica la zona "Remote Alaska" (costo di spedizione più alto)
```

**Scenario 2: Codice postale sovrasta stato**
```
Zona A: "Manhattan Premium"
  Paesi: ["US"]
  Stati: {"US": ["NY"]}
  Pattern dei codici postali: ["^100[0-2][0-9]$"]
  Priorità: 100

Zona B: "New York State"
  Paesi: ["US"]
  Stati: {"US": ["NY"]}
  Priorità: 50

Indirizzo: New York, NY 10001
→ Corrisponde a entrambe le zone
→ Priorità 100 vince
→ Si applica "Manhattan Premium" (servizio di spedizione premium)
```

---

## Creazione di zone di spedizione

**Flusso di lavoro passo passo**:

1. **Naviga verso le zone**
   - Vai a Impostazioni > Spedizione > Zone di spedizione
   - Clicca su "Aggiungi zona di spedizione"

2. **Configurazione di base**
   - **Nome**: Identificatore descrittivo (es. "Unione Europea", "West Coast", "Arene Remote")
   - **Priorità**: Imposta l'importanza relativa (100 per specifico, 50 per generale, 1 per fallback)
   - **Attivo**: Toggle per abilitare/disabilitare

3. **Definisci la copertura geografica**

   **Opzione A: Tutti i Paesi** (lascia la lista dei paesi vuota)
   - La zona corrisponde a ogni indirizzo a livello globale
   - Utilizzare per zone predefinite/fallback

   **Opzione B: Paesi Specifici**
   - Fare clic su "Aggiungi Paese"
   - Seleziona i paesi dal menu a discesa (US, CA, UK, ecc.)
   - Ripetere per tutti i paesi inclusi

   **Opzione C: Stati/Province Specifici**
   - Dopo aver aggiunto i paesi, fare clic su "Aggiungi Stati" per ogni paese
   - Seleziona gli stati dal menu a discesa
   - Esempio: US → CA, OR, WA per West Coast

   **Opzione D: Pattern dei Codici Postali** (avanzato)
   - Inserisci i pattern regex (uno per riga)
   - Testa i pattern con codici postali di esempio
   - Fare clic su "Valida Pattern" per controllare la sintassi

4. **Collega ai Metodi di Spedizione**
   - I metodi possono essere collegati quando si modifica il metodo (non nella configurazione della zona)
   - Oppure collega le zone ai metodi esistenti: Modifica Metodo → Zone di Spedizione → Seleziona le zone

5. **Imposta la Priorità di Visualizzazione**
   - Le zone con priorità più alta sovrascrivono quelle con priorità più bassa quando corrispondono a più di una zona
   - Consigliato: Zone specifiche (100), Zone regionali (50), Zona predefinita (1)

6. **Attiva la Zona**
   - Toggle "Attivo" = Sì
   - Salva

---

## Configurazioni di Zona Comuni

### Configurazione 1: Nazionale vs Internazionale

**Obiettivo**: Diverse tariffe per nazionale rispetto a tutti gli altri paesi.

```
Zona 1: "Domestico"
  Paesi: [Codice del tuo Paese]
  Priorità: 50

Zona 2: "Internazionale"
  Paesi: [Lascia vuoto o seleziona tutti gli altri paesi]
  Priorità: 1
```

**Metodi di Spedizione**:
- "Standard Nazionale" → Collegato alla zona Domestico
- "Spedizione Internazionale" → Collegato alla zona Internazionale

---

### Configurazione 2: Internazionale a Multi-Ruolo

**Obiettivo**: Diverse tariffe per UE, Nord America, Asia, Resto del Mondo.

```
Zona 1: "Unione Europea"
  Paesi: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priorità: 100

Zona 2: "Nord America"
  Paesi: [US, CA, MX]
  Priorità: 100

Zona 3: "Asia-Pacifico"
  Paesi: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priorità: 100

Zona 4: "Resto del Mondo"
  Paesi: [Lascia vuoto]
  Priorità: 1
```

**Metodi di Spedizione**:
- "Spedizione UE" → Zona UE
- "Spedizione Nord America" → Zona Nord America
- "Spedizione Asia-Pacifico" → Zona Asia-Pacifico
- "Spedizione Standard Internazionale" → Zona Resto del Mondo

---

### Configurazione 3: Soprattassa per Area Remota

**Obiettivo**: Aggiungi una soprattassa per codici postali remoti all'interno della zona nazionale.

```
Zona 1: "Domestico Remoto"
  Paesi: [US]
  Pattern Postali: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Priorità: 100

Zona 2: "Domestico Standard"
  Paesi: [US]
  Priorità: 50
```

**Metodi di Spedizione**:
- "Spedizione Remota" → Zona Domestico Remoto (costo più elevato)
- "Spedizione Standard" → Zona Domestico Standard

---

### Configurazione 4: Zone Specifiche per Stato

**Obiettivo**: Diverse tariffe per ogni regione degli Stati Uniti.

```
Zona 1: "West Coast"
  Paesi: [US]
  Stati: {"US": ["CA", "OR", "WA"]}
  Priorità: 100

Zona 2: "East Coast"
  Paesi: [US]
  Stati: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Priorità: 100

Zona 3: "Midwest"
  Paesi: [US]
  Stati: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Priorità: 100

Zona 4: "South"
  Paesi: [US]
  Stati: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Priorità: 100

Zona 5: "Altri Stati USA"
  Paesi: [US]
  Priorità: 50
```

---

## Esempi di Pattern dei Codici Postali

I codici postali utilizzano **regex** (espressioni regolari) per il matching dei pattern:

### Stati Uniti (Codici ZIP)

**Formato**: 5 cifre (es. 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canada (Codici Postali)

**Formato**: A1A 1A1 (lettera-numero-lettera spazio numero-lettera-numero)


Tutti i codici postali canadesi:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$

- **Inizia con 2 zone** - Nazionale e Internazionale, espandi quando necessario
- **Usa la priorità con saggezza** - Zone specifiche 100, regionali 50, fallback 1
- **Testa accuratamente i pattern postali** - Gli errori Regex falliscono in modo silenzioso, causando che le zone non corrispondano
- **Documenta la logica delle zone** - Aggiungi note alla descrizione della zona per spiegare l'intento della copertura
- **Evita troppe zone** - Troppa zone complica la configurazione; usa le promozioni di spedizione per scenari complessi
- **Usa i codici degli stati, non i nomi** - "CA" non "California", "NY" non "New York"
- **Crea una zona di fallback** - Tutti i paesi, priorità 1, assicura che sempre sia disponibile almeno un'opzione di spedizione
- **Monitora le prestazioni delle zone** - Se molti clienti vedono "nessuna spedizione disponibile", ispeziona la copertura delle zone
- **Aggiorna le zone per nuove regioni** - Aggiungi i paesi alla zona UE quando nuovi membri si uniscono
- **Usa nomi descrittivi** - "UE (Escludendo il Regno Unito)" è meglio di "Zona 3"
- **Testa con indirizzi reali** - Usa gli indirizzi reali dei clienti durante i test, non quelli inventati