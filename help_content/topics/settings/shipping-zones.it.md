---
title: Zona di spedizione
---

Le zone di spedizione definiscono aree geografiche per tariffe di spedizione mirate - raggruppa paesi, stati o codici postali in zone, quindi collega i metodi di spedizione a zone specifiche per un controllo preciso delle tariffe. Le zone utilizzano un abbinamento basato sulla priorità quando gli indirizzi corrispondono a più zone (la zona con la priorità più alta vince). Questo sistema consente strategie di prezzo sofisticate: addebitare di più per aree remote, offrire la spedizione gratuita all'interno del paese o fornire tariffe scontate per specifiche regioni.

Utilizza le zone quando hai bisogno di costi di spedizione diversi per diverse aree geografiche, da una semplice divisione tra domestico vs internazionale a una complessa tariffatura a livelli multi-regionale.

## Comprendere le zone di spedizione

**Cosa sono le zone**: Aree geografiche denominate definite da paesi, stati/province e pattern dei codici postali.

**Come funzionano le zone**:
1. Il cliente inserisce l'indirizzo di spedizione al momento del checkout
2. Il sistema valuta tutte le zone attive
3. Le zone che corrispondono all'indirizzo del cliente sono candidate
4. Se più zone corrispondono, la zona con la priorità più alta vince
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

Le zone utilizzano un **restringimento progressivo** per abbinare gli indirizzi:

### Livello 1: Abbinamento per paese

**Elenco dei paesi vuoto** → La zona corrisponde a TUTTI i paesi

**Elenco dei paesi fornito** → Il paese dell'indirizzo deve essere nell'elenco

Esempio:
```
Zona: "Domestico"
Paesi: ["US"]
→ Corrisponde: Qualsiasi indirizzo negli Stati Uniti
→ Non corrisponde: Canada, Regno Unito, ecc.
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
- `^SW[0-9]{1,2}` - Codici postali del Regno Unito che iniziano con SW

---

## Selezione della zona basata sulla priorità

Quando più zone corrispondono a un indirizzo, la **priorità** determina quale zona si applica:

**Come funziona la priorità**:
- Numero più alto = priorità più alta
- Se l'indirizzo corrisponde a zone con priorità 100 e 50, la priorità 100 vince
- Solo i metodi di spedizione della zona vincente sono disponibili

**Casi d'uso**:

**Scenario 1: Specifica sovrasta generale**
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
→ Si applica la zona "Remote Alaska" (costo di spedizione più elevato)
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
→ Si applica "Manhattan Premium" (servizio di consegna premium)
```

---

## Creare zone di spedizione

**Flusso di lavoro passo-passo**:

1. **Naviga verso le zone**
   - Vai a Impostazioni > Spedizione > Zone di spedizione
   - Clicca su "Aggiungi zona di spedizione"

2. **Configurazione di base**
   - **Nome**: Identificatore descrittivo (es. "Unione Europea", "West Coast", "Aree Remote")
   - **Priorità**: Imposta l'importanza relativa (100 per specifico, 50 per generale, 1 per fallback)
   - **Attivo**: Toggle per abilitare/disabilitare

