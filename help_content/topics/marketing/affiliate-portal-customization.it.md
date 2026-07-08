---
title: Personalizzazione del Portale degli Affiliati
---

Il portale degli affiliati di Spwig è la pagina di destinazione pubblica dove i potenziali affiliati apprendono informazioni sul vostro programma e si registrano. Personalizzare questo portale vi permette di allineare i messaggi, il branding e i call-to-action con la posizione unica del vostro negozio. Un portale ben progettato attira affiliati di alta qualità e converte i visitatori in partner attivi.

## Cosa è il Portale degli Affiliati?

Il portale degli affiliati è accessibile all'indirizzo `/affiliate/` nel dominio del vostro negozio. Funziona come:

- **Pagina di scoperta** — Dove i potenziali affiliati apprendono informazioni sulla vostra struttura delle commissioni, sui vantaggi e sui requisiti
- **Punto di accesso per la registrazione** — Modulo di registrazione per nuovi affiliati (registrazione come ospite o basata su account)
- **Gateway di accesso** — Gli affiliati esistenti possono accedere per visualizzare il loro dashboard
- **Mostra del branding** — Riflette l'identità del vostro negozio e la proposta di valore del programma degli affiliati

Il portale è completamente personalizzabile tramite le impostazioni degli affiliati nell'amministrazione, inclusi i messaggi principali, le caratteristiche principali, i flussi passo-passo e le opzioni di registrazione.