3. **Definisci la copertura geografica**

   **Opzione A: Tutti i paesi** (lascia l'elenco dei paesi vuoto)
   - La zona corrisponde a ogni indirizzo a livello globale
   - Utilizza per zone predefinite/fallback

   **Opzione B: Paesi specifici**
   - Clicca su "Aggiungi Paese"
   - Seleziona i paesi dal menu a discesa (US, CA, UK, ecc.)
   - Ripeti per tutti i paesi inclusi

   **Opzione C: Stati/Province specifici**
   - Dopo aver aggiunto i paesi, clicca su "Aggiungi Stati" per ogni paese
   - Seleziona gli stati dal menu a discesa
   - Esempio: US → CA, OR, WA per West Coast

   **Opzione D: Pattern dei codici postali** (avanzato)
   - Inserisci i pattern regex (uno per riga)
   - Testa i pattern con codici postali di esempio
   - Clicca su "Valida i pattern" per controllare la sintassi

4. **Collega ai metodi di spedizione**
   - I metodi possono essere collegati quando si modifica il metodo (non nella configurazione della zona)
   - Oppure collega le zone ai metodi esistenti: Modifica Metodo → Zone di spedizione → Seleziona le zone

5. **Imposta la priorità di visualizzazione**
   - Le zone con priorità più alta sovrastano quelle con priorità più bassa quando corrispondono a più zone
   - Consigliato: Zone specifiche (100), Zone regionali (50), Zona predefinita (1)

6. **Attiva la zona**
   - Toggle "Attivo" = Sì
   - Salva

---

## Configurazioni di zona comuni

### Configurazione 1: Domestico vs Internazionale

**Obiettivo**: Tariffe diverse per spedizioni domestiche rispetto a tutti gli altri paesi.

```
Zona 1: "Domestico"
  Paesi: [Codice del tuo paese]
  Priorità: 50

Zona 2: "Internazionale"
  Paesi: [Lascia vuoto o seleziona tutti gli altri paesi]
  Priorità: 1
```

**Metodi di spedizione**:
- "Spedizione Standard Domestica" → Collegata alla zona Domestica
- "Spedizione Internazionale" → Collegata alla zona Internazionale

---

### Configurazione 2: Internazionale multi-regionale

**Obiettivo**: Tariffe diverse per UE, Nord America, Asia, Resto del mondo.

```
Zona 1: "Unione Europea"
  Paesi: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priorità: 100

Zona 2: "Nord America"
  Paesi: [US, CA, MX]
  Priorità: 100

Zona 3: "Asia Pacifico"
  Paesi: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priorità: 100

Zona 4: "Resto del mondo"
  Paesi: [Lascia vuoto]
  Priorità: 1
```

**Metodi di spedizione**:
- "Spedizione UE" → Zona UE
- "Spedizione Nord America" → Zona Nord America
- "Spedizione Asia Pacifico" → Zona Asia Pacifico
- "Spedizione Internazionale Standard" → Zona Resto del mondo

---

### Configurazione 3: Soprattassa per aree remote

**Obiettivo**: Aggiungi una soprattassa per codici postali remoti all'interno della zona domestica.

```
Zona 1: "Domestico Remoto"
  Paesi: [US]
  Pattern dei codici postali: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Priorità: 100

Zona 2: "Domestico Standard"
  Paesi: [US]
  Priorità: 50
```

**Metodi di spedizione**:
- "Spedizione Remota" → Zona Domestico Remoto (costo più elevato)
- "Spedizione Standard" → Zona Domestico Standard

---

### Configurazione 4: Zone specifiche per stato

**Obiettivo**: Tariffe diverse per ogni regione degli Stati Uniti.

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

Zona 5: "Altri stati degli Stati Uniti"
  Paesi: [US]
  Priorità: 50
```

---

## Esempi di pattern dei codici postali

I codici postali utilizzano **regex** (espressioni regolari) per l'abbinamento dei pattern:

### Stati Uniti (Codici ZIP)

**Formato**: 5 cifre (es. 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canada (Codici postali)

**Formato**: A1A 1A1 (lettera-cifra-lettera spazio cifra-lettera-cifra)

```
Tutti i codici postali canadesi:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$
Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$\nQuebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$\n```

### Regno Unito (Postcodes)

**Formato**: AA1A 1AA o A1A 1AA

```
London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M):                        ^M[0-9]{1,2}
Birmingham (B):                        ^B[0-9]{1,2}
```

### Australia (Postcodes)

**Formato**: 4 cifre (es. 2000)

```
New South Wales (1000-2999):  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### Test dei pattern

**Prima di salvare i pattern**, testali con codici postali noti:

1. Inserisci pattern: `^90[0-9]{3}$`
2. Input di test: "90210" → Dovrebbe corrispondere
3. Input di test: "10001" → Dovrebbe NON corrispondere
4. Input di test: "9021" → Dovrebbe NON corrispondere (solo 4 cifre)

Utilizza testatori online per regex (regex101.com) per validare pattern complessi.

---

## Riepilogo della copertura delle zone

Le zone mostrano un **riepilogo della copertura** nella vista elenco amministratore che mostra cosa è incluso:

**Esempi**:
- "Tutti i paesi" → Nessuna restrizione sui paesi
- "US, CA, MX" → 3 paesi
- "US (CA, OR, WA)" → US con 3 stati
- "US (90xxx-91xxx)" → US con pattern dei codici postali

**Utilizza il riepilogo per**:
- Verificare rapidamente la copertura della zona senza aprirla
- Individuare sovrapposizioni o lacune nella copertura
- Effettuare un'ispezione rapida della configurazione della zona

---

## Collegamento delle zone ai metodi di spedizione

Le zone e i metodi hanno una **relazione molti-a-molti**:

**Dalla parte del metodo** (consigliato):
1. Modifica il metodo di spedizione
2. Scorri fino alla sezione "Zone di spedizione"
3. Seleziona le zone applicabili (selezione multipla)
4. Salva il metodo