![Pagina di destinazione del portale degli affiliati](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Accesso alle Impostazioni

Navigare a **Marketing > Programma degli Affiliati > Impostazioni del Portale** per personalizzare il portale.

Il modello di impostazioni degli affiliati è un **singleton** — avete esattamente un record di impostazioni per l'intero negozio. Tutti i campi sono **traducibili** utilizzando il sistema di traduzione di Spwig, quindi potete personalizzare i messaggi per ogni lingua supportata dal vostro negozio.

## Sezione Hero

La sezione hero è la prima cosa che i potenziali affiliati vedono. Include:

- **Titolo** — Testo principale (es. "Unisciti al Nostro Programma degli Affiliati")
- **Sottotitolo** — Testo di supporto che spiega il valore del programma (es. "Guadagna commissioni promuovendo prodotti premium al tuo pubblico")
- **Statistiche** — Metriche visualizzate automaticamente:
  - Totale programmi attivi
  - Totale affiliati attivi
  - Tasso medio di commissione (calcolato su tutti i programmi attivi)
- **Pulsanti CTA** — Generati automaticamente:
  - **Accedi** — Per gli affiliati esistenti
  - **Diventa un Affiliato** — Attiva il flusso di registrazione

### Personalizzazione del Messaggio Hero

| Campo | Valore Esempio | Scopo |
|-------|--------------|---------|
| **Titolo Hero** | "Unisciti a Noi e Guadagna" | Cattura l'attenzione con un titolo focalizzato sui vantaggi |
| **Sottotitolo Hero** | "Unisciti a 500+ affiliati che guadagnano commissioni competitive su ogni vendita che riferisci" | Fornisci una prova sociale e chiarisci l'offerta |

Le statistiche sono **calcolate automaticamente** e vengono aggiornate in tempo reale in base ai vostri programmi e affiliati attivi. Non è possibile modificare manualmente questi valori.

## Sezione Caratteristiche

La sezione caratteristiche evidenzia **6 carte di vantaggi personalizzabili** che spiegano perché gli affiliati dovrebbero unirsi al vostro programma. Ogni carta di caratteristica contiene:

- **Icona** — Classe di icona FontAwesome (es. `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Titolo** — Titolo del vantaggio (es. "Commissioni Competitive")
- **Descrizione** — Spiegazione di 1-2 frasi (es. "Guadagna fino al 15% su ogni vendita che riferisci")

### Caratteristiche Predefinite

Spwig fornisce caratteristiche predefinite quando installate per la prima volta l'app degli affiliati:

| Icona | Titolo | Descrizione |
|------|-------|-------------|
| `fa-dollar-sign` | Commissioni Competitive | Guadagna commissioni generose su ogni vendita che riferisci |
| `fa-link` | Collegamenti di Tracciamento Facili | Ottieni collegamenti di tracciamento unici che funzionano ovunque |
| `fa-chart-line` | Analisi in Tempo Reale | Traccia clic, conversioni e guadagni nel tuo dashboard |
| `fa-calendar-check` | Pagamenti Affidabili | Ricevi i pagamenti in tempo con PayPal o trasferimento bancario |
| `fa-headset` | Supporto dedicato | Il nostro team è qui per aiutarti a ottenere successo |
| `fa-gift` | Materiali di Marketing | Accedi a banner, immagini e contenuti promozionali |

### Personalizzazione delle Caratteristiche

Le caratteristiche sono salvate come un **array JSON** nel database. Modificale direttamente nel modulo amministrativo:

```json
[
  {
    "icon": "fa-percent",
    "title": "Fino al 20% di Commissione",
    "description": "Guadagna commissioni di settore leader su vendite di prodotti premium"
  },
  {
    "icon": "fa-rocket",
    "title": "Approvazione Rapida",
    "description": "Ottieni l'approvazione in 24 ore e inizia a promuovere immediatamente"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Dashboard Mobile",
    "description": "Gestisci i tuoi collegamenti e traccia i guadagni da qualsiasi dispositivo"
  }
]
```

**Riferimento Icona:** Utilizza qualsiasi classe di icona FontAwesome 5 Free. Esplora le icone su [fontawesome.com/icons](https://fontawesome.com/icons) e usa il nome della classe (es. `fa-trophy`, `fa-users`, `fa-star`).

## Sezione Come Funziona

La sezione "Come Funziona" visualizza un **flusso visivo a 4 passaggi** che spiega il percorso degli affiliati. Ogni passaggio include:

- **Titolo** — Nome del passaggio (es. "Registrati")
- **Descrizione** — Spiegazione di 1-2 frasi di ciò che accade

### Passaggi Predefiniti

| Passaggio | Titolo | Descrizione |
|------|-------|-------------|
| 1 | Registrati | Crea il tuo account affiliato gratuito in pochi minuti |
| 2 | Otteni i Tuoi Collegamenti | Genera collegamenti di tracciamento unici per qualsiasi prodotto o pagina |
| 3 | Promuovi | Condividi i tuoi collegamenti con il tuo pubblico attraverso contenuti, social media o email |
| 4 | Guadagna Commissioni | Ricevi i pagamenti quando i clienti acquistano utilizzando i tuoi collegamenti di riferimento |

### Personalizzazione dei Passaggi

I passaggi sono salvati come un **array JSON**. Puoi modificarli nell'amministrazione:

```json
[
  {
    "title": "Applica per Unirti",
    "description": "Invia la tua candidatura e raccontaci del tuo piattaforma"
  },
  {
    "title": "Ottieni l'Approvazione",
    "description": "Il nostro team esamina la tua candidatura entro 24 ore"
  },
  {
    "title": "Crea Collegamenti",
    "description": "Accedi al tuo dashboard e genera collegamenti di tracciamento immediatamente"
  },
  {
    "title": "Inizia a Guadagnare",
    "description": "Guadagna commissioni su ogni vendita che riferisci — pagamenti mensili tramite PayPal"
  }
]
```

Il flusso visivo numererà automaticamente ogni passaggio (1, 2, 3, 4) sulla pagina di destinazione.

## Sezione CTA

L'ultima sezione prima del modulo di registrazione è la **Sezione CTA (Call-to-Action)**. Fornisce un'ultima spinta per incoraggiare le registrazioni.

| Campo | Valore Esempio | Scopo |
|-------|--------------|---------|
| **Titolo CTA** | "Pronto a Iniziare a Guadagnare?" | Domanda diretta che crea urgenza |
| **Descrizione CTA** | "Unisciti al nostro programma degli affiliati oggi e inizia a guadagnare commissioni su prodotti che già ami e raccomandi." | Rafforza i vantaggi e elimina l'attrito |

La sezione CTA visualizza automaticamente il pulsante **Diventa un Affiliato** sotto il testo.

## Impostazioni di Registrazione

Controlla come i nuovi affiliati si registrano e le informazioni che forniscono.

### Modulo di Registrazione Personalizzato

**Campo:** `custom_form` (ForeignKey al modulo FormBuilder)

Se avete un modulo di registrazione personalizzato creato con lo Spwig Form Builder, selezionatelo qui. Questo vi permette di raccogliere informazioni aggiuntive durante la registrazione (es. URL del sito web, dimensione del pubblico, canali di promozione).

**Lasciare vuoto** per utilizzare il modulo di registrazione predefinito degli affiliati (email, password, dettagli di pagamento).

### Consentire la Registrazione come Ospite

**Campo:** `allow_guest_registration` (Boolean)

- **Selezionato** — I visitatori possono candidarsi senza creare un account Spwig in anticipo
- **Non selezionato** — I visitatori devono accedere o creare un account cliente prima di candidarsi

**Consiglio:** Abilitare la registrazione come ospite per ridurre l'attrito. Potete sempre richiedere l'approvazione per verificare gli affiliati prima di attivarli.

### Richiedere l'Approvazione

**Campo:** `require_approval` (Boolean)

- **Selezionato** — I nuovi affiliati devono attendere l'approvazione manuale prima di accedere al loro dashboard
- **Non selezionato** — I nuovi affiliati vengono approvati automaticamente e possono creare collegamenti immediatamente

**Consiglio:** Abilitare l'approvazione manuale se volete verificare gli affiliati per aderenza al brand, prevenzione frodi o programmi esclusivi.

### URL delle Condizioni di Utilizzo

**Campo:** `terms_url` (URL)

Link opzionale alle condizioni di utilizzo del vostro programma degli affiliati. Se fornito, il modulo di registrazione visualizza una casella di spunta che richiede agli affiliati di accettare le vostre condizioni prima di registrarsi.

**Esempio:** `/pages/affiliate-terms/`

### Messaggio di Benvenuto

**Campo:** `welcome_message` (Testo)

Messaggio visualizzato agli affiliati immediatamente dopo la registrazione riuscita. Utilizzalo per:

- Ringraziarli per l'adesione
- Spiegare i passaggi successivi (es. "Verificheremo la tua candidatura entro 24 ore")
- Collegare a risorse per l'avvio

**Esempio:*
```
Benvenuto nel nostro programma degli affiliati! Abbiamo ricevuto la tua candidatura e la verificheremo entro 24 ore. Controlla la tua email per la conferma dell'approvazione e le istruzioni per l'accesso.
```

## Supporto Multilingua

Tutti i campi di testo nelle Impostazioni degli Affiliati sono **traducibili** utilizzando il widget di traduzione di Spwig:

- Titolo Hero
- Sottotitolo Hero
- Caratteristiche (JSON tradotto per ogni lingua)
- Passaggi di Come Funziona (JSON tradotto per ogni lingua)
- Titolo CTA
- Descrizione CTA
- Messaggio di Benvenuto

### Come Funziona la Traduzione

Quando modifichi un campo traducibile, vedrai un widget di traduzione che ti permette di fornire contenuti per ogni lingua abilitata. Per i campi JSON (caratteristiche, passaggi), fornisci oggetti JSON separati per ogni lingua:

**Inglese:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**Spagnolo:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

Il portale visualizzerà automaticamente la versione della lingua corretta in base alla preferenza linguistica del visitatore.

## Anteprima delle Modifiche

Dopo aver personalizzato le impostazioni del portale:

1. **Salva** le tue modifiche nell'amministrazione
2. Visita `/affiliate/` sul frontend del vostro negozio (apri in una nuova scheda)
3. **Testa il flusso di registrazione** cliccando su "Diventa un Affiliato"
4. **Verifica la coerenza del branding** — il portale corrisponde al design e ai messaggi del vostro negozio?

Puoi apportare modifiche iterative e aggiornare la pagina per vedere gli aggiornamenti immediatamente.

## Esempi di Personalizzazioni

### Scenario 1: Negozio di Abbigliamento Online

**Obiettivo:** Recrutare influencer e blogger del settore moda.

| Impostazione | Valore |
|---------|-------|
| Titolo Hero | "Promuovi gli Stili che Ti Piacciono e Guadagna" |
| Sottotitolo Hero | "Unisciti a 1.200+ influencer che guadagnano il 12% di commissioni su ogni vendita" |
| Caratteristica 1 | Icona: `fa-tshirt`, Titolo: "Collezioni di Moda Selezionate", Descrizione: "Promuovi abbigliamento premium e accessori" |
| Caratteristica 2 | Icona: `fa-percentage`, Titolo: "12% di Commissione", Descrizione: "Tariffe di settore leader su tutti i prodotti" |
| Caratteristica 3 | Icona: `fa-camera`, Titolo: "Contenuti Esclusivi", Descrizione: "Accedi a foto, video e asset di campagna dei prodotti" |
| Consentire la Registrazione come Ospite | Selezionato |
| Richiedere l'Approvazione | Selezionato (revisione manuale per aderenza al brand) |

### Scenario 2: Programma di Partner per SaaS B2B

**Obiettivo:** Recrutare consulenti e agenzie per riferimenti di software per aziende.

| Impostazione | Valore |
|---------|-------|
| Titolo Hero | "Unisciti a Noi per Crescere i Guadagni" |
| Sottotitolo Hero | "Guadagna $500 per ogni riferimento aziendale attraverso il nostro programma di partner B2B" |
| Caratteristica 1 | Icona: `fa-handshake`, Titolo: "$500 per Riferimento", Descrizione: "Commissione fissa per lead aziendali qualificati" |
| Caratteristica 2 | Icona: `fa-clock`, Titolo: "Cookie di 180 Giorni", Descrizione: "Finestra di attribuzione lunga per cicli di vendita complessi" |
| Caratteristica 3 | Icona: `fa-user-tie`, Titolo: "Gestore Partner dedicato", Descrizione: "Supporto white-glove per i vostri clienti" |
| Consentire la Registrazione come Ospite | Non selezionato (B2B richiede account) |
| Richiedere l'Approvazione | Selezionato (programma a invito) |
| URL delle Condizioni | `/pages/partner-program-terms/` |

## Consigli

- Personalizza il **titolo hero** per concentrarti sui vantaggi, non sulle caratteristiche — "Guadagna Mentre Dormi" è più convincente di "Registrazione al Programma degli Affiliati"
- Utilizza **prova sociale** nel sottotitolo (es. "Unisciti a 500+ affiliati") per costruire fiducia e credibilità
- Scegli **icona FontAwesome** che rafforzino visivamente ogni vantaggio — l'icona deve comunicare immediatamente il valore
- Mantieni le descrizioni delle caratteristiche a **1-2 frasi** — il portale è per la conversione, non per spiegazioni esaustive
- Testa il **flusso di registrazione** da solo prima di promuovere il portale — individua i punti di attrito come campi del modulo confusi o collegamenti rotti
- Abilita la **registrazione come ospite** per ridurre l'attrito di registrazione, quindi utilizza **richiedi approvazione** per verificare gli affiliati dopo che hanno inviato la candidatura
- Utilizza il **messaggio di benvenuto** per stabilire aspettative (tempo di approvazione, passaggi successivi, contatto di supporto) e ridurre le richieste di supporto
- Aggiorna il portale **stacionalmente** per allinearlo a campagne — evidenzia promozioni di commissioni speciali o lanci di prodotti

Ricorda: Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.