**Dalla parte della zona**:
- Le zone non si collegano direttamente ai metodi
- Il collegamento viene sempre effettuato dalla configurazione del metodo

**Comportamento metodo-zona**:

**Nessuna zona collegata** → Metodo disponibile per TUTTI gli indirizzi

**Zone collegate** → Metodo disponibile solo se l'indirizzo del cliente corrisponde a almeno una zona collegata

**Esempio**:
```
Metodo: "Spedizione Standard Domestica"
Zone collegate: ["Domestico USA"]
→ Mostrato solo agli indirizzi degli Stati Uniti

Metodo: "Spedizione Express Internazionale"
Zone collegate: ["UE", "Asia Pacifico", "Resto del mondo"]
→ Mostrato a tutti gli indirizzi non USA
```

---

## Test del matching delle zone

Prima di andare online, testa la configurazione delle zone:

1. **Crea ordini di test**
   - Utilizza indirizzi in diverse zone
   - Verifica che corrispondano correttamente alle zone

2. **Controlla la risoluzione delle priorità**
   - Utilizza un indirizzo che corrisponde a più zone
   - Verifica che la zona con la priorità più alta vinca
   - Conferma che i metodi di spedizione previsti siano visibili

3. **Testa i casi limite**
   - Codici postali di confine (es. 90999 vs 91000)
   - Confini tra stati
   - Indirizzi internazionali con codici postali simili

4. **Utilizza lo strumento di anteprima delle zone** (se disponibile)
   - Inserisci un indirizzo di test
   - Vedi quali zone corrispondono
   - Visualizza la risoluzione delle priorità

---

## Risoluzione dei problemi

**Problema 1: Nessun metodo di spedizione disponibile al momento del checkout**

**Causa**:
- L'indirizzo del cliente non corrisponde a nessuna zona
- Tutti i metodi sono collegati a zone che non corrispondono
- Non esistono metodi senza restrizioni di zona

**Soluzione**:
- Crea una zona fallback (tutti i paesi, priorità 1)
- O rimuovi le restrizioni di zona da almeno un metodo
- Verifica i pattern di paese/stato/codice postale della zona

---

**Problema 2: Abbinamento di zona errato**

**Causa**:
- È selezionata una zona con priorità inferiore nonostante esista una zona con priorità più alta che corrisponde
- Errore di sintassi nei pattern dei codici postali (i pattern falliscono in silenzio)
- Discrepanza tra codici degli stati (CA vs California)

**Soluzione**:
- Verifica i valori di priorità (numero più alto = priorità più alta)
- Testa i pattern dei codici postali con un validatore regex
- Utilizza codici a due lettere per gli stati (CA, non California)

---

**Problema 3: Metodo visualizzato in modo inaspettato**

**Causa**:
- Il metodo non ha zone collegate (disponibile ovunque)
- Più zone corrispondono, ma una zona inaspettata ha una priorità più alta
- La copertura delle zone si sovrappone in modo non intenzionale

**Soluzione**:
- Rivedi le zone collegate al metodo
- Controlla la priorità delle zone corrispondenti
- Effettua un'ispezione del riepilogo della copertura delle zone per sovrapposizioni

---

## Consigli

- **Inizia con 2 zone** - Domestico e Internazionale, espandi quando necessario
- **Utilizza la priorità con saggezza** - Zone specifiche 100, regionali 50, fallback 1
- **Testa i pattern dei codici postali in modo approfondito** - Gli errori regex falliscono in silenzio, causando che le zone non corrispondano
- **Documenta la logica delle zone** - Aggiungi note alla descrizione della zona per spiegare l'intento della copertura
- **Evita troppe zone** - Troppa zone complica la configurazione; utilizza le regole di spedizione per scenari complessi
- **Utilizza codici degli stati, non i nomi** - "CA" non "California", "NY" non "New York"
- **Crea una zona fallback** - Tutti i paesi, priorità 1, assicura che almeno un'opzione di spedizione sia sempre disponibile
- **Monitora le prestazioni delle zone** - Se molti clienti vedono "nessuna spedizione disponibile", ispeziona la copertura delle zone
- **Aggiorna le zone per nuove regioni** - Aggiungi paesi alla zona UE quando nuovi membri si uniscono
- **Utilizza nomi descrittivi** - "UE (Escludendo il Regno Unito)" è meglio di "Zona 3"
- **Testa con indirizzi reali** - Utilizza gli indirizzi reali dei clienti durante i test, non quelli inventati

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.